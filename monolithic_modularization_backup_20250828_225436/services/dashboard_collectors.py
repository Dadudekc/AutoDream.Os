"""Data collection module for dashboard metrics."""

from __future__ import annotations

from typing import Dict, List

from .dashboard_utils import TIMESTAMP_KEY, VALUE_KEY, current_timestamp


class MetricsCollector:
    """Collects metric data points."""

    def __init__(self) -> None:
        self.metrics: Dict[str, List[Dict[str, float]]] = {}

    def record(self, name: str, value: float) -> None:
        """Record a metric value with a timestamp."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(
            {TIMESTAMP_KEY: current_timestamp(), VALUE_KEY: value}
        )
