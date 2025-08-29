from __future__ import annotations

"""High-level interface for decision metrics."""

import uuid
from datetime import datetime
from typing import Dict

from ..decision_types import DecisionType
from .calculator import (
    check_alerts,
    get_performance_score,
    get_summary,
    update_metrics,
)
from .definitions import DecisionMetrics, MetricsSnapshot, PerformanceAlert
from .storage import MetricsStorage


class DecisionMetricsManager:
    """Coordinate metric calculation and storage."""

    def __init__(self, storage: MetricsStorage | None = None) -> None:
        self.storage = storage or MetricsStorage()

    def record_decision(
        self,
        decision_type: DecisionType,
        success: bool,
        execution_time: float,
        confidence: float,
    ) -> DecisionMetrics:
        """Record a single decision's metrics."""
        metrics_id = decision_type.value
        metrics = self.storage.get_metrics(metrics_id)
        if metrics is None:
            metrics = DecisionMetrics(metrics_id=metrics_id, decision_type=decision_type)
            self.storage.save_metrics(metrics)

        update_metrics(metrics, success, execution_time, confidence)
        for message in check_alerts(metrics):
            alert = PerformanceAlert(
                alert_id=str(uuid.uuid4()),
                alert_type="threshold",
                severity="warning",
                message=message,
                threshold_value=0.0,
                current_value=0.0,
            )
            self.storage.add_alert(alert)
        return metrics

    def create_snapshot(self) -> MetricsSnapshot:
        """Persist a snapshot of all metrics."""
        total_decisions = sum(m.total_decisions for m in self.storage.metrics.values())
        successful_decisions = sum(m.successful_decisions for m in self.storage.metrics.values())
        failed_decisions = sum(m.failed_decisions for m in self.storage.metrics.values())
        average_time = (
            sum(m.average_execution_time for m in self.storage.metrics.values()) / len(self.storage.metrics)
            if self.storage.metrics
            else 0.0
        )
        success_rate = (successful_decisions / total_decisions) if total_decisions else 0.0
        performance_score = (
            sum(get_performance_score(m) for m in self.storage.metrics.values()) / len(self.storage.metrics)
            if self.storage.metrics
            else 0.0
        )

        snapshot = MetricsSnapshot(
            snapshot_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            total_decisions=total_decisions,
            successful_decisions=successful_decisions,
            failed_decisions=failed_decisions,
            average_decision_time=average_time,
            success_rate=success_rate,
            performance_score=performance_score,
            metrics_data={m.metrics_id: get_summary(m) for m in self.storage.metrics.values()},
        )
        self.storage.add_snapshot(snapshot)
        return snapshot

    def get_metrics_summary(self) -> Dict[str, Dict[str, float]]:
        """Return summaries for all tracked metrics."""
        return {m_id: get_summary(m) for m_id, m in self.storage.metrics.items()}
