#!/usr/bin/env python3
# Consolidated File Operations System - V2 Compliant
from __future__ import annotations
import hashlib, json, logging, os, shutil, time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import yaml

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


@dataclass
class BackupResult:
    """Result of backup operation."""

    success: bool
    backup_path: Path | None
    files_backed_up: int
    total_size: int
    duration_seconds: float
    errors: list[str] = field(default_factory=list)


@dataclass
class ScanResult:
    """Result of file scanning operation."""

    directory: Path
    files_found: list[Path]
    total_size: int
    scan_duration: float
    filters_applied: dict[str, Any] = field(default_factory=dict)


class FileOperation(ABC):
    """Abstract base class for file operations."""

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute the file operation."""
        pass


class FileMetadataOperations:
    """Handles file metadata operations with caching and performance optimizations."""

    _cache: dict[str, FileInfo] = {}
    _cache_timeout = 30  # seconds

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the metadata cache."""
        cls._cache.clear()

    @classmethod
    def get_file_info(cls, file_path: str | Path, use_cache: bool = True) -> FileInfo | None:
        """Get comprehensive file information with optional caching."""
        path = Path(file_path)

        # Check cache first
        cache_key = str(path.absolute())
        if use_cache and cache_key in cls._cache:
            cached_info = cls._cache[cache_key]
            # Check if cache is still valid
            if time.time() - cached_info.modified_time.timestamp() < cls._cache_timeout:
                return cached_info

        try:
            stat = path.stat()

            # Determine encoding for text files
            encoding = None
            if path.is_file():
                try:
                    with open(path, "rb") as f:
                        sample = f.read(1024)
                    encoding = "utf-8" if sample else None
                except Exception:
                    pass

            file_info = FileInfo(
                path=path,
                size=stat.st_size,
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                created_time=datetime.fromtimestamp(stat.st_ctime),
                is_file=path.is_file(),
                is_directory=path.is_directory(),
                permissions=oct(stat.st_mode)[-3:],
                encoding=encoding,
            )

            # Cache the result
            if use_cache:
                cls._cache[cache_key] = file_info

            return file_info

        except Exception as e:
            logger.warning(f"Failed to get file info for {path}: {e}")
            return None

    @staticmethod
    def file_exists(file_path: str | Path) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()

    @staticmethod
    def is_readable(file_path: str | Path) -> bool:
        """Check if a file is readable."""
        try:
            with open(file_path, encoding="utf-8") as f:
                f.read(1)
            return True
        except Exception:
            return False

    @staticmethod
    def is_writable(file_path: str | Path) -> bool:
        """Check if a file is writable."""
        try:
            with open(file_path, "a", encoding="utf-8"):
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def calculate_hash(file_path: str | Path, algorithm: str = "sha256") -> str | None:
        """Calculate file hash."""
        try:
            hash_func = getattr(hashlib, algorithm)()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return None


