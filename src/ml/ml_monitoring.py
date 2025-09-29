#!/usr/bin/env python3
"""
ML Monitoring System
===================

Comprehensive ML monitoring and alerting system.
"""

import logging
import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any

from .ml_monitoring_core import MLMonitoringCore
from .ml_monitoring_models import Alert, AlertSeverity

logger = logging.getLogger(__name__)


class MLMonitoring:
    """Comprehensive ML monitoring and alerting system."""

    def __init__(self, metrics_path: str = "/app/metrics", retention_days: int = 30):
        """Initialize ML monitoring system."""
        self.core = MLMonitoringCore(metrics_path, retention_days)
        logger.info("ML Monitoring System initialized")

    def create_alert_rule(
        self,
        name: str,
        metric_name: str,
        threshold: float,
        severity: AlertSeverity,
        operator: str = ">",
        description: str = "",
    ) -> str:
        """Create an alert rule."""
        rule_id = str(uuid.uuid4())

        rule = {
            "id": rule_id,
            "name": name,
            "metric_name": metric_name,
            "threshold": threshold,
            "severity": severity.value,
            "operator": operator,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "active": True,
        }

        self.core.alert_rules[rule_id] = rule
        logger.info(f"Created alert rule: {name}")

        return rule_id

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert by ID."""
        return self.core.storage.resolve_alert(alert_id)

    def get_active_alerts(self) -> list[Alert]:
        """Get all active alerts."""
        alerts_data = self.core.storage.get_alerts(active_only=True)

        alerts = []
        for alert_dict in alerts_data:
            alert = Alert(
                id=alert_dict["id"],
                rule_id=alert_dict["rule_id"],
                rule_name=alert_dict["rule_name"],
                severity=AlertSeverity(alert_dict["severity"]),
                message=alert_dict["message"],
                timestamp=datetime.fromisoformat(alert_dict["timestamp"]),
                resolved=alert_dict["resolved"],
                resolved_at=datetime.fromisoformat(alert_dict["resolved_at"])
                if alert_dict["resolved_at"]
                else None,
            )
            alerts.append(alert)

        return alerts

    def add_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """Add an alert callback function."""
        self.core.add_alert_callback(callback)

    def get_monitoring_dashboard_data(self) -> dict[str, Any]:
        """Get data for monitoring dashboard."""
        active_alerts = self.get_active_alerts()

        # Get recent metrics
        recent_metrics = {}
        metric_names = ["prediction_accuracy", "training_loss", "data_drift_score"]

        for metric_name in metric_names:
            stats = self.core.get_metric_statistics(metric_name, hours=24)
            if stats:
                recent_metrics[metric_name] = stats

        return {
            "active_alerts": len(active_alerts),
            "alert_severity_counts": {
                severity.value: len([a for a in active_alerts if a.severity == severity])
                for severity in AlertSeverity
            },
            "recent_metrics": recent_metrics,
            "system_status": "healthy" if len(active_alerts) == 0 else "warning",
        }

    # Delegate core methods
    def record_metric(self, name: str, value: float, metric_type, **kwargs):
        """Record a metric."""
        return self.core.record_metric(name, value, metric_type, **kwargs)

    def record_prediction_metrics(
        self, model_name: str, version: str, predictions: list[float], actuals: list[float]
    ):
        """Record prediction-related metrics."""
        return self.core.record_prediction_metrics(model_name, version, predictions, actuals)

    def record_training_metrics(
        self, model_name: str, version: str, loss: float, accuracy: float, epoch: int
    ):
        """Record training metrics."""
        return self.core.record_training_metrics(model_name, version, loss, accuracy, epoch)

    def record_data_drift_metrics(
        self, model_name: str, version: str, drift_score: float, feature_name: str
    ):
        """Record data drift metrics."""
        return self.core.record_data_drift_metrics(model_name, version, drift_score, feature_name)

    def get_metric_history(self, metric_name: str, hours: int = 24):
        """Get metric history for a specific metric."""
        return self.core.get_metric_history(metric_name, hours)

    def get_metric_statistics(self, metric_name: str, hours: int = 24):
        """Get statistics for a metric."""
        return self.core.get_metric_statistics(metric_name, hours)
