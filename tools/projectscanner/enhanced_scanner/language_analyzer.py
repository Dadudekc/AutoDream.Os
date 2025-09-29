"""
Enhanced Project Scanner Language Analyzer
=========================================

Language analysis coordinator with modular language-specific analyzers.
"""

import logging
import re
from pathlib import Path
from typing import Any

from .python_analyzer import PythonAnalyzer

logger = logging.getLogger(__name__)


class EnhancedLanguageAnalyzer:
    """Enhanced language analyzer coordinator."""

    def __init__(self):
        """Initialize language analyzers."""
        self.python_analyzer = PythonAnalyzer()
        self.analysis_cache = {}

    def analyze_file(self, file_path: Path, source_code: str) -> dict[str, Any]:
        """
        Analyze source code based on file extension with enhanced features.

        Returns:
            Dict with structure {language, functions, classes, routes, complexity, maturity, agent_type}
        """
        suffix = file_path.suffix.lower()

        if suffix == ".py":
            return self.python_analyzer.analyze_python_file(source_code, file_path)
        elif suffix == ".rs":
            return self._analyze_rust_fallback(source_code)
        elif suffix in [".js", ".ts"]:
            return self._analyze_javascript_fallback(source_code)
        else:
            return {
                "language": suffix,
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
                "maturity": "Unknown",
                "agent_type": "Unknown",
            }

    def _analyze_rust_fallback(self, source_code: str) -> dict[str, Any]:
        """Fallback Rust analysis using text patterns."""
        functions = []
        structs = {}

        lines = source_code.splitlines()
        for i, line in enumerate(lines, 1):
            if "fn " in line and not line.strip().startswith("//"):
                # Extract function name
                parts = line.split("fn ")
                if len(parts) > 1:
                    func_part = parts[1].split("(")[0].strip()
                    functions.append({"name": func_part, "line": i})
            elif "struct " in line and not line.strip().startswith("//"):
                parts = line.split("struct ")
                if len(parts) > 1:
                    struct_name = parts[1].split("{")[0].split(" ")[0].strip()
                    structs[struct_name] = {"line": i, "fields": []}

        return {
            "language": ".rs",
            "functions": functions,
            "structs": structs,
            "impls": {},
            "routes": [],
            "complexity": len(functions) + len(structs),
            "file_size": len(lines),
            "maturity": "Core Asset",
            "agent_type": "SystemAgent",
        }

    def _analyze_javascript_fallback(self, source_code: str) -> dict[str, Any]:
        """Fallback JS analysis using text patterns."""
        functions = []
        classes = {}
        routes = []

        lines = source_code.splitlines()
        for i, line in enumerate(lines, 1):
            # Function detection
            if "function " in line:
                parts = line.split("function ")
                if len(parts) > 1:
                    func_name = parts[1].split("(")[0].strip()
                    functions.append({"name": func_name, "line": i})
            # Class detection
            elif "class " in line:
                parts = line.split("class ")
                if len(parts) > 1:
                    class_name = parts[1].split("{")[0].split(" ")[0].strip()
                    classes[class_name] = {"line": i, "methods": []}
            # Route detection (Express.js patterns)
            elif any(
                method in line for method in [".get(", ".post(", ".put(", ".delete(", ".patch("]
            ):
                route_info = self._extract_route_from_line(line)
                if route_info:
                    routes.append(route_info)

        return {
            "language": ".js",
            "functions": functions,
            "classes": classes,
            "routes": routes,
            "complexity": len(functions) + len(classes),
            "file_size": len(lines),
            "maturity": "Prototype",
            "agent_type": "WebAgent",
        }

    def _extract_route_from_line(self, line: str) -> dict[str, str]:
        """Extract route information from a JavaScript line of code."""
        # Pattern for Express.js routes: app.get('/path', ...)
        pattern = r'(\w+)\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]'
        match = re.search(pattern, line)

        if match:
            obj, method, path = match.groups()
            return {
                "object": obj,
                "method": method.upper(),
                "path": path,
                "line": 0,  # Line number not available in fallback
            }
        return {}
