"""Data models for portfolio tracking modules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List


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
