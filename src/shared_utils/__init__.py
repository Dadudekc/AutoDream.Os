"""
Shared Utilities - Unified Workspace Integration
================================================

Shared utility functions for API clients, configuration, file hashing, and logging.
Ported from unified-workspace repository (Team Beta Repo 5/8).

V2 Compliance: Utilities integration.

Original: unified-workspace repository
Ported: Agent-7 - Repository Cloning Specialist
License: MIT
"""

from .api_client import APIClient, AsyncAPIClient
from .config import get_setting, get_workspace_root, load_env
from .file_hash import compute_file_sha256, find_duplicate_files
from .logger import setup_logger

__all__ = [
    "APIClient",
    "AsyncAPIClient",
    "get_setting",
    "get_workspace_root",
    "load_env",
    "compute_file_sha256",
    "find_duplicate_files",
    "setup_logger",
]
