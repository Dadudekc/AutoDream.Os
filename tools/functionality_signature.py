#!/usr/bin/env python3
"""
Functionality Signature Generator
==================================

Generates comprehensive functionality signatures for verification.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored from: functionality_verification.py
License: MIT
"""

import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Any


class SignatureGenerator:
    """Generates functionality signatures from codebase."""

    def __init__(self, project_root: Path):
        """Initialize signature generator."""
        self.project_root = project_root

    def generate_signature(self) -> dict[str, Any]:
        """Generate comprehensive functionality signature."""
        signature = {
            "timestamp": datetime.now().isoformat(),
            "files": {},
            "functions": {},
            "classes": {},
            "imports": {},
            "tests": {},
            "apis": {},
            "configurations": {},
        }

        # Scan Python files
        for py_file in self.project_root.rglob("*.py"):
            if self._should_include_file(py_file):
                try:
                    content = py_file.read_text(encoding="utf-8")
                    file_hash = hashlib.md5(content.encode()).hexdigest()

                    signature["files"][str(py_file.relative_to(self.project_root))] = {
                        "hash": file_hash,
                        "size": len(content),
                        "functions": self.extract_functions(content),
                        "classes": self.extract_classes(content),
                        "imports": self.extract_imports(content),
                    }
                except Exception as e:
                    print(f"Warning: Could not process {py_file}: {e}")

        return signature

    def _should_include_file(self, file_path: Path) -> bool:
        """Determine if file should be included in verification."""
        exclude_patterns = [
            "__pycache__",
            ".git",
            "node_modules",
            "*.pyc",
            ".pytest_cache",
            "verification_results",
            "runtime/backups",
        ]

        file_str = str(file_path)
        for pattern in exclude_patterns:
            if pattern in file_str:
                return False

        return file_path.suffix == ".py"

    @staticmethod
    def extract_functions(content: str) -> list[str]:
        """Extract function definitions from Python code."""
        functions = []
        pattern = r"^def\s+(\w+)\s*\("
        for line in content.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                functions.append(match.group(1))
        return functions

    @staticmethod
    def extract_classes(content: str) -> list[str]:
        """Extract class definitions from Python code."""
        classes = []
        pattern = r"^class\s+(\w+)"
        for line in content.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                classes.append(match.group(1))
        return classes

    @staticmethod
    def extract_imports(content: str) -> list[str]:
        """Extract import statements from Python code."""
        imports = []
        patterns = [r"^import\s+([\w.]+)", r"^from\s+([\w.]+)\s+import"]
        for line in content.split("\n"):
            for pattern in patterns:
                match = re.match(pattern, line.strip())
                if match:
                    imports.append(match.group(1))
        return list(set(imports))  # Remove duplicates
