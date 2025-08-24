"""Portfolio performance tracking orchestrator."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, List, Optional

from .data_acquisition import MarketDataService
from .data_management import PerformanceDataManager
from .models import PerformanceReport, PerformanceSnapshot, PortfolioAllocation
from .reporting import PerformanceReporter
from .strategy_logic import PerformanceCalculator

logger = logging.getLogger(__name__)


class PortfolioPerformanceTracker:
    """High level service coordinating portfolio tracking components."""

    def __init__(
        self,
        data_manager: Optional[PerformanceDataManager] = None,
        data_service: Optional[MarketDataService] = None,
        calculator: Optional[PerformanceCalculator] = None,
        reporter: Optional[PerformanceReporter] = None,
    ) -> None:
        self.data_manager = data_manager or PerformanceDataManager()
        self.data_service = data_service or MarketDataService()
        self.calculator = calculator or PerformanceCalculator()
        self.reporter = reporter or PerformanceReporter(self.data_manager)
        self.history: List[PerformanceSnapshot] = self.data_manager.load_history()

    # Expose history for backward compatibility
    @property
    def performance_history(self) -> List[PerformanceSnapshot]:
        return self.history

    # ------------------------------------------------------------------
    def track_portfolio_performance(
        self, portfolio_value: float, weights: Dict[str, float]
    ) -> PerformanceSnapshot:
        """Create and persist a new :class:`PerformanceSnapshot`."""

        prices = self.data_service.fetch_prices(list(weights.keys()))
        daily = self.calculator.calculate_daily_return(self.history, portfolio_value)
        total = self.calculator.calculate_total_return(self.history, portfolio_value)
        metrics = self.calculator.calculate_metrics(weights, prices)
        snapshot = PerformanceSnapshot(
            timestamp=datetime.now(),
            total_value=portfolio_value,
            total_return=total,
            daily_return=daily,
            weights=weights,
            metrics=metrics,
            allocations=[
                PortfolioAllocation(symbol=symbol, weight=weight)
                for symbol, weight in weights.items()
            ],
        )
        self.data_manager.save_snapshot(snapshot)
        self.history.append(snapshot)
        return snapshot

    def generate_performance_report(
        self, start_date: datetime, end_date: datetime
    ) -> Optional[PerformanceReport]:
        """Generate a report for the given period."""

        return self.reporter.generate_report(self.history, start_date, end_date)

    # Backwards compatible alias
    def generate_report(
        self, start_date: datetime, end_date: datetime
    ) -> Optional[PerformanceReport]:
        return self.generate_performance_report(start_date, end_date)
