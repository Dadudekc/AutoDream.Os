"""
Monitoring Rules Manager - Phase-2 V2 Compliance Refactoring
============================================================

Handles alert rules processing and rule-based actions.

Author: Agent-5 (Monitoring Specialist)
License: MIT
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .monitoring_state import MonitoringState


class MonitoringRules:
    """Handles alert rules and rule-based actions."""

    def __init__(self, state: MonitoringState):
        """Initialize monitoring rules manager."""
        self.state = state

    def check_alert_rules(self, alert: dict[str, Any]) -> None:
        """Check alert against rules and take actions."""
        try:
            alert_rules = self.state.get_alert_rules()
            for rule_name, rule in alert_rules.items():
                if not rule.get("enabled", True):
                    continue

                # Check if rule matches alert
                if not self._rule_matches_alert(rule, alert):
                    continue

                # Execute rule action
                self._execute_rule_action(rule, alert)

        except Exception:
            pass  # Ignore rule processing errors

    def _rule_matches_alert(self, rule: dict[str, Any], alert: dict[str, Any]) -> bool:
        """Check if a rule matches an alert."""
        # Check level match
        if "level" in rule and rule["level"] != alert.get("level"):
            return False

        # Check source match
        if "source" in rule and rule["source"] != alert.get("source"):
            return False

        # Check message pattern
        if "message_pattern" in rule:
            if not re.search(rule["message_pattern"], alert.get("message", "")):
                return False

        return True

    def _execute_rule_action(self, rule: dict[str, Any], alert: dict[str, Any]) -> None:
        """Execute rule action on alert."""
        action = rule.get("action", "notify")
        if action == "escalate":
            self.escalate_alert(alert, rule)
        elif action == "notify":
            self.notify_alert(alert, rule)
        elif action == "auto_resolve":
            self.auto_resolve_alert(alert, rule)

    def escalate_alert(self, alert: dict[str, Any], rule: dict[str, Any]) -> None:
        """Escalate an alert."""
        try:
            updates = {
                "escalated": True,
                "escalated_at": datetime.now().isoformat(),
                "escalation_rule": rule.get("name", "unknown"),
            }
            self.state.update_alert(alert["id"], updates)
        except Exception:
            pass

    def notify_alert(self, alert: dict[str, Any], rule: dict[str, Any]) -> None:
        """Send notification for alert."""
        try:
            updates = {
                "notified": True,
                "notified_at": datetime.now().isoformat(),
                "notification_rule": rule.get("name", "unknown"),
            }
            self.state.update_alert(alert["id"], updates)
        except Exception:
            pass

    def auto_resolve_alert(self, alert: dict[str, Any], rule: dict[str, Any]) -> None:
        """Auto-resolve an alert."""
        try:
            updates = {
                "resolved": True,
                "resolved_at": datetime.now().isoformat(),
                "auto_resolved": True,
                "auto_resolve_rule": rule.get("name", "unknown"),
                "status": "resolved",
            }
            self.state.update_alert(alert["id"], updates)
        except Exception:
            pass



