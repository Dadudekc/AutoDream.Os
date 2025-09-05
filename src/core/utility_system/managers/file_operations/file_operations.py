"""
File Operations Handler - V2 Compliance Refactored
==================================================

V2 compliant file operations using specialized handlers.
REFACTORED: 375 lines → <100 lines for V2 compliance.

Responsibilities:
- Orchestrates specialized operation handlers
- Provides unified interface for file operations
- Maintains backward compatibility

V2 Compliance: Modular architecture, <300 lines, single responsibility.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Refactoring
License: MIT
"""

from pathlib import Path
from typing import Dict, Any, Union

from ...utility_system_models import FileOperationResult
from ...validators.file_validator import FileValidator

# Import specialized handlers
from .handlers import (
    FileCopyHandler,
    FileMoveHandler,
    FileDeleteHandler,
    DirectoryListHandler
)


class FileOperations:
    """
    V2 Compliant File Operations Manager.
    
    Uses specialized handlers to provide file operation capabilities
    while maintaining clean, focused architecture.
    """
    
    def __init__(self, validator: FileValidator, config: Dict[str, Any]):
        """Initialize file operations with specialized handlers."""
        self.validator = validator
        self.config = config
        
        # Initialize specialized handlers
        self.copy_handler = FileCopyHandler(validator, config)
        self.move_handler = FileMoveHandler(validator, config)
        self.delete_handler = FileDeleteHandler(validator, config)
        self.list_handler = DirectoryListHandler(config)
        
    def copy_file(self, source_path: Union[str, Path], 
                  dest_path: Union[str, Path],
                  preserve_metadata: bool = True) -> FileOperationResult:
        """Copy file from source to destination."""
        return self.copy_handler.copy_file(source_path, dest_path, preserve_metadata)
    
    def move_file(self, source_path: Union[str, Path], 
                  dest_path: Union[str, Path]) -> FileOperationResult:
        """Move file from source to destination."""
        return self.move_handler.move_file(source_path, dest_path)
    
    def delete_file(self, file_path: Union[str, Path], 
                   create_backup: bool = None) -> FileOperationResult:
        """Delete file with optional backup."""
        return self.delete_handler.delete_file(file_path, create_backup)
    
    def list_directory(self, dir_path: Union[str, Path], 
                      pattern: str = "*",
                      recursive: bool = False) -> FileOperationResult:
        """List directory contents with optional pattern matching."""
        return self.list_handler.list_directory(dir_path, pattern, recursive)
    
    def get_operations_status(self) -> Dict[str, Any]:
        """Get comprehensive operations status."""
        try:
            return {
                "operations_available": ["copy", "move", "delete", "list"],
                "handlers_initialized": {
                    "copy_handler": self.copy_handler is not None,
                    "move_handler": self.move_handler is not None,
                    "delete_handler": self.delete_handler is not None,
                    "list_handler": self.list_handler is not None
                },
                "config": {
                    "validate_checksums": self.config.get('validate_checksums', True),
                    "backup_before_write": self.config.get('backup_before_write', True)
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def cleanup(self) -> None:
        """Cleanup file operations resources."""
        try:
            # Clear any cached data if needed
            pass
        except Exception as e:
            print(f"File operations cleanup failed: {e}")


# Factory function for backward compatibility
def create_file_operations(validator: FileValidator, config: Dict[str, Any]) -> FileOperations:
    """Create a file operations instance."""
    return FileOperations(validator, config)
