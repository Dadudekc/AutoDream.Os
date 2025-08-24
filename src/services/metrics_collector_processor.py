"""Utilities for processing collected metrics."""
from __future__ import annotations

from typing import Callable, Iterable, List

from .performance_monitor import MetricData, MetricType


class MetricsProcessor:
    """Provides simple processing helpers for metric data."""

    def normalize(self, metrics: Iterable[MetricData]) -> List[MetricData]:
        """Return a list copy of metric iterable."""
        return list(metrics)

    def filter_by_type(
        self, metrics: Iterable[MetricData], metric_type: MetricType
    ) -> List[MetricData]:
        """Filter metrics by MetricType."""
        return [m for m in metrics if m.metric_type == metric_type]

    def aggregate(
        self, metrics: Iterable[MetricData], agg: Callable[[List[float]], float]
    ) -> float:
        """Aggregate metric values using the supplied function."""
        values = [m.value for m in metrics]
        return agg(values) if values else 0.0


__all__ = ["MetricsProcessor"]
