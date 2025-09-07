"""
Base Monitoring Manager - Phase-2 V2 Compliance Refactoring
===========================================================

Base class for monitoring management with common functionality.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
import json
import threading
import uuid
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from enum import Enum
from ..contracts import MonitoringManager, ManagerContext, ManagerResult
from src.core.constants import get_completion_signal


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


class BaseMonitoringManager(MonitoringManager):
    """Base monitoring manager with common functionality."""

    def __init__(self):
        """Initialize base monitoring manager."""
        self.alerts: Dict[str, Dict[str, Any]] = {}
        self.metrics: Dict[str, Any] = {}
        self.metric_history: Dict[str, List[Dict[str, Any]]] = {}
        self.widgets: Dict[str, Dict[str, Any]] = {}
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self._alert_lock = threading.Lock()
        self._metric_lock = threading.Lock()
        self._widget_lock = threading.Lock()
        self.max_alerts = 1000
        self.max_metric_history = 10000

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize monitoring manager."""
        try:
            # Setup default alert rules
            self._setup_default_alert_rules()
            
            # Start background monitoring
            self._start_background_monitoring()
            
            context.logger("Base Monitoring Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize monitoring manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute monitoring operation."""
        try:
            if operation == "create_alert":
                return self.create_alert(context, payload)
            elif operation == "record_metric":
                return self.record_metric(context, payload)
            elif operation == "create_widget":
                return self.create_widget(context, payload)
            elif operation == "get_alerts":
                return self._get_alerts(context, payload)
            elif operation == "get_metrics":
                return self._get_metrics(context, payload)
            elif operation == "get_widgets":
                return self._get_widgets(context, payload)
            elif operation == "acknowledge_alert":
                return self._acknowledge_alert(context, payload)
            elif operation == "resolve_alert":
                return self._resolve_alert(context, payload)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown operation: {operation}",
                )
        except Exception as e:
            context.logger(f"Error executing monitoring operation {operation}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def create_alert(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
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

            with self._alert_lock:
                self.alerts[alert_id] = alert

            # Check alert rules
            self._check_alert_rules(alert)

            return ManagerResult(
                success=True,
                data={"alert_id": alert_id, "alert": alert},
                metrics={"alerts_created": 1},
            )

        except Exception as e:
            context.logger(f"Error creating alert: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def record_metric(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
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

            with self._metric_lock:
                # Update current metric value
                self.metrics[metric_name] = metric_entry

                # Add to history
                if metric_name not in self.metric_history:
                    self.metric_history[metric_name] = []
                
                self.metric_history[metric_name].append(metric_entry)

                # Limit history size
                if len(self.metric_history[metric_name]) > self.max_metric_history:
                    self.metric_history[metric_name] = self.metric_history[metric_name][-self.max_metric_history:]

            return ManagerResult(
                success=True,
                data={"metric_name": metric_name, "value": metric_value},
                metrics={"metrics_recorded": 1},
            )

        except Exception as e:
            context.logger(f"Error recording metric: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def create_widget(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
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

            with self._widget_lock:
                self.widgets[widget_id] = widget

            return ManagerResult(
                success=True,
                data={"widget_id": widget_id, "widget": widget},
                metrics={"widgets_created": 1},
            )

        except Exception as e:
            context.logger(f"Error creating widget: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup monitoring manager."""
        try:
            with self._alert_lock:
                self.alerts.clear()
            with self._metric_lock:
                self.metrics.clear()
                self.metric_history.clear()
            with self._widget_lock:
                self.widgets.clear()
            
            context.logger(
                f"Monitoring manager cleaned up {get_completion_signal()}"
            )
            return True
        except Exception as e:
            context.logger(f"Error cleaning up monitoring manager: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get monitoring manager status."""
        return {
            "total_alerts": len(self.alerts),
            "active_alerts": len([a for a in self.alerts.values() if a.get("status") == "active"]),
            "resolved_alerts": len([a for a in self.alerts.values() if a.get("resolved")]),
            "total_metrics": len(self.metrics),
            "total_widgets": len(self.widgets),
            "alert_rules": len(self.alert_rules),
            "max_alerts": self.max_alerts,
            "max_metric_history": self.max_metric_history,
        }

    def _get_alerts(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Get alerts with optional filtering."""
        try:
            level_filter = payload.get("level")
            status_filter = payload.get("status")
            source_filter = payload.get("source")

            alerts = dict(self.alerts)

            # Apply filters
            if level_filter:
                alerts = {k: v for k, v in alerts.items() if v.get("level") == level_filter}
            if status_filter:
                alerts = {k: v for k, v in alerts.items() if v.get("status") == status_filter}
            if source_filter:
                alerts = {k: v for k, v in alerts.items() if v.get("source") == source_filter}

            return ManagerResult(
                success=True,
                data={"alerts": alerts},
                metrics={"alerts_found": len(alerts)},
            )

        except Exception as e:
            context.logger(f"Error getting alerts: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _get_metrics(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Get metrics with optional filtering."""
        try:
            metric_name = payload.get("metric_name")
            include_history = payload.get("include_history", False)

            if metric_name:
                if metric_name not in self.metrics:
                    return ManagerResult(
                        success=False,
                        data={},
                        metrics={},
                        error=f"Metric {metric_name} not found",
                    )
                metrics = {metric_name: self.metrics[metric_name]}
                if include_history and metric_name in self.metric_history:
                    metrics[metric_name]["history"] = self.metric_history[metric_name]
            else:
                metrics = dict(self.metrics)
                if include_history:
                    for name, metric in metrics.items():
                        if name in self.metric_history:
                            metric["history"] = self.metric_history[name]

            return ManagerResult(
                success=True,
                data={"metrics": metrics},
                metrics={"metrics_found": len(metrics)},
            )

        except Exception as e:
            context.logger(f"Error getting metrics: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _get_widgets(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Get widgets with optional filtering."""
        try:
            widget_type_filter = payload.get("widget_type")

            widgets = dict(self.widgets)

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
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _acknowledge_alert(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Acknowledge an alert."""
        try:
            alert_id = payload.get("alert_id")
            if not alert_id or alert_id not in self.alerts:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Alert ID is required and must exist",
                )

            with self._alert_lock:
                alert = self.alerts[alert_id]
                alert["acknowledged"] = True
                alert["acknowledged_at"] = datetime.now().isoformat()

            return ManagerResult(
                success=True,
                data={"alert_id": alert_id},
                metrics={"alerts_acknowledged": 1},
            )

        except Exception as e:
            context.logger(f"Error acknowledging alert: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _resolve_alert(self, context: ManagerContext, payload: Dict[str, Any]) -> ManagerResult:
        """Resolve an alert."""
        try:
            alert_id = payload.get("alert_id")
            resolution_notes = payload.get("resolution_notes", "")

            if not alert_id or alert_id not in self.alerts:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error="Alert ID is required and must exist",
                )

            with self._alert_lock:
                alert = self.alerts[alert_id]
                alert["resolved"] = True
                alert["resolved_at"] = datetime.now().isoformat()
                alert["resolution_notes"] = resolution_notes
                alert["status"] = "resolved"

            return ManagerResult(
                success=True,
                data={"alert_id": alert_id},
                metrics={"alerts_resolved": 1},
            )

        except Exception as e:
            context.logger(f"Error resolving alert: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _check_alert_rules(self, alert: Dict[str, Any]) -> None:
        """Check alert against rules and take actions."""
        try:
            for rule_name, rule in self.alert_rules.items():
                if not rule.get("enabled", True):
                    continue

                # Check level match
                if "level" in rule and rule["level"] != alert.get("level"):
                    continue

                # Check source match
                if "source" in rule and rule["source"] != alert.get("source"):
                    continue

                # Check message pattern
                if "message_pattern" in rule:
                    import re
                    if not re.search(rule["message_pattern"], alert.get("message", "")):
                        continue

                # Execute rule action
                action = rule.get("action", "notify")
                if action == "escalate":
                    self._escalate_alert(alert, rule)
                elif action == "notify":
                    self._notify_alert(alert, rule)
                elif action == "auto_resolve":
                    self._auto_resolve_alert(alert, rule)

        except Exception:
            pass  # Ignore rule processing errors

    def _escalate_alert(self, alert: Dict[str, Any], rule: Dict[str, Any]) -> None:
        """Escalate an alert."""
        try:
            alert["escalated"] = True
            alert["escalated_at"] = datetime.now().isoformat()
            alert["escalation_rule"] = rule.get("name", "unknown")
        except Exception:
            pass

    def _notify_alert(self, alert: Dict[str, Any], rule: Dict[str, Any]) -> None:
        """Send notification for alert."""
        try:
            alert["notified"] = True
            alert["notified_at"] = datetime.now().isoformat()
            alert["notification_rule"] = rule.get("name", "unknown")
        except Exception:
            pass

    def _auto_resolve_alert(self, alert: Dict[str, Any], rule: Dict[str, Any]) -> None:
        """Auto-resolve an alert."""
        try:
            alert["resolved"] = True
            alert["resolved_at"] = datetime.now().isoformat()
            alert["auto_resolved"] = True
            alert["auto_resolve_rule"] = rule.get("name", "unknown")
            alert["status"] = "resolved"
        except Exception:
            pass

    def _setup_default_alert_rules(self) -> None:
        """Setup default alert rules."""
        self.alert_rules = {
            "critical_escalation": {
                "name": "critical_escalation",
                "level": "critical",
                "action": "escalate",
                "enabled": True,
            },
            "system_error_notification": {
                "name": "system_error_notification",
                "source": "system",
                "message_pattern": r"error|failed|exception",
                "action": "notify",
                "enabled": True,
            },
            "auto_resolve_info": {
                "name": "auto_resolve_info",
                "level": "low",
                "action": "auto_resolve",
                "enabled": True,
            },
        }

    def _start_background_monitoring(self) -> None:
        """Start background monitoring tasks."""

        def monitor():
            while True:
                try:
                    # Clean up old resolved alerts (older than 24 hours)
                    cutoff_time = datetime.now() - timedelta(hours=24)
                    with self._alert_lock:
                        to_remove = []
                        for alert_id, alert in self.alerts.items():
                            if (
                                alert.get("resolved")
                                and "resolved_at" in alert
                                and datetime.fromisoformat(alert["resolved_at"])
                                < cutoff_time
                            ):
                                to_remove.append(alert_id)

                        for alert_id in to_remove:
                            del self.alerts[alert_id]

                    # Clean up old metric history (older than 7 days)
                    cutoff_time = datetime.now() - timedelta(days=7)
                    with self._metric_lock:
                        for metric_name, history in self.metric_history.items():
                            self.metric_history[metric_name] = [
                                entry
                                for entry in history
                                if datetime.fromisoformat(entry["timestamp"])
                                > cutoff_time
                            ]

                    threading.Event().wait(300)  # Wait 5 minutes
                except Exception:
                    break

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
