import copy
import json
from pathlib import Path
import tempfile
import unittest

import exchange_calendars as xcals
import numpy as np
import pandas as pd

from trader import paper
from trader.broker import SimulatedBroker
from trader.ledger import Ledger

POLICY = json.loads(Path('trader_policy_v2.json').read_text())
CONFIG = json.loads(Path('paper_config.json').read_text())
SESSIONS = xcals.get_calendar('XNYS', start='2003-01-01', end='2026-12-31').sessions
SESSIONS = SESSIONS[SESSIONS <= '2026-11-20']

# After Oct 30 (a month end) closes; orders fill at the Nov 2 open.
AFTER_MONTH_END = '2026-10-31T01:00:00Z'


def make_fetch(drop_last_for=None, through='2026-11-20'):
    def fetch(symbol, start):
        index = SESSIONS[SESSIONS <= through]
        i = np.arange(len(index))
        base = 50 + 10 * POLICY['universe'].index(symbol)
        close = base * np.exp(0.0004 * i + 0.01 * np.sin(i / 7))
        frame = pd.DataFrame({'Open': close * 0.995, 'Close': close, 'Adj Close': close,
                              'Dividends': 0.0, 'Stock Splits': 0.0}, index=pd.DatetimeIndex(index))
        if symbol == drop_last_for:
            frame = frame.iloc[:-1]
        return frame
    return fetch


class PaperRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'paper'
        self.config = dict(CONFIG, halt_file=str(Path(self.tmp.name) / 'HALT'))

    def tearDown(self):
        self.tmp.cleanup()

    def run_at(self, now, fetch=None):
        return paper.run(self.config, POLICY, self.root, now=now, fetch=fetch or make_fetch(through=now[:10]))

    def broker(self):
        return json.loads((self.root / 'broker_state.json').read_text())

    def test_month_end_decides_once_and_orders_are_idempotent(self):
        self.run_at(AFTER_MONTH_END)
        ledger = Ledger(self.root)
        decision = ledger.get('decisions', '2026-10-30')
        orders = ledger.get('orders', '2026-10-30')
        self.assertEqual(decision['fill_date'], '2026-11-02')
        self.assertTrue(orders)
        self.assertTrue(all(o['side'] == 'buy' and o['qty'] == int(o['qty']) for o in orders))
        self.assertLessEqual(sum(decision['target_weights'].values()), 1 + 1e-9)
        self.run_at('2026-10-31T09:00:00Z')  # Backup run the same night.
        self.assertEqual(len(self.broker()['pending']), len(orders))
        self.assertEqual(len(set(self.broker()['known_ids'])), len(orders))

    def test_fills_at_next_open_and_reconciles(self):
        self.run_at(AFTER_MONTH_END)
        self.run_at('2026-11-03T02:00:00Z')
        ledger = Ledger(self.root)
        events = ledger.get('events', '2026-11-02')
        bars = make_fetch()(events[0]['symbol'], None)
        expected = bars.at[pd.Timestamp('2026-11-02'), 'Open'] * 1.0005
        self.assertAlmostEqual(events[0]['price'], expected)
        snapshot = ledger.get('daily', '2026-11-02')
        self.assertTrue(snapshot['positions'])
        self.assertGreater(snapshot['cash'], 0)
        self.assertEqual(self.broker()['pending'], [])

    def test_no_trade_before_first_month_end_after_start(self):
        self.run_at('2026-11-05T02:00:00Z')
        self.assertEqual(Ledger(self.root).all('decisions'), [])
        self.assertTrue((self.root / 'report.md').exists())

    def test_late_run_within_lag_still_rebalances(self):
        self.run_at('2026-10-21T02:00:00Z')  # Account opens mid-October.
        self.run_at('2026-11-04T02:00:00Z')  # Oct 30 decision filled two sessions late.
        decision = Ledger(self.root).get('decisions', '2026-10-30')
        self.assertEqual(decision['fill_date'], '2026-11-04')
        self.assertEqual(decision['fill_lag_sessions'], 2)

    def test_too_late_rebalance_is_skipped(self):
        self.run_at('2026-10-21T02:00:00Z')
        log = self.run_at('2026-11-12T02:00:00Z')
        self.assertFalse(Ledger(self.root).exists('decisions', '2026-10-30'))
        self.assertTrue(any('missed' in line for line in log))

    def test_halt_file_blocks_decision_but_writes_report(self):
        Path(self.config['halt_file']).write_text('stop')
        with self.assertRaises(paper.Halt):
            self.run_at(AFTER_MONTH_END)
        self.assertFalse(Ledger(self.root).exists('decisions', '2026-10-30'))
        self.assertIn('HALTED', (self.root / 'report.md').read_text())

    def test_stale_data_halts_before_anything_trades(self):
        with self.assertRaises(paper.Halt):
            self.run_at(AFTER_MONTH_END, make_fetch(drop_last_for='GLD', through='2026-10-30'))
        self.assertFalse(Ledger(self.root).exists('decisions', '2026-10-30'))

    def test_partial_bar_for_today_is_ignored(self):
        # During the Nov 2 session Yahoo already shows a Nov 2 bar; the latest completed session is Oct 30.
        self.run_at('2026-11-02T16:00:00Z', make_fetch(through='2026-11-02'))
        self.assertTrue(Ledger(self.root).exists('daily', '2026-10-30'))
        self.assertFalse(Ledger(self.root).exists('daily', '2026-11-02'))

    def test_broker_ledger_mismatch_halts(self):
        self.run_at(AFTER_MONTH_END)
        state = self.broker()
        state['cash'] += 500
        (self.root / 'broker_state.json').write_text(json.dumps(state))
        with self.assertRaises(paper.Halt):
            self.run_at('2026-10-31T09:00:00Z')

    def test_changed_config_rejected(self):
        self.run_at(AFTER_MONTH_END)
        self.config['starting_cash'] = 5
        with self.assertRaises(ValueError):
            self.run_at('2026-10-31T09:00:00Z')


