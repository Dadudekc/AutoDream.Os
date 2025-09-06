#!/usr/bin/env python3
"""
Architecture Analysis Tools Core - V2 Compliance Module
=======================================================

Core analysis functionality for architecture analysis tools.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import os
import hashlib
from typing import List, Dict, Any, Optional, Tuple
import logging

from .analysis_tools_models import (
    ArchitecturePattern,
    FileAnalysis,
    DuplicateFile,
    RefactoringSuggestion,
    AnalysisReport,
)

logger = logging.getLogger(__name__)


class ArchitectureAnalyzer:
    """Simplified architecture analyzer - KISS principle applied."""

    def __init__(self, project_root: str = "."):
        """Initialize analyzer with project root."""
        self.project_root = project_root
        self.analyzed_files = {}

    def analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze a single file - simplified."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Basic analysis
            line_count = len(lines)
            classes = self._extract_classes(content)
            functions = self._extract_functions(content)
            imports = self._extract_imports(content)
            complexity_score = self._calculate_complexity(content)
            v2_compliance = line_count <= 300

            return FileAnalysis(
                file_path=file_path,
                line_count=line_count,
                classes=classes,
                functions=functions,
                imports=imports,
                complexity_score=complexity_score,
                v2_compliance=v2_compliance,
            )
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return FileAnalysis(
                file_path=file_path,
                line_count=0,
                classes=[],
                functions=[],
                imports=[],
                complexity_score=0.0,
                v2_compliance=False,
            )

    def find_duplicates(self, files: List[str]) -> List[DuplicateFile]:
        """Find duplicate files - simplified."""
        duplicates = []
        file_hashes = {}

        for file_path in files:
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                    file_hash = hashlib.sha256(content).hexdigest()

                    if file_hash in file_hashes:
                        # Found duplicate
                        original = file_hashes[file_hash]
                        duplicate = DuplicateFile(
                            original_file=original,
                            duplicate_files=[file_path],
                            similarity_score=1.0,
                        )
                        duplicates.append(duplicate)
                    else:
                        file_hashes[file_hash] = file_path
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")

        return duplicates

    def identify_patterns(self, files: List[str]) -> List[ArchitecturePattern]:
        """Identify architecture patterns - simplified."""
        patterns = []

        # Simple pattern detection
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Check for common patterns
                    if "class" in content and "def __init__" in content:
                        pattern = ArchitecturePattern(
                            name="Class-based Architecture",
                            pattern_type="structural",
                            files=[file_path],
                            confidence=0.8,
                            description="File contains class definitions with constructors",
                        )
                        patterns.append(pattern)

                    if "def " in content and "class" not in content:
                        pattern = ArchitecturePattern(
                            name="Functional Architecture",
                            pattern_type="structural",
                            files=[file_path],
                            confidence=0.7,
                            description="File contains only functions",
                        )
                        patterns.append(pattern)
            except Exception as e:
                logger.error(f"Error analyzing file {file_path}: {e}")

        return patterns

    def generate_suggestions(
        self, file_analysis: FileAnalysis
    ) -> List[RefactoringSuggestion]:
        """Generate refactoring suggestions - simplified."""
        suggestions = []

        if not file_analysis.v2_compliance:
            suggestion = RefactoringSuggestion(
                file_path=file_analysis.file_path,
                suggestion_type="V2 Compliance",
                description=f"File has {file_analysis.line_count} lines, needs refactoring to <300 lines",
                priority="HIGH",
                estimated_effort="MEDIUM",
            )
            suggestions.append(suggestion)

        if file_analysis.complexity_score > 0.7:
            suggestion = RefactoringSuggestion(
                file_path=file_analysis.file_path,
                suggestion_type="Complexity Reduction",
                description="File has high complexity, consider breaking into smaller modules",
                priority="MEDIUM",
                estimated_effort="HIGH",
            )
            suggestions.append(suggestion)

        return suggestions

    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names from content."""
        classes = []
        lines = content.split("\n")
        for line in lines:
            if line.strip().startswith("class "):
                class_name = line.strip().split("(")[0].replace("class ", "").strip()
                classes.append(class_name)
        return classes

    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names from content."""
        functions = []
        lines = content.split("\n")
        for line in lines:
            if line.strip().startswith("def "):
                func_name = line.strip().split("(")[0].replace("def ", "").strip()
                functions.append(func_name)
        return functions

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from content."""
        imports = []
        lines = content.split("\n")
        for line in lines:
            if line.strip().startswith(("import ", "from ")):
                imports.append(line.strip())
        return imports

    def _calculate_complexity(self, content: str) -> float:
        """Calculate simple complexity score."""
        lines = content.split("\n")
        complexity_indicators = ["if ", "for ", "while ", "try:", "except:", "with "]
        complexity_count = 0

        for line in lines:
            for indicator in complexity_indicators:
                if indicator in line:
                    complexity_count += 1

        return min(complexity_count / len(lines), 1.0) if lines else 0.0
