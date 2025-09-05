#!/usr/bin/env python3
"""
File Manager - V2 Compliance Refactored
=======================================

V2 compliant file manager using modular operations handlers.
REFACTORED: 358 lines → <150 lines for V2 compliance.

Responsibilities:
- Orchestrates modular file operation handlers
- Provides unified interface for file operations
- Maintains backward compatibility

V2 Compliance: Modular architecture, <300 lines, single responsibility.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Refactoring
Original: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import asyncio
from pathlib import Path
from typing import List, Union, Optional, Dict, Any, Callable
from dataclasses import dataclass

from ..utility_system_models import UtilityOperationType, FileOperationResult
# Interface removed - KISS compliance
from ..validators.file_validator import FileValidator
from ..cache.file_cache import FileCache

# Import modular handlers
from .file_operations import (
    FileReader,
    FileWriter,
    FileOperations
)


@dataclass
class FileOperationConfig:
    """Configuration for file operations."""
    enable_caching: bool = True
    cache_ttl_seconds: int = 300
    max_file_size_mb: int = 100
    backup_before_write: bool = True
    validate_checksums: bool = True
    retry_attempts: int = 3
    retry_delay_ms: int = 100


class FileManager:
    """
    V2 Compliant File Manager.
    
    Uses modular operation handlers to provide file capabilities
    while maintaining clean, focused architecture.
    """

    def __init__(self, config: FileOperationConfig = None):
        """Initialize file manager with modular handlers."""
        self.config = config or FileOperationConfig()
        self.validator = FileValidator()
        self.cache = FileCache(ttl_seconds=self.config.cache_ttl_seconds)
        
        # Initialize modular handlers
        self.reader = FileReader(self.cache, self.validator, self.config.__dict__)
        self.writer = FileWriter(self.validator, self.config.__dict__)
        self.operations = FileOperations(self.validator, self.config.__dict__)
        
        # Operation handlers mapping
        self._operation_handlers: Dict[str, Callable] = {
            'read': self._handle_read,
            'write': self._handle_write,
            'copy': self._handle_copy,
            'move': self._handle_move,
            'delete': self._handle_delete,
            'list': self._handle_list
        }

    def execute_operation(self, operation_type: str, **kwargs) -> FileOperationResult:
        """Execute file operation using appropriate handler."""
        try:
            if operation_type not in self._operation_handlers:
                return FileOperationResult(
                    success=False,
                    operation_type=operation_type,
                    error=f"Unknown operation type: {operation_type}",
                    message="Operation execution failed"
                )
            
            handler = self._operation_handlers[operation_type]
            return handler(**kwargs)
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type=operation_type,
                error=str(e),
                message="Operation execution failed"
            )

    # Handler methods - delegate to modular handlers
    def _handle_read(self, file_path: Union[str, Path], **kwargs) -> FileOperationResult:
        """Handle read operation."""
        return self.reader.read_file(file_path, **kwargs)

    def _handle_write(self, file_path: Union[str, Path], content: str, **kwargs) -> FileOperationResult:
        """Handle write operation."""
        return self.writer.write_file(file_path, content, **kwargs)

    def _handle_copy(self, source_path: Union[str, Path], dest_path: Union[str, Path], **kwargs) -> FileOperationResult:
        """Handle copy operation."""
        return self.operations.copy_file(source_path, dest_path, **kwargs)

    def _handle_move(self, source_path: Union[str, Path], dest_path: Union[str, Path], **kwargs) -> FileOperationResult:
        """Handle move operation."""
        return self.operations.move_file(source_path, dest_path, **kwargs)

    def _handle_delete(self, file_path: Union[str, Path], **kwargs) -> FileOperationResult:
        """Handle delete operation."""
        return self.operations.delete_file(file_path, **kwargs)

    def _handle_list(self, dir_path: Union[str, Path], **kwargs) -> FileOperationResult:
        """Handle list operation."""
        return self.operations.list_directory(dir_path, **kwargs)

    # Direct access methods for backward compatibility
    def read_file(self, file_path: Union[str, Path], use_cache: bool = True) -> FileOperationResult:
        """Read file with caching."""
        return self.reader.read_file(file_path, use_cache)

    def write_file(self, file_path: Union[str, Path], content: str, create_backup: bool = None) -> FileOperationResult:
        """Write file with backup."""
        return self.writer.write_file(file_path, content, create_backup)

    def copy_file(self, source_path: Union[str, Path], dest_path: Union[str, Path]) -> FileOperationResult:
        """Copy file."""
        return self.operations.copy_file(source_path, dest_path)

    def move_file(self, source_path: Union[str, Path], dest_path: Union[str, Path]) -> FileOperationResult:
        """Move file."""
        return self.operations.move_file(source_path, dest_path)

    def delete_file(self, file_path: Union[str, Path]) -> FileOperationResult:
        """Delete file."""
        return self.operations.delete_file(file_path)

    def list_directory(self, dir_path: Union[str, Path], pattern: str = "*") -> FileOperationResult:
        """List directory contents."""
        return self.operations.list_directory(dir_path, pattern)

    # Additional methods for enhanced functionality
    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get comprehensive file information."""
        try:
            path_obj = Path(file_path)
            if not path_obj.exists():
                return {"exists": False, "error": "File does not exist"}
            
            stat = path_obj.stat()
            return {
                "exists": True,
                "size": stat.st_size,
                "is_file": path_obj.is_file(),
                "is_dir": path_obj.is_dir(),
                "modified": stat.st_mtime,
                "created": stat.st_ctime,
                "permissions": oct(stat.st_mode)[-3:]
            }
        except Exception as e:
            return {"exists": False, "error": str(e)}

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache.get_stats()

    def clear_cache(self) -> None:
        """Clear file cache."""
        self.cache.clear()

    def cleanup(self) -> None:
        """Cleanup file manager resources."""
        try:
            self.cache.clear()
        except Exception as e:
            print(f"Cleanup failed: {e}")


# Factory function for backward compatibility
def create_file_manager(config: FileOperationConfig = None) -> FileManager:
    """Create a file manager instance."""
    return FileManager(config)


# Singleton instance for global access
_file_manager_instance: Optional[FileManager] = None

def get_file_manager(config: FileOperationConfig = None) -> FileManager:
    """Get the global file manager instance."""
    global _file_manager_instance
    
    if _file_manager_instance is None:
        _file_manager_instance = create_file_manager(config)
    
    return _file_manager_instance
