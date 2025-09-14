"""
File Lock Operations - V2 Compliance Module
==========================================

Core file locking operations functionality.

V2 Compliance: < 300 lines, single responsibility, lock operations.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Any

from ..file_locking_manager import FileLockManager
from ..file_locking_models import LockConfig, LockInfo, LockMetrics, LockResult


class LockOperations:
    """Core file locking operations."""

    def __init__(self, config: LockConfig = None):
        """Initialize lock operations."""
        self.config = config or LockConfig()
        self.manager = FileLockManager(self.config)

    def create_file_lock(self, filepath: str, metadata: dict[str, Any] = None) -> LockResult:
        """Create a file lock."""
        return self.manager.create_file_lock(filepath, metadata)

    def acquire_lock(self, filepath: str, metadata: dict[str, Any] = None) -> LockResult:
        """Acquire a file lock."""
        return self.manager.acquire_lock(filepath, metadata)

    def release_lock(self, filepath: str) -> LockResult:
        """Release a file lock."""
        return self.manager.release_lock(filepath)

    def is_locked(self, filepath: str) -> bool:
        """Check if file is locked."""
        return self.manager.is_locked(filepath)

    def get_lock_info(self, filepath: str) -> LockInfo | None:
        """Get lock information for a file."""
        return self.manager.get_lock_info(filepath)

    def force_release_lock(self, filepath: str) -> LockResult:
        """Force release a file lock."""
        return self.manager.force_release_lock(filepath)

    def extend_lock(self, filepath: str, duration: int) -> LockResult:
        """Extend lock duration."""
        return self.manager.extend_lock(filepath, duration)

    def get_active_locks(self) -> list[LockInfo]:
        """Get all active locks."""
        return self.manager.get_active_locks()

    def get_lock_metrics(self) -> LockMetrics:
        """Get lock metrics."""
        return self.manager.get_lock_metrics()

    def cleanup_expired_locks(self) -> int:
        """Clean up expired locks."""
        return self.manager.cleanup_expired_locks()

    def batch_acquire_locks(
        self, filepaths: list[str], metadata: dict[str, Any] = None
    ) -> dict[str, LockResult]:
        """Acquire multiple locks."""
        results = {}
        for filepath in filepaths:
            results[filepath] = self.acquire_lock(filepath, metadata)
        return results

    def batch_release_locks(self, filepaths: list[str]) -> dict[str, LockResult]:
        """Release multiple locks."""
        results = {}
        for filepath in filepaths:
            results[filepath] = self.release_lock(filepath)
        return results
