from __future__ import annotations

"""Metric aggregation utilities."""

from collections import defaultdict
from typing import Dict, Iterable, List
import threading

from .adapters import Metric


class MetricAggregator:
    """Aggregate metrics in a thread safe manner."""

    def __init__(self) -> None:
        self._metrics: List[Metric] = []
        self._lock = threading.Lock()

    def add(self, metrics: Iterable[Metric]) -> None:
        """Store metrics for later aggregation."""
        with self._lock:
            self._metrics.extend(list(metrics))

    def summary(self) -> Dict[str, float]:
        """Return the average value for each metric name."""
        with self._lock:
            totals: Dict[str, float] = defaultdict(float)
            counts: Dict[str, int] = defaultdict(int)
            for metric in self._metrics:
                totals[metric.name] += metric.value
                counts[metric.name] += 1

        return {name: totals[name] / counts[name] for name in totals}
