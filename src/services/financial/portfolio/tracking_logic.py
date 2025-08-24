"""Tracking logic for portfolio performance.

This module focuses on the core logic required to track portfolio
performance over time. It exposes a simple interface used by the
rest of the portfolio package while delegating persistence and
report generation to separate modules.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Enumeration of supported performance metrics."""

    TOTAL_RETURN = "TOTAL_RETURN"
    ANNUALIZED_RETURN = "ANNUALIZED_RETURN"
    VOLATILITY = "VOLATILITY"
    SHARPE_RATIO = "SHARPE_RATIO"


@dataclass
class PortfolioAllocation:
    """Represents a single portfolio allocation entry."""

    symbol: str
    weight: float

    def to_dict(self) -> Dict[str, float]:
        return {"symbol": self.symbol, "weight": self.weight}

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "PortfolioAllocation":
        return cls(symbol=data["symbol"], weight=data["weight"])


@dataclass
class PerformanceSnapshot:
    """Snapshot of portfolio performance at a specific time."""

    timestamp: datetime
    total_value: float
    total_return: float
    daily_return: float
    weights: Dict[str, float]
    metrics: Dict[str, float]
    allocations: List[PortfolioAllocation]

    def to_dict(self) -> Dict[str, object]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "total_value": self.total_value,
            "total_return": self.total_return,
            "daily_return": self.daily_return,
            "weights": self.weights,
            "metrics": self.metrics,
            "allocations": [a.to_dict() for a in self.allocations],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "PerformanceSnapshot":
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            total_value=data["total_value"],
            total_return=data["total_return"],
            daily_return=data["daily_return"],
            weights=data["weights"],
            metrics=data["metrics"],
            allocations=[
                PortfolioAllocation.from_dict(a) for a in data.get("allocations", [])
            ],
        )


@dataclass
class PerformanceReport:
    """Simplified performance report."""

    report_id: str
    start_date: datetime
    end_date: datetime
    portfolio_value_start: float
    portfolio_value_end: float
    total_return: float

    def to_dict(self) -> Dict[str, object]:
        return {
            "report_id": self.report_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "portfolio_value_start": self.portfolio_value_start,
            "portfolio_value_end": self.portfolio_value_end,
            "total_return": self.total_return,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "PerformanceReport":
        return cls(
            report_id=data["report_id"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            portfolio_value_start=data["portfolio_value_start"],
            portfolio_value_end=data["portfolio_value_end"],
            total_return=data["total_return"],
        )


class PortfolioPerformanceTracker:
    """Core tracking logic without persistence or reporting concerns."""

    def __init__(
        self,
        data_manager: "PerformanceDataManager",
        reporter: Optional["PerformanceReporter"] = None,
    ) -> None:
        self.data_manager = data_manager
        if reporter is None:
            from .reporting import PerformanceReporter

            self.reporter = PerformanceReporter(data_manager)
        else:
            self.reporter = reporter
        self.performance_history: List[
            PerformanceSnapshot
        ] = self.data_manager.load_history()

    # -- Tracking logic -------------------------------------------------
    def track_portfolio_performance(
        self, portfolio_value: float, weights: Dict[str, float]
    ) -> Optional[PerformanceSnapshot]:
        """Create and persist a new :class:`PerformanceSnapshot`."""

        try:
            daily_return = self._calculate_daily_return(portfolio_value)
            total_return = self._calculate_total_return(portfolio_value)
            snapshot = PerformanceSnapshot(
                timestamp=datetime.now(),
                total_value=portfolio_value,
                total_return=total_return,
                daily_return=daily_return,
                weights=weights,
                metrics={},
                allocations=[
                    PortfolioAllocation(symbol=symbol, weight=weight)
                    for symbol, weight in weights.items()
                ],
            )
            self.data_manager.save_snapshot(snapshot)
            self.performance_history.append(snapshot)
            return snapshot
        except Exception as exc:  # pragma: no cover - defensive programming
            logger.error(f"Error tracking portfolio performance: {exc}")
            return None

    def generate_report(
        self, start_date: datetime, end_date: datetime
    ) -> Optional[PerformanceReport]:
        """Generate a performance report for the specified period."""

        return self.reporter.generate_report(
            self.performance_history, start_date, end_date
        )

    # -- Internal calculations ----------------------------------------
    def _calculate_daily_return(self, current_value: float) -> float:
        try:
            if not self.performance_history:
                return 0.0
            prev = self.performance_history[-1].total_value
            return (current_value - prev) / prev if prev else 0.0
        except Exception as exc:  # pragma: no cover - defensive
            logger.error(f"Error calculating daily return: {exc}")
            return 0.0

    def _calculate_total_return(self, current_value: float) -> float:
        try:
            if not self.performance_history:
                return 0.0
            initial = self.performance_history[0].total_value
            return (current_value - initial) / initial if initial else 0.0
        except Exception as exc:  # pragma: no cover - defensive
            logger.error(f"Error calculating total return: {exc}")
            return 0.0
