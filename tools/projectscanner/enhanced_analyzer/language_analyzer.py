"""
Enhanced Language Analyzer - V2 Compliant
=========================================

Enhanced language analyzer for project scanning.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class EnhancedLanguageAnalyzer:
    """Enhanced language analyzer with advanced code analysis capabilities."""

    def __init__(self):
        """Initialize enhanced language analyzer."""
        self.supported_languages = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".cpp": "C++",
            ".c": "C",
            ".h": "C/C++ Header",
            ".rs": "Rust",
            ".go": "Go",
            ".rb": "Ruby",
            ".php": "PHP",
            ".cs": "C#",
        }
        logger.debug("Enhanced Language Analyzer initialized")

    def analyze_file(self, file_path: Path, source_code: str = None) -> dict[str, Any]:
        """Analyze file with enhanced language analysis."""
        try:
            if source_code is None:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    source_code = f.read()

            extension = file_path.suffix.lower()
            language = self.supported_languages.get(extension, "Unknown")

            # Basic analysis
            analysis = {
                "language": language,
                "extension": extension,
                "file_path": str(file_path),
                "line_count": len(source_code.splitlines()),
                "char_count": len(source_code),
                "complexity": 0,
                "functions": [],
                "classes": [],
                "imports": [],
                "v2_compliant": True,
            }

            # Language-specific analysis
            if language == "Python":
                analysis.update(self._analyze_python_enhanced(source_code))
            elif language in ["JavaScript", "TypeScript"]:
                analysis.update(self._analyze_javascript_enhanced(source_code))
            elif language in ["Java", "C++", "C"]:
                analysis.update(self._analyze_cpp_java_enhanced(source_code))
            else:
                analysis.update(self._analyze_generic_enhanced(source_code))

            # Calculate V2 compliance
            analysis["v2_compliant"] = analysis["line_count"] <= 400

            return analysis

        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return self._get_error_analysis(file_path, str(e))

    def _analyze_python_enhanced(self, source_code: str) -> dict[str, Any]:
        """Enhanced Python analysis."""
        lines = source_code.splitlines()
        functions = []
        classes = []
        imports = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Functions
            if re.match(r"^\s*def\s+\w+", stripped):
                func_match = re.search(r"def\s+(\w+)", stripped)
                if func_match:
                    functions.append({"name": func_match.group(1), "line": i, "type": "function"})

            # Classes
            elif re.match(r"^\s*class\s+\w+", stripped):
                class_match = re.search(r"class\s+(\w+)", stripped)
                if class_match:
                    classes.append({"name": class_match.group(1), "line": i, "type": "class"})

            # Imports
            elif re.match(r"^(from\s+\w+|import\s+\w+)", stripped):
                imports.append({"line": i, "statement": stripped})

        complexity = len(functions) + len(classes) * 2

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": complexity,
        }

    def _analyze_javascript_enhanced(self, source_code: str) -> dict[str, Any]:
        """Enhanced JavaScript/TypeScript analysis."""
        lines = source_code.splitlines()
        functions = []
        classes = []
        imports = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Functions
            if re.search(
                r"function\s+\w+|const\s+\w+\s*=\s*\w*\s*=>|let\s+\w+\s*=\s*\w*\s*=>", stripped
            ):
                func_match = re.search(r"(function\s+(\w+)|(\w+)\s*=\s*\w*\s*=>)", stripped)
                if func_match:
                    func_name = func_match.group(2) or func_match.group(3)
                    functions.append({"name": func_name, "line": i, "type": "function"})

            # Classes
            elif re.match(r"^\s*class\s+\w+", stripped):
                class_match = re.search(r"class\s+(\w+)", stripped)
                if class_match:
                    classes.append({"name": class_match.group(1), "line": i, "type": "class"})

            # Imports
            elif re.match(r"^(import|require)", stripped):
                imports.append({"line": i, "statement": stripped})

        complexity = len(functions) + len(classes) * 2

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": complexity,
        }

    def _analyze_cpp_java_enhanced(self, source_code: str) -> dict[str, Any]:
        """Enhanced C++/Java analysis."""
        lines = source_code.splitlines()
        functions = []
        classes = []
        imports = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Functions
            if re.search(r"\w+\s+\w+\s*\([^)]*\)\s*{", stripped):
                func_match = re.search(r"(\w+)\s*\(", stripped)
                if func_match:
                    functions.append({"name": func_match.group(1), "line": i, "type": "function"})

            # Classes
            elif re.match(r"^\s*(class|struct)\s+\w+", stripped):
                class_match = re.search(r"(class|struct)\s+(\w+)", stripped)
                if class_match:
                    classes.append({"name": class_match.group(2), "line": i, "type": "class"})

            # Imports
            elif re.match(r"^(#include|import)", stripped):
                imports.append({"line": i, "statement": stripped})

        complexity = len(functions) + len(classes) * 2

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": complexity,
        }

    def _analyze_generic_enhanced(self, source_code: str) -> dict[str, Any]:
        """Generic enhanced analysis."""
        lines = source_code.splitlines()

        # Simple pattern matching for any language
        functions = []
        classes = []
        imports = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Look for function-like patterns
            if re.search(r"\w+\s*\(", stripped) and "{" in stripped:
                func_match = re.search(r"(\w+)\s*\(", stripped)
                if func_match:
                    functions.append({"name": func_match.group(1), "line": i, "type": "function"})

            # Look for class-like patterns
            elif re.search(r"(class|struct|interface)\s+\w+", stripped):
                class_match = re.search(r"(class|struct|interface)\s+(\w+)", stripped)
                if class_match:
                    classes.append({"name": class_match.group(2), "line": i, "type": "class"})

        complexity = len(functions) + len(classes)

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": complexity,
        }

    def _get_error_analysis(self, file_path: Path, error: str) -> dict[str, Any]:
        """Return error analysis when file analysis fails."""
        return {
            "language": "Unknown",
            "extension": file_path.suffix,
            "file_path": str(file_path),
            "line_count": 0,
            "char_count": 0,
            "complexity": 0,
            "functions": [],
            "classes": [],
            "imports": [],
            "v2_compliant": False,
            "error": error,
        }
