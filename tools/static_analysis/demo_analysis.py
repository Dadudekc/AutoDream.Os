#!/usr/bin/env python3
"""
Demo Analysis - Static Analysis Tools Demonstration
==================================================

Demonstration script showing how to use all static analysis tools
with comprehensive reporting and visualization.

Author: Agent-2 (Security & Quality Specialist)
License: MIT
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.static_analysis.analysis_dashboard import AnalysisDashboard
from tools.static_analysis.code_quality_analyzer import CodeQualityAnalyzer
from tools.static_analysis.dependency_scanner import DependencyScanner
from tools.static_analysis.security_scanner import SecurityScanner
from tools.static_analysis.static_analysis_runner import StaticAnalysisRunner

logger = logging.getLogger(__name__)


class DemoAnalysis:
    """Demonstration of static analysis tools."""

    def __init__(self, project_root: str = "."):
        """Initialize demo analysis."""
        self.project_root = Path(project_root).resolve()
        self.runner = StaticAnalysisRunner(str(self.project_root))
        self.dashboard = AnalysisDashboard(str(self.project_root))

    def run_demo(self) -> None:
        """Run complete demonstration."""
        print("🚀 Static Analysis Tools Demonstration")
        print("=" * 50)

        # Step 1: Run comprehensive analysis
        print("\n📊 Step 1: Running Comprehensive Analysis...")
        results = self.runner.run_full_analysis()

        # Step 2: Generate reports
        print("\n📄 Step 2: Generating Reports...")
        reports = self.runner.generate_reports()

        # Step 3: Display dashboard
        print("\n🎯 Step 3: Displaying Analysis Dashboard...")
        self.dashboard.load_and_display_reports()

        # Step 4: Generate HTML report
        print("\n🌐 Step 4: Generating HTML Dashboard...")
        html_file = self.dashboard.generate_html_report()

        # Step 5: Show summary
        print("\n📋 Step 5: Analysis Summary...")
        self._show_summary(results, reports, html_file)

    def _show_summary(
        self, results: dict[str, Any], reports: dict[str, str], html_file: str
    ) -> None:
        """Show analysis summary."""
        summary = results["summary"]

        print(f"\n🎯 Overall Status: {summary['overall_status']}")
        print(f"🔒 Security Status: {summary['security_status']}")
        print(f"🔍 Quality Status: {summary['quality_status']}")
        print(f"📦 Total Issues: {summary['total_issues']}")
        print(f"🚨 Critical Issues: {summary['critical_issues']}")

        print("\n📄 Generated Reports:")
        for report_type, report_path in reports.items():
            print(f"  {report_type.title()}: {report_path}")
        print(f"  HTML Dashboard: {html_file}")

        if summary["recommendations"]:
            print("\n📋 Recommendations:")
            for rec in summary["recommendations"]:
                print(f"  {rec}")

        if summary["next_steps"]:
            print("\n🎯 Next Steps:")
            for step in summary["next_steps"]:
                print(f"  {step}")

    def run_individual_demos(self) -> None:
        """Run individual tool demonstrations."""
        print("🔧 Individual Tool Demonstrations")
        print("=" * 40)

        # Security Scanner Demo
        print("\n🔒 Security Scanner Demo:")
        security_scanner = SecurityScanner(str(self.project_root))
        security_results = security_scanner.run_comprehensive_scan()
        security_report = security_scanner.generate_report()
        print(f"  Security report: {security_report}")

        # Code Quality Analyzer Demo
        print("\n🔍 Code Quality Analyzer Demo:")
        quality_analyzer = CodeQualityAnalyzer(str(self.project_root))
        quality_results = quality_analyzer.run_comprehensive_analysis()
        quality_report = quality_analyzer.generate_report()
        print(f"  Quality report: {quality_report}")

        # Dependency Scanner Demo
        print("\n📦 Dependency Scanner Demo:")
        dependency_scanner = DependencyScanner(str(self.project_root))
        dependency_results = dependency_scanner.run_comprehensive_scan()
        dependency_report = dependency_scanner.generate_report()
        remediation_report = dependency_scanner.generate_remediation_report()
        print(f"  Dependency report: {dependency_report}")
        print(f"  Remediation report: {remediation_report}")

    def show_tool_capabilities(self) -> None:
        """Show capabilities of each tool."""
        print("🛠️  Tool Capabilities Overview")
        print("=" * 35)

        capabilities = {
            "Security Scanner": [
                "Bandit: Python security linter",
                "Safety: Dependency vulnerability scanner",
                "Semgrep: Advanced static analysis",
                "Manual Check: Custom vulnerability detection",
            ],
            "Code Quality Analyzer": [
                "Ruff: Fast Python linter",
                "Pylint: Advanced code analysis",
                "MyPy: Static type checking",
                "Flake8: Style guide enforcement",
                "Radon: Complexity analysis",
            ],
            "Dependency Scanner": [
                "Safety: Known vulnerability database",
                "pip-audit: Comprehensive dependency audit",
                "OSV Scanner: Open Source Vulnerabilities",
                "Manual Check: Custom package detection",
            ],
            "Analysis Dashboard": [
                "Interactive console display",
                "HTML report generation",
                "Rich visualizations",
                "Comprehensive summaries",
            ],
        }

        for tool, features in capabilities.items():
            print(f"\n{tool}:")
            for feature in features:
                print(f"  • {feature}")

    def show_configuration_options(self) -> None:
        """Show configuration options."""
        print("⚙️  Configuration Options")
        print("=" * 30)

        config_file = self.project_root / "config" / "static_analysis_config.yaml"
        if config_file.exists():
            print(f"\n📄 Main Configuration: {config_file}")
            print("  • Security analysis settings")
            print("  • Code quality thresholds")
            print("  • Dependency scanning options")
            print("  • Reporting preferences")
            print("  • CI/CD integration settings")
        else:
            print(f"\n❌ Configuration file not found: {config_file}")

        print("\n🔧 Tool-Specific Configuration:")
        print("  • .bandit - Bandit security linter")
        print("  • .safety - Safety dependency scanner")
        print("  • pyproject.toml - Ruff, Pylint, MyPy")
        print("  • .flake8 - Flake8 configuration")

    def show_ci_integration(self) -> None:
        """Show CI/CD integration examples."""
        print("🏗️  CI/CD Integration")
        print("=" * 25)

        print("\n📋 Makefile Commands:")
        print("  make analysis     # Run all analysis")
        print("  make security     # Security scan only")
        print("  make quality      # Quality analysis only")
        print("  make deps         # Dependency scan only")
        print("  make ci           # Full CI pipeline")

        print("\n🔄 GitHub Actions:")
        print("  • Automatic analysis on push/PR")
        print("  • Security vulnerability scanning")
        print("  • Code quality checks")
        print("  • Dependency vulnerability scanning")
        print("  • Report artifact upload")

        print("\n🎯 Pre-commit Hooks:")
        print("  • Bandit security scanning")
        print("  • Safety dependency check")
        print("  • Code formatting (Black, isort)")
        print("  • Linting (Ruff, Flake8)")


def main():
    """Main entry point for demo analysis."""
    parser = argparse.ArgumentParser(description="Static Analysis Tools Demonstration")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument(
        "--demo-type",
        choices=["full", "individual", "capabilities", "config", "ci"],
        default="full",
        help="Type of demonstration to run",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    demo = DemoAnalysis(args.project_root)

    if args.demo_type == "full":
        demo.run_demo()
    elif args.demo_type == "individual":
        demo.run_individual_demos()
    elif args.demo_type == "capabilities":
        demo.show_tool_capabilities()
    elif args.demo_type == "config":
        demo.show_configuration_options()
    elif args.demo_type == "ci":
        demo.show_ci_integration()

    return 0


if __name__ == "__main__":
    sys.exit(main())
