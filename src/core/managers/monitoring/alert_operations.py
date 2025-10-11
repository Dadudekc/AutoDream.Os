"""
Alert Operations Helper
=======================

Extracted operations from AlertManager for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

from datetime import datetime

from ..contracts import ManagerResult


class AlertOperations:
    """Helper for alert CRUD operations."""

    @staticmethod
    def acknowledge_alert_internal(alerts, payload) -> ManagerResult:
        """Acknowledge an alert."""
        try:
            alert_id = payload.get("alert_id")
            if not alert_id or alert_id not in alerts:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Alert not found: {alert_id}",
                    errors=[f"Alert not found: {alert_id}"],
                )

            alert = alerts[alert_id]
            alert["acknowledged"] = True
            alert["acknowledged_at"] = datetime.now().isoformat()
            alert["acknowledged_by"] = payload.get("acknowledged_by", "system")

            return ManagerResult(
                success=True,
                data={"alert_id": alert_id},
                message=f"Alert acknowledged: {alert_id}",
                errors=[],
            )
        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                message=f"Failed to acknowledge alert: {e}",
                errors=[str(e)],
            )

    @staticmethod
    def resolve_alert_internal(alerts, payload) -> ManagerResult:
        """Resolve an alert."""
        try:
            alert_id = payload.get("alert_id")
            if not alert_id or alert_id not in alerts:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Alert not found: {alert_id}",
                    errors=[f"Alert not found: {alert_id}"],
                )

            alert = alerts[alert_id]
            alert["resolved"] = True
            alert["resolved_at"] = datetime.now().isoformat()
            alert["resolved_by"] = payload.get("resolved_by", "system")
            alert["resolution_notes"] = payload.get("resolution_notes", "")

            return ManagerResult(
                success=True,
                data={"alert_id": alert_id},
                message=f"Alert resolved: {alert_id}",
                errors=[],
            )
        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                message=f"Failed to resolve alert: {e}",
                errors=[str(e)],
            )
