#!/usr/bin/env python3
"""
File Utils - File and Directory Operations

This module provides file utility functions including:
- JSON/YAML read/write operations
- Directory management
- File hashing and validation
- Path operations

Architecture: Single Responsibility Principle - file operations only
LOC: 150 lines (under 200 limit)
"""

import json
import yaml
import os
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class FileUtils:
    """File and directory utility functions"""

    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists, create if not"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False

    @staticmethod
    def read_json(file_path: str) -> Optional[Dict[str, Any]]:
        """Read JSON file and return data"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read JSON {file_path}: {e}")
            return None

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]) -> bool:
        """Write data to JSON file"""
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
        """Read YAML file and return data"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to read YAML {file_path}: {e}")
            return None

    @staticmethod
    def write_yaml(file_path: str, data: Dict[str, Any]) -> bool:
        """Write data to YAML file"""
        try:
            FileUtils.ensure_directory(os.path.dirname(file_path))
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            logger.error(f"Failed to write YAML {file_path}: {e}")
            return False

    @staticmethod
    def get_file_hash(file_path: str) -> Optional[str]:
        """Get SHA256 hash of file"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Failed to get hash for {file_path}: {e}")
            return None

    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """List files in directory matching pattern"""
        try:
            path = Path(directory)
            if not path.exists():
                return []
            return [str(f) for f in path.glob(pattern)]
        except Exception as e:
            logger.error(f"Failed to list files in {directory}: {e}")
            return []

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists"""
        try:
            return Path(file_path).exists()
        except Exception:
            return False

    @staticmethod
    def get_file_size(file_path: str) -> Optional[int]:
        """Get file size in bytes"""
        try:
            return Path(file_path).stat().st_size
        except Exception as e:
            logger.error(f"Failed to get file size for {file_path}: {e}")
            return None

    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file from source to destination"""
        try:
            import shutil

            FileUtils.ensure_directory(os.path.dirname(destination))
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            logger.error(f"Failed to copy file from {source} to {destination}: {e}")
            return False


def main():
    """CLI interface for file utilities testing."""
    import argparse

    parser = argparse.ArgumentParser(description="File Utils CLI")
    parser.add_argument("--read-json", help="Read JSON file")
    parser.add_argument("--read-yaml", help="Read YAML file")
    parser.add_argument("--write-json", help="Write JSON file")
    parser.add_argument("--write-yaml", help="Write YAML file")
    parser.add_argument("--hash", help="Get file hash")
    parser.add_argument("--list", help="List files in directory")
    parser.add_argument("--exists", help="Check if file exists")
    parser.add_argument("--size", help="Get file size")

    args = parser.parse_args()

    if args.read_json:
        data = FileUtils.read_json(args.read_json)
        print(f"JSON data: {data}")
    elif args.read_yaml:
        data = FileUtils.read_yaml(args.read_yaml)
        print(f"YAML data: {data}")
    elif args.write_json:
        test_data = {"test": "data", "number": 42}
        success = FileUtils.write_json(args.write_json, test_data)
        print(f"Write JSON success: {success}")
    elif args.write_yaml:
        test_data = {"test": "data", "number": 42}
        success = FileUtils.write_yaml(args.write_yaml, test_data)
        print(f"Write YAML success: {success}")
    elif args.hash:
        file_hash = FileUtils.get_file_hash(args.hash)
        print(f"File hash: {file_hash}")
    elif args.list:
        files = FileUtils.list_files(args.list)
        print(f"Files: {files}")
    elif args.exists:
        exists = FileUtils.file_exists(args.exists)
        print(f"File exists: {exists}")
    elif args.size:
        size = FileUtils.get_file_size(args.size)
        print(f"File size: {size} bytes")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
