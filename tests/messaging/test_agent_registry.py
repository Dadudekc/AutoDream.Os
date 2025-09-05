"""Tests for agent registry utilities."""

from src.services.agent_registry import format_agent_list
from src.services.utils.agent_registry import list_agents


def test_format_agent_list_returns_standard_structure():
    agents = list_agents()
    result = format_agent_list(agents)
    assert result["success"] is True
    assert result["data"]["agents"] == agents
    assert result["data"]["agent_count"] == len(agents)
    assert "Available agents" in result["message"]
