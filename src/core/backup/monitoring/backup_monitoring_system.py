#!/usr/bin/env python3
"""
Backup Monitoring System - V2 Compliant Main Coordinator
========================================================

Consolidated backup monitoring system coordinating all components.
V2 COMPLIANT: Under 300 lines, focused orchestration responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .backup_monitor import BackupMonitor, MonitoringStatus
from .backup_metrics import BackupMetricsCollector, MetricType

logger = logging.getLogger(__name__)


class BackupMonitoringSystem:
    """Main backup monitoring system coordinator."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.backup_monitor = BackupMonitor(config)
        self.metrics_collector = BackupMetricsCollector(
            retention_hours=config.get('metrics_retention_hours', 24)
        )
        
        # System state
        self.running = False
        self.start_time: Optional[datetime] = None
        self.monitoring_tasks: List[asyncio.Task] = []
    
    async def initialize(self) -> bool:
        """Initialize the backup monitoring system."""
        try:
            self.logger.info("Initializing backup monitoring system")
            
            # Validate configuration
            if not self._validate_config():
                self.logger.error("Invalid configuration")
                return False
            
            # Initialize components
            await self._initialize_components()
            
            self.logger.info("Backup monitoring system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize backup monitoring system: {e}")
            return False
    
    def _validate_config(self) -> bool:
        """Validate system configuration."""
        required_keys = ['backup_paths', 'check_interval']
        
        for key in required_keys:
            if key not in self.config:
                self.logger.error(f"Missing required config key: {key}")
                return False
        
        # Validate backup paths exist
        for path_str in self.config['backup_paths']:
            path = Path(path_str)
            if not path.exists():
                self.logger.warning(f"Backup path does not exist: {path}")
        
        return True
    
    async def _initialize_components(self) -> None:
        """Initialize system components."""
        # Initialize backup monitor
        if not await self.backup_monitor.start_monitoring():
            raise RuntimeError("Failed to start backup monitor")
        
        # Start background tasks
        self.monitoring_tasks = [
            asyncio.create_task(self._metrics_collection_loop()),
            asyncio.create_task(self._health_check_loop())
        ]
    
    async def start(self) -> bool:
        """Start the backup monitoring system."""
        if self.running:
            self.logger.warning("System already running")
            return True
        
        try:
            if not await self.initialize():
                return False
            
            self.running = True
            self.start_time = datetime.now()
            
            self.logger.info("Backup monitoring system started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start system: {e}")
            return False
    
    async def stop(self) -> bool:
        """Stop the backup monitoring system."""
        if not self.running:
            self.logger.warning("System not running")
            return True
        
        try:
            self.running = False
            
            # Stop monitoring
            await self.backup_monitor.stop_monitoring()
            
            # Cancel background tasks
            for task in self.monitoring_tasks:
                if not task.done():
                    task.cancel()
            
            # Wait for tasks to complete
            if self.monitoring_tasks:
                await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)
            
            self.monitoring_tasks.clear()
            
            self.logger.info("Backup monitoring system stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop system: {e}")
            return False
    
    async def _metrics_collection_loop(self) -> None:
        """Background task for collecting metrics."""
        while self.running:
            try:
                await self._collect_system_metrics()
                await asyncio.sleep(self.config.get('metrics_interval', 30))
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in metrics collection: {e}")
                await asyncio.sleep(5)
    
    async def _health_check_loop(self) -> None:
        """Background task for health checks."""
        while self.running:
            try:
                await self._perform_health_check()
                await asyncio.sleep(self.config.get('health_check_interval', 60))
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in health check: {e}")
                await asyncio.sleep(5)
    
    async def _collect_system_metrics(self) -> None:
        """Collect system metrics."""
        try:
            # Get backup summary
            backup_summary = self.backup_monitor.get_backup_summary()
            
            # Record metrics
            self.metrics_collector.record_metric(
                "total_backups",
                backup_summary['total_backups'],
                MetricType.GAUGE,
                description="Total number of monitored backups"
            )
            
            self.metrics_collector.record_metric(
                "total_backup_size_bytes",
                backup_summary['total_size_bytes'],
                MetricType.GAUGE,
                description="Total size of all backups in bytes"
            )
            
            # Record status counts
            for status, count in backup_summary['status_counts'].items():
                self.metrics_collector.record_metric(
                    f"backup_count_{status}",
                    count,
                    MetricType.GAUGE,
                    {"status": status},
                    f"Number of backups with status {status}"
                )
            
            # Record system uptime
            if self.start_time:
                uptime_seconds = (datetime.now() - self.start_time).total_seconds()
                self.metrics_collector.record_metric(
                    "system_uptime_seconds",
                    uptime_seconds,
                    MetricType.GAUGE,
                    description="System uptime in seconds"
                )
            
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")
    
    async def _perform_health_check(self) -> None:
        """Perform system health check."""
        try:
            # Check monitoring status
            monitor_status = self.backup_monitor.get_monitoring_status()
            
            if monitor_status['status'] != MonitoringStatus.RUNNING.value:
                self.logger.warning("Backup monitor not running")
                self.metrics_collector.record_metric(
                    "health_check_failed",
                    1,
                    MetricType.COUNTER,
                    {"component": "backup_monitor"},
                    "Backup monitor health check failed"
                )
            else:
                self.metrics_collector.record_metric(
                    "health_check_passed",
                    1,
                    MetricType.COUNTER,
                    {"component": "backup_monitor"},
                    "Backup monitor health check passed"
                )
            
            # Check for stale backups
            backup_summary = self.backup_monitor.get_backup_summary()
            stale_count = sum(
                1 for backup in backup_summary['backups']
                if backup['age_hours'] > self.config.get('max_backup_age_hours', 168)
            )
            
            if stale_count > 0:
                self.logger.warning(f"Found {stale_count} stale backups")
                self.metrics_collector.record_metric(
                    "stale_backups_detected",
                    stale_count,
                    MetricType.GAUGE,
                    description="Number of stale backups detected"
                )
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        monitor_status = self.backup_monitor.get_monitoring_status()
        backup_summary = self.backup_monitor.get_backup_summary()
        metrics_summary = self.metrics_collector.get_system_health_summary()
        
        return {
            "system": {
                "running": self.running,
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            },
            "monitoring": monitor_status,
            "backups": backup_summary,
            "metrics": metrics_summary,
            "configuration": {
                "backup_paths": self.config['backup_paths'],
                "check_interval": self.config.get('check_interval', 60),
                "metrics_interval": self.config.get('metrics_interval', 30),
                "health_check_interval": self.config.get('health_check_interval', 60)
            }
        }
    
    def get_backup_health_report(self) -> Dict[str, Any]:
        """Get detailed backup health report."""
        backup_summary = self.backup_monitor.get_backup_summary()
        
        # Calculate health scores for each backup
        backup_health = {}
        for backup in backup_summary['backups']:
            health_score = self.metrics_collector.get_backup_health_score(backup['id'])
            backup_health[backup['id']] = {
                "name": backup['name'],
                "status": backup['status'],
                "health_score": round(health_score, 2),
                "size_bytes": backup['size_bytes'],
                "age_hours": backup['age_hours']
            }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_backups": len(backup_health),
            "average_health_score": round(
                sum(b['health_score'] for b in backup_health.values()) / len(backup_health) 
                if backup_health else 0, 2
            ),
            "backups": backup_health
        }
    
    def get_metrics_export(self, format_type: str = "json", time_window_minutes: int = 60) -> str:
        """Export metrics in specified format."""
        return self.metrics_collector.export_metrics(format_type, time_window_minutes)

