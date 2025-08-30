#!/usr/bin/env python3
"""
File Utilities for Emergency Database Recovery.

This module provides utility functions for file operations:
- File existence and accessibility checks
- File backup and restoration
- File validation and integrity checks
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class FileUtils:
    """Utility class for file operations."""

    @staticmethod
    def ensure_directory_exists(directory_path: str) -> bool:
        """Ensure a directory exists, create if it doesn't."""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()

    @staticmethod
    def is_file_readable(file_path: str) -> bool:
        """Check if a file is readable."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1)
            return True
        except Exception:
            return False

    @staticmethod
    def is_file_writable(file_path: str) -> bool:
        """Check if a file is writable."""
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0

    @staticmethod
    def get_file_modified_time(file_path: str) -> Optional[datetime]:
        """Get file last modified time."""
        try:
            timestamp = Path(file_path).stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except Exception:
            return None

    @staticmethod
    def create_backup(file_path: str, backup_suffix: str = ".backup") -> Optional[str]:
        """Create a backup of a file."""
        try:
            if not FileUtils.file_exists(file_path):
                return None

            backup_path = f"{file_path}{backup_suffix}"
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception:
            return None

    @staticmethod
    def restore_from_backup(backup_path: str, target_path: str) -> bool:
        """Restore a file from backup."""
        try:
            if not FileUtils.file_exists(backup_path):
                return False

            # Create backup of current file if it exists
            if FileUtils.file_exists(target_path):
                FileUtils.create_backup(target_path, ".pre_restore_backup")

            shutil.copy2(backup_path, target_path)
            return True
        except Exception:
            return False

    @staticmethod
    def safe_delete_file(file_path: str) -> bool:
        """Safely delete a file with backup."""
        try:
            if not FileUtils.file_exists(file_path):
                return True

            # Create backup before deletion
            backup_path = FileUtils.create_backup(file_path, ".pre_delete_backup")
            if not backup_path:
                return False

            Path(file_path).unlink()
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension."""
        return Path(file_path).suffix.lower()

    @staticmethod
    def is_json_file(file_path: str) -> bool:
        """Check if file has JSON extension."""
        return FileUtils.get_file_extension(file_path) == '.json'

    @staticmethod
    def list_files_in_directory(directory_path: str, pattern: str = "*") -> List[str]:
        """List files in directory matching pattern."""
        try:
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                return []

            return [str(f) for f in directory.glob(pattern) if f.is_file()]
        except Exception:
            return []

    @staticmethod
    def get_directory_size(directory_path: str) -> int:
        """Get total size of directory in bytes."""
        try:
            total_size = 0
            directory = Path(directory_path)
            
            if not directory.exists() or not directory.is_dir():
                return 0

            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size

            return total_size
        except Exception:
            return 0

    @staticmethod
    def validate_file_path(file_path: str) -> Dict[str, Any]:
        """Validate file path and return detailed information."""
        validation_result = {
            "path": file_path,
            "exists": False,
            "is_file": False,
            "is_directory": False,
            "readable": False,
            "writable": False,
            "size_bytes": 0,
            "modified_time": None,
            "errors": []
        }

        try:
            path_obj = Path(file_path)
            validation_result["exists"] = path_obj.exists()

            if validation_result["exists"]:
                validation_result["is_file"] = path_obj.is_file()
                validation_result["is_directory"] = path_obj.is_dir()
                validation_result["readable"] = FileUtils.is_file_readable(file_path)
                validation_result["writable"] = FileUtils.is_file_writable(file_path)
                validation_result["size_bytes"] = FileUtils.get_file_size(file_path)
                validation_result["modified_time"] = FileUtils.get_file_modified_time(file_path)

        except Exception as e:
            validation_result["errors"].append(str(e))

        return validation_result
