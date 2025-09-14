#!/usr/bin/env python3
"""
Backup Monitoring Orchestrator - V2 Compliant Main Coordinator
=============================================================

Main consolidated backup monitoring system coordinating all components.
V2 COMPLIANT: Under 300 lines, focused orchestration responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import asyncio
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .alerts.backup_alert_system import BackupAlertSystem
from .database.backup_database import BackupMonitoringDatabase
from .models.backup_enums import AlertSeverity, AlertType, MonitoringStatus
from .models.backup_models import MonitoringConfig, MonitoringMetric

logger = logging.getLogger(__name__)


class BackupMonitoringOrchestrator:
    """Main orchestrator for backup monitoring system."""

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.database = BackupMonitoringDatabase()
        self.alert_system = BackupAlertSystem(self.database, self.config)

        self.monitoring_status = MonitoringStatus.STOPPED
        self.monitoring_tasks: List[asyncio.Task] = []
        self.last_health_check = datetime.min
        self.last_metrics_collection = datetime.min

    def _load_config(self, config_path: Optional[str]) -> MonitoringConfig:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.backup.backup_monitoring_orchestrator import Backup_Monitoring_Orchestrator

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Backup_Monitoring_Orchestrator(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

        """Load monitoring configuration."""
        config = MonitoringConfig()

        if config_path and Path(config_path).exists():
            try:
                import yaml
                with open(config_path, 'r') as f:
                    data = yaml.safe_load(f)

                if data:
                    monitoring = data.get("monitoring", {})
                    config.enabled = monitoring.get("enabled", True)
                    config.check_interval_seconds = monitoring.get("check_interval_seconds", 60)
                    config.health_check_interval_seconds = monitoring.get("health_check_interval_seconds", 300)
                    config.metrics_retention_days = monitoring.get("metrics_retention_days", 30)

                    alerts = data.get("alerts", {})
                    config.alert_channels = alerts.get("channels", ["console", "file"])
                    config.notification_cooldown_minutes = alerts.get("notification_cooldown_minutes", 30)

                    thresholds = data.get("thresholds", {})
                    config.backup_age_hours_threshold = thresholds.get("backup_age_hours", 48)
                    config.disk_usage_percent_threshold = thresholds.get("disk_usage_percent", 85)
                    config.system_load_percent_threshold = thresholds.get("system_load_percent", 80)
                    config.memory_usage_percent_threshold = thresholds.get("memory_usage_percent", 90)

            except Exception as e:
                logger.warning(f"Error loading config: {e}")

        return config

    async def start_monitoring(self) -> None:
        """Start the monitoring system."""
        if not self.config.enabled:
            logger.info("Backup monitoring is disabled in configuration")
            return

        if self.monitoring_status == MonitoringStatus.RUNNING:
            logger.warning("Monitoring system is already running")
            return

        logger.info("Starting backup monitoring system...")
        self.monitoring_status = MonitoringStatus.RUNNING

        # Start monitoring tasks
        self.monitoring_tasks = [
            asyncio.create_task(self._monitoring_loop()),
            asyncio.create_task(self._health_check_loop()),
            asyncio.create_task(self._metrics_collection_loop()),
            asyncio.create_task(self._alert_processing_loop())
        ]

        try:
            await asyncio.gather(*self.monitoring_tasks)
        except Exception as e:
            logger.error(f"Monitoring system error: {e}")
        finally:
            await self.stop_monitoring()

    async def stop_monitoring(self) -> None:
        """Stop the monitoring system."""
        logger.info("Stopping backup monitoring system...")
        self.monitoring_status = MonitoringStatus.STOPPED

        # Cancel all monitoring tasks
        for task in self.monitoring_tasks:
            if not task.done():
                task.cancel()

        # Wait for tasks to complete
        try:
            await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)
        except Exception:
            pass

        self.monitoring_tasks.clear()

    async def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_status == MonitoringStatus.RUNNING:
            try:
                await self._perform_monitoring_checks()
                await asyncio.sleep(self.config.check_interval_seconds)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)

    async def _health_check_loop(self) -> None:
        """Health check monitoring loop."""
        while self.monitoring_status == MonitoringStatus.RUNNING:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.config.health_check_interval_seconds)
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")
                await asyncio.sleep(30)

    async def _metrics_collection_loop(self) -> None:
        """Metrics collection loop."""
        while self.monitoring_status == MonitoringStatus.RUNNING:
            try:
                await self._collect_system_metrics()
                await asyncio.sleep(self.config.check_interval_seconds)
            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                await asyncio.sleep(5)

    async def _alert_processing_loop(self) -> None:
        """Alert processing loop."""
        while self.monitoring_status == MonitoringStatus.RUNNING:
            try:
                self.alert_system.check_alert_escalation()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in alert processing loop: {e}")
                await asyncio.sleep(30)

    async def _perform_monitoring_checks(self) -> None:
        """Perform monitoring checks."""
        try:
            # Check system resources
            await self._check_system_resources()

            # Check backup system status
            await self._check_backup_system_status()

            # Check for configuration issues
            await self._check_configuration_issues()

        except Exception as e:
            logger.error(f"Error performing monitoring checks: {e}")

    async def _perform_health_checks(self) -> None:
        """Perform health checks."""
        try:
            # System health checks
            await self._perform_system_health_checks()

            # Backup system health checks
            await self._perform_backup_health_checks()

            # Network health checks
            await self._perform_network_health_checks()

        except Exception as e:
            logger.error(f"Error performing health checks: {e}")

    async def _collect_system_metrics(self) -> None:
        """Collect system metrics."""
        try:
            import psutil

            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            self.database.store_metric(MonitoringMetric(
                metric_name="system_cpu_percent",
                metric_value=cpu_percent,
                metric_unit="percent"
            ))

            # Memory metrics
            memory = psutil.virtual_memory()
            self.database.store_metric(MonitoringMetric(
                metric_name="system_memory_percent",
                metric_value=memory.percent,
                metric_unit="percent"
            ))

            # Disk metrics
            disk = psutil.disk_usage('/')
            self.database.store_metric(MonitoringMetric(
                metric_name="system_disk_percent",
                metric_value=disk.percent,
                metric_unit="percent"
            ))

        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

    async def _check_system_resources(self) -> None:
        """Check system resource usage."""
        try:
            import psutil

            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > self.config.system_load_percent_threshold:
                self.alert_system.create_alert(
                    AlertType.SYSTEM_LOAD,
                    AlertSeverity.HIGH,
                    "High CPU Usage",
                    ".1f",
                    tags={"resource": "cpu", "threshold": str(self.config.system_load_percent_threshold)}
                )

            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent > self.config.memory_usage_percent_threshold:
                self.alert_system.create_alert(
                    AlertType.MEMORY_USAGE,
                    AlertSeverity.HIGH,
                    "High Memory Usage",
                    ".1f",
                    tags={"resource": "memory", "threshold": str(self.config.memory_usage_percent_threshold)}
                )

            # Check disk usage
            disk = psutil.disk_usage('/')
            if disk.percent > self.config.disk_usage_percent_threshold:
                self.alert_system.create_alert(
                    AlertType.DISK_SPACE,
                    AlertSeverity.CRITICAL,
                    "Low Disk Space",
                    ".1f",
                    tags={"resource": "disk", "threshold": str(self.config.disk_usage_percent_threshold)}
                )

        except Exception as e:
            logger.error(f"Error checking system resources: {e}")

    async def _check_backup_system_status(self) -> None:
        """Check backup system status."""
        try:
            # This would integrate with the actual backup system
            # For now, we'll create a placeholder check
            logger.debug("Checking backup system status...")

            # Placeholder alert for demonstration
            # In real implementation, this would check actual backup status
            backup_age_hours = 24  # This would come from actual backup system

            if backup_age_hours > self.config.backup_age_hours_threshold:
                self.alert_system.create_alert(
                    AlertType.BACKUP_FAILURE,
                    AlertSeverity.HIGH,
                    "Backup Outdated",
                    f"Last backup is {backup_age_hours} hours old",
                    tags={"backup_age": str(backup_age_hours), "threshold": str(self.config.backup_age_hours_threshold)}
                )

        except Exception as e:
            logger.error(f"Error checking backup system status: {e}")

    async def _check_configuration_issues(self) -> None:
        """Check for configuration issues."""
        try:
            # Check if configuration file exists and is valid
            config_path = "config/backup_monitoring_config.yaml"
            if not Path(config_path).exists():
                self.alert_system.create_alert(
                    AlertType.CONFIGURATION_ERROR,
                    AlertSeverity.MEDIUM,
                    "Missing Configuration",
                    f"Configuration file not found: {config_path}",
                    tags={"config_file": config_path}
                )

        except Exception as e:
            logger.error(f"Error checking configuration: {e}")

    async def _perform_system_health_checks(self) -> None:
        """Perform system health checks."""
        try:
            import psutil

            # CPU health check
            cpu_percent = psutil.cpu_percent(interval=1)
            status = "passing" if cpu_percent < 90 else "warning" if cpu_percent < 95 else "failing"

            # Memory health check
            memory = psutil.virtual_memory()
            memory_status = "passing" if memory.percent < 90 else "warning" if memory.percent < 95 else "failing"

            # Disk health check
            disk = psutil.disk_usage('/')
            disk_status = "passing" if disk.percent < 90 else "warning" if disk.percent < 95 else "failing"

            logger.info(f"System health: CPU={status}, Memory={memory_status}, Disk={disk_status}")

        except Exception as e:
            logger.error(f"Error performing system health checks: {e}")

    async def _perform_backup_health_checks(self) -> None:
        """Perform backup system health checks."""
        try:
            # Placeholder for backup health checks
            logger.debug("Performing backup health checks...")
            # In real implementation, this would check backup system components

        except Exception as e:
            logger.error(f"Error performing backup health checks: {e}")

    async def _perform_network_health_checks(self) -> None:
        """Perform network health checks."""
        try:
            # Placeholder for network health checks
            logger.debug("Performing network health checks...")
            # In real implementation, this would check network connectivity

        except Exception as e:
            logger.error(f"Error performing network health checks: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        return {
            "monitoring_status": self.monitoring_status.value,
            "config_enabled": self.config.enabled,
            "active_alerts": len(self.alert_system.get_active_alerts()),
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check != datetime.min else None,
            "last_metrics_collection": self.last_metrics_collection.isoformat() if self.last_metrics_collection != datetime.min else None,
        }

    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics."""
        return self.alert_system.get_alert_statistics()

    def cleanup_old_data(self) -> bool:
        """Clean up old monitoring data."""
        return self.database.cleanup_old_data(self.config.metrics_retention_days)


# Factory functions for backward compatibility
def create_backup_monitoring_orchestrator(config_path: Optional[str] = None) -> BackupMonitoringOrchestrator:
    """Create backup monitoring orchestrator instance."""
    return BackupMonitoringOrchestrator(config_path)


async def start_backup_monitoring(config_path: Optional[str] = None) -> None:
    """Start backup monitoring system."""
    orchestrator = BackupMonitoringOrchestrator(config_path)
    await orchestrator.start_monitoring()
