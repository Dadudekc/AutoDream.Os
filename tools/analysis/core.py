"""
V2 Compliance Analysis Core Module
=================================

Core analysis functions for V2 compliance checking.

Features:
- File exclusion logic
- AST line counting
- Basic file analysis
"""

from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# V2 Compliance Constants
MAX_FILE_LOC = 400
MAX_CLASS_LOC = 100
MAX_FUNCTION_LOC = 50
MAX_LINE_LENGTH = 100

EXCLUDE_PATTERNS = [
    "__pycache__",
    ".venv",
    "node_modules",
    ".git",
    "build",
    "dist",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".tox",
    ".coverage",
    "htmlcov",
    "*.egg-info",
    ".mypy_cache",
    ".DS_Store",
]


def should_exclude_file(path: Path) -> bool:
    """Check if file should be excluded from analysis."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    if "test" in path_str.lower() and not path_str.endswith("test_models.py"):
        return False
    return False


def count_lines(node: ast.AST) -> int:
    """Count lines of code for an AST node."""
    if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
        return (node.end_lineno or 0) - (node.lineno or 0) + 1
    return 0


class AnalysisCore:
    """Core analysis functionality for V2 compliance checking."""
    
    def __init__(self):
        self.max_file_loc = MAX_FILE_LOC
        self.max_class_loc = MAX_CLASS_LOC
        self.max_function_loc = MAX_FUNCTION_LOC
        self.max_line_length = MAX_LINE_LENGTH
    
    def analyze_python_file(self, file_path: Path) -> dict[str, Any]:
        """Analyze a single Python file for V2 compliance violations."""
        try:
            with open(file_path, encoding="utf-8") as f:
                source = f.read()
            violations = []
            lines = source.splitlines()
            
            # Check file length
            if len(lines) > self.max_file_loc:
                violations.append({
                    "type": "file_loc",
                    "file": str(file_path),
                    "line": 1,
                    "message": f"File has {len(lines)} lines, exceeds {self.max_file_loc} limit",
                    "severity": "error"
                })
            
            # Check line length
            for i, line in enumerate(lines, 1):
                if len(line) > self.max_line_length:
                    violations.append({
                        "type": "line_length",
                        "file": str(file_path),
                        "line": i,
                        "message": f"Line {i} has {len(line)} characters, exceeds {self.max_line_length} limit",
                        "severity": "warning"
                    })
            
            # Check for print statements
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("print(") and not stripped.startswith("print("):
                    violations.append({
                        "type": "print_statement",
                        "file": str(file_path),
                        "line": i,
                        "message": f"Line {i} contains print statement, use logger instead",
                        "severity": "warning"
                    })
            
            # Parse AST for class/function analysis
            try:
                tree = ast.parse(source, filename=str(file_path))
                violations.extend(self._analyze_ast_node(tree, file_path))
            except SyntaxError as e:
                violations.append({
                    "type": "syntax_error",
                    "file": str(file_path),
                    "line": e.lineno or 0,
                    "message": f"Syntax error: {e.msg}",
                    "severity": "error"
                })
            
            return {
                "file": str(file_path),
                "lines": len(lines),
                "violations": violations,
                "status": "error" if any(v["severity"] == "error" for v in violations) else "warning" if violations else "ok"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return {
                "file": str(file_path),
                "lines": 0,
                "violations": [{
                    "type": "analysis_error",
                    "file": str(file_path),
                    "line": 0,
                    "message": f"Analysis error: {e}",
                    "severity": "error"
                }],
                "status": "error"
            }
    
    def _analyze_ast_node(self, node: ast.AST, file_path: Path) -> list[dict[str, Any]]:
        """Analyze AST node for class/function violations."""
        violations = []
        
        if isinstance(node, ast.ClassDef):
            class_lines = count_lines(node)
            if class_lines > self.max_class_loc:
                violations.append({
                    "type": "class_loc",
                    "file": str(file_path),
                    "line": node.lineno,
                    "message": f"Class '{node.name}' has {class_lines} lines, exceeds {self.max_class_loc} limit",
                    "severity": "error"
                })
        
        elif isinstance(node, ast.FunctionDef):
            func_lines = count_lines(node)
            if func_lines > self.max_function_loc:
                violations.append({
                    "type": "function_loc",
                    "file": str(file_path),
                    "line": node.lineno,
                    "message": f"Function '{node.name}' has {func_lines} lines, exceeds {self.max_function_loc} limit",
                    "severity": "error"
                })
        
        # Recursively analyze child nodes
        for child in ast.iter_child_nodes(node):
            violations.extend(self._analyze_ast_node(child, file_path))
        
        return violations


