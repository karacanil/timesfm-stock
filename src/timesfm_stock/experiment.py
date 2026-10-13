"""Immutable prospective runs and first-observed outcomes."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd

from .data import aligned_context, completed_sessions, future_sessions, utc_now, yahoo_history
from .model import TimesFM, UPSTREAM_COMMIT, resolve_revision


def write_new(path, value):
    """Atomically publish complete JSON; never replace an existing snapshot."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as tmp:
        json.dump(value, tmp, indent=2, allow_nan=False)
        tmp.write("\n")
        name = tmp.name
    try:
        os.link(name, path)  # Exclusive creation; readers cannot see partial JSON.
    finally:
        os.unlink(name)


def read(path):
    return json.loads(Path(path).read_text())


def validate_config(config):
    symbols = config["symbols"]
    if not symbols or len(set(symbols)) != len(symbols) or len(symbols) > 32:
        raise ValueError("Use 1–32 unique symbols")
    if any(not isinstance(s, str) or not s or not all(c.isalnum() or c in '.^-=' for c in s) for s in symbols):
        raise ValueError("Invalid ticker symbols")
    for key, lower, upper in [("context_sessions", 32, 15360), ("horizon_sessions", 1, 64),
                              ("batch_size", 1, 32), ("collection_days", 1, 366),
                              ("close_delay_minutes", 0, 1440)]:
        if type(config[key]) is not int or not lower <= config[key] <= upper:
            raise ValueError(f"Invalid {key}: expected integer in [{lower}, {upper}]")
    if not config["modes"] or len(set(config["modes"])) != len(config["modes"]) or not set(config["modes"]) <= {"univariate", "multivariate"}:
        raise ValueError("modes must contain univariate and/or multivariate")
    if config["checkpoint"] != "google/timesfm-3.0-pytorch":
        raise ValueError("This experiment expects the official TimesFM 3.0 checkpoint")
    if not isinstance(config["checkpoint_revision"], str) or not config["checkpoint_revision"]:
        raise ValueError("checkpoint_revision is required")


def collect(config, root, now=None, fetch=yahoo_history, model_factory=TimesFM, resolve=resolve_revision):
    validate_config(config)
    root = Path(root)
    live_clock = now is None
    now = pd.Timestamp(now) if now is not None else utc_now()
    manifest_path = root / "experiment.json"
    manifest = read(manifest_path) if manifest_path.exists() else None
    if manifest and manifest["config"] != config:
        raise ValueError("Configuration changed: use a new --output directory for a new experiment")
    if manifest and now >= pd.Timestamp(manifest["collect_until"]):
        print("Collection window finished; evaluation can continue until all horizons mature.")
        return None
    calendar, sessions = completed_sessions(config["calendar"], now, config["close_delay_minutes"])
    if len(sessions) < config["context_sessions"]:
        raise ValueError("Insufficient completed sessions in calendar")
    origin = sessions[-1].date().isoformat()
    run_path = root / "runs" / f"{origin}.json"
    if run_path.exists():
        print(f"Forecast for {origin} already frozen; skipping.")
        return run_path
    required = sessions[-config["context_sessions"]:]
    end = (sessions[-1] + pd.Timedelta(days=1)).date().isoformat()
    snapshots, contexts = {}, []
    for symbol in config["symbols"]:
        frame = fetch(symbol, required[0].date().isoformat(), end)
        values = aligned_context(frame, sessions, config["context_sessions"])
        contexts.append(values)
        snapshots[symbol] = [{"date": day.date().isoformat(), "close": float(price)}
                             for day, price in zip(required, values)]
    revision = manifest["weight_revision"] if manifest else resolve(config)
    model = model_factory(config, revision)
    predictions = model.predict(np.stack(contexts), config["horizon_sessions"], config["modes"])
    issued = utc_now() if live_clock else now
    dates = future_sessions(calendar, origin, config["horizon_sessions"])
    if issued >= calendar.session_open(dates[0]):
        raise ValueError("Next target session has opened; wait for its completed close to forecast")
    packages = {}
    for package in ["timesfm", "torch", "numpy", "pandas", "yfinance", "exchange-calendars"]:
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not installed"
    payload = {
        "schema_version": 1, "origin": origin, "issued_at": issued.isoformat(),
        "data_fetched_at": now.isoformat(), "config": config,
        "weight_revision": revision, "timesfm_source_commit": UPSTREAM_COMMIT,
        "package_versions": packages, "target_policy": "Yahoo Close; auto_adjust=False; split-affected outcomes excluded",
        "symbols": config["symbols"], "target_dates": dates,
        "history": snapshots, "predictions": predictions,
        "last_price": [float(row[-1]) for row in contexts],
    }
    payload["history_sha256"] = hashlib.sha256(json.dumps(snapshots, sort_keys=True).encode()).hexdigest()
    if not manifest:
        manifest = {"schema_version": 1, "config": config, "weight_revision": revision,
                    "started_at": issued.isoformat(),
                    "collect_until": (issued + pd.Timedelta(days=config["collection_days"])).isoformat()}
        write_new(manifest_path, manifest)
    write_new(run_path, payload)
    print(f"Saved prospective forecast: {run_path}")
    return run_path


def evaluate(root, now=None, fetch=yahoo_history):
    root = Path(root)
    now = pd.Timestamp(now) if now is not None else utc_now()
    runs = sorted((root / "runs").glob("*.json"))
    if not runs:
        print("No forecasts yet; generate a forecast first.")
        return
    # One Yahoo fetch per symbol for all runs, rather than once per forecast.
    first = min(read(p)["origin"] for p in runs)
    config = read(runs[0])["config"]
    _, completed = completed_sessions(config["calendar"], now, config["close_delay_minutes"], start=first)
    completed_dates = {day.date().isoformat() for day in completed}
    due_runs = [(path, read(path)) for path in runs]
    due_runs = [(p, r) for p, r in due_runs if any(d in completed_dates for d in r["target_dates"])]
    if not due_runs:
        print("No target sessions have completed yet.")
        return
    end = (now + pd.Timedelta(days=1)).date().isoformat()
    frames = {}
    for symbol in config["symbols"]:
        needs = any(not (root / "observations" / p.stem / symbol / f"{d}.json").exists()
                    for p, r in due_runs for d in r["target_dates"] if d in completed_dates)
        if needs:
            frames[symbol] = fetch(symbol, first, end)
    for path, run in due_runs:
        for symbol in run["symbols"]:
            frame = frames.get(symbol)
            if frame is None:
                continue
            splits = frame.get("Stock Splits", pd.Series(0., index=frame.index))
            split_dates = splits[(splits != 0) & (splits.index > pd.Timestamp(run["origin"]))].index
            for target in run["target_dates"]:
                destination = root / "observations" / path.stem / symbol / f"{target}.json"
                day = pd.Timestamp(target)
                if target not in completed_dates or destination.exists():
                    continue
                # Yahoo rewrites pre-split history, so compare no post-split bars to old-scale forecasts.
                if len(split_dates):
                    outcome = {"status": "excluded_split", "actual": None}
                elif day not in frame.index or not np.isfinite(frame.at[day, "Close"]):
                    print(f"Pending provider data: {symbol} {target}")
                    continue
                else:
                    outcome = {"status": "observed", "actual": float(frame.at[day, "Close"])}
                write_new(destination, {"date": target, "observed_at": now.isoformat(), **outcome})
    print("Updated first-observed outcomes; existing observations were preserved.")
