#!/usr/bin/env python3
"""
Compliance History Reports
==========================

Trend analysis and report generation for compliance history.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored from: compliance_history_tracker.py
License: MIT
"""

from datetime import datetime
from typing import Any

from compliance_history_models import ComplianceSnapshot, TrendReport


class ComplianceReports:
    """Generates trend reports and analysis."""

    @staticmethod
    def get_trend_data(snapshots: list[ComplianceSnapshot]) -> dict[str, list[Any]]:
        """Get trend data formatted for charts (oldest to newest)."""
        return {
            "timestamps": [s.timestamp for s in snapshots],
            "dates": [datetime.fromisoformat(s.timestamp).strftime("%Y-%m-%d") for s in snapshots],
            "v2_rates": [s.v2_compliance_rate for s in snapshots],
            "complexity_rates": [s.complexity_compliance_rate for s in snapshots],
            "overall_scores": [s.overall_score for s in snapshots],
            "critical_violations": [s.critical_violations for s in snapshots],
            "major_violations": [s.major_violations for s in snapshots],
            "total_files": [s.total_files for s in snapshots],
        }

    @staticmethod
    def get_week_comparison(snapshots: list[ComplianceSnapshot]) -> dict[str, Any] | None:
        """Get week-over-week comparison data."""
        if len(snapshots) < 2:
            return None

        # Get latest snapshot
        current = snapshots[-1]
        current_date = datetime.fromisoformat(current.timestamp)

        # Find snapshot from ~7 days ago
        week_ago = None
        for s in reversed(snapshots[:-1]):
            s_date = datetime.fromisoformat(s.timestamp)
            days_diff = (current_date - s_date).days
            if 6 <= days_diff <= 8:  # Within 6-8 days
                week_ago = s
                break

        # If no exact week match, use oldest available
        if not week_ago:
            week_ago = snapshots[0] if len(snapshots) > 1 else current

        # Calculate changes
        v2_change = current.v2_compliance_rate - week_ago.v2_compliance_rate
        complexity_change = current.complexity_compliance_rate - week_ago.complexity_compliance_rate
        score_change = current.overall_score - week_ago.overall_score
        critical_change = current.critical_violations - week_ago.critical_violations

        return {
            "current": {
                "date": current_date.strftime("%Y-%m-%d"),
                "v2_rate": current.v2_compliance_rate,
                "complexity_rate": current.complexity_compliance_rate,
                "score": current.overall_score,
                "critical": current.critical_violations,
            },
            "previous": {
                "date": datetime.fromisoformat(week_ago.timestamp).strftime("%Y-%m-%d"),
                "v2_rate": week_ago.v2_compliance_rate,
                "complexity_rate": week_ago.complexity_compliance_rate,
                "score": week_ago.overall_score,
                "critical": week_ago.critical_violations,
            },
            "changes": {
                "v2_rate": round(v2_change, 1),
                "complexity_rate": round(complexity_change, 1),
                "score": round(score_change, 1),
                "critical": critical_change,
            },
            "days_apart": (current_date - datetime.fromisoformat(week_ago.timestamp)).days,
        }

    @staticmethod
    def generate_trend_report(snapshots: list[ComplianceSnapshot]) -> TrendReport | None:
        """Generate trend analysis report."""
        if len(snapshots) < 2:
            return None

        # Analyze trends (compare newest to oldest)
        newest = snapshots[0]
        oldest = snapshots[-1]

        compliance_change = newest.v2_compliance_rate - oldest.v2_compliance_rate
        complexity_change = newest.complexity_compliance_rate - oldest.complexity_compliance_rate
        score_change = newest.overall_score - oldest.overall_score

        # Determine trend direction
        if score_change > 5:
            trend = "improving"
        elif score_change < -5:
            trend = "degrading"
        else:
            trend = "stable"

        # Generate recommendations
        recommendations = ComplianceReports._generate_recommendations(
            newest, oldest, compliance_change, complexity_change
        )

        return TrendReport(
            snapshots=snapshots,
            trend_direction=trend,
            compliance_change=compliance_change,
            complexity_change=complexity_change,
            score_change=score_change,
            recommendations=recommendations,
        )

    @staticmethod
    def _generate_recommendations(
        newest: ComplianceSnapshot,
        oldest: ComplianceSnapshot,
        v2_change: float,
        complexity_change: float,
    ) -> list[str]:
        """Generate recommendations based on trends."""
        recommendations = []

        if v2_change < 0:
            recommendations.append(
                f"⚠️ V2 compliance decreased by {abs(v2_change):.1f}% - review recent changes"
            )
        elif v2_change > 0:
            recommendations.append(
                f"✅ V2 compliance improved by {v2_change:.1f}% - great progress!"
            )

        if complexity_change < 0:
            recommendations.append(
                f"⚠️ Complexity compliance decreased by {abs(complexity_change):.1f}% - simplify recent code"
            )
        elif complexity_change > 0:
            recommendations.append(
                f"✅ Complexity improved by {complexity_change:.1f}% - excellent refactoring!"
            )

        if newest.critical_violations > 0:
            recommendations.append(
                f"🔴 {newest.critical_violations} CRITICAL violations - immediate action required"
            )

        if newest.high_complexity > 0:
            recommendations.append(
                f"🔴 {newest.high_complexity} HIGH complexity violations - refactor complex functions"
            )

        return recommendations

    @staticmethod
    def format_trend_report(report: TrendReport) -> str:
        """Format trend report as string."""
        lines = []
        lines.append("=" * 80)
        lines.append("COMPLIANCE TREND ANALYSIS")
        lines.append("=" * 80)
        lines.append(f"Snapshots analyzed: {len(report.snapshots)}")
        lines.append(f"Trend direction: {report.trend_direction.upper()}")
        lines.append("")

        lines.append("CHANGES:")
        lines.append(f"  V2 Compliance: {report.compliance_change:+.1f}%")
        lines.append(f"  Complexity Compliance: {report.complexity_change:+.1f}%")
        lines.append(f"  Overall Score: {report.score_change:+.1f}")
        lines.append("")

        if report.recommendations:
            lines.append("RECOMMENDATIONS:")
            for rec in report.recommendations:
                lines.append(f"  {rec}")
            lines.append("")

        lines.append("RECENT SNAPSHOTS:")
        lines.append(f"{'Date':<20} {'V2%':>8} {'Complexity%':>12} {'Score':>8} {'Critical':>10}")
        lines.append("-" * 80)

        for snapshot in report.snapshots:
            date = datetime.fromisoformat(snapshot.timestamp).strftime("%Y-%m-%d %H:%M")
            lines.append(
                f"{date:<20} {snapshot.v2_compliance_rate:>7.1f}% {snapshot.complexity_compliance_rate:>11.1f}% {snapshot.overall_score:>7.1f} {snapshot.critical_violations:>10}"
            )

        lines.append("=" * 80)
        return "\n".join(lines)
