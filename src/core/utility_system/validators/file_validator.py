#!/usr/bin/env python3
"""
File Validator - V2 Compliance Module
====================================

Validation utilities for file operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from pathlib import Path
from typing import Union


class FileValidator:
    """Validator for file operations."""

    def validate_file_exists(self, file_path: Union[str, Path]) -> bool:
        """Validate file exists."""
        try:
            path = Path(file_path)
            return path.exists()
        except Exception:
            return False

    def validate_file_readable(self, file_path: Union[str, Path]) -> bool:
        """Validate file is readable."""
        try:
            path = Path(file_path)
            return path.exists() and path.is_file() and path.stat().st_mode & 0o444
        except Exception:
            return False

    def validate_file_writable(self, file_path: Union[str, Path]) -> bool:
        """Validate file is writable."""
        try:
            path = Path(file_path)
            if path.exists():
                return path.stat().st_mode & 0o222
            else:
                # Check if parent directory is writable
                return path.parent.exists() and path.parent.stat().st_mode & 0o222
        except Exception:
            return False

    def validate_content_size(self, content: str, max_size_mb: int) -> bool:
        """Validate content size."""
        try:
            size_bytes = len(content.encode('utf-8'))
            max_size_bytes = max_size_mb * 1024 * 1024
            return size_bytes <= max_size_bytes
        except Exception:
            return False

    def validate_file_extension(self, file_path: Union[str, Path], allowed_extensions: list = None) -> bool:
        """Validate file extension."""
        try:
            if allowed_extensions is None:
                return True
            
            path = Path(file_path)
            extension = path.suffix.lower()
            return extension in [ext.lower() for ext in allowed_extensions]
        except Exception:
            return False

    def validate_directory_path(self, dir_path: Union[str, Path]) -> bool:
        """Validate directory path."""
        try:
            path = Path(dir_path)
            # Check if path is valid and parent exists or can be created
            return path.parent.exists() or path.parent.parent.exists()
        except Exception:
            return False
