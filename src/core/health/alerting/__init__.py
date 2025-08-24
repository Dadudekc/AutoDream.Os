"""Health Alerting Package

Utilities for generating health alerts, dispatching notifications and
handling escalation policies. The legacy ``HealthAlertingManager`` has
been removed in favour of these focused modules.
"""

from .alert_generation import (
    generate_alert,
    should_suppress_alert,
    rule_matches_alert,
    find_applicable_rule,
)
from .channel_dispatch import (
    send_alert_notifications,
    send_notification,
)
from .escalation import (
    check_escalations,
    escalate_alert,
    get_next_escalation_level,
    send_escalation_notifications,
)
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
    # Alert generation
    "generate_alert",
    "should_suppress_alert",
    "rule_matches_alert",
    "find_applicable_rule",

    # Notification dispatch
    "send_alert_notifications",
    "send_notification",

    # Escalation utilities
    "check_escalations",
    "escalate_alert",
    "get_next_escalation_level",
    "send_escalation_notifications",

    # Data models
    "AlertSeverity",
    "AlertStatus",
    "NotificationChannel",
    "EscalationLevel",
    "AlertRule",
    "HealthAlert",
    "NotificationConfig",
    "EscalationPolicy",
]
