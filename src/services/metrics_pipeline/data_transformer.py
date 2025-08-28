"""Transform collected metrics into useful summaries."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from .metrics_config import (
    SUMMARY_METRICS_TRACKED,
    SUMMARY_TOTAL_METRICS,
    MetricRecord,
)


class MetricsTransformer:
    """Provides simple aggregation helpers for metric data."""

    def summarize(self, metrics: Dict[str, List[MetricRecord]]) -> Dict[str, int | str]:
        """Return a summary dictionary for the provided metrics."""

        total = sum(len(values) for values in metrics.values())
        return {
            SUMMARY_TOTAL_METRICS: total,
            SUMMARY_METRICS_TRACKED: len(metrics),
            "timestamp": datetime.now().isoformat(),
        }


__all__ = ["MetricsTransformer"]
