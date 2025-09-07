"""Trading strategy implementations."""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

from .models import StrategyType, TradingSignal, SignalType, SignalStrength

logger = logging.getLogger(__name__)


def momentum_strategy(symbol: str, data: pd.DataFrame) -> Optional[TradingSignal]:
    """Simple momentum strategy using the last two closing prices."""
    logger.info("Running momentum strategy for %s", symbol)
    if len(data) < 2:
        logger.debug("Not enough data for momentum strategy")
        return None
    last_close = float(data["Close"].iloc[-1])
    prev_close = float(data["Close"].iloc[-2])
    if last_close > prev_close:
        signal_type = SignalType.BUY
    elif last_close < prev_close:
        signal_type = SignalType.SELL
    else:
        signal_type = SignalType.HOLD
    return TradingSignal(
        symbol=symbol,
        signal_type=signal_type,
        strength=SignalStrength.WEAK,
        confidence=0.0,
        price=last_close,
        target_price=last_close,
        stop_loss=last_close,
        strategy=StrategyType.MOMENTUM,
        reasoning="momentum" if signal_type != SignalType.HOLD else "no momentum",
    )


def mean_reversion_strategy(symbol: str, data: pd.DataFrame) -> Optional[TradingSignal]:
    """Generate a signal when price deviates from its mean."""
    logger.info("Running mean reversion strategy for %s", symbol)
    if data.empty:
        logger.debug("No data for mean reversion strategy")
        return None
    price = float(data["Close"].iloc[-1])
    mean_price = float(data["Close"].mean())
    if price > mean_price:
        signal_type = SignalType.SELL
        reasoning = "price above mean"
    elif price < mean_price:
        signal_type = SignalType.BUY
        reasoning = "price below mean"
    else:
        return None
    return TradingSignal(
        symbol=symbol,
        signal_type=signal_type,
        strength=SignalStrength.WEAK,
        confidence=0.0,
        price=price,
        target_price=mean_price,
        stop_loss=mean_price,
        strategy=StrategyType.MEAN_REVERSION,
        reasoning=reasoning,
    )
