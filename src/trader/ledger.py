"""Append-only paper-trading records. Files are created once and never rewritten."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as tmp:
        json.dump(value, tmp, indent=2, allow_nan=False)
        tmp.write("\n")
        name = tmp.name
    try:
        os.link(name, path)  # Fails if the record already exists.
    finally:
        os.unlink(name)


def read(path):
    return json.loads(Path(path).read_text())


class Ledger:
    """account.json, decisions/<month end>.json, orders/<month end>.json,
    events/<session>.json (fills, dividends, splits), daily/<session>.json."""

    def __init__(self, root):
        self.root = Path(root)

    def path(self, kind, day=None):
        return self.root / "account.json" if kind == "account" else self.root / kind / f"{day}.json"

    def exists(self, kind, day=None):
        return self.path(kind, day).exists()

    def get(self, kind, day=None):
        return read(self.path(kind, day))

    def put(self, kind, value, day=None):
        write_new(self.path(kind, day), value)

    def all(self, kind):
        folder = self.root / kind
        return [(p.stem, read(p)) for p in sorted(folder.glob("*.json"))] if folder.exists() else []

    def expected_holdings(self):
        """Replay recorded events from the starting cash to the cash and shares we should hold."""
        cash = float(self.get("account")["starting_cash"])
        shares = {}
        for _, events in self.all("events"):
            for event in events:
                symbol = event.get("symbol")
                if event["type"] == "split":
                    shares[symbol] = shares.get(symbol, 0.0) * event["ratio"]
                elif event["type"] == "dividend":
                    cash += event["amount"]
                elif event["type"] == "fill":
                    signed = event["qty"] if event["side"] == "buy" else -event["qty"]
                    shares[symbol] = shares.get(symbol, 0.0) + signed
                    cash -= signed * event["price"] + event["commission"]
        return cash, {s: q for s, q in shares.items() if abs(q) > 1e-9}
