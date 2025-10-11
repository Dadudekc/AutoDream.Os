#!/usr/bin/env python3
"""
Compliance History Tracker - Trend Analysis
============================================

Tracks V2 compliance and complexity metrics over time.
Stores historical data in SQLite and generates trend reports.

Features:
- Historical compliance tracking
- Trend analysis and visualization
- Progress tracking over commits
- Improvement/degradation detection

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from v2_compliance_checker import V2ComplianceChecker
    from complexity_analyzer import ComplexityAnalysisService
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False


@dataclass
class ComplianceSnapshot:
    """Snapshot of compliance metrics at a point in time."""

    timestamp: str
    commit_hash: Optional[str]
    total_files: int
    v2_compliance_rate: float
    complexity_compliance_rate: float
    critical_violations: int
    major_violations: int
    high_complexity: int
    medium_complexity: int
    overall_score: float


@dataclass
class TrendReport:
    """Trend analysis report."""

    snapshots: List[ComplianceSnapshot]
    trend_direction: str  # "improving", "stable", "degrading"
    compliance_change: float
    complexity_change: float
    score_change: float
    recommendations: List[str]


class ComplianceHistoryTracker:
    """Tracks compliance history and trends."""

    def __init__(self, db_path: str = "data/compliance_history.db"):
        """Initialize history tracker."""
        self.db_path = db_path
        self._ensure_database()

    def _ensure_database(self) -> None:
        """Ensure database and tables exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS compliance_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                commit_hash TEXT,
                total_files INTEGER,
                v2_compliance_rate REAL,
                complexity_compliance_rate REAL,
                critical_violations INTEGER,
                major_violations INTEGER,
                high_complexity INTEGER,
                medium_complexity INTEGER,
                overall_score REAL
            )
        """)
        conn.commit()
        conn.close()

    def record_snapshot(
        self, directory: str, commit_hash: Optional[str] = None
    ) -> ComplianceSnapshot:
        """Record current compliance snapshot."""
        if not TOOLS_AVAILABLE:
            raise RuntimeError("Quality tools not available")

        print("📊 Collecting current compliance metrics...")

        # Run V2 compliance check
        v2_checker = V2ComplianceChecker(directory)
        v2_report = v2_checker.scan_directory(Path(directory), "**/*.py")

        # Run complexity analysis
        complexity_service = ComplexityAnalysisService()
        complexity_reports = complexity_service.analyze_directory(directory, "**/*.py")

        # Calculate metrics
        files_with_complexity = [r for r in complexity_reports if r.has_violations]
        complexity_rate = (
            (len(complexity_reports) - len(files_with_complexity))
            / len(complexity_reports)
            * 100
            if complexity_reports
            else 100
        )

        high = sum(
            len([v for v in r.violations if v.severity == "HIGH"])
            for r in files_with_complexity
        )
        medium = sum(
            len([v for v in r.violations if v.severity == "MEDIUM"])
            for r in files_with_complexity
        )

        # Calculate overall score
        base_score = (v2_report.compliance_rate + complexity_rate) / 2
        penalty = (len(v2_report.critical_violations) * 5) + (high * 2)
        overall_score = max(0, base_score - penalty)

        # Create snapshot
        snapshot = ComplianceSnapshot(
            timestamp=datetime.now().isoformat(),
            commit_hash=commit_hash,
            total_files=v2_report.total_files,
            v2_compliance_rate=v2_report.compliance_rate,
            complexity_compliance_rate=complexity_rate,
            critical_violations=len(v2_report.critical_violations),
            major_violations=len(v2_report.major_violations),
            high_complexity=high,
            medium_complexity=medium,
            overall_score=round(overall_score, 1),
        )

        # Save to database
        self._save_snapshot(snapshot)

        print(f"✅ Snapshot recorded: Score {snapshot.overall_score}")
        return snapshot

    def _save_snapshot(self, snapshot: ComplianceSnapshot) -> None:
        """Save snapshot to database."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            INSERT INTO compliance_snapshots (
                timestamp, commit_hash, total_files, v2_compliance_rate,
                complexity_compliance_rate, critical_violations, major_violations,
                high_complexity, medium_complexity, overall_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot.timestamp,
                snapshot.commit_hash,
                snapshot.total_files,
                snapshot.v2_compliance_rate,
                snapshot.complexity_compliance_rate,
                snapshot.critical_violations,
                snapshot.major_violations,
                snapshot.high_complexity,
                snapshot.medium_complexity,
                snapshot.overall_score,
            ),
        )
        conn.commit()
        conn.close()

    def get_recent_snapshots(self, limit: int = 10) -> List[ComplianceSnapshot]:
        """Get recent snapshots."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            """
            SELECT timestamp, commit_hash, total_files, v2_compliance_rate,
                   complexity_compliance_rate, critical_violations, major_violations,
                   high_complexity, medium_complexity, overall_score
            FROM compliance_snapshots
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )

        snapshots = []
        for row in cursor.fetchall():
            snapshots.append(
                ComplianceSnapshot(
                    timestamp=row[0],
                    commit_hash=row[1],
                    total_files=row[2],
                    v2_compliance_rate=row[3],
                    complexity_compliance_rate=row[4],
                    critical_violations=row[5],
                    major_violations=row[6],
                    high_complexity=row[7],
                    medium_complexity=row[8],
                    overall_score=row[9],
                )
            )

        conn.close()
        return snapshots

    def get_all_snapshots(self) -> List[ComplianceSnapshot]:
        """Get all snapshots ordered by timestamp (oldest first for chart display)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            """
            SELECT timestamp, commit_hash, total_files, v2_compliance_rate,
                   complexity_compliance_rate, critical_violations, major_violations,
                   high_complexity, medium_complexity, overall_score
            FROM compliance_snapshots
            ORDER BY timestamp ASC
            """
        )

        snapshots = []
        for row in cursor.fetchall():
            snapshots.append(
                ComplianceSnapshot(
                    timestamp=row[0],
                    commit_hash=row[1],
                    total_files=row[2],
                    v2_compliance_rate=row[3],
                    complexity_compliance_rate=row[4],
                    critical_violations=row[5],
                    major_violations=row[6],
                    high_complexity=row[7],
                    medium_complexity=row[8],
                    overall_score=row[9],
                )
            )

        conn.close()
        return snapshots

    def get_trend_data(self) -> Dict[str, List[Any]]:
        """Get trend data formatted for charts (oldest to newest)."""
        snapshots = self.get_all_snapshots()
        
        return {
            "timestamps": [s.timestamp for s in snapshots],
            "dates": [datetime.fromisoformat(s.timestamp).strftime("%Y-%m-%d") 
                     for s in snapshots],
            "v2_rates": [s.v2_compliance_rate for s in snapshots],
            "complexity_rates": [s.complexity_compliance_rate for s in snapshots],
            "overall_scores": [s.overall_score for s in snapshots],
            "critical_violations": [s.critical_violations for s in snapshots],
            "major_violations": [s.major_violations for s in snapshots],
            "total_files": [s.total_files for s in snapshots],
        }

    def get_week_comparison(self) -> Optional[Dict[str, Any]]:
        """Get week-over-week comparison data."""
        snapshots = self.get_all_snapshots()
        
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

    def generate_trend_report(self, limit: int = 10) -> Optional[TrendReport]:
        """Generate trend analysis report."""
        snapshots = self.get_recent_snapshots(limit)

        if len(snapshots) < 2:
            return None

        # Analyze trends (compare newest to oldest)
        newest = snapshots[0]
        oldest = snapshots[-1]

        compliance_change = newest.v2_compliance_rate - oldest.v2_compliance_rate
        complexity_change = (
            newest.complexity_compliance_rate - oldest.complexity_compliance_rate
        )
        score_change = newest.overall_score - oldest.overall_score

        # Determine trend direction
        if score_change > 5:
            trend = "improving"
        elif score_change < -5:
            trend = "degrading"
        else:
            trend = "stable"

        # Generate recommendations
        recommendations = self._generate_recommendations(
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

    def _generate_recommendations(
        self,
        newest: ComplianceSnapshot,
        oldest: ComplianceSnapshot,
        v2_change: float,
        complexity_change: float,
    ) -> List[str]:
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

    def format_trend_report(self, report: TrendReport) -> str:
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
        lines.append(
            f"{'Date':<20} {'V2%':>8} {'Complexity%':>12} {'Score':>8} {'Critical':>10}"
        )
        lines.append("-" * 80)

        for snapshot in report.snapshots:
            date = datetime.fromisoformat(snapshot.timestamp).strftime("%Y-%m-%d %H:%M")
            lines.append(
                f"{date:<20} {snapshot.v2_compliance_rate:>7.1f}% {snapshot.complexity_compliance_rate:>11.1f}% {snapshot.overall_score:>7.1f} {snapshot.critical_violations:>10}"
            )

        lines.append("=" * 80)
        return "\n".join(lines)


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Compliance History Tracker")
    parser.add_argument(
        "command",
        choices=["snapshot", "report", "list"],
        help="Command: snapshot (record), report (trend), list (history)",
    )
    parser.add_argument("directory", nargs="?", default="src", help="Directory to analyze")
    parser.add_argument("--commit", help="Commit hash for snapshot")
    parser.add_argument("--limit", type=int, default=10, help="Number of snapshots for report")

    args = parser.parse_args()

    tracker = ComplianceHistoryTracker()

    if args.command == "snapshot":
        # Record new snapshot
        snapshot = tracker.record_snapshot(args.directory, args.commit)
        print(f"\n✅ Snapshot recorded!")
        print(f"Score: {snapshot.overall_score}")
        print(f"V2 Compliance: {snapshot.v2_compliance_rate:.1f}%")
        print(f"Complexity: {snapshot.complexity_compliance_rate:.1f}%")

    elif args.command == "report":
        # Generate trend report
        report = tracker.generate_trend_report(args.limit)
        if report:
            print(tracker.format_trend_report(report))
        else:
            print("⚠️ Not enough data for trend analysis (need at least 2 snapshots)")

    elif args.command == "list":
        # List recent snapshots
        snapshots = tracker.get_recent_snapshots(args.limit)
        print(f"Recent {len(snapshots)} snapshots:")
        for s in snapshots:
            date = datetime.fromisoformat(s.timestamp).strftime("%Y-%m-%d %H:%M")
            print(
                f"{date} - Score: {s.overall_score:.1f}, V2: {s.v2_compliance_rate:.1f}%, Complexity: {s.complexity_compliance_rate:.1f}%"
            )


if __name__ == "__main__":
    main()

