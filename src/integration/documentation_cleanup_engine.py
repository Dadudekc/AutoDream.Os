#!/usr/bin/env python3
"""
Documentation Cleanup Engine - Cleanup logic for Aggressive Documentation Cleanup System
==================================================================================

Cleanup logic extracted from aggressive_documentation_cleanup_system.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import hashlib
import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .documentation_cleanup_models import (
    CleanupConfiguration,
    CleanupFile,
    CleanupStrategy,
    FileAnalysisResult,
    FileCategory,
)

logger = logging.getLogger(__name__)


class DocumentationCleanupEngine:
    """Documentation cleanup engine for aggressive cleanup operations."""

    def __init__(self):
        """Initialize documentation cleanup engine."""
        self.file_cache: dict[str, CleanupFile] = {}
        self.content_hashes: dict[str, list[str]] = defaultdict(list)
        self.duplicate_groups: list[list[str]] = []
        logger.info("Documentation cleanup engine initialized")

    def analyze_directory(
        self, directory_path: str, config: CleanupConfiguration
    ) -> FileAnalysisResult:
        """Analyze directory for cleanup potential."""
        try:
            total_files = 0
            total_size = 0
            critical_files = 0
            recent_files = 0
            duplicate_files = 0
            empty_files = 0
            old_files = 0
            devlog_files = 0
            potential_savings = 0

            directory = Path(directory_path)
            if not directory.exists():
                raise ValueError(f"Directory {directory_path} does not exist")

            # Process all files
            for file_path in directory.rglob("*"):
                if file_path.is_file() and file_path.suffix in config.file_extensions:
                    file_analysis = self._analyze_file(file_path, config)
                    self.file_cache[str(file_path)] = file_analysis

                    total_files += 1
                    total_size += file_analysis.size

                    # Categorize files
                    if file_analysis.category == FileCategory.KEEP_CRITICAL:
                        critical_files += 1
                    elif file_analysis.category == FileCategory.KEEP_RECENT:
                        recent_files += 1
                    elif file_analysis.is_duplicate:
                        duplicate_files += 1
                        potential_savings += file_analysis.size
                    elif file_analysis.is_empty:
                        empty_files += 1
                        potential_savings += file_analysis.size
                    elif file_analysis.is_old:
                        old_files += 1
                        potential_savings += file_analysis.size

                    if file_analysis.is_devlog:
                        devlog_files += 1

            # Identify duplicate groups
            self._identify_duplicate_groups()

            logger.info(f"Directory analysis completed: {total_files} files analyzed")

            return FileAnalysisResult(
                total_files=total_files,
                total_size=total_size,
                critical_files=critical_files,
                recent_files=recent_files,
                duplicate_files=duplicate_files,
                empty_files=empty_files,
                old_files=old_files,
                devlog_files=devlog_files,
                potential_savings=potential_savings,
                analysis_timestamp=datetime.now(),
            )

        except Exception as e:
            logger.error(f"Error analyzing directory {directory_path}: {e}")
            raise

    def _analyze_file(self, file_path: Path, config: CleanupConfiguration) -> CleanupFile:
        """Analyze individual file for cleanup potential."""
        try:
            # Get file stats
            stat = file_path.stat()
            size = stat.st_size
            last_modified = datetime.fromtimestamp(stat.st_mtime)

            # Read file content
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                    content_preview = content[:200] if len(content) > 200 else content
            except:
                content = ""
                content_preview = ""

            # Calculate content hash
            content_hash = hashlib.md5(content.encode()).hexdigest()

            # Determine file category
            category = self._categorize_file(file_path, content, config, last_modified)

            # Check for duplicates
            is_duplicate = content_hash in self.content_hashes
            if not is_duplicate:
                self.content_hashes[content_hash].append(str(file_path))

            # Check if file is old
            age_threshold = datetime.now() - timedelta(days=config.max_file_age_days)
            is_old = last_modified < age_threshold

            # Check if file is empty
            is_empty = size < config.min_file_size_bytes

            # Check if file is devlog
            is_devlog = self._is_devlog_file(file_path, content)

            # Check for duplicate names
            is_duplicate_name = self._has_duplicate_name(file_path)

            # Calculate priority score
            priority_score = self._calculate_priority_score(
                category, is_duplicate, is_empty, is_old, is_devlog
            )

            return CleanupFile(
                path=str(file_path),
                size=size,
                category=category,
                priority_score=priority_score,
                content_hash=content_hash,
                is_duplicate=is_duplicate,
                is_empty=is_empty,
                is_old=is_old,
                is_devlog=is_devlog,
                is_duplicate_name=is_duplicate_name,
                last_modified=last_modified,
                content_preview=content_preview,
                dependencies=self._find_dependencies(content),
            )

        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            # Return minimal file info on error
            return CleanupFile(
                path=str(file_path),
                size=0,
                category=FileCategory.KEEP_CRITICAL,  # Default to keep on error
                priority_score=0,
                content_hash="",
                is_duplicate=False,
                is_empty=True,
                is_old=False,
                is_devlog=False,
                is_duplicate_name=False,
                last_modified=datetime.now(),
                content_preview="",
                dependencies=[],
            )

    def _categorize_file(
        self, file_path: Path, content: str, config: CleanupConfiguration, last_modified: datetime
    ) -> FileCategory:
        """Categorize file based on various criteria."""
        file_name = file_path.name.lower()
        file_path_str = str(file_path).lower()

        # Check if file is in preserve list
        for preserve_pattern in config.preserve_critical_files:
            if preserve_pattern.lower() in file_path_str:
                return FileCategory.KEEP_CRITICAL

        # Check for critical files
        critical_patterns = [
            "readme",
            "license",
            "changelog",
            "contributing",
            "install",
            "setup",
            "config",
            "main",
            "index",
            "api",
            "documentation",
        ]

        for pattern in critical_patterns:
            if pattern in file_name or pattern in file_path_str:
                return FileCategory.KEEP_CRITICAL

        # Check if file is recent and should be kept
        if config.preserve_recent_files:
            recent_threshold = datetime.now() - timedelta(days=30)
            if last_modified > recent_threshold:
                return FileCategory.KEEP_RECENT

        # Check if file is a devlog
        if self._is_devlog_file(file_path, content):
            return FileCategory.CONSOLIDATE

        # Check if file is old
        age_threshold = datetime.now() - timedelta(days=config.max_file_age_days)
        if last_modified < age_threshold:
            return FileCategory.DELETE_AGGRESSIVE

        # Default categorization
        return FileCategory.DELETE_AGGRESSIVE

    def _is_devlog_file(self, file_path: Path, content: str) -> bool:
        """Check if file is a devlog."""
        file_name = file_path.name.lower()
        return (
            "devlog" in file_name
            or "dev_log" in file_name
            or "agent" in file_name
            or "log" in file_name
            and "dev" in content.lower()
        )

    def _has_duplicate_name(self, file_path: Path) -> bool:
        """Check if file has duplicate name."""
        file_name = file_path.name
        parent_dir = file_path.parent

        # Check for files with same name in same directory
        for other_file in parent_dir.iterdir():
            if other_file.is_file() and other_file != file_path and other_file.name == file_name:
                return True
        return False

    def _calculate_priority_score(
        self,
        category: FileCategory,
        is_duplicate: bool,
        is_empty: bool,
        is_old: bool,
        is_devlog: bool,
    ) -> int:
        """Calculate priority score for cleanup."""
        score = 0

        # Category scoring
        if category == FileCategory.KEEP_CRITICAL:
            score = 100
        elif category == FileCategory.KEEP_RECENT:
            score = 80
        elif category == FileCategory.CONSOLIDATE:
            score = 60
        elif category == FileCategory.DELETE_AGGRESSIVE:
            score = 40
        else:  # DELETE_NUCLEAR
            score = 20

        # Adjustment factors
        if is_duplicate:
            score -= 30
        if is_empty:
            score -= 20
        if is_old:
            score -= 15
        if is_devlog:
            score -= 10

        return max(0, min(100, score))

    def _find_dependencies(self, content: str) -> list[str]:
        """Find file dependencies from content."""
        dependencies = []

        # Look for markdown links
        markdown_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        for _, link in markdown_links:
            if link.startswith("./") or link.startswith("../"):
                dependencies.append(link)

        # Look for include statements
        include_patterns = re.findall(r"include\s*:\s*([^\s\n]+)", content, re.IGNORECASE)
        dependencies.extend(include_patterns)

        return dependencies

    def _identify_duplicate_groups(self):
        """Identify groups of duplicate files."""
        self.duplicate_groups = []
        for content_hash, file_paths in self.content_hashes.items():
            if len(file_paths) > 1:
                self.duplicate_groups.append(file_paths)

    def get_cleanup_recommendations(self, strategy: CleanupStrategy) -> dict[str, Any]:
        """Get cleanup recommendations based on strategy."""
        recommendations = {
            "strategy": strategy.value,
            "files_to_keep": [],
            "files_to_delete": [],
            "files_to_consolidate": [],
            "estimated_space_saved": 0,
            "estimated_files_removed": 0,
        }

        for file_path, file_analysis in self.file_cache.items():
            action = file_analysis.get_cleanup_action(strategy)

            if action == "keep":
                recommendations["files_to_keep"].append(file_path)
            elif action == "delete":
                recommendations["files_to_delete"].append(file_path)
                recommendations["estimated_space_saved"] += file_analysis.size
                recommendations["estimated_files_removed"] += 1
            elif action == "consolidate":
                recommendations["files_to_consolidate"].append(file_path)

        return recommendations

    def get_duplicate_analysis(self) -> dict[str, Any]:
        """Get duplicate file analysis."""
        return {
            "duplicate_groups": len(self.duplicate_groups),
            "total_duplicate_files": sum(len(group) for group in self.duplicate_groups),
            "potential_space_saved": sum(
                sum(self.file_cache[path].size for path in group[1:])
                for group in self.duplicate_groups
            ),
            "largest_duplicate_group": max(len(group) for group in self.duplicate_groups)
            if self.duplicate_groups
            else 0,
        }
