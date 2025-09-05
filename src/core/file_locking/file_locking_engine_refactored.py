"""
File Locking Engine Refactored - V2 Compliance Module
====================================================

Refactored core business logic for file locking operations.

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
    LockConfig, LockInfo, LockStatus, LockResult, LockMetrics
)
from .file_locking_engine_base import FileLockEngineBase
from .file_locking_engine_operations import FileLockEngineOperations
from .file_locking_engine_platform import FileLockEnginePlatform


class FileLockEngine(FileLockEngineBase):
    """Refactored core engine for file locking operations."""

    def __init__(self, config: LockConfig = None):
        """Initialize file locking engine."""
        super().__init__(config)
        
        # Initialize modular components
        self.operations = FileLockEngineOperations(self, None)
        self.platform = FileLockEnginePlatform(self, None)

    def acquire_lock(self, lock_info: LockInfo) -> LockResult:
        """Acquire a file lock."""
        return self.operations.acquire_lock(lock_info)

    def release_lock(self, lock_info: LockInfo) -> LockResult:
        """Release a file lock."""
        return self.operations.release_lock(lock_info)

    def cleanup_stale_locks(self) -> int:
        """Clean up stale lock files."""
        return self.operations.cleanup_stale_locks()

    def _acquire_windows_lock(self, lock_file: Path) -> bool:
        """Acquire lock on Windows using msvcrt."""
        return self.platform._acquire_windows_lock(lock_file)

    def _acquire_unix_lock(self, lock_file: Path) -> bool:
        """Acquire lock on Unix-like systems using fcntl."""
        return self.platform._acquire_unix_lock(lock_file)

    def _is_lock_stale(self, lock_file: Path) -> bool:
        """Check if a lock file is stale."""
        return self.platform._is_lock_stale(lock_file)

    def _remove_stale_lock(self, lock_file: Path) -> None:
        """Remove a stale lock file."""
        self.platform._remove_stale_lock(lock_file)
