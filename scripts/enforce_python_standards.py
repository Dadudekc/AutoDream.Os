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
    """Enforces Python coding standards including LOC limits."""

    def __init__(self):
        """Initialize the standard enforcer."""
        self.violations = []

    def check_file(self, file_path: str) -> list[Violation]:
        """Check a single file for violations."""
        violations = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content)

            # Check line count
            lines = content.split('\n')
            if len(lines) > 400:
                violations.append(Violation(
                    file_path=file_path,
                    line_number=len(lines),
                    violation_type="FILE_TOO_LONG",
                    message=f"File has {len(lines)} lines, exceeds 400 LOC limit",
                    severity="ERROR"
                ))

            # Check class and function lengths
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_lines = node.end_lineno - node.lineno + 1
                    if class_lines > 100:
                        violations.append(Violation(
                            file_path=file_path,
                            line_number=node.lineno,
                            violation_type="CLASS_TOO_LONG",
                            message=f"Class '{node.name}' has {class_lines} lines, exceeds 100 LOC limit",
                            severity="ERROR"
                        ))

                elif isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno + 1
                    if func_lines > 50:
                        violations.append(Violation(
                            file_path=file_path,
                            line_number=node.lineno,
                            violation_type="FUNCTION_TOO_LONG",
                            message=f"Function '{node.name}' has {func_lines} lines, exceeds 50 LOC limit",
                            severity="ERROR"
                        ))

        except Exception as e:
            violations.append(Violation(
                file_path=file_path,
                line_number=0,
                violation_type="PARSE_ERROR",
                message=f"Failed to parse file: {str(e)}",
                severity="ERROR"
            ))

        return violations


def main():
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(description="Enforce Python coding standards")
    parser.add_argument("--input-file", help="Input file to check")
    parser.add_argument("--output-dir", help="Output directory for results")

    args = parser.parse_args()

    enforcer = PythonStandardEnforcer()

    if args.input_file:
        violations = enforcer.check_file(args.input_file)
        for violation in violations:
            logger.error(f"{violation.file_path}:{violation.line_number} - {violation.message}")
    else:
        logger.info("No input file specified. Use --input-file to check a specific file.")


if __name__ == "__main__":
    main()
