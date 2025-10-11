#!/usr/bin/env python3
"""
Compliance History Database
============================

Database operations for compliance history tracking.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored from: compliance_history_tracker.py
License: MIT
"""

import sqlite3
from pathlib import Path

from compliance_history_models import ComplianceSnapshot


class ComplianceDatabase:
    """Handles database operations for compliance history."""

    def __init__(self, db_path: str = "data/compliance_history.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self._ensure_database()

    def _ensure_database(self) -> None:
        """Ensure database and tables exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
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
        """
        )
        conn.commit()
        conn.close()

    def save_snapshot(self, snapshot: ComplianceSnapshot) -> None:
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

    def get_recent_snapshots(self, limit: int = 10) -> list[ComplianceSnapshot]:
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

        snapshots = [self._row_to_snapshot(row) for row in cursor.fetchall()]
        conn.close()
        return snapshots

    def get_all_snapshots(self) -> list[ComplianceSnapshot]:
        """Get all snapshots ordered by timestamp (oldest first)."""
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

        snapshots = [self._row_to_snapshot(row) for row in cursor.fetchall()]
        conn.close()
        return snapshots

    @staticmethod
    def _row_to_snapshot(row: tuple) -> ComplianceSnapshot:
        """Convert database row to ComplianceSnapshot."""
        return ComplianceSnapshot(
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
