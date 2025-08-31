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
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0

    def record(self, name: str, value: float) -> None:
        """Record a metric value."""

        self._metrics[name] = float(value)

    def get(self, name: str) -> Optional[float]:
        """Return the latest value for *name* if available."""

        return self._metrics.get(name)

    def all(self) -> Dict[str, float]:
        """Return a copy of all metrics."""

        return dict(self._metrics)

    def record_success(self) -> None:
        """Record a successful operation."""

        self.total_operations += 1
        self.successful_operations += 1

    def record_failure(self) -> None:
        """Record a failed operation."""

        self.total_operations += 1
        self.failed_operations += 1


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
    tasks_processed: int, errors: int, duration: float
) -> OptimizationRunMetrics:
    """Gather metrics for an optimization run."""

    return OptimizationRunMetrics(
        timestamp=datetime.now().isoformat(),
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