class OrderPlanTests(unittest.TestCase):
    prices = {s: 100.0 for s in POLICY['universe']}

    def plan(self, targets, positions=None, cash=100_000, previous=None, config=None):
        return paper.plan_orders(POLICY, config or CONFIG, targets, cash, positions or {}, self.prices,
                                 previous or self.prices, '2026-10-30')

    def test_whole_shares_and_cash_buffer(self):
        orders, _ = self.plan({'SPY': 0.25, 'TLT': 0.2})
        quantities = {o['symbol']: o['qty'] for o in orders}
        self.assertEqual(quantities, {'SPY': 245, 'TLT': 196})
        self.assertEqual(orders[0]['client_order_id'], 'tp-v2-2026-10-30-SPY')

    def test_small_change_skipped_but_full_exit_kept(self):
        orders, _ = self.plan({'SPY': 0.25, 'TLT': 0.0}, positions={'SPY': 240, 'TLT': 10}, cash=75_000)
        self.assertEqual([(o['symbol'], o['side']) for o in orders], [('TLT', 'sell')])

    def test_oversized_order_halts(self):
        with self.assertRaises(paper.Halt):
            self.plan({'SPY': 0.6})

    def test_suspicious_price_move_halts(self):
        previous = dict(self.prices, SPY=50.0)
        with self.assertRaises(paper.Halt):
            self.plan({'SPY': 0.25}, previous=previous)


class SimulatedBrokerTests(unittest.TestCase):
    def test_dividends_splits_and_cash_limited_buys(self):
        with tempfile.TemporaryDirectory() as tmp:
            broker = SimulatedBroker(Path(tmp) / 's.json', 1000, commission_bps=0, slippage_bps=0)
            broker.state['positions'] = {'A': 10}
            index = pd.DatetimeIndex(['2026-11-02', '2026-11-03'])
            bars = {'A': pd.DataFrame({'Open': [50., 25.], 'Close': [50., 25.], 'Dividends': [1.0, 0.],
                                       'Stock Splits': [0., 2.]}, index=index)}
            broker.submit([{'client_order_id': 'x', 'symbol': 'A', 'side': 'buy', 'qty': 1000,
                            'fill_date': '2026-11-03'}])
            broker.submit([{'client_order_id': 'x', 'symbol': 'A', 'side': 'buy', 'qty': 1000,
                            'fill_date': '2026-11-03'}])
            events = broker.settle(bars, index)
            self.assertEqual(len(broker.state['pending']), 0)
            self.assertEqual(events['2026-11-02'], [{'type': 'dividend', 'symbol': 'A', 'per_share': 1.0, 'amount': 10.0}])
            fill = [e for e in events['2026-11-03'] if e['type'] == 'fill'][0]
            self.assertEqual(fill['qty'], 40)  # $1,010 cash buys 40 shares at $25.
            self.assertEqual(broker.state['positions']['A'], 20 + 40)
            self.assertEqual(broker.settle(bars, index), {})  # Already processed.


if __name__ == '__main__':
    unittest.main()
