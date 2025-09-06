"""
File Lock Queries - V2 Compliance Module
=======================================

File locking query functionality.

V2 Compliance: < 300 lines, single responsibility, lock queries.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List, Optional, Dict, Any

from ..file_locking_models import LockInfo, LockMetrics
from ..file_locking_manager import FileLockManager


class LockQueries:
    """File locking query functionality."""

    def __init__(self, manager: FileLockManager):
        """Initialize lock queries."""
        self.manager = manager

    def get_locks_by_process(self, pid: int) -> List[LockInfo]:
        """Get locks owned by specific process."""
        active_locks = self.manager.get_active_locks()
        return [lock for lock in active_locks if lock.pid == pid]

    def get_locks_by_thread(self, thread_id: str) -> List[LockInfo]:
        """Get locks owned by specific thread."""
        active_locks = self.manager.get_active_locks()
        return [lock for lock in active_locks if lock.thread_id == thread_id]

    def get_locks_by_owner(self, owner: str) -> List[LockInfo]:
        """Get locks owned by specific owner."""
        active_locks = self.manager.get_active_locks()
        return [lock for lock in active_locks if lock.owner == owner]

    def get_locks_by_type(self, lock_type: str) -> List[LockInfo]:
        """Get locks by type."""
        active_locks = self.manager.get_active_locks()
        return [lock for lock in active_locks if lock.lock_type == lock_type]

    def get_locks_by_duration(
        self, min_duration: int, max_duration: int = None
    ) -> List[LockInfo]:
        """Get locks by duration range."""
        active_locks = self.manager.get_active_locks()
        filtered_locks = []

        for lock in active_locks:
            duration = lock.duration
            if min_duration <= duration:
                if max_duration is None or duration <= max_duration:
                    filtered_locks.append(lock)

        return filtered_locks

    def get_locks_by_metadata(
        self, metadata_key: str, metadata_value: Any
    ) -> List[LockInfo]:
        """Get locks by metadata key-value pair."""
        active_locks = self.manager.get_active_locks()
        return [
            lock
            for lock in active_locks
            if lock.metadata and lock.metadata.get(metadata_key) == metadata_value
        ]

    def get_lock_statistics(self) -> Dict[str, Any]:
        """Get lock statistics."""
        active_locks = self.manager.get_active_locks()

        if not active_locks:
            return {
                "total_locks": 0,
                "locks_by_type": {},
                "locks_by_owner": {},
                "average_duration": 0,
            }

        locks_by_type = {}
        locks_by_owner = {}
        total_duration = 0

        for lock in active_locks:
            # Count by type
            lock_type = lock.lock_type
            locks_by_type[lock_type] = locks_by_type.get(lock_type, 0) + 1

            # Count by owner
            owner = lock.owner
            locks_by_owner[owner] = locks_by_owner.get(owner, 0) + 1

            # Sum duration
            total_duration += lock.duration

        return {
            "total_locks": len(active_locks),
            "locks_by_type": locks_by_type,
            "locks_by_owner": locks_by_owner,
            "average_duration": (
                total_duration / len(active_locks) if active_locks else 0
            ),
        }

    def find_conflicting_locks(self, filepath: str) -> List[LockInfo]:
        """Find locks that conflict with the given filepath."""
        active_locks = self.manager.get_active_locks()
        conflicting_locks = []

        for lock in active_locks:
            if lock.filepath == filepath:
                conflicting_locks.append(lock)

        return conflicting_locks

    def get_lock_health_status(self) -> Dict[str, Any]:
        """Get lock health status."""
        metrics = self.manager.get_lock_metrics()

        return {
            "total_locks": metrics.total_locks,
            "active_locks": metrics.active_locks,
            "expired_locks": metrics.expired_locks,
            "failed_operations": metrics.failed_operations,
            "success_rate": metrics.success_rate,
            "health_status": "healthy" if metrics.success_rate > 0.9 else "degraded",
        }
