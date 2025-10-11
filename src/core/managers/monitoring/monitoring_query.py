"""
Monitoring Query Operations - Phase-2 V2 Compliance Refactoring
===============================================================
Handles query and update operations for monitoring resources.
Author: Agent-5 (Monitoring Specialist) | License: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .monitoring_state import MonitoringState

from ..contracts import ManagerContext, ManagerResult


class MonitoringQuery:
    """Handles query and update operations for monitoring."""

    def __init__(self, state: MonitoringState):
        """Initialize monitoring query manager."""
        self.state = state

    def get_alerts(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get alerts with optional filtering."""
        try:
            level_filter = payload.get("level")
            status_filter = payload.get("status")
            source_filter = payload.get("source")
            alerts = self.state.get_all_alerts()
            # Apply filters
            if level_filter:
                alerts = {k: v for k, v in alerts.items() if v.get("level") == level_filter}
            if status_filter:
                alerts = {k: v for k, v in alerts.items() if v.get("status") == status_filter}
            if source_filter:
                alerts = {k: v for k, v in alerts.items() if v.get("source") == source_filter}
            return ManagerResult(
                success=True, data={"alerts": alerts}, metrics={"alerts_found": len(alerts)}
            )
        except Exception as e:
            context.logger(f"Error getting alerts: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def get_metrics(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get metrics with optional filtering."""
        try:
            metric_name = payload.get("metric_name")
            include_history = payload.get("include_history", False)
            if metric_name:
                metric = self.state.get_metric(metric_name)
                if not metric:
                    return ManagerResult(
                        success=False,
                        data={},
                        metrics={},
                        error=f"Metric {metric_name} not found",
                    )
                metrics = {metric_name: metric}
                if include_history:
                    metrics[metric_name]["history"] = self.state.get_metric_history(metric_name)
            else:
                metrics = self.state.get_all_metrics()
                if include_history:
                    for name in metrics:
                        metrics[name]["history"] = self.state.get_metric_history(name)
            return ManagerResult(
                success=True,
                data={"metrics": metrics},
                metrics={"metrics_found": len(metrics)},
            )
        except Exception as e:
            context.logger(f"Error getting metrics: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def get_widgets(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get widgets with optional filtering."""
        try:
            widget_type_filter = payload.get("widget_type")
            widgets = self.state.get_all_widgets()
            # Apply filters
            if widget_type_filter:
                widgets = {k: v for k, v in widgets.items() if v.get("type") == widget_type_filter}
            return ManagerResult(
                success=True,
                data={"widgets": widgets},
                metrics={"widgets_found": len(widgets)},
            )
        except Exception as e:
            context.logger(f"Error getting widgets: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def acknowledge_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Acknowledge an alert."""
        try:
            alert_id = payload.get("alert_id")
            if not alert_id or not self.state.get_alert(alert_id):
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Alert ID is required and must exist",
                )
            updates = {
                "acknowledged": True,
                "acknowledged_at": datetime.now().isoformat(),
            }
            self.state.update_alert(alert_id, updates)
            return ManagerResult(
                success=True,
                data={"alert_id": alert_id},
                metrics={"alerts_acknowledged": 1},
            )
        except Exception as e:
            context.logger(f"Error acknowledging alert: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def resolve_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Resolve an alert."""
        try:
            alert_id = payload.get("alert_id")
            resolution_notes = payload.get("resolution_notes", "")
            if not alert_id or not self.state.get_alert(alert_id):
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Alert ID is required and must exist",
                )
            updates = {
                "resolved": True,
                "resolved_at": datetime.now().isoformat(),
                "resolution_notes": resolution_notes,
                "status": "resolved",
            }
            self.state.update_alert(alert_id, updates)
            return ManagerResult(
                success=True,
                data={"alert_id": alert_id},
                metrics={"alerts_resolved": 1},
            )
        except Exception as e:
            context.logger(f"Error resolving alert: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

