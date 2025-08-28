#!/usr/bin/env python3
"""
Health Alerting Package - V2 Modular Architecture
================================================

Health alert creation and management system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .alert_detection import (
    generate_alert,
    find_applicable_rule,
    should_suppress_alert,
)
from .notification_dispatch import send_alert_notifications
from .escalation import check_escalations
from .health_alert_manager import HealthAlertManager
from .models import (
    AlertRule,
    AlertSeverity,
    EscalationLevel,
    EscalationPolicy,
    NotificationChannel,
    NotificationConfig,
)

__all__ = [
    "generate_alert",
    "find_applicable_rule",
    "should_suppress_alert",
    "send_alert_notifications",
    "check_escalations",
    "AlertSeverity",
    "EscalationLevel",
    "AlertRule",
    "NotificationChannel",
    "NotificationConfig",
    "EscalationPolicy",
    "HealthAlertManager",
]
