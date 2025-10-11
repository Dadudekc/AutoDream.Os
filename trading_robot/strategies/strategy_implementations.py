"""
Strategy Implementations - V2 Compliant
========================================

Concrete trading strategy implementations.
Extracted from base_strategy.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

from typing import Any

import pandas as pd

from .base_strategy import BaseStrategy
from .signal_processing import Signal, StrategyResult


class TrendFollowingStrategy(BaseStrategy):
    """Trend following strategy using moving averages."""

    def __init__(self, parameters: dict[str, Any] = None):
        super().__init__("Trend Following", parameters)

    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze using trend following logic."""
        if not self.validate_data(data):
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Invalid data"})

        fast_ma = self.get_indicator_value(data, "sma", period=10)
        slow_ma = self.get_indicator_value(data, "sma", period=50)

        if fast_ma is None or slow_ma is None:
            return StrategyResult(symbol, Signal.HOLD, 0.0)

        signal = Signal.BUY if fast_ma > slow_ma else Signal.SELL
        diff = abs(fast_ma - slow_ma) / slow_ma
        confidence = min(diff * 10, 1.0)

        return StrategyResult(
            symbol, signal, confidence, indicators={"fast_ma": fast_ma, "slow_ma": slow_ma}
        )


class MeanReversionStrategy(BaseStrategy):
    """Mean reversion strategy using Bollinger Bands."""

    def __init__(self, parameters: dict[str, Any] = None):
        super().__init__("Mean Reversion", parameters)

    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze using mean reversion logic."""
        if not self.validate_data(data):
            return StrategyResult(symbol, Signal.HOLD, 0.0, metadata={"error": "Invalid data"})

        bb_upper = self.get_indicator_value(data, "bb_upper", period=20)
        bb_lower = self.get_indicator_value(data, "bb_lower", period=20)
        current_price = data["close"].iloc[-1]

        if bb_upper is None or bb_lower is None:
            return StrategyResult(symbol, Signal.HOLD, 0.0)

        if current_price < bb_lower:
            signal = Signal.BUY
            distance = (bb_lower - current_price) / bb_lower
        elif current_price > bb_upper:
            signal = Signal.SELL
            distance = (current_price - bb_upper) / bb_upper
        else:
            signal = Signal.HOLD
            distance = 0.0

        confidence = min(distance * 10, 1.0)

        return StrategyResult(
            symbol, signal, confidence, indicators={"bb_upper": bb_upper, "bb_lower": bb_lower}
        )
