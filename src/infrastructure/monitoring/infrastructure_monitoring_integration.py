#!/usr/bin/env python3
"""
🐝 INFRASTRUCTURE MONITORING INTEGRATION
Phase 2 Batch 2A: Infrastructure Health Dashboard Integration

This module integrates consolidated infrastructure components with the health monitoring system:
- Unified logging system monitoring
- Consolidated file operations monitoring
- Configuration management health checks
- Infrastructure performance metrics
- Automated alerting integration
"""

from __future__ import annotations

import logging
import threading
import time
from datetime import datetime
from typing import Any

from .components.infrastructure_services import InfrastructureServices
from .components.monitoring_components import MonitoringComponents
from .components.performance_metrics import PerformanceMetricsCollector

try:
    from ...core.health.monitoring.health_monitoring_service import (
        AlertSeverity,
        HealthMetric,
        HealthMonitoringService,
        ServiceEndpoint,
        ServiceType,
        SystemHealthSnapshot,
    )
except ImportError:
    # Fallback mock classes for when health monitoring is not available
    class ServiceType:
        FILE_SYSTEM = "file_system"
        LOGGING_SYSTEM = "logging_system"
        CONFIGURATION_SYSTEM = "configuration_system"

    class AlertSeverity:
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"

    class ServiceEndpoint:
        def __init__(self, name: str, url: str = "", check_interval: int = 60):
            self.name = name
            self.url = url
            self.check_interval = check_interval

    class HealthMetric:
        def __init__(
            self, name: str, value: Any, unit: str = "", timestamp: datetime | None = None
        ):
            self.name = name
            self.value = value
            self.unit = unit
            self.timestamp = timestamp or datetime.now()

    class SystemHealthSnapshot:
        def __init__(self):
            self.overall_status = None
            self.services = {}
            self.metrics = []
            self.alerts = []
            self.timestamp = datetime.now()

    class HealthMonitoringService:
        def __init__(self):
            self.logger = logging.getLogger(__name__)

        def add_service(self, service_type: str, service_config: dict[str, Any]) -> None:
            self.logger.info(f"Mock: Added service {service_type}")

        def get_health_snapshot(self) -> SystemHealthSnapshot:
            return SystemHealthSnapshot()

        def add_alert_handler(self, handler: Any) -> None:
            self.logger.info("Mock: Added alert handler")


logger = logging.getLogger(__name__)


