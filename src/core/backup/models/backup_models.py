import logging

logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Backup Data Models - V2 Compliant Module
======================================

Data models for backup monitoring system with V2 compliance validation.
V2 COMPLIANT: Focused data models under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .backup_enums import (
    AlertSeverity,
    AlertStatus,
    AlertType,
    HealthCheckStatus,
    HealthCheckType,
    MetricType,
    MonitoringStatus,
)


@dataclass
class Alert:
    """Alert data model."""

    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    status: AlertStatus = AlertStatus.ACTIVE
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    escalation_count: int = 0
    last_escalation: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def acknowledge(self, acknowledged_by: str) -> None:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.backup.models.backup_models import Backup_Models

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Backup_Models(config)

# Execute primary functionality
result = component.process_data(input_data)
logger.info(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    logger.info(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    logger.info(f"Operation failed: {e}")
    # Implement recovery logic

        """Acknowledge the alert."""
        self.acknowledged = True
        self.acknowledged_by = acknowledged_by
        self.acknowledged_at = datetime.now()
        self.status = AlertStatus.ACKNOWLEDGED

    def resolve(self) -> None:
        """Resolve the alert."""
        self.resolved_at = datetime.now()
        self.status = AlertStatus.RESOLVED

    def escalate(self) -> None:
        """Escalate the alert."""
        self.escalation_count += 1
        self.last_escalation = datetime.now()
        self.status = AlertStatus.ESCALATED


@dataclass
class HealthCheck:
    """Health check data model."""

    check_name: str
    check_type: HealthCheckType
    status: HealthCheckStatus
    message: Optional[str] = None
    duration_ms: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)

    def update_status(self, status: HealthCheckStatus, message: Optional[str] = None,
                      duration_ms: Optional[int] = None) -> None:
        """Update health check status."""
        self.status = status
        self.message = message
        self.duration_ms = duration_ms
        self.timestamp = datetime.now()


@dataclass
class MonitoringMetric:
    """Monitoring metric data model."""

    metric_name: str
    metric_value: float
    metric_unit: Optional[str] = None
    metric_type: MetricType = MetricType.GAUGE
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary."""
        return {
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "metric_unit": self.metric_unit,
            "metric_type": self.metric_type.value,
            "timestamp": self.timestamp.isoformat(),
            "tags": self.tags,
            "metadata": self.metadata,
        }


@dataclass
class MonitoringConfig:
    """Monitoring configuration data model."""

    enabled: bool = True
    check_interval_seconds: int = 60
    health_check_interval_seconds: int = 300
    metrics_retention_days: int = 30
    alert_channels: List[str] = field(default_factory=lambda: ["console", "file"])
    notification_cooldown_minutes: int = 30

    # Thresholds
    backup_age_hours_threshold: int = 48
    disk_usage_percent_threshold: int = 85
    backup_failure_rate_threshold: float = 20.0
    recovery_time_minutes_threshold: int = 120
    data_integrity_failures_threshold: int = 1
    system_load_percent_threshold: int = 80
    memory_usage_percent_threshold: int = 90

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "enabled": self.enabled,
            "check_interval_seconds": self.check_interval_seconds,
            "health_check_interval_seconds": self.health_check_interval_seconds,
            "metrics_retention_days": self.metrics_retention_days,
            "alert_channels": self.alert_channels,
            "notification_cooldown_minutes": self.notification_cooldown_minutes,
            "thresholds": {
                "backup_age_hours": self.backup_age_hours_threshold,
                "disk_usage_percent": self.disk_usage_percent_threshold,
                "backup_failure_rate_percent": self.backup_failure_rate_threshold,
                "recovery_time_minutes": self.recovery_time_minutes_threshold,
                "data_integrity_failures": self.data_integrity_failures_threshold,
                "system_load_percent": self.system_load_percent_threshold,
                "memory_usage_percent": self.memory_usage_percent_threshold,
            }
        }


@dataclass
class AlertHistory:
    """Alert history data model."""

    alert_id: str
    action: str
    details: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringDashboard:
    """Monitoring dashboard data model."""

    dashboard_id: str
    title: str
    description: str
    widgets: List[Dict[str, Any]] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    refresh_interval_seconds: int = 60

    def add_widget(self, widget_id: str, widget_type: str, title: str,
                   config: Dict[str, Any]) -> None:
        """Add a widget to the dashboard."""
        widget = {
            "id": widget_id,
            "type": widget_type,
            "title": title,
            "config": config,
            "position": {"x": 0, "y": len(self.widgets)},
            "size": {"width": 6, "height": 4}
        }
        self.widgets.append(widget)
        self.last_updated = datetime.now()
