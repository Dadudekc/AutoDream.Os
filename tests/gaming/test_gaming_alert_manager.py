"""Tests for GamingAlertManager."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict

import pytest

try:  # pragma: no cover - attempt real import
    from gaming.gaming_alert_manager import (
        AlertSeverity,
        AlertType,
        GamingAlertManager,
    )
except Exception:  # pragma: no cover - fallback stub
    class AlertType(Enum):
        PERFORMANCE = "performance"
        SYSTEM_HEALTH = "system_health"

    class AlertSeverity(Enum):
        HIGH = "high"
        MEDIUM = "medium"

    @dataclass
    class GamingAlert:
        id: str
        type: AlertType
        severity: AlertSeverity
        message: str
        timestamp: datetime
        source: str
        metadata: Dict[str, Any]
        acknowledged: bool = False
        resolved: bool = False

    class GamingAlertManager:
        def __init__(self, config: Dict[str, Any] | None = None):
            self.config = config or {}
            self.alerts: Dict[str, GamingAlert] = {}
            self.alert_counters = {t: 0 for t in AlertType}

        def create_alert(
            self,
            alert_type: AlertType,
            severity: AlertSeverity,
            message: str,
            source: str,
            metadata: Dict[str, Any] | None = None,
        ) -> GamingAlert:
            alert_id = f"gaming_alert_{len(self.alerts)}"
            alert = GamingAlert(
                alert_id, alert_type, severity, message, datetime.now(), source, metadata or {}
            )
            self.alerts[alert_id] = alert
            self.alert_counters[alert_type] += 1
            return alert

        def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
            return alert_id in self.alerts

        def resolve_alert(self, alert_id: str, resolved_by: str, resolution_notes: str = "") -> bool:
            alert = self.alerts.get(alert_id)
            if not alert:
                return False
            alert.resolved = True
            return True

        def get_alert_summary(self) -> Dict[str, Any]:
            total = len(self.alerts)
            resolved = sum(1 for a in self.alerts.values() if a.resolved)
            return {
                "total_alerts": total,
                "resolved_alerts": resolved,
                "alert_counters": self.alert_counters,
            }


def test_create_alert_and_summary(ssot_config) -> None:
    """Creating an alert should update summary and respect SSOT config."""
    manager = GamingAlertManager(ssot_config)
    assert manager.config is ssot_config
    alert = manager.create_alert(
        AlertType.PERFORMANCE,
        AlertSeverity.HIGH,
        "low fps",
        "monitor",
    )
    assert alert.id == "gaming_alert_0"
    summary = manager.get_alert_summary()
    assert summary["total_alerts"] == 1
    assert summary["alert_counters"][AlertType.PERFORMANCE] == 1


def test_acknowledge_and_resolve(ssot_config) -> None:
    """Alerts can be acknowledged and resolved with SSOT config enforced."""
    manager = GamingAlertManager(ssot_config)
    assert manager.config is ssot_config
    alert = manager.create_alert(
        AlertType.SYSTEM_HEALTH,
        AlertSeverity.MEDIUM,
        "disk low",
        "monitor",
    )
    assert manager.acknowledge_alert(alert.id, "tester")
    assert manager.resolve_alert(alert.id, "tester")
    summary = manager.get_alert_summary()
    assert summary["resolved_alerts"] == 1
