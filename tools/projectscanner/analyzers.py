"""
Project Scanner Analyzers
========================

Language-specific analyzers for project scanning.
"""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class LanguageAnalyzer:
    """Base language analyzer for project scanning."""

    def __init__(self):
        """Initialize language analyzer."""
        self.supported_extensions = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".h"}
        logger.debug("Initialized LanguageAnalyzer")

    def analyze_file(self, file_path: Path, source_code: str = None) -> dict[str, Any]:
        """Analyze a file and return language-specific information."""
        try:
            if source_code is None:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    source_code = f.read()

            extension = file_path.suffix.lower()

            if extension == ".py":
                return self._analyze_python(file_path, source_code)
            elif extension in {".js", ".ts"}:
                return self._analyze_javascript(file_path, source_code)
            elif extension in {".java", ".cpp", ".c", ".h"}:
                return self._analyze_cpp_java(file_path, source_code)
            else:
                return self._analyze_generic(file_path, source_code)

        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")
            return self._analyze_generic(file_path, "")

    def _analyze_python(self, file_path: Path, source_code: str) -> dict[str, Any]:
        """Analyze Python file."""
        lines = source_code.splitlines()
        line_count = len(lines)

        # Count functions and classes
        functions = []
        classes = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("def ") and "(" in stripped:
                func_name = stripped.split("(")[0].replace("def ", "").strip()
                functions.append({"name": func_name, "line": i + 1})
            elif stripped.startswith("class ") and ":" in stripped:
                class_name = stripped.split(":")[0].replace("class ", "").strip()
                classes.append({"name": class_name, "line": i + 1})

        return {
            "language": "Python",
            "extension": ".py",
            "line_count": line_count,
            "functions": functions,
            "classes": classes,
            "complexity": len(functions) + len(classes),
            "v2_compliant": line_count <= 400,
        }

    def _analyze_javascript(self, file_path: Path, source_code: str) -> dict[str, Any]:
        """Analyze JavaScript/TypeScript file."""
        lines = source_code.splitlines()
        line_count = len(lines)

        # Count functions and classes
        functions = []
        classes = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            if "function " in stripped or "=>" in stripped:
                if "function " in stripped:
                    func_name = stripped.split("(")[0].replace("function ", "").strip()
                    functions.append({"name": func_name, "line": i + 1})
            elif stripped.startswith("class ") and "{" in stripped:
                class_name = stripped.split("{")[0].replace("class ", "").strip()
                classes.append({"name": class_name, "line": i + 1})

        return {
            "language": "JavaScript/TypeScript",
            "extension": file_path.suffix,
            "line_count": line_count,
            "functions": functions,
            "classes": classes,
            "complexity": len(functions) + len(classes),
            "v2_compliant": line_count <= 400,
        }

    def _analyze_cpp_java(self, file_path: Path, source_code: str) -> dict[str, Any]:
        """Analyze C++/Java file."""
        lines = source_code.splitlines()
        line_count = len(lines)

        # Count functions and classes
        functions = []
        classes = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            if "{" in stripped and ("(" in stripped or "class" in stripped):
                if "class " in stripped:
                    class_name = stripped.split("{")[0].replace("class ", "").strip()
                    classes.append({"name": class_name, "line": i + 1})
                elif "(" in stripped and "class" not in stripped:
                    func_name = stripped.split("(")[0].strip().split()[-1]
                    functions.append({"name": func_name, "line": i + 1})

        return {
            "language": "C++/Java",
            "extension": file_path.suffix,
            "line_count": line_count,
            "functions": functions,
            "classes": classes,
            "complexity": len(functions) + len(classes),
            "v2_compliant": line_count <= 400,
        }

    def _analyze_generic(self, file_path: Path, source_code: str) -> dict[str, Any]:
        """Analyze generic file."""
        lines = source_code.splitlines() if source_code else []
        line_count = len(lines)

        return {
            "language": "Generic",
            "extension": file_path.suffix,
            "line_count": line_count,
            "functions": [],
            "classes": [],
            "complexity": 0,
            "v2_compliant": line_count <= 400,
        }
