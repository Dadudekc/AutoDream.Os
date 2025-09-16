#!/usr/bin/env python3
"""
Swarm Monitoring Data - Data persistence and management
======================================================

Data management functionality extracted from swarm_monitoring_dashboard.py
V2 compliant: ≤400 lines, focused responsibility
"""

import json
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .swarm_monitoring_core import AgentStatus, Alert, SystemMetrics

logger = logging.getLogger(__name__)


class SwarmMonitoringData:
    """Data persistence and management for swarm monitoring."""

    def __init__(self, data_path: str = "data/monitoring.db"):
        """Initialize data manager."""
        self.data_path = Path(data_path)
        self.data_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_database()
        logger.info(f"Swarm monitoring data initialized: {self.data_path}")

    def _init_database(self) -> None:
        """Initialize SQLite database."""
        with sqlite3.connect(self.data_path) as conn:
            cursor = conn.cursor()

            # Agent status table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_phase TEXT NOT NULL,
                    current_mission TEXT,
                    mission_priority TEXT,
                    progress_percentage REAL,
                    active_tasks TEXT,
                    completed_tasks TEXT,
                    coordination_status TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Alerts table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT UNIQUE NOT NULL,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    component TEXT NOT NULL,
                    resolved BOOLEAN DEFAULT FALSE,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # System metrics table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpu_usage REAL NOT NULL,
                    memory_usage REAL NOT NULL,
                    disk_usage REAL NOT NULL,
                    network_io TEXT,
                    active_connections INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create indexes for better performance
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_agent_status_agent_id ON agent_status(agent_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_agent_status_timestamp ON agent_status(timestamp)"
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON alerts(resolved)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)")
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON system_metrics(timestamp)"
            )

            conn.commit()

    def save_agent_status(self, status: AgentStatus) -> bool:
        """Save agent status to database."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO agent_status (
                        agent_id, status, current_phase, current_mission,
                        mission_priority, progress_percentage, active_tasks,
                        completed_tasks, coordination_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        status.agent_id,
                        status.status,
                        status.current_phase,
                        status.current_mission,
                        status.mission_priority,
                        status.progress_percentage,
                        json.dumps(status.active_tasks),
                        json.dumps(status.completed_tasks),
                        json.dumps(status.coordination_status),
                    ),
                )

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to save agent status: {e}")
            return False

    def get_agent_status_history(self, agent_id: str, hours: int = 24) -> list[dict[str, Any]]:
        """Get agent status history."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cutoff = datetime.now() - timedelta(hours=hours)
                cursor.execute(
                    """
                    SELECT * FROM agent_status
                    WHERE agent_id = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                """,
                    (agent_id, cutoff),
                )

                columns = [description[0] for description in cursor.description]
                results = []

                for row in cursor.fetchall():
                    record = dict(zip(columns, row, strict=False))
                    # Parse JSON fields
                    record["active_tasks"] = json.loads(record["active_tasks"] or "[]")
                    record["completed_tasks"] = json.loads(record["completed_tasks"] or "[]")
                    record["coordination_status"] = json.loads(
                        record["coordination_status"] or "{}"
                    )
                    results.append(record)

                return results
        except Exception as e:
            logger.error(f"Failed to get agent status history: {e}")
            return []

    def save_alert(self, alert: Alert) -> bool:
        """Save alert to database."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO alerts (
                        alert_id, level, message, component, resolved, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        alert.alert_id,
                        alert.level,
                        alert.message,
                        alert.component,
                        alert.resolved,
                        alert.timestamp,
                    ),
                )

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to save alert: {e}")
            return False

    def get_alerts(self, resolved: bool | None = None, hours: int = 24) -> list[dict[str, Any]]:
        """Get alerts from database."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cutoff = datetime.now() - timedelta(hours=hours)
                query = "SELECT * FROM alerts WHERE timestamp >= ?"
                params = [cutoff]

                if resolved is not None:
                    query += " AND resolved = ?"
                    params.append(resolved)

                query += " ORDER BY timestamp DESC"

                cursor.execute(query, params)

                columns = [description[0] for description in cursor.description]
                results = []

                for row in cursor.fetchall():
                    record = dict(zip(columns, row, strict=False))
                    results.append(record)

                return results
        except Exception as e:
            logger.error(f"Failed to get alerts: {e}")
            return []

    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve alert in database."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE alerts SET resolved = TRUE
                    WHERE alert_id = ?
                """,
                    (alert_id,),
                )

                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to resolve alert: {e}")
            return False

    def save_system_metrics(self, metrics: SystemMetrics) -> bool:
        """Save system metrics to database."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO system_metrics (
                        cpu_usage, memory_usage, disk_usage,
                        network_io, active_connections, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        metrics.cpu_usage,
                        metrics.memory_usage,
                        metrics.disk_usage,
                        json.dumps(metrics.network_io),
                        metrics.active_connections,
                        metrics.timestamp,
                    ),
                )

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to save system metrics: {e}")
            return False

    def get_metrics_history(self, hours: int = 24) -> list[dict[str, Any]]:
        """Get metrics history from database."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cutoff = datetime.now() - timedelta(hours=hours)
                cursor.execute(
                    """
                    SELECT * FROM system_metrics
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                """,
                    (cutoff,),
                )

                columns = [description[0] for description in cursor.description]
                results = []

                for row in cursor.fetchall():
                    record = dict(zip(columns, row, strict=False))
                    # Parse JSON fields
                    record["network_io"] = json.loads(record["network_io"] or "{}")
                    results.append(record)

                return results
        except Exception as e:
            logger.error(f"Failed to get metrics history: {e}")
            return []

    def get_agent_statistics(self, agent_id: str, days: int = 7) -> dict[str, Any]:
        """Get agent statistics."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cutoff = datetime.now() - timedelta(days=days)

                # Get status distribution
                cursor.execute(
                    """
                    SELECT status, COUNT(*) as count
                    FROM agent_status
                    WHERE agent_id = ? AND timestamp >= ?
                    GROUP BY status
                """,
                    (agent_id, cutoff),
                )

                status_distribution = dict(cursor.fetchall())

                # Get phase distribution
                cursor.execute(
                    """
                    SELECT current_phase, COUNT(*) as count
                    FROM agent_status
                    WHERE agent_id = ? AND timestamp >= ?
                    GROUP BY current_phase
                """,
                    (agent_id, cutoff),
                )

                phase_distribution = dict(cursor.fetchall())

                # Get average progress
                cursor.execute(
                    """
                    SELECT AVG(progress_percentage) as avg_progress
                    FROM agent_status
                    WHERE agent_id = ? AND timestamp >= ? AND progress_percentage IS NOT NULL
                """,
                    (agent_id, cutoff),
                )

                avg_progress = cursor.fetchone()[0] or 0

                return {
                    "status_distribution": status_distribution,
                    "phase_distribution": phase_distribution,
                    "average_progress": round(avg_progress, 2),
                    "period_days": days,
                }
        except Exception as e:
            logger.error(f"Failed to get agent statistics: {e}")
            return {}

    def cleanup_old_data(self, days: int = 30) -> int:
        """Clean up old data."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                cutoff = datetime.now() - timedelta(days=days)

                # Clean up old agent status
                cursor.execute("DELETE FROM agent_status WHERE timestamp < ?", (cutoff,))
                agent_deleted = cursor.rowcount

                # Clean up old metrics
                cursor.execute("DELETE FROM system_metrics WHERE timestamp < ?", (cutoff,))
                metrics_deleted = cursor.rowcount

                # Clean up resolved alerts older than 7 days
                alert_cutoff = datetime.now() - timedelta(days=7)
                cursor.execute(
                    """
                    DELETE FROM alerts
                    WHERE resolved = TRUE AND timestamp < ?
                """,
                    (alert_cutoff,),
                )
                alerts_deleted = cursor.rowcount

                conn.commit()

                total_deleted = agent_deleted + metrics_deleted + alerts_deleted
                logger.info(f"Cleaned up {total_deleted} old records")
                return total_deleted
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")
            return 0

    def get_database_stats(self) -> dict[str, Any]:
        """Get database statistics."""
        try:
            with sqlite3.connect(self.data_path) as conn:
                cursor = conn.cursor()

                # Get table counts
                cursor.execute("SELECT COUNT(*) FROM agent_status")
                agent_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM alerts")
                alert_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM system_metrics")
                metrics_count = cursor.fetchone()[0]

                # Get database size
                cursor.execute(
                    "SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()"
                )
                db_size = cursor.fetchone()[0]

                return {
                    "agent_status_records": agent_count,
                    "alert_records": alert_count,
                    "metrics_records": metrics_count,
                    "database_size_bytes": db_size,
                    "database_size_mb": round(db_size / (1024 * 1024), 2),
                }
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}
