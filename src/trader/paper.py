"""One paper-trading run: settle -> reconcile -> daily snapshot -> month-end rebalance -> report.

Safe to run several times a day: every step is keyed by session date and recorded once.
Trading decisions use the same strategy functions as the backtest; no LLM is involved.
"""
from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np
import pandas as pd

from . import data
from .broker import SimulatedBroker
from .ledger import Ledger
from .sessions import Sessions
from .strategy import target_weights, trend_on


class Halt(RuntimeError):
    """Stop before trading; the workflow fails visibly and nothing is submitted."""


def halted(config):
    return Path(config["halt_file"]).exists() or os.environ.get("TRADER_HALT", "").strip() not in {"", "0"}


def fetch_bars(symbols, start, latest, fetch):
    """Download bars, drop anything after the last completed session (Yahoo shows today's
    partial bar during market hours), and refuse stale or broken data."""
    bars = {}
    for symbol in symbols:
        frame = fetch(symbol, start)
        frame = frame[frame.index <= latest]
        if frame.empty or frame.index[-1] != latest:
            last = None if frame.empty else frame.index[-1].date().isoformat()
            raise Halt(f"Stale data for {symbol}: latest bar {last}, expected {latest.date().isoformat()}")
        if not np.isfinite(frame[["Open", "Close", "Adj Close"]].iloc[-1]).all() or (frame[["Open", "Close"]].iloc[-1] <= 0).any():
            raise Halt(f"Invalid latest prices for {symbol}")
        bars[symbol] = frame
    return bars


def plan_orders(policy, config, targets, cash, positions, prices, previous, month_end):
    equity = cash + sum(q * prices[s] for s, q in positions.items())
    investable = equity * (1 - config["cash_buffer"])
    orders = []
    for symbol in policy["universe"]:
        price = prices[symbol]
        move = abs(price / previous[symbol] - 1)
        current = positions.get(symbol, 0)
        target = math.floor(targets.get(symbol, 0.0) * investable / price)
        delta = target - current
        if delta == 0:
            continue
        weight_change = abs(delta) * price / equity
        if weight_change < policy["execution"]["min_trade_weight"] and target > 0:
            continue
        if move > config["max_daily_move"]:
            raise Halt(f"{symbol} moved {move:.0%} on the decision day; check the data before trading")
        if weight_change > config["max_order_fraction"]:
            raise Halt(f"{symbol} order is {weight_change:.0%} of equity, above the {config['max_order_fraction']:.0%} limit")
        orders.append({"client_order_id": f"tp-v{policy['version']}-{month_end}-{symbol}", "symbol": symbol,
                       "side": "buy" if delta > 0 else "sell", "qty": abs(delta), "type": "market",
                       "time_in_force": "opg", "reference_price": price})
    if len(orders) > config["max_orders"]:
        raise Halt(f"{len(orders)} orders exceed the limit of {config['max_orders']}")
    return orders, equity


def decide(policy, bars, month_end):
    """Target weights from adjusted closes up to and including the month-end session."""
    closes = pd.DataFrame({s: bars[s]["Adj Close"] for s in policy["universe"]})
    closes = closes[closes.index <= month_end]
    signal, portfolio = policy["signal"], policy["portfolio"]
    on = trend_on(closes, signal["momentum_lookback_sessions"], signal["momentum_skip_sessions"], signal["sma_sessions"])
    window = closes.iloc[-(portfolio["volatility_lookback_sessions"] + 1):]
    weights = target_weights(window, on.iloc[-1].to_dict(), portfolio["target_volatility"],
                             portfolio["max_gross_exposure"], portfolio["max_weight"])
    return weights, on.iloc[-1]


