#!/usr/bin/env python3
"""
File Interface - V2 Compliance Module
====================================

Interface definition for file operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any
from pathlib import Path


class IFileManager(ABC):
    """Interface for file operations."""

    @abstractmethod
    def read_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> str:
        """Read file content."""
        pass

    @abstractmethod
    def write_file(self, file_path: Union[str, Path], content: str, encoding: str = "utf-8") -> bool:
        """Write content to file."""
        pass

    @abstractmethod
    def copy_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Copy file."""
        pass

    @abstractmethod
    def move_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Move file."""
        pass

    @abstractmethod
    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """Delete file."""
        pass

    @abstractmethod
    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """Get file size in bytes."""
        pass

    @abstractmethod
    def get_file_hash(self, file_path: Union[str, Path], algorithm: str = "md5") -> str:
        """Get file hash."""
        pass

    @abstractmethod
    def backup_file(self, file_path: Union[str, Path]) -> bool:
        """Backup file."""
        pass

    @abstractmethod
    def restore_file(self, backup_path: Union[str, Path], target_path: Union[str, Path]) -> bool:
        """Restore file from backup."""
        pass

    @abstractmethod
    def batch_operations(self, operations: List[Dict[str, Any]]) -> List[bool]:
        """Execute batch file operations."""
        pass
