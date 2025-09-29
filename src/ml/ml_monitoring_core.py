#!/usr/bin/env python3
"""
ML Monitoring Core
=================

Core monitoring functionality for ML systems.
"""

import logging
import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any

from .ml_monitoring_models import Alert, AlertSeverity, MetricData, MetricType
from .ml_monitoring_storage import MLMonitoringStorage

logger = logging.getLogger(__name__)


class MLMonitoringCore:
    """Core ML monitoring functionality."""

    def __init__(self, metrics_path: str = "/app/metrics", retention_days: int = 30):
        """Initialize ML monitoring core."""
        self.storage = MLMonitoringStorage(metrics_path, retention_days)
        self.alert_rules: dict[str, dict[str, Any]] = {}
        self.alert_callbacks: list[Callable[[Alert], None]] = []

        logger.info("ML Monitoring Core initialized")

    def record_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType,
        labels: dict[str, str] = None,
        model_name: str = None,
        model_version: str = None,
    ) -> None:
        """Record a metric."""
        if labels is None:
            labels = {}

        metric_data = MetricData(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.now(),
            labels=labels,
            model_name=model_name,
            model_version=model_version,
        )

        self.storage.add_metric(metric_data)

        # Check for alerts
        self._check_alerts(name, value)

        logger.debug(f"Recorded metric: {name}={value}")

    def record_prediction_metrics(
        self, model_name: str, version: str, predictions: list[float], actuals: list[float]
    ) -> None:
        """Record prediction-related metrics."""
        if len(predictions) != len(actuals):
            logger.warning("Mismatch between predictions and actuals length")
            return

        # Calculate accuracy
        correct = sum(1 for p, a in zip(predictions, actuals, strict=False) if abs(p - a) < 0.1)
        accuracy = correct / len(predictions) if predictions else 0

        # Record metrics
        self.record_metric(
            "prediction_accuracy",
            accuracy,
            MetricType.GAUGE,
            {"model": model_name, "version": version},
            model_name,
            version,
        )

        # Record prediction count
        self.record_metric(
            "prediction_count",
            len(predictions),
            MetricType.COUNTER,
            {"model": model_name, "version": version},
            model_name,
            version,
        )

    def record_training_metrics(
        self, model_name: str, version: str, loss: float, accuracy: float, epoch: int
    ) -> None:
        """Record training metrics."""
        labels = {"model": model_name, "version": version, "epoch": str(epoch)}

        self.record_metric("training_loss", loss, MetricType.GAUGE, labels, model_name, version)
        self.record_metric(
            "training_accuracy", accuracy, MetricType.GAUGE, labels, model_name, version
        )

    def record_data_drift_metrics(
        self, model_name: str, version: str, drift_score: float, feature_name: str
    ) -> None:
        """Record data drift metrics."""
        labels = {"model": model_name, "version": version, "feature": feature_name}

        self.record_metric(
            "data_drift_score", drift_score, MetricType.GAUGE, labels, model_name, version
        )

    def get_metric_history(self, metric_name: str, hours: int = 24) -> list[MetricData]:
        """Get metric history for a specific metric."""
        metrics_data = self.storage.get_metrics(metric_name, hours)

        history = []
        for metric_dict in metrics_data:
            metric_data = MetricData(
                name=metric_dict["name"],
                value=metric_dict["value"],
                metric_type=MetricType(metric_dict["metric_type"]),
                timestamp=datetime.fromisoformat(metric_dict["timestamp"]),
                labels=metric_dict["labels"],
                model_name=metric_dict.get("model_name"),
                model_version=metric_dict.get("model_version"),
            )
            history.append(metric_data)

        return history

    def get_metric_statistics(self, metric_name: str, hours: int = 24) -> dict[str, float]:
        """Get statistics for a metric."""
        history = self.get_metric_history(metric_name, hours)

        if not history:
            return {}

        values = [m.value for m in history]

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "latest": values[-1] if values else 0,
        }

    def _check_alerts(self, metric_name: str, value: float) -> None:
        """Check if any alert rules are triggered."""
        for rule_id, rule in self.alert_rules.items():
            if rule["metric_name"] == metric_name:
                threshold = rule["threshold"]
                operator = rule.get("operator", ">")

                triggered = False
                if operator == ">":
                    triggered = value > threshold
                elif operator == "<":
                    triggered = value < threshold
                elif operator == ">=":
                    triggered = value >= threshold
                elif operator == "<=":
                    triggered = value <= threshold
                elif operator == "==":
                    triggered = value == threshold

                if triggered:
                    self._trigger_alert(rule_id, rule, value)

    def _trigger_alert(self, rule_id: str, rule: dict[str, Any], current_value: float) -> None:
        """Trigger an alert."""
        alert = Alert(
            id=str(uuid.uuid4()),
            rule_id=rule_id,
            rule_name=rule["name"],
            severity=AlertSeverity(rule["severity"]),
            message=f"Alert triggered: {rule['name']} - {rule['metric_name']} = {current_value}",
            timestamp=datetime.now(),
        )

        self.storage.add_alert(alert)

        # Call registered callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

        logger.warning(f"Alert triggered: {alert.message}")

    def add_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """Add an alert callback function."""
        self.alert_callbacks.append(callback)
        logger.info("Alert callback added")
