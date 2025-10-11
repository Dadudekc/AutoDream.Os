"""
Monitoring Lifecycle Manager - Phase-2 V2 Compliance Refactoring
================================================================
Manages monitoring lifecycle, initialization, cleanup, and background tasks.
Author: Agent-5 (Monitoring Specialist) | License: MIT
"""

from __future__ import annotations

import threading
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .monitoring_state import MonitoringState

from ..contracts import ManagerContext


class MonitoringLifecycle:
    """Manages monitoring lifecycle operations."""

    def __init__(self, state: MonitoringState):
        """Initialize monitoring lifecycle manager."""
        self.state = state
        self._background_thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize monitoring system."""
        try:
            # Setup default alert rules
            self._setup_default_alert_rules()

            # Start background monitoring
            self._start_background_monitoring()

            context.logger("Monitoring Lifecycle initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize monitoring lifecycle: {e}")
            return False

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup monitoring system."""
        try:
            # Stop background monitoring
            self._stop_background_monitoring()

            # Clear all state
            self.state.clear_all()

            context.logger("Monitoring Lifecycle cleaned up")
            return True
        except Exception as e:
            context.logger(f"Error cleaning up monitoring lifecycle: {e}")
            return False

    def _setup_default_alert_rules(self) -> None:
        """Setup default alert rules."""
        default_rules = {
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
        self.state.set_alert_rules(default_rules)

    def _start_background_monitoring(self) -> None:
        """Start background monitoring tasks."""
        if self._background_thread and self._background_thread.is_alive():
            return

        self._stop_event.clear()
        self._background_thread = threading.Thread(target=self._background_monitor, daemon=True)
        self._background_thread.start()

    def _stop_background_monitoring(self) -> None:
        """Stop background monitoring tasks."""
        self._stop_event.set()
        if self._background_thread:
            self._background_thread.join(timeout=5.0)

    def _background_monitor(self) -> None:
        """Background monitoring loop."""
        while not self._stop_event.is_set():
            try:
                # Clean up old resolved alerts (older than 24 hours)
                self._cleanup_old_alerts()

                # Clean up old metric history (older than 7 days)
                self._cleanup_old_metrics()

                # Wait 5 minutes before next cleanup cycle
                if self._stop_event.wait(300):
                    break

            except Exception:
                # Continue on error, don't crash background thread
                continue

    def _cleanup_old_alerts(self) -> None:
        """Clean up old resolved alerts."""
        cutoff_time = datetime.now() - timedelta(hours=24)
        alerts = self.state.get_all_alerts()

        to_remove = []
        for alert_id, alert in alerts.items():
            if (
                alert.get("resolved")
                and "resolved_at" in alert
                and datetime.fromisoformat(alert["resolved_at"]) < cutoff_time
            ):
                to_remove.append(alert_id)

        for alert_id in to_remove:
            self.state.remove_alert(alert_id)

    def _cleanup_old_metrics(self) -> None:
        """Clean up old metric history."""
        cutoff_time = datetime.now() - timedelta(days=7)

        for metric_name in list(self.state.metric_history.keys()):
            history = self.state.metric_history[metric_name]
            filtered_history = [
                entry
                for entry in history
                if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
            ]
            self.state.metric_history[metric_name] = filtered_history
