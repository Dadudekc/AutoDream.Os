#!/usr/bin/env python3
"""Audit logging utilities."""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import json
import logging
import sqlite3
import time


@dataclass
class AuditEvent:
    """Audit event structure."""

    timestamp: float
    user_id: str
    action: str
    resource: str
    details: Dict
    ip_address: str
    user_agent: str
    session_id: Optional[str] = None
    outcome: str = "success"


class AuditLogger:
    """Comprehensive audit logging system."""

    def __init__(self, db_file: str = "audit.db") -> None:
        self.logger = logging.getLogger(__name__)
        self.db_file = db_file
        self.audit_events: List[AuditEvent] = []
        self._init_audit_database()

    def log_audit_event(
        self,
        user_id: str,
        action: str,
        resource: str,
        details: Dict,
        ip_address: str,
        user_agent: str | None = None,
        session_id: str | None = None,
        outcome: str = "success",
    ) -> Dict:
        """Log audit event to database and memory."""
        try:
            timestamp = time.time()
            audit_event = AuditEvent(
                timestamp=timestamp,
                user_id=user_id,
                action=action,
                resource=resource,
                details=details,
                ip_address=ip_address,
                user_agent=user_agent or "unknown",
                session_id=session_id,
                outcome=outcome,
            )
            self.audit_events.append(audit_event)
            self._store_audit_event(audit_event)
            self.logger.info(
                "AUDIT: %s performed %s on %s - %s", user_id, action, resource, outcome
            )
            return asdict(audit_event)
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to log audit event: %s", exc)
            return {}

    def get_audit_trail(
        self,
        user_id: str | None = None,
        resource: str | None = None,
        action: str | None = None,
        start_time: float | None = None,
        end_time: float | None = None,
    ) -> List[Dict]:
        """Retrieve audit trail with optional filtering."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            query = "SELECT * FROM audit_events WHERE 1=1"
            params: List = []
            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)
            if resource:
                query += " AND resource = ?"
                params.append(resource)
            if action:
                query += " AND action = ?"
                params.append(action)
            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time)
            if end_time:
                query += " AND timestamp <= ?"
                params.append(end_time)
            query += " ORDER BY timestamp DESC"
            cursor.execute(query, params)
            events = cursor.fetchall()
            conn.close()
            audit_trail: List[Dict] = []
            for event in events:
                event_dict = {
                    "timestamp": event[0],
                    "user_id": event[1],
                    "action": event[2],
                    "resource": event[3],
                    "details": json.loads(event[4]) if event[4] else {},
                    "ip_address": event[5],
                    "user_agent": event[6],
                    "session_id": event[7],
                    "outcome": event[8],
                }
                audit_trail.append(event_dict)
            return audit_trail
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to retrieve audit trail: %s", exc)
            return []

    def _init_audit_database(self) -> None:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    timestamp REAL NOT NULL,
                    user_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT NOT NULL,
                    user_agent TEXT,
                    session_id TEXT,
                    outcome TEXT DEFAULT 'success'
                )
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_events(user_id)"
            )
            conn.commit()
            conn.close()
            self.logger.info("Audit database initialized successfully")
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to initialize audit database: %s", exc)

    def _store_audit_event(self, audit_event: AuditEvent) -> None:
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO audit_events
                (timestamp, user_id, action, resource, details, ip_address, user_agent, session_id, outcome)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_event.timestamp,
                    audit_event.user_id,
                    audit_event.action,
                    audit_event.resource,
                    json.dumps(audit_event.details),
                    audit_event.ip_address,
                    audit_event.user_agent,
                    audit_event.session_id,
                    audit_event.outcome,
                ),
            )
            conn.commit()
            conn.close()
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to store audit event: %s", exc)
