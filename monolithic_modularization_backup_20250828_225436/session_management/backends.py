"""Backend implementations for the unified session manager."""
from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Protocol


@dataclass
class SessionData:
    """Serializable session information."""

    session_id: str
    user_id: str
    created_at: float
    last_activity: float
    ip_address: str
    user_agent: str
    is_active: bool = True
    expires_at: Optional[float] = None
    metadata: Dict[str, object] = field(default_factory=dict)


class SessionBackend(Protocol):
    """Protocol for session persistence backends."""

    def save(self, session: SessionData) -> None:
        """Persist session information."""

    def load(self, session_id: str) -> Optional[SessionData]:
        """Retrieve session information by ID."""

    def deactivate(self, session_id: str) -> None:
        """Mark a session as inactive."""

    def deactivate_all(self) -> None:
        """Mark all sessions as inactive."""

    def flush(self) -> None:
        """Flush cached data and close resources."""


class MemorySessionBackend:
    """In-memory backend for session storage."""

    def __init__(self) -> None:
        self.sessions: Dict[str, SessionData] = {}

    def save(self, session: SessionData) -> None:
        self.sessions[session.session_id] = session

    def load(self, session_id: str) -> Optional[SessionData]:
        return self.sessions.get(session_id)

    def deactivate(self, session_id: str) -> None:
        session = self.sessions.get(session_id)
        if session:
            session.is_active = False

    def deactivate_all(self) -> None:
        for session in self.sessions.values():
            session.is_active = False

    def flush(self) -> None:
        self.sessions.clear()


class SQLiteSessionBackend:
    """SQLite-backed session storage backend."""

    def __init__(self, db_path: str, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(__name__)
        path = Path(db_path)
        try:
            self.db = sqlite3.connect(path)
            self.db.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    created_at REAL,
                    last_activity REAL,
                    ip_address TEXT,
                    user_agent TEXT,
                    is_active INTEGER,
                    expires_at REAL,
                    metadata TEXT
                )
                """
            )
            self.db.commit()
        except Exception as exc:  # pragma: no cover - initialization failure
            self.logger.error("Failed to initialize session database: %s", exc)
            self.db = None

    def save(self, session: SessionData) -> None:
        if not self.db:
            return
        try:
            with self.db:
                self.db.execute(
                    """
                    INSERT OR REPLACE INTO sessions (
                        session_id, user_id, created_at, last_activity,
                        ip_address, user_agent, is_active, expires_at, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session.session_id,
                        session.user_id,
                        session.created_at,
                        session.last_activity,
                        session.ip_address,
                        session.user_agent,
                        int(session.is_active),
                        session.expires_at,
                        json.dumps(session.metadata),
                    ),
                )
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to store session: %s", exc)

    def load(self, session_id: str) -> Optional[SessionData]:
        if not self.db:
            return None
        try:
            cursor = self.db.execute(
                """
                SELECT session_id, user_id, created_at, last_activity,
                       ip_address, user_agent, is_active, expires_at, metadata
                FROM sessions WHERE session_id = ?
                """,
                (session_id,),
            )
            row = cursor.fetchone()
            if row:
                return SessionData(
                    session_id=row[0],
                    user_id=row[1],
                    created_at=row[2],
                    last_activity=row[3],
                    ip_address=row[4],
                    user_agent=row[5],
                    is_active=bool(row[6]),
                    expires_at=row[7],
                    metadata=json.loads(row[8] or "{}"),
                )
            return None
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to load session: %s", exc)
            return None

    def deactivate(self, session_id: str) -> None:
        if not self.db:
            return
        try:
            with self.db:
                self.db.execute(
                    "UPDATE sessions SET is_active = 0 WHERE session_id = ?",
                    (session_id,),
                )
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to deactivate session: %s", exc)

    def deactivate_all(self) -> None:
        if not self.db:
            return
        try:
            with self.db:
                self.db.execute("UPDATE sessions SET is_active = 0")
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to deactivate sessions: %s", exc)

    def flush(self) -> None:
        if not self.db:
            return
        try:
            self.db.commit()
            self.db.close()
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to close session database: %s", exc)
