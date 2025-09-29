"""
V2 Compliance Violation Detection and Reporting
==============================================

Violation detection, formatting, and reporting functionality.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ViolationDetector:
    """Detects and reports V2 compliance violations."""

    def __init__(self):
        self.violation_counts = {
            "file_loc": 0,
            "class_loc": 0,
            "function_loc": 0,
            "line_length": 0,
            "print_statement": 0,
            "syntax_error": 0,
            "analysis_error": 0,
        }

    def analyze_project(self, root_path: Path, max_files: int = 100000) -> dict[str, Any]:
        """Analyze entire project for V2 compliance violations."""
        from .core import AnalysisCore, should_exclude_file

        core = AnalysisCore()
        results = {
            "project_root": str(root_path),
            "files_analyzed": 0,
            "total_violations": 0,
            "violation_counts": self.violation_counts.copy(),
            "files": [],
            "summary": {},
        }

        python_files = list(root_path.rglob("*.py"))
        files_to_analyze = [f for f in python_files if not should_exclude_file(f)][:max_files]

        logger.info(f"Analyzing {len(files_to_analyze)} Python files...")

        for file_path in files_to_analyze:
            file_result = core.analyze_python_file(file_path)
            results["files"].append(file_result)
            results["files_analyzed"] += 1

            # Count violations by type
            for violation in file_result["violations"]:
                violation_type = violation["type"]
                if violation_type in self.violation_counts:
                    self.violation_counts[violation_type] += 1
                    results["total_violations"] += 1

        # Generate summary
        results["summary"] = self._generate_summary(results)
        results["violation_counts"] = self.violation_counts.copy()

        return results

    def _generate_summary(self, results: dict[str, Any]) -> dict[str, Any]:
        """Generate summary statistics."""
        total_files = results["files_analyzed"]
        total_violations = results["total_violations"]

        error_files = sum(1 for f in results["files"] if f["status"] == "error")
        warning_files = sum(1 for f in results["files"] if f["status"] == "warning")
        ok_files = sum(1 for f in results["files"] if f["status"] == "ok")

        return {
            "total_files": total_files,
            "total_violations": total_violations,
            "error_files": error_files,
            "warning_files": warning_files,
            "ok_files": ok_files,
            "compliance_rate": (ok_files / total_files * 100) if total_files > 0 else 0,
            "violation_rate": (total_violations / total_files) if total_files > 0 else 0,
        }

    def ci_gate_check(self, results: dict[str, Any]) -> tuple[bool, str]:
        """Check if project passes CI gate requirements."""
        summary = results["summary"]

        # CI gate fails if there are any error-level violations
        if summary["error_files"] > 0:
            return (
                False,
                f"CI gate failed: {summary['error_files']} files have error-level violations",
            )

        # CI gate fails if compliance rate is below 90%
        if summary["compliance_rate"] < 90:
            return (
                False,
                f"CI gate failed: compliance rate {summary['compliance_rate']:.1f}% below 90% threshold",
            )

        return True, f"CI gate passed: {summary['compliance_rate']:.1f}% compliance rate"


def format_violations_text(results: dict[str, Any]) -> str:
    """Format violation results as human-readable text."""
    summary = results["summary"]
    violation_counts = results["violation_counts"]

    output = []
    output.append("=" * 80)
    output.append("V2 COMPLIANCE ANALYSIS REPORT")
    output.append("=" * 80)
    output.append("")

    # Summary
    output.append("SUMMARY:")
    output.append(f"  Total files analyzed: {summary['total_files']}")
    output.append(f"  Total violations: {summary['total_violations']}")
    output.append(f"  Compliance rate: {summary['compliance_rate']:.1f}%")
    output.append(f"  Error files: {summary['error_files']}")
    output.append(f"  Warning files: {summary['warning_files']}")
    output.append(f"  OK files: {summary['ok_files']}")
    output.append("")

    # Violation breakdown
    output.append("VIOLATION BREAKDOWN:")
    for violation_type, count in violation_counts.items():
        if count > 0:
            output.append(f"  {violation_type}: {count}")
    output.append("")

    # File details
    output.append("FILE DETAILS:")
    for file_result in results["files"]:
        if file_result["violations"]:
            output.append(
                f"  {file_result['file']} ({file_result['lines']} lines) - {file_result['status']}"
            )
            for violation in file_result["violations"]:
                output.append(f"    Line {violation['line']}: {violation['message']}")
            output.append("")

    return "\n".join(output)
