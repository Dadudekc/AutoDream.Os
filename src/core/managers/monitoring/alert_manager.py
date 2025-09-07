"""
Alert Manager - Phase-2 V2 Compliance Refactoring
=================================================

Handles alert-specific monitoring operations.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from .base_monitoring_manager import BaseMonitoringManager, AlertLevel
from ..contracts import ManagerContext, ManagerResult


class AlertManager(BaseMonitoringManager):
    """Manages alert operations."""

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute alert operation."""
        try:
            if operation == "create_alert":
                return self.create_alert(context, payload)
            elif operation == "get_alerts":
                return self._get_alerts(context, payload)
            elif operation == "acknowledge_alert":
                return self._acknowledge_alert(context, payload)
            elif operation == "resolve_alert":
                return self._resolve_alert(context, payload)
            elif operation == "get_alert_stats":
                return self._get_alert_stats(context, payload)
            elif operation == "bulk_acknowledge":
                return self._bulk_acknowledge(context, payload)
            elif operation == "bulk_resolve":
                return self._bulk_resolve(context, payload)
            else:
                return super().execute(context, operation, payload)
        except Exception as e:
            context.logger(f"Error executing alert operation {operation}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _get_alert_stats(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Get alert statistics."""
        try:
            with self._alert_lock:
                total_alerts = len(self.alerts)
                active_alerts = len([a for a in self.alerts.values() if a.get("status") == "active"])
                resolved_alerts = len([a for a in self.alerts.values() if a.get("resolved")])
                acknowledged_alerts = len([a for a in self.alerts.values() if a.get("acknowledged")])
                
                # Count by level
                level_counts = {}
                for alert in self.alerts.values():
                    level = alert.get("level", "unknown")
                    level_counts[level] = level_counts.get(level, 0) + 1
                
                # Count by source
                source_counts = {}
                for alert in self.alerts.values():
                    source = alert.get("source", "unknown")
                    source_counts[source] = source_counts.get(source, 0) + 1

            return ManagerResult(
                success=True,
                data={
                    "total_alerts": total_alerts,
                    "active_alerts": active_alerts,
                    "resolved_alerts": resolved_alerts,
                    "acknowledged_alerts": acknowledged_alerts,
                    "level_counts": level_counts,
                    "source_counts": source_counts,
                },
                metrics={"alerts_analyzed": total_alerts},
            )

        except Exception as e:
            context.logger(f"Error getting alert stats: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _bulk_acknowledge(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Bulk acknowledge alerts."""
        try:
            alert_ids = payload.get("alert_ids", [])
            if not alert_ids:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="alert_ids list is required",
                )

            acknowledged_count = 0
            with self._alert_lock:
                for alert_id in alert_ids:
                    if alert_id in self.alerts:
                        alert = self.alerts[alert_id]
                        if not alert.get("acknowledged"):
                            alert["acknowledged"] = True
                            alert["acknowledged_at"] = context.timestamp.isoformat()
                            acknowledged_count += 1

            return ManagerResult(
                success=True,
                data={"acknowledged_count": acknowledged_count},
                metrics={"alerts_acknowledged": acknowledged_count},
            )

        except Exception as e:
            context.logger(f"Error bulk acknowledging alerts: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _bulk_resolve(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Bulk resolve alerts."""
        try:
            alert_ids = payload.get("alert_ids", [])
            resolution_notes = payload.get("resolution_notes", "Bulk resolved")
            
            if not alert_ids:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="alert_ids list is required",
                )

            resolved_count = 0
            with self._alert_lock:
                for alert_id in alert_ids:
                    if alert_id in self.alerts:
                        alert = self.alerts[alert_id]
                        if not alert.get("resolved"):
                            alert["resolved"] = True
                            alert["resolved_at"] = context.timestamp.isoformat()
                            alert["resolution_notes"] = resolution_notes
                            alert["status"] = "resolved"
                            resolved_count += 1

            return ManagerResult(
                success=True,
                data={"resolved_count": resolved_count},
                metrics={"alerts_resolved": resolved_count},
            )

        except Exception as e:
            context.logger(f"Error bulk resolving alerts: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def get_status(self) -> Dict[str, Any]:
        """Get alert manager status."""
        base_status = super().get_status()
        base_status.update({
            "alert_rules_count": len(self.alert_rules),
            "enabled_rules": len([r for r in self.alert_rules.values() if r.get("enabled", True)]),
            "alert_levels": list(set(a.get("level", "unknown") for a in self.alerts.values())),
            "alert_sources": list(set(a.get("source", "unknown") for a in self.alerts.values())),
        })
        return base_status
