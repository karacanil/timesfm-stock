import copy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from trader import data
from trader.backtest import pass_bar, simulate, statistics, trend_strategy, week_ends
from trader.cli import freeze_policy, run_backtest
from trader.strategy import target_weights, trend_on

POLICY = json.loads(Path('trader_policy_v1.json').read_text())


def synthetic(symbols, sessions=900, seed=0, start='2004-01-02'):
    rng = np.random.default_rng(seed)
    index = pd.bdate_range(start, periods=sessions)
    drift = np.linspace(-0.0004, 0.0006, len(symbols))
    returns = rng.normal(drift, 0.01, size=(sessions, len(symbols)))
    closes = pd.DataFrame(100 * np.exp(np.cumsum(returns, axis=0)), index=index, columns=symbols)
    opens = closes.shift(1).fillna(closes.iloc[0]) * (1 + rng.normal(0, 0.002, size=closes.shape))
    return opens, closes


def small_policy(start):
    policy = copy.deepcopy(POLICY)
    policy['backtest_start'] = start
    return policy


class StrategyTests(unittest.TestCase):
    def test_signal_uses_no_future_data(self):
        _, closes = synthetic(['A', 'B', 'C'])
        full = trend_on(closes)
        for t in [300, 500, 899]:
            np.testing.assert_array_equal(trend_on(closes.iloc[:t + 1]).iloc[t].to_numpy(), full.iloc[t].to_numpy())

    def test_signal_off_without_enough_history(self):
        _, closes = synthetic(['A'], sessions=260)
        self.assertFalse(trend_on(closes).iloc[:252].any().any())

    def test_target_weights_respect_caps_and_off_assets(self):
        _, closes = synthetic(['A', 'B', 'C', 'D'], sessions=61)
        weights = target_weights(closes, {'A': True, 'B': True, 'C': False, 'D': True},
                                 target_vol=1.0, max_gross=1.0, max_weight=0.3)
        self.assertEqual(weights['C'], 0.0)
        self.assertTrue((weights <= 0.3 + 1e-12).all())
        self.assertLessEqual(weights.sum(), 1.0 + 1e-12)

    def test_target_weights_scale_down_to_volatility_target(self):
        _, closes = synthetic(['A', 'B'], sessions=61)
        weights = target_weights(closes, {'A': True, 'B': True}, target_vol=0.02, max_weight=1.0)
        returns = np.log(closes).diff().iloc[1:]
        realized = float(np.sqrt(weights.to_numpy() @ (returns.cov().to_numpy() * 252) @ weights.to_numpy()))
        self.assertAlmostEqual(realized, 0.02, places=6)

    def test_all_off_means_all_cash(self):
        _, closes = synthetic(['A', 'B'], sessions=61)
        self.assertEqual(target_weights(closes, {'A': False, 'B': False}).sum(), 0.0)

    def test_week_end_moves_to_thursday_on_friday_holiday(self):
        index = pd.DatetimeIndex(['2026-11-23', '2026-11-24', '2026-11-25', '2026-11-26', '2026-11-30'])
        self.assertIn(pd.Timestamp('2026-11-26'), week_ends(index))
        self.assertNotIn(pd.Timestamp('2026-11-25'), week_ends(index))


class SimulationTests(unittest.TestCase):
    def setUp(self):
        index = pd.bdate_range('2020-01-06', periods=4)
        self.closes = pd.DataFrame({'A': [100., 110., 121., 121.]}, index=index)
        self.opens = pd.DataFrame({'A': [100., 105., 115., 120.]}, index=index)
        self.cash = pd.Series(0.0, index=index)

    def test_fills_at_next_open_with_costs(self):
        decide = lambda i: pd.Series({'A': 1.0}) if i == 0 else None
        equity, trades = simulate(self.opens, self.closes, self.cash, '2020-01-06', decide, cost_bps=10)
        self.assertEqual(equity.iloc[0], 1.0)  # Nothing happens on the decision day.
        shares = 1.0 / 105
        self.assertAlmostEqual(equity.iloc[1], shares * 110 - 0.001)
        self.assertAlmostEqual(trades['cost'].iloc[0], 0.001)
        self.assertEqual(trades['date'].iloc[0], '2020-01-07')

    def test_small_trades_skipped_but_exits_allowed(self):
        targets = {0: pd.Series({'A': 0.5}), 1: pd.Series({'A': 0.51}), 2: pd.Series({'A': 0.0})}
        equity, trades = simulate(self.opens, self.closes, self.cash, '2020-01-06', targets.get, 0, min_trade=0.02)
        self.assertEqual(list(trades['date']), ['2020-01-07', '2020-01-09'])
        self.assertLess(trades['weight_change'].iloc[-1], 0)

    def test_cash_accrues_interest(self):
        cash = pd.Series(0.001, index=self.closes.index)
        equity, _ = simulate(self.opens, self.closes, cash, '2020-01-06', lambda i: None, 0)
        self.assertAlmostEqual(equity.iloc[-1], 1.001 ** 3)

    def test_future_prices_do_not_change_past_decisions_or_equity(self):
        opens, closes = synthetic(['SPY', 'B', 'C'], sessions=700)
        cash = pd.Series(0.0001, index=closes.index)
        policy = small_policy('2005-03-01')
        equity, _, decisions = trend_strategy(opens, closes, cash, policy)
        cut = 600
        shocked_closes, shocked_opens = closes.copy(), opens.copy()
        shocked_closes.iloc[cut + 1:] *= 3.0
        shocked_opens.iloc[cut + 1:] *= 3.0
        shocked_equity, _, shocked_decisions = trend_strategy(shocked_opens, shocked_closes, cash, policy)
        day = closes.index[cut]
        pd.testing.assert_series_equal(equity[:day], shocked_equity[:day])
        pd.testing.assert_frame_equal(decisions[decisions.index <= day.date().isoformat()],
                                      shocked_decisions[shocked_decisions.index <= day.date().isoformat()])


