#!/usr/bin/env python3
"""
File Metadata Operations Module - V2 Compliant
=============================================

File metadata functionality extracted from consolidated_file_operations.py
for V2 compliance (≤400 lines).

Provides:
- File metadata operations and analysis
- File information extraction
- Directory statistics and analysis
- File hash and MIME type detection

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import hashlib
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """Comprehensive file information."""

    path: Path
    size: int
    modified_time: datetime
    created_time: datetime
    is_file: bool
    is_directory: bool
    permissions: str
    hash_sha256: str | None = None
    mime_type: str | None = None
    encoding: str | None = None


@dataclass
class DirectoryInfo:
    """Directory information with statistics."""

    path: Path
    total_files: int
    total_dirs: int
    total_size: int
    file_types: dict[str, int] = field(default_factory=dict)
    last_modified: datetime | None = None


class FileMetadataOperations:
    """Handles file metadata operations and analysis."""

    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes

    def get_file_info(self, file_path: Path) -> FileInfo:
        """Get comprehensive file information."""
        try:
            stat = file_path.stat()
            
            # Get basic file information
            file_info = FileInfo(
                path=file_path,
                size=stat.st_size,
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                created_time=datetime.fromtimestamp(stat.st_ctime),
                is_file=file_path.is_file(),
                is_directory=file_path.is_dir(),
                permissions=oct(stat.st_mode)[-3:]
            )
            
            # Add hash if it's a file
            if file_info.is_file:
                file_info.hash_sha256 = self._calculate_file_hash(file_path)
                file_info.mime_type = self._detect_mime_type(file_path)
                file_info.encoding = self._detect_encoding(file_path)
            
            return file_info
            
        except Exception as e:
            logger.error(f"Failed to get file info for {file_path}: {e}")
            raise

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return ""

    def _detect_mime_type(self, file_path: Path) -> str:
        """Detect MIME type of a file."""
        try:
            import mimetypes
            mime_type, _ = mimetypes.guess_type(str(file_path))
            return mime_type or "application/octet-stream"
        except Exception as e:
            logger.error(f"Failed to detect MIME type for {file_path}: {e}")
            return "application/octet-stream"

    def _detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding."""
        try:
            import chardet
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8')
        except Exception as e:
            logger.error(f"Failed to detect encoding for {file_path}: {e}")
            return 'utf-8'

    def get_directory_info(self, directory_path: Path) -> DirectoryInfo:
        """Get comprehensive directory information."""
        try:
            total_files = 0
            total_dirs = 0
            total_size = 0
            file_types = {}
            last_modified = None
            
            for item in directory_path.rglob('*'):
                try:
                    stat = item.stat()
                    total_size += stat.st_size
                    
                    if item.is_file():
                        total_files += 1
                        # Count file types
                        ext = item.suffix.lower()
                        file_types[ext] = file_types.get(ext, 0) + 1
                    elif item.is_dir():
                        total_dirs += 1
                    
                    # Track last modified
                    item_modified = datetime.fromtimestamp(stat.st_mtime)
                    if last_modified is None or item_modified > last_modified:
                        last_modified = item_modified
                        
                except (OSError, PermissionError):
                    # Skip files we can't access
                    continue
            
            return DirectoryInfo(
                path=directory_path,
                total_files=total_files,
                total_dirs=total_dirs,
                total_size=total_size,
                file_types=file_types,
                last_modified=last_modified
            )
            
        except Exception as e:
            logger.error(f"Failed to get directory info for {directory_path}: {e}")
            raise

    def compare_files(self, file1: Path, file2: Path) -> dict[str, Any]:
        """Compare two files and return differences."""
        try:
            info1 = self.get_file_info(file1)
            info2 = self.get_file_info(file2)
            
            comparison = {
                "files_identical": info1.hash_sha256 == info2.hash_sha256,
                "size_difference": info1.size - info2.size,
                "size_ratio": info1.size / info2.size if info2.size > 0 else float('inf'),
                "modified_time_difference": (info1.modified_time - info2.modified_time).total_seconds(),
                "permissions_different": info1.permissions != info2.permissions,
                "mime_types_different": info1.mime_type != info2.mime_type
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Failed to compare files {file1} and {file2}: {e}")
            raise

    def find_duplicate_files(self, directory: Path) -> dict[str, list[Path]]:
        """Find duplicate files in a directory based on hash."""
        try:
            hash_to_files = {}
            
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    try:
                        file_hash = self._calculate_file_hash(file_path)
                        if file_hash not in hash_to_files:
                            hash_to_files[file_hash] = []
                        hash_to_files[file_hash].append(file_path)
                    except Exception as e:
                        logger.warning(f"Failed to hash file {file_path}: {e}")
                        continue
            
            # Return only duplicates (files with same hash)
            duplicates = {hash_val: files for hash_val, files in hash_to_files.items() if len(files) > 1}
            
            return duplicates
            
        except Exception as e:
            logger.error(f"Failed to find duplicate files in {directory}: {e}")
            raise

    def get_file_statistics(self, directory: Path) -> dict[str, Any]:
        """Get comprehensive file statistics for a directory."""
        try:
            dir_info = self.get_directory_info(directory)
            
            # Calculate additional statistics
            stats = {
                "total_files": dir_info.total_files,
                "total_directories": dir_info.total_dirs,
                "total_size_bytes": dir_info.total_size,
                "total_size_mb": round(dir_info.total_size / (1024 * 1024), 2),
                "total_size_gb": round(dir_info.total_size / (1024 * 1024 * 1024), 2),
                "file_types": dir_info.file_types,
                "most_common_extension": max(dir_info.file_types.items(), key=lambda x: x[1])[0] if dir_info.file_types else None,
                "last_modified": dir_info.last_modified.isoformat() if dir_info.last_modified else None,
                "average_file_size": round(dir_info.total_size / dir_info.total_files, 2) if dir_info.total_files > 0 else 0
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get file statistics for {directory}: {e}")
            raise

    def cache_file_info(self, file_path: Path, file_info: FileInfo):
        """Cache file information with TTL."""
        cache_key = str(file_path)
        self.cache[cache_key] = {
            "info": file_info,
            "timestamp": datetime.now()
        }

    def get_cached_file_info(self, file_path: Path) -> FileInfo | None:
        """Get cached file information if still valid."""
        cache_key = str(file_path)
        
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            age = (datetime.now() - cached_data["timestamp"]).total_seconds()
            
            if age < self.cache_ttl:
                return cached_data["info"]
            else:
                # Remove expired cache entry
                del self.cache[cache_key]
        
        return None

    def clear_cache(self):
        """Clear the file info cache."""
        self.cache.clear()
        logger.info("File metadata cache cleared")


if __name__ == "__main__":
    # Example usage
    metadata_ops = FileMetadataOperations()
    
    # Test with current directory
    current_dir = Path(".")
    
    # Get directory info
    dir_info = metadata_ops.get_directory_info(current_dir)
    print(f"Directory: {dir_info.path}")
    print(f"Files: {dir_info.total_files}, Directories: {dir_info.total_dirs}")
    print(f"Total size: {dir_info.total_size} bytes")
    print(f"File types: {dir_info.file_types}")
    
    # Get file statistics
    stats = metadata_ops.get_file_statistics(current_dir)
    print(f"\nFile Statistics:")
    print(f"Total size: {stats['total_size_mb']} MB")
    print(f"Average file size: {stats['average_file_size']} bytes")
    print(f"Most common extension: {stats['most_common_extension']}")
    
    # Find duplicates
    duplicates = metadata_ops.find_duplicate_files(current_dir)
    if duplicates:
        print(f"\nFound {len(duplicates)} sets of duplicate files")
    else:
        print("\nNo duplicate files found")
