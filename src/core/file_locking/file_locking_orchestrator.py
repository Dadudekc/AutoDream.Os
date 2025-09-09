"""
File Locking Orchestrator - V2 Compliance Refactored
====================================================

Main coordination logic for file locking operations.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Any

from .file_locking_manager import FileLockManager
from .file_locking_models import LockConfig, LockInfo, LockMetrics, LockResult

# Import modular components
from .operations.lock_operations import LockOperations
from .operations.lock_queries import LockQueries


class FileLockingOrchestrator:
    """Main orchestrator for file locking operations - V2 compliant."""

    def __init__(self, config: LockConfig = None):
        """Initialize file locking orchestrator."""
        self.config = config or LockConfig()
        self.manager = FileLockManager(self.config)

        # Initialize modular components
        self.lock_operations = LockOperations(self.config)
        self.lock_queries = LockQueries(self.manager)

    # Delegate core operations to LockOperations
    def create_file_lock(self, filepath: str, metadata: dict[str, Any] = None) -> LockResult:
        """Create a file lock."""
        return self.lock_operations.create_file_lock(filepath, metadata)

    def acquire_lock(self, filepath: str, metadata: dict[str, Any] = None) -> LockResult:
        """Acquire a file lock."""
        return self.lock_operations.acquire_lock(filepath, metadata)

    def release_lock(self, filepath: str) -> LockResult:
        """Release a file lock."""
        return self.lock_operations.release_lock(filepath)

    def is_locked(self, filepath: str) -> bool:
        """Check if file is locked."""
        return self.lock_operations.is_locked(filepath)

    def get_lock_info(self, filepath: str) -> LockInfo | None:
        """Get lock information for a file."""
        return self.lock_operations.get_lock_info(filepath)

    def force_release_lock(self, filepath: str) -> LockResult:
        """Force release a file lock."""
        return self.lock_operations.force_release_lock(filepath)

    def extend_lock(self, filepath: str, duration: int) -> LockResult:
        """Extend lock duration."""
        return self.lock_operations.extend_lock(filepath, duration)

    def get_active_locks(self) -> list[LockInfo]:
        """Get all active locks."""
        return self.lock_operations.get_active_locks()

    def get_lock_metrics(self) -> LockMetrics:
        """Get lock metrics."""
        return self.lock_operations.get_lock_metrics()

    def cleanup_expired_locks(self) -> int:
        """Clean up expired locks."""
        return self.lock_operations.cleanup_expired_locks()

    def batch_acquire_locks(
        self, filepaths: list[str], metadata: dict[str, Any] = None
    ) -> dict[str, LockResult]:
        """Acquire multiple locks."""
        return self.lock_operations.batch_acquire_locks(filepaths, metadata)

    def batch_release_locks(self, filepaths: list[str]) -> dict[str, LockResult]:
        """Release multiple locks."""
        return self.lock_operations.batch_release_locks(filepaths)

    # Delegate query operations to LockQueries
    def get_locks_by_process(self, pid: int) -> list[LockInfo]:
        """Get locks owned by specific process."""
        return self.lock_queries.get_locks_by_process(pid)

    def get_locks_by_thread(self, thread_id: str) -> list[LockInfo]:
        """Get locks owned by specific thread."""
        return self.lock_queries.get_locks_by_thread(thread_id)

    def get_locks_by_owner(self, owner: str) -> list[LockInfo]:
        """Get locks owned by specific owner."""
        return self.lock_queries.get_locks_by_owner(owner)

    def get_locks_by_type(self, lock_type: str) -> list[LockInfo]:
        """Get locks by type."""
        return self.lock_queries.get_locks_by_type(lock_type)

    def get_locks_by_duration(self, min_duration: int, max_duration: int = None) -> list[LockInfo]:
        """Get locks by duration range."""
        return self.lock_queries.get_locks_by_duration(min_duration, max_duration)

    def get_locks_by_metadata(self, metadata_key: str, metadata_value: Any) -> list[LockInfo]:
        """Get locks by metadata key-value pair."""
        return self.lock_queries.get_locks_by_metadata(metadata_key, metadata_value)

    def get_lock_statistics(self) -> dict[str, Any]:
        """Get lock statistics."""
        return self.lock_queries.get_lock_statistics()

    def find_conflicting_locks(self, filepath: str) -> list[LockInfo]:
        """Find locks that conflict with the given filepath."""
        return self.lock_queries.find_conflicting_locks(filepath)

    def get_lock_health_status(self) -> dict[str, Any]:
        """Get lock health status."""
        return self.lock_queries.get_lock_health_status()


class FileLockContext:
    """Context manager for file locking."""

    def __init__(self, manager: FileLockManager, filepath: str, metadata: dict[str, Any] = None):
        """Initialize context manager."""
        self.manager = manager
        self.filepath = filepath
        self.metadata = metadata
        self.lock_result = None

    def __enter__(self):
        """Enter context and acquire lock."""
        self.lock_result = self.manager.acquire_lock(self.filepath, self.metadata)
        if not self.lock_result.success:
            raise RuntimeError(f"Failed to acquire lock: {self.lock_result.error_message}")
        return self.lock_result

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and release lock."""
        if self.lock_result and self.lock_result.success:
            self.manager.release_lock(self.filepath)


# Global instance for backward compatibility
_global_file_lock_manager = None


def get_file_lock_manager() -> FileLockingOrchestrator:
    """Get global file lock manager instance."""
    global _global_file_lock_manager

    if _global_file_lock_manager is None:
        _global_file_lock_manager = FileLockingOrchestrator()

    return _global_file_lock_manager
