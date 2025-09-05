#!/usr/bin/env python3
"""
File Locking Engine - V2 Compliance Module
=========================================

Core business logic for file locking operations.

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


class FileLockEngine:
    """Core engine for file locking operations."""

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
        """Create a file lock."""
        start_time = time.time()
        
        try:
            lock_file = f"{filepath}.lock"
            pid = os.getpid()
            thread_id = threading.get_ident()
            timestamp = time.time()
            
            lock_info = LockInfo(
                lock_file=lock_file,
                pid=pid,
                thread_id=str(thread_id),
                timestamp=timestamp,
                process_name=os.path.basename(filepath),
                metadata=metadata or {}
            )
            
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics("create", True, execution_time)
            
            return LockResult(
                success=True,
                status=LockStatus.LOCKED,
                lock_info=lock_info,
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics("create", False, execution_time)
            
            return LockResult(
                success=False,
                status=LockStatus.ERROR,
                error_message=str(e),
                execution_time_ms=execution_time
            )

    def acquire_lock(self, lock_info: LockInfo) -> LockResult:
        """Acquire a file lock."""
        start_time = time.time()
        retry_count = 0
        
        try:
            lock_file = Path(lock_info.lock_file)
            
            # Check if lock file exists and is not stale
            if lock_file.exists():
                if self._is_lock_stale(lock_file):
                    self._remove_stale_lock(lock_file)
                else:
                    # Lock is held by another process
                    execution_time = (time.time() - start_time) * 1000
                    self._update_metrics("acquire", False, execution_time)
                    
                    return LockResult(
                        success=False,
                        status=LockStatus.LOCKED,
                        execution_time_ms=execution_time,
                        retry_count=retry_count
                    )
            
            # Create lock file
            with open(lock_file, 'w') as f:
                f.write(f"{lock_info.pid}\n{lock_info.thread_id}\n{lock_info.timestamp}\n")
            
            # Platform-specific locking
            if self._is_windows:
                success = self._acquire_windows_lock(lock_file)
            else:
                success = self._acquire_unix_lock(lock_file)
            
            if success:
                with self._lock:
                    self._active_locks[lock_info.lock_file] = lock_info
                    self.metrics.active_locks = len(self._active_locks)
            
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics("acquire", success, execution_time)
            
            return LockResult(
                success=success,
                status=LockStatus.LOCKED if success else LockStatus.ERROR,
                lock_info=lock_info if success else None,
                execution_time_ms=execution_time,
                retry_count=retry_count
            )
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics("acquire", False, execution_time)
            
            return LockResult(
                success=False,
                status=LockStatus.ERROR,
                error_message=str(e),
                execution_time_ms=execution_time,
                retry_count=retry_count
            )

    def release_lock(self, lock_info: LockInfo) -> LockResult:
        """Release a file lock."""
        start_time = time.time()
        
        try:
            lock_file = Path(lock_info.lock_file)
            
            # Remove from active locks
            with self._lock:
                if lock_info.lock_file in self._active_locks:
                    del self._active_locks[lock_info.lock_file]
                    self.metrics.active_locks = len(self._active_locks)
            
            # Remove lock file
            if lock_file.exists():
                lock_file.unlink()
            
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics("release", True, execution_time)
            
            return LockResult(
                success=True,
                status=LockStatus.UNLOCKED,
                lock_info=lock_info,
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self._update_metrics("release", False, execution_time)
            
            return LockResult(
                success=False,
                status=LockStatus.ERROR,
                error_message=str(e),
                execution_time_ms=execution_time
            )

    def is_locked(self, filepath: str) -> bool:
        """Check if file is locked."""
        lock_file = Path(f"{filepath}.lock")
        
        if not lock_file.exists():
            return False
        
        if self._is_lock_stale(lock_file):
            self._remove_stale_lock(lock_file)
            return False
        
        return True

    def cleanup_stale_locks(self) -> int:
        """Clean up stale locks."""
        cleaned_count = 0
        current_time = time.time()
        
        for lock_file in Path(".").glob("*.lock"):
            if self._is_lock_stale(lock_file):
                self._remove_stale_lock(lock_file)
                cleaned_count += 1
        
        self.metrics.total_stale_cleanups += cleaned_count
        return cleaned_count

    def _acquire_windows_lock(self, lock_file: Path) -> bool:
        """Acquire lock on Windows."""
        if not self._msvcrt:
            return False
        
        try:
            with open(lock_file, 'r+b') as f:
                self._msvcrt.locking(f.fileno(), self._msvcrt.LK_NBLCK, 1)
                return True
        except (OSError, IOError):
            return False

    def _acquire_unix_lock(self, lock_file: Path) -> bool:
        """Acquire lock on Unix/Linux."""
        if not self._fcntl:
            return False
        
        try:
            with open(lock_file, 'r+b') as f:
                self._fcntl.flock(f.fileno(), self._fcntl.LOCK_EX | self._fcntl.LOCK_NB)
                return True
        except (OSError, IOError):
            return False

    def _is_lock_stale(self, lock_file: Path) -> bool:
        """Check if lock file is stale."""
        try:
            stat = lock_file.stat()
            return (time.time() - stat.st_mtime) > self.config.stale_lock_age
        except (OSError, IOError):
            return True

    def _remove_stale_lock(self, lock_file: Path) -> None:
        """Remove stale lock file."""
        try:
            lock_file.unlink()
        except (OSError, IOError):
            pass

    def get_metrics(self) -> LockMetrics:
        """Get locking metrics."""
        return self.metrics

    def _update_metrics(self, operation: str, success: bool, execution_time: float) -> None:
        """Update metrics."""
        self.metrics.total_execution_time_ms += execution_time
        
        if operation == "create":
            self.metrics.total_locks_created += 1
        elif operation == "acquire":
            self.metrics.total_locks_acquired += 1
            if not success:
                self.metrics.total_errors += 1
        elif operation == "release":
            self.metrics.total_locks_released += 1
            if not success:
                self.metrics.total_errors += 1
        
        self.metrics.update_averages()
        self.metrics.last_updated = time.time()
