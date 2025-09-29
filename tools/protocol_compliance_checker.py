#!/usr/bin/env python3
"""
Protocol Compliance Checker
===========================

Tool to verify compliance with Agent Protocol System standards.
Checks git workflow, code quality, documentation, and agent coordination protocols.

Agent-3: Infrastructure & DevOps Specialist
Mission: V3 Infrastructure Deployment
"""

import argparse
import json
import logging
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

logger = logging.getLogger(__name__)


class ComplianceLevel(Enum):
    """Compliance level."""

    COMPLIANT = "compliant"
    WARNING = "warning"
    VIOLATION = "violation"
    CRITICAL = "critical"


class ProtocolCategory(Enum):
    """Protocol category."""

    GIT_WORKFLOW = "git_workflow"
    CODE_QUALITY = "code_quality"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    AGENT_COORDINATION = "agent_coordination"
    BRANCH_STRATEGY = "branch_strategy"


@dataclass
class ComplianceIssue:
    """Compliance issue."""

    category: ProtocolCategory
    level: ComplianceLevel
    message: str
    file_path: str | None = None
    line_number: int | None = None
    suggestion: str | None = None


@dataclass
class ComplianceReport:
    """Compliance report."""

    timestamp: str
    total_issues: int
    critical_issues: int
    violations: int
    warnings: int
    compliant_items: int
    issues: list[ComplianceIssue]
    recommendations: list[str]


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
        if not self._branch_exists("develop"):
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.GIT_WORKFLOW,
                    level=ComplianceLevel.CRITICAL,
                    message="Missing develop branch - required for proper integration flow",
                    suggestion="Create develop branch: git checkout -b develop && git push origin develop",
                )
            )

        # Check current branch naming
        current_branch = self._get_current_branch()
        if current_branch and not self._is_valid_branch_name(current_branch):
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.BRANCH_STRATEGY,
                    level=ComplianceLevel.VIOLATION,
                    message=f"Invalid branch name: {current_branch}",
                    suggestion="Use proper naming: feat/feature-name, fix/issue-description, etc.",
                )
            )

        # Check for uncommitted changes
        if self._has_uncommitted_changes():
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.GIT_WORKFLOW,
                    level=ComplianceLevel.WARNING,
                    message="Uncommitted changes detected",
                    suggestion="Commit or stash changes before creating PR",
                )
            )

    def check_code_quality_compliance(self, file_paths: list[str]) -> None:
        """Check code quality compliance."""
        logger.info("Checking code quality compliance...")

        for file_path in file_paths:
            if not Path(file_path).exists():
                continue

            # Check file size
            if self._is_python_file(file_path):
                self._check_file_size_compliance(file_path)
                self._check_class_count_compliance(file_path)
                self._check_function_count_compliance(file_path)

    def check_documentation_compliance(self) -> None:
        """Check documentation compliance."""
        logger.info("Checking documentation compliance...")

        required_docs = [
            "README.md",
            "CHANGELOG.md",
            "docs/AGENT_PROTOCOL_SYSTEM.md",
            "docs/AGENT_PROTOCOL_QUICK_REFERENCE.md",
        ]

        for doc_path in required_docs:
            if not Path(doc_path).exists():
                self.issues.append(
                    ComplianceIssue(
                        category=ProtocolCategory.DOCUMENTATION,
                        level=ComplianceLevel.VIOLATION,
                        message=f"Missing required documentation: {doc_path}",
                        suggestion=f"Create {doc_path} following documentation protocol",
                    )
                )

    def check_agent_coordination_compliance(self) -> None:
        """Check agent coordination compliance."""
        logger.info("Checking agent coordination compliance...")

        # Check agent workspace structure
        agent_workspaces = Path("agent_workspaces")
        if not agent_workspaces.exists():
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.AGENT_COORDINATION,
                    level=ComplianceLevel.CRITICAL,
                    message="Missing agent_workspaces directory",
                    suggestion="Create agent workspace structure for team coordination",
                )
            )
            return

        # Check agent status files
        for agent_dir in agent_workspaces.iterdir():
            if agent_dir.is_dir():
                status_file = agent_dir / "status.json"
                if not status_file.exists():
                    self.issues.append(
                        ComplianceIssue(
                            category=ProtocolCategory.AGENT_COORDINATION,
                            level=ComplianceLevel.WARNING,
                            message=f"Missing status.json for {agent_dir.name}",
                            suggestion="Create status.json following agent coordination protocol",
                        )
                    )

    def check_testing_compliance(self) -> None:
        """Check testing compliance."""
        logger.info("Checking testing compliance...")

        # Check if tests directory exists
        if not Path("tests").exists():
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.TESTING,
                    level=ComplianceLevel.VIOLATION,
                    message="Missing tests directory",
                    suggestion="Create tests directory and add unit tests",
                )
            )

        # Check for test files
        test_files = list(Path("tests").glob("test_*.py")) if Path("tests").exists() else []
        if len(test_files) == 0:
            self.issues.append(
                ComplianceIssue(
                    category=ProtocolCategory.TESTING,
                    level=ComplianceLevel.WARNING,
                    message="No test files found",
                    suggestion="Add unit tests for all new features",
                )
            )

    def generate_compliance_report(self) -> ComplianceReport:
        """Generate compliance report."""
        logger.info("Generating compliance report...")

        # Count issues by level
        critical_issues = len([i for i in self.issues if i.level == ComplianceLevel.CRITICAL])
        violations = len([i for i in self.issues if i.level == ComplianceLevel.VIOLATION])
        warnings = len([i for i in self.issues if i.level == ComplianceLevel.WARNING])
        compliant_items = len([i for i in self.issues if i.level == ComplianceLevel.COMPLIANT])

        # Generate recommendations
        self._generate_recommendations()

        return ComplianceReport(
            timestamp=datetime.now().isoformat(),
            total_issues=len(self.issues),
            critical_issues=critical_issues,
            violations=violations,
            warnings=warnings,
            compliant_items=compliant_items,
            issues=self.issues,
            recommendations=self.recommendations,
        )

    def run_full_compliance_check(self) -> ComplianceReport:
        """Run full compliance check."""
        logger.info("Running full protocol compliance check...")

        # Check all protocol categories
        self.check_git_workflow_compliance()
        self.check_documentation_compliance()
        self.check_agent_coordination_compliance()
        self.check_testing_compliance()

        # Check code quality for Python files
        python_files = list(Path("src").glob("**/*.py")) if Path("src").exists() else []
        if python_files:
            self.check_code_quality_compliance([str(f) for f in python_files])

        return self.generate_compliance_report()

    # Helper methods
    def _branch_exists(self, branch_name: str) -> bool:
        """Check if branch exists."""
        try:
            import subprocess

            result = subprocess.run(
                ["git", "branch", "-a"], capture_output=True, text=True, cwd=self.project_root
            )
            return branch_name in result.stdout
        except Exception:
            return False

    def _get_current_branch(self) -> str | None:
        """Get current branch name."""
        try:
            import subprocess

            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            return result.stdout.strip() if result.stdout.strip() else None
        except Exception:
            return None

    def _is_valid_branch_name(self, branch_name: str) -> bool:
        """Check if branch name follows protocol."""
        import re

        # Check against all patterns
        for pattern in self.branch_patterns.values():
            if re.match(pattern, branch_name):
                return True

        # Allow main, develop, and no-verify-pushes
        allowed_branches = ["main", "develop", "no-verify-pushes"]
        return branch_name in allowed_branches

    def _has_uncommitted_changes(self) -> bool:
        """Check for uncommitted changes."""
        try:
            import subprocess

            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            return bool(result.stdout.strip())
        except Exception:
            return False

    def _is_python_file(self, file_path: str) -> bool:
        """Check if file is Python file."""
        return file_path.endswith(".py")

    def _check_file_size_compliance(self, file_path: str) -> None:
        """Check file size compliance."""
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()

            if len(lines) > self.v2_limits["max_file_lines"]:
                self.issues.append(
                    ComplianceIssue(
                        category=ProtocolCategory.CODE_QUALITY,
                        level=ComplianceLevel.VIOLATION,
                        message=f"File {file_path} exceeds {self.v2_limits['max_file_lines']} lines ({len(lines)} lines)",
                        file_path=file_path,
                        suggestion=f"Refactor file to stay under {self.v2_limits['max_file_lines']} lines",
                    )
                )
        except Exception as e:
            logger.error(f"Error checking file size for {file_path}: {e}")

    def _check_class_count_compliance(self, file_path: str) -> None:
        """Check class count compliance."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Simple class count (look for class definitions)
            import re

            class_count = len(re.findall(r"^class\s+\w+", content, re.MULTILINE))

            if class_count > self.v2_limits["max_classes_per_file"]:
                self.issues.append(
                    ComplianceIssue(
                        category=ProtocolCategory.CODE_QUALITY,
                        level=ComplianceLevel.VIOLATION,
                        message=f"File {file_path} has {class_count} classes (limit: {self.v2_limits['max_classes_per_file']})",
                        file_path=file_path,
                        suggestion="Split classes into separate files",
                    )
                )
        except Exception as e:
            logger.error(f"Error checking class count for {file_path}: {e}")

    def _check_function_count_compliance(self, file_path: str) -> None:
        """Check function count compliance."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Simple function count (look for function definitions)
            import re

            function_count = len(re.findall(r"^def\s+\w+", content, re.MULTILINE))

            if function_count > self.v2_limits["max_functions_per_file"]:
                self.issues.append(
                    ComplianceIssue(
                        category=ProtocolCategory.CODE_QUALITY,
                        level=ComplianceLevel.VIOLATION,
                        message=f"File {file_path} has {function_count} functions (limit: {self.v2_limits['max_functions_per_file']})",
                        file_path=file_path,
                        suggestion="Split functions into separate files or modules",
                    )
                )
        except Exception as e:
            logger.error(f"Error checking function count for {file_path}: {e}")

    def _generate_recommendations(self) -> None:
        """Generate recommendations based on issues."""
        if not self.issues:
            self.recommendations.append("✅ All protocol compliance checks passed!")
            return

        # Group recommendations by category
        categories = set(issue.category for issue in self.issues)

        for category in categories:
            category_issues = [i for i in self.issues if i.category == category]
            critical_count = len(
                [i for i in category_issues if i.level == ComplianceLevel.CRITICAL]
            )

            if critical_count > 0:
                self.recommendations.append(
                    f"🚨 CRITICAL: Fix {critical_count} critical issues in {category.value}"
                )
            elif len(category_issues) > 0:
                self.recommendations.append(
                    f"⚠️ Address {len(category_issues)} issues in {category.value}"
                )

        # General recommendations
        if any(i.level == ComplianceLevel.CRITICAL for i in self.issues):
            self.recommendations.append("🚨 CRITICAL: Fix critical issues before proceeding")

        if any(i.category == ProtocolCategory.GIT_WORKFLOW for i in self.issues):
            self.recommendations.append("📋 Review git workflow compliance")

        if any(i.category == ProtocolCategory.CODE_QUALITY for i in self.issues):
            self.recommendations.append("🔧 Review V2 compliance standards")


