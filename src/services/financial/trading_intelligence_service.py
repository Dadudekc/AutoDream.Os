"""High level trading intelligence service orchestrating data processing,
strategy analysis, execution and reporting."""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

from .trading_intelligence import (
    StrategyExecutor,
    StrategyType,
    TradingSignal,
    log_signal,
    mean_reversion_strategy,
    momentum_strategy,
    prepare_market_data,
)

logger = logging.getLogger(__name__)


class TradingIntelligenceService:
    """Facade providing a simple interface to run trading strategies."""

    def __init__(self) -> None:
        self.executor = StrategyExecutor()
        self.executor.register_strategy(StrategyType.MOMENTUM, momentum_strategy)
        self.executor.register_strategy(
            StrategyType.MEAN_REVERSION, mean_reversion_strategy
        )
        logger.info("TradingIntelligenceService initialised")

    def run_strategy(
        self, strategy: StrategyType, symbol: str, market_data: pd.DataFrame
    ) -> Optional[TradingSignal]:
        """Prepare data, execute a strategy and log the resulting signal."""
        logger.debug("Running %s strategy for %s", strategy, symbol)
        processed = prepare_market_data(market_data)
        signal = self.executor.execute(strategy, symbol, processed)
        if signal:
            log_signal(signal)
        return signal
