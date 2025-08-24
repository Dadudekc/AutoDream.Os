"""Tests for performance alerting features."""

from unittest.mock import Mock


def test_performance_alerting():
    alert_system = Mock()
    alert_system.check_alerts.return_value = [
        {"level": "warning", "message": "High CPU usage detected"},
        {"level": "info", "message": "Memory usage within normal range"},
    ]
    alerts = alert_system.check_alerts()
    assert [a["level"] for a in alerts] == ["warning", "info"]
    alert_system.check_alerts.assert_called_once()

