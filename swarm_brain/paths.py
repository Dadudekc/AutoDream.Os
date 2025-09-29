#!/usr/bin/env python3
"""
Swarm Brain Path Management
===========================

Ensures required directories exist and manages path operations.
V2 Compliance: ≤400 lines, focused path functionality.
"""

import logging
from pathlib import Path

from .config import CONFIG

logger = logging.getLogger(__name__)


def ensure_directories() -> None:
    """Ensure all required directories exist."""
    try:
        if CONFIG.create_dirs:
            CONFIG.root.mkdir(parents=True, exist_ok=True)
            CONFIG.index_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directories: {CONFIG.root}, {CONFIG.index_path}")
    except Exception as e:
        logger.error(f"Failed to create directories: {e}")
        raise


def get_brain_root() -> Path:
    """Get the brain root directory."""
    ensure_directories()
    return CONFIG.root


def get_sqlite_path() -> Path:
    """Get the SQLite database path."""
    ensure_directories()
    return CONFIG.sqlite_path


def get_index_path() -> Path:
    """Get the embeddings index path."""
    ensure_directories()
    return CONFIG.index_path


def cleanup_old_files(max_age_days: int = 30) -> int:
    """Clean up old files in the brain directory."""
    try:
        import time

        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60

        cleaned_count = 0
        for file_path in CONFIG.root.rglob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()
                    cleaned_count += 1

        logger.info(f"Cleaned up {cleaned_count} old files")
        return cleaned_count

    except Exception as e:
        logger.error(f"Failed to cleanup old files: {e}")
        return 0


# Ensure directories exist on import
ensure_directories()
