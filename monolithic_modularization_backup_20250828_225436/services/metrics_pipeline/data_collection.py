"""Metrics data collection utilities."""

from __future__ import annotations

import time
from typing import Dict, List

from .metrics_config import MetricRecord


class MetricsDataCollector:
    """Collects metric values in memory."""

    def __init__(self) -> None:
        self.metrics: Dict[str, List[MetricRecord]] = {}

    def record(self, name: str, value: float) -> None:
        """Record a metric value under ``name``."""

        self.metrics.setdefault(name, []).append(
            MetricRecord(timestamp=time.time(), value=value)
        )


__all__ = ["MetricsDataCollector"]
