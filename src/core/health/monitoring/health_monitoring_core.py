import logging
import threading
import time
from datetime import datetime
from typing import Any, Dict, Optional

from ..alerting.models import AlertSeverity
from .health_monitoring_config import (
    HealthThreshold,
    initialize_default_thresholds,
)

from .health_monitoring_metrics import HealthMetricType, HealthSnapshot, HealthStatus
from .health_check_executor import HealthCheckExecutor
from .health_metrics_collector import HealthMetricsCollector
from .health_notification_manager import HealthNotificationManager
from .health_status_analyzer import HealthStatusAnalyzer

logger = logging.getLogger(__name__)


class HealthMonitoringOrchestrator:
    """Coordinates health monitoring activities."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.monitoring_active = False
        self.health_data: Dict[str, HealthSnapshot] = {}
        self.thresholds: Dict[
            HealthMetricType, HealthThreshold
        ] = initialize_default_thresholds()

        self.notification_manager = HealthNotificationManager()
        self.metrics_collector = HealthMetricsCollector(self.health_data)
        self.check_executor = HealthCheckExecutor(
            self.notification_manager, self.thresholds
        )
        self.status_analyzer = HealthStatusAnalyzer()

        self.health_check_interval = self.config.get("health_check_interval", 60)
        self.monitor_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start health monitoring."""
        if self.monitoring_active:
            logger.warning("Health monitoring already active")
            return
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._loop, daemon=True)
        self.monitor_thread.start()

    def stop(self) -> None:
        """Stop health monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)

    def _loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                self._collect_health_metrics()
                self._perform_health_checks()
                time.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"Error in health monitoring loop: {e}")
                time.sleep(10)

    def _collect_health_metrics(self) -> None:
        """Collect health metrics from all agents."""
        try:
            self.metrics_collector.collect_metrics()
        except Exception as e:
            logger.error(f"Error collecting health metrics: {e}")

    def _perform_health_checks(self) -> None:
        """Perform comprehensive health checks."""
        try:
            self.check_executor.execute_health_checks()
        except Exception as e:
            logger.error(f"Error executing health checks: {e}")

    def get_health_status(self, agent_id: str) -> Optional[HealthSnapshot]:
        """Get health status for a specific agent."""
        return self.health_data.get(agent_id)

    def get_all_health_status(self) -> Dict[str, HealthSnapshot]:
        """Get health status for all agents."""
        return self.health_data.copy()

    def update_health_thresholds(self, new_thresholds: Dict[HealthMetricType, HealthThreshold]) -> None:
        """Update health monitoring thresholds."""
        self.thresholds.update(new_thresholds)
        logger.info("Health monitoring thresholds updated")
