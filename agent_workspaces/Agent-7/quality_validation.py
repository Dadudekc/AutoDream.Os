#!/usr/bin/env python3
"""Quality validation orchestrator."""

import sys

from data_loader import get_project_root
from reporting import print_report
from validation_rules import QualityValidator


def main() -> None:
    """Entry point for running the quality validation suite."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Quality Validation Script - Agent-7 (Quality Assurance Manager)")
        print("\nUsage: python quality_validation.py [--help]")
        print(
            "\nThis script runs comprehensive quality validation for the V2 workspace."
        )
        print(
            "It checks code quality, testing quality, integration quality, and quality standards compliance."
        )
        return

    project_root = get_project_root()
    validator = QualityValidator(project_root)
    report = validator.run_comprehensive_validation()
    print_report(report)

    if report.failed_checks > 0:
        sys.exit(1)
    elif report.warning_checks > 0:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