class DirectoryOperations:
    """Directory management operations."""

    @staticmethod
    def ensure_directory(path: str | Path) -> bool:
        """Ensure directory exists, create if not."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False

    @staticmethod
    def get_directory_info(directory: str | Path, recursive: bool = True) -> DirectoryInfo | None:
        """Get comprehensive directory information."""
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            return None

        total_files = 0
        total_dirs = 0
        total_size = 0
        file_types = {}
        last_modified = None

        try:
            if recursive:
                for item in dir_path.rglob("*"):
                    if item.is_file():
                        total_files += 1
                        total_size += item.stat().st_size
                        ext = item.suffix.lower() or "no_extension"
                        file_types[ext] = file_types.get(ext, 0) + 1

                        mtime = datetime.fromtimestamp(item.stat().st_mtime)
                        if last_modified is None or mtime > last_modified:
                            last_modified = mtime
                    elif item.is_dir():
                        total_dirs += 1
            else:
                for item in dir_path.iterdir():
                    if item.is_file():
                        total_files += 1
                        total_size += item.stat().st_size
                        ext = item.suffix.lower() or "no_extension"
                        file_types[ext] = file_types.get(ext, 0) + 1
                    elif item.is_dir():
                        total_dirs += 1

        except Exception as e:
            logger.error(f"Failed to analyze directory {directory}: {e}")
            return None

        return DirectoryInfo(
            path=dir_path,
            total_files=total_files,
            total_dirs=total_dirs,
            total_size=total_size,
            file_types=file_types,
            last_modified=last_modified,
        )

    @staticmethod
    def find_files(directory: str | Path, pattern: str = "*", recursive: bool = True) -> list[Path]:
        """Find files matching a pattern."""
        dir_path = Path(directory)
        if recursive:
            return list(dir_path.rglob(pattern))
        else:
            return list(dir_path.glob(pattern))

    @staticmethod
    def cleanup_directory(
        directory: str | Path, pattern: str = "*", older_than_days: int | None = None
    ) -> int:
        """Clean up files in directory based on criteria."""
        dir_path = Path(directory)
        cleaned_count = 0

        try:
            cutoff_time = None
            if older_than_days:
                cutoff_time = datetime.now().timestamp() - (older_than_days * 24 * 60 * 60)

            for file_path in dir_path.rglob(pattern):
                if file_path.is_file():
                    should_remove = True

                    if cutoff_time:
                        file_mtime = file_path.stat().st_mtime
                        if file_mtime >= cutoff_time:
                            should_remove = False

                    if should_remove:
                        try:
                            file_path.unlink()
                            cleaned_count += 1
                        except Exception as e:
                            logger.warning(f"Failed to remove {file_path}: {e}")

        except Exception as e:
            logger.error(f"Failed to cleanup directory {directory}: {e}")

        return cleaned_count


class SerializationOperations:
    """JSON/YAML serialization and deserialization operations."""

    @staticmethod
    def read_json(file_path: str | Path) -> dict[str, Any] | None:
        """Read JSON file and return data."""
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"JSON file not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {file_path}: {e}")
            return None

    @staticmethod
    def write_json(
        file_path: str | Path, data: dict[str, Any], indent: int = 2, ensure_dir: bool = True
    ) -> bool:
        """Write data to JSON file."""
        try:
            path = Path(file_path)
            if ensure_dir:
                path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent, default=str)
            return True
        except Exception as e:
            logger.error(f"Failed to write JSON to {file_path}: {e}")
            return False

    @staticmethod
    def read_yaml(file_path: str | Path) -> dict[str, Any] | None:
        """Read YAML file and return data."""
        try:
            with open(file_path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"YAML file not found: {file_path}")
            return None
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML from {file_path}: {e}")
            return None

    @staticmethod
    def write_yaml(file_path: str | Path, data: dict[str, Any], ensure_dir: bool = True) -> bool:
        """Write data to YAML file."""
        try:
            path = Path(file_path)
            if ensure_dir:
                path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            logger.error(f"Failed to write YAML to {file_path}: {e}")
            return False


class BackupOperations:
    """Backup and restore operations with progress tracking."""

    @staticmethod
    def create_backup(
        source_dir: str | Path,
        backup_dir: str | Path,
        include_pattern: str | None = None,
        exclude_patterns: list[str] | None = None,
    ) -> BackupResult:
        """Create a backup of source directory."""
        start_time = time.time()

        source = Path(source_dir)
        backup_root = Path(backup_dir)

        if not source.exists():
            return BackupResult(
                success=False,
                backup_path=None,
                files_backed_up=0,
                total_size=0,
                duration_seconds=time.time() - start_time,
                errors=[f"Source directory {source} does not exist"],
            )

        # Create backup directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_root / f"backup_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)

        files_backed_up = 0
        total_size = 0
        errors = []

        try:
            # Walk through source directory
            for root, dirs, files in os.walk(source):
                root_path = Path(root)
                relative_root = root_path.relative_to(source)
                dest_root = backup_path / relative_root

                # Create destination directory
                dest_root.mkdir(parents=True, exist_ok=True)

                for file in files:
                    src_file = root_path / file

                    # Apply include/exclude filters
                    should_backup = True

                    if include_pattern and not src_file.match(include_pattern):
                        should_backup = False

                    if exclude_patterns:
                        for pattern in exclude_patterns:
                            if src_file.match(pattern):
                                should_backup = False
                                break

                    if should_backup:
                        dest_file = dest_root / file
                        try:
                            shutil.copy2(src_file, dest_file)
                            files_backed_up += 1
                            total_size += src_file.stat().st_size
                        except Exception as e:
                            errors.append(f"Failed to backup {src_file}: {e}")

        except Exception as e:
            errors.append(f"Backup operation failed: {e}")
            return BackupResult(
                success=False,
                backup_path=None,
                files_backed_up=files_backed_up,
                total_size=total_size,
                duration_seconds=time.time() - start_time,
                errors=errors,
            )

        duration = time.time() - start_time
        success = len(errors) == 0

        return BackupResult(
            success=success,
            backup_path=backup_path,
            files_backed_up=files_backed_up,
            total_size=total_size,
            duration_seconds=duration,
            errors=errors,
        )

    @staticmethod
    def restore_backup(
        backup_path: str | Path, restore_dir: str | Path, overwrite: bool = False
    ) -> BackupResult:
        """Restore files from backup."""
        start_time = time.time()

        backup = Path(backup_path)
        restore = Path(restore_dir)

        if not backup.exists():
            return BackupResult(
                success=False,
                backup_path=backup,
                files_backed_up=0,
                total_size=0,
                duration_seconds=time.time() - start_time,
                errors=[f"Backup directory {backup} does not exist"],
            )

        files_restored = 0
        total_size = 0
        errors = []

        try:
            for src_file in backup.rglob("*"):
                if src_file.is_file():
                    relative_path = src_file.relative_to(backup)
                    dest_file = restore / relative_path

                    # Check if destination exists
                    if dest_file.exists() and not overwrite:
                        errors.append(f"File {dest_file} exists, skipping (overwrite=False)")
                        continue

                    # Ensure destination directory exists
                    dest_file.parent.mkdir(parents=True, exist_ok=True)

                    try:
                        shutil.copy2(src_file, dest_file)
                        files_restored += 1
                        total_size += src_file.stat().st_size
                    except Exception as e:
                        errors.append(f"Failed to restore {src_file}: {e}")

        except Exception as e:
            errors.append(f"Restore operation failed: {e}")

        duration = time.time() - start_time
        success = len(errors) == 0

        return BackupResult(
            success=success,
            backup_path=backup,
            files_backed_up=files_restored,
            total_size=total_size,
            duration_seconds=duration,
            errors=errors,
        )


class FileScanner:
    """Advanced file scanning with filtering and performance optimizations."""

    @staticmethod
    def scan_directory(
        directory: str | Path,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        max_depth: int | None = None,
    ) -> ScanResult:
        """Scan directory with advanced filtering."""
        start_time = time.time()
        dir_path = Path(directory)

        if not dir_path.exists():
            return ScanResult(
                directory=dir_path,
                files_found=[],
                total_size=0,
                scan_duration=time.time() - start_time,
            )

        files_found = []
        total_size = 0

        try:
            for root, dirs, files in os.walk(dir_path):
                root_path = Path(root)

                # Check depth limit
                if max_depth is not None:
                    relative_depth = len(root_path.relative_to(dir_path).parts)
                    if relative_depth > max_depth:
                        dirs[:] = []  # Don't recurse deeper
                        continue

                # Apply directory exclusions
                if exclude_patterns:
                    dirs[:] = [
                        d
                        for d in dirs
                        if not any((Path(root) / d).match(pattern) for pattern in exclude_patterns)
                    ]

                for file in files:
                    file_path = root_path / file

                    # Apply include/exclude filters
                    should_include = True

                    if include_patterns:
                        should_include = any(
                            file_path.match(pattern) for pattern in include_patterns
                        )

                    if exclude_patterns:
                        if any(file_path.match(pattern) for pattern in exclude_patterns):
                            should_include = False

                    if should_include:
                        files_found.append(file_path)
                        try:
                            total_size += file_path.stat().st_size
                        except Exception:
                            pass

        except Exception as e:
            logger.error(f"Failed to scan directory {directory}: {e}")

        scan_duration = time.time() - start_time

        return ScanResult(
            directory=dir_path,
            files_found=files_found,
            total_size=total_size,
            scan_duration=scan_duration,
            filters_applied={
                "include_patterns": include_patterns or [],
                "exclude_patterns": exclude_patterns or [],
                "max_depth": max_depth,
            },
        )

    @staticmethod
    def find_duplicates(directory: str | Path, algorithm: str = "sha256") -> dict[str, list[Path]]:
        """Find duplicate files based on content hash."""
        dir_path = Path(directory)
        hash_map: dict[str, list[Path]] = {}

        if not dir_path.exists():
            return hash_map

        # Calculate hashes for all files
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                file_hash = FileMetadataOperations.calculate_hash(file_path, algorithm)
                if file_hash:
                    if file_hash not in hash_map:
                        hash_map[file_hash] = []
                    hash_map[file_hash].append(file_path)

        # Filter to only duplicates (files with same hash appearing more than once)
        duplicates = {hash_val: paths for hash_val, paths in hash_map.items() if len(paths) > 1}
        return duplicates


# Global instances for convenience
file_metadata = FileMetadataOperations()
directory_ops = DirectoryOperations()
serialization_ops = SerializationOperations()
backup_ops = BackupOperations()
file_scanner = FileScanner()


# Convenience functions
def ensure_dir(path: str | Path) -> bool:
    """Ensure directory exists."""
    return directory_ops.ensure_directory(path)


def read_json_file(file_path: str | Path) -> dict[str, Any] | None:
    """Read JSON file."""
    return serialization_ops.read_json(file_path)


def write_json_file(file_path: str | Path, data: dict[str, Any]) -> bool:
    """Write JSON file."""
    return serialization_ops.write_json(file_path, data)


def create_backup(source: str | Path, destination: str | Path) -> BackupResult:
    """Create backup."""
    return backup_ops.create_backup(source, destination)


# Backwards compatibility aliases
FileUtils = SerializationOperations
BackupManager = BackupOperations
