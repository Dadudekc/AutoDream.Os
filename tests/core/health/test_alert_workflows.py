import pytest

from src.core.health.alerting import (
    HealthAlertingManager,
    AlertSeverity,
    EscalationLevel,
    NotificationChannel,
)
from src.core.health.alerting.escalation import check_escalations


def test_alert_dispatch_console(capfd):
    manager = HealthAlertingManager()
    manager.create_alert(
        "test_agent",
        AlertSeverity.WARNING,
        "Test alert message",
        "cpu_usage",
        90.0,
        85.0,
    )
    out, _ = capfd.readouterr()
    assert "[CONSOLE]" in out


def test_escalation_to_next_level():
    manager = HealthAlertingManager()
    alert_id = manager.create_alert(
        "agent1",
        AlertSeverity.CRITICAL,
        "Critical response time",
        "response_time",
        6000.0,
        5000.0,
    )
    alert = manager.get_alert(alert_id)
    assert alert.escalation_level == EscalationLevel.LEVEL_1
    check_escalations(
        manager.alerts, manager.escalation_policies, manager.notification_configs
    )
    assert alert.escalation_level == EscalationLevel.LEVEL_2


def test_alert_suppression_due_to_cooldown():
    manager = HealthAlertingManager()
    alert_id = manager.create_alert(
        "agent1",
        AlertSeverity.WARNING,
        "High CPU",
        "cpu_usage",
        90.0,
        85.0,
    )
    assert alert_id != ""
    suppressed = manager.create_alert(
        "agent1",
        AlertSeverity.WARNING,
        "High CPU",
        "cpu_usage",
        92.0,
        85.0,
    )
    assert suppressed == ""


def test_disabled_channel_no_output(capfd):
    manager = HealthAlertingManager()
    manager.notification_configs[NotificationChannel.CONSOLE].enabled = False
    manager.create_alert(
        "agent1",
        AlertSeverity.WARNING,
        "High CPU",
        "cpu_usage",
        90.0,
        85.0,
    )
    out, _ = capfd.readouterr()
    assert "[CONSOLE]" not in out
