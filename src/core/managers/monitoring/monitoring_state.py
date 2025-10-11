"""
Monitoring State Manager - Phase-2 V2 Compliance Refactoring
============================================================

Manages monitoring state, data structures, and thread-safe access.

Author: Agent-5 (Monitoring Specialist)
License: MIT
"""

from __future__ import annotations

import threading
from typing import Any


class MonitoringState:
    """Manages monitoring state and data structures."""

    def __init__(self):
        """Initialize monitoring state."""
        # Core data structures
        self.alerts: dict[str, dict[str, Any]] = {}
        self.metrics: dict[str, Any] = {}
        self.metric_history: dict[str, list[dict[str, Any]]] = {}
        self.widgets: dict[str, dict[str, Any]] = {}
        self.alert_rules: dict[str, dict[str, Any]] = {}

        # Thread safety locks
        self._alert_lock = threading.Lock()
        self._metric_lock = threading.Lock()
        self._widget_lock = threading.Lock()

        # Configuration
        self.max_alerts = 1000
        self.max_metric_history = 10000

    def add_alert(self, alert_id: str, alert: dict[str, Any]) -> None:
        """Add an alert to state."""
        with self._alert_lock:
            self.alerts[alert_id] = alert

    def get_alert(self, alert_id: str) -> dict[str, Any] | None:
        """Get an alert by ID."""
        return self.alerts.get(alert_id)

    def update_alert(self, alert_id: str, updates: dict[str, Any]) -> bool:
        """Update an alert."""
        if alert_id not in self.alerts:
            return False
        with self._alert_lock:
            self.alerts[alert_id].update(updates)
        return True

    def get_all_alerts(self) -> dict[str, dict[str, Any]]:
        """Get all alerts."""
        return dict(self.alerts)

    def remove_alert(self, alert_id: str) -> bool:
        """Remove an alert."""
        if alert_id not in self.alerts:
            return False
        with self._alert_lock:
            del self.alerts[alert_id]
        return True

    def add_metric(self, metric_name: str, metric_entry: dict[str, Any]) -> None:
        """Add or update a metric."""
        with self._metric_lock:
            self.metrics[metric_name] = metric_entry

            # Add to history
            if metric_name not in self.metric_history:
                self.metric_history[metric_name] = []

            self.metric_history[metric_name].append(metric_entry)

            # Prevent memory leak: limit history size
            if len(self.metric_history[metric_name]) > self.max_metric_history:
                self.metric_history[metric_name] = self.metric_history[metric_name][
                    -self.max_metric_history :
                ]

    def get_metric(self, metric_name: str) -> dict[str, Any] | None:
        """Get a metric by name."""
        return self.metrics.get(metric_name)

    def get_all_metrics(self) -> dict[str, Any]:
        """Get all metrics."""
        return dict(self.metrics)

    def get_metric_history(self, metric_name: str) -> list[dict[str, Any]]:
        """Get metric history."""
        return self.metric_history.get(metric_name, [])

    def add_widget(self, widget_id: str, widget: dict[str, Any]) -> None:
        """Add a widget to state."""
        with self._widget_lock:
            self.widgets[widget_id] = widget

    def get_widget(self, widget_id: str) -> dict[str, Any] | None:
        """Get a widget by ID."""
        return self.widgets.get(widget_id)

    def get_all_widgets(self) -> dict[str, dict[str, Any]]:
        """Get all widgets."""
        return dict(self.widgets)

    def set_alert_rules(self, rules: dict[str, dict[str, Any]]) -> None:
        """Set alert rules."""
        self.alert_rules = rules

    def get_alert_rules(self) -> dict[str, dict[str, Any]]:
        """Get alert rules."""
        return self.alert_rules

    def clear_all(self) -> None:
        """Clear all state."""
        with self._alert_lock:
            self.alerts.clear()
        with self._metric_lock:
            self.metrics.clear()
            self.metric_history.clear()
        with self._widget_lock:
            self.widgets.clear()

    def get_status(self) -> dict[str, Any]:
        """Get state status."""
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
