#!/usr/bin/env python3
"""
Language Analyzer Service - Agent Cellphone V2
==============================================

TDD-compliant language analysis service for multiple programming languages.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Any

from .python_analyzer import PythonAnalyzer
from .tree_sitter_analyzer import TreeSitterAnalyzer

logger = logging.getLogger(__name__)


class LanguageAnalyzerService:
    """
    Handles language-specific code analysis for different programming languages.
    Coordinates specialized analyzers for Python, Rust, JavaScript, TypeScript.
    """

    def __init__(self):
        """Initialize language analyzers."""
        self.python_analyzer = PythonAnalyzer()
        self.tree_sitter_analyzer = TreeSitterAnalyzer()

    def analyze_file(self, file_path: Path, source_code: str) -> Dict[str, Any]:
        """
        Analyze source code based on file extension.

        Args:
            file_path: Path to the source file
            source_code: Contents of the source file

        Returns:
            Dict with structure {language, functions, classes, routes, complexity}
        """
        suffix = file_path.suffix.lower()

        if suffix == ".py":
            return self.python_analyzer.analyze(source_code)
        elif suffix == ".rs":
            return self.tree_sitter_analyzer.analyze_rust(source_code)
        elif suffix in [".js", ".ts"]:
            return self.tree_sitter_analyzer.analyze_javascript(source_code)
        else:
            return {
                "language": suffix,
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
            }
