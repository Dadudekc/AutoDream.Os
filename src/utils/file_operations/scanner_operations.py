#!/usr/bin/env python3
"""
File Scanner Operations Module
==============================

Handles directory scanning, file discovery, and pattern matching.
Part of the unified file utilities system.

Author: Agent-8 (Operations & Support Specialist)
License: MIT
"""

from pathlib import Path


class UnifiedFileScanner:
    """
    Unified file scanner with filtering and pattern matching.

    Provides efficient directory scanning with support for:
    - Extension filtering
    - Exclude patterns
    - Recursive scanning
    - Scan history tracking
    """

    def __init__(self, root_directory: str):
        """
        Initialize file scanner.

        Args:
            root_directory: Root directory to scan from
        """
        self.root = Path(root_directory)
        self.scanned_files: set[str] = set()

    def scan_directory(
        self, extensions: list[str] | None = None, exclude_patterns: list[str] | None = None
    ) -> list[str]:
        """
        Scan directory for files matching criteria.

        Args:
            extensions: List of file extensions to include (e.g., ['.py', '.json'])
                       None = include all extensions
            exclude_patterns: List of patterns to exclude (e.g., ['__pycache__', '.git'])
                            None = no exclusions

        Returns:
            list[str]: List of file paths matching criteria
        """
        files = []
        exclude_patterns = exclude_patterns or []

        if not self.root.exists():
            return files

        for file_path in self.root.rglob("*"):
            if not file_path.is_file():
                continue

            if any(pattern in str(file_path) for pattern in exclude_patterns):
                continue

            if extensions and file_path.suffix.lower() not in extensions:
                continue

            files.append(str(file_path))
            self.scanned_files.add(str(file_path))

        return files

    def scan_by_pattern(self, pattern: str) -> list[str]:
        """
        Scan directory using glob pattern.

        Args:
            pattern: Glob pattern (e.g., '*.py', '**/*.json')

        Returns:
            list[str]: List of matching file paths
        """
        files = []

        if not self.root.exists():
            return files

        for file_path in self.root.glob(pattern):
            if file_path.is_file():
                files.append(str(file_path))
                self.scanned_files.add(str(file_path))

        return files

    def get_scanned_files(self) -> set[str]:
        """
        Get set of all scanned files.

        Returns:
            set[str]: Set of file paths that have been scanned
        """
        return self.scanned_files.copy()

    def reset_scan(self) -> None:
        """Reset scanned files history."""
        self.scanned_files.clear()

    def count_files_by_extension(self) -> dict[str, int]:
        """
        Count scanned files by extension.

        Returns:
            dict[str, int]: Dictionary mapping extensions to file counts
        """
        extension_counts: dict[str, int] = {}

        for file_path in self.scanned_files:
            ext = Path(file_path).suffix.lower() or "no_extension"
            extension_counts[ext] = extension_counts.get(ext, 0) + 1

        return extension_counts


__all__ = [
    "UnifiedFileScanner",
]
