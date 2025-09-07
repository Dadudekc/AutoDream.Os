"""Metric aggregation utilities.

Provides helpers for processing and storing collected metrics.  This module
combines the responsibilities of the previous ``metrics_collector_processor``
and ``metrics_collector_storage`` modules.
"""
from __future__ import annotations

from typing import Callable, Dict, Iterable, List

from .metrics_definitions import MetricData, MetricType


class MetricsAggregator:
    """Process and persist metrics in memory."""

    def __init__(self) -> None:
        self._data: Dict[str, List[MetricData]] = {}

    # Processing helpers -------------------------------------------------
    def normalize(self, metrics: Iterable[MetricData]) -> List[MetricData]:
        """Return a list copy of ``metrics``."""

        return list(metrics)

    def filter_by_type(
        self, metrics: Iterable[MetricData], metric_type: MetricType
    ) -> List[MetricData]:
        """Filter ``metrics`` by :class:`MetricType`."""

        return [m for m in metrics if m.metric_type == metric_type]

    def aggregate(
        self, metrics: Iterable[MetricData], agg: Callable[[List[float]], float]
    ) -> float:
        """Aggregate metric values using ``agg`` function."""

        values = [m.value for m in metrics]
        return agg(values) if values else 0.0

    # Storage helpers ----------------------------------------------------
    def store(self, metrics: List[MetricData]) -> None:
        """Store metrics grouped by metric name."""

        for metric in metrics:
            self._data.setdefault(metric.metric_name, []).append(metric)

    def get(self, name: str) -> List[MetricData]:
        """Retrieve stored metrics by name."""

        return list(self._data.get(name, []))

    def all_metrics(self) -> Dict[str, List[MetricData]]:
        """Return a copy of all stored metrics."""

        return {k: list(v) for k, v in self._data.items()}


__all__ = ["MetricsAggregator"]

