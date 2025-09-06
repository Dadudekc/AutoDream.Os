"""
File Locking Engine Base - V2 Compliance Module
===============================================

Base functionality for file locking operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import os
import time
import threading
import platform
from pathlib import Path
from typing import Optional, Dict, Any

from .file_locking_models import (
    LockConfig,
    LockInfo,
    LockStatus,
    LockResult,
    LockMetrics,
)


class FileLockEngineBase:
    """Base engine for file locking operations."""

    def __init__(self, config: LockConfig = None):
        """Initialize file locking engine."""
        self.config = config or LockConfig()
        self.metrics = LockMetrics()
        self._active_locks: Dict[str, LockInfo] = {}
        self._lock = threading.Lock()

        # Platform-specific setup
        self._is_windows = platform.system() == "Windows"
        self._setup_platform_specific()

    def _setup_platform_specific(self) -> None:
        """Setup platform-specific imports and configurations."""
        if self._is_windows:
            try:
                import msvcrt

                self._msvcrt = msvcrt
            except ImportError:
                self._msvcrt = None
        else:
            try:
                import fcntl

                self._fcntl = fcntl
            except ImportError:
                self._fcntl = None

    def create_lock(self, filepath: str, metadata: Dict[str, Any] = None) -> LockResult:
        """Create a lock for a file."""
        start_time = time.time()

        try:
            lock_file = Path(filepath + ".lock")
            lock_info = LockInfo(
                filepath=filepath,
                lock_file=str(lock_file),
                metadata=metadata or {},
                created_at=time.time(),
            )

            result = self.acquire_lock(lock_info)
            execution_time = time.time() - start_time
            self._update_metrics("create_lock", result.success, execution_time)

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            self._update_metrics("create_lock", False, execution_time)
            return LockResult(
                success=False,
                message=f"Failed to create lock: {str(e)}",
                lock_info=None,
            )

    def is_locked(self, filepath: str) -> bool:
        """Check if a file is currently locked."""
        try:
            with self._lock:
                return filepath in self._active_locks
        except Exception:
            return False

    def get_metrics(self) -> LockMetrics:
        """Get current lock metrics."""
        return self.metrics

    def _update_metrics(
        self, operation: str, success: bool, execution_time: float
    ) -> None:
        """Update lock metrics."""
        self.metrics.total_operations += 1
        if success:
            self.metrics.successful_operations += 1
        else:
            self.metrics.failed_operations += 1

        self.metrics.total_execution_time += execution_time
        self.metrics.average_execution_time = (
            self.metrics.total_execution_time / self.metrics.total_operations
        )
