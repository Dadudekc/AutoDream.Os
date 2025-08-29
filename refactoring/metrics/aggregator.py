from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class Metric:
    """Simple representation of a collected metric sample."""

    source: str
    name: str
    value: float
    timestamp: float


class MetricsAggregator:
    """Aggregate metrics and provide summary statistics."""

    def __init__(self) -> None:
        self._metrics: List[Metric] = []

    def add(self, metrics: Iterable[Metric]) -> None:
        """Add an iterable of metrics to the aggregator."""
        self._metrics.extend(list(metrics))

    def summary(self) -> Dict[str, object]:
        """Return summary statistics for the collected metrics."""
        totals: Dict[str, float] = defaultdict(float)
        counts: Dict[str, int] = defaultdict(int)
        for metric in self._metrics:
            totals[metric.name] += metric.value
            counts[metric.name] += 1
        averages = {name: totals[name] / counts[name] for name in totals}
        return {
            "averages": averages,
            "total_metrics": sum(counts.values()),
            "metrics_tracked": len(counts),
        }
