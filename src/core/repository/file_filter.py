#!/usr/bin/env python3
"""
File Filter
==========

Handles file filtering and exclusion logic for repository discovery.
Separates filtering concerns from discovery logic.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


class FileFilter:
    """Handles file filtering and exclusion logic"""
    
    def __init__(self, excluded_patterns: List[str]):
        """Initialize the file filter"""
        self.excluded_patterns = excluded_patterns
        logger.info(f"File Filter initialized with {len(excluded_patterns)} patterns")

    def should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded from analysis"""
        try:
            for pattern in self.excluded_patterns:
                if "*" in pattern:
                    # Wildcard pattern matching
                    if file_path.match(pattern):
                        return True
                else:
                    # Exact name matching
                    if file_path.name == pattern or file_path.name.endswith(pattern):
                        return True

            return False
            
        except Exception as e:
            logger.error(f"Error checking file exclusion for {file_path}: {e}")
            return False

    def add_excluded_pattern(self, pattern: str):
        """Add a new excluded pattern"""
        if pattern not in self.excluded_patterns:
            self.excluded_patterns.append(pattern)
            logger.info(f"Added excluded pattern: {pattern}")

    def get_excluded_patterns(self) -> List[str]:
        """Get all excluded patterns"""
        return self.excluded_patterns.copy()

    def get_patterns_count(self) -> int:
        """Get count of excluded patterns"""
        return len(self.excluded_patterns)

