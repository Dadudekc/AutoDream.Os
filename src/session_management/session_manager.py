"""Unified session manager with pluggable persistence backends."""
from __future__ import annotations

import logging
import secrets
import time
from typing import Dict, Optional

from .backends import SessionBackend, SessionData


class SessionManager:
    """Create, validate and manage user sessions."""

    def __init__(
        self,
        backend: SessionBackend,
        session_timeout: int = 3600,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.backend = backend
        self.session_timeout = session_timeout
        self.active_sessions: Dict[str, SessionData] = {}
        self.logger = logger or logging.getLogger(__name__)

    def create_session(
        self,
        user_id: str,
        ip_address: str,
        user_agent: str,
        metadata: Optional[Dict[str, object]] = None,
    ) -> SessionData:
        """Generate and persist a new session."""
        session_id = secrets.token_urlsafe(32)
        current = time.time()
        session = SessionData(
            session_id=session_id,
            user_id=user_id,
            created_at=current,
            last_activity=current,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=current + self.session_timeout,
            metadata=metadata or {},
        )
        self.backend.save(session)
        self.active_sessions[session_id] = session
        return session

    def validate_session(self, session_id: str) -> Optional[SessionData]:
        """Validate and refresh a session by ID."""
        session = self.active_sessions.get(session_id)
        if session and self._is_valid(session):
            self._touch(session)
            return session

        session = self.backend.load(session_id)
        if session and self._is_valid(session):
            self.active_sessions[session_id] = session
            self._touch(session)
            return session
        return None

    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate a session by ID."""
        self.active_sessions.pop(session_id, None)
        try:
            self.backend.deactivate(session_id)
            return True
        except Exception as exc:  # pragma: no cover - protective logging
            self.logger.error("Failed to invalidate session %s: %s", session_id, exc)
            return False

    def cleanup_expired_sessions(self) -> None:
        """Remove expired sessions from cache and backend."""
        expired = [sid for sid, sess in self.active_sessions.items() if not self._is_valid(sess)]
        for sid in expired:
            del self.active_sessions[sid]
            self.backend.deactivate(sid)
        if expired:
            self.logger.info("Cleaned up %d expired sessions", len(expired))

    def invalidate_all_sessions(self) -> None:
        """Invalidate all sessions."""
        self.active_sessions.clear()
        self.backend.deactivate_all()

    def flush(self) -> None:
        """Flush backend resources."""
        self.backend.flush()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _touch(self, session: SessionData) -> None:
        session.last_activity = time.time()
        self.backend.save(session)

    def _is_valid(self, session: SessionData) -> bool:
        if not session.is_active:
            return False
        current = time.time()
        if session.expires_at and current > session.expires_at:
            return False
        return (current - session.last_activity) <= self.session_timeout
