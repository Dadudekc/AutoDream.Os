"""
Python Analyzer - V2 Compliant
==============================

Specialized Python code analyzer.
V2 Compliance: ≤150 lines, single responsibility, KISS principle.
"""

import ast
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PythonAnalyzer:
    """Specialized Python code analyzer with AST parsing."""

    def __init__(self):
        """Initialize Python analyzer."""
        logger.debug("Python Analyzer initialized")

    def analyze_python_file(self, file_path: Path, source_code: str) -> dict[str, Any]:
        """Analyze Python file using AST parsing."""
        try:
            tree = ast.parse(source_code)
            analysis = {
                "language": "Python",
                "extension": ".py",
                "file_path": str(file_path),
                "line_count": len(source_code.splitlines()),
                "char_count": len(source_code),
                "functions": [],
                "classes": [],
                "imports": [],
                "decorators": [],
                "complexity": 0,
                "v2_compliant": True,
            }

            # Analyze AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "args": len(node.args.args),
                            "decorators": [
                                d.id if hasattr(d, "id") else str(d) for d in node.decorator_list
                            ],
                            "type": "function",
                        }
                    )
                elif isinstance(node, ast.AsyncFunctionDef):
                    analysis["functions"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "args": len(node.args.args),
                            "decorators": [
                                d.id if hasattr(d, "id") else str(d) for d in node.decorator_list
                            ],
                            "type": "async_function",
                        }
                    )
                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "bases": [b.id if hasattr(b, "id") else str(b) for b in node.bases],
                            "methods": len(
                                [
                                    n
                                    for n in node.body
                                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                                ]
                            ),
                            "decorators": [
                                d.id if hasattr(d, "id") else str(d) for d in node.decorator_list
                            ],
                        }
                    )
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(
                                {
                                    "line": node.lineno,
                                    "type": "import",
                                    "module": alias.name,
                                    "alias": alias.asname,
                                }
                            )
                    else:  # ImportFrom
                        for alias in node.names:
                            analysis["imports"].append(
                                {
                                    "line": node.lineno,
                                    "type": "from_import",
                                    "module": node.module or "",
                                    "name": alias.name,
                                    "alias": alias.asname,
                                }
                            )

            # Calculate complexity (functions + classes + decorators)
            analysis["complexity"] = (
                len(analysis["functions"]) + len(analysis["classes"]) + len(analysis["decorators"])
            )

            # Check V2 compliance
            analysis["v2_compliant"] = analysis["line_count"] <= 400

            return analysis

        except SyntaxError as e:
            logger.warning(f"Syntax error in {file_path}: {e}")
            return self._get_error_analysis(file_path, f"Syntax error: {e}")
        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return self._get_error_analysis(file_path, str(e))

    def get_python_metrics(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Extract Python-specific metrics from analysis."""
        return {
            "total_functions": len(analysis.get("functions", [])),
            "total_classes": len(analysis.get("classes", [])),
            "total_imports": len(analysis.get("imports", [])),
            "async_functions": len(
                [f for f in analysis.get("functions", []) if f.get("type") == "async_function"]
            ),
            "decorated_functions": len(
                [f for f in analysis.get("functions", []) if f.get("decorators")]
            ),
            "inherited_classes": len([c for c in analysis.get("classes", []) if c.get("bases")]),
            "average_function_args": self._calculate_average_args(analysis.get("functions", [])),
            "average_class_methods": self._calculate_average_methods(analysis.get("classes", [])),
        }

    def _calculate_average_args(self, functions: list[dict[str, Any]]) -> float:
        """Calculate average number of function arguments."""
        if not functions:
            return 0.0
        total_args = sum(func.get("args", 0) for func in functions)
        return total_args / len(functions)

    def _calculate_average_methods(self, classes: list[dict[str, Any]]) -> float:
        """Calculate average number of class methods."""
        if not classes:
            return 0.0
        total_methods = sum(cls.get("methods", 0) for cls in classes)
        return total_methods / len(classes)

    def _get_error_analysis(self, file_path: Path, error: str) -> dict[str, Any]:
        """Return error analysis when file analysis fails."""
        return {
            "language": "Python",
            "extension": ".py",
            "file_path": str(file_path),
            "line_count": 0,
            "char_count": 0,
            "functions": [],
            "classes": [],
            "imports": [],
            "decorators": [],
            "complexity": 0,
            "v2_compliant": False,
            "error": error,
        }
