"""Trend signal and volatility-scaled target weights. Every value at row t uses closes up to t only."""
from __future__ import annotations

import numpy as np
import pandas as pd


def trend_on(close, lookback=252, skip=21, sma=200):
    """True where 12-1 momentum > 0 AND close > SMA. False when history is too short."""
    momentum = close.shift(skip) / close.shift(lookback) - 1
    average = close.rolling(sma, min_periods=sma).mean()
    return (momentum > 0) & (close > average)


def target_weights(close_window, on, target_vol=0.10, max_gross=1.0, max_weight=0.25):
    """Inverse-volatility weights over 'on' assets, scaled toward target portfolio volatility,
    capped per asset; whatever is not invested stays in cash.

    close_window: the last (vol_lookback + 1) closes ending at the decision date.
    """
    weights = pd.Series(0.0, index=close_window.columns)
    returns = np.log(close_window).diff().iloc[1:]
    active = [s for s in close_window.columns if on.get(s, False) and returns[s].notna().all()]
    if not active:
        return weights
    returns = returns[active]
    vol = returns.std() * np.sqrt(252)
    if (vol <= 0).any():
        return weights
    raw = (1 / vol) / (1 / vol).sum()
    portfolio_vol = float(np.sqrt(raw.to_numpy() @ (returns.cov().to_numpy() * 252) @ raw.to_numpy()))
    scale = min(max_gross, target_vol / portfolio_vol) if portfolio_vol > 0 else 0.0
    weights[active] = np.minimum(raw * scale, max_weight)
    return weights
