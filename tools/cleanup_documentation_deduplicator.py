#!/usr/bin/env python3
"""
Documentation Cleanup - Deduplication Module
============================================

Handles deduplication logic to consolidate duplicate documentation.

V2 Compliance: Extracted from cleanup_documentation.py (448 lines → modular)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-10-11
License: MIT
"""

import re
from collections import defaultdict
from pathlib import Path


class DocumentationDeduplicator:
    """Handles deduplication of documentation files."""

    def __init__(self, repo_root: Path):
        """Initialize deduplicator.

        Args:
            repo_root: Path to repository root
        """
        self.repo_root = repo_root
        self.dedup_groups: dict[str, list[Path]] = defaultdict(list)

    def apply_deduplication(self, candidates: list[Path]) -> list[Path]:
        """Apply deduplication logic to candidates.

        Args:
            candidates: List of candidate files to deduplicate

        Returns:
            List of files to archive (duplicates only, keeping preferred)
        """
        archive_set = []

        # Group by normalized topic
        for candidate in candidates:
            topic = self._normalize_topic(candidate)
            self.dedup_groups[topic].append(candidate)

        # For each group, select file to keep
        for topic, files in self.dedup_groups.items():
            if len(files) <= 1:
                # No duplicates
                archive_set.extend(files)
                continue

            # Sort by preference: docs/** > newer mtime > root
            kept = self._select_preferred_file(files)

            # Archive the rest
            for file in files:
                if file != kept:
                    archive_set.append(file)

        return archive_set

    def _normalize_topic(self, path: Path) -> str:
        """Normalize path to topic name for deduplication.

        Args:
            path: Path to normalize

        Returns:
            Normalized topic string
        """
        name = path.stem.lower()

        # Strip common prefixes
        prefixes = [
            "consolidation_",
            "swarm_",
            "survey_",
            "notes_",
            "draft_",
            "old_",
            "backup_",
            "temp_",
            "tmp_",
        ]
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix) :]

        # Remove numbers, dashes, underscores
        name = re.sub(r"[-_0-9]+", " ", name)
        name = name.strip()

        return name

    def _select_preferred_file(self, files: list[Path]) -> Path:
        """Select preferred file from duplicate group.

        Args:
            files: List of duplicate files

        Returns:
            Preferred file to keep
        """
        # Prefer docs/** files
        docs_files = [f for f in files if str(f).startswith("docs/")]
        if docs_files:
            # Among docs files, prefer newer
            return max(docs_files, key=lambda f: (self.repo_root / f).stat().st_mtime)

        # Otherwise, prefer newer file
        return max(files, key=lambda f: (self.repo_root / f).stat().st_mtime)