def main():
    """Main function for Protocol Compliance Checker."""
    parser = argparse.ArgumentParser(description="Protocol Compliance Checker")
    parser.add_argument(
        "--category",
        choices=["all", "git", "code", "docs", "agent", "testing"],
        default="all",
        help="Compliance category to check",
    )
    parser.add_argument(
        "--output", choices=["console", "json", "file"], default="console", help="Output format"
    )
    parser.add_argument(
        "--output-file", default="compliance_report.json", help="Output file for JSON/file output"
    )

    args = parser.parse_args()

    checker = ProtocolComplianceChecker()

    if args.category == "all":
        report = checker.run_full_compliance_check()
    else:
        # Run specific category checks
        if args.category == "git":
            checker.check_git_workflow_compliance()
        elif args.category == "code":
            python_files = list(Path("src").glob("**/*.py")) if Path("src").exists() else []
            checker.check_code_quality_compliance([str(f) for f in python_files])
        elif args.category == "docs":
            checker.check_documentation_compliance()
        elif args.category == "agent":
            checker.check_agent_coordination_compliance()
        elif args.category == "testing":
            checker.check_testing_compliance()

        report = checker.generate_compliance_report()

    # Output results
    if args.output == "console":
        print_compliance_report(report)
    elif args.output == "json":
        with open(args.output_file, "w") as f:
            json.dump(asdict(report), f, indent=2)
        print(f"Compliance report saved to {args.output_file}")
    elif args.output == "file":
        with open(args.output_file, "w") as f:
            f.write(format_compliance_report(report))
        print(f"Compliance report saved to {args.output_file}")


