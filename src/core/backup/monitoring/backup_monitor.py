#!/usr/bin/env python3
"""
Backup Monitor - V2 Compliant
=============================

Focused module for backup monitoring core functionality.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class BackupStatus(Enum):
    """Backup status enumeration."""
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    CANCELLED = "cancelled"


class MonitoringStatus(Enum):
    """Monitoring system status."""
    RUNNING = "running"
    STOPPED = "stopped"
    PAUSED = "paused"
    ERROR = "error"


@dataclass
class BackupInfo:
    """Backup information structure."""
    backup_id: str
    name: str
    path: Path
    size_bytes: int
    status: BackupStatus
    created_at: datetime
    modified_at: datetime
    checksum: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class MonitoringMetric:
    """Monitoring metric data."""
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    tags: Dict[str, str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}


class BackupMonitor:
    """Core backup monitoring functionality."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.monitoring_status = MonitoringStatus.STOPPED
        self.last_check = datetime.min
        self.check_interval = config.get('check_interval', 60)  # seconds
        
        # Backup tracking
        self.known_backups: Dict[str, BackupInfo] = {}
        self.metrics_history: List[MonitoringMetric] = []
        self.max_metrics_history = config.get('max_metrics_history', 1000)
    
    async def start_monitoring(self) -> bool:
        """Start backup monitoring."""
        try:
            if self.monitoring_status == MonitoringStatus.RUNNING:
                self.logger.warning("Monitoring already running")
                return True
            
            self.monitoring_status = MonitoringStatus.RUNNING
            self.logger.info("Starting backup monitoring")
            
            # Start monitoring loop
            asyncio.create_task(self._monitoring_loop())
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            self.monitoring_status = MonitoringStatus.ERROR
            return False
    
    async def stop_monitoring(self) -> bool:
        """Stop backup monitoring."""
        try:
            self.monitoring_status = MonitoringStatus.STOPPED
            self.logger.info("Stopped backup monitoring")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop monitoring: {e}")
            return False
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_status == MonitoringStatus.RUNNING:
            try:
                await self._check_backups()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.check_interval)
    
    async def _check_backups(self) -> None:
        """Check all monitored backup locations."""
        backup_paths = self.config.get('backup_paths', [])
        
        for backup_path in backup_paths:
            try:
                await self._scan_backup_location(Path(backup_path))
            except Exception as e:
                self.logger.error(f"Failed to scan backup path {backup_path}: {e}")
        
        self.last_check = datetime.now()
    
    async def _scan_backup_location(self, path: Path) -> None:
        """Scan a backup location for files."""
        if not path.exists():
            self.logger.warning(f"Backup path does not exist: {path}")
            return
        
        current_files = {}
        
        # Scan for backup files
        for file_path in path.rglob('*'):
            if file_path.is_file():
                backup_info = await self._analyze_backup_file(file_path)
                if backup_info:
                    current_files[backup_info.backup_id] = backup_info
        
        # Update known backups
        await self._update_backup_registry(current_files)
    
    async def _analyze_backup_file(self, file_path: Path) -> Optional[BackupInfo]:
        """Analyze a backup file and extract information."""
        try:
            stat = file_path.stat()
            
            # Determine backup status based on file age and size
            age_hours = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).total_seconds() / 3600
            status = self._determine_backup_status(file_path, age_hours, stat.st_size)
            
            backup_info = BackupInfo(
                backup_id=f"{file_path.parent.name}_{file_path.name}",
                name=file_path.name,
                path=file_path,
                size_bytes=stat.st_size,
                status=status,
                created_at=datetime.fromtimestamp(stat.st_ctime),
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                metadata={
                    'age_hours': age_hours,
                    'file_extension': file_path.suffix,
                    'parent_dir': str(file_path.parent)
                }
            )
            
            return backup_info
            
        except Exception as e:
            self.logger.error(f"Failed to analyze backup file {file_path}: {e}")
            return None
    
    def _determine_backup_status(self, file_path: Path, age_hours: float, size_bytes: int) -> BackupStatus:
        """Determine backup status based on file characteristics."""
        # Check if file is currently being written (size 0 or very small)
        if size_bytes == 0:
            return BackupStatus.IN_PROGRESS
        
        # Check if file is very new (might still be in progress)
        if age_hours < 0.1:  # Less than 6 minutes
            return BackupStatus.IN_PROGRESS
        
        # Check if file is too old (might be stale)
        max_age_hours = self.config.get('max_backup_age_hours', 168)  # 7 days default
        if age_hours > max_age_hours:
            return BackupStatus.FAILED
        
        # Check if file is reasonable size
        min_size_bytes = self.config.get('min_backup_size_bytes', 1024)  # 1KB default
        if size_bytes < min_size_bytes:
            return BackupStatus.FAILED
        
        return BackupStatus.SUCCESS
    
    async def _update_backup_registry(self, current_files: Dict[str, BackupInfo]) -> None:
        """Update the backup registry with current files."""
        # Record metrics for new/changed backups
        for backup_id, backup_info in current_files.items():
            if backup_id not in self.known_backups:
                # New backup detected
                self.logger.info(f"New backup detected: {backup_info.name}")
                await self._record_metric("backup_detected", 1, "count", {"backup_id": backup_id})
            else:
                # Check for changes
                old_info = self.known_backups[backup_id]
                if old_info.status != backup_info.status:
                    self.logger.info(f"Backup status changed: {backup_info.name} -> {backup_info.status.value}")
                    await self._record_metric("backup_status_change", 1, "count", {
                        "backup_id": backup_id,
                        "old_status": old_info.status.value,
                        "new_status": backup_info.status.value
                    })
        
        # Check for removed backups
        for backup_id in list(self.known_backups.keys()):
            if backup_id not in current_files:
                self.logger.warning(f"Backup removed: {self.known_backups[backup_id].name}")
                await self._record_metric("backup_removed", 1, "count", {"backup_id": backup_id})
                del self.known_backups[backup_id]
        
        # Update registry
        self.known_backups.update(current_files)
    
    async def _record_metric(self, name: str, value: float, unit: str, tags: Dict[str, str] = None) -> None:
        """Record a monitoring metric."""
        metric = MonitoringMetric(
            metric_name=name,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            tags=tags or {}
        )
        
        self.metrics_history.append(metric)
        
        # Maintain history limit
        if len(self.metrics_history) > self.max_metrics_history:
            self.metrics_history = self.metrics_history[-self.max_metrics_history:]
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status."""
        return {
            "status": self.monitoring_status.value,
            "last_check": self.last_check.isoformat(),
            "check_interval": self.check_interval,
            "known_backups": len(self.known_backups),
            "metrics_count": len(self.metrics_history)
        }
    
    def get_backup_summary(self) -> Dict[str, Any]:
        """Get summary of all backups."""
        status_counts = {}
        total_size = 0
        
        for backup in self.known_backups.values():
            status_counts[backup.status.value] = status_counts.get(backup.status.value, 0) + 1
            total_size += backup.size_bytes
        
        return {
            "total_backups": len(self.known_backups),
            "status_counts": status_counts,
            "total_size_bytes": total_size,
            "backups": [
                {
                    "id": backup.backup_id,
                    "name": backup.name,
                    "status": backup.status.value,
                    "size_bytes": backup.size_bytes,
                    "age_hours": backup.metadata.get('age_hours', 0)
                }
                for backup in self.known_backups.values()
            ]
        }
    
    def get_recent_metrics(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent monitoring metrics."""
        return [
            {
                "name": metric.metric_name,
                "value": metric.value,
                "unit": metric.unit,
                "timestamp": metric.timestamp.isoformat(),
                "tags": metric.tags
            }
            for metric in self.metrics_history[-limit:]
        ]

