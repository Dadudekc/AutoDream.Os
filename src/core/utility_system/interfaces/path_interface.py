#!/usr/bin/env python3
"""
Path Interface - V2 Compliance Module
====================================

Interface definition for path operations.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any
from pathlib import Path


class IPathManager(ABC):
    """Interface for path operations."""

    @abstractmethod
    def resolve_path(self, relative_path: Union[str, Path]) -> Path:
        """Resolve relative path to absolute path."""
        pass

    @abstractmethod
    def normalize_path(self, path: Union[str, Path]) -> str:
        """Normalize path."""
        pass

    @abstractmethod
    def get_relative_path(self, file_path: Union[str, Path], base_path: Union[str, Path] = None) -> str:
        """Get relative path."""
        pass

    @abstractmethod
    def get_file_extension(self, file_path: Union[str, Path]) -> str:
        """Get file extension."""
        pass

    @abstractmethod
    def path_exists(self, path: Union[str, Path]) -> bool:
        """Check if path exists."""
        pass

    @abstractmethod
    def is_file(self, path: Union[str, Path]) -> bool:
        """Check if path is a file."""
        pass

    @abstractmethod
    def is_directory(self, path: Union[str, Path]) -> bool:
        """Check if path is a directory."""
        pass

    @abstractmethod
    def create_directory(self, dir_path: Union[str, Path]) -> bool:
        """Create directory."""
        pass

    @abstractmethod
    def get_directory_contents(self, dir_path: Union[str, Path], recursive: bool = False) -> List[Path]:
        """Get directory contents."""
        pass

    @abstractmethod
    def batch_operations(self, operations: List[Dict[str, Any]]) -> List[Any]:
        """Execute batch path operations."""
        pass
