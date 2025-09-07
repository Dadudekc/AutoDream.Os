"""Tests for agent registry utility."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.services.utils.agent_registry import list_agents


def test_list_agents_contains_expected_agents():
    agents = list_agents()
    assert "Agent-1" in agents
    assert "Agent-8" in agents
    assert len(agents) >= 8
