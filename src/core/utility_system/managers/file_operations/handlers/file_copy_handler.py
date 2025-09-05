"""
File Copy Handler
=================

Handles file copy operations with validation and verification.
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


class FileCopyHandler:
    """Handles file copy operations with validation and verification."""
    
    def __init__(self, validator: FileValidator, config: Dict[str, Any]):
        """Initialize file copy handler."""
        self.validator = validator
        self.config = config
        
    def copy_file(self, source_path: Union[str, Path], 
                  dest_path: Union[str, Path],
                  preserve_metadata: bool = True) -> FileOperationResult:
        """Copy file from source to destination."""
        try:
            source_obj = Path(source_path)
            dest_obj = Path(dest_path)
            
            # Validate source file
            validation_result = self.validator.validate_file_access(source_obj, 'read')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="copy",
                    file_path=str(source_obj),
                    error=validation_result.error_message,
                    message="Source file validation failed"
                )
            
            # Validate destination
            validation_result = self.validator.validate_file_access(dest_obj, 'write')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="copy",
                    file_path=str(dest_obj),
                    error=validation_result.error_message,
                    message="Destination validation failed"
                )
            
            # Ensure destination directory exists
            dest_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Perform copy
            if preserve_metadata:
                shutil.copy2(source_obj, dest_obj)
            else:
                shutil.copy(source_obj, dest_obj)
            
            # Verify copy if checksums enabled
            verification_result = None
            if self.config.get('validate_checksums', True):
                verification_result = self._verify_copy(source_obj, dest_obj)
            
            # Generate metadata
            metadata = self._generate_copy_metadata(source_obj, dest_obj, preserve_metadata, verification_result)
            
            return FileOperationResult(
                success=True,
                operation_type="copy",
                file_path=str(source_obj),
                data={"destination": str(dest_obj), "preserve_metadata": preserve_metadata},
                metadata=metadata,
                message=f"File copied successfully to {dest_obj}"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="copy",
                file_path=str(source_path),
                error=str(e),
                message="File copy operation failed"
            )
    
    def _verify_copy(self, source_obj: Path, dest_obj: Path) -> Dict[str, Any]:
        """Verify that copy operation was successful."""
        try:
            source_hash = self._calculate_file_hash(source_obj)
            dest_hash = self._calculate_file_hash(dest_obj)
            
            verification_passed = source_hash == dest_hash
            
            return {
                "verification_passed": verification_passed,
                "source_hash": source_hash,
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
    
    def _generate_copy_metadata(self, source_obj: Path, dest_obj: Path, 
                               preserve_metadata: bool, 
                               verification_result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate metadata for copy operation."""
        try:
            source_stat = source_obj.stat()
            dest_stat = dest_obj.stat()
            
            metadata = {
                "source_path": str(source_obj),
                "dest_path": str(dest_obj),
                "source_size": source_stat.st_size,
                "dest_size": dest_stat.st_size,
                "preserve_metadata": preserve_metadata,
                "copy_timestamp": datetime.now().isoformat()
            }
            
            if verification_result:
                metadata["verification"] = verification_result
            
            return metadata
            
        except Exception as e:
            return {
                "error": f"Failed to generate metadata: {e}",
                "copy_timestamp": datetime.now().isoformat()
            }
