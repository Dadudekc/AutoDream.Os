#!/usr/bin/env python3
"""
Coverage Improver - V2 Compliance Module
=======================================

Main module for coordinating coverage improvement activities.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Coverage Improvement
"""

import argparse
from pathlib import Path
from typing import Any

from .coverage_analyzer import CoverageAnalyzer
from .coverage_reporter import CoverageReporter


class CoverageImprover:
    """Main coordinator for coverage improvement activities."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.analyzer = CoverageAnalyzer(project_root)
        self.reporter = CoverageReporter(project_root)

    def analyze_current_coverage(self, target: str = "all") -> dict[str, Any]:
        """Analyze current test coverage for specified target."""
        print(f"🔍 Analyzing test coverage for target: {target}")

        # Run coverage analysis
        coverage_data = self.analyzer.run_coverage_analysis(target)

        # Analyze coverage gaps
        gaps = self.analyzer.analyze_coverage_gaps(coverage_data)

        # Generate recommendations
        recommendations = self.reporter.generate_recommendations(gaps, target)

        return {
            "target": target,
            "coverage_data": coverage_data,
            "gaps": gaps,
            "recommendations": recommendations,
            "timestamp": self._get_timestamp(),
        }

    def generate_comprehensive_report(self, target: str = "all") -> dict[str, Any]:
        """Generate comprehensive coverage report."""
        analysis_data = self.analyze_current_coverage(target)
        report = self.reporter.generate_report(analysis_data)
        
        # Save report
        report_path = self.reporter.save_report(report)
        print(f"📄 Coverage report saved to: {report_path}")
        
        # Print summary
        self.reporter.print_report_summary(report)
        
        return report

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """Main entry point for coverage improvement tool."""
    parser = argparse.ArgumentParser(description="Test Coverage Improvement Tool")
    parser.add_argument("--analyze", action="store_true", help="Run coverage analysis")
    parser.add_argument("--target", default="all", help="Target for analysis (all, messaging, consolidated, routing, gateway)")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    
    args = parser.parse_args()
    
    project_root = Path(".")
    improver = CoverageImprover(project_root)
    
    if args.analyze or args.report:
        report = improver.generate_comprehensive_report(args.target)
        
        # Exit with appropriate code
        summary = report.get("summary", {})
        if summary.get("high_priority_recommendations", 0) > 0:
            print("\n⚠️  High priority coverage issues found!")
            exit(1)
        else:
            print("\n✅ Coverage analysis completed successfully!")
            exit(0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
