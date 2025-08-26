"""Session storage selector for the auth service.

Delegates persistence to a configured backend implementation.
"""
from __future__ import annotations

import logging
from typing import Dict, Optional

from .session_backend import (
    SessionBackend,
    MemorySessionBackend,
    SQLiteSessionBackend,
)


class SessionStore:
    """Store session data using a selectable backend."""

    def __init__(
        self,
        backend: str = "memory",
        db_path: str = "auth_sessions.db",
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        if backend == "sqlite":
            self.backend: SessionBackend = SQLiteSessionBackend(db_path, self.logger)
        elif backend == "memory":
            self.backend = MemorySessionBackend()
        else:
            self.logger.warning("Unknown session backend '%s', defaulting to 'memory'.", backend)
            self.backend = MemorySessionBackend()

    def store(self, session_data: Dict[str, object]) -> None:
        """Persist the provided session data."""
        self.backend.store(session_data)

    def flush(self) -> None:
        """Flush sessions and close resources."""
        self.backend.flush()
