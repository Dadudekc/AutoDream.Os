"""File processing utilities for project scanning."""

import hashlib
import logging
from pathlib import Path
from typing import Any

from .language_analyzer import LanguageAnalyzer

logger = logging.getLogger(__name__)


class FileProcessor:
    """Handles individual file processing and analysis."""

    def __init__(self, language_analyzer: LanguageAnalyzer):
        """Initialize file processor with language analyzer."""
        self.language_analyzer = language_analyzer

    def process_file(self, file_path: Path) -> dict[str, Any]:
        """
        Process a single file and extract metadata.

        Args:
            file_path: Path to the file to process

        Returns:
            Dictionary containing file metadata and analysis
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Could not read {file_path}: {e}")
            return {}

        # Basic file metadata
        stat = file_path.stat()
        file_hash = hashlib.md5(content.encode('utf-8')).hexdigest()

        # Language-specific analysis
        analysis = self.language_analyzer.analyze_file(file_path, content)

        return {
            'path': str(file_path),
            'name': file_path.name,
            'size': stat.st_size,
            'lines': len(content.splitlines()),
            'hash': file_hash,
            'modified': stat.st_mtime,
            'language': analysis.get('language', file_path.suffix),
            'functions': analysis.get('functions', []),
            'classes': analysis.get('classes', {}),
            'routes': analysis.get('routes', []),
            'complexity': analysis.get('complexity', 0),
        }

    def should_skip_file(self, file_path: Path) -> bool:
        """
        Determine if a file should be skipped during processing.

        Args:
            file_path: Path to the file

        Returns:
            True if file should be skipped
        """
        skip_patterns = {
            '__pycache__',
            '.git',
            'venv',
            'env',
            'node_modules',
            '.pytest_cache',
            '.mypy_cache',
            'build',
            'dist',
            '.coverage',
        }

        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts):
            return True

        # Skip common build/cache directories
        if any(pattern in str(file_path) for pattern in skip_patterns):
            return True

        # Skip binary files
        binary_extensions = {'.pyc', '.so', '.dll', '.exe', '.bin', '.jpg', '.png', '.gif', '.pdf'}
        if file_path.suffix.lower() in binary_extensions:
            return True

        return False

    def get_file_type(self, file_path: Path) -> str:
        """
        Determine the type of file based on extension and content.

        Args:
            file_path: Path to the file

        Returns:
            File type string
        """
        suffix = file_path.suffix.lower()
        
        type_mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript_react',
            '.jsx': 'javascript_react',
            '.rs': 'rust',
            '.go': 'go',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'header',
            '.hpp': 'cpp_header',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.toml': 'toml',
            '.md': 'markdown',
            '.txt': 'text',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sql': 'sql',
            '.sh': 'shell',
            '.bat': 'batch',
            '.ps1': 'powershell',
        }

        return type_mapping.get(suffix, 'unknown')