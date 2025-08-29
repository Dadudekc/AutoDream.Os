"""Utilities for parsing source files for duplication analysis."""
from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional


class CodeParser:
    """Advanced code parsing and analysis."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.CodeParser")
        self.supported_extensions = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs"}

    def parse_file(self, file_path: Path) -> Optional[ast.AST]:
        """Parse a Python file and return its AST."""
        try:
            if file_path.suffix != ".py":
                return None

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                return ast.parse(content)
        except Exception as exc:  # pragma: no cover - logging
            self.logger.warning("Failed to parse %s: %s", file_path, exc)
            return None

    def extract_functions(self, ast_tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions from an AST."""
        functions: List[Dict[str, Any]] = []
        try:
            for node in ast.walk(ast_tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "lineno": node.lineno,
                        "end_lineno": getattr(node, "end_lineno", node.lineno),
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [
                            d.id for d in node.decorator_list if hasattr(d, "id")
                        ],
                        "body_lines": len(node.body),
                        "docstring": ast.get_docstring(node),
                    }
                    functions.append(func_info)
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to extract functions: %s", exc)
        return functions

    def extract_classes(self, ast_tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions from an AST."""
        classes: List[Dict[str, Any]] = []
        try:
            for node in ast.walk(ast_tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "lineno": node.lineno,
                        "end_lineno": getattr(node, "end_lineno", node.lineno),
                        "bases": [
                            base.id for base in node.bases if hasattr(base, "id")
                        ],
                        "methods": len(
                            [n for n in node.body if isinstance(n, ast.FunctionDef)]
                        ),
                        "docstring": ast.get_docstring(node),
                    }
                    classes.append(class_info)
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to extract classes: %s", exc)
        return classes

    def extract_imports(self, ast_tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import statements from an AST."""
        imports: List[Dict[str, Any]] = []
        try:
            for node in ast.walk(ast_tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(
                            {
                                "type": "import",
                                "module": alias.name,
                                "alias": alias.asname,
                                "lineno": node.lineno,
                            }
                        )
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports.append(
                            {
                                "type": "from_import",
                                "module": node.module,
                                "name": alias.name,
                                "alias": alias.asname,
                                "lineno": node.lineno,
                            }
                        )
        except Exception as exc:  # pragma: no cover - logging
            self.logger.error("Failed to extract imports: %s", exc)
        return imports
