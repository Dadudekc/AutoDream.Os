#!/usr/bin/env python3
"""
File Locking System - Agent Cellphone V2
=======================================

Atomic file locking system for preventing race conditions in messaging operations.
Provides cross-platform file locking with timeout and cleanup mechanisms.

Features:
- Atomic file operations with advisory locking
- Cross-platform compatibility (Windows/Linux)
- Timeout and deadlock prevention
- Automatic lock cleanup on failures
- Thread-safe operations

Architecture:
- Repository Pattern: FileLockManager handles atomic file operations
- Service Layer: Integrates with messaging delivery services
- Dependency Injection: Modular locking injected via constructor

@maintainer Agent-1 (Integration & Core Systems Specialist)
@license MIT
"""

import os
import time
import json
import tempfile
import threading
import platform
from typing import Optional, Callable, Any, Dict
from pathlib import Path
from contextlib import contextmanager
from dataclasses import dataclass, field

from ..utils.logger import get_messaging_logger

# Platform-specific imports
if platform.system() == 'Windows':
    import msvcrt
else:
    import fcntl


@dataclass
class LockConfig:
    """Configuration for file locking operations."""
    timeout_seconds: float = 30.0
    retry_interval: float = 0.1
    max_retries: int = 300
    cleanup_interval: float = 60.0
    stale_lock_age: float = 300.0  # 5 minutes


@dataclass
class LockInfo:
    """Information about an active file lock."""
    lock_file: str
    pid: int
    thread_id: str
    timestamp: float
    operation: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class FileLockError(Exception):
    """Base exception for file locking operations."""
    pass


class LockTimeoutError(FileLockError):
    """Raised when lock acquisition times out."""
    pass


class LockCleanupError(FileLockError):
    """Raised when lock cleanup fails."""
    pass


