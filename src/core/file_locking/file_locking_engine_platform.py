"""
File Locking Engine Platform - V2 Compliance Module
===================================================

Platform-specific functionality for file locking operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
from pathlib import Path


class FileLockEnginePlatform:
    """Platform-specific operations for file locking engine."""

    def __init__(self, base_engine, logger=None):
        """Initialize platform operations with base engine reference."""
        self.base_engine = base_engine
        self.logger = logger

    def _acquire_windows_lock(self, lock_file: Path) -> bool:
        """Acquire lock on Windows using msvcrt."""
        try:
            if not self.base_engine._msvcrt:
                return False

            # Create lock file if it doesn't exist
            lock_file.touch()

            # Open file for exclusive access
            with open(lock_file, "r+b") as f:
                # Try to lock the file
                try:
                    self.base_engine._msvcrt.locking(
                        f.fileno(), self.base_engine._msvcrt.LK_NBLCK, 1
                    )
                    return True
                except OSError:
                    return False

        except Exception as e:
            if self.logger:
                self.logger.error(f"Windows lock acquisition failed: {e}")
            return False

    def _acquire_unix_lock(self, lock_file: Path) -> bool:
        """Acquire lock on Unix-like systems using fcntl."""
        try:
            if not self.base_engine._fcntl:
                return False

            # Create lock file if it doesn't exist
            lock_file.touch()

            # Open file for exclusive access
            with open(lock_file, "r+b") as f:
                # Try to lock the file
                try:
                    self.base_engine._fcntl.flock(
                        f.fileno(),
                        self.base_engine._fcntl.LOCK_EX | self.base_engine._fcntl.LOCK_NB,
                    )
                    return True
                except OSError:
                    return False

        except Exception as e:
            if self.logger:
                self.logger.error(f"Unix lock acquisition failed: {e}")
            return False

    def _is_lock_stale(self, lock_file: Path) -> bool:
        """Check if a lock file is stale."""
        try:
            if not lock_file.exists():
                return False

            # Check file age
            file_age = time.time() - lock_file.stat().st_mtime
            stale_threshold = getattr(
                self.base_engine.config, "stale_lock_threshold", 3600
            )  # 1 hour default

            return file_age > stale_threshold

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error checking lock staleness: {e}")
            return False

    def _remove_stale_lock(self, lock_file: Path) -> None:
        """Remove a stale lock file."""
        try:
            if lock_file.exists():
                lock_file.unlink()
                if self.logger:
                    self.logger.info(f"Removed stale lock file: {lock_file}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error removing stale lock file: {e}")
