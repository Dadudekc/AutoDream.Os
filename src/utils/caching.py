"""Caching utility functions for optimization.

Provides reusable helpers for generating cache keys and calculating file
hashes so individual services can share common implementations.
"""

import hashlib
from pathlib import Path

__all__ = ["generate_cache_key", "calculate_file_hash"]


def generate_cache_key(file_path: Path) -> str:
    """Generate a unique cache key for a file.

    The key is derived from the file path, modification time and size to ensure
    changes invalidate cached entries.
    """

    file_stat = file_path.stat()
    key_string = f"{file_path}_{file_stat.st_mtime}_{file_stat.st_size}"
    return hashlib.md5(key_string.encode()).hexdigest()


def calculate_file_hash(file_path: Path) -> str:
    """Calculate a SHA256 hash of the file contents."""

    try:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return "unknown"
