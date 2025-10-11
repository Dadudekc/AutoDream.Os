#!/usr/bin/env python3
"""
File Serialization Operations - V2 Compliance Module
==================================================

JSON/YAML serialization operations.
Extracted from unified_file_utils.py.

Author: Agent-5 (Business Intelligence & Team Beta Leader) - V2 Refactoring
License: MIT
"""

import json
import logging
import os
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class DataSerializationOperations:
    """Handles data serialization operations (JSON/YAML)."""

    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists, create if not."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False

    @staticmethod
    def read_json(file_path: str) -> dict[str, Any] | None:
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
    def write_json(file_path: str, data: dict[str, Any]) -> bool:
        """Write data to JSON file."""
        try:
            DataSerializationOperations.ensure_directory(os.path.dirname(file_path))
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to write JSON {file_path}: {e}")
            return False

    @staticmethod
    def read_yaml(file_path: str) -> dict[str, Any] | None:
        """Read YAML file and return data."""
        try:
            with open(file_path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to read YAML {file_path}: {e}")
            return None

    @staticmethod
    def write_yaml(file_path: str, data: dict[str, Any]) -> bool:
        """Write data to YAML file."""
        try:
            DataSerializationOperations.ensure_directory(os.path.dirname(file_path))
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            logger.error(f"Failed to write YAML {file_path}: {e}")
            return False