def print_compliance_report(report: ComplianceReport) -> None:
    """Print compliance report to console."""
    print("=" * 80)
    print("🔍 PROTOCOL COMPLIANCE REPORT")
    print("=" * 80)
    print(f"📅 Timestamp: {report.timestamp}")
    print(f"📊 Total Issues: {report.total_issues}")
    print(f"🚨 Critical: {report.critical_issues}")
    print(f"❌ Violations: {report.violations}")
    print(f"⚠️ Warnings: {report.warnings}")
    print(f"✅ Compliant: {report.compliant_items}")
    print()

    if report.issues:
        print("📋 ISSUES FOUND:")
        print("-" * 40)

        for issue in report.issues:
            level_emoji = {
                ComplianceLevel.CRITICAL: "🚨",
                ComplianceLevel.VIOLATION: "❌",
                ComplianceLevel.WARNING: "⚠️",
                ComplianceLevel.COMPLIANT: "✅",
            }

            print(f"{level_emoji[issue.level]} [{issue.category.value.upper()}] {issue.message}")
            if issue.file_path:
                print(f"   📁 File: {issue.file_path}")
            if issue.line_number:
                print(f"   📍 Line: {issue.line_number}")
            if issue.suggestion:
                print(f"   💡 Suggestion: {issue.suggestion}")
            print()

    if report.recommendations:
        print("🎯 RECOMMENDATIONS:")
        print("-" * 40)
        for rec in report.recommendations:
            print(f"• {rec}")
        print()

    # Overall status
    if report.critical_issues > 0:
        print("🚨 STATUS: CRITICAL ISSUES - IMMEDIATE ACTION REQUIRED")
    elif report.violations > 0:
        print("❌ STATUS: VIOLATIONS FOUND - FIX BEFORE PROCEEDING")
    elif report.warnings > 0:
        print("⚠️ STATUS: WARNINGS - REVIEW AND ADDRESS")
    else:
        print("✅ STATUS: FULLY COMPLIANT - EXCELLENT WORK!")


