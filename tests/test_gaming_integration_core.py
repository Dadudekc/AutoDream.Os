import pytest

from gaming.integration.core import GamingIntegrationCore, GameType


def test_session_lifecycle():
    core = GamingIntegrationCore()
    session = core.create_game_session(GameType.ACTION, "player1")
    assert session.session_id in core.game_sessions
    assert core.end_game_session(session.session_id)
    assert core.get_system_status()["active_sessions"] == 0
