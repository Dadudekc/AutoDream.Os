#!/usr/bin/env python3
"""
DRY Elimination File Discovery Engine
====================================

File discovery engine for DRY elimination system.
Handles file discovery, pattern matching, and filtering.
V2 COMPLIANT: Focused file discovery under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR FILE DISCOVERY
@license MIT
"""

import logging
from pathlib import Path

from ..dry_eliminator_models import DRYEliminatorConfig


class FileDiscoveryEngine:
    """File discovery engine for DRY elimination system."""

    def __init__(self, config: DRYEliminatorConfig):
        """Initialize file discovery engine with configuration."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.discovered_files: list[Path] = []
        self.file_metadata: dict = {}

    def discover_python_files(self, project_root: Path) -> list[Path]:
        """Discover Python files in project based on configuration."""
        python_files = []

        try:
            # Find all Python files
            for pattern in self.config.include_patterns:
                for file_path in project_root.glob(pattern):
                    if file_path.is_file() and file_path.suffix == ".py":
                        # Check if file should be excluded
                        if not self._should_exclude_file(file_path):
                            python_files.append(file_path)
                            self._analyze_file_metadata(file_path)

            self.discovered_files = python_files
            self.logger.info(f"Discovered {len(python_files)} Python files for analysis")
            return python_files

        except Exception as e:
            self.logger.error(f"Error discovering Python files: {e}")
            return []

    def _should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded based on patterns."""
        for exclude_pattern in self.config.exclude_patterns:
            if file_path.match(exclude_pattern):
                return True
        return False

    def _analyze_file_metadata(self, file_path: Path):
        """Analyze and store file metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            self.file_metadata[str(file_path)] = {
                "size_bytes": file_path.stat().st_size,
                "line_count": len(content.splitlines()),
                "char_count": len(content),
                "last_modified": file_path.stat().st_mtime,
            }
        except Exception as e:
            self.logger.warning(f"Could not analyze metadata for {file_path}: {e}")

    def get_file_statistics(self) -> dict:
        """Get statistics about discovered files."""
        if not self.discovered_files:
            return {"total_files": 0}

        total_size = sum(meta["size_bytes"] for meta in self.file_metadata.values())
        total_lines = sum(meta["line_count"] for meta in self.file_metadata.values())

        return {
            "total_files": len(self.discovered_files),
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "total_lines": total_lines,
            "avg_file_size": total_size / len(self.discovered_files),
            "avg_lines_per_file": total_lines / len(self.discovered_files),
        }

    def get_files_by_size(self, min_size: int = 0, max_size: int | None = None) -> list[Path]:
        """Get files filtered by size."""
        filtered_files = []

        for file_path in self.discovered_files:
            metadata = self.file_metadata.get(str(file_path), {})
            file_size = metadata.get("size_bytes", 0)

            if file_size >= min_size and (max_size is None or file_size <= max_size):
                filtered_files.append(file_path)

        return filtered_files

    def get_files_by_line_count(
        self, min_lines: int = 0, max_lines: int | None = None
    ) -> list[Path]:
        """Get files filtered by line count."""
        filtered_files = []

        for file_path in self.discovered_files:
            metadata = self.file_metadata.get(str(file_path), {})
            line_count = metadata.get("line_count", 0)

            if line_count >= min_lines and (max_lines is None or line_count <= max_lines):
                filtered_files.append(file_path)

        return filtered_files

    def get_largest_files(self, count: int = 10) -> list[tuple]:
        """Get largest files by size."""
        file_sizes = []

        for file_path in self.discovered_files:
            metadata = self.file_metadata.get(str(file_path), {})
            file_size = metadata.get("size_bytes", 0)
            file_sizes.append((file_path, file_size))

        # Sort by size descending
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        return file_sizes[:count]

    def get_files_by_extension(self, extensions: list[str]) -> list[Path]:
        """Get files filtered by extension."""
        filtered_files = []

        for file_path in self.discovered_files:
            if file_path.suffix.lower() in [ext.lower() for ext in extensions]:
                filtered_files.append(file_path)

        return filtered_files

    def get_files_in_directory(self, directory: str) -> list[Path]:
        """Get files in specific directory."""
        filtered_files = []
        target_dir = Path(directory)

        for file_path in self.discovered_files:
            if target_dir in file_path.parents or file_path.parent == target_dir:
                filtered_files.append(file_path)

        return filtered_files

    def refresh_file_list(self, project_root: Path) -> list[Path]:
        """Refresh the file list (useful for detecting new files)"""
        return self.discover_python_files(project_root)

    def get_file_metadata(self, file_path: Path) -> dict:
        """Get metadata for specific file."""
        return self.file_metadata.get(str(file_path), {})

    def clear_cache(self):
        """Clear discovered files and metadata cache."""
        self.discovered_files.clear()
        self.file_metadata.clear()

    def validate_file(self, file_path: Path) -> bool:
        """Validate that file exists and is readable."""
        try:
            if not file_path.exists():
                return False

            if not file_path.is_file():
                return False

            # Try to read the file
            with open(file_path, encoding="utf-8") as f:
                f.read(1)  # Read just one character to test

            return True
        except Exception:
            return False


# Factory function for dependency injection
def create_file_discovery_engine(config: DRYEliminatorConfig) -> FileDiscoveryEngine:
    """Factory function to create file discovery engine with configuration."""
    return FileDiscoveryEngine(config)


# Export for DI
__all__ = ["FileDiscoveryEngine", "create_file_discovery_engine"]
