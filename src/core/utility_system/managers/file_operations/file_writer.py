"""
File Writer Handler
===================

Handles file writing operations with backup and validation.
Extracted from file_manager.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import shutil
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime

from ...utility_system_models import FileOperationResult
from ...validators.file_validator import FileValidator


class FileWriter:
    """Handles file writing operations with backup and validation."""
    
    def __init__(self, validator: FileValidator, config: Dict[str, Any]):
        """Initialize file writer."""
        self.validator = validator
        self.config = config
        
    def write_file(self, file_path: Union[str, Path], content: str,
                   create_backup: bool = None) -> FileOperationResult:
        """Write content to file with optional backup."""
        try:
            path_obj = Path(file_path)
            
            # Use config default if backup not specified
            if create_backup is None:
                create_backup = self.config.get('backup_before_write', True)
            
            # Validate file before writing
            validation_result = self.validator.validate_file_access(path_obj, 'write')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="write",
                    file_path=str(path_obj),
                    error=validation_result.error_message,
                    message="File validation failed"
                )
            
            # Create backup if file exists and backup is enabled
            backup_path = None
            if create_backup and path_obj.exists():
                backup_path = self._create_backup(path_obj)
            
            # Ensure parent directory exists
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            path_obj.write_text(content, encoding='utf-8')
            
            # Verify write if checksums are enabled
            verification_result = None
            if self.config.get('validate_checksums', True):
                verification_result = self._verify_write(path_obj, content)
            
            # Generate metadata
            metadata = self._generate_write_metadata(path_obj, content, backup_path, verification_result)
            
            return FileOperationResult(
                success=True,
                operation_type="write",
                file_path=str(path_obj),
                data={"content_length": len(content), "backup_created": backup_path is not None},
                metadata=metadata,
                message=f"File written successfully ({len(content)} characters)"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="write",
                file_path=str(file_path),
                error=str(e),
                message="File write operation failed"
            )
    
    def write_binary_file(self, file_path: Union[str, Path], content: bytes,
                         create_backup: bool = None) -> FileOperationResult:
        """Write binary content to file."""
        try:
            path_obj = Path(file_path)
            
            # Use config default if backup not specified
            if create_backup is None:
                create_backup = self.config.get('backup_before_write', True)
            
            # Validate file before writing
            validation_result = self.validator.validate_file_access(path_obj, 'write')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="write_binary",
                    file_path=str(path_obj),
                    error=validation_result.error_message,
                    message="File validation failed"
                )
            
            # Create backup if file exists and backup is enabled
            backup_path = None
            if create_backup and path_obj.exists():
                backup_path = self._create_backup(path_obj)
            
            # Ensure parent directory exists
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Write binary content
            path_obj.write_bytes(content)
            
            # Generate metadata
            metadata = {
                "file_size": len(content),
                "content_hash": hashlib.md5(content).hexdigest(),
                "backup_created": backup_path is not None,
                "backup_path": str(backup_path) if backup_path else None,
                "write_timestamp": datetime.now().isoformat(),
                "type": "binary"
            }
            
            return FileOperationResult(
                success=True,
                operation_type="write_binary",
                file_path=str(path_obj),
                data={"content_length": len(content), "backup_created": backup_path is not None},
                metadata=metadata,
                message=f"Binary file written successfully ({len(content)} bytes)"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="write_binary",
                file_path=str(file_path),
                error=str(e),
                message="Binary file write operation failed"
            )
    
    def append_to_file(self, file_path: Union[str, Path], content: str) -> FileOperationResult:
        """Append content to file."""
        try:
            path_obj = Path(file_path)
            
            # Validate file before writing
            validation_result = self.validator.validate_file_access(path_obj, 'write')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="append",
                    file_path=str(path_obj),
                    error=validation_result.error_message,
                    message="File validation failed"
                )
            
            # Get original size for metadata
            original_size = path_obj.stat().st_size if path_obj.exists() else 0
            
            # Ensure parent directory exists
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Append content
            with path_obj.open('a', encoding='utf-8') as f:
                f.write(content)
            
            # Generate metadata
            new_size = path_obj.stat().st_size
            metadata = {
                "original_size": original_size,
                "new_size": new_size,
                "appended_length": len(content),
                "size_increase": new_size - original_size,
                "append_timestamp": datetime.now().isoformat()
            }
            
            return FileOperationResult(
                success=True,
                operation_type="append",
                file_path=str(path_obj),
                data={"appended_length": len(content)},
                metadata=metadata,
                message=f"Content appended successfully ({len(content)} characters)"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="append",
                file_path=str(file_path),
                error=str(e),
                message="File append operation failed"
            )
    
    def _create_backup(self, path_obj: Path) -> Optional[Path]:
        """Create backup of existing file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = path_obj.with_suffix(f".bak_{timestamp}{path_obj.suffix}")
            
            shutil.copy2(path_obj, backup_path)
            return backup_path
            
        except Exception as e:
            # Log error but don't fail the write operation
            print(f"Warning: Failed to create backup for {path_obj}: {e}")
            return None
    
    def _verify_write(self, path_obj: Path, original_content: str) -> Dict[str, Any]:
        """Verify that file was written correctly."""
        try:
            # Read back the content
            written_content = path_obj.read_text(encoding='utf-8')
            
            # Calculate hashes
            original_hash = hashlib.md5(original_content.encode('utf-8')).hexdigest()
            written_hash = hashlib.md5(written_content.encode('utf-8')).hexdigest()
            
            # Compare
            verification_passed = original_hash == written_hash
            
            return {
                "verification_passed": verification_passed,
                "original_hash": original_hash,
                "written_hash": written_hash,
                "original_length": len(original_content),
                "written_length": len(written_content)
            }
            
        except Exception as e:
            return {
                "verification_passed": False,
                "error": str(e)
            }
    
    def _generate_write_metadata(self, path_obj: Path, content: str, 
                                backup_path: Optional[Path], 
                                verification_result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate metadata for write operation."""
        try:
            stat = path_obj.stat()
            
            metadata = {
                "file_size": stat.st_size,
                "content_length": len(content),
                "content_hash": hashlib.md5(content.encode('utf-8')).hexdigest(),
                "backup_created": backup_path is not None,
                "backup_path": str(backup_path) if backup_path else None,
                "write_timestamp": datetime.now().isoformat(),
                "encoding": "utf-8"
            }
            
            if verification_result:
                metadata["verification"] = verification_result
            
            return metadata
            
        except Exception as e:
            return {
                "error": f"Failed to generate metadata: {e}",
                "write_timestamp": datetime.now().isoformat()
            }
