"""Daily backtest: decide at a session's close, trade at the next session's open, pay costs."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .strategy import target_weights, trend_on


def week_ends(index):
    """Last session of each calendar week (Friday, or earlier when Friday is a holiday)."""
    weeks = pd.Series(index.to_period("W"), index=index)
    return set(index[(weeks != weeks.shift(-1)).to_numpy()])


def month_ends(index):
    months = pd.Series(index.to_period("M"), index=index)
    return set(index[(months != months.shift(-1)).to_numpy()])


def simulate(opens, closes, cash_daily, start, decide, cost_bps, min_trade=0.0):
    """Run one portfolio from equity 1.0 at the close of the first session >= start.

    decide(i) returns target weights (Series) using information up to session i, or None.
    Targets fill at session i+1's open. Trades smaller than min_trade (as a weight) are skipped,
    except full exits to zero, so small leftover positions can always be closed.
    """
    index = closes.index
    first = int(index.searchsorted(pd.Timestamp(start)))
    shares = pd.Series(0.0, index=closes.columns)
    cash, pending = 1.0, None
    equity, trades = [], []
    cost_rate = cost_bps / 10_000
    for i in range(first, len(index)):
        day = index[i]
        if i > first:
            cash *= 1 + cash_daily.iloc[i - 1]
        if pending is not None:
            open_px = opens.iloc[i].fillna(closes.iloc[i - 1])
            held = shares * open_px.fillna(0.0)
            equity_open = cash + held.sum()
            current = held / equity_open
            for symbol, target in pending.items():
                delta = target - current[symbol]
                if abs(delta) < 1e-12 or (abs(delta) < min_trade and target > 0):
                    continue
                notional = delta * equity_open
                cost = abs(notional) * cost_rate
                shares[symbol] += notional / open_px[symbol]
                cash -= notional + cost
                trades.append({"date": day.date().isoformat(), "symbol": symbol,
                               "weight_change": float(delta), "notional": float(notional),
                               "cost": float(cost), "equity": float(equity_open)})
            pending = None
        value = cash + float((shares * closes.iloc[i].fillna(0.0)).sum())
        equity.append(value)
        if i + 1 < len(index):
            targets = decide(i)
            if targets is not None:
                pending = targets.reindex(closes.columns).fillna(0.0)
    return pd.Series(equity, index=index[first:]), pd.DataFrame(trades)


def trend_strategy(opens, closes, cash_daily, policy, cost_multiplier=1.0):
    signal, portfolio, execution = policy["signal"], policy["portfolio"], policy["execution"]
    on = trend_on(closes, signal["momentum_lookback_sessions"], signal["momentum_skip_sessions"],
                  signal["sma_sessions"])
    rebalance = week_ends(closes.index)
    window = portfolio["volatility_lookback_sessions"] + 1
    decisions = {}

    def decide(i):
        day = closes.index[i]
        if day not in rebalance or i + 1 < window:
            return None
        weights = target_weights(closes.iloc[i + 1 - window:i + 1], on.iloc[i].to_dict(),
                                 portfolio["target_volatility"], portfolio["max_gross_exposure"],
                                 portfolio["max_weight"])
        decisions[day.date().isoformat()] = weights
        return weights

    cost = (execution["commission_bps"] + execution["slippage_bps"]) * cost_multiplier
    equity, trades = simulate(opens, closes, cash_daily, policy["backtest_start"], decide, cost,
                              execution["min_trade_weight"])
    return equity, trades, pd.DataFrame(decisions).T


def fixed_mix(opens, closes, cash_daily, policy, weights, monthly):
    """Benchmark: buy the mix once, optionally rebalance at each month end. Same costs."""
    target = pd.Series(weights, dtype=float)
    first = int(closes.index.searchsorted(pd.Timestamp(policy["backtest_start"])))
    rebalance = month_ends(closes.index)
    execution = policy["execution"]

    def decide(i):
        if i == first or (monthly and closes.index[i] in rebalance):
            return target
        return None

    equity, trades = simulate(opens, closes, cash_daily, policy["backtest_start"], decide,
                              execution["commission_bps"] + execution["slippage_bps"])
    return equity, trades


def statistics(equity, cash_daily, trades=None):
    returns = equity.pct_change().dropna()
    excess = returns - cash_daily.reindex(returns.index).shift(1).fillna(0.0)
    years = (equity.index[-1] - equity.index[0]).days / 365.25
    drawdown = equity / equity.cummax() - 1
    yearly = equity.groupby(equity.index.year).last()
    yearly_returns = yearly.pct_change()
    yearly_returns.iloc[0] = yearly.iloc[0] / equity.iloc[0] - 1
    thirds = np.array_split(np.arange(len(equity)), 3)
    stats = {
        "start": equity.index[0].date().isoformat(), "end": equity.index[-1].date().isoformat(),
        "final_multiple": float(equity.iloc[-1] / equity.iloc[0]),
        "cagr_pct": 100 * float((equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1),
        "volatility_pct": 100 * float(returns.std() * np.sqrt(252)),
        "sharpe": float(excess.mean() / excess.std() * np.sqrt(252)) if excess.std() > 0 else None,
        "max_drawdown_pct": 100 * float(drawdown.min()),
        "max_drawdown_date": drawdown.idxmin().date().isoformat(),
        "worst_year": int(yearly_returns.idxmin()), "worst_year_pct": 100 * float(yearly_returns.min()),
        "cagr_by_third_pct": [],
        "calendar_year_pct": {int(y): 100 * float(r) for y, r in yearly_returns.items()},
    }
    for part in thirds:
        segment = equity.iloc[part]
        span = (segment.index[-1] - segment.index[0]).days / 365.25
        stats["cagr_by_third_pct"].append(100 * float((segment.iloc[-1] / segment.iloc[0]) ** (1 / span) - 1))
    if trades is not None and len(trades):
        stats["annual_turnover_pct"] = 100 * float((trades["notional"].abs() / trades["equity"]).sum() / years)
        stats["annual_cost_drag_pct"] = 100 * float((trades["cost"] / trades["equity"]).sum() / years)
    return stats


def pass_bar(strategy, spy, sixty_forty, doubled, policy):
    bar = policy["pass_bar"]
    sharpe_floor = spy["sharpe"] - bar["sharpe_vs_spy_tolerance"]
    checks = {
        "max_drawdown_better_than_spy_and_60_40":
            strategy["max_drawdown_pct"] > max(spy["max_drawdown_pct"], sixty_forty["max_drawdown_pct"]),
        "max_drawdown_above_floor": strategy["max_drawdown_pct"] >= bar["max_drawdown_floor_pct"],
        "sharpe_within_tolerance_of_spy": strategy["sharpe"] >= sharpe_floor,
        "positive_cagr_each_third": all(x > 0 for x in strategy["cagr_by_third_pct"]),
        "cost_drag_within_limit": strategy["annual_cost_drag_pct"] <= bar["max_annual_cost_drag_pct"],
        "doubled_costs_still_meets_sharpe_bar": doubled["sharpe"] >= sharpe_floor,
    }
    return {"verdict": "PROCEED" if all(checks.values()) else "RETHINK",
            "sharpe_floor": sharpe_floor, "checks": checks}