def run(config, policy, root, now=None, fetch=data.yahoo_full):
    now = pd.Timestamp(now) if now is not None else pd.Timestamp.now(tz="UTC")
    ledger = Ledger(root)
    sessions = Sessions(config["calendar"], now, config["close_delay_minutes"])
    latest = sessions.latest
    if not ledger.exists("account"):
        ledger.put("account", {"created_at": now.isoformat(), "first_session": latest.date().isoformat(),
                               "starting_cash": config["starting_cash"], "broker": config["broker"],
                               "config": config, "policy": policy})
    account = ledger.get("account")
    if account["config"] != config or account["policy"] != policy:
        raise ValueError("Paper config or policy changed; start a new account directory instead")
    if config["broker"] != "simulated":
        raise ValueError("Only the simulated broker exists so far")
    execution = policy["execution"]
    broker = SimulatedBroker(Path(root) / "broker_state.json", config["starting_cash"],
                             execution["commission_bps"], execution["slippage_bps"])
    log, halt_reason = [], None

    bars = fetch_bars(policy["universe"], policy["data_start"], latest, fetch)

    # 1. Settle fills, dividends and splits through the latest completed session.
    for day, events in broker.settle(bars, sessions.completed).items():
        ledger.put("events", events, day)
        log.append(f"{day}: recorded {len(events)} broker events")
    broker.save()

    # 2. Reconcile the broker with the ledger. Any difference stops trading.
    cash, positions = broker.holdings()
    expected_cash, expected_positions = ledger.expected_holdings()
    if abs(cash - expected_cash) > 0.01 or set(positions) != set(expected_positions) or \
            any(abs(positions[s] - expected_positions[s]) > 1e-6 for s in positions):
        raise Halt(f"Broker and ledger disagree: broker {cash:.2f} {positions}, ledger {expected_cash:.2f} {expected_positions}")

    # 3. Daily snapshot at the latest close.
    day = latest.date().isoformat()
    prices = {s: float(bars[s]["Close"].iloc[-1]) for s in policy["universe"]}
    if not ledger.exists("daily", day):
        equity = cash + sum(q * prices[s] for s, q in positions.items())
        ledger.put("daily", {"date": day, "recorded_at": now.isoformat(), "cash": cash, "positions": positions,
                             "closes": {s: prices[s] for s in positions}, "equity": equity,
                             "spy_adjusted_close": float(bars["SPY"]["Adj Close"].iloc[-1])}, day)

    # 4. Month-end rebalance: decide once per month end, submit before the next open.
    month_end = sessions.latest_month_end()
    first = pd.Timestamp(account["first_session"])
    fill_date = sessions.next_session(latest)
    if month_end is not None and month_end >= first:
        key = month_end.date().isoformat()
        lag = sessions.count_between(month_end, fill_date) - 1
        if not ledger.exists("decisions", key):
            if lag > config["max_fill_lag_sessions"]:
                log.append(f"{key}: rebalance missed ({lag} sessions late); waiting for the next month end")
            elif sessions.opened(fill_date):
                log.append(f"{key}: next session already open; will submit for the following open")
            elif halted(config):
                halt_reason = f"{key}: HALT is set; month-end rebalance not decided or submitted"
            else:
                weights, on = decide(policy, bars, month_end)
                previous = {s: float(bars[s]["Close"].iloc[-2]) for s in policy["universe"]}
                orders, equity = plan_orders(policy, config, weights.to_dict(), cash, positions, prices, previous, key)
                for order in orders:
                    order["fill_date"] = fill_date.date().isoformat()
                ledger.put("decisions", {"month_end": key, "decided_at": now.isoformat(), "fill_date": fill_date.date().isoformat(),
                                         "fill_lag_sessions": lag, "trend_on": {s: bool(v) for s, v in on.items()},
                                         "target_weights": {s: float(w) for s, w in weights.items()},
                                         "equity_estimate": equity, "prices": prices}, key)
                ledger.put("orders", orders, key)
                log.append(f"{key}: decided; {len(orders)} orders for the {fill_date.date().isoformat()} open")
        # Submit any recorded orders the broker has not received yet (recovers from a crash mid-run).
        if ledger.exists("orders", key):
            unsent = [o for o in ledger.get("orders", key) if not broker.known(o["client_order_id"])]
            if unsent:
                if halted(config):
                    halt_reason = f"{key}: HALT is set; {len(unsent)} recorded orders not submitted"
                elif sessions.opened(pd.Timestamp(unsent[0]["fill_date"])):
                    log.append(f"{key}: {len(unsent)} recorded orders missed their open and were not sent")
                else:
                    broker.submit(unsent)
                    log.append(f"{key}: submitted {len(unsent)} orders")

    report(ledger, policy, Path(root) / "report.md", broker, halt_reason)
    if halt_reason:
        raise Halt(halt_reason)
    return log


def report(ledger, policy, destination, broker, halt_reason=None):
    account = ledger.get("account")
    daily = ledger.all("daily")
    lines = [f"# Paper trading (policy v{policy['version']}, {account['broker']} broker)", "",
             f"Started {account['first_session']} with ${account['starting_cash']:,.0f}. "
             "Rebalances at month ends, filled at the next open.", ""]
    if halt_reason:
        lines += [f"**HALTED:** {halt_reason}", ""]
    if daily:
        first, last = daily[0][1], daily[-1][1]
        account_return = last["equity"] / account["starting_cash"] - 1
        spy_return = last["spy_adjusted_close"] / first["spy_adjusted_close"] - 1
        equity = pd.Series([d["equity"] for _, d in daily])
        drawdown = float((equity / equity.cummax() - 1).min())
        lines += ["| As of | Equity | Return | SPY return | Max drawdown | Cash |", "|---|---:|---:|---:|---:|---:|",
                  f"| {last['date']} | ${last['equity']:,.2f} | {account_return:+.2%} | {spy_return:+.2%} | {drawdown:.2%} | ${last['cash']:,.2f} |",
                  "", "## Positions", "", "| Symbol | Shares | Close | Value | Weight |", "|---|---:|---:|---:|---:|"]
        for symbol, qty in sorted(last["positions"].items()):
            value = qty * last["closes"][symbol]
            lines.append(f"| {symbol} | {qty:g} | {last['closes'][symbol]:.2f} | ${value:,.2f} | {value / last['equity']:.1%} |")
        if not last["positions"]:
            lines.append("| (all cash) | | | | |")
    decisions = ledger.all("decisions")
    if decisions:
        key, decision = decisions[-1]
        lines += ["", f"## Latest decision: {key} (fill {decision['fill_date']})", "",
                  "| Symbol | Trend on | Target weight |", "|---|---|---:|"]
        lines += [f"| {s} | {'yes' if decision['trend_on'][s] else 'no'} | {w:.1%} |" for s, w in decision["target_weights"].items()]
    pending = broker.state["pending"]
    lines += ["", f"Pending orders: {len(pending)}.", "",
              "Simulated fills use Yahoo's raw open plus the policy's slippage and commission; whole shares only; "
              "cash earns no interest. Paper results are not a forecast of live results.", ""]
    destination.write_text("\n".join(lines))
