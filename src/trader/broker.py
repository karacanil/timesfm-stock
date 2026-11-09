"""Broker adapters share one interface so the same rebalance code drives simulated and real paper accounts.

    holdings() -> (cash, {symbol: shares})
    submit(orders) -> None          # idempotent on client_order_id
    known(client_order_id) -> bool
    settle(bars, completed) -> [events]   # simulated only; real brokers fill on their side
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd


class SimulatedBroker:
    """Fills market-on-open orders at the raw open of their fill session, with the policy's
    slippage and commission. Credits dividends and applies splits on held shares. Whole shares only;
    buys are cut to what cash allows after the same day's sells."""

    def __init__(self, state_path, starting_cash, commission_bps, slippage_bps):
        self.path = Path(state_path)
        self.commission = commission_bps / 10_000
        self.slippage = slippage_bps / 10_000
        if self.path.exists():
            self.state = json.loads(self.path.read_text())
        else:
            self.state = {"cash": float(starting_cash), "positions": {}, "pending": [],
                          "known_ids": [], "processed_through": None}

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.state, indent=2) + "\n")

    def holdings(self):
        return self.state["cash"], {s: q for s, q in self.state["positions"].items() if q}

    def known(self, client_order_id):
        return client_order_id in self.state["known_ids"]

    def submit(self, orders):
        for order in orders:
            if self.known(order["client_order_id"]):
                continue
            self.state["pending"].append(order)
            self.state["known_ids"].append(order["client_order_id"])
        self.save()

    def settle(self, bars, completed):
        """Process corporate actions and fills for completed sessions not processed yet.
        Returns events grouped by session: {date: [event, ...]}."""
        start = self.state["processed_through"]
        days = [d.date().isoformat() for d in completed if start is None or d.date().isoformat() > start]
        grouped = {}
        positions = self.state["positions"]
        for day in days:
            events = []
            stamp = pd.Timestamp(day)
            for symbol in sorted(positions):
                bar = bars[symbol].loc[stamp] if stamp in bars[symbol].index else None
                if bar is None or not positions[symbol]:
                    continue
                if bar["Stock Splits"]:
                    positions[symbol] *= float(bar["Stock Splits"])
                    events.append({"type": "split", "symbol": symbol, "ratio": float(bar["Stock Splits"])})
                if bar["Dividends"]:
                    amount = positions[symbol] * float(bar["Dividends"])
                    self.state["cash"] += amount
                    events.append({"type": "dividend", "symbol": symbol, "per_share": float(bar["Dividends"]),
                                   "amount": amount})
            due = [o for o in self.state["pending"] if o["fill_date"] == day]
            for order in sorted(due, key=lambda o: o["side"] != "sell"):  # Sells first free up cash.
                if stamp not in bars[order["symbol"]].index:
                    raise ValueError(f"No bar for {order['symbol']} on fill date {day}")
                sign = 1 if order["side"] == "buy" else -1
                price = float(bars[order["symbol"]].at[stamp, "Open"]) * (1 + sign * self.slippage)
                qty = order["qty"]
                if order["side"] == "buy":
                    qty = min(qty, math.floor(self.state["cash"] / (price * (1 + self.commission))))
                else:
                    qty = min(qty, positions.get(order["symbol"], 0))
                if qty <= 0:
                    events.append({"type": "rejected", "symbol": order["symbol"],
                                   "client_order_id": order["client_order_id"], "reason": "insufficient cash or shares"})
                    continue
                commission = qty * price * self.commission
                positions[order["symbol"]] = positions.get(order["symbol"], 0) + sign * qty
                self.state["cash"] -= sign * qty * price + commission
                events.append({"type": "fill", "symbol": order["symbol"], "side": order["side"], "qty": qty,
                               "price": price, "commission": commission,
                               "client_order_id": order["client_order_id"]})
            self.state["pending"] = [o for o in self.state["pending"] if o["fill_date"] != day]
            if events:
                grouped[day] = events
        if days:
            self.state["processed_through"] = days[-1]
        return grouped
