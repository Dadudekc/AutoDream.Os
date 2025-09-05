"""Tests for agent registry utilities."""

from src.services.utils.agent_registry import (
    AGENTS,
    format_agent_list,
    list_agents,
)


def test_format_agent_list_returns_standard_structure():
    agents = ["Agent-2", "Agent-1"]
    result = format_agent_list(agents)
    assert result["success"] is True
    assert result["data"]["agents"] == ["Agent-1", "Agent-2"]
    assert result["data"]["agent_count"] == 2
    assert "Available agents" in result["message"]


def test_list_agents_matches_registry_keys():
    assert set(list_agents()) == set(AGENTS.keys())
