#!/usr/bin/env python3
"""
ML Monitoring Storage
====================

Storage operations for ML monitoring system.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .ml_monitoring_models import Alert, MetricData

logger = logging.getLogger(__name__)


class MLMonitoringStorage:
    """Storage operations for ML monitoring data."""

    def __init__(self, metrics_path: str = "/app/metrics", retention_days: int = 30):
        """Initialize storage with metrics path and retention policy."""
        self.metrics_path = Path(metrics_path)
        self.retention_days = retention_days
        self.metrics_file = self.metrics_path / "metrics.json"
        self.alerts_file = self.metrics_path / "alerts.json"

        # Ensure metrics directory exists
        self.metrics_path.mkdir(parents=True, exist_ok=True)

        # Initialize storage
        self.metrics: list[dict[str, Any]] = []
        self.alerts: list[dict[str, Any]] = []

        self._load_metrics()
        self._load_alerts()

    def _load_metrics(self) -> None:
        """Load metrics from storage."""
        try:
            if self.metrics_file.exists():
                with open(self.metrics_file) as f:
                    self.metrics = json.load(f)
                logger.info(f"Loaded {len(self.metrics)} metrics from storage")
            else:
                self.metrics = []
                logger.info("No existing metrics found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
            self.metrics = []

    def _save_metrics(self) -> None:
        """Save metrics to storage."""
        try:
            # Clean up old metrics based on retention policy
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            self.metrics = [
                m for m in self.metrics if datetime.fromisoformat(m["timestamp"]) > cutoff_date
            ]

            # Save to file
            with open(self.metrics_file, "w") as f:
                json.dump(self.metrics, f, indent=2)

            logger.debug(f"Saved {len(self.metrics)} metrics to storage")
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

    def _load_alerts(self) -> None:
        """Load alerts from storage."""
        try:
            if self.alerts_file.exists():
                with open(self.alerts_file) as f:
                    self.alerts = json.load(f)
                logger.info(f"Loaded {len(self.alerts)} alerts from storage")
            else:
                self.alerts = []
                logger.info("No existing alerts found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading alerts: {e}")
            self.alerts = []

    def _save_alerts(self) -> None:
        """Save alerts to storage."""
        try:
            with open(self.alerts_file, "w") as f:
                json.dump(self.alerts, f, indent=2)

            logger.debug(f"Saved {len(self.alerts)} alerts to storage")
        except Exception as e:
            logger.error(f"Error saving alerts: {e}")

    def add_metric(self, metric_data: MetricData) -> None:
        """Add a metric to storage."""
        metric_dict = {
            "name": metric_data.name,
            "value": metric_data.value,
            "metric_type": metric_data.metric_type.value,
            "timestamp": metric_data.timestamp.isoformat(),
            "labels": metric_data.labels,
            "model_name": metric_data.model_name,
            "model_version": metric_data.model_version,
        }

        self.metrics.append(metric_dict)
        self._save_metrics()

    def add_alert(self, alert: Alert) -> None:
        """Add an alert to storage."""
        alert_dict = {
            "id": alert.id,
            "rule_id": alert.rule_id,
            "rule_name": alert.rule_name,
            "severity": alert.severity.value,
            "message": alert.message,
            "timestamp": alert.timestamp.isoformat(),
            "resolved": alert.resolved,
            "resolved_at": alert.resolved_at.isoformat() if alert.resolved_at else None,
        }

        self.alerts.append(alert_dict)
        self._save_alerts()

    def get_metrics(self, metric_name: str = None, hours: int = 24) -> list[dict[str, Any]]:
        """Get metrics filtered by name and time range."""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        filtered_metrics = []
        for metric in self.metrics:
            metric_time = datetime.fromisoformat(metric["timestamp"])
            if metric_time > cutoff_time:
                if metric_name is None or metric["name"] == metric_name:
                    filtered_metrics.append(metric)

        return filtered_metrics

    def get_alerts(self, active_only: bool = True) -> list[dict[str, Any]]:
        """Get alerts, optionally filtered to active only."""
        if active_only:
            return [alert for alert in self.alerts if not alert["resolved"]]
        return self.alerts

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert by ID."""
        for alert in self.alerts:
            if alert["id"] == alert_id and not alert["resolved"]:
                alert["resolved"] = True
                alert["resolved_at"] = datetime.now().isoformat()
                self._save_alerts()
                return True
        return False
