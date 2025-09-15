#!/usr/bin/env python3
"""
Verification Reporter - V2 Compliance Module
==========================================

Focused module for generating verification reports.

V2 Compliance: < 400 lines, single responsibility, modular design.

Author: Agent-5 (Data Organization Specialist)
Test Type: Verification Reporting
"""

import json
from pathlib import Path
from typing import Any


class VerificationReporter:
    """Generates reports for functionality verification."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.reports_dir = project_root / "runtime" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_verification_report(self, verification_result: dict[str, Any]) -> dict[str, Any]:
        """Generate comprehensive verification report."""
        report = {
            "report_type": "functionality_verification",
            "timestamp": verification_result.get("timestamp", ""),
            "verification_summary": self._generate_verification_summary(verification_result),
            "change_analysis": self._analyze_changes(verification_result),
            "preservation_analysis": self._analyze_preservation(verification_result),
            "recommendations": verification_result.get("recommendations", []),
            "raw_result": verification_result,
        }

        return report

    def _generate_verification_summary(self, result: dict[str, Any]) -> dict[str, Any]:
        """Generate verification summary."""
        return {
            "status": result.get("verification_status", "unknown"),
            "preservation_score": result.get("preservation_score", 0.0),
            "baseline_exists": result.get("baseline_exists", False),
            "has_errors": bool(result.get("error")),
            "error_message": result.get("error", ""),
        }

    def _analyze_changes(self, result: dict[str, Any]) -> dict[str, Any]:
        """Analyze changes detected."""
        differences = result.get("differences", {})

        return {
            "file_changes": {
                "total": len(differences.get("file_changes", [])),
                "added": len(
                    [
                        c
                        for c in differences.get("file_changes", [])
                        if c.get("change_type") == "added"
                    ]
                ),
                "modified": len(
                    [
                        c
                        for c in differences.get("file_changes", [])
                        if c.get("change_type") == "modified"
                    ]
                ),
                "deleted": len(
                    [
                        c
                        for c in differences.get("file_changes", [])
                        if c.get("change_type") == "deleted"
                    ]
                ),
            },
            "import_changes": len(differences.get("import_changes", [])),
            "function_changes": len(differences.get("function_changes", [])),
            "class_changes": len(differences.get("class_changes", [])),
            "test_changes": len(differences.get("test_changes", [])),
        }

    def _analyze_preservation(self, result: dict[str, Any]) -> dict[str, Any]:
        """Analyze functionality preservation."""
        preservation_score = result.get("preservation_score", 0.0)

        return {
            "score": preservation_score,
            "grade": self._get_preservation_grade(preservation_score),
            "status": self._get_preservation_status(preservation_score),
            "risk_level": self._get_risk_level(preservation_score),
        }

    def _get_preservation_grade(self, score: float) -> str:
        """Get preservation grade based on score."""
        if score >= 95.0:
            return "A"
        elif score >= 90.0:
            return "B"
        elif score >= 80.0:
            return "C"
        elif score >= 70.0:
            return "D"
        else:
            return "F"

    def _get_preservation_status(self, score: float) -> str:
        """Get preservation status based on score."""
        if score >= 95.0:
            return "Excellent"
        elif score >= 90.0:
            return "Good"
        elif score >= 80.0:
            return "Acceptable"
        elif score >= 70.0:
            return "Concerning"
        else:
            return "Critical"

    def _get_risk_level(self, score: float) -> str:
        """Get risk level based on score."""
        if score >= 95.0:
            return "Low"
        elif score >= 80.0:
            return "Medium"
        else:
            return "High"

    def save_report(self, report: dict[str, Any], filename: str = None) -> Path:
        """Save verification report to file."""
        if filename is None:
            timestamp = report.get("timestamp", "").replace(":", "-").replace(".", "-")
            filename = f"verification_report_{timestamp}.json"

        report_path = self.reports_dir / filename

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report_path

    def print_verification_summary(self, report: dict[str, Any]) -> None:
        """Print verification summary to console."""
        print("\n" + "=" * 70)
        print("📋 FUNCTIONALITY VERIFICATION REPORT")
        print("=" * 70)

        summary = report.get("verification_summary", {})
        print(f"Status: {summary.get('status', 'UNKNOWN')}")
        print(f"Preservation Score: {summary.get('preservation_score', 0.0):.1f}%")
        print(f"Baseline Exists: {summary.get('baseline_exists', False)}")

        if summary.get("has_errors"):
            print(f"⚠️  Errors: {summary.get('error_message', 'Unknown error')}")

        # Change analysis
        changes = report.get("change_analysis", {})
        print("\n📊 CHANGE ANALYSIS:")
        file_changes = changes.get("file_changes", {})
        print(
            f"  File Changes: {file_changes.get('total', 0)} (Added: {file_changes.get('added', 0)}, Modified: {file_changes.get('modified', 0)}, Deleted: {file_changes.get('deleted', 0)})"
        )
        print(f"  Import Changes: {changes.get('import_changes', 0)}")
        print(f"  Function Changes: {changes.get('function_changes', 0)}")
        print(f"  Class Changes: {changes.get('class_changes', 0)}")
        print(f"  Test Changes: {changes.get('test_changes', 0)}")

        # Preservation analysis
        preservation = report.get("preservation_analysis", {})
        print("\n🎯 PRESERVATION ANALYSIS:")
        print(f"  Grade: {preservation.get('grade', 'N/A')}")
        print(f"  Status: {preservation.get('status', 'UNKNOWN')}")
        print(f"  Risk Level: {preservation.get('risk_level', 'UNKNOWN')}")

        # Recommendations
        recommendations = report.get("recommendations", [])
        if recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")

        print("=" * 70)
