#!/usr/bin/env python3
"""
File Metadata Operations - V2 Compliance Module
==============================================

File metadata and basic operations.
Extracted from unified_file_utils.py.

Author: Agent-5 (Business Intelligence & Team Beta Leader) - V2 Refactoring
License: MIT
"""

import hashlib
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class FileOperation(ABC):
    """Abstract base class for file operations."""

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute the file operation."""
        pass


class FileMetadataOperations:
    """Handles file metadata operations."""

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()

    @staticmethod
    def is_file_readable(file_path: str) -> bool:
        """Check if a file is readable."""
        try:
            with open(file_path, encoding="utf-8") as f:
                f.read(1)
            return True
        except Exception:
            return False

    @staticmethod
    def is_file_writable(file_path: str) -> bool:
        """Check if a file is writable."""
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_size(file_path: str) -> int | None:
        """Get file size in bytes."""
        try:
            return Path(file_path).stat().st_size
        except Exception as e:
            logger.error(f"Failed to get file size for {file_path}: {e}")
            return None

    @staticmethod
    def get_file_modified_time(file_path: str) -> datetime | None:
        """Get file last modified time."""
        try:
            timestamp = Path(file_path).stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except Exception:
            return None

    @staticmethod
    def get_file_hash(file_path: str) -> str | None:
        """Get SHA256 hash of file."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Failed to get hash for {file_path}: {e}")
            return None

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension."""
        return Path(file_path).suffix.lower()

    @staticmethod
    def is_json_file(file_path: str) -> bool:
        """Check if file has JSON extension."""
        return FileMetadataOperations.get_file_extension(file_path) == ".json"
