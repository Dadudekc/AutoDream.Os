#!/usr/bin/env python3
"""
File Locking Models - V2 Compliance Module
=========================================

Data models and enums for file locking operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any
import time


class LockStatus(Enum):
    """Status of file lock operations."""
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    TIMEOUT = "timeout"
    ERROR = "error"
    STALE = "stale"


@dataclass
class LockConfig:
    """Configuration for file locking operations."""
    
    timeout_seconds: float = 30.0
    retry_interval: float = 0.1
    max_retries: int = 300
    cleanup_interval: float = 60.0
    stale_lock_age: float = 300.0  # 5 minutes
    enable_logging: bool = True
    enable_metrics: bool = True


@dataclass
class LockInfo:
    """Information about an active file lock."""
    
    lock_file: str
    pid: int
    thread_id: str
    timestamp: float
    process_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_stale(self, stale_age: float = 300.0) -> bool:
        """Check if lock is stale."""
        return time.time() - self.timestamp > stale_age
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "lock_file": self.lock_file,
            "pid": self.pid,
            "thread_id": self.thread_id,
            "timestamp": self.timestamp,
            "process_name": self.process_name,
            "metadata": self.metadata
        }


@dataclass
class LockResult:
    """Result of file lock operation."""
    
    success: bool
    status: LockStatus
    lock_info: Optional[LockInfo] = None
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "status": self.status.value,
            "lock_info": self.lock_info.to_dict() if self.lock_info else None,
            "error_message": self.error_message,
            "execution_time_ms": self.execution_time_ms,
            "retry_count": self.retry_count
        }


@dataclass
class LockMetrics:
    """Metrics for file locking operations."""
    
    total_locks_created: int = 0
    total_locks_acquired: int = 0
    total_locks_released: int = 0
    total_timeouts: int = 0
    total_errors: int = 0
    total_stale_cleanups: int = 0
    average_acquire_time_ms: float = 0.0
    average_release_time_ms: float = 0.0
    total_execution_time_ms: float = 0.0
    active_locks: int = 0
    last_updated: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_locks_created": self.total_locks_created,
            "total_locks_acquired": self.total_locks_acquired,
            "total_locks_released": self.total_locks_released,
            "total_timeouts": self.total_timeouts,
            "total_errors": self.total_errors,
            "total_stale_cleanups": self.total_stale_cleanups,
            "average_acquire_time_ms": self.average_acquire_time_ms,
            "average_release_time_ms": self.average_release_time_ms,
            "total_execution_time_ms": self.total_execution_time_ms,
            "active_locks": self.active_locks,
            "last_updated": self.last_updated
        }
    
    def update_averages(self) -> None:
        """Update average execution times."""
        if self.total_locks_acquired > 0:
            self.average_acquire_time_ms = self.total_execution_time_ms / self.total_locks_acquired
        if self.total_locks_released > 0:
            self.average_release_time_ms = self.total_execution_time_ms / self.total_locks_released
