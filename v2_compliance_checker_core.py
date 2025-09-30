#!/usr/bin/env python3
"""
V2 Compliance Checker Core
=========================

Core functionality for checking V2 compliance violations.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused compliance checker
"""

from pathlib import Path
from typing import List, Dict


class V2ComplianceChecker:
    """Core V2 compliance checking functionality."""

    def __init__(self):
        """Initialize the compliance checker."""
        self.violations: List[Dict] = []

    def check_v2_compliance(self) -> List[Dict]:
        """Check for V2 compliance violations."""
        self.violations = []

        for py_file in Path(".").rglob("*.py"):
            # Skip test files and __pycache__ directories
            if any(x in str(py_file) for x in ["test", "__pycache__", ".git"]):
                continue

            try:
                with open(py_file, encoding="utf-8") as f:
                    lines = f.readlines()
                    line_count = len(lines)

                    if line_count > 400:
                        self.violations.append(
                            {
                                "file": str(py_file),
                                "lines": line_count,
                                "excess": line_count - 400
                            }
                        )
            except Exception as e:
                print(f"Error reading {py_file}: {e}")
                continue

        return self.violations

    def print_violations(self):
        """Print violations in a formatted way."""
        print("V2 Compliance Violations:")
        print("=" * 50)

        if self.violations:
            for violation in self.violations:
                print(
                    f"  {violation['file']}: {violation['lines']} lines "
                    f"({violation['excess']} over limit)"
                )
        else:
            print("  ✅ No V2 compliance violations found!")

    def get_total_violations(self) -> int:
        """Get total number of violations."""
        return len(self.violations)
