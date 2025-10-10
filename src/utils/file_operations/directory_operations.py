#!/usr/bin/env python3
"""
Directory Operations - V2 Compliance Module
==========================================

Directory and file listing operations.
Extracted from unified_file_utils.py.

Author: Agent-5 (Business Intelligence & Team Beta Leader) - V2 Refactoring
License: MIT
"""

import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class DirectoryOperations:
    """Handles directory and file listing operations."""

    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> list[str]:
        """List files in directory matching pattern."""
        try:
            path = Path(directory)
            if not path.exists() or not path.is_dir():
                return []
            return [str(f) for f in path.glob(pattern) if f.is_file()]
        except Exception as e:
            logger.error(f"Failed to list files in {directory}: {e}")
            return []

    @staticmethod
    def get_directory_size(directory_path: str) -> int:
        """Get total size of directory in bytes."""
        try:
            total = 0
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                return 0
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total += file_path.stat().st_size
            return total
        except Exception as e:
            logger.error(f"Failed to get directory size for {directory_path}: {e}")
            return 0

    @staticmethod
    def count_files(directory_path: str) -> int:
        """Count total files in directory recursively."""
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                return 0
            return sum(1 for _ in directory.rglob("*") if _.is_file())
        except Exception as e:
            logger.error(f"Failed to count files in {directory_path}: {e}")
            return 0




