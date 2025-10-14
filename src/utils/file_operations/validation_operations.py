#!/usr/bin/env python3
"""
File Validation Operations Module
=================================

Handles comprehensive file validation and path checking.
Part of the unified file utilities system.

Author: Agent-8 (Operations & Support Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .file_metadata import FileMetadataOperations


@dataclass
class FileValidationResult:
    """
    Result of file validation.

    Attributes:
        path: File path that was validated
        exists: Whether the file/directory exists
        is_file: Whether the path is a file
        is_directory: Whether the path is a directory
        readable: Whether the file is readable
        writable: Whether the file is writable
        size_bytes: File size in bytes
        modified_time: Last modification time
        errors: List of validation errors (if any)
    """

    path: str
    exists: bool
    is_file: bool
    is_directory: bool
    readable: bool
    writable: bool
    size_bytes: int
    modified_time: datetime | None
    errors: list[str]


class FileValidator:
    """Handles comprehensive file validation."""

    @staticmethod
    def validate_file_path(file_path: str) -> FileValidationResult:
        """
        Validate file path and return detailed information.

        Args:
            file_path: Path to validate

        Returns:
            FileValidationResult: Detailed validation results
        """
        path = Path(file_path)
        errors = []

        return FileValidationResult(
            path=file_path,
            exists=path.exists(),
            is_file=path.is_file() if path.exists() else False,
            is_directory=path.is_dir() if path.exists() else False,
            readable=(
                FileMetadataOperations.is_file_readable(file_path) if path.exists() else False
            ),
            writable=(
                FileMetadataOperations.is_file_writable(file_path) if path.exists() else False
            ),
            size_bytes=FileMetadataOperations.get_file_size(file_path) or 0,
            modified_time=FileMetadataOperations.get_file_modified_time(file_path),
            errors=errors,
        )

    @staticmethod
    def is_path_safe(file_path: str, allowed_dirs: list[str] | None = None) -> bool:
        """
        Check if a path is safe (not trying to escape allowed directories).

        Args:
            file_path: Path to check
            allowed_dirs: List of allowed directory prefixes (None = all allowed)

        Returns:
            bool: True if path is safe, False otherwise
        """
        if not allowed_dirs:
            return True

        path = Path(file_path).resolve()
        return any(str(path).startswith(str(Path(allowed).resolve())) for allowed in allowed_dirs)

    @staticmethod
    def validate_file_extension(file_path: str, allowed_extensions: list[str]) -> bool:
        """
        Validate that file has an allowed extension.

        Args:
            file_path: Path to check
            allowed_extensions: List of allowed extensions (e.g., ['.json', '.yaml'])

        Returns:
            bool: True if extension is allowed, False otherwise
        """
        path = Path(file_path)
        return path.suffix.lower() in [ext.lower() for ext in allowed_extensions]


__all__ = [
    "FileValidationResult",
    "FileValidator",
]
