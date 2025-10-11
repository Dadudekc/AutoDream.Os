"""Configuration utilities for the unified workspace.

This module loads environment variables and provides helper
functions for accessing workspace settings.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


def get_workspace_root() -> Path:
    """Return the root directory of the workspace."""
    return Path(__file__).resolve().parents[2]


def load_env() -> None:
    """Load environment variables from .env file if present."""
    env_path = get_workspace_root() / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def get_setting(key: str, default: str | None = None) -> str | None:
    """Retrieve a setting from the environment.

    Args:
        key: Name of the environment variable to retrieve.
        default: Value to return if the key is not found.
    """
    load_env()
    return os.getenv(key, default)
