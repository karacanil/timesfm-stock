"""Daily dividend-adjusted bars, cached locally so backtests are repeatable offline."""
from __future__ import annotations

import hashlib
import time
from pathlib import Path

import pandas as pd


def yahoo_adjusted(symbol, start):
    import yfinance as yf
    for attempt in range(3):
        try:
            frame = yf.Ticker(symbol).history(start=start, interval="1d", auto_adjust=True,
                                              actions=False, raise_errors=True, timeout=30)
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))
    if frame.empty:
        raise ValueError(f"Yahoo returned no data for {symbol}")
    frame.index = pd.DatetimeIndex([pd.Timestamp(x).date() for x in frame.index])
    if frame.index.has_duplicates:
        raise ValueError(f"Duplicate daily bars for {symbol}")
    return frame[["Open", "Close"]].sort_index()


def yahoo_full(symbol, start):
    """Raw Open/Close for trading, Adj Close for signals, plus dividends and splits."""
    import yfinance as yf
    for attempt in range(3):
        try:
            frame = yf.Ticker(symbol).history(start=start, interval="1d", auto_adjust=False,
                                              actions=True, raise_errors=True, timeout=30)
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))
    if frame.empty:
        raise ValueError(f"Yahoo returned no data for {symbol}")
    frame.index = pd.DatetimeIndex([pd.Timestamp(x).date() for x in frame.index])
    if frame.index.has_duplicates:
        raise ValueError(f"Duplicate daily bars for {symbol}")
    return frame[["Open", "Close", "Adj Close", "Dividends", "Stock Splits"]].sort_index()


def load(symbols, start, cache_dir, refresh=False, fetch=yahoo_adjusted):
    """Return {symbol: DataFrame[Open, Close]}; cached as CSV under cache_dir."""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    frames = {}
    for symbol in symbols:
        path = cache_dir / f"{symbol.replace('^', '_')}.csv"
        if path.exists() and not refresh:
            frame = pd.read_csv(path, index_col=0, parse_dates=True)
        else:
            frame = fetch(symbol, start)
            frame.to_csv(path)
        frames[symbol] = frame
    return frames


def panel(frames, universe, calendar_symbol="SPY"):
    """Align asset bars to the calendar symbol's sessions. Gaps after inception are forward-filled
    (at most 5 sessions) and counted; anything before inception stays NaN."""
    index = frames[calendar_symbol].index
    opens, closes, filled = {}, {}, {}
    for symbol in universe:
        frame = frames[symbol].reindex(index)
        inception = frames[symbol].index.min()
        live = frame.index >= inception
        filled[symbol] = int(frame["Close"][live].isna().sum())
        frame = frame.ffill(limit=5)
        opens[symbol] = frame["Open"].fillna(frame["Close"]).where(live)
        closes[symbol] = frame["Close"].where(live)
    return pd.DataFrame(opens), pd.DataFrame(closes), filled


def cash_rate(frames, symbol, index):
    """Daily simple rate from the 13-week T-bill yield (percent, annualized)."""
    yields = frames[symbol]["Close"].reindex(index).ffill().fillna(0.0)
    return yields / 100 / 252


def fingerprint(frames):
    digest = hashlib.sha256()
    for symbol in sorted(frames):
        digest.update(symbol.encode())
        digest.update(frames[symbol].round(6).to_csv().encode())
    return digest.hexdigest()
