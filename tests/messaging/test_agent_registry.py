"""Tests for agent registry utilities."""

from src.services.agent_registry import format_agent_list


def test_format_agent_list_returns_standard_structure():
    agents = ["Agent-2", "Agent-1"]
    result = format_agent_list(agents)
    assert result["success"] is True
    assert result["data"]["agents"] == ["Agent-1", "Agent-2"]
    assert result["data"]["agent_count"] == 2
    assert "Available agents" in result["message"]
