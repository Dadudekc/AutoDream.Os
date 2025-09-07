"""Shared metrics utilities.

This module provides a single source of truth for simple metrics
collection patterns used across the codebase."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class Metric:
    """Representation of a single metric value."""

    name: str
    value: float


class MetricsCollector:
    """Store and retrieve metric values in-memory."""

    def __init__(self) -> None:
        self._metrics: Dict[str, float] = {}
        self._counters = CounterMetrics()

    def record(self, name: str, value: float) -> None:
        """Record a metric value."""

        self._metrics[name] = float(value)

    def get(self, name: str) -> Optional[float]:
        """Return the latest value for *name* if available."""

        return self._metrics.get(name)

    def all(self) -> Dict[str, float]:
        """Return a copy of all metrics."""

        return dict(self._metrics)

    @property
    def total_operations(self) -> int:
        return self._counters.get("total_operations")

    @property
    def successful_operations(self) -> int:
        return self._counters.get("successful_operations")

    @property
    def failed_operations(self) -> int:
        return self._counters.get("failed_operations")

    def record_success(self) -> None:
        """Record a successful operation."""

        self._counters.increment("total_operations")
        self._counters.increment("successful_operations")

    def record_failure(self) -> None:
        """Record a failed operation."""

        self._counters.increment("total_operations")
        self._counters.increment("failed_operations")


class CounterMetrics:
    """Lightweight counter-based metrics manager."""

    def __init__(self) -> None:
        self.counters: Dict[str, int] = defaultdict(int)

    def increment(self, name: str, amount: int = 1) -> None:
        """Increment a named counter."""

        self.counters[name] += amount

    def get(self, name: str) -> int:
        """Retrieve a counter value (defaults to 0)."""

        return self.counters.get(name, 0)


@dataclass
class OptimizationRunMetrics:
    """Metrics captured for a single optimization run."""

    timestamp: str
    tasks_processed: int
    errors: int
    duration: float


def gather_run_metrics(
    tasks_processed: int, errors: int, duration: float, _now: Optional[datetime] = None
) -> OptimizationRunMetrics:
    """Gather metrics for an optimization run."""

    return OptimizationRunMetrics(
        timestamp=(_now or datetime.now()).isoformat(),
        tasks_processed=tasks_processed,
        errors=errors,
        duration=duration,
    )


__all__ = [
    "Metric",
    "MetricsCollector",
    "CounterMetrics",
    "OptimizationRunMetrics",
    "gather_run_metrics",
]