def format_compliance_report(report: ComplianceReport) -> str:
    """Format compliance report as text."""
    output = []
    output.append("=" * 80)
    output.append("🔍 PROTOCOL COMPLIANCE REPORT")
    output.append("=" * 80)
    output.append(f"📅 Timestamp: {report.timestamp}")
    output.append(f"📊 Total Issues: {report.total_issues}")
    output.append(f"🚨 Critical: {report.critical_issues}")
    output.append(f"❌ Violations: {report.violations}")
    output.append(f"⚠️ Warnings: {report.warnings}")
    output.append(f"✅ Compliant: {report.compliant_items}")
    output.append("")

    if report.issues:
        output.append("📋 ISSUES FOUND:")
        output.append("-" * 40)

        for issue in report.issues:
            level_emoji = {
                ComplianceLevel.CRITICAL: "🚨",
                ComplianceLevel.VIOLATION: "❌",
                ComplianceLevel.WARNING: "⚠️",
                ComplianceLevel.COMPLIANT: "✅",
            }

            output.append(
                f"{level_emoji[issue.level]} [{issue.category.value.upper()}] {issue.message}"
            )
            if issue.file_path:
                output.append(f"   📁 File: {issue.file_path}")
            if issue.line_number:
                output.append(f"   📍 Line: {issue.line_number}")
            if issue.suggestion:
                output.append(f"   💡 Suggestion: {issue.suggestion}")
            output.append("")

    if report.recommendations:
        output.append("🎯 RECOMMENDATIONS:")
        output.append("-" * 40)
        for rec in report.recommendations:
            output.append(f"• {rec}")
        output.append("")

    # Overall status
    if report.critical_issues > 0:
        output.append("🚨 STATUS: CRITICAL ISSUES - IMMEDIATE ACTION REQUIRED")
    elif report.violations > 0:
        output.append("❌ STATUS: VIOLATIONS FOUND - FIX BEFORE PROCEEDING")
    elif report.warnings > 0:
        output.append("⚠️ STATUS: WARNINGS - REVIEW AND ADDRESS")
    else:
        output.append("✅ STATUS: FULLY COMPLIANT - EXCELLENT WORK!")

    return "\n".join(output)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
