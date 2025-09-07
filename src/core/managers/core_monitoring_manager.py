"""
Core Monitoring Manager - Phase-2 Manager Consolidation
======================================================

Consolidates AlertManager, MetricManager, WidgetManager, and GamingAlertManager.
Handles all monitoring operations: alerts, metrics, and dashboard widgets.

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
from .contracts import MonitoringManager, ManagerContext, ManagerResult
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


class CoreMonitoringManager(MonitoringManager):
    """Core monitoring manager - consolidates alerts, metrics, and widgets."""

    def __init__(self):
        """Initialize core monitoring manager."""
        self.alerts: Dict[str, Dict[str, Any]] = {}
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.widgets: Dict[str, Dict[str, Any]] = {}
        self.alert_callbacks: Dict[str, Callable] = {}
        self.metric_callbacks: Dict[str, Callable] = {}
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self.metric_history: Dict[str, List[Dict[str, Any]]] = {}
        self._alert_lock = threading.Lock()
        self._metric_lock = threading.Lock()

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize monitoring manager."""
        try:
            # Setup default alert rules
            self._setup_default_alert_rules()

            # Start background monitoring
            self._start_background_monitoring()

            context.logger("Core Monitoring Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize Core Monitoring Manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute monitoring operation."""
        try:
            if operation == "create_alert":
                alert_data = payload.get("alert_data", {})
                return self.create_alert(context, alert_data)
            elif operation == "record_metric":
                metric_name = payload.get("metric_name", "")
                metric_value = payload.get("metric_value")
                return self.record_metric(context, metric_name, metric_value)
            elif operation == "create_widget":
                widget_data = payload.get("widget_data", {})
                return self.create_widget(context, widget_data)
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
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def create_alert(
        self, context: ManagerContext, alert_data: Dict[str, Any]
    ) -> ManagerResult:
        """Create an alert."""
        try:
            alert_id = alert_data.get("alert_id", str(uuid.uuid4()))
            level = AlertLevel(alert_data.get("level", "medium"))
            message = alert_data.get("message", "")
            source = alert_data.get("source", "system")

            with self._alert_lock:
                alert = {
                    "id": alert_id,
                    "level": level,
                    "message": message,
                    "source": source,
                    "status": "active",
                    "created_at": datetime.now().isoformat(),
                    "acknowledged": False,
                    "resolved": False,
                    "metadata": alert_data.get("metadata", {}),
                }

                self.alerts[alert_id] = alert

                # Check alert rules
                self._check_alert_rules(alert)

                # Execute callbacks
                for callback in self.alert_callbacks.values():
                    try:
                        callback(alert)
                    except Exception as e:
                        context.logger(f"Alert callback failed: {e}")

            return ManagerResult(
                success=True,
                data={"alert_id": alert_id, "alert": alert, "created": True},
                metrics={"total_alerts": len(self.alerts)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def record_metric(
        self, context: ManagerContext, metric_name: str, metric_value: Any
    ) -> ManagerResult:
        """Record a metric."""
        try:
            # Map Python types to MetricType enum values
            type_mapping = {
                "int": "counter",
                "float": "gauge",
                "str": "gauge",
                "bool": "gauge",
            }
            metric_type_name = type_mapping.get(
                type(metric_value).__name__.lower(), "gauge"
            )
            metric_type = MetricType(metric_type_name)
            timestamp = datetime.now()

            with self._metric_lock:
                # Store current metric value
                self.metrics[metric_name] = {
                    "name": metric_name,
                    "value": metric_value,
                    "type": metric_type,
                    "timestamp": timestamp.isoformat(),
                    "metadata": {},
                }

                # Store in history
                if metric_name not in self.metric_history:
                    self.metric_history[metric_name] = []

                self.metric_history[metric_name].append(
                    {
                        "value": metric_value,
                        "timestamp": timestamp.isoformat(),
                    }
                )

                # Keep only last 1000 entries
                if len(self.metric_history[metric_name]) > 1000:
                    self.metric_history[metric_name] = self.metric_history[metric_name][
                        -1000:
                    ]

                # Execute callbacks
                for callback in self.metric_callbacks.values():
                    try:
                        callback(metric_name, metric_value, timestamp)
                    except Exception as e:
                        context.logger(f"Metric callback failed: {e}")

            return ManagerResult(
                success=True,
                data={
                    "metric_name": metric_name,
                    "value": metric_value,
                    "recorded": True,
                },
                metrics={"total_metrics": len(self.metrics)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def create_widget(
        self, context: ManagerContext, widget_data: Dict[str, Any]
    ) -> ManagerResult:
        """Create a widget."""
        try:
            widget_id = widget_data.get("widget_id", str(uuid.uuid4()))
            widget_type = WidgetType(widget_data.get("type", "metric"))
            title = widget_data.get("title", f"Widget {widget_id}")
            config = widget_data.get("config", {})

            widget = {
                "id": widget_id,
                "type": widget_type,
                "title": title,
                "config": config,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "enabled": widget_data.get("enabled", True),
                "metadata": widget_data.get("metadata", {}),
            }

            self.widgets[widget_id] = widget

            return ManagerResult(
                success=True,
                data={"widget_id": widget_id, "widget": widget, "created": True},
                metrics={"total_widgets": len(self.widgets)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup monitoring manager."""
        try:
            # Clear all data
            with self._alert_lock:
                self.alerts.clear()

            with self._metric_lock:
                self.metrics.clear()
                self.metric_history.clear()

            self.widgets.clear()
            self.alert_callbacks.clear()
            self.metric_callbacks.clear()
            self.alert_rules.clear()

            context.logger(
                f"Core Monitoring Manager cleaned up {get_completion_signal()}"
            )
            return True
        except Exception as e:
            context.logger(f"Failed to cleanup Core Monitoring Manager: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get monitoring manager status."""
        active_alerts = sum(
            1 for alert in self.alerts.values() if alert["status"] == "active"
        )
        acknowledged_alerts = sum(
            1 for alert in self.alerts.values() if alert["acknowledged"]
        )
        resolved_alerts = sum(1 for alert in self.alerts.values() if alert["resolved"])

        return {
            "total_alerts": len(self.alerts),
            "active_alerts": active_alerts,
            "acknowledged_alerts": acknowledged_alerts,
            "resolved_alerts": resolved_alerts,
            "total_metrics": len(self.metrics),
            "total_widgets": len(self.widgets),
            "enabled_widgets": sum(1 for w in self.widgets.values() if w["enabled"]),
            "alert_rules": len(self.alert_rules),
        }

    def _get_alerts(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Get alerts with filters."""
        try:
            level_filter = payload.get("level_filter")
            status_filter = payload.get("status_filter")
            source_filter = payload.get("source_filter")

            filtered_alerts = []
            for alert in self.alerts.values():
                if level_filter and alert["level"].value != level_filter:
                    continue
                if status_filter and alert["status"] != status_filter:
                    continue
                if source_filter and alert["source"] != source_filter:
                    continue
                filtered_alerts.append(alert)

            return ManagerResult(
                success=True,
                data={"alerts": filtered_alerts},
                metrics={"total_alerts": len(filtered_alerts)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _get_metrics(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Get metrics with filters."""
        try:
            metric_name_filter = payload.get("metric_name_filter")
            include_history = payload.get("include_history", False)

            filtered_metrics = []
            for metric_name, metric in self.metrics.items():
                if metric_name_filter and metric_name != metric_name_filter:
                    continue

                metric_data = dict(metric)
                if include_history and metric_name in self.metric_history:
                    metric_data["history"] = self.metric_history[metric_name]

                filtered_metrics.append(metric_data)

            return ManagerResult(
                success=True,
                data={"metrics": filtered_metrics},
                metrics={"total_metrics": len(filtered_metrics)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _get_widgets(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Get widgets with filters."""
        try:
            widget_type_filter = payload.get("widget_type_filter")
            enabled_only = payload.get("enabled_only", False)

            filtered_widgets = []
            for widget in self.widgets.values():
                if widget_type_filter and widget["type"].value != widget_type_filter:
                    continue
                if enabled_only and not widget["enabled"]:
                    continue
                filtered_widgets.append(widget)

            return ManagerResult(
                success=True,
                data={"widgets": filtered_widgets},
                metrics={"total_widgets": len(filtered_widgets)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _acknowledge_alert(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Acknowledge an alert."""
        try:
            alert_id = payload.get("alert_id", "")
            acknowledged_by = payload.get("acknowledged_by", "system")

            if alert_id not in self.alerts:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Alert not found: {alert_id}",
                )

            with self._alert_lock:
                alert = self.alerts[alert_id]
                alert["acknowledged"] = True
                alert["acknowledged_by"] = acknowledged_by
                alert["acknowledged_at"] = datetime.now().isoformat()

            return ManagerResult(
                success=True,
                data={"alert_id": alert_id, "acknowledged": True},
                metrics={},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _resolve_alert(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Resolve an alert."""
        try:
            alert_id = payload.get("alert_id", "")
            resolved_by = payload.get("resolved_by", "system")
            resolution_notes = payload.get("resolution_notes", "")

            if alert_id not in self.alerts:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Alert not found: {alert_id}",
                )

            with self._alert_lock:
                alert = self.alerts[alert_id]
                alert["resolved"] = True
                alert["resolved_by"] = resolved_by
                alert["resolved_at"] = datetime.now().isoformat()
                alert["resolution_notes"] = resolution_notes
                alert["status"] = "resolved"

            return ManagerResult(
                success=True, data={"alert_id": alert_id, "resolved": True}, metrics={}
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _check_alert_rules(self, alert: Dict[str, Any]) -> None:
        """Check alert rules and trigger actions."""
        try:
            for rule_name, rule in self.alert_rules.items():
                if not rule.get("enabled", True):
                    continue

                # Check level match
                if rule.get("level") and alert["level"].value != rule["level"]:
                    continue

                # Check source match
                if rule.get("source") and alert["source"] != rule["source"]:
                    continue

                # Check message pattern
                if rule.get("message_pattern"):
                    import re

                    if not re.search(rule["message_pattern"], alert["message"]):
                        continue

                # Execute rule action
                action = rule.get("action", "log")
                if action == "escalate":
                    self._escalate_alert(alert, rule)
                elif action == "notify":
                    self._notify_alert(alert, rule)
                elif action == "auto_resolve":
                    self._auto_resolve_alert(alert, rule)

        except Exception as e:
            # Don't fail alert creation due to rule errors
            pass

    def _escalate_alert(self, alert: Dict[str, Any], rule: Dict[str, Any]) -> None:
        """Escalate an alert."""
        try:
            # Increase alert level
            current_level = alert["level"]
            if current_level == AlertLevel.LOW:
                alert["level"] = AlertLevel.MEDIUM
            elif current_level == AlertLevel.MEDIUM:
                alert["level"] = AlertLevel.HIGH
            elif current_level == AlertLevel.HIGH:
                alert["level"] = AlertLevel.CRITICAL

            alert["escalated"] = True
            alert["escalated_at"] = datetime.now().isoformat()
            alert["escalation_rule"] = rule.get("name", "unknown")
        except Exception:
            pass

    def _notify_alert(self, alert: Dict[str, Any], rule: Dict[str, Any]) -> None:
        """Send notification for alert."""
        try:
            # Add notification metadata
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
