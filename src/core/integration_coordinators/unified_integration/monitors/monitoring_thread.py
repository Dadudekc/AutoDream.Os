"""
Monitoring Thread
=================

Specialized component for managing monitoring thread operations.
Extracted from monitor.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import time
import threading
from typing import Dict, Optional, Any, Callable

from ..models import IntegrationType
from .metrics_collector import MetricsCollector
from .alert_manager import AlertManager


class MonitoringThread:
    """Manages monitoring thread operations."""

    def __init__(
        self,
        metrics_collector: MetricsCollector,
        alert_manager: AlertManager,
        config: Dict[str, Any],
    ):
        """Initialize monitoring thread."""
        self.metrics_collector = metrics_collector
        self.alert_manager = alert_manager
        self.config = config
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_interval = config.get("monitoring_interval", 5.0)  # seconds

    def start_monitoring(self) -> None:
        """Start monitoring thread."""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def stop_monitoring(self) -> None:
        """Stop monitoring thread."""
        self.monitoring_active = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        try:
            while self.monitoring_active:
                try:
                    # Collect metrics for all integration types
                    all_metrics = self.metrics_collector.get_all_metrics()

                    # Check alerts for each integration type
                    for integration_type, metrics in all_metrics.items():
                        alerts = self.alert_manager.check_alerts(metrics)
                        if alerts:
                            self.alert_manager.trigger_alerts(alerts)

                    # Sleep for monitoring interval
                    time.sleep(self.monitoring_interval)

                except Exception as e:
                    print(f"Error in monitoring loop: {e}")
                    time.sleep(1.0)  # Brief pause on error

        except Exception as e:
            print(f"Fatal error in monitoring loop: {e}")

    def is_monitoring_active(self) -> bool:
        """Check if monitoring is active."""
        return self.monitoring_active

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring thread status."""
        try:
            thread_alive = (
                self.monitoring_thread is not None and self.monitoring_thread.is_alive()
            )

            return {
                "active": self.monitoring_active,
                "thread_alive": thread_alive,
                "monitoring_interval": self.monitoring_interval,
                "thread_name": (
                    self.monitoring_thread.name if self.monitoring_thread else None
                ),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def set_monitoring_interval(self, interval: float) -> None:
        """Set monitoring interval."""
        try:
            if interval > 0:
                self.monitoring_interval = interval
        except Exception as e:
            print(f"Error setting monitoring interval: {e}")

    def cleanup(self) -> None:
        """Cleanup monitoring thread resources."""
        try:
            self.stop_monitoring()
        except Exception as e:
            print(f"Monitoring thread cleanup failed: {e}")
