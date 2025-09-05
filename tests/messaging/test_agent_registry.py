"""Tests for agent registry utilities."""

from src.services.handlers.utility_handler import UtilityHandler
from src.services.messaging_handlers_engine import MessagingHandlersEngine
from src.services.utils.agent_registry import AGENTS, list_agents


def test_list_agents_returns_sorted_keys():
    agents = list_agents()
    assert agents == sorted(AGENTS.keys())


def test_utility_handler_lists_agents_from_registry():
    handler = UtilityHandler()
    expected = [
        f"{agent_id}: {AGENTS[agent_id]['description']}" for agent_id in list_agents()
    ]
    assert handler.list_agents() == expected


def test_engine_uses_registry_coordinates():
    engine = MessagingHandlersEngine()
    for agent_id in list_agents():
        coord = engine.get_agent_coordinates(agent_id)
        coords = AGENTS[agent_id]["coords"]
        assert coord is not None
        assert coord.x == coords["x"]
        assert coord.y == coords["y"]
