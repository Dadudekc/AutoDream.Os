"""Reporting helpers for trading intelligence."""

from __future__ import annotations

import logging
from typing import Iterable

from .strategy_analysis import TradingSignal

logger = logging.getLogger(__name__)


def log_signal(signal: TradingSignal) -> None:
    """Log information about a generated trading signal."""
    logger.info(
        "Signal generated: symbol=%s type=%s price=%s",  # pragma: no cover - simple logging
        signal.symbol,
        signal.signal_type.value,
        signal.price,
    )


def log_signals(signals: Iterable[TradingSignal]) -> None:
    """Log a list of trading signals."""
    for signal in signals:
        log_signal(signal)
