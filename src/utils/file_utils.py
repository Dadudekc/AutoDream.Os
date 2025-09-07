#!/usr/bin/env python3
"""Centralized file utility helpers."""
import json
import yaml
import hashlib
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class FileUtils:
    """Unified file utility operations."""

    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists, create if not."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False

    # ------------------------------------------------------------------
    # JSON/YAML operations
    # ------------------------------------------------------------------
    @staticmethod
    def read_json(file_path: str) -> Optional[Dict[str, Any]]:
        """Read JSON file and return data."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"JSON file not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {file_path}: {e}")
            return None

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]) -> bool:
        """Write data to JSON file."""
        try:
            FileUtils.ensure_directory(os.path.dirname(file_path))
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to write JSON {file_path}: {e}")
            return False

    @staticmethod
    def read_yaml(file_path: str) -> Optional[Dict[str, Any]]:
        """Read YAML file and return data."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to read YAML {file_path}: {e}")
            return None

    @staticmethod
    def write_yaml(file_path: str, data: Dict[str, Any]) -> bool:
        """Write data to YAML file."""
        try:
            FileUtils.ensure_directory(os.path.dirname(file_path))
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            logger.error(f"Failed to write YAML {file_path}: {e}")
            return False

    # ------------------------------------------------------------------
    # File metadata operations
    # ------------------------------------------------------------------
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()

    @staticmethod
    def is_file_readable(file_path: str) -> bool:
        """Check if a file is readable."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                f.read(1)
            return True
        except Exception:
            return False

    @staticmethod
    def is_file_writable(file_path: str) -> bool:
        """Check if a file is writable."""
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_size(file_path: str) -> Optional[int]:
        """Get file size in bytes."""
        try:
            return Path(file_path).stat().st_size
        except Exception as e:
            logger.error(f"Failed to get file size for {file_path}: {e}")
            return None

    @staticmethod
    def get_file_modified_time(file_path: str) -> Optional[datetime]:
        """Get file last modified time."""
        try:
            timestamp = Path(file_path).stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except Exception:
            return None

    @staticmethod
    def get_file_hash(file_path: str) -> Optional[str]:
        """Get SHA256 hash of file."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Failed to get hash for {file_path}: {e}")
            return None

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension."""
        return Path(file_path).suffix.lower()

    @staticmethod
    def is_json_file(file_path: str) -> bool:
        """Check if file has JSON extension."""
        return FileUtils.get_file_extension(file_path) == ".json"

    # ------------------------------------------------------------------
    # Directory and list operations
    # ------------------------------------------------------------------
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """List files in directory matching pattern."""
        try:
            path = Path(directory)
            if not path.exists() or not path.is_dir():
                return []
            return [str(f) for f in path.glob(pattern) if f.is_file()]
        except Exception as e:
            logger.error(f"Failed to list files in {directory}: {e}")
            return []

    @staticmethod
    def get_directory_size(directory_path: str) -> int:
        """Get total size of directory in bytes."""
        try:
            total = 0
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                return 0
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total += file_path.stat().st_size
            return total
        except Exception:
            return 0

    # ------------------------------------------------------------------
    # Backup and copy operations
    # ------------------------------------------------------------------
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file from source to destination."""
        try:
            FileUtils.ensure_directory(os.path.dirname(destination))
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            logger.error(f"Failed to copy file from {source} to {destination}: {e}")
            return False

    @staticmethod
    def create_backup(file_path: str, backup_suffix: str = ".backup") -> Optional[str]:
        """Create a backup of a file."""
        try:
            if not FileUtils.file_exists(file_path):
                return None
            backup_path = f"{file_path}{backup_suffix}"
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception:
            return None

    @staticmethod
    def restore_from_backup(backup_path: str, target_path: str) -> bool:
        """Restore a file from backup."""
        try:
            if not FileUtils.file_exists(backup_path):
                return False
            if FileUtils.file_exists(target_path):
                FileUtils.create_backup(target_path, ".pre_restore_backup")
            shutil.copy2(backup_path, target_path)
            return True
        except Exception:
            return False

    @staticmethod
    def safe_delete_file(file_path: str) -> bool:
        """Safely delete a file with backup."""
        try:
            if not FileUtils.file_exists(file_path):
                return True
            backup_path = FileUtils.create_backup(file_path, ".pre_delete_backup")
            if not backup_path:
                return False
            Path(file_path).unlink()
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------
    @staticmethod
    def validate_file_path(file_path: str) -> Dict[str, Any]:
        """Validate file path and return detailed information."""
        result = {
            "path": file_path,
            "exists": False,
            "is_file": False,
            "is_directory": False,
            "readable": False,
            "writable": False,
            "size_bytes": 0,
            "modified_time": None,
            "errors": [],
        }
        try:
            path_obj = Path(file_path)
            result["exists"] = path_obj.exists()
            if result["exists"]:
                result["is_file"] = path_obj.is_file()
                result["is_directory"] = path_obj.is_dir()
                result["readable"] = FileUtils.is_file_readable(file_path)
                result["writable"] = FileUtils.is_file_writable(file_path)
                size = FileUtils.get_file_size(file_path)
                result["size_bytes"] = size or 0
                result["modified_time"] = FileUtils.get_file_modified_time(file_path)
        except Exception as e:
            result["errors"].append(str(e))
        return result
