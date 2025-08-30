#!/usr/bin/env python3
"""Path utilities for centralized path construction."""

import os
from pathlib import Path
from typing import Optional


class PathUtils:
    """Centralized path construction utilities to eliminate duplication."""
    
    @staticmethod
    def get_task_list_path() -> str:
        """Get standardized task list path."""
        return os.path.join(
            os.getcwd(), "agent_workspaces", "meeting", "task_list.json"
        )
    
    @staticmethod
    def get_meeting_path() -> str:
        """Get meeting directory path."""
        return os.path.join(os.getcwd(), "agent_workspaces", "meeting")
    
    @staticmethod
    def get_contract_system_path() -> str:
        """Get contract system module path."""
        return os.path.join(
            os.getcwd(), "agent_workspaces", "meeting"
        )
    
    @staticmethod
    def ensure_directory_exists(path: str) -> bool:
        """Ensure directory exists, create if necessary."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def is_valid_path(path: str) -> bool:
        """Check if path is valid and accessible."""
        try:
            return os.path.exists(path) and os.access(path, os.R_OK)
        except Exception:
            return False
