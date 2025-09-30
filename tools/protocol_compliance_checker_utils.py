#!/usr/bin/env python3
"""
Protocol Compliance Checker Utils
=================================

Utility functions and helper methods for protocol compliance checking.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path

from .protocol_compliance_checker_core import (
    ComplianceIssue,
    ComplianceLevel,
    ComplianceReport,
    ProtocolCategory,
)

logger = logging.getLogger(__name__)


def check_branch_exists(branch_name: str) -> bool:
    """Check if branch exists."""
    try:
        result = subprocess.run(
            ["git", "branch", "--list", branch_name],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def get_current_branch() -> str | None:
    """Get current branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def is_valid_branch_name(branch_name: str) -> bool:
    """Check if branch name follows naming conventions."""
    import re

    patterns = {
        "feature": r"^feat/",
        "bugfix": r"^fix/",
        "hotfix": r"^hotfix/",
        "release": r"^release/",
    }

    for pattern in patterns.values():
        if re.match(pattern, branch_name):
            return True
    return False


def has_uncommitted_changes() -> bool:
    """Check if there are uncommitted changes."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def is_python_file(file_path: str) -> bool:
    """Check if file is a Python file."""
    return file_path.endswith(".py")


def check_file_size_compliance(file_path: str, max_lines: int = 400) -> ComplianceIssue | None:
    """Check file size compliance."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            line_count = len(lines)

            if line_count > max_lines:
                return ComplianceIssue(
                    category=ProtocolCategory.CODE_QUALITY,
                    level=ComplianceLevel.VIOLATION,
                    message=f"File has {line_count} lines, exceeds {max_lines} limit",
                    suggestion=f"Refactor file to reduce line count below {max_lines}",
                    file_path=file_path,
                )
    except Exception as e:
        logger.warning(f"Could not check file size for {file_path}: {e}")
    return None


def check_class_count_compliance(file_path: str, max_classes: int = 5) -> ComplianceIssue | None:
    """Check class count compliance."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            class_count = content.count("class ")

            if class_count > max_classes:
                return ComplianceIssue(
                    category=ProtocolCategory.CODE_QUALITY,
                    level=ComplianceLevel.VIOLATION,
                    message=f"File has {class_count} classes, exceeds {max_classes} limit",
                    suggestion=f"Split file to reduce class count below {max_classes}",
                    file_path=file_path,
                )
    except Exception as e:
        logger.warning(f"Could not check class count for {file_path}: {e}")
    return None


def check_function_count_compliance(file_path: str, max_functions: int = 10) -> ComplianceIssue | None:
    """Check function count compliance."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            function_count = content.count("def ")

            if function_count > max_functions:
                return ComplianceIssue(
                    category=ProtocolCategory.CODE_QUALITY,
                    level=ComplianceLevel.VIOLATION,
                    message=f"File has {function_count} functions, exceeds {max_functions} limit",
                    suggestion=f"Split file to reduce function count below {max_functions}",
                    file_path=file_path,
                )
    except Exception as e:
        logger.warning(f"Could not check function count for {file_path}: {e}")
    return None


def generate_recommendations(issues: list[ComplianceIssue]) -> list[str]:
    """Generate recommendations based on issues."""
    recommendations = []

    critical_count = sum(1 for issue in issues if issue.level == ComplianceLevel.CRITICAL)
    violation_count = sum(1 for issue in issues if issue.level == ComplianceLevel.VIOLATION)

    if critical_count > 0:
        recommendations.append(f"Address {critical_count} critical issues immediately")

    if violation_count > 0:
        recommendations.append(f"Fix {violation_count} violations to improve compliance")

    if not issues:
        recommendations.append("Excellent! No compliance issues found")

    return recommendations


def print_compliance_report(report: ComplianceReport) -> None:
    """Print compliance report to console."""
    print("\n" + "=" * 60)
    print("PROTOCOL COMPLIANCE REPORT")
    print("=" * 60)
    print(f"Timestamp: {report.timestamp}")
    print(f"Project Root: {report.project_root}")
    print(f"Total Issues: {report.total_issues}")
    print(f"Critical: {report.critical_issues}")
    print(f"Violations: {report.violations}")
    print(f"Warnings: {report.warnings}")
    print(f"Compliant Items: {report.compliant_items}")
    print("=" * 60)

    if report.issues:
        print("\nISSUES:")
        for issue in report.issues:
            print(f"\n[{issue.level.value.upper()}] {issue.category.value}")
            print(f"Message: {issue.message}")
            print(f"Suggestion: {issue.suggestion}")
            if issue.file_path:
                print(f"File: {issue.file_path}")
            if issue.line_number:
                print(f"Line: {issue.line_number}")

    if report.recommendations:
        print("\nRECOMMENDATIONS:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"{i}. {rec}")

    print("\n" + "=" * 60)


def format_compliance_report(report: ComplianceReport) -> str:
    """Format compliance report as string."""
    lines = []
    lines.append("=" * 60)
    lines.append("PROTOCOL COMPLIANCE REPORT")
    lines.append("=" * 60)
    lines.append(f"Timestamp: {report.timestamp}")
    lines.append(f"Project Root: {report.project_root}")
    lines.append(f"Total Issues: {report.total_issues}")
    lines.append(f"Critical: {report.critical_issues}")
    lines.append(f"Violations: {report.violations}")
    lines.append(f"Warnings: {report.warnings}")
    lines.append(f"Compliant Items: {report.compliant_items}")
    lines.append("=" * 60)

    if report.issues:
        lines.append("\nISSUES:")
        for issue in report.issues:
            lines.append(f"\n[{issue.level.value.upper()}] {issue.category.value}")
            lines.append(f"Message: {issue.message}")
            lines.append(f"Suggestion: {issue.suggestion}")
            if issue.file_path:
                lines.append(f"File: {issue.file_path}")
            if issue.line_number:
                lines.append(f"Line: {issue.line_number}")

    if report.recommendations:
        lines.append("\nRECOMMENDATIONS:")
        for i, rec in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {rec}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Protocol Compliance Checker")
    parser.add_argument("--check-all", action="store_true", help="Run all compliance checks")
    parser.add_argument("--check-git-workflow", action="store_true", help="Check git workflow compliance")
    parser.add_argument("--check-code-quality", action="store_true", help="Check code quality compliance")
    parser.add_argument("--check-agent-coordination", action="store_true", help="Check agent coordination compliance")
    parser.add_argument("--generate-report", action="store_true", help="Generate compliance report")
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    # Import here to avoid circular imports
    from .protocol_compliance_checker_main import ProtocolComplianceChecker

    checker = ProtocolComplianceChecker()

    if args.check_all or not any([args.check_git_workflow, args.check_code_quality, args.check_agent_coordination]):
        report = checker.run_full_compliance_check()
    else:
        report = checker.generate_compliance_report()

    if args.output:
        with open(args.output, "w") as f:
            f.write(format_compliance_report(report))
        print(f"Report saved to {args.output}")
    else:
        print_compliance_report(report)

    # Exit with error code if critical issues found
    if report.critical_issues > 0:
        sys.exit(1)
