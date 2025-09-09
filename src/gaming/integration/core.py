"""Core integration logic for gaming systems."""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any

from .models import EntertainmentSystem, GameSession, GameType, IntegrationStatus

logger = logging.getLogger(__name__)


class GamingIntegrationCore:
    """Simplified gaming integration core used by tests and services."""

    # Re-export GameType for backward compatibility
    GameType = GameType

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.status = IntegrationStatus.DISCONNECTED
        self.game_sessions: dict[str, GameSession] = {}
        self.entertainment_systems: dict[str, EntertainmentSystem] = {}
        self.handlers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}
        self.is_initialized = False
        self._initialize()

    def _initialize(self) -> None:
        """Initialize integration and register handlers."""
        try:
            self._setup_handlers()
            self.status = IntegrationStatus.CONNECTED
            self.is_initialized = True
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("Initialization failed: %s", exc)
            self.status = IntegrationStatus.ERROR

    def _setup_handlers(self) -> None:
        self.handlers = {
            "session_management": self._handle_session_management,
            "system_health": self._handle_system_health,
        }

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------
    def create_game_session(
        self,
        game_type: GameType,
        player_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> GameSession:
        """Create and register a new game session."""
        session_id = f"session_{int(datetime.now().timestamp())}"
        session = GameSession(
            session_id=session_id,
            game_type=game_type,
            player_id=player_id,
            start_time=datetime.now(),
            status="active",
            metadata=metadata or {},
            performance_metrics={},
        )
        self.game_sessions[session_id] = session
        return session

    def end_game_session(self, session_id: str, end_metadata: dict[str, Any] | None = None) -> bool:
        """End a running game session."""
        session = self.game_sessions.get(session_id)
        if not session:
            return False
        session.status = "ended"
        if end_metadata:
            session.metadata.update(end_metadata)
        session.metadata["end_time"] = datetime.now().isoformat()
        return True

    def get_active_sessions(self) -> list[GameSession]:
        """Return all active sessions."""
        return [s for s in self.game_sessions.values() if s.status == "active"]

    # ------------------------------------------------------------------
    # System status
    # ------------------------------------------------------------------
    def get_system_status(self) -> dict[str, Any]:
        """Return high level integration status."""
        return {
            "status": self.status.value,
            "active_sessions": len(self.get_active_sessions()),
            "registered_systems": len(self.entertainment_systems),
        }

    # ------------------------------------------------------------------
    # Event processing
    # ------------------------------------------------------------------
    def _handle_session_management(self, event: dict[str, Any]) -> dict[str, Any]:
        event_type = event.get("type")
        if event_type == "create":
            game_type = GameType(event.get("game_type", GameType.ACTION.value))
            player_id = event.get("player_id", "unknown")
            session = self.create_game_session(game_type, player_id)
            return {"success": True, "session_id": session.session_id}
        if event_type == "end":
            session_id = event.get("session_id", "")
            return {"success": self.end_game_session(session_id)}
        return {"success": False, "error": "unknown event"}

    def _handle_system_health(self, event: dict[str, Any]) -> dict[str, Any]:
        return {"success": True, **self.get_system_status()}

    def process_event(self, event_type: str, event_data: dict[str, Any]) -> dict[str, Any]:
        """Process an integration event."""
        handler = self.handlers.get(event_type)
        if not handler:
            return {"success": False, "error": f"no handler for {event_type}"}
        return handler(event_data)

    # ------------------------------------------------------------------
    # Entertainment system registration (minimal)
    # ------------------------------------------------------------------
    def register_entertainment_system(self, system_id: str, system_type: str) -> bool:
        system = EntertainmentSystem(
            system_id=system_id,
            system_type=system_type,
            status=IntegrationStatus.CONNECTED,
            capabilities=[],
            configuration={},
            last_updated=datetime.now(),
        )
        self.entertainment_systems[system_id] = system
        return True
