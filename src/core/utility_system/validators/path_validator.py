#!/usr/bin/env python3
"""
Path Validator - V2 Compliance Module
====================================

Validation utilities for path operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import os
from pathlib import Path
from typing import Union


class PathValidator:
    """Validator for path operations."""

    def validate_path_format(self, path: Union[str, Path]) -> bool:
        """Validate path format."""
        try:
            if isinstance(path, str):
                # Check for invalid characters
                invalid_chars = '<>:"|?*'
                if any(char in path for char in invalid_chars):
                    return False
                
                # Check for reserved names on Windows
                reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
                if os.name == 'nt':  # Windows
                    name = Path(path).stem.upper()
                    if name in reserved_names:
                        return False
            
            return True
        except Exception:
            return False

    def validate_path_length(self, path: Union[str, Path], max_length: int) -> bool:
        """Validate path length."""
        try:
            path_str = str(path)
            return len(path_str) <= max_length
        except Exception:
            return False

    def validate_path_exists(self, path: Union[str, Path]) -> bool:
        """Validate path exists."""
        try:
            return Path(path).exists()
        except Exception:
            return False

    def validate_path_is_directory(self, path: Union[str, Path]) -> bool:
        """Validate path is a directory."""
        try:
            path_obj = Path(path)
            return path_obj.exists() and path_obj.is_dir()
        except Exception:
            return False

    def validate_path_is_file(self, path: Union[str, Path]) -> bool:
        """Validate path is a file."""
        try:
            path_obj = Path(path)
            return path_obj.exists() and path_obj.is_file()
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

    def validate_absolute_path(self, path: Union[str, Path]) -> bool:
        """Validate path is absolute."""
        try:
            return Path(path).is_absolute()
        except Exception:
            return False

    def validate_relative_path(self, path: Union[str, Path]) -> bool:
        """Validate path is relative."""
        try:
            return not Path(path).is_absolute()
        except Exception:
            return False
