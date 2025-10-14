#!/usr/bin/env python3
"""
Architecture Pattern Validator

Validates Python files against V2 architectural patterns and best practices.
Helps agents quickly assess code quality and identify refactoring opportunities.

Usage:
    python tools/arch_pattern_validator.py <file_path>
    python tools/arch_pattern_validator.py <file_path> --detailed
    python tools/arch_pattern_validator.py <directory> --recursive

Author: Agent-2 - Architecture & Design Specialist
Created: 2025-10-11
Purpose: Automated V2 compliance and pattern detection
"""

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    """Results from validating a single file."""

    file_path: str
    line_count: int
    v2_compliant: bool
    patterns_found: list[str]
    issues: list[str]
    recommendations: list[str]
    complexity_score: int
    quality_score: float


class ArchitectureValidator:
    """Validates code against V2 architectural patterns."""

    # V2 Compliance limits
    MAX_LINES_COMPLIANT = 400
    MAX_LINES_MAJOR_VIOLATION = 600
    MAX_FUNCTION_LINES = 30
    MAX_CLASS_LINES = 200

    def __init__(self, detailed: bool = False):
        self.detailed = detailed

    def validate_file(self, file_path: str) -> ValidationResult:
        """Validate a single Python file."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.suffix == ".py":
            raise ValueError(f"Not a Python file: {file_path}")

        # Read file
        with open(path, encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()

        line_count = len(lines)
        issues = []
        patterns_found = []
        recommendations = []

        # Parse AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return ValidationResult(
                file_path=str(path),
                line_count=line_count,
                v2_compliant=False,
                patterns_found=[],
                issues=[f"Syntax error: {e}"],
                recommendations=[],
                complexity_score=0,
                quality_score=0.0,
            )

        # V2 Compliance Check
        v2_compliant = line_count <= self.MAX_LINES_COMPLIANT
        if not v2_compliant:
            if line_count <= self.MAX_LINES_MAJOR_VIOLATION:
                issues.append(
                    f"MAJOR VIOLATION: {line_count} lines " f"(limit: {self.MAX_LINES_COMPLIANT})"
                )
            else:
                issues.append(
                    f"CRITICAL VIOLATION: {line_count} lines "
                    f"(limit: {self.MAX_LINES_COMPLIANT})"
                )
            recommendations.append("Consider splitting into smaller modules")

        # Analyze patterns
        self._analyze_patterns(tree, lines, patterns_found, issues, recommendations)

        # Calculate complexity score
        complexity_score = self._calculate_complexity(tree)

        # Calculate quality score
        quality_score = self._calculate_quality_score(
            v2_compliant, len(patterns_found), len(issues), complexity_score
        )

        return ValidationResult(
            file_path=str(path),
            line_count=line_count,
            v2_compliant=v2_compliant,
            patterns_found=patterns_found,
            issues=issues,
            recommendations=recommendations,
            complexity_score=complexity_score,
            quality_score=quality_score,
        )

    def _analyze_patterns(
        self,
        tree: ast.AST,
        lines: list[str],
        patterns: list[str],
        issues: list[str],
        recommendations: list[str],
    ):
        """Analyze code for architectural patterns."""

        # Check for repository pattern
        if self._has_repository_pattern(tree):
            patterns.append("Repository Pattern")

        # Check for service layer
        if self._has_service_pattern(tree):
            patterns.append("Service Layer")

        # Check for dependency injection
        if self._has_dependency_injection(tree):
            patterns.append("Dependency Injection")

        # Check for error handling
        if self._has_error_handling(tree):
            patterns.append("Error Handling")
        else:
            issues.append("Missing error handling (no try/except blocks)")
            recommendations.append("Add error handling for robustness")

        # Check for logging
        if self._has_logging(tree):
            patterns.append("Logging")
        else:
            recommendations.append("Consider adding logging for debugging")

        # Check for type hints
        if self._has_type_hints(tree):
            patterns.append("Type Hints")
        else:
            recommendations.append("Add type hints for better code clarity")

        # Check for docstrings
        if self._has_docstrings(tree):
            patterns.append("Documentation (Docstrings)")
        else:
            issues.append("Missing docstrings")
            recommendations.append("Add docstrings for public functions/classes")

        # Check function/class sizes
        self._check_function_sizes(tree, issues, recommendations)
        self._check_class_sizes(tree, lines, issues, recommendations)

    def _has_repository_pattern(self, tree: ast.AST) -> bool:
        """Check if code uses repository pattern."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if "repository" in node.name.lower() or "repo" in node.name.lower():
                    return True
        return False

    def _has_service_pattern(self, tree: ast.AST) -> bool:
        """Check if code uses service layer pattern."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if "service" in node.name.lower():
                    return True
        return False

    def _has_dependency_injection(self, tree: ast.AST) -> bool:
        """Check for dependency injection usage."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "__init__" and len(node.args.args) > 1:
                    return True
        return False

    def _has_error_handling(self, tree: ast.AST) -> bool:
        """Check for error handling."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                return True
        return False

    def _has_logging(self, tree: ast.AST) -> bool:
        """Check for logging usage."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "logging" in alias.name:
                        return True
            if isinstance(node, ast.ImportFrom):
                if node.module and "logging" in node.module:
                    return True
        return False

    def _has_type_hints(self, tree: ast.AST) -> bool:
        """Check for type hints."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.returns or any(arg.annotation for arg in node.args.args):
                    return True
        return False

    def _has_docstrings(self, tree: ast.AST) -> bool:
        """Check for docstrings."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node):
                    return True
        return False

    def _check_function_sizes(self, tree: ast.AST, issues: list[str], recommendations: list[str]):
        """Check function sizes against V2 limits."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno + 1
                if func_lines > self.MAX_FUNCTION_LINES:
                    issues.append(
                        f"Function '{node.name}' too long: "
                        f"{func_lines} lines (limit: {self.MAX_FUNCTION_LINES})"
                    )
                    recommendations.append(f"Refactor '{node.name}' into smaller functions")

    def _check_class_sizes(
        self, tree: ast.AST, lines: list[str], issues: list[str], recommendations: list[str]
    ):
        """Check class sizes against V2 limits."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_lines = node.end_lineno - node.lineno + 1
                if class_lines > self.MAX_CLASS_LINES:
                    issues.append(
                        f"Class '{node.name}' too long: "
                        f"{class_lines} lines (limit: {self.MAX_CLASS_LINES})"
                    )
                    recommendations.append(f"Refactor '{node.name}' into smaller classes")

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            # Add complexity for control flow
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += len(node.handlers)
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity

    def _calculate_quality_score(
        self, v2_compliant: bool, patterns_count: int, issues_count: int, complexity: int
    ) -> float:
        """Calculate overall quality score (0-10)."""
        score = 10.0

        # V2 compliance
        if not v2_compliant:
            score -= 2.0

        # Patterns (positive)
        score += min(patterns_count * 0.5, 2.0)

        # Issues (negative)
        score -= min(issues_count * 0.5, 3.0)

        # Complexity (negative if too high)
        if complexity > 20:
            score -= 2.0
        elif complexity > 10:
            score -= 1.0

        return max(0.0, min(10.0, score))

    def print_result(self, result: ValidationResult):
        """Print validation results."""
        print(f"\n{'='*70}")
        print(f"🔍 Architecture Validation: {result.file_path}")
        print(f"{'='*70}")

        # V2 Compliance
        status = "✅ COMPLIANT" if result.v2_compliant else "❌ NOT COMPLIANT"
        print(f"\n📏 V2 Compliance: {status}")
        print(f"   Lines: {result.line_count} (limit: {self.MAX_LINES_COMPLIANT})")

        # Quality Score
        print(f"\n⭐ Quality Score: {result.quality_score:.1f}/10.0")
        print(f"   Complexity: {result.complexity_score}")

        # Patterns Found
        if result.patterns_found:
            print(f"\n✨ Patterns Found ({len(result.patterns_found)}):")
            for pattern in result.patterns_found:
                print(f"   ✅ {pattern}")

        # Issues
        if result.issues:
            print(f"\n⚠️  Issues Found ({len(result.issues)}):")
            for issue in result.issues:
                print(f"   ❌ {issue}")

        # Recommendations
        if result.recommendations:
            print(f"\n💡 Recommendations ({len(result.recommendations)}):")
            for rec in result.recommendations:
                print(f"   • {rec}")

        print(f"\n{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate Python files against V2 architectural patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single file
  python tools/arch_pattern_validator.py src/services/messaging_cli.py
  
  # Validate with detailed output
  python tools/arch_pattern_validator.py src/services/messaging_cli.py --detailed
  
  # Validate all Python files in directory
  python tools/arch_pattern_validator.py src/services/ --recursive
        """,
    )

    parser.add_argument("path", type=str, help="File or directory to validate")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed analysis")
    parser.add_argument(
        "--recursive", "-r", action="store_true", help="Recursively validate directory"
    )

    args = parser.parse_args()

    validator = ArchitectureValidator(detailed=args.detailed)
    path = Path(args.path)

    if path.is_file():
        # Validate single file
        result = validator.validate_file(str(path))
        validator.print_result(result)
        return 0 if result.v2_compliant else 1

    elif path.is_dir():
        # Validate directory
        if args.recursive:
            py_files = list(path.rglob("*.py"))
        else:
            py_files = list(path.glob("*.py"))

        if not py_files:
            print(f"No Python files found in {path}")
            return 1

        print(f"\n🔍 Validating {len(py_files)} Python files in {path}")

        results = []
        for py_file in py_files:
            try:
                result = validator.validate_file(str(py_file))
                results.append(result)
                if args.detailed:
                    validator.print_result(result)
            except Exception as e:
                print(f"❌ Error validating {py_file}: {e}")

        # Summary
        compliant = sum(1 for r in results if r.v2_compliant)
        avg_quality = sum(r.quality_score for r in results) / len(results)

        print(f"\n{'='*70}")
        print("📊 SUMMARY")
        print(f"{'='*70}")
        print(f"Total Files: {len(results)}")
        print(f"V2 Compliant: {compliant}/{len(results)} " f"({compliant/len(results)*100:.1f}%)")
        print(f"Average Quality Score: {avg_quality:.1f}/10.0")
        print(f"{'='*70}\n")

        print("🐝 WE. ARE. SWARM. ⚡")

        return 0 if compliant == len(results) else 1

    else:
        print(f"❌ Error: Path not found: {path}")
        return 1


if __name__ == "__main__":
    exit(main())
