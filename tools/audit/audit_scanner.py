#!/usr/bin/env python3
"""
Audit Scanner - V2 Compliance Module
==================================

Focused module for scanning and auditing project files.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Audit Scanning
"""

import hashlib
import json
import os
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


class AuditScanner:
    """Scans and audits project files for cleanup opportunities."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_path = project_root / "tools" / "audit_config.json"
        self.auditignore_path = project_root / ".auditignore"
        self.min_py_files = 50
        self.max_py_drop = 10

    def scan_working_tree(self) -> dict[str, Any]:
        """Scan working tree for files and analysis."""
        scan_results = {
            "timestamp": self._get_timestamp(),
            "file_counts": defaultdict(int),
            "file_sizes": defaultdict(int),
            "duplicate_groups": {},
            "temp_files": [],
            "versioned_files": [],
            "total_files": 0,
            "total_size": 0
        }
        
        # Load ignore patterns
        ignore_patterns = self._load_ignore_patterns()
        
        # Scan files
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and not self._should_ignore(file_path, ignore_patterns):
                self._analyze_file(file_path, scan_results)
        
        return scan_results

    def _load_ignore_patterns(self) -> list[str]:
        """Load ignore patterns from config and auditignore file."""
        patterns = [
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            ".tox",
            ".venv",
            "node_modules",
            "build",
            "dist",
            "*.egg-info",
            ".mypy_cache"
        ]
        
        # Load from auditignore file if it exists
        if self.auditignore_path.exists():
            try:
                with open(self.auditignore_path, 'r', encoding='utf-8') as f:
                    patterns.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])
            except Exception:
                pass
        
        return patterns

    def _should_ignore(self, file_path: Path, ignore_patterns: list[str]) -> bool:
        """Check if file should be ignored."""
        path_str = str(file_path.relative_to(self.project_root))
        
        for pattern in ignore_patterns:
            if pattern in path_str:
                return True
        
        return False

    def _analyze_file(self, file_path: Path, scan_results: dict[str, Any]) -> None:
        """Analyze individual file."""
        try:
            file_size = file_path.stat().st_size
            file_ext = file_path.suffix.lower()
            
            # Update counts and sizes
            scan_results["file_counts"][file_ext] += 1
            scan_results["file_sizes"][file_ext] += file_size
            scan_results["total_files"] += 1
            scan_results["total_size"] += file_size
            
            # Check for duplicates
            file_hash = self._calculate_file_hash(file_path)
            if file_hash in scan_results["duplicate_groups"]:
                scan_results["duplicate_groups"][file_hash].append(str(file_path))
            else:
                scan_results["duplicate_groups"][file_hash] = [str(file_path)]
            
            # Check for temp files
            if self._is_temp_file(file_path):
                scan_results["temp_files"].append(str(file_path))
            
            # Check for versioned files
            if self._is_versioned_file(file_path):
                scan_results["versioned_files"].append(str(file_path))
                
        except Exception:
            # Skip files that can't be analyzed
            pass

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""

    def _is_temp_file(self, file_path: Path) -> bool:
        """Check if file is a temporary file."""
        temp_patterns = [
            ".tmp", ".temp", ".bak", ".backup", "~", ".swp", ".swo"
        ]
        
        file_name = file_path.name.lower()
        return any(pattern in file_name for pattern in temp_patterns)

    def _is_versioned_file(self, file_path: Path) -> bool:
        """Check if file is a versioned file."""
        versioned_patterns = [
            ".orig", ".rej", ".patch", ".diff"
        ]
        
        file_name = file_path.name.lower()
        return any(pattern in file_name for pattern in versioned_patterns)

    def compare_with_git(self, scan_results: dict[str, Any]) -> dict[str, Any]:
        """Compare current state with git repository."""
        git_comparison = {
            "git_available": False,
            "files_changed": 0,
            "files_added": 0,
            "files_deleted": 0,
            "py_files_changed": 0
        }
        
        try:
            # Check if git is available
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                git_comparison["git_available"] = True
                
                # Parse git status
                for line in result.stdout.split('\n'):
                    if line.strip():
                        status = line[:2]
                        file_path = line[3:]
                        
                        if 'M' in status:
                            git_comparison["files_changed"] += 1
                        if 'A' in status:
                            git_comparison["files_added"] += 1
                        if 'D' in status:
                            git_comparison["files_deleted"] += 1
                        
                        if file_path.endswith('.py'):
                            git_comparison["py_files_changed"] += 1
                            
        except Exception:
            pass
        
        return git_comparison

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")
