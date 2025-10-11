"""
Base Monitoring Manager - Phase-2 V2 Compliance Refactoring
===========================================================

Base class for monitoring management with common functionality.
Refactored to use specialized managers for better separation of concerns.

Author: Agent-5 (Monitoring Specialist)
License: MIT
"""

from __future__ import annotations

from typing import Any

from ..contracts import ManagerContext, ManagerResult, MonitoringManager
from .monitoring_crud import AlertLevel, MetricType, MonitoringCRUD, WidgetType
from .monitoring_lifecycle import MonitoringLifecycle
from .monitoring_query import MonitoringQuery
from .monitoring_rules import MonitoringRules
from .monitoring_state import MonitoringState


class BaseMonitoringManager(MonitoringManager):
    """Base monitoring manager with common functionality."""

    def __init__(self):
        """Initialize base monitoring manager."""
        # Initialize specialized managers
        self.state = MonitoringState()
        self.lifecycle = MonitoringLifecycle(self.state)
        self.rules = MonitoringRules(self.state)
        self.crud = MonitoringCRUD(self.state, self.rules)
        self.query = MonitoringQuery(self.state)

        # Expose commonly used enums for compatibility
        self.AlertLevel = AlertLevel
        self.MetricType = MetricType
        self.WidgetType = WidgetType

        # Expose state attributes for backward compatibility
        self.alerts = self.state.alerts
        self.metrics = self.state.metrics
        self.metric_history = self.state.metric_history
        self.widgets = self.state.widgets
        self.alert_rules = self.state.alert_rules

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize monitoring manager."""
        return self.lifecycle.initialize(context)

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute monitoring operation."""
        try:
            if operation == "create_alert":
                return self.crud.create_alert(context, payload)
            elif operation == "record_metric":
                return self.crud.record_metric(context, payload)
            elif operation == "create_widget":
                return self.crud.create_widget(context, payload)
            elif operation == "get_alerts":
                return self.query.get_alerts(context, payload)
            elif operation == "get_metrics":
                return self.query.get_metrics(context, payload)
            elif operation == "get_widgets":
                return self.query.get_widgets(context, payload)
            elif operation == "acknowledge_alert":
                return self.query.acknowledge_alert(context, payload)
            elif operation == "resolve_alert":
                return self.query.resolve_alert(context, payload)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown operation: {operation}",
                )
        except Exception as e:
            context.logger(f"Error executing monitoring operation {operation}: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def create_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Create a new alert."""
        return self.crud.create_alert(context, payload)

    def record_metric(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Record a metric value."""
        return self.crud.record_metric(context, payload)

    def create_widget(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Create a dashboard widget."""
        return self.crud.create_widget(context, payload)

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup monitoring manager."""
        return self.lifecycle.cleanup(context)

    def get_status(self) -> dict[str, Any]:
        """Get monitoring manager status."""
        return self.state.get_status()

    # Private methods for backward compatibility
    def _get_alerts(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get alerts with optional filtering."""
        return self.query.get_alerts(context, payload)

    def _get_metrics(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get metrics with optional filtering."""
        return self.query.get_metrics(context, payload)

    def _get_widgets(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Get widgets with optional filtering."""
        return self.query.get_widgets(context, payload)

    def _acknowledge_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Acknowledge an alert."""
        return self.query.acknowledge_alert(context, payload)

    def _resolve_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Resolve an alert."""
        return self.query.resolve_alert(context, payload)
