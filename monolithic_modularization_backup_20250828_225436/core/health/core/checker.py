#!/usr/bin/env python3
"""
Health Checker Core - Agent Cellphone V2
========================================

Health checking and alert functionality for the health monitoring system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable

from src.utils.stability_improvements import stability_manager, safe_import
from ...status.status_core import LiveStatusSystem
from ...status.status_types import StatusEventType, StatusEvent
from ...health_models import (
    HealthStatus,
    HealthMetricType,
    AlertSeverity,
    HealthMetric,
    HealthSnapshot,
    HealthAlert,
    HealthThreshold,
    HealthReport,
    HealthCheck,
    HealthCheckResult,
)

# Define alert levels locally to avoid dependency on removed module
class AlertLevel:
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class HealthChecker:
    """
    Health checking and alert functionality
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.HealthChecker")
        
        # Health tracking
        self.health_metrics: Dict[str, Dict[str, HealthMetric]] = {}
        self.health_scores: Dict[str, float] = {}
        
        # Alerting system
        self.alerts: List[HealthAlert] = []
        self.alert_callbacks: List[Callable[[HealthAlert], None]] = []

        # Integration with status system
        self.status_system: Optional[LiveStatusSystem] = None

        # Configuration
        self.health_thresholds = {
            "response_time": {"warning": 1000.0, "critical": 5000.0},  # ms
            "error_rate": {"warning": 0.05, "critical": 0.20},  # percentage
            "availability": {"warning": 0.95, "critical": 0.80},  # percentage
            "throughput": {"warning": 100.0, "critical": 50.0},  # requests/sec
            "memory_usage": {"warning": 0.80, "critical": 0.95},  # percentage
            "cpu_usage": {"warning": 0.70, "critical": 0.90},  # percentage
        }

    def set_status_system(self, status_system: LiveStatusSystem):
        """Set the status system for integration"""
        self.status_system = status_system

    def register_component(self, component_id: str):
        """Register a component for health checking"""
        self.health_metrics[component_id] = {}
        self.health_scores[component_id] = 1.0

    def unregister_component(self, component_id: str):
        """Unregister a component from health checking"""
        if component_id in self.health_metrics:
            del self.health_metrics[component_id]
        if component_id in self.health_scores:
            del self.health_scores[component_id]

    def update_component_metrics(
        self, component_id: str, metrics_data: Dict[str, float]
    ):
        """Update health metrics for a component"""
        if component_id not in self.health_metrics:
            return

        current_time = time.time()

        for metric_name, value in metrics_data.items():
            if metric_name not in self.health_metrics[component_id]:
                # Create new metric
                thresholds = self.health_thresholds.get(
                    metric_name, {"warning": 100.0, "critical": 200.0}
                )
                metric = HealthMetric(
                    name=metric_name,
                    value=value,
                    unit=self._get_metric_unit(metric_name),
                    threshold_warning=thresholds["warning"],
                    threshold_critical=thresholds["critical"],
                    timestamp=current_time,
                )
                self.health_metrics[component_id][metric_name] = metric
            else:
                # Update existing metric
                metric = self.health_metrics[component_id][metric_name]
                metric.trend.append(metric.value)
                if len(metric.trend) > 10:  # Keep last 10 values
                    metric.trend.pop(0)
                metric.value = value
                metric.timestamp = current_time

    def mark_component_failed(self, component_id: str, error_message: str):
        """Mark a component as failed"""
        if component_id in self.health_metrics:
            for metric in self.health_metrics[component_id].values():
                metric.value = metric.threshold_critical * 1.5  # Mark as critical

        self.health_scores[component_id] = 0.0

        # Create alert
        self._create_alert(
            component_id,
            "health_check",
            AlertLevel.CRITICAL,
            f"Component health check failed: {error_message}",
        )

    def update_health_scores(self):
        """Update overall health scores for all components"""
        for component_id in self.health_metrics:
            if component_id not in self.health_scores:
                self.health_scores[component_id] = 1.0

            metrics = self.health_metrics[component_id]
            if not metrics:
                continue

            # Calculate weighted health score
            total_weight = 0
            weighted_score = 0

            for metric in metrics.values():
                weight = self._get_metric_weight(metric.name)
                status = metric.get_status()

                if status == HealthStatus.EXCELLENT:
                    score = 1.0
                elif status == HealthStatus.GOOD:
                    score = 0.8
                elif status == HealthStatus.WARNING:
                    score = 0.5
                elif status == HealthStatus.CRITICAL:
                    score = 0.2
                else:
                    score = 0.0

                weighted_score += score * weight
                total_weight += weight

            if total_weight > 0:
                self.health_scores[component_id] = weighted_score / total_weight

    def check_alert_conditions(self):
        """Check for alert conditions and create alerts"""
        for component_id, metrics in self.health_metrics.items():
            for metric_name, metric in metrics.items():
                status = metric.get_status()

                if status in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
                    alert_level = (
                        AlertLevel.CRITICAL
                        if status == HealthStatus.CRITICAL
                        else AlertLevel.WARNING
                    )
                    message = f"{metric_name} is {status.value}: {metric.value}{metric.unit}"

                    # Check if alert already exists
                    existing_alert = self._find_existing_alert(
                        component_id, metric_name
                    )
                    if not existing_alert:
                        self._create_alert(
                            component_id, metric_name, alert_level, message
                        )

    def _create_alert(
        self, component_id: str, metric_name: str, alert_level: str, message: str
    ):
        """Create a new health alert"""
        alert = HealthAlert(
            alert_id=f"alert_{int(time.time())}_{component_id}_{metric_name}",
            component_id=component_id,
            metric_name=metric_name,
            alert_level=alert_level,
            message=message,
            timestamp=time.time(),
        )

        self.alerts.append(alert)

        # Notify callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Alert callback failed: {e}")

        # Integrate with status system
        if self.status_system:
            self.status_system._create_status_event(
                StatusEventType.HEALTH_ALERT,
                component_id,
                message,
                {"alert_level": alert_level, "metric": metric_name},
                "high"
                if alert_level in [AlertLevel.ERROR, AlertLevel.CRITICAL]
                else "medium",
            )

        self.logger.warning(f"Health alert created: {component_id} - {message}")

    def _find_existing_alert(
        self, component_id: str, metric_name: str
    ) -> Optional[HealthAlert]:
        """Find existing alert for component and metric"""
        for alert in self.alerts:
            if (
                alert.component_id == component_id
                and alert.metric_name == metric_name
                and not alert.is_acknowledged
            ):
                return alert
        return None

    def _get_metric_unit(self, metric_name: str) -> str:
        """Get unit for a metric"""
        units = {
            "response_time": "ms",
            "error_rate": "%",
            "availability": "%",
            "throughput": "req/s",
            "memory_usage": "%",
            "cpu_usage": "%",
        }
        return units.get(metric_name, "")

    def _get_metric_weight(self, metric_name: str) -> float:
        """Get weight for a metric in health score calculation"""
        weights = {
            "response_time": 0.25,
            "error_rate": 0.30,
            "availability": 0.25,
            "throughput": 0.10,
            "memory_usage": 0.05,
            "cpu_usage": 0.05,
        }
        return weights.get(metric_name, 0.1)

    def get_health_metrics(self) -> Dict[str, Dict[str, HealthMetric]]:
        """Get all health metrics"""
        return self.health_metrics

    def get_health_scores(self) -> Dict[str, float]:
        """Get all health scores"""
        return self.health_scores

    def get_alerts(self) -> List[HealthAlert]:
        """Get all alerts"""
        return self.alerts