class StatisticsTests(unittest.TestCase):
    def test_drawdown_and_cagr(self):
        index = pd.date_range('2020-01-01', '2021-01-01', freq='D')
        path = np.interp(np.arange(len(index)), [0, 182, len(index) - 1], [1.0, 0.5, 1.21])
        equity = pd.Series(path, index=index)
        stats = statistics(equity, pd.Series(0.0, index=index))
        self.assertAlmostEqual(stats['max_drawdown_pct'], -50.0)
        self.assertAlmostEqual(stats['cagr_pct'], 100 * (1.21 ** (365.25 / 366) - 1), places=6)

    def test_pass_bar_requires_every_check(self):
        good = {'max_drawdown_pct': -15, 'sharpe': 0.7, 'cagr_by_third_pct': [3, 4, 5], 'annual_cost_drag_pct': 0.2}
        spy = {'max_drawdown_pct': -55, 'sharpe': 0.6}
        mix = {'max_drawdown_pct': -30, 'sharpe': 0.6}
        self.assertEqual(pass_bar(good, spy, mix, good, POLICY)['verdict'], 'PROCEED')
        bad = dict(good, cagr_by_third_pct=[3, -1, 5])
        self.assertEqual(pass_bar(bad, spy, mix, good, POLICY)['verdict'], 'RETHINK')


class EndToEndTests(unittest.TestCase):
    def test_policy_cannot_change_after_freeze(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy_path = Path(tmp) / 'policy.json'
            policy_path.write_text(json.dumps(POLICY))
            freeze_policy(policy_path, Path(tmp) / 'out')
            changed = dict(POLICY, universe=['SPY'])
            policy_path.write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                freeze_policy(policy_path, Path(tmp) / 'out')

    def test_offline_backtest_writes_report(self):
        symbols = POLICY['universe']
        opens, closes = synthetic(symbols, sessions=1000, seed=3, start='2003-01-01')

        def fetch(symbol, start):
            if symbol.startswith('^'):
                return pd.DataFrame({'Open': 4.0, 'Close': 4.0}, index=closes.index)
            return pd.DataFrame({'Open': opens[symbol], 'Close': closes[symbol]})

        with tempfile.TemporaryDirectory() as tmp:
            policy = small_policy('2004-06-01')
            summary = run_backtest(policy, Path(tmp), Path(tmp) / 'cache', fetch=fetch)
            self.assertIn(summary['pass_bar']['verdict'], {'PROCEED', 'RETHINK'})
            for name in ['report.md', 'summary.json', 'equity.csv', 'trades.csv', 'weekly_targets.csv']:
                self.assertTrue((Path(tmp) / 'backtest' / name).exists())
            # Second run reads the cache instead of fetching again.
            run_backtest(policy, Path(tmp), Path(tmp) / 'cache', fetch=None)

    def test_panel_keeps_pre_inception_empty(self):
        index = pd.bdate_range('2020-01-01', periods=5)
        frames = {'SPY': pd.DataFrame({'Open': 1.0, 'Close': 1.0}, index=index),
                  'NEW': pd.DataFrame({'Open': 2.0, 'Close': 2.0}, index=index[2:])}
        opens, closes, filled = data.panel(frames, ['SPY', 'NEW'])
        self.assertTrue(closes['NEW'].iloc[:2].isna().all())
        self.assertEqual(filled['NEW'], 0)


if __name__ == '__main__':
    unittest.main()
