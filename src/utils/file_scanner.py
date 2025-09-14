"""
File Scanner - V2 Compliance Module
================================

Handles file scanning operations following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

import logging
from pathlib import Path

from .config_consolidator import ConfigPattern
from .config_scanners import ConfigurationScanner

logger = logging.getLogger(__name__)


class FileScanner:
    """Handles file scanning operations for configuration patterns."""

    def __init__(self, scanners: list[ConfigurationScanner]):
        """Initialize file scanner with available scanners."""
        self.scanners = scanners
        self.skip_patterns = self._get_skip_patterns()

    def _get_skip_patterns(self) -> set[str]:
        """Get patterns for files that should be skipped."""
        return {
            '__pycache__', '.git', 'venv', 'env', 'node_modules',
            '*.pyc', 'config_core.py', 'config_consolidator.py'
        }

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during scanning."""
        file_str = str(file_path)
        return any(pattern in file_str for pattern in self.skip_patterns)

    def scan_file(self, file_path: Path) -> list[ConfigPattern]:
        """Scan a single file for configuration patterns."""
        if self.should_skip_file(file_path):
            return []

        patterns = []
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Use all registered scanners
            for scanner in self.scanners:
                file_patterns = scanner.scan_file(file_path, lines)
                patterns.extend(file_patterns)

        except Exception as e:
            logger.warning(f'Error scanning {file_path}: {e}')

        return patterns

    def scan_directory(self, root_dir: Path) -> list[ConfigPattern]:
        """Scan all Python files in a directory."""
        all_patterns = []

        for py_file in root_dir.rglob('*.py'):
            file_patterns = self.scan_file(py_file)
            all_patterns.extend(file_patterns)

        logger.info(f'Scanned {len(all_patterns)} patterns from {len(list(root_dir.rglob("*.py")))} files')
        return all_patterns
