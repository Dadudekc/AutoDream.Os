"""
File Reader Handler
===================

Handles file reading operations with caching and validation.
Extracted from file_manager.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import hashlib
import time
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime

from ...utility_system_models import FileOperationResult
from ...validators.file_validator import FileValidator
from ...cache.file_cache import FileCache


class FileReader:
    """Handles file reading operations with caching and validation."""
    
    def __init__(self, cache: FileCache, validator: FileValidator, config: Dict[str, Any]):
        """Initialize file reader."""
        self.cache = cache
        self.validator = validator
        self.config = config
        
    def read_file(self, file_path: Union[str, Path], 
                  use_cache: bool = True) -> FileOperationResult:
        """Read file with caching and validation."""
        try:
            path_obj = Path(file_path)
            cache_key = f"read_{path_obj.as_posix()}"
            
            # Check cache first if enabled
            if use_cache and self.config.get('enable_caching', True):
                cached_result = self.cache.get(cache_key)
                if cached_result:
                    return FileOperationResult(
                        success=True,
                        operation_type="read",
                        file_path=str(path_obj),
                        data=cached_result,
                        metadata={"source": "cache", "timestamp": datetime.now()},
                        message="File read from cache"
                    )
            
            # Validate file before reading
            validation_result = self.validator.validate_file_access(path_obj, 'read')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="read",
                    file_path=str(path_obj),
                    error=validation_result.error_message,
                    message="File validation failed"
                )
            
            # Read file content
            content = self._read_file_content(path_obj)
            
            # Cache the result if enabled
            if use_cache and self.config.get('enable_caching', True):
                self.cache.set(cache_key, content)
            
            # Generate metadata
            metadata = self._generate_read_metadata(path_obj, content)
            
            return FileOperationResult(
                success=True,
                operation_type="read",
                file_path=str(path_obj),
                data=content,
                metadata=metadata,
                message=f"File read successfully ({len(content)} characters)"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="read",
                file_path=str(file_path),
                error=str(e),
                message="File read operation failed"
            )
    
    def _read_file_content(self, path_obj: Path) -> str:
        """Read file content with encoding detection."""
        try:
            # Try UTF-8 first
            return path_obj.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1
                return path_obj.read_text(encoding='latin-1')
            except Exception:
                # Last resort: read as binary and decode with errors='ignore'
                return path_obj.read_text(encoding='utf-8', errors='ignore')
    
    def _generate_read_metadata(self, path_obj: Path, content: str) -> Dict[str, Any]:
        """Generate metadata for read operation."""
        try:
            stat = path_obj.stat()
            
            # Calculate content hash
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            
            return {
                "file_size": stat.st_size,
                "content_length": len(content),
                "content_hash": content_hash,
                "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "read_timestamp": datetime.now().isoformat(),
                "encoding": "utf-8"
            }
            
        except Exception as e:
            return {
                "error": f"Failed to generate metadata: {e}",
                "read_timestamp": datetime.now().isoformat()
            }
    
    def read_binary_file(self, file_path: Union[str, Path]) -> FileOperationResult:
        """Read binary file."""
        try:
            path_obj = Path(file_path)
            
            # Validate file before reading
            validation_result = self.validator.validate_file_access(path_obj, 'read')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="read_binary",
                    file_path=str(path_obj),
                    error=validation_result.error_message,
                    message="File validation failed"
                )
            
            # Read binary content
            content = path_obj.read_bytes()
            
            # Generate metadata
            metadata = {
                "file_size": len(content),
                "content_hash": hashlib.md5(content).hexdigest(),
                "read_timestamp": datetime.now().isoformat(),
                "type": "binary"
            }
            
            return FileOperationResult(
                success=True,
                operation_type="read_binary",
                file_path=str(path_obj),
                data=content,
                metadata=metadata,
                message=f"Binary file read successfully ({len(content)} bytes)"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="read_binary",
                file_path=str(file_path),
                error=str(e),
                message="Binary file read operation failed"
            )
    
    def read_lines(self, file_path: Union[str, Path], 
                   max_lines: Optional[int] = None) -> FileOperationResult:
        """Read file lines with optional limit."""
        try:
            path_obj = Path(file_path)
            
            # Validate file before reading
            validation_result = self.validator.validate_file_access(path_obj, 'read')
            if not validation_result.is_valid:
                return FileOperationResult(
                    success=False,
                    operation_type="read_lines",
                    file_path=str(path_obj),
                    error=validation_result.error_message,
                    message="File validation failed"
                )
            
            # Read lines
            with path_obj.open('r', encoding='utf-8') as f:
                if max_lines:
                    lines = [f.readline().rstrip('\n\r') for _ in range(max_lines)]
                    lines = [line for line in lines if line]  # Remove empty lines from EOF
                else:
                    lines = [line.rstrip('\n\r') for line in f.readlines()]
            
            # Generate metadata
            metadata = {
                "line_count": len(lines),
                "max_lines_requested": max_lines,
                "truncated": max_lines is not None and len(lines) == max_lines,
                "read_timestamp": datetime.now().isoformat()
            }
            
            return FileOperationResult(
                success=True,
                operation_type="read_lines",
                file_path=str(path_obj),
                data=lines,
                metadata=metadata,
                message=f"Read {len(lines)} lines from file"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="read_lines",
                file_path=str(file_path),
                error=str(e),
                message="File lines read operation failed"
            )
