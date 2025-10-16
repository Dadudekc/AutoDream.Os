"""
Base Monitoring Manager - Phase-2 V2 Compliance Refactoring + DUP-004
===========================================================

Base class for monitoring management with common functionality.
DUP-004: Now inherits from BaseManager for proper hierarchy.

Author: Agent-5 (Monitoring Specialist) | DUP-004: Agent-2 | License: MIT
"""

from __future__ import annotations

from typing import Any

from ..base_manager import BaseManager
from ..contracts import ManagerContext, ManagerResult
from ..manager_state import ManagerType
from .monitoring_crud import AlertLevel, MetricType, MonitoringCRUD, WidgetType
from .monitoring_query import MonitoringQuery
from .monitoring_rules import MonitoringRules
from .monitoring_state import MonitoringState


class BaseMonitoringManager(BaseManager):
    """Base monitoring manager with common functionality - inherits from BaseManager."""

    def __init__(self):
        """Initialize base monitoring manager."""
        # Initialize BaseManager first (gets all utilities for free!)
        super().__init__(ManagerType.MONITORING, "Base Monitoring Manager")

        # Monitoring-specific state
        self.monitoring_state = MonitoringState()
        self.rules = MonitoringRules(self.monitoring_state)
        self.crud = MonitoringCRUD(self.monitoring_state, self.rules)
        self.query = MonitoringQuery(self.monitoring_state)

        # Expose commonly used enums for compatibility
        self.AlertLevel = AlertLevel
        self.MetricType = MetricType
        self.WidgetType = WidgetType

        # Expose state attributes for backward compatibility
        self.alerts = self.monitoring_state.alerts
        self.metrics = self.monitoring_state.metrics
        self.metric_history = self.monitoring_state.metric_history
        self.widgets = self.monitoring_state.widgets
        self.alert_rules = self.monitoring_state.alert_rules

    def _execute_operation(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute monitoring-specific operations."""
        # Monitoring-specific operations only (BaseManager handles validation/error handling)
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

    def create_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Create a new alert."""
        return self.crud.create_alert(context, payload)

    def record_metric(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Record a metric value."""
        return self.crud.record_metric(context, payload)

    def create_widget(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Create a dashboard widget."""
        return self.crud.create_widget(context, payload)

    def get_status(self) -> dict[str, Any]:
        """Get monitoring manager status - extends BaseManager status."""
        base_status = super().get_status()
        monitoring_status = self.monitoring_state.get_status()
        base_status.update(monitoring_status)
        return base_status

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
