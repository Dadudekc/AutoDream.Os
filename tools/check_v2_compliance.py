#!/usr/bin/env python3
"""
V2 Compliance Checker
====================

Check for V2 compliance violations in the project.

Author: Agent-4 (Captain & Operations Coordinator)
V2 Compliance: ≤400 lines, focused compliance checker
"""

from v2_compliance_checker_core import V2ComplianceChecker


def main():
    """Main function to run V2 compliance check."""
    checker = V2ComplianceChecker()
    violations = checker.check_v2_compliance()
    checker.print_violations()
    print(f"\nTotal violations: {checker.get_total_violations()}")


if __name__ == "__main__":
    main()