class InfrastructureMonitoringIntegration:
    """
    Integrates infrastructure components with health monitoring dashboard.

    Monitors:
    - File system health and usage
    - Logging system performance
    - Configuration management status
    - Backup system health
    - Cache performance
    - Operation error rates
    """

    def __init__(self, health_service: HealthMonitoringService | None = None):
        """Initialize infrastructure monitoring integration."""
        self.health_service = health_service or HealthMonitoringService()
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.monitoring_components = MonitoringComponents(health_service)
        self.infrastructure_services = InfrastructureServices()
        self.performance_collector = PerformanceMetricsCollector()

        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread: threading.Thread | None = None
        self.last_health_snapshot: SystemHealthSnapshot | None = None

    def start_monitoring(self) -> None:
        """Start infrastructure monitoring."""
        if self.monitoring_active:
            self.logger.warning("Infrastructure monitoring is already active")
            return

        try:
            # Register services with health monitoring
            self.monitoring_components.register_services()

            # Start monitoring components
            self.monitoring_components.start_monitoring()

            # Start main monitoring loop
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()

            self.logger.info("Infrastructure monitoring integration started successfully")

        except Exception as e:
            self.logger.error(f"Failed to start infrastructure monitoring: {e}")
            raise

    def stop_monitoring(self) -> None:
        """Stop infrastructure monitoring."""
        self.monitoring_active = False

        # Stop monitoring components
        self.monitoring_components.stop_monitoring()

        # Wait for monitoring thread to finish
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)

        self.logger.info("Infrastructure monitoring integration stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active:
            try:
                # Collect infrastructure status
                infrastructure_status = self.infrastructure_services.get_infrastructure_status()

                # Collect performance metrics
                performance_summary = self.performance_collector.get_performance_summary()

                # Update health service
                self._update_health_service(infrastructure_status, performance_summary)

                # Sleep for monitoring interval
                time.sleep(30)

            except Exception as e:
                self.logger.error(f"Error in infrastructure monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error

    def _update_health_service(
        self, infrastructure_status: dict[str, Any], performance_summary: dict[str, Any]
    ) -> None:
        """Update health service with collected data."""
        try:
            # Get current health snapshot
            snapshot = self.health_service.get_health_snapshot()

            # Add infrastructure metrics
            self._add_infrastructure_metrics(snapshot, infrastructure_status)

            # Add performance metrics
            performance_metrics = self.performance_collector.get_health_metrics()
            snapshot.metrics.extend(performance_metrics)

            # Update services status
            snapshot.services.update(
                {
                    "file_system": infrastructure_status.get("file_system", {}),
                    "logging_system": infrastructure_status.get("logging_system", {}),
                    "configuration_system": infrastructure_status.get("configuration_system", {}),
                }
            )

            # Store snapshot
            self.last_health_snapshot = snapshot

        except Exception as e:
            self.logger.error(f"Failed to update health service: {e}")

    def _add_infrastructure_metrics(
        self, snapshot: SystemHealthSnapshot, infrastructure_status: dict[str, Any]
    ) -> None:
        """Add infrastructure-specific metrics to health snapshot."""
        try:
            # File system metrics
            file_system = infrastructure_status.get("file_system", {})
            if "disk_usage" in file_system:
                disk_usage = file_system["disk_usage"]
                snapshot.metrics.extend(
                    [
                        HealthMetric("disk_usage_percent", disk_usage.get("usage_percent", 0), "%"),
                        HealthMetric("disk_free_gb", disk_usage.get("free_gb", 0), "GB"),
                    ]
                )

            # Logging system metrics
            logging_system = infrastructure_status.get("logging_system", {})
            if "total_size_mb" in logging_system:
                snapshot.metrics.append(
                    HealthMetric("log_size_mb", logging_system.get("total_size_mb", 0), "MB")
                )

            # Configuration system metrics
            config_system = infrastructure_status.get("configuration_system", {})
            if "file_count" in config_system:
                snapshot.metrics.append(
                    HealthMetric("config_files_count", config_system.get("file_count", 0), "files")
                )

        except Exception as e:
            self.logger.error(f"Failed to add infrastructure metrics: {e}")

    def get_health_snapshot(self) -> SystemHealthSnapshot | None:
        """Get the latest health snapshot."""
        return self.last_health_snapshot

    def get_infrastructure_status(self) -> dict[str, Any]:
        """Get current infrastructure status."""
        return self.infrastructure_services.get_infrastructure_status()

    def get_performance_summary(self) -> dict[str, Any]:
        """Get current performance summary."""
        return self.performance_collector.get_performance_summary()

    def record_operation_metrics(
        self,
        operation: str,
        response_time: float,
        success: bool = True,
        error_type: str | None = None,
    ) -> None:
        """Record operation metrics for monitoring."""
        # Record response time
        self.performance_collector.record_response_time(operation, response_time)

        # Record error if applicable
        if not success and error_type:
            self.performance_collector.record_error(operation, error_type)

    def record_cache_metrics(self, cache_name: str, hit: bool) -> None:
        """Record cache performance metrics."""
        if hit:
            self.performance_collector.record_cache_hit(cache_name)
        else:
            self.performance_collector.record_cache_miss(cache_name)

    def record_resource_usage(self, resource: str, usage: float) -> None:
        """Record resource usage metrics."""
        self.performance_collector.record_resource_usage(resource, usage)