class FileLock:
    """
    Atomic file locking with cross-platform support.

    Provides advisory locking with timeout and cleanup mechanisms.
    Uses lock files alongside target files for atomic operations.
    """

    def __init__(self, filepath: str, config: Optional[LockConfig] = None):
        """Initialize file lock for specific file.

        Args:
            filepath: Path to the file to lock
            config: Lock configuration (uses defaults if None)
        """
        self.filepath = Path(filepath)
        self.config = config or LockConfig()
        self.lock_file = self.filepath.with_suffix(self.filepath.suffix + '.lock')
        self.logger = get_messaging_logger()
        self._lock_fd: Optional[int] = None
        self._lock_info: Optional[LockInfo] = None

    def acquire(self, operation: str = "unknown", metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Acquire exclusive lock on file.

        Args:
            operation: Description of the operation requiring the lock
            metadata: Additional metadata for lock tracking

        Returns:
            bool: True if lock acquired, False if timeout

        Raises:
            LockTimeoutError: If lock cannot be acquired within timeout
        """
        start_time = time.time()
        attempts = 0

        while attempts < self.config.max_retries:
            try:
                # Try to acquire lock
                if self._try_acquire_lock(operation, metadata):
                    return True

                # Check for stale locks and clean them up
                self._cleanup_stale_locks()

                # Wait before retry
                time.sleep(self.config.retry_interval)
                attempts += 1

            except Exception as e:
                self.logger.error(f"Error acquiring lock for {self.filepath}: {e}")
                time.sleep(self.config.retry_interval)
                attempts += 1

        elapsed = time.time() - start_time
        self.logger.error(f"Lock acquisition timeout for {self.filepath} after {elapsed:.2f}s")
        raise LockTimeoutError(f"Could not acquire lock for {self.filepath} within {self.config.timeout_seconds}s")

    def release(self) -> bool:
        """Release the file lock.

        Returns:
            bool: True if lock released successfully, False otherwise
        """
        try:
            if self._lock_fd is not None:
                # Remove lock file
                if self.lock_file.exists():
                    self.lock_file.unlink()

                # Unlock file (platform-specific)
                if platform.system() == 'Windows':
                    try:
                        msvcrt.locking(self._lock_fd, msvcrt.LK_UNLCK, 1)
                    except (OSError, ValueError):
                        pass  # Lock might already be released or FD invalid

                # Close file descriptor
                try:
                    os.close(self._lock_fd)
                except OSError:
                    pass  # FD might already be closed

                self._lock_fd = None
                self._lock_info = None

                self.logger.debug(f"Lock released for {self.filepath}")
                return True

        except Exception as e:
            self.logger.error(f"Error releasing lock for {self.filepath}: {e}")

        return False

    def _try_acquire_lock(self, operation: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Attempt to acquire lock once.

        Returns:
            bool: True if lock acquired, False otherwise
        """
        try:
            # Create lock info
            self._lock_info = LockInfo(
                lock_file=str(self.lock_file),
                pid=os.getpid(),
                thread_id=threading.current_thread().ident or "unknown",
                timestamp=time.time(),
                operation=operation,
                metadata=metadata or {}
            )

            # Try to create and lock the lock file
            self._lock_fd = os.open(str(self.lock_file), os.O_CREAT | os.O_EXCL | os.O_RDWR)

            # Write lock info
            lock_data = {
                "pid": self._lock_info.pid,
                "thread_id": self._lock_info.thread_id,
                "timestamp": self._lock_info.timestamp,
                "operation": self._lock_info.operation,
                "metadata": self._lock_info.metadata
            }
            os.write(self._lock_fd, json.dumps(lock_data).encode('utf-8'))

            # Apply file lock (platform-specific)
            if platform.system() == 'Windows':
                # Windows: Use msvcrt.locking with retry mechanism
                import time
                max_retries = 10
                for attempt in range(max_retries):
                    try:
                        msvcrt.locking(self._lock_fd, msvcrt.LK_LOCK, 1)
                        break
                    except OSError as e:
                        if attempt == max_retries - 1:
                            raise BlockingIOError("Lock is held by another process") from e
                        time.sleep(0.01)  # Brief pause before retry
            else:
                # Unix/Linux: Use fcntl.flock
                fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

            self.logger.debug(f"Lock acquired for {self.filepath} ({operation})")
            return True

        except (OSError, BlockingIOError):
            # Lock file already exists or lock is held
            if self._lock_fd is not None:
                try:
                    os.close(self._lock_fd)
                except OSError:
                    pass
                self._lock_fd = None
            return False

        except Exception as e:
            self.logger.error(f"Unexpected error acquiring lock: {e}")
            if self._lock_fd is not None:
                try:
                    os.close(self._lock_fd)
                except OSError:
                    pass
                self._lock_fd = None
            return False

    def _cleanup_stale_locks(self) -> None:
        """Clean up stale lock files."""
        try:
            if not self.lock_file.exists():
                return

            # Read lock file to check if it's stale
            try:
                with open(self.lock_file, 'r') as f:
                    lock_data = json.load(f)

                lock_timestamp = lock_data.get('timestamp', 0)
                lock_pid = lock_data.get('pid', 0)
                current_time = time.time()

                # Check if lock is stale (old or dead process)
                if (current_time - lock_timestamp > self.config.stale_lock_age or
                    not self._is_process_alive(lock_pid)):

                    self.logger.warning(f"Cleaning up stale lock file: {self.lock_file}")
                    try:
                        self.lock_file.unlink()
                    except OSError as e:
                        self.logger.error(f"Failed to remove stale lock file: {e}")

            except (json.JSONDecodeError, OSError) as e:
                # Lock file is corrupted, remove it
                self.logger.warning(f"Removing corrupted lock file {self.lock_file}: {e}")
                try:
                    self.lock_file.unlink()
                except (OSError, PermissionError):
                    # On Windows, we might need to wait a bit and retry
                    time.sleep(0.1)
                    try:
                        self.lock_file.unlink()
                    except (OSError, PermissionError):
                        pass  # Give up if still can't delete

        except Exception as e:
            self.logger.error(f"Error during lock cleanup: {e}")

    def _is_process_alive(self, pid: int) -> bool:
        """Check if a process is still alive.

        Args:
            pid: Process ID to check

        Returns:
            bool: True if process is alive, False otherwise
        """
        try:
            os.kill(pid, 0)  # Signal 0 just checks if process exists
            return True
        except OSError:
            return False


@contextmanager
def atomic_file_operation(filepath: str, operation: str = "unknown",
                         config: Optional[LockConfig] = None,
                         metadata: Optional[Dict[str, Any]] = None):
    """Context manager for atomic file operations with locking.

    Args:
        filepath: Path to the file to operate on
        operation: Description of the operation
        config: Lock configuration
        metadata: Additional metadata

    Yields:
        Path: Path to the file (locked for exclusive access)

    Raises:
        LockTimeoutError: If lock cannot be acquired
        FileLockError: For other locking errors
    """
    lock = FileLock(filepath, config)
    lock.acquire(operation, metadata)

    try:
        yield filepath
    finally:
        lock.release()


class FileLockManager:
    """
    Manager for file locking operations across the messaging system.

    Provides high-level interface for atomic file operations with
    comprehensive error handling and cleanup.
    """

    def __init__(self, config: Optional[LockConfig] = None):
        """Initialize file lock manager.

        Args:
            config: Global lock configuration
        """
        self.config = config or LockConfig()
        self.logger = get_messaging_logger()
        self._active_locks: Dict[str, FileLock] = {}
        self._lock = threading.RLock()

    def atomic_write(self, filepath: str, content: str,
                    operation: str = "write", encoding: str = 'utf-8',
                    metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Atomically write content to file with locking.

        Args:
            filepath: Path to write to
            content: Content to write
            operation: Description of write operation
            encoding: File encoding
            metadata: Additional metadata

        Returns:
            bool: True if write successful, False otherwise
        """
        try:
            with atomic_file_operation(filepath, operation, self.config, metadata):
                # Ensure directory exists
                Path(filepath).parent.mkdir(parents=True, exist_ok=True)

                # Write content atomically
                with open(filepath, 'w', encoding=encoding) as f:
                    f.write(content)
                    f.flush()
                    os.fsync(f.fileno())  # Force write to disk

                self.logger.debug(f"Atomic write completed: {filepath}")
                return True

        except Exception as e:
            self.logger.error(f"Atomic write failed for {filepath}: {e}")
            return False

    def atomic_read(self, filepath: str, operation: str = "read",
                   encoding: str = 'utf-8',
                   metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Atomically read content from file with locking.

        Args:
            filepath: Path to read from
            operation: Description of read operation
            encoding: File encoding
            metadata: Additional metadata

        Returns:
            Optional[str]: File content if successful, None otherwise
        """
        try:
            with atomic_file_operation(filepath, operation, self.config, metadata):
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()

                self.logger.debug(f"Atomic read completed: {filepath}")
                return content

        except FileNotFoundError:
            self.logger.debug(f"File not found for atomic read: {filepath}")
            return None
        except Exception as e:
            self.logger.error(f"Atomic read failed for {filepath}: {e}")
            return None

    def atomic_update(self, filepath: str, update_func: Callable[[str], str],
                     operation: str = "update", encoding: str = 'utf-8',
                     metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Atomically update file content using a function.

        Args:
            filepath: Path to update
            update_func: Function that takes current content and returns new content
            operation: Description of update operation
            encoding: File encoding
            metadata: Additional metadata

        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            with atomic_file_operation(filepath, operation, self.config, metadata):
                # Read current content
                current_content = ""
                if Path(filepath).exists():
                    with open(filepath, 'r', encoding=encoding) as f:
                        current_content = f.read()

                # Apply update function
                new_content = update_func(current_content)

                # Write updated content
                with open(filepath, 'w', encoding=encoding) as f:
                    f.write(new_content)
                    f.flush()
                    os.fsync(f.fileno())

                self.logger.debug(f"Atomic update completed: {filepath}")
                return True

        except Exception as e:
            self.logger.error(f"Atomic update failed for {filepath}: {e}")
            return False

    def cleanup_stale_locks(self, directory: str) -> int:
        """Clean up all stale lock files in a directory.

        Args:
            directory: Directory to clean up

        Returns:
            int: Number of stale locks cleaned up
        """
        cleaned = 0
        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return 0

            # Find all lock files
            lock_files = list(dir_path.glob("**/*.lock"))

            for lock_file in lock_files:
                try:
                    lock = FileLock(str(lock_file.with_suffix('')), self.config)
                    lock._cleanup_stale_locks()
                    if not lock_file.exists():
                        cleaned += 1
                except Exception as e:
                    self.logger.error(f"Error cleaning lock {lock_file}: {e}")

        except Exception as e:
            self.logger.error(f"Error during lock cleanup in {directory}: {e}")

        if cleaned > 0:
            self.logger.info(f"Cleaned up {cleaned} stale lock files in {directory}")

        return cleaned
