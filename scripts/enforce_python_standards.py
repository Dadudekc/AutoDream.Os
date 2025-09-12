#!/usr/bin/env python3
"""
Dream.OS Python Coding Standard Enforcer
========================================

Enforces Dream.OS Python Coding Standard v1.0 including LOC limits and other quality checks.

LOC Limits:
- File: ≤ 400 LOC
- Class: ≤ 100 LOC
- Function: ≤ 50 LOC

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

import ast
import logging
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class Violation:
    """Represents a coding standard violation."""

    file_path: str
    line_number: int
    violation_type: str
    message: str
    severity: str


class PythonStandardEnforcer:
    """Enforces Dream.OS Python coding standards."""

    def __init__(self):
        self.violations: list[Violation] = []
        self.checked_files = 0

        # LOC limits
        self.max_file_loc = 400
        self.max_class_loc = 100
        self.max_function_loc = 50

    def enforce_standards(self, root_path: str = "src") -> bool:
        """Enforce Python coding standards on all Python files.

        Args:
            root_path: Root path to scan for Python files

        Returns:
            bool: True if no violations found, False otherwise
        """
        logger.info("🎯 Dream.OS Python Coding Standard Enforcer")
        logger.info("=" * 60)
        logger.info(f"📊 Scanning: {root_path}")
        logger.info(
            f"📏 LOC Limits: File ≤ {self.max_file_loc}, Class ≤ {self.max_class_loc}, Function ≤ {self.max_function_loc}"
        )
        logger.info("=" * 60)

        python_files = self._find_python_files(root_path)

        for file_path in python_files:
            self._check_file(file_path)

        self._report_results()
        return len(self.violations) == 0

    def _find_python_files(self, root_path: str) -> list[str]:
        """Find all Python files in the given path."""
        python_files = []
        root = Path(root_path)

        if not root.exists():
            logger.info(f"❌ Root path does not exist: {root_path}")
            return []

        for file_path in root.rglob("*.py"):
            # Skip test files, __pycache__, and venv directories
            if (
                not str(file_path).startswith("__pycache__")
                and not str(file_path).startswith("venv")
                and not str(file_path).startswith(".venv")
                and "test" not in str(file_path).lower()
            ):
                python_files.append(str(file_path))

        return python_files

    def _check_file(self, file_path: str) -> None:
        """Check a single Python file for violations."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")
            self.checked_files += 1

            # Check file-level LOC limit
            if len(lines) > self.max_file_loc:
                self.violations.append(
                    Violation(
                        file_path=file_path,
                        line_number=1,
                        violation_type="file_loc_limit",
                        message=f"File exceeds {self.max_file_loc} LOC limit ({len(lines)} lines)",
                        severity="error",
                    )
                )

            # Parse AST for structural analysis
            try:
                tree = ast.parse(content, filename=file_path)
                self._analyze_ast(tree, file_path, content)
            except SyntaxError as e:
                self.violations.append(
                    Violation(
                        file_path=file_path,
                        line_number=e.lineno or 1,
                        violation_type="syntax_error",
                        message=f"Syntax error: {e.msg}",
                        severity="error",
                    )
                )

            # Check for other violations
            self._check_coding_violations(file_path, content, lines)

        except Exception as e:
            logger.info(f"❌ Error checking file {file_path}: {e}")

    def _analyze_ast(self, tree: ast.AST, file_path: str, content: str) -> None:
        """Analyze AST for structural violations."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_loc = self._get_node_loc(node, content)
                if class_loc > self.max_class_loc:
                    self.violations.append(
                        Violation(
                            file_path=file_path,
                            line_number=node.lineno,
                            violation_type="class_loc_limit",
                            message=f"Class '{node.name}' exceeds {self.max_class_loc} LOC limit ({class_loc} lines)",
                            severity="warning",
                        )
                    )

            elif isinstance(node, ast.FunctionDef):
                func_loc = self._get_node_loc(node, content)
                if func_loc > self.max_function_loc:
                    self.violations.append(
                        Violation(
                            file_path=file_path,
                            line_number=node.lineno,
                            violation_type="function_loc_limit",
                            message=f"Function '{node.name}' exceeds {self.max_function_loc} LOC limit ({func_loc} lines)",
                            severity="warning",
                        )
                    )

    def _get_node_loc(self, node: ast.AST, content: str) -> int:
        """Get lines of code for an AST node."""
        lines = content.split("\n")
        start_line = getattr(node, "lineno", 1) - 1
        end_line = getattr(node, "end_lineno", len(lines))

        # Count non-empty, non-comment lines
        loc = 0
        for i in range(start_line, min(end_line, len(lines))):
            line = lines[i].strip()
            if line and not line.startswith("#"):
                loc += 1

        return loc

    def _check_coding_violations(self, file_path: str, content: str, lines: list[str]) -> None:
        """Check for other coding standard violations."""
        # Check for print statements in non-test files
        if "print(" in content and "test" not in file_path.lower():
            self.violations.append(
                Violation(
                    file_path=file_path,
                    line_number=1,
                    violation_type="print_statement",
                    message="Print statement found in non-test file (use logging instead)",
                    severity="warning",
                )
            )

        # Check for TODO comments without proper formatting
        for i, line in enumerate(lines, 1):
            if "TODO" in line and "TODO:" not in line:
                self.violations.append(
                    Violation(
                        file_path=file_path,
                        line_number=i,
                        violation_type="todo_format",
                        message="TODO comment should be formatted as 'TODO: description'",
                        severity="info",
                    )
                )

        # Check for long lines (> 100 characters)
        for i, line in enumerate(lines, 1):
            if len(line) > 100 and not line.strip().startswith("#"):
                self.violations.append(
                    Violation(
                        file_path=file_path,
                        line_number=i,
                        violation_type="line_length",
                        message=f"Line exceeds 100 characters ({len(line)} chars)",
                        severity="warning",
                    )
                )

    def _report_results(self) -> None:
        """Report enforcement results."""
        logger.info("\n📊 ENFORCEMENT RESULTS")
        logger.info("=" * 60)
        logger.info(f"📁 Files checked: {self.checked_files}")
        logger.info(f"🚨 Violations found: {len(self.violations)}")

        if self.violations:
            logger.info("\n🚨 VIOLATIONS:")
            logger.info("-" * 60)

            # Group violations by type
            violation_counts = {}
            for violation in self.violations:
                violation_type = violation.violation_type
                violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1

            # Show summary by type
            for violation_type, count in violation_counts.items():
                logger.info(f"  {violation_type}: {count}")

            logger.info("\n📋 TOP VIOLATIONS:")
            logger.info("-" * 60)

            # Show first 10 violations
            for i, violation in enumerate(self.violations[:10], 1):
                severity_icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(
                    violation.severity, "❓"
                )

                logger.info(f"{i}. {severity_icon} {violation.file_path}:{violation.line_number}")
                logger.info(f"   {violation.message}")

            if len(self.violations) > 10:
                logger.info(f"   ... and {len(self.violations) - 10} more violations")

            logger.info("\n❌ STANDARD ENFORCEMENT FAILED")
            logger.info("🔧 Fix violations and re-run enforcement")
        else:
            logger.info("\n✅ ALL STANDARDS PASSED!")
            logger.info("🎉 Dream.OS Python Coding Standard v1.0 compliance achieved")
            logger.info("📏 All LOC limits respected, no violations found")

        logger.info("=" * 60)


if __name__ == "__main__":
    enforcer = PythonStandardEnforcer()
    enforcer.enforce_standards()
