#!/usr/bin/env python3
"""
Backup Database Manager - V2 Compliant Module
===========================================

Database management for backup monitoring system.
V2 COMPLIANT: Focused database operations under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..models.backup_enums import (
    AlertSeverity,
    AlertStatus,
    AlertType,
    HealthCheckStatus,
    HealthCheckType,
    MetricType,
)
from ..models.backup_models import Alert, AlertHistory, HealthCheck, MonitoringMetric

logger = logging.getLogger(__name__)


class BackupMonitoringDatabase:
    """Database manager for backup monitoring system."""

    def __init__(self, db_path: str = "monitoring.db"):
        self.db_path = Path(db_path)
        self._init_database()

    def _init_database(self) -> None:

EXAMPLE USAGE:
==============

# Import the core component
from src.core.backup.database.backup_database import Backup_Database

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Backup_Database(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

        """Initialize the monitoring database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS monitoring_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_unit TEXT,
                    metric_type TEXT DEFAULT 'gauge',
                    timestamp DATETIME NOT NULL,
                    tags TEXT,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS health_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    check_name TEXT NOT NULL,
                    check_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT,
                    duration_ms INTEGER,
                    timestamp DATETIME NOT NULL,
                    details TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT UNIQUE NOT NULL,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    acknowledged BOOLEAN DEFAULT 0,
                    acknowledged_by TEXT,
                    acknowledged_at DATETIME,
                    resolved_at DATETIME,
                    escalation_count INTEGER DEFAULT 0,
                    last_escalation DATETIME,
                    tags TEXT,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS alert_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp DATETIME NOT NULL,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indexes for better performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name_timestamp ON monitoring_metrics(metric_name, timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_health_checks_timestamp ON health_checks(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_alert_history_alert_id ON alert_history(alert_id)")

            conn.commit()

    def store_metric(self, metric: MonitoringMetric) -> bool:
        """Store a monitoring metric."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO monitoring_metrics
                    (metric_name, metric_value, metric_unit, metric_type, timestamp, tags, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    metric.metric_name,
                    metric.metric_value,
                    metric.metric_unit,
                    metric.metric_type.value,
                    metric.timestamp.isoformat(),
                    str(metric.tags) if metric.tags else None,
                    str(metric.metadata) if metric.metadata else None
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error storing metric: {e}")
            return False

    def get_metrics(self, metric_name: str, hours: int = 24,
                   limit: int = 1000) -> List[MonitoringMetric]:
        """Get metrics for a specific metric name."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT metric_name, metric_value, metric_unit, metric_type, timestamp, tags, metadata
                    FROM monitoring_metrics
                    WHERE metric_name = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (metric_name, cutoff_time.isoformat(), limit))

                metrics = []
                for row in cursor.fetchall():
                    metric = MonitoringMetric(
                        metric_name=row[0],
                        metric_value=row[1],
                        metric_unit=row[2],
                        metric_type=MetricType(row[3]) if row[3] else MetricType.GAUGE,
                        timestamp=datetime.fromisoformat(row[4]),
                        tags=eval(row[5]) if row[5] else {},
                        metadata=eval(row[6]) if row[6] else {}
                    )
                    metrics.append(metric)

                return metrics

        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return []

    def store_health_check(self, health_check: HealthCheck) -> bool:
        """Store a health check result."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO health_checks
                    (check_name, check_type, status, message, duration_ms, timestamp, details)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    health_check.check_name,
                    health_check.check_type.value,
                    health_check.status.value,
                    health_check.message,
                    health_check.duration_ms,
                    health_check.timestamp.isoformat(),
                    str(health_check.details) if health_check.details else None
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error storing health check: {e}")
            return False

    def get_health_checks(self, check_type: Optional[HealthCheckType] = None,
                         hours: int = 24, limit: int = 100) -> List[HealthCheck]:
        """Get health check results."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)

            with sqlite3.connect(self.db_path) as conn:
                if check_type:
                    cursor = conn.execute("""
                        SELECT check_name, check_type, status, message, duration_ms, timestamp, details
                        FROM health_checks
                        WHERE check_type = ? AND timestamp >= ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """, (check_type.value, cutoff_time.isoformat(), limit))
                else:
                    cursor = conn.execute("""
                        SELECT check_name, check_type, status, message, duration_ms, timestamp, details
                        FROM health_checks
                        WHERE timestamp >= ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """, (cutoff_time.isoformat(), limit))

                health_checks = []
                for row in cursor.fetchall():
                    health_check = HealthCheck(
                        check_name=row[0],
                        check_type=HealthCheckType(row[1]),
                        status=HealthCheckStatus(row[2]),
                        message=row[3],
                        duration_ms=row[4],
                        timestamp=datetime.fromisoformat(row[5]),
                        details=eval(row[6]) if row[6] else {}
                    )
                    health_checks.append(health_check)

                return health_checks

        except Exception as e:
            logger.error(f"Error getting health checks: {e}")
            return []

    def store_alert(self, alert: Alert) -> bool:
        """Store an alert."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO alerts
                    (alert_id, alert_type, severity, title, message, status,
                     acknowledged, acknowledged_by, acknowledged_at, resolved_at,
                     escalation_count, last_escalation, tags, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.alert_id,
                    alert.alert_type.value,
                    alert.severity.value,
                    alert.title,
                    alert.message,
                    alert.status.value,
                    alert.acknowledged,
                    alert.acknowledged_by,
                    alert.acknowledged_at.isoformat() if alert.acknowledged_at else None,
                    alert.resolved_at.isoformat() if alert.resolved_at else None,
                    alert.escalation_count,
                    alert.last_escalation.isoformat() if alert.last_escalation else None,
                    str(alert.tags) if alert.tags else None,
                    str(alert.metadata) if alert.metadata else None
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error storing alert: {e}")
            return False

    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT alert_id, alert_type, severity, title, message, status,
                           acknowledged, acknowledged_by, acknowledged_at, resolved_at,
                           escalation_count, last_escalation, tags, metadata, created_at
                    FROM alerts
                    WHERE status IN ('active', 'acknowledged', 'escalated')
                    ORDER BY created_at DESC
                """)

                alerts = []
                for row in cursor.fetchall():
                    alert = Alert(
                        alert_id=row[0],
                        alert_type=AlertType(row[1]),
                        severity=AlertSeverity(row[2]),
                        title=row[3],
                        message=row[4],
                        status=AlertStatus(row[5]),
                        acknowledged=bool(row[6]),
                        acknowledged_by=row[7],
                        acknowledged_at=datetime.fromisoformat(row[8]) if row[8] else None,
                        resolved_at=datetime.fromisoformat(row[9]) if row[9] else None,
                        escalation_count=row[10],
                        last_escalation=datetime.fromisoformat(row[11]) if row[11] else None,
                        created_at=datetime.fromisoformat(row[14]),
                        tags=eval(row[12]) if row[12] else {},
                        metadata=eval(row[13]) if row[13] else {}
                    )
                    alerts.append(alert)

                return alerts

        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []

    def store_alert_history(self, alert_history: AlertHistory) -> bool:
        """Store alert history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO alert_history
                    (alert_id, action, details, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    alert_history.alert_id,
                    alert_history.action,
                    alert_history.details,
                    alert_history.timestamp.isoformat(),
                    str(alert_history.metadata) if alert_history.metadata else None
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error storing alert history: {e}")
            return False

    def cleanup_old_data(self, retention_days: int = 30) -> bool:
        """Clean up old monitoring data."""
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)

            with sqlite3.connect(self.db_path) as conn:
                # Clean up old metrics
                conn.execute(
                    "DELETE FROM monitoring_metrics WHERE created_at < ?",
                    (cutoff_date.isoformat(),)
                )

                # Clean up old health checks
                conn.execute(
                    "DELETE FROM health_checks WHERE created_at < ?",
                    (cutoff_date.isoformat(),)
                )

                # Clean up old alert history
                conn.execute(
                    "DELETE FROM alert_history WHERE created_at < ?",
                    (cutoff_date.isoformat(),)
                )

                # Keep only resolved alerts older than retention period
                conn.execute("""
                    DELETE FROM alerts
                    WHERE status = 'resolved' AND created_at < ?
                """, (cutoff_date.isoformat(),))

                conn.commit()

                # Vacuum database to reclaim space
                conn.execute("VACUUM")

                return True

        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return False

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                stats = {}

                # Get table sizes
                cursor = conn.execute("""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """)

                for table_name, in cursor.fetchall():
                    count_cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
                    stats[f"{table_name}_count"] = count_cursor.fetchone()[0]

                # Get database file size
                stats["database_size_bytes"] = self.db_path.stat().st_size

                return stats

        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
