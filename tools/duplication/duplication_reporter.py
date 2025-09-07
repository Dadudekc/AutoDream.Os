#!/usr/bin/env python3
"""
Duplication Reporter - Agent Cellphone V2
=======================================

Report generation utilities for the duplication detection system.
Follows V2 standards: ≤200 LOC, OOP design, SRP compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from .duplication_types import DuplicationIssue, DuplicationSeverity


class DuplicationReporter:
    """Generates human readable and JSON reports."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def generate_report(
        self, issues: List[DuplicationIssue], total_files: int
    ) -> Dict[str, Any]:
        """Create a structured report from detected issues."""
        severity_counts = {s.value: 0 for s in DuplicationSeverity}
        for issue in issues:
            severity_counts[issue.severity.value] += 1

        return {
            "summary": {
                "total_files": total_files,
                "total_issues": len(issues),
                "severity_counts": severity_counts,
            },
            "issues": [issue.to_dict() for issue in issues],
        }

    def print_report(self, report: Dict[str, Any]) -> None:
        """Print a human readable report to stdout."""
        summary = report["summary"]
        print("=== Duplication Report ===")
        print(f"Analyzed files: {summary['total_files']}")
        print(f"Issues found: {summary['total_issues']}")
        for sev, count in summary["severity_counts"].items():
            print(f"{sev.title()}: {count}")

        if not report["issues"]:
            print("\nNo issues detected.")
            return

        print("\nDetailed Issues:")
        for issue in report["issues"]:
            print(f"- [{issue['severity']}] {issue['description']}")
            for file_path, line in issue["line_numbers"]:
                print(f"  {file_path}:{line}")
            print()

    def save_json_report(self, report: Dict[str, Any], output_path: str) -> None:
        """Save the report to a JSON file."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        self.logger.info("Report saved to %s", output_path)
