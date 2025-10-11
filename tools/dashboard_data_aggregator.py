"""
Dashboard Data Aggregator - Compliance Dashboard
=================================================

Aggregates data from quality tools for dashboard generation.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DashboardData:
    """Data for dashboard generation."""

    scan_date: str
    total_files: int
    v2_compliance_rate: float
    complexity_compliance_rate: float
    critical_violations: int
    major_violations: int
    minor_violations: int
    high_complexity: int
    medium_complexity: int
    low_complexity: int
    top_violators: List[Dict[str, Any]]
    suggestions_summary: List[Dict[str, Any]]
    overall_score: float
    historical: Optional[Dict[str, Any]] = None
    week_comparison: Optional[Dict[str, Any]] = None


class DashboardDataAggregator:
    """Aggregates data from all quality tools."""

    def aggregate_data(self, v2_report, complexity_reports, suggestions) -> DashboardData:
        """Aggregate data from all tools."""
        # V2 data
        critical = len(v2_report.critical_violations)
        major = len(v2_report.major_violations)
        minor = len(v2_report.minor_violations)

        # Complexity data
        files_with_complexity = [r for r in complexity_reports if r.has_violations]
        high = sum(
            len([v for v in r.violations if v.severity == "HIGH"])
            for r in files_with_complexity
        )
        medium = sum(
            len([v for v in r.violations if v.severity == "MEDIUM"])
            for r in files_with_complexity
        )
        low = sum(
            len([v for v in r.violations if v.severity == "LOW"])
            for r in files_with_complexity
        )

        complexity_rate = (
            (len(complexity_reports) - len(files_with_complexity))
            / len(complexity_reports)
            * 100
            if complexity_reports
            else 100
        )

        # Top violators
        top_violators = self.identify_top_violators(v2_report, complexity_reports, suggestions[:10])

        # Suggestions summary
        suggestions_summary = [
            {
                "file": Path(s.file_path).name,
                "current_lines": s.current_lines,
                "estimated_lines": s.estimated_main_file_lines,
                "confidence": s.confidence,
                "modules": len(s.suggested_modules),
            }
            for s in suggestions[:10]
        ]

        # Calculate overall quality score
        overall_score = self.calculate_overall_score(
            v2_report.compliance_rate, complexity_rate, critical, high
        )

        return DashboardData(
            scan_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_files=v2_report.total_files,
            v2_compliance_rate=v2_report.compliance_rate,
            complexity_compliance_rate=complexity_rate,
            critical_violations=critical,
            major_violations=major,
            minor_violations=minor,
            high_complexity=high,
            medium_complexity=medium,
            low_complexity=low,
            top_violators=top_violators,
            suggestions_summary=suggestions_summary,
            overall_score=overall_score,
        )

    def identify_top_violators(
        self, v2_report, complexity_reports, suggestions
    ) -> List[Dict[str, Any]]:
        """Identify files with most issues."""
        violators = {}

        # Collect V2 violations
        for violation in v2_report.violations:
            file = violation.file_path
            if file not in violators:
                violators[file] = {
                    "file": Path(file).name,
                    "v2_violations": 0,
                    "complexity_violations": 0,
                    "has_suggestion": False,
                    "total_score": 0,
                }
            violators[file]["v2_violations"] += 1
            if violation.severity == "CRITICAL":
                violators[file]["total_score"] += 10
            elif violation.severity == "MAJOR":
                violators[file]["total_score"] += 5
            else:
                violators[file]["total_score"] += 1

        # Collect complexity violations
        for report in complexity_reports:
            if report.has_violations:
                file = report.file_path
                if file not in violators:
                    violators[file] = {
                        "file": Path(file).name,
                        "v2_violations": 0,
                        "complexity_violations": 0,
                        "has_suggestion": False,
                        "total_score": 0,
                    }
                violators[file]["complexity_violations"] = len(report.violations)
                for v in report.violations:
                    if v.severity == "HIGH":
                        violators[file]["total_score"] += 3
                    elif v.severity == "MEDIUM":
                        violators[file]["total_score"] += 2
                    else:
                        violators[file]["total_score"] += 1

        # Mark files with suggestions
        for suggestion in suggestions:
            file = suggestion.file_path
            if file in violators:
                violators[file]["has_suggestion"] = True

        # Sort by total score
        sorted_violators = sorted(
            violators.values(), key=lambda x: x["total_score"], reverse=True
        )
        return sorted_violators[:10]

    def calculate_overall_score(
        self, v2_rate: float, complexity_rate: float, critical: int, high: int
    ) -> float:
        """Calculate overall quality score (0-100)."""
        base_score = (v2_rate + complexity_rate) / 2
        penalty = (critical * 5) + (high * 2)
        score = max(0, base_score - penalty)
        return round(score, 1)



