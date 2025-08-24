"""Strategy execution utilities."""

from __future__ import annotations

import logging
from typing import Callable, Dict, Optional

import pandas as pd

from .strategy_analysis import StrategyType, TradingSignal

logger = logging.getLogger(__name__)


class StrategyExecutor:
    """Execute registered trading strategies and return their signals."""

    def __init__(self) -> None:
        self._strategies: Dict[
            StrategyType, Callable[[str, pd.DataFrame], Optional[TradingSignal]]
        ] = {}
        logger.info("StrategyExecutor initialised")

    def register_strategy(
        self,
        strategy_type: StrategyType,
        func: Callable[[str, pd.DataFrame], Optional[TradingSignal]],
    ) -> None:
        """Register a strategy implementation."""
        logger.debug("Registering strategy %s", strategy_type)
        self._strategies[strategy_type] = func

    def execute(
        self, strategy_type: StrategyType, symbol: str, data: pd.DataFrame
    ) -> Optional[TradingSignal]:
        """Execute a strategy and return its trading signal."""
        logger.info("Executing %s for %s", strategy_type, symbol)
        strategy = self._strategies.get(strategy_type)
        if not strategy:
            logger.error("Strategy %s not registered", strategy_type)
            raise ValueError(f"Strategy {strategy_type} not registered")
        return strategy(symbol, data)
