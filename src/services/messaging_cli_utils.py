#!/usr/bin/env python3
"""
Messaging CLI Utilities - Agent Cellphone V2
===========================================

Utility functions for messaging CLI operations.
V2 Compliance: Clean, tested, class-based, reusable, scalable code.

Author: Agent-3 (Infrastructure & DevOps)
License: MIT
"""

import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MessagingCLIUtils:
    """Utility functions for messaging CLI operations."""

    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """Read JSON file safely.

        Args:
            file_path: Path to the JSON file

        Returns:
            Dict containing file contents or empty dict on error
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return {}

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]) -> bool:
        """Write JSON file safely.

        Args:
            file_path: Path to write the JSON file
            data: Data to write to the file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Only create directory if file_path has a directory component
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error writing {file_path}: {e}")
            return False
