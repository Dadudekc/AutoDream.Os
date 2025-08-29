#!/usr/bin/env python3
"""
File Analysis Utilities - Agent Cellphone V2
============================================

Utility functions for file analysis operations.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import ast
import re

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, List


class FileAnalysisUtils:
    """Utility class for file analysis operations."""

    @staticmethod
    def extract_python_imports(content: str) -> List[Dict[str, str]]:
        """Extract import statements from Python code."""
        imports = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(
                            {
                                "type": "import",
                                "module": alias.name,
                                "name": alias.asname or alias.name,
                            }
                        )
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(
                            {
                                "type": "from_import",
                                "module": module,
                                "name": f"{module}.{alias.name}"
                                if module
                                else alias.name,
                            }
                        )
        except Exception:
            pass
        return imports

    @staticmethod
    def extract_work_items(content: str) -> List[Dict[str, Any]]:
        """Extract TODO, FIXME, BUG comments from code."""
        work_items = []
        patterns = {
            "TODO": r"#\s*TODO:?\s*(.+)",
            "FIXME": r"#\s*FIXME:?\s*(.+)",
            "BUG": r"#\s*BUG:?\s*(.+)",
        }
        for line_num, line in enumerate(content.splitlines(), 1):
            for item_type, pattern in patterns.items():
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    work_items.append(
                        {
                            "type": item_type,
                            "line": line_num,
                            "description": match.group(1).strip(),
                        }
                    )
        return work_items

    @staticmethod
    def get_file_type(file_path) -> str:
        """Determine file type from extension."""
        suffix = file_path.suffix.lower()
        type_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".rs": "rust",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".h": "header",
        }
        return type_map.get(suffix, "text")

    @staticmethod
    def calculate_complexity_level(complexity_score: float) -> str:
        """Calculate complexity level from score."""
        if complexity_score <= 5:
            return "low"
        elif complexity_score <= 10:
            return "medium"
        elif complexity_score <= 20:
            return "high"
        else:
            return "very_high"

    @staticmethod
    def get_file_stats_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get comprehensive statistics for multiple files."""
        stats = {
            "total_files": len(results),
            "total_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "file_types": {},
            "work_items_count": 0,
        }

        for result in results:
            if "error" not in result:
                stats["total_lines"] += result.get("lines_count", 0)
                stats["total_functions"] += result.get("functions_count", 0)
                stats["total_classes"] += result.get("classes_count", 0)

                file_type = result.get("file_type", "unknown")
                stats["file_types"][file_type] = (
                    stats["file_types"].get(file_type, 0) + 1
                )

                stats["work_items_count"] += len(result.get("work_items", []))

        return stats
