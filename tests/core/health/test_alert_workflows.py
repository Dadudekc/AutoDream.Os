import pytest

from src.core.health.alerting import (
    generate_alert,
    send_alert_notifications,
    check_escalations,
    AlertSeverity,
    EscalationLevel,
    AlertRule,
    NotificationChannel,
    NotificationConfig,
    EscalationPolicy,
)


def test_alert_dispatch_console(capfd):
    alert = generate_alert(
        "test_agent",
        AlertSeverity.WARNING,
        "Test alert message",
        "cpu_usage",
        90.0,
        85.0,
    )
    rule = AlertRule(
        rule_id="high_cpu_usage",
        name="High CPU Usage",
        description="Alert when CPU usage exceeds threshold",
        severity=AlertSeverity.WARNING,
        conditions={"metric": "cpu_usage", "operator": ">", "threshold": 85.0},
        notification_channels=[NotificationChannel.CONSOLE],
    )
    config = NotificationConfig(
        channel=NotificationChannel.CONSOLE,
        template="{severity}: {message} ({agent_id}) at {timestamp}",
    )
    send_alert_notifications(alert, rule, {NotificationChannel.CONSOLE: config})
    out, _ = capfd.readouterr()
    assert "[CONSOLE]" in out


def test_escalation_to_next_level():
    alert = generate_alert(
        "agent1",
        AlertSeverity.CRITICAL,
        "Critical response time",
        "response_time",
        6000.0,
        5000.0,
    )
    policy = EscalationPolicy(
        level=EscalationLevel.LEVEL_1,
        delay_minutes=0,
        contacts=[],
        notification_channels=[],
    )
    check_escalations({alert.alert_id: alert}, {EscalationLevel.LEVEL_1: policy}, {})
    assert alert.escalation_level == EscalationLevel.LEVEL_2
