#!/usr/bin/env python3
"""
File Locking Orchestrator - V2 Compliance Module
===============================================

Main coordination logic for file locking operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import Optional, Dict, Any, List

from .file_locking_models import (
    LockConfig,
    LockInfo,
    LockResult,
    LockMetrics,
)
from .file_locking_manager import FileLockManager


class FileLockingOrchestrator:
    """Main orchestrator for file locking operations."""

    def __init__(self, config: LockConfig = None):
        """Initialize file locking orchestrator."""
        self.config = config or LockConfig()
        self.manager = FileLockManager(self.config)

    # ================================
    # CORE LOCKING OPERATIONS
    # ================================
    
    def create_file_lock(self, filepath: str, metadata: Dict[str, Any] = None) -> LockResult:
        """Create a file lock."""
        return self.manager.create_file_lock(filepath, metadata)

    def acquire_lock(self, filepath: str, metadata: Dict[str, Any] = None) -> LockResult:
        """Acquire a file lock."""
        return self.manager.acquire_lock(filepath, metadata)

    def release_lock(self, filepath: str) -> LockResult:
        """Release a file lock."""
        return self.manager.release_lock(filepath)

    def is_locked(self, filepath: str) -> bool:
        """Check if file is locked."""
        return self.manager.is_locked(filepath)

    def cleanup_stale_locks(self) -> int:
        """Clean up stale locks."""
        return self.manager.cleanup_stale_locks()

    # ================================
    # ADVANCED OPERATIONS
    # ================================
    
    def get_active_locks(self) -> List[LockInfo]:
        """Get list of active locks."""
        return self.manager.get_active_locks()

    def get_lock_info(self, filepath: str) -> Optional[LockInfo]:
        """Get lock information for a file."""
        return self.manager.get_lock_info(filepath)

    def force_release_lock(self, filepath: str) -> LockResult:
        """Force release a lock."""
        return self.manager.force_release_lock(filepath)

    def get_metrics(self) -> LockMetrics:
        """Get locking metrics."""
        return self.manager.get_metrics()

    def reset_metrics(self) -> None:
        """Reset metrics."""
        self.manager.reset_metrics()

    def get_lock_summary(self) -> Dict[str, Any]:
        """Get summary of lock status."""
        return self.manager.get_lock_summary()

    # ================================
    # CONVENIENCE METHODS
    # ================================
    
    def with_lock(self, filepath: str, metadata: Dict[str, Any] = None):
        """Context manager for file locking."""
        return FileLockContext(self.manager, filepath, metadata)

    def batch_acquire_locks(self, filepaths: List[str]) -> Dict[str, LockResult]:
        """Acquire multiple locks."""
        results = {}
        for filepath in filepaths:
            results[filepath] = self.acquire_lock(filepath)
        return results

    def batch_release_locks(self, filepaths: List[str]) -> Dict[str, LockResult]:
        """Release multiple locks."""
        results = {}
        for filepath in filepaths:
            results[filepath] = self.release_lock(filepath)
        return results

    def get_locks_by_process(self, pid: int) -> List[LockInfo]:
        """Get locks owned by specific process."""
        active_locks = self.get_active_locks()
        return [lock for lock in active_locks if lock.pid == pid]

    def get_locks_by_thread(self, thread_id: str) -> List[LockInfo]:
        """Get locks owned by specific thread."""
        active_locks = self.get_active_locks()
        return [lock for lock in active_locks if lock.thread_id == thread_id]


class FileLockContext:
    """Context manager for file locking."""
    
    def __init__(self, manager: FileLockManager, filepath: str, metadata: Dict[str, Any] = None):
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


# ================================
# GLOBAL INSTANCE
# ================================

_global_file_lock_manager = None

def get_file_lock_manager() -> FileLockingOrchestrator:
    """Get global file lock manager instance."""
    global _global_file_lock_manager
    
    if _global_file_lock_manager is None:
        _global_file_lock_manager = FileLockingOrchestrator()
    
    return _global_file_lock_manager


# ================================
# CONVENIENCE FUNCTIONS
# ================================

def create_file_lock(filepath: str, metadata: Dict[str, Any] = None) -> LockResult:
    """Convenience function to create file lock."""
    orchestrator = get_file_lock_manager()
    return orchestrator.create_file_lock(filepath, metadata)

def acquire_lock(filepath: str, metadata: Dict[str, Any] = None) -> LockResult:
    """Convenience function to acquire lock."""
    orchestrator = get_file_lock_manager()
    return orchestrator.acquire_lock(filepath, metadata)

def release_lock(filepath: str) -> LockResult:
    """Convenience function to release lock."""
    orchestrator = get_file_lock_manager()
    return orchestrator.release_lock(filepath)

def is_locked(filepath: str) -> bool:
    """Convenience function to check if locked."""
    orchestrator = get_file_lock_manager()
    return orchestrator.is_locked(filepath)

def cleanup_stale_locks() -> int:
    """Convenience function to cleanup stale locks."""
    orchestrator = get_file_lock_manager()
    return orchestrator.cleanup_stale_locks()

def get_lock_metrics() -> LockMetrics:
    """Convenience function to get lock metrics."""
    orchestrator = get_file_lock_manager()
    return orchestrator.get_metrics()
