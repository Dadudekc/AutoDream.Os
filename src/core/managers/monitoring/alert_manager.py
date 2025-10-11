#!/usr/bin/env python3
"""
Alert Manager - V2 Compliance Module
===================================

Alert management functionality.
Extracted from core_monitoring_manager.py.

Author: Agent-5 (Business Intelligence & Team Beta Leader) - V2 Refactoring
License: MIT
"""

import threading
import uuid
from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Any

from ..contracts import ManagerContext, ManagerResult
from .alert_operations import AlertOperations


class AlertLevel(Enum):
    """Alert severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertManager:
    """Manages alerts and alert rules."""

    def __init__(self):
        """Initialize alert manager."""
        self.alerts: dict[str, dict[str, Any]] = {}
        self.alert_callbacks: dict[str, Callable] = {}
        self.alert_rules: dict[str, dict[str, Any]] = {}
        self._alert_lock = threading.Lock()

    def create_alert(self, context: ManagerContext, alert_data: dict[str, Any]) -> ManagerResult:
        """Create a new alert."""
        try:
            with self._alert_lock:
                alert_id = str(uuid.uuid4())
                alert = {
                    "alert_id": alert_id,
                    "level": alert_data.get("level", AlertLevel.MEDIUM.value),
                    "message": alert_data.get("message", ""),
                    "source": alert_data.get("source", "system"),
                    "created_at": datetime.now().isoformat(),
                    "acknowledged": False,
                    "resolved": False,
                    "metadata": alert_data.get("metadata", {}),
                }
                self.alerts[alert_id] = alert

                # Check alert rules
                self._check_alert_rules(alert)

                # Call alert callbacks
                for callback in self.alert_callbacks.values():
                    try:
                        callback(alert)
                    except Exception:
                        pass

                return ManagerResult(
                    success=True,
                    data={"alert_id": alert_id, "alert": alert},
                    message=f"Alert created: {alert_id}",
                    errors=[],
                )
        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                message=f"Failed to create alert: {e}",
                errors=[str(e)],
            )

    def acknowledge_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Acknowledge an alert."""
        return AlertOperations.acknowledge_alert_internal(self.alerts, payload)

    def resolve_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Resolve an alert."""
        return AlertOperations.resolve_alert_internal(self.alerts, payload)

    def get_alerts(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get alerts with optional filtering."""
        try:
            level_filter = payload.get("level")
            unresolved_only = payload.get("unresolved_only", False)

            filtered_alerts = []
            for alert in self.alerts.values():
                if level_filter and alert["level"] != level_filter:
                    continue
                if unresolved_only and alert["resolved"]:
                    continue
                filtered_alerts.append(alert)

            return ManagerResult(
                success=True,
                data={"alerts": filtered_alerts, "count": len(filtered_alerts)},
                message=f"Found {len(filtered_alerts)} alerts",
                errors=[],
            )
        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                message=f"Failed to get alerts: {e}",
                errors=[str(e)],
            )

    def _check_alert_rules(self, alert: dict[str, Any]) -> None:
        """Check and apply alert rules."""
        for rule_name, rule in self.alert_rules.items():
            try:
                if rule.get("level") == alert["level"]:
                    if rule.get("action") == "escalate":
                        self._escalate_alert(alert, rule)
                    elif rule.get("action") == "notify":
                        self._notify_alert(alert, rule)
                    elif rule.get("action") == "auto_resolve":
                        self._auto_resolve_alert(alert, rule)
            except Exception:
                pass

    def _escalate_alert(self, alert: dict[str, Any], rule: dict[str, Any]) -> None:
        """Escalate alert to higher level."""
        alert["escalated"] = True
        alert["escalated_at"] = datetime.now().isoformat()
        alert["escalated_to"] = rule.get("escalate_to", "admin")

    def _notify_alert(self, alert: dict[str, Any], rule: dict[str, Any]) -> None:
        """Send alert notification."""
        alert["notified"] = True
        alert["notified_at"] = datetime.now().isoformat()
        alert["notified_to"] = rule.get("notify_to", [])

    def _auto_resolve_alert(self, alert: dict[str, Any], rule: dict[str, Any]) -> None:
        """Auto-resolve alert based on rule."""
        alert["resolved"] = True
        alert["resolved_at"] = datetime.now().isoformat()
        alert["resolved_by"] = "auto_rule"

    def setup_default_alert_rules(self) -> None:
        """Setup default alert rules."""
        self.alert_rules["critical_escalation"] = {
            "level": AlertLevel.CRITICAL.value,
            "action": "escalate",
            "escalate_to": "captain",
        }

        self.alert_rules["high_notification"] = {
            "level": AlertLevel.HIGH.value,
            "action": "notify",
            "notify_to": ["admin", "ops"],
        }
