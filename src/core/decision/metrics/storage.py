from __future__ import annotations

"""Simple in-memory storage for decision metrics."""

from typing import Dict, List, Optional

from .definitions import DecisionMetrics, MetricsSnapshot, PerformanceAlert


class MetricsStorage:
    """Store metrics, snapshots, and alerts."""

    def __init__(self) -> None:
        self.metrics: Dict[str, DecisionMetrics] = {}
        self.snapshots: List[MetricsSnapshot] = []
        self.alerts: List[PerformanceAlert] = []

    def save_metrics(self, metrics: DecisionMetrics) -> None:
        """Persist metrics instance."""
        self.metrics[metrics.metrics_id] = metrics

    def get_metrics(self, metrics_id: str) -> Optional[DecisionMetrics]:
        """Retrieve metrics by identifier."""
        return self.metrics.get(metrics_id)

    def add_snapshot(self, snapshot: MetricsSnapshot) -> None:
        """Store a metrics snapshot."""
        self.snapshots.append(snapshot)

    def add_alert(self, alert: PerformanceAlert) -> None:
        """Store a performance alert."""
        self.alerts.append(alert)
