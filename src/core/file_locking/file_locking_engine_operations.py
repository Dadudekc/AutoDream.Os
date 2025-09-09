"""
File Locking Engine Operations - V2 Compliance Module
====================================================

Core operations for file locking functionality.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
from pathlib import Path

from .file_locking_models import LockInfo, LockResult


class FileLockEngineOperations:
    """Core operations for file locking engine."""

    def __init__(self, base_engine, logger=None):
        """Initialize operations with base engine reference."""
        self.base_engine = base_engine
        self.logger = logger

    def acquire_lock(self, lock_info: LockInfo) -> LockResult:
        """Acquire a file lock."""
        start_time = time.time()

        try:
            lock_file = Path(lock_info.lock_file)

            # Check if lock file exists and is stale
            if lock_file.exists() and self._is_lock_stale(lock_file):
                self._remove_stale_lock(lock_file)

            # Try to acquire lock
            success = False
            if self.base_engine._is_windows:
                success = self._acquire_windows_lock(lock_file)
            else:
                success = self._acquire_unix_lock(lock_file)

            if success:
                with self.base_engine._lock:
                    self.base_engine._active_locks[lock_info.filepath] = lock_info

                execution_time = time.time() - start_time
                self.base_engine._update_metrics("acquire_lock", True, execution_time)

                return LockResult(
                    success=True,
                    message="Lock acquired successfully",
                    lock_info=lock_info,
                )
            else:
                execution_time = time.time() - start_time
                self.base_engine._update_metrics("acquire_lock", False, execution_time)

                return LockResult(
                    success=False,
                    message="Failed to acquire lock - file may be locked by another process",
                    lock_info=None,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            self.base_engine._update_metrics("acquire_lock", False, execution_time)

            return LockResult(
                success=False, message=f"Error acquiring lock: {str(e)}", lock_info=None
            )

    def release_lock(self, lock_info: LockInfo) -> LockResult:
        """Release a file lock."""
        start_time = time.time()

        try:
            lock_file = Path(lock_info.lock_file)

            # Remove from active locks
            with self.base_engine._lock:
                if lock_info.filepath in self.base_engine._active_locks:
                    del self.base_engine._active_locks[lock_info.filepath]

            # Remove lock file
            if lock_file.exists():
                lock_file.unlink()

            execution_time = time.time() - start_time
            self.base_engine._update_metrics("release_lock", True, execution_time)

            return LockResult(
                success=True, message="Lock released successfully", lock_info=lock_info
            )

        except Exception as e:
            execution_time = time.time() - start_time
            self.base_engine._update_metrics("release_lock", False, execution_time)

            return LockResult(
                success=False, message=f"Error releasing lock: {str(e)}", lock_info=None
            )

    def cleanup_stale_locks(self) -> int:
        """Clean up stale lock files."""
        cleaned_count = 0

        try:
            # Get all lock files in the system
            lock_files = []
            for lock_info in self.base_engine._active_locks.values():
                lock_file = Path(lock_info.lock_file)
                if lock_file.exists() and self._is_lock_stale(lock_file):
                    lock_files.append(lock_file)

            # Remove stale locks
            for lock_file in lock_files:
                self._remove_stale_lock(lock_file)
                cleaned_count += 1

            if cleaned_count > 0:
                self.base_engine._update_metrics("cleanup_stale_locks", True, 0.0)

            return cleaned_count

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error cleaning up stale locks: {e}")
            return cleaned_count
