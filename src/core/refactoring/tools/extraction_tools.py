"""
Refactoring Extraction Tools - V2 Compliance Module
==================================================

Extraction functionality for refactoring tools.

V2 Compliance: < 300 lines, single responsibility, extraction tools.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import ast
from typing import List, Dict, Any
from dataclasses import dataclass

from ...unified_import_system import get_unified_import_system

# Keywords and messages used across extraction methods (SSOT)
MODEL_KEYWORDS = ("model", "data", "entity")
UTIL_KEYWORDS = ("util", "helper")
NO_MODELS = "# No models found\n"
NO_UTILS = "# No utilities found\n"
NO_CORE = "# No core logic found\n"

__all__ = [
    "ExtractionPlan",
    "ExtractionTools",
    "MODEL_KEYWORDS",
    "UTIL_KEYWORDS",
    "NO_MODELS",
    "NO_UTILS",
    "NO_CORE",
]


@dataclass
class ExtractionPlan:
    """Plan for extracting code from a file."""

    source_file: str
    target_files: List[str]
    extraction_rules: List[str]
    estimated_impact: str
    v2_compliance_target: bool


class ExtractionTools:
    """Extraction tools for refactoring."""

    def __init__(self):
        """Initialize extraction tools."""
        self.unified_imports = get_unified_import_system()

    def create_extraction_plan(self, file_path: str) -> ExtractionPlan:
        """Create an extraction plan for a file."""
        try:
            # Analyze file structure
            source_path = self.unified_imports.Path(file_path)
            source_content = source_path.read_text(encoding="utf-8")
            tree = ast.parse(source_content)

            # Determine extraction targets
            target_files = self._determine_target_files(file_path)
            extraction_rules = self._generate_extraction_rules(tree)

            return ExtractionPlan(
                source_file=file_path,
                target_files=target_files,
                extraction_rules=extraction_rules,
                estimated_impact="Moderate",
                v2_compliance_target=True,
            )
        except Exception as e:
            return ExtractionPlan(
                source_file=file_path,
                target_files=[],
                extraction_rules=[],
                estimated_impact="Error",
                v2_compliance_target=False,
            )

    def execute_extraction(self, plan: ExtractionPlan) -> bool:
        """Execute extraction plan."""
        try:
            if not plan.target_files:
                return True  # No extraction needed

            source_path = self.unified_imports.Path(plan.source_file)
            source_content = source_path.read_text(encoding="utf-8")
            tree = ast.parse(source_content)

            # Extract different components
            models = self._extract_models(tree)
            utils = self._extract_utils(tree)
            core = self._extract_core(tree)

            # Write extracted files
            for target_file in plan.target_files:
                target_path = self.unified_imports.Path(target_file)
                if "models" in target_file:
                    target_path.write_text(models, encoding="utf-8")
                elif "utils" in target_file:
                    target_path.write_text(utils, encoding="utf-8")
                elif "core" in target_file:
                    target_path.write_text(core, encoding="utf-8")

            return True
        except Exception as e:
            return False

    def _determine_target_files(self, file_path: str) -> List[str]:
        """Determine target files for extraction."""
        base_path = file_path.replace(".py", "")
        return [
            f"{base_path}_models.py",
            f"{base_path}_utils.py",
            f"{base_path}_core.py",
        ]

    def _generate_extraction_rules(self, tree: ast.AST) -> List[str]:
        """Generate extraction rules based on AST analysis."""
        rules = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                rules.append(f"Extract class: {node.name}")
            elif isinstance(node, ast.FunctionDef):
                rules.append(f"Extract function: {node.name}")
            elif isinstance(node, ast.Import):
                rules.append(f"Extract imports: {[alias.name for alias in node.names]}")

        return rules

    def _extract_models(self, tree: ast.AST) -> str:
        """Extract model class definitions from an AST.

        Returns source code for classes whose names include any keyword in
        ``MODEL_KEYWORDS``. Each class definition is separated by two newlines
        and the result ends with a newline. If no classes are found,
        ``NO_MODELS`` is returned.
        """

        models = [
            ast.unparse(node)
            for node in tree.body
            if isinstance(node, ast.ClassDef)
            and any(key in node.name.lower() for key in MODEL_KEYWORDS)
        ]

        return "\n\n".join(models) + ("\n" if models else NO_MODELS)

    def _extract_utils(self, tree: ast.AST) -> str:
        """Extract utility function definitions from an AST.

        Returns source code for functions whose names include any keyword in
        ``UTIL_KEYWORDS``. Each function is separated by two newlines and the
        result ends with a newline. If no functions are found, ``NO_UTILS`` is
        returned.
        """

        utils = [
            ast.unparse(node)
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and any(key in node.name.lower() for key in UTIL_KEYWORDS)
        ]

        return "\n\n".join(utils) + ("\n" if utils else NO_UTILS)

    def _extract_core(self, tree: ast.AST) -> str:
        """Extract core logic from an AST.

        Returns source code for top-level classes and functions not classified
        as models or utilities. Elements are separated by two newlines and the
        result ends with a newline. If no core logic is found, ``NO_CORE`` is
        returned.
        """

        model_names = {
            node.name
            for node in tree.body
            if isinstance(node, ast.ClassDef)
            and any(key in node.name.lower() for key in MODEL_KEYWORDS)
        }
        util_names = {
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and any(key in node.name.lower() for key in UTIL_KEYWORDS)
        }

        core = []
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name in model_names:
                continue
            if isinstance(node, ast.FunctionDef) and node.name in util_names:
                continue
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                core.append(ast.unparse(node))

        return "\n\n".join(core) + ("\n" if core else NO_CORE)
