#!/usr/bin/env python3
"""
Protocol Compliance Checker Main
===============================

Main protocol compliance checker class and CLI interface.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
from datetime import datetime
from pathlib import Path

from .protocol_compliance_checker_core import (
    ComplianceIssue,
    ComplianceLevel,
    ComplianceReport,
    ProtocolCategory,
)
from .protocol_compliance_checker_utils import (
    check_branch_exists,
    check_class_count_compliance,
    check_file_size_compliance,
    check_function_count_compliance,
    format_compliance_report,
    generate_recommendations,
    get_current_branch,
    has_uncommitted_changes,
    is_python_file,
    is_valid_branch_name,
    main,
    print_compliance_report,
)

logger = logging.getLogger(__name__)


class ProtocolComplianceChecker:
    """Protocol Compliance Checker."""

    def __init__(self):
        self.project_root = Path.cwd()
        self.issues: list[ComplianceIssue] = []
        self.recommendations: list[str] = []

        # Protocol standards
        self.v2_limits = {
            "max_file_lines": 400,
            "max_classes_per_file": 5,
            "max_functions_per_file": 10,
            "max_cyclomatic_complexity": 10,
            "max_parameters_per_function": 5,
            "max_inheritance_levels": 2,
        }

        self.branch_patterns = {
            "feature": r"^feat/",
            "bugfix": r"^fix/",
            "hotfix": r"^hotfix/",
            "release": r"^release/",
        }

        self.commit_patterns = {
            "feat": r"^feat:",
            "fix": r"^fix:",
            "docs": r"^docs:",
            "refactor": r"^refactor:",
            "test": r"^test:",
            "chore": r"^chore:",
        }

    def check_git_workflow_compliance(self) -> None:
        """Check git workflow compliance."""
        logger.info("Checking git workflow compliance...")

        # Check if develop branch exists
        if not check_branch_exists("develop"):
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.GIT_WORKFLOW,
                    level=ComplianceLevel.CRITICAL,
                    message="Missing develop branch - required for proper integration flow",
                    suggestion="Create develop branch: git checkout -b develop && git push origin develop",
                )
            )

        # Check current branch naming
        current_branch = get_current_branch()
        if current_branch and current_branch not in ["main", "develop"]:
            if not is_valid_branch_name(current_branch):
                self.issues.append(
                    ComplianceIssue(
                        category=ProtocolCategory.BRANCH_STRATEGY,
                        level=ComplianceLevel.WARNING,
                        message=f"Branch '{current_branch}' doesn't follow naming conventions",
                        suggestion="Use prefixes: feat/, fix/, hotfix/, release/",
                    )
                )

        # Check for uncommitted changes
        if has_uncommitted_changes():
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.GIT_WORKFLOW,
                    level=ComplianceLevel.WARNING,
                    message="Uncommitted changes detected",
                    suggestion="Commit or stash changes before proceeding",
                )
            )

    def check_code_quality_compliance(self, file_paths: list[str]) -> None:
        """Check code quality compliance."""
        logger.info("Checking code quality compliance...")

        for file_path in file_paths:
            if not is_python_file(file_path):
                continue

            # Check file size
            issue = check_file_size_compliance(file_path, self.v2_limits["max_file_lines"])
            if issue:
                self.issues.append(issue)

            # Check class count
            issue = check_class_count_compliance(file_path, self.v2_limits["max_classes_per_file"])
            if issue:
                self.issues.append(issue)

            # Check function count
            issue = check_function_count_compliance(file_path, self.v2_limits["max_functions_per_file"])
            if issue:
                self.issues.append(issue)

    def check_documentation_compliance(self) -> None:
        """Check documentation compliance."""
        logger.info("Checking documentation compliance...")

        required_files = ["README.md", "CHANGELOG.md"]
        for file_name in required_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                self.issues.append(
                    ComplianceIssue(
                        category=ProtocolCategory.DOCUMENTATION,
                        level=ComplianceLevel.WARNING,
                        message=f"Missing {file_name}",
                        suggestion=f"Create {file_name} with project documentation",
                        file_path=str(file_path),
                    )
                )

    def check_agent_coordination_compliance(self) -> None:
        """Check agent coordination compliance."""
        logger.info("Checking agent coordination compliance...")

        # Check for required agent files
        agent_files = [
            "agent_workspaces",
            "src/services/consolidated_messaging_service.py",
        ]

        for file_path in agent_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.issues.append(
                    ComplianceIssue(
                        category=ProtocolCategory.AGENT_COORDINATION,
                        level=ComplianceLevel.CRITICAL,
                        message=f"Missing agent coordination file: {file_path}",
                        suggestion=f"Ensure {file_path} exists for proper agent coordination",
                        file_path=str(full_path),
                    )
                )

    def check_testing_compliance(self) -> None:
        """Check testing compliance."""
        logger.info("Checking testing compliance...")

        # Check for test directory
        test_dirs = ["tests", "test", "src/tests"]
        test_dir_found = False

        for test_dir in test_dirs:
            if (self.project_root / test_dir).exists():
                test_dir_found = True
                break

        if not test_dir_found:
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.TESTING,
                    level=ComplianceLevel.WARNING,
                    message="No test directory found",
                    suggestion="Create tests/ directory with unit tests",
                )
            )

    def generate_compliance_report(self) -> ComplianceReport:
        """Generate compliance report."""
        # Count issues by level
        critical_count = sum(1 for issue in self.issues if issue.level == ComplianceLevel.CRITICAL)
        violation_count = sum(1 for issue in self.issues if issue.level == ComplianceLevel.VIOLATION)
        warning_count = sum(1 for issue in self.issues if issue.level == ComplianceLevel.WARNING)
        compliant_count = sum(1 for issue in self.issues if issue.level == ComplianceLevel.COMPLIANT)

        # Generate recommendations
        self.recommendations = generate_recommendations(self.issues)

        return ComplianceReport(
            timestamp=datetime.now().isoformat(),
            project_root=str(self.project_root),
            total_issues=len(self.issues),
            critical_issues=critical_count,
            violations=violation_count,
            warnings=warning_count,
            compliant_items=compliant_count,
            issues=self.issues,
            recommendations=self.recommendations,
        )

    def run_full_compliance_check(self) -> ComplianceReport:
        """Run full compliance check."""
        logger.info("Running full compliance check...")

        # Clear previous issues
        self.issues = []

        # Run all checks
        self.check_git_workflow_compliance()
        self.check_documentation_compliance()
        self.check_agent_coordination_compliance()
        self.check_testing_compliance()

        # Get Python files for code quality check
        python_files = []
        for py_file in self.project_root.rglob("*.py"):
            python_files.append(str(py_file))

        self.check_code_quality_compliance(python_files)

        return self.generate_compliance_report()


# For direct execution
if __name__ == "__main__":
    main()
