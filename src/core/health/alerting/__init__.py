"""
Health Alerting Package

This package contains modules for health alerting and notification management.
"""

from .manager import HealthAlertingManager
from .models import (
    AlertSeverity,
    AlertStatus,
    NotificationChannel,
    EscalationLevel,
    AlertRule,
    HealthAlert,
    NotificationConfig,
    EscalationPolicy,
)

__all__ = [
    "HealthAlertingManager",
    "AlertSeverity",
    "AlertStatus",
    "NotificationChannel",
    "EscalationLevel",
    "AlertRule",
    "HealthAlert",
    "NotificationConfig",
    "EscalationPolicy",
]
