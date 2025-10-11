#!/usr/bin/env python3
"""
V2 Checker CLI - Command Line Interface
========================================

CLI interface for V2 compliance checker.
Extracted from v2_compliance_checker.py for V2 compliance.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import argparse
import sys
from pathlib import Path

try:
    from .v2_compliance_checker import V2ComplianceChecker
except ImportError:
    from v2_compliance_checker import V2ComplianceChecker


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(description="V2 Compliance Checker - Automated Quality Gate")
    parser.add_argument(
        "path", nargs="?", default=".", help="Path to scan (default: current directory)"
    )
    parser.add_argument(
        "--pattern", default="**/*.py", help="File pattern to scan (default: **/*.py)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--fail-on-major",
        action="store_true",
        help="Exit with error code if major violations found",
    )
    parser.add_argument(
        "--fail-on-critical",
        action="store_true",
        help="Exit with error code if critical violations found",
    )
    parser.add_argument(
        "--suggest",
        "-s",
        action="store_true",
        help="Show refactoring suggestions for violations (requires refactoring_suggestion_engine.py)",
    )
    parser.add_argument(
        "--complexity",
        "-c",
        action="store_true",
        help="Show complexity analysis for files (requires complexity_analyzer.py)",
    )

    args = parser.parse_args()

    checker = V2ComplianceChecker(args.path)
    report = checker.scan_directory(Path(args.path), args.pattern)

    print(
        checker.format_report(
            report, args.verbose, show_suggestions=args.suggest, show_complexity=args.complexity
        )
    )

    # Exit with error code if violations found
    if args.fail_on_critical and report.critical_violations:
        sys.exit(1)
    if args.fail_on_major and report.major_violations:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
