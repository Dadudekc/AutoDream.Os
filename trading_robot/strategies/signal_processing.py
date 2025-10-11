"""
Signal Processing - V2 Compliant
=================================

Trading signal types and result processing.
Extracted from base_strategy.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

from enum import Enum
from typing import Any

import pandas as pd


class Signal(Enum):
    """Trading signals."""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class StrategyResult:
    """Result of strategy analysis."""

    def __init__(
        self,
        symbol: str,
        signal: Signal,
        confidence: float,
        indicators: dict[str, Any] = None,
        metadata: dict[str, Any] = None,
    ):
        self.symbol = symbol
        self.signal = signal
        self.confidence = confidence
        self.indicators = indicators or {}
        self.metadata = metadata or {}
        self.timestamp = pd.Timestamp.now()
