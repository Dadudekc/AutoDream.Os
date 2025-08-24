import pytest

from src.core.health.alerting import (
    HealthAlertingManager,
    AlertSeverity,
    EscalationLevel,
)


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
    manager._check_escalations()
    assert alert.escalation_level == EscalationLevel.LEVEL_2
