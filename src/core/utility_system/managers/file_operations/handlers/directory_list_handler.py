"""
Directory List Handler
======================

Handles directory listing operations with pattern matching.
Extracted from file_operations.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from pathlib import Path
from typing import Dict, Any, Union, List
from datetime import datetime

from ....utility_system_models import FileOperationResult


class DirectoryListHandler:
    """Handles directory listing operations with pattern matching."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize directory list handler."""
        self.config = config
        
    def list_directory(self, dir_path: Union[str, Path], 
                      pattern: str = "*",
                      recursive: bool = False) -> FileOperationResult:
        """List directory contents with optional pattern matching."""
        try:
            path_obj = Path(dir_path)
            
            # Validate directory
            if not path_obj.exists():
                return FileOperationResult(
                    success=False,
                    operation_type="list",
                    file_path=str(path_obj),
                    error="Directory does not exist",
                    message="Directory listing failed"
                )
            
            if not path_obj.is_dir():
                return FileOperationResult(
                    success=False,
                    operation_type="list",
                    file_path=str(path_obj),
                    error="Path is not a directory",
                    message="Directory listing failed"
                )
            
            # Get file list
            if recursive:
                files = list(path_obj.rglob(pattern))
            else:
                files = list(path_obj.glob(pattern))
            
            # Generate file info
            file_info = []
            for file_path in files:
                try:
                    stat = file_path.stat()
                    file_info.append({
                        "path": str(file_path),
                        "name": file_path.name,
                        "size": stat.st_size,
                        "is_dir": file_path.is_dir(),
                        "is_file": file_path.is_file(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                except Exception:
                    # Skip files that can't be accessed
                    continue
            
            # Generate metadata
            metadata = {
                "directory": str(path_obj),
                "pattern": pattern,
                "recursive": recursive,
                "total_items": len(file_info),
                "files": len([f for f in file_info if f["is_file"]]),
                "directories": len([f for f in file_info if f["is_dir"]]),
                "list_timestamp": datetime.now().isoformat()
            }
            
            return FileOperationResult(
                success=True,
                operation_type="list",
                file_path=str(path_obj),
                data=file_info,
                metadata=metadata,
                message=f"Directory listing completed ({len(file_info)} items)"
            )
            
        except Exception as e:
            return FileOperationResult(
                success=False,
                operation_type="list",
                file_path=str(dir_path),
                error=str(e),
                message="Directory listing operation failed"
            )
