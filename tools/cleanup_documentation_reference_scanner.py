#!/usr/bin/env python3
"""
Documentation Cleanup - Reference Scanner Module
================================================

Handles reference scanning to protect actively-used documentation.

V2 Compliance: Extracted from cleanup_documentation.py (448 lines → modular)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-10-11
License: MIT
"""

from pathlib import Path


class ReferenceScanner:
    """Scans for references to documentation files in code and canonical docs."""

    def __init__(self, repo_root: Path):
        """Initialize reference scanner.

        Args:
            repo_root: Path to repository root
        """
        self.repo_root = repo_root

    def scan_references(self, candidates: list[Path]) -> set[Path]:
        """Scan for references to candidates in code and canonical docs.

        Args:
            candidates: List of candidate files to check

        Returns:
            Set of files that are referenced (should be preserved)
        """
        referenced_files = set()

        # Define reference sources
        reference_sources = []

        # Canonical docs
        for pattern in ["README.md", "AGENTS.md", "docs/**/*.md", "docs/**/*.rst"]:
            reference_sources.extend(self._glob_files(pattern))

        # Source code
        for pattern in ["src/**/*.py", "src/**/*.ts", "src/**/*.js"]:
            reference_sources.extend(self._glob_files(pattern))

        # CI/Build files
        for pattern in [".github/workflows/*.yml", "Makefile", "pyproject.toml", "setup.py"]:
            reference_sources.extend(self._glob_files(pattern))

        # Scan each reference source for mentions of candidates
        for candidate in candidates:
            if self._is_referenced(candidate, reference_sources):
                referenced_files.add(candidate)

        return referenced_files

    def _glob_files(self, pattern: str) -> list[Path]:
        """Glob files matching pattern.

        Args:
            pattern: Glob pattern to match

        Returns:
            List of matching file paths (relative to repo_root)
        """
        files = []
        if "**" in pattern:
            # Recursive glob
            parts = pattern.split("**")
            base = parts[0].rstrip("/")
            suffix = parts[1].lstrip("/")
            base_path = self.repo_root / base if base else self.repo_root
            if base_path.exists():
                for path in base_path.rglob(suffix):
                    if path.is_file():
                        files.append(path.relative_to(self.repo_root))
        else:
            # Simple glob
            for path in self.repo_root.glob(pattern):
                if path.is_file():
                    files.append(path.relative_to(self.repo_root))
        return files

    def _is_referenced(self, candidate: Path, sources: list[Path]) -> bool:
        """Check if candidate is referenced in any source file.

        Args:
            candidate: File to check for references
            sources: List of source files to scan

        Returns:
            True if candidate is referenced in any source
        """
        candidate_str = str(candidate)
        candidate_name = candidate.name

        for source in sources:
            source_path = self.repo_root / source
            if not source_path.exists():
                continue

            try:
                with open(source_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    # Check for path or filename mention
                    if candidate_str in content or candidate_name in content:
                        return True
            except Exception:
                # Skip files that can't be read
                continue

        return False
