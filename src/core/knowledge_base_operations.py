#!/usr/bin/env python3
"""
Knowledge Base Core - Core Operations
=====================================

Core operations for knowledge base system.
Handles validation, guidelines, and simplification suggestions.

V2 Compliance: ≤400 lines, focused core operations module
Author: Agent-6 (Quality Assurance Specialist)
"""

from typing import Any

from .knowledge_base_patterns import KnowledgeBasePatterns
from .knowledge_base_principles import KnowledgeBasePrinciples


class KnowledgeBaseCore:
    """
    Core operations for knowledge base system.

    Handles validation, guidelines, and simplification suggestions.
    """

    def __init__(self):
        """Initialize knowledge base core."""
        self.principles = KnowledgeBasePrinciples()
        self.patterns = KnowledgeBasePatterns()
        self.guidelines = self._load_project_guidelines()

    def _load_project_guidelines(self) -> dict[str, Any]:
        """Load project-specific guidelines."""
        return {
            "file_size_limit": 400,
            "max_classes_per_file": 5,
            "max_functions_per_file": 10,
            "max_parameters_per_function": 5,
            "max_complexity_per_function": 10,
            "max_inheritance_levels": 2,
            "max_enums_per_file": 3,
            "preferred_patterns": ["simple_function", "data_class", "repository", "service_layer"],
            "forbidden_patterns": [
                "god_class",
                "premature_optimization",
                "bare_except",
                "stringly_typed",
                "copy_paste",
            ],
            "required_principles": ["kiss", "yagni", "sr", "error_handling"],
            "code_style": {
                "line_length": 100,
                "use_type_hints": True,
                "use_docstrings": True,
                "naming_convention": "snake_case",
            },
            "testing_requirements": {
                "coverage_threshold": 85,
                "unit_tests_required": True,
                "integration_tests_required": True,
                "mock_external_dependencies": True,
            },
            "documentation_requirements": {
                "docstrings_required": True,
                "type_hints_required": True,
                "examples_in_docstrings": True,
                "api_documentation": True,
            },
            "performance_guidelines": {
                "profile_before_optimize": True,
                "avoid_premature_optimization": True,
                "measure_performance": True,
                "optimize_bottlenecks_only": True,
            },
            "security_guidelines": {
                "validate_all_inputs": True,
                "use_parameterized_queries": True,
                "handle_errors_gracefully": True,
                "log_security_events": True,
            },
        }

    def validate_code_against_principles(self, code_analysis: dict[str, Any]) -> dict[str, Any]:
        """Validate code against design principles."""
        violations = []
        recommendations = []

        # Check file size
        if code_analysis.get("line_count", 0) > self.guidelines["file_size_limit"]:
            violations.append(
                {
                    "principle": "kiss",
                    "violation": f"File too large: {code_analysis['line_count']} lines",
                    "severity": "critical",
                }
            )

        # Check class count
        if code_analysis.get("class_count", 0) > self.guidelines["max_classes_per_file"]:
            violations.append(
                {
                    "principle": "sr",
                    "violation": f"Too many classes: {code_analysis['class_count']}",
                    "severity": "high",
                }
            )

        # Check function count
        if code_analysis.get("function_count", 0) > self.guidelines["max_functions_per_file"]:
            violations.append(
                {
                    "principle": "sr",
                    "violation": f"Too many functions: {code_analysis['function_count']}",
                    "severity": "high",
                }
            )

        # Check complexity
        max_complexity = max(code_analysis.get("function_complexities", [0]))
        if max_complexity > self.guidelines["max_complexity_per_function"]:
            violations.append(
                {
                    "principle": "kiss",
                    "violation": f"Function too complex: {max_complexity}",
                    "severity": "high",
                }
            )

        return {
            "violations": violations,
            "recommendations": recommendations,
            "score": self._calculate_compliance_score(violations),
        }

    def _calculate_compliance_score(self, violations: list[dict[str, Any]]) -> int:
        """Calculate compliance score based on violations."""
        if not violations:
            return 100

        critical_count = sum(1 for v in violations if v.get("severity") == "critical")
        high_count = sum(1 for v in violations if v.get("severity") == "high")
        medium_count = sum(1 for v in violations if v.get("severity") == "medium")

        # Penalty calculation
        penalty = (critical_count * 20) + (high_count * 10) + (medium_count * 5)
        score = max(0, 100 - penalty)

        return score

    def get_guideline(self, guideline_name: str) -> Any:
        """Get a specific guideline by name."""
        return self.guidelines.get(guideline_name)

    def get_all_guidelines(self) -> dict[str, Any]:
        """Get all guidelines."""
        return self.guidelines.copy()

    def suggest_simplification(self, code_analysis: dict[str, Any]) -> list[str]:
        """Suggest simplifications based on code analysis."""
        suggestions = []

        # File size suggestions
        if code_analysis.get("line_count", 0) > self.guidelines["file_size_limit"]:
            suggestions.append("Split large file into smaller, focused modules")

        # Class count suggestions
        if code_analysis.get("class_count", 0) > self.guidelines["max_classes_per_file"]:
            suggestions.append("Extract classes into separate files")

        # Function count suggestions
        if code_analysis.get("function_count", 0) > self.guidelines["max_functions_per_file"]:
            suggestions.append("Extract functions into separate modules")

        # Complexity suggestions
        max_complexity = max(code_analysis.get("function_complexities", [0]))
        if max_complexity > self.guidelines["max_complexity_per_function"]:
            suggestions.append("Break down complex functions into smaller ones")

        # Parameter count suggestions
        max_params = max(code_analysis.get("function_parameters", [0]))
        if max_params > self.guidelines["max_parameters_per_function"]:
            suggestions.append("Reduce function parameters using data classes")

        # Inheritance suggestions
        max_inheritance = max(code_analysis.get("inheritance_levels", [0]))
        if max_inheritance > self.guidelines["max_inheritance_levels"]:
            suggestions.append("Use composition instead of deep inheritance")

        # Pattern suggestions
        if code_analysis.get("has_god_class", False):
            suggestions.append("Split god class into smaller, focused classes")

        if code_analysis.get("has_bare_except", False):
            suggestions.append("Use specific exception types instead of bare except")

        if code_analysis.get("has_stringly_typed", False):
            suggestions.append("Use enums or proper types instead of magic strings")

        return suggestions


__all__ = ["KnowledgeBaseCore"]

