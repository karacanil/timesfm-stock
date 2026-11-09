"""Exchange sessions: which closes are final, which session is a month end, when orders still fit."""
from __future__ import annotations

import exchange_calendars as xcals
import pandas as pd


class Sessions:
    def __init__(self, name, now, delay_minutes=60, start="2003-01-01"):
        now = pd.Timestamp(now)
        if now.tzinfo is None:
            raise ValueError("now must have a timezone")
        self.now = now
        self.calendar = xcals.get_calendar(name, start=start, end=(now + pd.Timedelta(days=60)).date().isoformat())
        sessions = self.calendar.sessions
        delay = pd.Timedelta(minutes=delay_minutes)
        past = sessions[sessions <= pd.Timestamp(now.date())]
        self.completed = pd.DatetimeIndex([s for s in past if self.calendar.session_close(s) + delay <= now])

    @property
    def latest(self):
        return self.completed[-1]

    def next_session(self, session):
        sessions = self.calendar.sessions
        return sessions[sessions > pd.Timestamp(session)][0]

    def is_month_end(self, session):
        return self.next_session(session).month != pd.Timestamp(session).month

    def latest_month_end(self):
        for session in reversed(self.completed):
            if self.is_month_end(session):
                return session
        return None

    def opened(self, session):
        return self.now >= self.calendar.session_open(session)

    def count_between(self, first, last):
        """Number of sessions s with first < s <= last."""
        sessions = self.calendar.sessions
        return int(((sessions > pd.Timestamp(first)) & (sessions <= pd.Timestamp(last))).sum())
