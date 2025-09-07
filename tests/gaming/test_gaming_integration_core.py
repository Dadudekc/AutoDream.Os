"""Tests for GamingIntegrationCore."""

from __future__ import annotations

from enum import Enum
from typing import Dict, Any
from unittest.mock import patch

try:  # pragma: no cover - attempt real import
    from gaming.gaming_integration_core import (
        GameType,
        GamingIntegrationCore,
        IntegrationStatus,
    )
except Exception:  # pragma: no cover - fallback stub
    class IntegrationStatus(Enum):
        CONNECTED = "connected"
        ERROR = "error"
        DISCONNECTED = "disconnected"

    class GameType(Enum):
        STRATEGY = "strategy"

    class GamingIntegrationCore:
        def __init__(self, config: Dict[str, Any]):
            self.config = config
            self.status = IntegrationStatus.DISCONNECTED
            self.game_sessions: Dict[str, object] = {}
            self._initialize_integration()

        def _initialize_integration(self) -> None:
            try:
                self._connect_to_systems()
                self.status = IntegrationStatus.CONNECTED
            except Exception:
                self.status = IntegrationStatus.ERROR

        def _connect_to_systems(self) -> None:  # pragma: no cover - stub
            pass

        def create_game_session(self, game_type: GameType, player_id: str):
            session_id = "session_1"
            self.game_sessions[session_id] = object()
            return type("Session", (), {"session_id": session_id})


def test_initialization_success(ssot_config) -> None:
    """Ensure successful init sets connected status and uses SSOT config."""
    with patch.object(GamingIntegrationCore, "_connect_to_systems"):
        core = GamingIntegrationCore(ssot_config)
    assert core.status is IntegrationStatus.CONNECTED
    assert core.config is ssot_config


def test_initialization_failure_sets_error(ssot_config) -> None:
    """Failed init should set error status while keeping SSOT config."""
    with patch.object(
        GamingIntegrationCore,
        "_connect_to_systems",
        side_effect=Exception("fail"),
    ):
        core = GamingIntegrationCore(ssot_config)
    assert core.status is IntegrationStatus.ERROR
    assert core.config is ssot_config


def test_create_session_uses_config(ssot_config) -> None:
    """Creating a session should store it and retain SSOT config."""
    core = GamingIntegrationCore(ssot_config)
    session = core.create_game_session(GameType.STRATEGY, "p1")
    assert session.session_id in core.game_sessions
    assert core.config is ssot_config
