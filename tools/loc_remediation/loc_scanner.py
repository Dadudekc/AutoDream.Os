#!/usr/bin/env python3
"""
LOC Scanner - V2 Compliance Module
=================================

Focused module for scanning files and identifying LOC violations.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: LOC Scanning
"""

import ast
from pathlib import Path
from typing import Any


class LOCScanner:
    """Scans files for LOC violations."""

    def __init__(self):
        self.max_file_loc = 400
        self.max_class_loc = 100
        self.max_function_loc = 50
        self.exclude_patterns = [
            "__pycache__",
            ".venv",
            "node_modules",
            ".git",
            "build",
            "dist",
            "tests",
            ".pytest_cache",
            ".tox",
            ".coverage",
            "htmlcov",
            "*.egg-info",
            ".mypy_cache",
        ]

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        path_str = str(path)

        for pattern in self.exclude_patterns:
            if pattern in path_str:
                return True

            # Handle wildcard patterns
            if pattern.endswith("*"):
                base_pattern = pattern[:-1]
                if base_pattern in path_str:
                    return True

            # Handle directory patterns
            if pattern.endswith("/"):
                if pattern.rstrip("/") in path_str:
                    return True

        return False

    def count_file_lines(self, file_path: Path) -> int:
        """Count lines in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except Exception:
            return 0

    def count_ast_lines(self, node: ast.AST) -> int:
        """Count lines in an AST node."""
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            if node.end_lineno and node.lineno:
                return node.end_lineno - node.lineno + 1
        return 0

    def scan_file(self, file_path: Path) -> dict[str, Any]:
        """Scan a single file for LOC violations."""
        violations = []
        
        # Check file-level LOC
        file_lines = self.count_file_lines(file_path)
        if file_lines > self.max_file_loc:
            violations.append({
                "type": "file_loc",
                "file": str(file_path),
                "current": file_lines,
                "max": self.max_file_loc,
                "excess": file_lines - self.max_file_loc
            })

        # Parse AST for class/function violations
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_lines = self.count_ast_lines(node)
                    if class_lines > self.max_class_loc:
                        violations.append({
                            "type": "class_loc",
                            "file": str(file_path),
                            "class": node.name,
                            "current": class_lines,
                            "max": self.max_class_loc,
                            "excess": class_lines - self.max_class_loc
                        })
                
                elif isinstance(node, ast.FunctionDef):
                    func_lines = self.count_ast_lines(node)
                    if func_lines > self.max_function_loc:
                        violations.append({
                            "type": "function_loc",
                            "file": str(file_path),
                            "function": node.name,
                            "current": func_lines,
                            "max": self.max_function_loc,
                            "excess": func_lines - self.max_function_loc
                        })
        
        except Exception as e:
            violations.append({
                "type": "parse_error",
                "file": str(file_path),
                "error": str(e)
            })

        return {
            "file": str(file_path),
            "violations": violations,
            "total_violations": len(violations)
        }

    def scan_directory(self, root_path: Path) -> list[dict[str, Any]]:
        """Scan directory for LOC violations."""
        results = []
        
        for py_file in root_path.rglob("*.py"):
            if not self.should_exclude(py_file):
                result = self.scan_file(py_file)
                if result["total_violations"] > 0:
                    results.append(result)
        
        return results
