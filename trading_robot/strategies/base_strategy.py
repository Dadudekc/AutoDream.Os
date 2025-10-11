"""
Base Trading Strategy Framework - V2 Compliant
===============================================

Abstract base class for trading strategies.
Refactored for V2 compliance by Agent-3.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 refactor)
"""

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd
from loguru import logger
from strategies.indicators import TechnicalIndicators

from .risk_management import RiskManagement
from .signal_processing import Signal, StrategyResult


class BaseStrategy(ABC):
    """Abstract base class for trading strategies."""

    def __init__(self, name: str, parameters: dict[str, Any] = None):
        """Initialize strategy."""
        self.name = name
        self.parameters = parameters or {}
        self.indicators = TechnicalIndicators()
        self.risk_mgmt = RiskManagement()

    @abstractmethod
    def analyze(self, data: pd.DataFrame, symbol: str) -> StrategyResult:
        """Analyze market data and generate trading signal."""
        pass

    def calculate_position_size(
        self, account_balance: float, price: float, risk_pct: float = 0.01
    ) -> int:
        """Calculate position size based on risk management."""
        return self.risk_mgmt.calculate_position_size(account_balance, price, risk_pct)

    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate input data."""
        if data is None or data.empty:
            logger.warning(f"{self.name}: Empty data provided")
            return False

        required_columns = ["open", "high", "low", "close", "volume"]
        missing = [col for col in required_columns if col not in data.columns]

        if missing:
            logger.warning(f"{self.name}: Missing columns: {missing}")
            return False

        if len(data) < 50:
            logger.warning(f"{self.name}: Insufficient data ({len(data)} bars, need 50+)")
            return False

        return True

    def get_indicator_value(
        self, data: pd.DataFrame, indicator_name: str, period: int = 14, **kwargs
    ):
        """Get technical indicator value."""
        try:
            if indicator_name == "sma":
                return self.indicators.sma(data["close"], period)
            elif indicator_name == "ema":
                return self.indicators.ema(data["close"], period)
            elif indicator_name == "rsi":
                return self.indicators.rsi(data["close"], period)
            elif indicator_name == "macd":
                return self.indicators.macd(data["close"])
            elif indicator_name == "bb_upper":
                bb = self.indicators.bollinger_bands(data["close"], period)
                return bb["upper"]
            elif indicator_name == "bb_lower":
                bb = self.indicators.bollinger_bands(data["close"], period)
                return bb["lower"]
            else:
                logger.warning(f"Unknown indicator: {indicator_name}")
                return None

        except Exception as e:
            logger.error(f"Error calculating {indicator_name}: {e}")
            return None


class StrategyManager:
    """Manages multiple trading strategies."""

    def __init__(self):
        """Initialize strategy manager."""
        self.strategies: list[BaseStrategy] = []

    def add_strategy(self, strategy: BaseStrategy):
        """Add a strategy."""
        self.strategies.append(strategy)
        logger.info(f"Added strategy: {strategy.name}")

    def remove_strategy(self, strategy_name: str):
        """Remove a strategy."""
        self.strategies = [s for s in self.strategies if s.name != strategy_name]
        logger.info(f"Removed strategy: {strategy_name}")

    def get_strategies(self) -> list[str]:
        """Get list of active strategies."""
        return [s.name for s in self.strategies]

    def analyze_symbol(self, symbol: str, data: pd.DataFrame) -> list[StrategyResult]:
        """Run all strategies on symbol."""
        results = []
        for strategy in self.strategies:
            try:
                result = strategy.analyze(data, symbol)
                results.append(result)
            except Exception as e:
                logger.error(f"Error in {strategy.name}: {e}")
        return results

    def get_consensus_signal(self, results: list[StrategyResult]) -> Tuple[Signal, float]:
        """Get consensus signal."""
        return RiskManagement.get_consensus_signal(results)
