#!/usr/bin/env python3
"""
Cross-Platform Test Utilities
=============================

This module provides cross-platform testing utilities for the Agent Cellphone V2 system,
ensuring tests work correctly on both Windows and Linux platforms.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import os
import sys
import platform
import tempfile
import shutil
import sqlite3
from pathlib import Path
from typing import Optional, Any, Dict, List
from contextlib import contextmanager
import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrossPlatformTestManager:
    """Cross-platform test management utilities."""
    
    def __init__(self):
        self.platform = platform.system()
        self.is_windows = self.platform == "Windows"
        self.temp_dir = None
        self.test_databases = []
    
    def setup_test_environment(self):
        """Set up cross-platform test environment."""
        # Create temporary directory for tests
        self.temp_dir = Path(tempfile.mkdtemp(prefix="agent_test_"))
        
        # Set up platform-specific configurations
        if self.is_windows:
            # Windows-specific test setup
            os.environ["TEST_PLATFORM"] = "windows"
        else:
            # Linux-specific test setup
            os.environ["TEST_PLATFORM"] = "linux"
        
        logger.info(f"Test environment setup for {self.platform}")
        return self.temp_dir
    
    def cleanup_test_environment(self):
        """Clean up test environment across platforms."""
        try:
            # Close all test databases
            for db_path in self.test_databases:
                self.cleanup_test_database(db_path)
            
            # Remove temporary directory
            if self.temp_dir and self.temp_dir.exists():
                if self.is_windows:
                    # Windows: Make files writable before removal
                    self._make_writable_recursive(self.temp_dir)
                
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                
        except Exception as e:
            logger.warning(f"Error cleaning up test environment: {e}")
    
    def _make_writable_recursive(self, path: Path):
        """Make directory and files writable (Windows-specific)."""
        try:
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o666)
        except (OSError, PermissionError):
            pass
    
    def create_test_database(self, name: str = "test.db") -> Path:
        """Create test database with cross-platform compatibility."""
        if not self.temp_dir:
            self.setup_test_environment()
        
        db_path = self.temp_dir / name
        
        # Create database with platform-specific settings
        try:
            if self.is_windows:
                # Windows: Use WAL mode and proper timeout
                conn = sqlite3.connect(
                    str(db_path),
                    timeout=30.0,
                    check_same_thread=False
                )
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
            else:
                # Linux: Standard connection
                conn = sqlite3.connect(str(db_path))
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
            
            conn.close()
            self.test_databases.append(db_path)
            return db_path
            
        except sqlite3.Error as e:
            logger.error(f"Error creating test database: {e}")
            raise
    
    def cleanup_test_database(self, db_path: Path):
        """Clean up test database across platforms."""
        try:
            if db_path.exists():
                if self.is_windows:
                    # Windows: Force close connections and wait
                    try:
                        conn = sqlite3.connect(str(db_path), timeout=1.0)
                        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                        conn.close()
                    except sqlite3.Error:
                        pass
                    
                    import time
                    time.sleep(0.1)
                
                # Remove database files
                db_path.unlink(missing_ok=True)
                
                # Remove WAL and SHM files
                wal_file = db_path.with_suffix('.db-wal')
                shm_file = db_path.with_suffix('.db-shm')
                wal_file.unlink(missing_ok=True)
                shm_file.unlink(missing_ok=True)
                
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not cleanup test database {db_path}: {e}")
    
    @contextmanager
    def test_database_connection(self, db_path: Path):
        """Context manager for test database connections."""
        connection = None
        try:
            if self.is_windows:
                connection = sqlite3.connect(
                    str(db_path),
                    timeout=30.0,
                    check_same_thread=False
                )
            else:
                connection = sqlite3.connect(str(db_path))
            
            connection.row_factory = sqlite3.Row
            yield connection
            
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                try:
                    connection.close()
                except sqlite3.Error as e:
                    logger.warning(f"Error closing connection: {e}")

# Global test manager instance
test_manager = CrossPlatformTestManager()

# Pytest fixtures
@pytest.fixture(scope="function")
def temp_dir():
    """Provide temporary directory for tests."""
    temp_path = test_manager.setup_test_environment()
    yield temp_path
    test_manager.cleanup_test_environment()

@pytest.fixture(scope="function")
def test_database(temp_dir):
    """Provide test database for tests."""
    db_path = test_manager.create_test_database()
    yield db_path
    test_manager.cleanup_test_database(db_path)

@pytest.fixture(scope="function")
def db_connection(test_database):
    """Provide database connection for tests."""
    with test_manager.test_database_connection(test_database) as conn:
        yield conn

# Platform detection utilities
def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"

def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"

def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"

def get_platform_name() -> str:
    """Get current platform name."""
    return platform.system()

def skip_if_windows(reason: str = "Test not supported on Windows"):
    """Skip test if running on Windows."""
    return pytest.mark.skipif(is_windows(), reason=reason)

def skip_if_linux(reason: str = "Test not supported on Linux"):
    """Skip test if running on Linux."""
    return pytest.mark.skipif(is_linux(), reason=reason)

def skip_if_macos(reason: str = "Test not supported on macOS"):
    """Skip test if running on macOS."""
    return pytest.mark.skipif(is_macos(), reason=reason)

# Test utilities
def assert_file_exists(file_path: Path):
    """Assert file exists with platform-specific error message."""
    assert file_path.exists(), f"File {file_path} does not exist on {get_platform_name()}"

def assert_file_not_exists(file_path: Path):
    """Assert file does not exist with platform-specific error message."""
    assert not file_path.exists(), f"File {file_path} still exists on {get_platform_name()}"

def assert_database_accessible(db_path: Path):
    """Assert database is accessible with platform-specific error message."""
    try:
        if is_windows():
            conn = sqlite3.connect(str(db_path), timeout=5.0)
        else:
            conn = sqlite3.connect(str(db_path))
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Database {db_path} not accessible on {get_platform_name()}: {e}")

def get_test_timeout() -> float:
    """Get platform-appropriate test timeout."""
    if is_windows():
        return 30.0  # Windows needs longer timeout
    else:
        return 10.0  # Linux is faster


