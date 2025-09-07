"""
Portfolio Optimization Service (Refactored)
------------------------------------------

Lightweight wrapper that delegates optimization and rebalancing operations
to dedicated modules in ``src/services/financial/portfolio``.
The former monolithic implementation (≈1000 lines) has been replaced by
this orchestrator to maintain backward compatibility while leveraging the
modular architecture.
"""

from typing import Dict, List, Optional
import logging

from .portfolio import (
    PortfolioOptimizationAlgorithms,
    PortfolioRebalancing,
    OptimizationConstraint,
    OptimizationResult,
    RebalancingSignal,
)


logger = logging.getLogger(__name__)


class PortfolioOptimizationService:
    """Thin wrapper around modular portfolio optimization components."""

    def __init__(self, market_data_service=None):
        self.market_data_service = market_data_service
        self.algorithms = PortfolioOptimizationAlgorithms()
        self.rebalancing = PortfolioRebalancing()

    def calculate_returns_and_covariance(
        self,
        symbols: List[str],
        period: str = "1y",
        interval: str = "1d",
    ):
        """Fetch historical data and compute returns and covariance."""
        if not self.market_data_service:
            logger.warning("Market data service not available")
            return None, None

        historical_data = {}
        for symbol in symbols:
            data = self.market_data_service.get_historical_data(symbol, period, interval)
            if data and data.data is not None:
                historical_data[symbol] = data.data
        return self.algorithms.calculate_returns_and_covariance(historical_data)

    def optimize_portfolio_sharpe(
        self,
        symbols: List[str],
        current_weights: Optional[Dict[str, float]] = None,
        constraints: Optional[List[OptimizationConstraint]] = None,
    ) -> Optional[OptimizationResult]:
        """Optimize portfolio for maximum Sharpe ratio."""
        mean_returns, covariance = self.calculate_returns_and_covariance(symbols)
        if mean_returns is None or covariance is None:
            return None
        return self.algorithms.optimize_portfolio_sharpe(
            symbols, mean_returns, covariance, current_weights, constraints
        )

    def generate_rebalancing_signals(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
    ) -> List[RebalancingSignal]:
        """Generate rebalancing signals based on current and target weights."""
        return self.rebalancing.generate_rebalancing_signals(
            current_weights, target_weights
        )

