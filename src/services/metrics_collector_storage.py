"""Simple in-memory storage for collected metrics."""
from __future__ import annotations

from typing import Dict, List

from .performance_monitor import MetricData


class MetricsStorage:
    """Store metrics in memory keyed by metric name."""

    def __init__(self):
        self._data: Dict[str, List[MetricData]] = {}

    def store(self, metrics: List[MetricData]) -> None:
        for metric in metrics:
            self._data.setdefault(metric.metric_name, []).append(metric)

    def get(self, name: str) -> List[MetricData]:
        return list(self._data.get(name, []))

    def all_metrics(self) -> Dict[str, List[MetricData]]:
        return {k: list(v) for k, v in self._data.items()}


__all__ = ["MetricsStorage"]
