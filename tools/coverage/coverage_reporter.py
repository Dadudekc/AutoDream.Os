#!/usr/bin/env python3
"""
Coverage Reporter - V2 Compliance Module
======================================

Focused module for generating coverage reports and recommendations.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Coverage Reporting
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class CoverageReporter:
    """Generates coverage reports and recommendations."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.reports_dir = project_root / "runtime" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_recommendations(
        self, gaps: list[dict[str, Any]], target: str
    ) -> list[dict[str, Any]]:
        """Generate recommendations based on coverage gaps."""
        recommendations = []

        for gap in gaps:
            if gap.get("type") == "overall_coverage":
                current = gap.get("current", 0)
                target_coverage = gap.get("target", 80)

                if current < target_coverage:
                    recommendations.append(
                        {
                            "type": "increase_coverage",
                            "priority": "high" if current < 50 else "medium",
                            "description": f"Increase overall test coverage from {current}% to {target_coverage}%",
                            "actions": [
                                "Add unit tests for uncovered functions",
                                "Increase integration test coverage",
                                "Add edge case testing",
                            ],
                        }
                    )

        return recommendations

    def generate_report(self, analysis_data: dict[str, Any]) -> dict[str, Any]:
        """Generate comprehensive coverage report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "target": analysis_data.get("target", "all"),
            "coverage_data": analysis_data.get("coverage_data", {}),
            "gaps": analysis_data.get("gaps", []),
            "recommendations": analysis_data.get("recommendations", []),
            "summary": self._generate_summary(analysis_data),
        }

        return report

    def _generate_summary(self, analysis_data: dict[str, Any]) -> dict[str, Any]:
        """Generate summary of coverage analysis."""
        gaps = analysis_data.get("gaps", [])
        recommendations = analysis_data.get("recommendations", [])

        return {
            "total_gaps": len(gaps),
            "total_recommendations": len(recommendations),
            "high_priority_recommendations": len(
                [r for r in recommendations if r.get("priority") == "high"]
            ),
            "coverage_success": analysis_data.get("coverage_data", {}).get("success", False),
        }

    def save_report(self, report: dict[str, Any], filename: str = None) -> Path:
        """Save coverage report to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coverage_report_{timestamp}.json"

        report_path = self.reports_dir / filename

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report_path

    def print_report_summary(self, report: dict[str, Any]) -> None:
        """Print coverage report summary to console."""
        print("\n" + "=" * 60)
        print("📊 COVERAGE ANALYSIS REPORT")
        print("=" * 60)

        summary = report.get("summary", {})
        print(f"Target: {report.get('target', 'all')}")
        print(f"Analysis Time: {report.get('timestamp', 'N/A')}")
        print(f"Coverage Success: {summary.get('coverage_success', False)}")
        print(f"Total Gaps: {summary.get('total_gaps', 0)}")
        print(f"Total Recommendations: {summary.get('total_recommendations', 0)}")
        print(f"High Priority Issues: {summary.get('high_priority_recommendations', 0)}")

        # Print recommendations
        recommendations = report.get("recommendations", [])
        if recommendations:
            print("\n🎯 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                priority = rec.get("priority", "medium")
                description = rec.get("description", "No description")
                print(f"  {i}. [{priority.upper()}] {description}")

        print("=" * 60)
