"""
File Move Handler
=================

Handles file move operations with validation and verification.
Extracted from file_operations.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import shutil
import hashlib
from pathlib import Path
from typing import Dict, Any, Union
from datetime import datetime

from ....utility_system_models import FileOperationResult
from ....validators.file_validator import FileValidator


class FileMoveHandler:
    """Handles file move operations with validation and verification."""
    
    def __init__(self, validator: FileValidator, config: Dict[str, Any]):
        """Initialize file move handler."""
        self.validator = validator
        self.config = config
        
    def move_file(self, source_path: Union[str, Path], 
                  dest_path: Union[str, Path]) -> FileOperationResult:
        """Move file from source to destination."""
        try:
            source_obj = Path(source_path)
            dest_obj = Path(dest_path)
            
            # Validate source file
            validation_result = self.validator.validate_file_access(source_obj, 'write')  # Need write to delete
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="move",
                    file_path=str(source_obj),
                    error=validation_result.error_message,
                    message="Source file validation failed"
                )
            
            # Store original metadata before move
            original_stat = source_obj.stat()
            original_hash = self._calculate_file_hash(source_obj)
            
            # Ensure destination directory exists
            dest_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Perform move
            shutil.move(str(source_obj), str(dest_obj))
            
            # Verify move if checksums enabled
            verification_result = None
            if self.config.get('validate_checksums', True):
                verification_result = self._verify_move(dest_obj, original_hash)
            
            # Generate metadata
            metadata = {
                "original_path": str(source_obj),
                "new_path": str(dest_obj),
                "original_size": original_stat.st_size,
                "original_hash": original_hash,
                "move_timestamp": datetime.now().isoformat()
            }
            
            if verification_result:
                metadata["verification"] = verification_result
            
            return FileOperationResult(
                success=True,
                operation_type="move",
                file_path=str(source_obj),
                data={"destination": str(dest_obj)},
                metadata=metadata,
                message=f"File moved successfully to {dest_obj}"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="move",
                file_path=str(source_path),
                error=str(e),
                message="File move operation failed"
            )
    
    def _verify_move(self, dest_obj: Path, original_hash: str) -> Dict[str, Any]:
        """Verify that move operation was successful."""
        try:
            dest_hash = self._calculate_file_hash(dest_obj)
            verification_passed = original_hash == dest_hash
            
            return {
                "verification_passed": verification_passed,
                "original_hash": original_hash,
                "dest_hash": dest_hash
            }
            
        except Exception as e:
            return {
                "verification_passed": False,
                "error": str(e)
            }
    
    def _calculate_file_hash(self, path_obj: Path) -> str:
        """Calculate MD5 hash of file."""
        try:
            with path_obj.open('rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return "hash_error"
