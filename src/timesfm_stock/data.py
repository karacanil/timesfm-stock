"""Yahoo daily closes aligned to finalized exchange sessions."""
from __future__ import annotations

import time

import numpy as np
import pandas as pd
import exchange_calendars as xcals


def utc_now():
    return pd.Timestamp.now(tz="UTC")


def completed_sessions(calendar_name, now, delay_minutes=60, start=None):
    now = pd.Timestamp(now)
    if now.tzinfo is None:
        raise ValueError("now must have a timezone")
    start = start or (now - pd.Timedelta(days=365 * 8)).date().isoformat()
    calendar = xcals.get_calendar(calendar_name, start=start,
                                 end=(now + pd.Timedelta(days=180)).date().isoformat())
    sessions = calendar.sessions[(calendar.sessions >= pd.Timestamp(start)) &
                                 (calendar.sessions <= pd.Timestamp(now.date()))]
    delay = pd.Timedelta(minutes=delay_minutes)
    return calendar, pd.DatetimeIndex([
        session for session in sessions if calendar.session_close(session) + delay <= now
    ])


def future_sessions(calendar, origin, horizon):
    sessions = calendar.sessions
    future = sessions[sessions > pd.Timestamp(origin)][:horizon]
    if len(future) != horizon:
        raise ValueError("Calendar does not cover the forecast horizon")
    return [day.date().isoformat() for day in future]


def yahoo_history(symbol, start, end):
    import yfinance as yf
    # The end is exclusive. Explicit raw-close policy: no dividend adjustment.
    for attempt in range(3):
        try:
            frame = yf.Ticker(symbol).history(start=start, end=end, interval="1d",
                                             auto_adjust=False, actions=True,
                                             raise_errors=True, timeout=20)
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
    return frame.sort_index()


def aligned_context(frame, sessions, count):
    if len(sessions) < count:
        raise ValueError("Insufficient completed sessions")
    required = sessions[-count:]
    close = frame["Close"].reindex(required)
    values = close.to_numpy(dtype=np.float64)
    if not np.isfinite(values).all() or (values <= 0).any():
        missing = [x.date().isoformat() for x in close.index[close.isna()]]
        raise ValueError(f"Missing/invalid closes; no interpolation allowed: {missing}")
    return values
