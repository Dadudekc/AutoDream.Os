#!/usr/bin/env python3
"""
Path Manager - V2 Compliance Module
==================================

Specialized manager for path operations with enhanced validation,
normalization, and cross-platform compatibility.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import os
import time
import asyncio
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Callable
from dataclasses import dataclass

from ..utility_system_models import UtilityOperationType, PathOperationResult
# Interface removed - KISS compliance
from ..validators.path_validator import PathValidator


@dataclass
class PathOperationConfig:
    """Configuration for path operations."""
    enable_validation: bool = True
    enable_normalization: bool = True
    cross_platform: bool = True
    max_path_length: int = 260  # Windows limit
    allow_relative_paths: bool = True
    project_root: Optional[Path] = None


class PathManager:
    """Enhanced path manager with validation and cross-platform support."""

    def __init__(self, config: PathOperationConfig = None):
        """Initialize path manager."""
        self.config = config or PathOperationConfig()
        self.validator = PathValidator()
        self._project_root = self.config.project_root or self._find_project_root()
        self._operation_handlers: Dict[str, Callable] = {
            'resolve': self._handle_resolve,
            'normalize': self._handle_normalize,
            'relative': self._handle_relative,
            'extension': self._handle_extension,
            'exists': self._handle_exists,
            'create': self._handle_create
        }

    def resolve_path(self, relative_path: Union[str, Path]) -> Path:
        """Resolve relative path to absolute path with validation."""
        start_time = time.time()
        
        try:
            if isinstance(relative_path, str):
                relative_path = Path(relative_path)
            
            # Validate path
            if not self.validator.validate_path_format(relative_path):
                raise ValueError(f"Invalid path format: {relative_path}")
            
            # Resolve path
            if relative_path.is_absolute():
                resolved_path = relative_path
            else:
                resolved_path = self._project_root / relative_path
            
            # Validate resolved path
            if not self.validator.validate_path_length(resolved_path, self.config.max_path_length):
                raise ValueError(f"Path too long: {resolved_path}")
            
            execution_time = (time.time() - start_time) * 1000
            return resolved_path
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise PathOperationError(f"Failed to resolve path: {str(e)}", execution_time)

    def normalize_path(self, path: Union[str, Path]) -> str:
        """Normalize path with cross-platform compatibility."""
        start_time = time.time()
        
        try:
            if isinstance(path, str):
                path = Path(path)
            
            # Validate path
            if not self.validator.validate_path_format(path):
                raise ValueError(f"Invalid path format: {path}")
            
            # Normalize path
            if self.config.cross_platform:
                normalized = self._cross_platform_normalize(path)
            else:
                normalized = str(path.resolve())
            
            # Validate normalized path
            if not self.validator.validate_path_length(Path(normalized), self.config.max_path_length):
                raise ValueError(f"Normalized path too long: {normalized}")
            
            execution_time = (time.time() - start_time) * 1000
            return normalized
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise PathOperationError(f"Failed to normalize path: {str(e)}", execution_time)

    def get_relative_path(self, file_path: Union[str, Path], base_path: Union[str, Path] = None) -> str:
        """Get relative path with validation."""
        start_time = time.time()
        
        try:
            file_path = self.resolve_path(file_path)
            
            if base_path is None:
                base_path = self._project_root
            else:
                base_path = self.resolve_path(base_path)
            
            # Validate paths
            if not self.validator.validate_path_exists(file_path):
                raise FileNotFoundError(f"File path does not exist: {file_path}")
            
            if not self.validator.validate_path_exists(base_path):
                raise FileNotFoundError(f"Base path does not exist: {base_path}")
            
            # Get relative path
            try:
                relative = file_path.relative_to(base_path)
                execution_time = (time.time() - start_time) * 1000
                return str(relative)
            except ValueError:
                # Paths are not relative, return absolute path
                execution_time = (time.time() - start_time) * 1000
                return str(file_path)
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise PathOperationError(f"Failed to get relative path: {str(e)}", execution_time)

    def get_file_extension(self, file_path: Union[str, Path]) -> str:
        """Get file extension with validation."""
        start_time = time.time()
        
        try:
            path = self.resolve_path(file_path)
            extension = path.suffix.lower()
            
            execution_time = (time.time() - start_time) * 1000
            return extension
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise PathOperationError(f"Failed to get file extension: {str(e)}", execution_time)

    def path_exists(self, path: Union[str, Path]) -> bool:
        """Check if path exists."""
        try:
            resolved_path = self.resolve_path(path)
            return resolved_path.exists()
        except Exception:
            return False

    def is_file(self, path: Union[str, Path]) -> bool:
        """Check if path is a file."""
        try:
            resolved_path = self.resolve_path(path)
            return resolved_path.is_file()
        except Exception:
            return False

    def is_directory(self, path: Union[str, Path]) -> bool:
        """Check if path is a directory."""
        try:
            resolved_path = self.resolve_path(path)
            return resolved_path.is_dir()
        except Exception:
            return False

    def create_directory(self, dir_path: Union[str, Path]) -> bool:
        """Create directory with validation."""
        start_time = time.time()
        
        try:
            path = self.resolve_path(dir_path)
            
            # Validate path
            if not self.validator.validate_directory_path(path):
                raise ValueError(f"Invalid directory path: {path}")
            
            # Create directory
            path.mkdir(parents=True, exist_ok=True)
            
            execution_time = (time.time() - start_time) * 1000
            return True
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise PathOperationError(f"Failed to create directory: {str(e)}", execution_time)

    def get_directory_contents(self, dir_path: Union[str, Path], recursive: bool = False) -> List[Path]:
        """Get directory contents with validation."""
        start_time = time.time()
        
        try:
            path = self.resolve_path(dir_path)
            
            # Validate directory
            if not self.validator.validate_path_exists(path):
                raise FileNotFoundError(f"Directory does not exist: {path}")
            
            if not self.validator.validate_path_is_directory(path):
                raise NotADirectoryError(f"Path is not a directory: {path}")
            
            # Get contents
            if recursive:
                contents = list(path.rglob('*'))
            else:
                contents = list(path.iterdir())
            
            execution_time = (time.time() - start_time) * 1000
            return contents
            
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            raise PathOperationError(f"Failed to get directory contents: {str(e)}", execution_time)

    def get_path_info(self, path: Union[str, Path]) -> Dict[str, Any]:
        """Get comprehensive path information."""
        try:
            resolved_path = self.resolve_path(path)
            
            return {
                "path": str(resolved_path),
                "exists": resolved_path.exists(),
                "is_file": resolved_path.is_file() if resolved_path.exists() else False,
                "is_directory": resolved_path.is_dir() if resolved_path.exists() else False,
                "is_absolute": resolved_path.is_absolute(),
                "parent": str(resolved_path.parent),
                "name": resolved_path.name,
                "stem": resolved_path.stem,
                "suffix": resolved_path.suffix,
                "size": resolved_path.stat().st_size if resolved_path.exists() and resolved_path.is_file() else 0
            }
        except Exception as e:
            return {"error": str(e)}

    def batch_operations(self, operations: List[Dict[str, Any]]) -> List[Any]:
        """Execute batch path operations."""
        results = []
        
        for operation in operations:
            try:
                op_type = operation.get("type")
                handler = self._operation_handlers.get(op_type)
                
                if handler:
                    result = handler(operation)
                    results.append(result)
                else:
                    results.append(None)
                    
            except Exception as e:
                results.append(PathOperationError(f"Operation failed: {str(e)}"))
        
        return results


    def _find_project_root(self) -> Path:
        """Find project root directory."""
        current_path = Path.cwd()
        
        while current_path != current_path.parent:
            if (current_path / "pyproject.toml").exists() or (current_path / "requirements.txt").exists():
                return current_path
            current_path = current_path.parent
        
        return Path.cwd()

    def _cross_platform_normalize(self, path: Path) -> str:
        """Normalize path for cross-platform compatibility."""
        # Convert to string and normalize separators
        normalized = str(path.resolve())
        
        # Ensure consistent separators
        if os.sep != '/':
            normalized = normalized.replace(os.sep, '/')
        
        return normalized

    def _handle_resolve(self, operation: Dict[str, Any]) -> Path:
        """Handle resolve operation."""
        return self.resolve_path(operation["path"])

    def _handle_normalize(self, operation: Dict[str, Any]) -> str:
        """Handle normalize operation."""
        return self.normalize_path(operation["path"])

    def _handle_relative(self, operation: Dict[str, Any]) -> str:
        """Handle relative operation."""
        return self.get_relative_path(
            operation["file_path"], 
            operation.get("base_path")
        )

    def _handle_extension(self, operation: Dict[str, Any]) -> str:
        """Handle extension operation."""
        return self.get_file_extension(operation["file_path"])

    def _handle_exists(self, operation: Dict[str, Any]) -> bool:
        """Handle exists operation."""
        return self.path_exists(operation["path"])

    def _handle_create(self, operation: Dict[str, Any]) -> bool:
        """Handle create operation."""
        return self.create_directory(operation["dir_path"])


class PathOperationError(Exception):
    """Custom exception for path operations."""
    
    def __init__(self, message: str, execution_time_ms: float = 0.0):
        super().__init__(message)
        self.execution_time_ms = execution_time_ms
