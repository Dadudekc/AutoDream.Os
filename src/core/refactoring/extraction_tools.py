"""
Extraction Tools
===============

Tools for extracting code from files.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import ast
from dataclasses import dataclass
from pathlib import Path

from .extraction_helpers import extract_core, extract_models, extract_utils


@dataclass
class ExtractionPlan:
    """Plan for extracting code from a file."""

    source_file: str
    target_files: list[str]
    extraction_rules: list[str]
    estimated_impact: str
    v2_compliance_target: bool = False


@dataclass
class FileAnalysis:
    """Analysis results for a file."""

    line_count: int
    v2_compliance: bool
    has_models: bool
    has_utils: bool


class ExtractionTools:
    """Tools for code extraction operations."""

    def create_extraction_plan(self, file_path: str) -> ExtractionPlan:
        """Create an extraction plan for a file."""
        analysis = self._analyze_file_for_extraction(file_path)

        if not analysis.v2_compliance:
            # File exceeds V2 compliance limit, needs extraction
            target_files = [
                f"{Path(file_path).stem}_core.py",
                f"{Path(file_path).stem}_models.py",
                f"{Path(file_path).stem}_utils.py",
            ]

            extraction_rules = [
                "Extract data models to separate file",
                "Extract utility functions to separate file",
                "Keep core logic in main file",
                "Ensure each file is under 400 lines",
            ]

            return ExtractionPlan(
                source_file=file_path,
                target_files=target_files,
                extraction_rules=extraction_rules,
                estimated_impact="High - Will achieve V2 compliance",
                v2_compliance_target=True,
            )
        else:
            return ExtractionPlan(
                source_file=file_path,
                target_files=[],
                extraction_rules=[],
                estimated_impact="None - Already V2 compliant",
                v2_compliance_target=False,
            )

    def execute_extraction(self, plan: ExtractionPlan) -> bool:
        """Execute extraction plan."""
        try:
            if not plan.target_files:
                return True  # No extraction needed

            source_path = Path(plan.source_file)
            source_content = source_path.read_text(encoding="utf-8")

            # Parse the source file
            tree = ast.parse(source_content)

            # Extract different components
            models = extract_models(tree)
            utils = extract_utils(tree)
            core = extract_core(tree)

            # Write extracted files
            for target_file in plan.target_files:
                target_path = Path(target_file)
                if "models" in target_file:
                    target_path.write_text(models, encoding="utf-8")
                elif "utils" in target_file:
                    target_path.write_text(utils, encoding="utf-8")
                elif "core" in target_file:
                    target_path.write_text(core, encoding="utf-8")

            return True
        except Exception as e:
            print(f"Extraction failed: {e}")
            return False

    def _analyze_file_for_extraction(self, file_path: str) -> FileAnalysis:
        """Analyze file for extraction opportunities."""
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                return FileAnalysis(
                    line_count=0, v2_compliance=True, has_models=False, has_utils=False
                )

            content = source_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            return FileAnalysis(
                line_count=len(lines),
                v2_compliance=len(lines) < 400,
                has_models="class" in content.lower(),
                has_utils="def" in content.lower(),
            )
        except Exception:
            return FileAnalysis(line_count=0, v2_compliance=True, has_models=False, has_utils=False)
