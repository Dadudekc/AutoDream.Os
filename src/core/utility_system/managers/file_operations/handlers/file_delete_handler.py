"""
File Delete Handler
===================

Handles file delete operations with validation and backup.
Extracted from file_operations.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import shutil
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime

from ....utility_system_models import FileOperationResult
from ....validators.file_validator import FileValidator


class FileDeleteHandler:
    """Handles file delete operations with validation and backup."""
    
    def __init__(self, validator: FileValidator, config: Dict[str, Any]):
        """Initialize file delete handler."""
        self.validator = validator
        self.config = config
        
    def delete_file(self, file_path: Union[str, Path], 
                   create_backup: bool = None) -> FileOperationResult:
        """Delete file with optional backup."""
        try:
            path_obj = Path(file_path)
            
            # Use config default if backup not specified
            if create_backup is None:
                create_backup = self.config.get('backup_before_write', True)
            
            # Validate file before deletion
            validation_result = self.validator.validate_file_access(path_obj, 'write')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="delete",
                    file_path=str(path_obj),
                    error=validation_result.error_message,
                    message="File validation failed"
                )
            
            # Store metadata before deletion
            original_stat = path_obj.stat()
            original_hash = self._calculate_file_hash(path_obj)
            
            # Create backup if enabled
            backup_path = None
            if create_backup:
                backup_path = self._create_backup(path_obj)
            
            # Delete file
            path_obj.unlink()
            
            # Generate metadata
            metadata = {
                "original_size": original_stat.st_size,
                "original_hash": original_hash,
                "backup_created": backup_path is not None,
                "backup_path": str(backup_path) if backup_path else None,
                "delete_timestamp": datetime.now().isoformat()
            }
            
            return FileOperationResult(
                success=True,
                operation_type="delete",
                file_path=str(path_obj),
                data={"backup_created": backup_path is not None},
                metadata=metadata,
                message="File deleted successfully"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="delete",
                file_path=str(file_path),
                error=str(e),
                message="File delete operation failed"
            )
    
    def _calculate_file_hash(self, path_obj: Path) -> str:
        """Calculate MD5 hash of file."""
        try:
            with path_obj.open('rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return "hash_error"
    
    def _create_backup(self, path_obj: Path) -> Optional[Path]:
        """Create backup of file before deletion."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = path_obj.with_suffix(f".deleted_{timestamp}{path_obj.suffix}")
            
            shutil.copy2(path_obj, backup_path)
            return backup_path
            
        except Exception as e:
            print(f"Warning: Failed to create backup for {path_obj}: {e}")
            return None
