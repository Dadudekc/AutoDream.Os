#!/usr/bin/env python3
"""
Project Analyzer - File Analysis Module
========================================

Handles analysis of individual files across multiple languages.
Part of comprehensive_project_analyzer.py refactoring (623→<400L).

Author: Agent-2 - Architecture & Design Specialist
Pattern: Facade + Module Splitting (CONSOLIDATION_ARCHITECTURE_PATTERNS.md)
"""

import ast
import os
import re
from pathlib import Path
from typing import Any


class FileAnalyzer:
    """Analyzes individual files for various languages."""

    def analyze_python_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a Python file with comprehensive metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            functions = []
            classes = {}
            imports = []
            decorators = []
            docstrings = []
            complexity_indicators = 0
            lines = content.splitlines()

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    complexity_indicators += 1
                    # Count nested structures
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                            complexity_indicators += 1
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes[node.name] = {
                        "methods": methods,
                        "line_count": len(node.body),
                        "base_classes": [
                            base.id for base in node.bases if isinstance(base, ast.Name)
                        ],
                    }
                    complexity_indicators += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        module = node.module or ""
                        imports.extend([f"{module}.{alias.name}" for alias in node.names])
                elif isinstance(node, ast.Decorator):
                    if isinstance(node.decorator, ast.Name):
                        decorators.append(node.decorator.id)
                elif (
                    isinstance(node, ast.Expr)
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                ):
                    if node.value.value.strip().startswith(('"""', "'''")):
                        docstrings.append(node.value.value.strip())

            non_empty_lines = [line for line in lines if line.strip()]
            comment_lines = [line for line in lines if line.strip().startswith("#")]

            return {
                "language": ".py",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "decorators": decorators,
                "docstrings": len(docstrings),
                "line_count": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "comment_lines": len(comment_lines),
                "complexity": complexity_indicators,
                "file_size": os.path.getsize(file_path),
                "import_count": len(imports),
                "function_count": len(functions),
                "class_count": len(classes),
                "has_main": "__main__" in content,
                "has_tests": any(
                    keyword in content.lower() for keyword in ["test", "pytest", "unittest"]
                ),
                "has_async": "async" in content,
                "has_type_hints": ":" in content and "->" in content,
            }
        except Exception as e:
            return self._get_error_result(".py", str(e))

    def analyze_js_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a JavaScript file with enhanced metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            functions = re.findall(r"function\s+(\w+)\s*\(", content)
            classes = re.findall(r"class\s+(\w+)", content)
            imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content)
            exports = re.findall(
                r"export\s+(?:default\s+)?(?:function\s+(\w+)|const\s+(\w+)|class\s+(\w+))", content
            )
            async_functions = re.findall(r"async\s+function\s+(\w+)", content)
            arrow_functions = re.findall(r"const\s+(\w+)\s*=\s*\([^)]*\)\s*=>", content)

            lines = content.splitlines()
            non_empty_lines = [line for line in lines if line.strip()]
            comment_lines = [line for line in lines if line.strip().startswith(("//", "/*", "*"))]

            return {
                "language": ".js",
                "functions": functions,
                "classes": {cls: {"methods": []} for cls in classes},
                "imports": imports,
                "exports": [exp for exp in exports if exp],
                "async_functions": async_functions,
                "arrow_functions": arrow_functions,
                "line_count": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "comment_lines": len(comment_lines),
                "complexity": len(functions) + len(classes),
                "file_size": os.path.getsize(file_path),
                "import_count": len(imports),
                "function_count": len(functions),
                "class_count": len(classes),
                "has_async": len(async_functions) > 0,
                "has_arrow_functions": len(arrow_functions) > 0,
                "has_es6": "=>" in content or "class " in content,
                "has_jquery": "$" in content,
                "has_react": "React" in content or "useState" in content,
            }
        except Exception as e:
            return self._get_error_result(".js", str(e))

    def analyze_md_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a Markdown file with comprehensive metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            headers = re.findall(r"^#+\s+(.+)$", content, re.MULTILINE)
            code_blocks = re.findall(r"```(\w+)?\n(.*?)```", content, re.DOTALL)
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)
            tables = re.findall(r"\|.*\|", content)

            lines = content.splitlines()
            non_empty_lines = [line for line in lines if line.strip()]

            return {
                "language": ".md",
                "functions": [],
                "classes": {},
                "headers": headers,
                "code_blocks": len(code_blocks),
                "links": len(links),
                "images": len(images),
                "tables": len(tables),
                "line_count": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "complexity": len(headers),
                "file_size": os.path.getsize(file_path),
                "header_count": len(headers),
                "has_toc": "Table of Contents" in content or "## Contents" in content,
                "has_code": len(code_blocks) > 0,
                "has_images": len(images) > 0,
                "has_links": len(links) > 0,
            }
        except Exception as e:
            return self._get_error_result(".md", str(e))

    def analyze_yaml_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a YAML file with comprehensive metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            keys = [
                line.split(":")[0].strip()
                for line in lines
                if ":" in line and not line.startswith("#")
            ]
            comments = [line for line in lines if line.strip().startswith("#")]
            non_empty_lines = [line for line in lines if line.strip()]

            return {
                "language": ".yaml",
                "functions": [],
                "classes": {},
                "keys": keys,
                "line_count": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "comment_lines": len(comments),
                "complexity": len(keys),
                "file_size": os.path.getsize(file_path),
                "key_count": len(keys),
                "has_anchors": "&" in content,
                "has_aliases": "*" in content,
                "has_multiline": "|-" in content or "|+" in content,
            }
        except Exception as e:
            return self._get_error_result(".yaml", str(e))

    def analyze_file(self, file_path: str) -> dict[str, Any]:
        """Dispatch to appropriate analyzer based on file extension."""
        ext = Path(file_path).suffix.lower()

        if ext == ".py":
            return self.analyze_python_file(file_path)
        elif ext in [".js", ".jsx"]:
            return self.analyze_js_file(file_path)
        elif ext == ".md":
            return self.analyze_md_file(file_path)
        elif ext in [".yaml", ".yml"]:
            return self.analyze_yaml_file(file_path)
        else:
            return {
                "language": ext,
                "functions": [],
                "classes": {},
                "line_count": 0,
                "complexity": 0,
            }

    def _get_error_result(self, language: str, error: str) -> dict[str, Any]:
        """Return standardized error result."""
        return {
            "language": language,
            "functions": [],
            "classes": {},
            "imports": [],
            "line_count": 0,
            "non_empty_lines": 0,
            "comment_lines": 0,
            "complexity": 0,
            "file_size": 0,
            "error": error,
        }
