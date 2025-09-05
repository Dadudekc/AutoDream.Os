"""Tests for agent registry utilities."""

from src.services.agent_registry import COORDINATES, format_agent_list
from src.services.handlers.utility_handler import UtilityHandler
from src.services.messaging_handlers_engine import MessagingHandlersEngine


def test_format_agent_list_returns_standard_structure():
    agents = ["Agent-2", "Agent-1"]
    result = format_agent_list(agents)
    assert result["success"] is True
    assert result["data"]["agents"] == ["Agent-1", "Agent-2"]
    assert result["data"]["agent_count"] == 2
    assert "Available agents" in result["message"]


def test_coordinates_mapping_is_accessible():
    handler = UtilityHandler()
    assert handler.get_coordinates() == COORDINATES


def test_engine_uses_registry_coordinates():
    engine = MessagingHandlersEngine()
    for agent_id, coords in COORDINATES.items():
        coord = engine.get_agent_coordinates(agent_id)
        assert coord is not None
        assert coord.x == coords["x"]
        assert coord.y == coords["y"]
