#!/usr/bin/env python3
"""
Discovery Configuration
======================

Manages configuration settings for repository discovery operations.
Separates configuration concerns from discovery logic.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class DiscoveryConfig:
    """Discovery configuration settings"""

    scan_depth: int = 3
    max_file_size_mb: int = 10
    excluded_patterns: List[str] = field(
        default_factory=lambda: [
            "*.pyc",
            "*.pyo",
            "__pycache__",
            ".git",
            ".svn",
            "node_modules",
            "*.log",
            "*.tmp",
            "*.cache",
            ".DS_Store",
            "Thumbs.db",
        ]
    )
    included_extensions: List[str] = field(
        default_factory=lambda: [
            ".py",
            ".js",
            ".ts",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".cs",
            ".go",
            ".rs",
            ".php",
            ".rb",
            ".swift",
            ".kt",
            ".scala",
            ".html",
            ".css",
            ".xml",
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".ini",
            ".cfg",
            ".conf",
        ]
    )

    def get_excluded_patterns_count(self) -> int:
        """Get count of excluded patterns"""
        return len(self.excluded_patterns)

    def get_included_extensions_count(self) -> int:
        """Get count of included extensions"""
        return len(self.included_extensions)

    def add_excluded_pattern(self, pattern: str):
        """Add a new excluded pattern"""
        if pattern not in self.excluded_patterns:
            self.excluded_patterns.append(pattern)

    def add_included_extension(self, extension: str):
        """Add a new included extension"""
        if extension not in self.included_extensions:
            self.included_extensions.append(extension)

