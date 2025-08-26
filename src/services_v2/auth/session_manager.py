"""Session creation and management utilities."""
from __future__ import annotations

import secrets
import time
from datetime import datetime
from typing import Any, Dict

from services_v2.auth.session_store import SessionStore


class SessionManager:
    """Create and persist session data through a SessionStore."""

    def __init__(
        self, store: SessionStore, session_timeout: int, security_level: str
    ) -> None:
        self.store = store
        self.session_timeout = session_timeout
        self.security_level = security_level

    def create_session(
        self, username: str, source_ip: str, user_agent: str
    ) -> Dict[str, Any]:
        """Generate and persist a new session."""
        session_id = secrets.token_urlsafe(32)
        current_time = time.time()
        expires_at = datetime.fromtimestamp(current_time + self.session_timeout)

        session_data = {
            "session_id": session_id,
            "user_id": username,
            "source_ip": source_ip,
            "user_agent": user_agent,
            "created_at": current_time,
            "expires_at": expires_at,
            "metadata": {
                "v2_features": True,
                "security_level": self.security_level,
                "session_type": "enhanced",
            },
        }

        self.store.store(session_data)
        return session_data

    def flush(self) -> None:
        """Flush sessions via the underlying store."""
        self.store.flush()
