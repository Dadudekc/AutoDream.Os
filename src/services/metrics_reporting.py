"""Reporting utilities for collected metrics."""
from __future__ import annotations

from typing import Dict

from .metrics_common import THRESHOLDS, above_threshold
from .metrics_collector_storage import MetricsStorage


class MetricsReporter:
    """Generate simple reports for collected metrics."""

    def __init__(self, storage: MetricsStorage) -> None:
        self.storage = storage

    def generate_report(self) -> Dict[str, Dict[str, float]]:
        """Return metrics exceeding configured thresholds."""
        report: Dict[str, Dict[str, float]] = {}
        for name, metrics in self.storage.all_metrics().items():
            if not metrics:
                continue
            latest = metrics[-1].value
            if above_threshold(name, latest):
                report[name] = {"value": latest, "threshold": THRESHOLDS[name]}
        return report

    def summarize(self) -> Dict[str, float]:
        """Return the average value for each stored metric."""
        summary: Dict[str, float] = {}
        for name, metrics in self.storage.all_metrics().items():
            if metrics:
                summary[name] = sum(m.value for m in metrics) / len(metrics)
        return summary


__all__ = ["MetricsReporter"]
