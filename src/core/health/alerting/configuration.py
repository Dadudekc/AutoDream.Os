"""Configuration helpers for the health alerting subsystem."""

from __future__ import annotations

from typing import Dict

from .models import (
    AlertRule,
    NotificationChannel,
    NotificationConfig,
    EscalationPolicy,
    EscalationLevel,
    AlertSeverity,
)


def load_default_rules() -> Dict[str, AlertRule]:
    """Return the default set of alert rules."""

    default_rules = [
        AlertRule(
            rule_id="high_cpu_usage",
            name="High CPU Usage",
            description="Alert when CPU usage exceeds threshold",
            severity=AlertSeverity.WARNING,
            conditions={
                "metric": "cpu_usage",
                "operator": ">",
                "threshold": 85.0,
                "duration": 300,
            },
            notification_channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.CONSOLE,
            ],
        ),
        AlertRule(
            rule_id="high_memory_usage",
            name="High Memory Usage",
            description="Alert when memory usage exceeds threshold",
            severity=AlertSeverity.WARNING,
            conditions={
                "metric": "memory_usage",
                "operator": ">",
                "threshold": 90.0,
                "duration": 300,
            },
            notification_channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.CONSOLE,
            ],
        ),
        AlertRule(
            rule_id="critical_response_time",
            name="Critical Response Time",
            description="Alert when response time is critically high",
            severity=AlertSeverity.CRITICAL,
            conditions={
                "metric": "response_time",
                "operator": ">",
                "threshold": 5000.0,
                "duration": 60,
            },
            notification_channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.SLACK,
                NotificationChannel.SMS,
            ],
            escalation_enabled=True,
        ),
        AlertRule(
            rule_id="high_error_rate",
            name="High Error Rate",
            description="Alert when error rate is high",
            severity=AlertSeverity.CRITICAL,
            conditions={
                "metric": "error_rate",
                "operator": ">",
                "threshold": 10.0,
                "duration": 600,
            },
            notification_channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.SLACK,
            ],
            escalation_enabled=True,
        ),
    ]

    return {rule.rule_id: rule for rule in default_rules}


def load_default_notifications() -> Dict[NotificationChannel, NotificationConfig]:
    """Return the default notification channel configurations."""

    default_configs = [
        NotificationConfig(
            channel=NotificationChannel.EMAIL,
            enabled=True,
            recipients=["admin@example.com"],
            template="Alert: {severity} - {message}",
            retry_attempts=3,
            retry_delay=60,
        ),
        NotificationConfig(
            channel=NotificationChannel.CONSOLE,
            enabled=True,
            template="[{severity}] {message}",
        ),
        NotificationConfig(
            channel=NotificationChannel.LOG,
            enabled=True,
            template="Health Alert: {severity} - {message}",
        ),
        NotificationConfig(
            channel=NotificationChannel.SLACK,
            enabled=False,
            recipients=["#alerts"],
            template=":warning: *{severity}*: {message}",
            custom_parameters={"webhook_url": "https://hooks.slack.com/..."},
        ),
    ]

    return {config.channel: config for config in default_configs}


def load_default_escalation() -> Dict[EscalationLevel, EscalationPolicy]:
    """Return the default escalation policies."""

    default_policies = [
        EscalationPolicy(
            level=EscalationLevel.LEVEL_1,
            delay_minutes=0,
            contacts=["oncall@example.com"],
            notification_channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.SMS,
            ],
            auto_escalate=True,
            require_acknowledgment=False,
        ),
        EscalationPolicy(
            level=EscalationLevel.LEVEL_2,
            delay_minutes=15,
            contacts=["supervisor@example.com"],
            notification_channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.SLACK,
            ],
            auto_escalate=True,
            require_acknowledgment=True,
        ),
        EscalationPolicy(
            level=EscalationLevel.LEVEL_3,
            delay_minutes=60,
            contacts=["manager@example.com"],
            notification_channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.SMS,
            ],
            auto_escalate=True,
            require_acknowledgment=True,
        ),
        EscalationPolicy(
            level=EscalationLevel.LEVEL_4,
            delay_minutes=240,
            contacts=["emergency@example.com"],
            notification_channels=[
                NotificationChannel.EMAIL,
                NotificationChannel.SMS,
                NotificationChannel.PAGER_DUTY,
            ],
            auto_escalate=True,
            require_acknowledgment=True,
        ),
    ]

    return {policy.level: policy for policy in default_policies}

