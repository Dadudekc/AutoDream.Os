"""
Vibe Check Analyzers - Core analysis logic for vibe check.
"""

import ast

from .design_authority import DecisionSeverity
from .vibe_check_models import VibeViolation


class VibeAnalyzer:
    """Core analysis logic for vibe check."""

    def __init__(self, violation_thresholds: dict[str, int]):
        self.violation_thresholds = violation_thresholds

    def check_complexity(self, file_path: str, tree: ast.AST) -> list[VibeViolation]:
        """Check cyclomatic complexity of functions."""
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > self.violation_thresholds["complexity_score"]:
                    violations.append(
                        VibeViolation(
                            file_path=file_path,
                            line_number=node.lineno,
                            violation_type="high_complexity",
                            description=f"Function '{node.name}' has complexity {complexity} (max: {self.violation_thresholds['complexity_score']})",
                            severity=DecisionSeverity.ERROR,
                            suggestion="Break down into smaller functions or simplify logic",
                        )
                    )

        return violations

    def check_function_length(
        self, file_path: str, content: str, tree: ast.AST
    ) -> list[VibeViolation]:
        """Check function length in lines."""
        violations = []
        lines = content.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_start = node.lineno - 1
                func_end = node.end_lineno or func_start + 1
                func_length = func_end - func_start

                if func_length > self.violation_thresholds["function_length"]:
                    violations.append(
                        VibeViolation(
                            file_path=file_path,
                            line_number=node.lineno,
                            violation_type="long_function",
                            description=f"Function '{node.name}' has {func_length} lines (max: {self.violation_thresholds['function_length']})",
                            severity=DecisionSeverity.ERROR,
                            suggestion="Break into smaller functions",
                            code_snippet=lines[func_start:func_end][:3]
                            if len(lines) > func_start
                            else "",
                        )
                    )

        return violations

    def check_nesting_depth(
        self, file_path: str, content: str, tree: ast.AST
    ) -> list[VibeViolation]:
        """Check maximum nesting depth."""
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                max_depth = self._calculate_nesting_depth(node)
                if max_depth > self.violation_thresholds["nesting_depth"]:
                    violations.append(
                        VibeViolation(
                            file_path=file_path,
                            line_number=node.lineno,
                            violation_type="deep_nesting",
                            description=f"{node.__class__.__name__} '{node.name}' has nesting depth {max_depth} (max: {self.violation_thresholds['nesting_depth']})",
                            severity=DecisionSeverity.ERROR,
                            suggestion="Use early returns or extract nested logic",
                        )
                    )

        return violations

    def check_parameter_count(self, file_path: str, tree: ast.AST) -> list[VibeViolation]:
        """Check function parameter count."""
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                arg_count = len(node.args.args)
                if arg_count > self.violation_thresholds["parameter_count"]:
                    violations.append(
                        VibeViolation(
                            file_path=file_path,
                            line_number=node.lineno,
                            violation_type="too_many_parameters",
                            description=f"Function '{node.name}' has {arg_count} parameters (max: {self.violation_thresholds['parameter_count']})",
                            severity=DecisionSeverity.WARNING,
                            suggestion="Consider using a dataclass or dictionary for parameters",
                        )
                    )

        return violations

    def check_file_length(self, file_path: str, content: str) -> list[VibeViolation]:
        """Check total file length."""
        violations = []
        lines = len(content.split("\n"))

        if lines > self.violation_thresholds["file_length"]:
            violations.append(
                VibeViolation(
                    file_path=file_path,
                    line_number=0,
                    violation_type="long_file",
                    description=f"File has {lines} lines (max: {self.violation_thresholds['file_length']})",
                    severity=DecisionSeverity.ERROR,
                    suggestion="Split into smaller modules",
                )
            )

        return violations

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1

        return complexity

    def _calculate_nesting_depth(self, node: ast.AST) -> int:
        """Calculate maximum nesting depth in a function or class."""
        max_depth = 0
        current_depth = 0

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.Try)):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                current_depth = 0

        return max_depth
