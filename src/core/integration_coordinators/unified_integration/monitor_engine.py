import logging

logger = logging.getLogger(__name__)
"""
Integration Monitor Engine - V2 Compliance Module
================================================

Core engine logic for integration monitoring system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""
import threading
import time
from collections.abc import Callable
from datetime import datetime

from .models import IntegrationConfig, IntegrationMetrics, IntegrationType
from .monitor_models import MonitoringAlert, MonitoringConfig, MonitoringStats


class IntegrationMonitorEngine:
    """Core engine for integration monitoring operations."""

    def __init__(self, config: IntegrationConfig, monitoring_config: MonitoringConfig = None):
        """Initialize integration monitor engine."""
        self.config = config
        self.monitoring_config = monitoring_config or MonitoringConfig()
        self.metrics: dict[IntegrationType, IntegrationMetrics] = {}
        self.monitoring_active = False
        self.monitoring_thread: threading.Thread | None = None
        self.monitoring_callbacks: list[Callable] = []
        self.stats = MonitoringStats()
        self.start_time = datetime.now()

    def start_monitoring(self) -> None:
        """Start monitoring system."""
        if self.monitoring_active:
            return
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def stop_monitoring(self) -> None:
        """Stop monitoring system."""
        self.monitoring_active = False
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5.0)

    def add_callback(self, callback: Callable) -> None:
        """Add monitoring callback."""
        if callback not in self.monitoring_callbacks:
            self.monitoring_callbacks.append(callback)

    def remove_callback(self, callback: Callable) -> None:
        """Remove monitoring callback."""
        if callback in self.monitoring_callbacks:
            self.monitoring_callbacks.remove(callback)

    def get_metrics(self, integration_type: IntegrationType) -> IntegrationMetrics | None:
        """Get metrics for specific integration type."""
        return self.metrics.get(integration_type)

    def get_all_metrics(self) -> dict[IntegrationType, IntegrationMetrics]:
        """Get all metrics."""
        return self.metrics.copy()

    def get_stats(self) -> MonitoringStats:
        """Get monitoring statistics."""
        self.stats.uptime_seconds = (datetime.now() - self.start_time).total_seconds()
        return self.stats

    def check_integration_health(self, integration_type: IntegrationType) -> bool:
        """Check health of specific integration."""
        metrics = self.metrics.get(integration_type)
        if not metrics:
            return False
        if metrics.error_rate > self.monitoring_config.alert_thresholds["error_rate"]:
            self._trigger_alert(
                MonitoringAlert(
                    alert_id=f"error_rate_{integration_type.value}_{int(time.time())}",
                    alert_type="error_rate",
                    message=f"High error rate detected: {metrics.error_rate:.2%}",
                    severity="warning",
                    timestamp=datetime.now(),
                    metadata={
                        "integration_type": integration_type.value,
                        "error_rate": metrics.error_rate,
                    },
                )
            )
            return False
        if metrics.avg_response_time > self.monitoring_config.alert_thresholds["response_time"]:
            self._trigger_alert(
                MonitoringAlert(
                    alert_id=f"response_time_{integration_type.value}_{int(time.time())}",
                    alert_type="response_time",
                    message=f"High response time detected: {metrics.avg_response_time:.2f}s",
                    severity="warning",
                    timestamp=datetime.now(),
                    metadata={
                        "integration_type": integration_type.value,
                        "response_time": metrics.avg_response_time,
                    },
                )
            )
            return False
        if metrics.throughput < self.monitoring_config.alert_thresholds["throughput"]:
            self._trigger_alert(
                MonitoringAlert(
                    alert_id=f"throughput_{integration_type.value}_{int(time.time())}",
                    alert_type="throughput",
                    message=f"Low throughput detected: {metrics.throughput:.2f} req/s",
                    severity="warning",
                    timestamp=datetime.now(),
                    metadata={
                        "integration_type": integration_type.value,
                        "throughput": metrics.throughput,
                    },
                )
            )
            return False
        return True

    def update_metrics(
        self, integration_type: IntegrationType, metrics: IntegrationMetrics
    ) -> None:
        """Update metrics for specific integration type."""
        self.metrics[integration_type] = metrics

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                self._perform_monitoring_cycle()
                time.sleep(self.monitoring_config.monitoring_interval)
            except Exception as e:
                self._handle_monitoring_error(e)

    def _perform_monitoring_cycle(self) -> None:
        """Perform one monitoring cycle."""
        self.stats.total_checks += 1
        self.stats.last_check_time = datetime.now()
        try:
            for integration_type in self.metrics.keys():
                if self.check_integration_health(integration_type):
                    self.stats.successful_checks += 1
                else:
                    self.stats.failed_checks += 1
            for callback in self.monitoring_callbacks:
                try:
                    callback(self.metrics)
                except Exception as e:
                    self._handle_callback_error(callback, e)
        except Exception as e:
            self.stats.failed_checks += 1
            self._handle_monitoring_error(e)

    def _trigger_alert(self, alert: MonitoringAlert) -> None:
        """Trigger monitoring alert."""
        if not self.monitoring_config.enable_alerts:
            return
        self.stats.alerts_triggered += 1
        if self.monitoring_config.enable_logging:
            logger.info(f"[MONITORING ALERT] {alert.alert_type}: {alert.message}")
        for callback in self.monitoring_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self._handle_callback_error(callback, e)

    def _handle_monitoring_error(self, error: Exception) -> None:
        """Handle monitoring error."""
        logger.info(f"[MONITORING ERROR] {error}")

    def _handle_callback_error(self, callback: Callable, error: Exception) -> None:
        """Handle callback error."""
        logger.info(f"[CALLBACK ERROR] {callback.__name__}: {error}")
