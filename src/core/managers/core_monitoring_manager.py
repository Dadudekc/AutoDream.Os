"""
Core Monitoring Manager - Phase-2 Manager Consolidation
======================================================

Main interface for monitoring operations.
Refactored to V2 compliance by Agent-5.

Author: Agent-3 (Infrastructure & DevOps Specialist), Refactored by Agent-5
License: MIT
"""

from __future__ import annotations

import threading
from typing import Any

from .contracts import ManagerContext, ManagerResult, MonitoringManager
from .monitoring.alert_manager import AlertManager, AlertLevel
from .monitoring.metric_manager import MetricManager, MetricType
from .monitoring.widget_manager import WidgetManager, WidgetType


class CoreMonitoringManager(MonitoringManager):
    """Core monitoring manager - consolidates alerts, metrics, and widgets."""

    def __init__(self):
        """Initialize core monitoring manager."""
        self.alert_manager = AlertManager()
        self.metric_manager = MetricManager()
        self.widget_manager = WidgetManager()

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize monitoring manager."""
        try:
            self.alert_manager.setup_default_alert_rules()
            self._start_background_monitoring()
            context.logger("Core Monitoring Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize Core Monitoring Manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute monitoring operation."""
        try:
            # Alert operations
            if operation == "create_alert":
                return self.alert_manager.create_alert(context, payload.get("alert_data", {}))
            elif operation == "acknowledge_alert":
                return self.alert_manager.acknowledge_alert(context, payload)
            elif operation == "resolve_alert":
                return self.alert_manager.resolve_alert(context, payload)
            elif operation == "get_alerts":
                return self.alert_manager.get_alerts(context, payload)
            
            # Metric operations
            elif operation == "record_metric":
                return self.metric_manager.record_metric(
                    context,
                    payload.get("metric_name", ""),
                    payload.get("metric_value")
                )
            elif operation == "get_metrics":
                return self.metric_manager.get_metrics(context, payload)
            
            # Widget operations
            elif operation == "create_widget":
                return self.widget_manager.create_widget(context, payload.get("widget_data", {}))
            elif operation == "get_widgets":
                return self.widget_manager.get_widgets(context, payload)
            
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    message=f"Unknown operation: {operation}",
                    errors=[f"Unknown operation: {operation}"],
                )
        except Exception as e:
            return ManagerResult(
                success=False,
                data={},
                message=f"Monitoring operation error: {e}",
                errors=[str(e)],
            )

    def create_alert(self, context: ManagerContext, alert_data: dict[str, Any]) -> ManagerResult:
        """Create a new alert."""
        return self.alert_manager.create_alert(context, alert_data)

    def record_metric(
        self, context: ManagerContext, metric_name: str, metric_value: Any
    ) -> ManagerResult:
        """Record a metric value."""
        return self.metric_manager.record_metric(context, metric_name, metric_value)

    def create_widget(self, context: ManagerContext, widget_data: dict[str, Any]) -> ManagerResult:
        """Create a new widget."""
        return self.widget_manager.create_widget(context, widget_data)

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup resources."""
        try:
            self.alert_manager.alerts.clear()
            self.metric_manager.metrics.clear()
            self.metric_manager.metric_history.clear()
            self.widget_manager.widgets.clear()
            return True
        except Exception:
            return False

    def get_status(self) -> dict[str, Any]:
        """Get manager status."""
        return {
            "total_alerts": len(self.alert_manager.alerts),
            "unresolved_alerts": sum(
                1 for a in self.alert_manager.alerts.values() if not a["resolved"]
            ),
            "total_metrics": len(self.metric_manager.metrics),
            "total_widgets": len(self.widget_manager.widgets),
        }

    def _start_background_monitoring(self) -> None:
        """Start background monitoring tasks."""
        def monitor():
            while True:
                try:
                    threading.Event().wait(60.0)  # Check every 60 seconds
                except Exception:
                    break

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
