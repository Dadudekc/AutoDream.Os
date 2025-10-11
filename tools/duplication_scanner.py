#!/usr/bin/env python3
"""
Duplication Scanner - V2 Compliant
===================================

Codebase scanning and hash generation for duplication detection.
Extracted from duplication_analyzer.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

import ast
import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Any


class DuplicationScanner:
    """Scans codebase for potential duplications using AST hashing."""

    def __init__(self, project_root: Path):
        """Initialize scanner."""
        self.project_root = project_root
        self.exclude_patterns = [
            "__pycache__",
            ".git",
            "node_modules",
            "*.pyc",
            ".pytest_cache",
            "build",
            "dist",
            "venv",
        ]

    def scan_codebase(self) -> dict[str, Any]:
        """Scan entire codebase for potential duplications."""
        print("🔍 Scanning codebase for duplications...")

        functions = defaultdict(list)
        classes = defaultdict(list)
        imports = defaultdict(list)

        for py_file in self.project_root.rglob("*.py"):
            if self._should_include_file(py_file):
                try:
                    content = py_file.read_text(encoding="utf-8")
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            func_hash = self._get_function_hash(node, content)
                            functions[func_hash].append(
                                {
                                    "file": str(py_file.relative_to(self.project_root)),
                                    "name": node.name,
                                    "line": node.lineno,
                                    "content": self._get_node_content(node, content),
                                }
                            )

                        elif isinstance(node, ast.ClassDef):
                            class_hash = self._get_class_hash(node, content)
                            classes[class_hash].append(
                                {
                                    "file": str(py_file.relative_to(self.project_root)),
                                    "name": node.name,
                                    "line": node.lineno,
                                    "content": self._get_node_content(node, content),
                                }
                            )

                except Exception as e:
                    print(f"Warning: Could not process {py_file}: {e}")

        return {
            "functions": dict(functions),
            "classes": dict(classes),
            "imports": dict(imports),
            "summary": {
                "total_files": len(list(self.project_root.rglob("*.py"))),
                "processed_files": len(
                    [f for f in self.project_root.rglob("*.py") if self._should_include_file(f)]
                ),
                "function_groups": len(functions),
                "class_groups": len(classes),
                "potential_duplicates": sum(len(v) > 1 for v in functions.values())
                + sum(len(v) > 1 for v in classes.values()),
            },
        }

    def _should_include_file(self, file_path: Path) -> bool:
        """Determine if file should be included in analysis."""
        file_str = str(file_path)
        for pattern in self.exclude_patterns:
            if pattern in file_str:
                return False
        return file_path.suffix == ".py"

    def _get_function_hash(self, node: ast.FunctionDef, content: str) -> str:
        """Generate hash for function content."""
        func_content = self._get_node_content(node, content)
        clean_content = self._clean_code_content(func_content)
        return hashlib.md5(clean_content.encode()).hexdigest()

    def _get_class_hash(self, node: ast.ClassDef, content: str) -> str:
        """Generate hash for class content."""
        class_content = self._get_node_content(node, content)
        clean_content = self._clean_code_content(class_content)
        return hashlib.md5(clean_content.encode()).hexdigest()

    def _get_node_content(self, node: ast.AST, content: str) -> str:
        """Extract source code for AST node."""
        if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
            lines = content.split("\n")
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
        return ""

    def _clean_code_content(self, content: str) -> str:
        """Clean code content for better duplicate detection."""
        lines = []
        for line in content.split("\n"):
            line = line.split("#")[0]  # Remove comments
            line = line.strip()  # Remove whitespace
            if line:
                lines.append(line)
        return "\n".join(lines)
