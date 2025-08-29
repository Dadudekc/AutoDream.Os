"""Test discovery utilities."""

from pathlib import Path
from typing import List


def discover_test_files(start_dir: str, pattern: str = "test_*.py") -> List[Path]:
    """Recursively discover test files.

    Args:
        start_dir: Directory to begin searching from.
        pattern: Glob pattern for matching test files.

    Returns:
        A list of paths to discovered test files.
    """
    return list(Path(start_dir).rglob(pattern))
