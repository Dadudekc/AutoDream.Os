#!/usr/bin/env python3
"""
Functionality Scanner - V2 Compliance Module
==========================================

Focused module for scanning and analyzing functionality signatures.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Functionality Scanning
"""

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


class FunctionalityScanner:
    """Scans and analyzes functionality signatures."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.baseline_file = project_root / "verification_baseline.json"
        self.results_dir = project_root / "verification_results"
        self.results_dir.mkdir(exist_ok=True)

    def generate_functionality_signature(self) -> dict[str, Any]:
        """Generate comprehensive functionality signature."""
        signature = {
            "timestamp": self._get_timestamp(),
            "file_signatures": self._scan_file_signatures(),
            "import_signatures": self._scan_import_signatures(),
            "function_signatures": self._scan_function_signatures(),
            "class_signatures": self._scan_class_signatures(),
            "test_signatures": self._scan_test_signatures()
        }
        
        return signature

    def _scan_file_signatures(self) -> dict[str, str]:
        """Scan file signatures using MD5 hashes."""
        signatures = {}
        
        for py_file in self.project_root.rglob("*.py"):
            if self._should_include_file(py_file):
                try:
                    with open(py_file, 'rb') as f:
                        content = f.read()
                        signatures[str(py_file.relative_to(self.project_root))] = hashlib.md5(content).hexdigest()
                except Exception:
                    # Skip files that can't be read
                    pass
        
        return signatures

    def _scan_import_signatures(self) -> dict[str, list[str]]:
        """Scan import signatures."""
        import_signatures = {}
        
        for py_file in self.project_root.rglob("*.py"):
            if self._should_include_file(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        imports = self._extract_imports(content)
                        if imports:
                            import_signatures[str(py_file.relative_to(self.project_root))] = imports
                except Exception:
                    pass
        
        return import_signatures

    def _scan_function_signatures(self) -> dict[str, list[str]]:
        """Scan function signatures."""
        function_signatures = {}
        
        for py_file in self.project_root.rglob("*.py"):
            if self._should_include_file(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        functions = self._extract_functions(content)
                        if functions:
                            function_signatures[str(py_file.relative_to(self.project_root))] = functions
                except Exception:
                    pass
        
        return function_signatures

    def _scan_class_signatures(self) -> dict[str, list[str]]:
        """Scan class signatures."""
        class_signatures = {}
        
        for py_file in self.project_root.rglob("*.py"):
            if self._should_include_file(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        classes = self._extract_classes(content)
                        if classes:
                            class_signatures[str(py_file.relative_to(self.project_root))] = classes
                except Exception:
                    pass
        
        return class_signatures

    def _scan_test_signatures(self) -> dict[str, Any]:
        """Scan test signatures."""
        test_signatures = {
            "test_files": [],
            "test_functions": [],
            "test_coverage": {}
        }
        
        # Find test files
        for test_file in self.project_root.rglob("test_*.py"):
            if self._should_include_file(test_file):
                test_signatures["test_files"].append(str(test_file.relative_to(self.project_root)))
        
        # Find test functions
        for py_file in self.project_root.rglob("*.py"):
            if self._should_include_file(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        test_functions = self._extract_test_functions(content)
                        if test_functions:
                            test_signatures["test_functions"].extend(test_functions)
                except Exception:
                    pass
        
        return test_signatures

    def _should_include_file(self, file_path: Path) -> bool:
        """Check if file should be included in scanning."""
        exclude_patterns = [
            "__pycache__",
            ".venv",
            "node_modules",
            ".git",
            "build",
            "dist",
            ".pytest_cache",
            ".tox",
            ".coverage",
            "htmlcov"
        ]
        
        path_str = str(file_path)
        return not any(pattern in path_str for pattern in exclude_patterns)

    def _extract_imports(self, content: str) -> list[str]:
        """Extract import statements from content."""
        imports = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('import ', 'from ')):
                imports.append(line)
        
        return imports

    def _extract_functions(self, content: str) -> list[str]:
        """Extract function definitions from content."""
        functions = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('def ') and ':' in line:
                functions.append(line)
        
        return functions

    def _extract_classes(self, content: str) -> list[str]:
        """Extract class definitions from content."""
        classes = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('class ') and ':' in line:
                classes.append(line)
        
        return classes

    def _extract_test_functions(self, content: str) -> list[str]:
        """Extract test function definitions from content."""
        test_functions = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('def test_') and ':' in line:
                test_functions.append(line)
        
        return test_functions

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
