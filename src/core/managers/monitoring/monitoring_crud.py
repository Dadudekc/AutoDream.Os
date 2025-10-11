"""
Monitoring CRUD Operations - Phase-2 V2 Compliance Refactoring
==============================================================
Handles create operations for monitoring resources.
Author: Agent-5 (Monitoring Specialist) | License: MIT
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .monitoring_state import MonitoringState
    from .monitoring_rules import MonitoringRules

from ..contracts import ManagerContext, ManagerResult


class AlertLevel(Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MetricType(Enum):
    """Metric types."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


class WidgetType(Enum):
    """Widget types."""
    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    ALERT = "alert"


class MonitoringCRUD:
    """Handles create operations for monitoring."""

    def __init__(self, state: MonitoringState, rules: MonitoringRules | None = None):
        """Initialize monitoring CRUD manager."""
        self.state = state
        self.rules = rules

    def create_alert(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Create a new alert."""
        try:
            alert_id = str(uuid.uuid4())
            level = payload.get("level", AlertLevel.MEDIUM)
            source = payload.get("source", "system")
            message = payload.get("message", "")
            metadata = payload.get("metadata", {})
            alert = {
                "id": alert_id,
                "level": level.value if hasattr(level, "value") else str(level),
                "source": source,
                "message": message,
                "metadata": metadata,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "acknowledged": False,
                "resolved": False,
            }
            self.state.add_alert(alert_id, alert)
            # Check alert rules if rules manager is available
            if self.rules:
                self.rules.check_alert_rules(alert)
            return ManagerResult(
                success=True,
                data={"alert_id": alert_id, "alert": alert},
                metrics={"alerts_created": 1},
            )
        except Exception as e:
            context.logger(f"Error creating alert: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def record_metric(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Record a metric value."""
        try:
            metric_name = payload.get("metric_name")
            metric_value = payload.get("metric_value")
            metric_type = payload.get("metric_type", MetricType.GAUGE)
            tags = payload.get("tags", {})
            if not metric_name or metric_value is None:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="metric_name and metric_value are required",
                )
            # Convert enum to string if needed
            if hasattr(metric_type, "value"):
                metric_type = metric_type.value
            metric_entry = {
                "name": metric_name,
                "value": metric_value,
                "type": metric_type,
                "tags": tags,
                "timestamp": datetime.now().isoformat(),
            }
            self.state.add_metric(metric_name, metric_entry)
            return ManagerResult(
                success=True,
                data={"metric_name": metric_name, "value": metric_value},
                metrics={"metrics_recorded": 1},
            )
        except Exception as e:
            context.logger(f"Error recording metric: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def create_widget(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Create a dashboard widget."""
        try:
            widget_id = str(uuid.uuid4())
            widget_type = payload.get("widget_type", WidgetType.METRIC)
            title = payload.get("title", "Untitled Widget")
            config = payload.get("config", {})
            # Convert enum to string if needed
            if hasattr(widget_type, "value"):
                widget_type = widget_type.value
            widget = {
                "id": widget_id,
                "type": widget_type,
                "title": title,
                "config": config,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            self.state.add_widget(widget_id, widget)
            return ManagerResult(
                success=True,
                data={"widget_id": widget_id, "widget": widget},
                metrics={"widgets_created": 1},
            )
        except Exception as e:
            context.logger(f"Error creating widget: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

