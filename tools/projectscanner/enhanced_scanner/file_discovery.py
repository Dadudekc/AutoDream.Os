#!/usr/bin/env python3
"""
File Discovery Handler - V2 Compliant
=====================================

Handles file discovery for enhanced project scanner.
V2 Compliance: ≤150 lines, single responsibility, KISS principle.
"""

import logging
from pathlib import Path
from typing import List, Set

logger = logging.getLogger(__name__)


class FileDiscoveryHandler:
    """Handles file discovery for enhanced project scanner."""
    
    def __init__(self, core):
        """Initialize file discovery handler."""
        self.core = core
        
        # Default ignore directories
        self.default_ignore_dirs = {
            '.git', '__pycache__', 'node_modules', '.pytest_cache',
            'venv', 'env', '.venv', '.env', 'build', 'dist',
            'htmlcov', '.coverage', '.tox', '.mypy_cache',
            'logs', 'tmp', 'temp', '.DS_Store', 'Thumbs.db'
        }
    
    def discover_files(self, file_extensions: Set[str] = None) -> List[Path]:
        """Discover files to scan in the project."""
        
        if file_extensions is None:
            file_extensions = {
                '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c',
                '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift',
                '.kt', '.scala', '.clj', '.hs', '.ml', '.fs', '.vb', '.sql',
                '.html', '.css', '.scss', '.sass', '.less', '.xml', '.json',
                '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.md',
                '.txt', '.rst', '.sh', '.bat', '.ps1', '.dockerfile'
            }
        
        files_to_scan = []
        
        # Discover files recursively
        for file_path in self.core.project_root.rglob('*'):
            if file_path.is_file() and self._should_include_file(file_path, file_extensions):
                files_to_scan.append(file_path)
        
        logger.info(f"📁 Discovered {len(files_to_scan)} files to scan")
        return files_to_scan
    
    def _should_include_file(self, file_path: Path, file_extensions: Set[str]) -> bool:
        """Check if file should be included in scan."""
        
        # Check file extension
        if file_path.suffix.lower() not in file_extensions:
            return False
        
        # Check if in ignored directory
        if self._should_exclude_directory(file_path.parent):
            return False
        
        # Check if file should be excluded
        if self._should_exclude_file(file_path):
            return False
        
        return True
    
    def _should_exclude_directory(self, dir_path: Path) -> bool:
        """Check if directory should be excluded."""
        
        # Check default ignore directories
        if dir_path.name in self.default_ignore_dirs:
            return True
        
        # Check additional ignore directories
        if dir_path.name in self.core.additional_ignore_dirs:
            return True
        
        # Check if any parent directory is ignored
        for parent in dir_path.parents:
            if parent.name in self.default_ignore_dirs:
                return True
            if parent.name in self.core.additional_ignore_dirs:
                return True
        
        return False
    
    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded."""
        
        # Exclude hidden files
        if file_path.name.startswith('.'):
            return True
        
        # Exclude backup files
        if file_path.suffix in {'.bak', '.backup', '.orig', '.tmp'}:
            return True
        
        # Exclude compiled files
        if file_path.suffix in {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe'}:
            return True
        
        # Exclude large files (>10MB)
        try:
            if file_path.stat().st_size > 10 * 1024 * 1024:
                return True
        except (OSError, IOError):
            return True
        
        return False
