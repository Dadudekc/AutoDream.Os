#!/usr/bin/env python3
"""
File Locking Manager - V2 Compliance Module
==========================================

High-level file locking management for V2 compliance.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
from pathlib import Path
from typing import Optional, Dict, Any, List

from .file_locking_models import (
    LockConfig,
    LockInfo,
    LockStatus,
    LockResult,
    LockMetrics,
)
from .file_locking_engine import FileLockEngine


class FileLockManager:
    """High-level file locking manager."""

    def __init__(self, config: LockConfig = None):
        """Initialize file lock manager."""
        self.config = config or LockConfig()
        self.engine = FileLockEngine(self.config)

    def create_file_lock(
        self, filepath: str, metadata: Dict[str, Any] = None
    ) -> LockResult:
        """Create a file lock."""
        return self.engine.create_lock(filepath, metadata)

    def acquire_lock(
        self, filepath: str, metadata: Dict[str, Any] = None
    ) -> LockResult:
        """Acquire a file lock with retry logic."""
        lock_result = self.engine.create_lock(filepath, metadata)

        if not lock_result.success:
            return lock_result

        # Try to acquire lock with retry logic
        for attempt in range(self.config.max_retries):
            acquire_result = self.engine.acquire_lock(lock_result.lock_info)

            if acquire_result.success:
                return acquire_result

            if acquire_result.status == LockStatus.LOCKED:
                # Lock is held by another process, wait and retry
                time.sleep(self.config.retry_interval)
                continue
            else:
                # Error occurred, return immediately
                return acquire_result

        # Timeout reached
        return LockResult(
            success=False,
            status=LockStatus.TIMEOUT,
            error_message=f"Timeout after {self.config.max_retries} attempts",
            execution_time_ms=self.config.max_retries
            * self.config.retry_interval
            * 1000,
            retry_count=self.config.max_retries,
        )

    def release_lock(self, filepath: str) -> LockResult:
        """Release a file lock."""
        lock_file = f"{filepath}.lock"

        # Find the lock info
        lock_info = None
        for active_lock in self.engine._active_locks.values():
            if active_lock.lock_file == lock_file:
                lock_info = active_lock
                break

        if not lock_info:
            return LockResult(
                success=False, status=LockStatus.ERROR, error_message="Lock not found"
            )

        return self.engine.release_lock(lock_info)

    def is_locked(self, filepath: str) -> bool:
        """Check if file is locked."""
        return self.engine.is_locked(filepath)

    def cleanup_stale_locks(self) -> int:
        """Clean up stale locks."""
        return self.engine.cleanup_stale_locks()

    def get_active_locks(self) -> List[LockInfo]:
        """Get list of active locks."""
        return list(self.engine._active_locks.values())

    def get_lock_info(self, filepath: str) -> Optional[LockInfo]:
        """Get lock information for a file."""
        lock_file = f"{filepath}.lock"
        return self.engine._active_locks.get(lock_file)

    def force_release_lock(self, filepath: str) -> LockResult:
        """Force release a lock (use with caution)."""
        lock_file = Path(f"{filepath}.lock")

        try:
            if lock_file.exists():
                lock_file.unlink()

            # Remove from active locks
            lock_key = f"{filepath}.lock"
            if lock_key in self.engine._active_locks:
                del self.engine._active_locks[lock_key]
                self.engine.metrics.active_locks = len(self.engine._active_locks)

            return LockResult(
                success=True, status=LockStatus.UNLOCKED, execution_time_ms=0.0
            )

        except Exception as e:
            return LockResult(
                success=False, status=LockStatus.ERROR, error_message=str(e)
            )

    def get_metrics(self) -> LockMetrics:
        """Get locking metrics."""
        return self.engine.get_metrics()

    def reset_metrics(self) -> None:
        """Reset metrics."""
        self.engine.metrics = LockMetrics()

    def get_lock_summary(self) -> Dict[str, Any]:
        """Get summary of lock status."""
        active_locks = self.get_active_locks()
        metrics = self.get_metrics()

        return {
            "active_locks": len(active_locks),
            "total_created": metrics.total_locks_created,
            "total_acquired": metrics.total_locks_acquired,
            "total_released": metrics.total_locks_released,
            "total_errors": metrics.total_errors,
            "total_timeouts": metrics.total_timeouts,
            "average_acquire_time_ms": metrics.average_acquire_time_ms,
            "average_release_time_ms": metrics.average_release_time_ms,
            "stale_cleanups": metrics.total_stale_cleanups,
        }
