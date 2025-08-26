"""Session backend implementations for AuthService.

Defines lightweight backends for session persistence to keep
`SessionStore` focused on backend selection.
"""
from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Dict, Protocol


class SessionBackend(Protocol):
    """Protocol for session backend implementations."""

    def store(self, session_data: Dict[str, object]) -> None:
        """Persist session information."""

    def flush(self) -> None:
        """Flush cached sessions and release resources."""


class MemorySessionBackend:
    """In-memory session storage backend."""

    def __init__(self) -> None:
        self.sessions: Dict[str, Dict[str, object]] = {}

    def store(self, session_data: Dict[str, object]) -> None:
        self.sessions[session_data["session_id"]] = session_data

    def flush(self) -> None:
        self.sessions.clear()


class SQLiteSessionBackend:
    """SQLite-backed session storage backend."""

    def __init__(self, db_path: str, logger: logging.Logger) -> None:
        path = Path(db_path)
        self.logger = logger
        try:
            self.db = sqlite3.connect(path)
            self.db.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    source_ip TEXT,
                    user_agent TEXT,
                    created_at REAL,
                    expires_at TEXT,
                    metadata TEXT
                )
                """
            )
            self.db.commit()
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to initialize session database: %s", exc)
            self.db = None

    def store(self, session_data: Dict[str, object]) -> None:
        if not self.db:
            return
        try:
            with self.db:
                self.db.execute(
                    """
                    INSERT OR REPLACE INTO sessions (
                        session_id, user_id, source_ip, user_agent, created_at, expires_at, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session_data["session_id"],
                        session_data["user_id"],
                        session_data["source_ip"],
                        session_data["user_agent"],
                        session_data["created_at"],
                        session_data["expires_at"].isoformat(),
                        json.dumps(session_data.get("metadata", {})),
                    ),
                )
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to store session: %s", exc)

    def flush(self) -> None:
        if not self.db:
            return
        try:
            self.db.commit()
            self.db.close()
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to close session database: %s", exc)
