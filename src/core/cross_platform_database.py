#!/usr/bin/env python3
"""
Cross-Platform Database Utilities
=================================

This module provides cross-platform database utilities for the Agent Cellphone V2 system,
ensuring compatibility between Windows and Linux platforms.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import logging
import os
import platform
import shutil
import sqlite3
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrossPlatformDatabase:
    """Cross-platform database management utilities."""

    def __init__(self, db_path: str = "data/agent_system.db"):
        """Initialize cross-platform database manager."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self.platform = platform.system()
        self.is_windows = self.platform == "Windows"

    def get_connection_string(self) -> str:
        """Get platform-appropriate connection string."""
        if self.is_windows:
            # Windows-specific connection options
            return f"file:{self.db_path}?mode=rwc&cache=shared&timeout=30000"
        else:
            # Linux/Unix connection options
            return str(self.db_path)

    @contextmanager
    def get_connection(self):
        """Get database connection with proper cleanup."""
        connection = None
        try:
            if self.is_windows:
                # Windows: Use WAL mode and proper timeout
                with sqlite3.connect(
                    str(self.db_path), timeout=30.0, check_same_thread=False
                ) as connection:
                    connection.execute("PRAGMA journal_mode=WAL")
                    connection.execute("PRAGMA synchronous=NORMAL")
                    connection.execute("PRAGMA cache_size=10000")
                    connection.execute("PRAGMA temp_store=MEMORY")
            else:
                # Linux: Standard connection
                with sqlite3.connect(str(self.db_path)) as connection:
                    connection.execute("PRAGMA journal_mode=WAL")
                    connection.execute("PRAGMA synchronous=NORMAL")

            connection.row_factory = sqlite3.Row
            yield connection

        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                try:
                    connection.close()
                except sqlite3.Error as e:
                    logger.warning(f"Error closing connection: {e}")

    def cleanup_database(self):
        """Cross-platform database cleanup."""
        try:
            if self.db_path.exists():
                if self.is_windows:
                    # Windows: Force close any remaining connections
                    try:
                        with self.get_connection() as conn:
                            conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                    except sqlite3.Error:
                        pass

                    # Wait a moment for file handles to release
                    import time

                    time.sleep(0.1)

                # Remove database file
                self.db_path.unlink(missing_ok=True)

                # Remove WAL and SHM files (SQLite temporary files)
                wal_file = self.db_path.with_suffix(".db-wal")
                shm_file = self.db_path.with_suffix(".db-shm")
                wal_file.unlink(missing_ok=True)
                shm_file.unlink(missing_ok=True)

        except (OSError, PermissionError) as e:
            logger.warning(f"Could not cleanup database: {e}")

    def create_temp_database(self) -> Path:
        """Create temporary database for testing."""
        temp_dir = Path(tempfile.gettempdir())
        temp_db = temp_dir / f"test_agent_system_{os.getpid()}.db"

        # Ensure temp directory exists
        temp_dir.mkdir(parents=True, exist_ok=True)

        return temp_db

    def copy_database(self, source: Path, destination: Path):
        """Cross-platform database copying."""
        try:
            if self.is_windows:
                # Windows: Use shutil for reliable copying
                shutil.copy2(source, destination)
            else:
                # Linux: Use shutil as well for consistency
                shutil.copy2(source, destination)
        except (OSError, PermissionError) as e:
            logger.error(f"Could not copy database: {e}")
            raise

    def get_platform_info(self) -> dict[str, Any]:
        """Get platform-specific information."""
        return {
            "platform": self.platform,
            "is_windows": self.is_windows,
            "python_version": sys.version,
            "architecture": platform.architecture(),
            "temp_dir": tempfile.gettempdir(),
            "db_path": str(self.db_path),
        }


class CrossPlatformFileManager:
    """Cross-platform file management utilities."""

    def __init__(self):
        self.platform = platform.system()
        self.is_windows = self.platform == "Windows"

    def safe_remove(self, file_path: Path):
        """Safely remove file across platforms."""
        try:
            if file_path.exists():
                if self.is_windows:
                    # Windows: Make file writable first
                    file_path.chmod(0o666)

                file_path.unlink(missing_ok=True)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not remove file {file_path}: {e}")

    def safe_remove_dir(self, dir_path: Path):
        """Safely remove directory across platforms."""
        try:
            if dir_path.exists():
                if self.is_windows:
                    # Windows: Make directory writable first
                    for root, dirs, files in os.walk(dir_path):
                        for d in dirs:
                            os.chmod(os.path.join(root, d), 0o777)
                        for f in files:
                            os.chmod(os.path.join(root, f), 0o666)

                shutil.rmtree(dir_path, ignore_errors=True)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not remove directory {dir_path}: {e}")

    def get_line_separator(self) -> str:
        """Get platform-appropriate line separator."""
        return os.linesep

    def normalize_path(self, path: str) -> Path:
        """Normalize path for current platform."""
        return Path(path).resolve()


# Global instances for easy access
db_manager = CrossPlatformDatabase()
file_manager = CrossPlatformFileManager()


def get_platform_info() -> dict[str, Any]:
    """Get current platform information."""
    return db_manager.get_platform_info()


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"
