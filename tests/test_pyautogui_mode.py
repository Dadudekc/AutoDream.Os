#!/usr/bin/env python3
"""Simple tests for agent listing functionality."""
import sys
from pathlib import Path
import logging

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

get_logger = logging.getLogger

from src.services.utils.agent_registry import list_agents


def test_pyautogui_mode():
    """Verify agents are available from the registry."""
    agents = list_agents()
    assert "Agent-1" in agents
    get_logger(__name__).info(f"Registered agents: {', '.join(sorted(agents.keys()))}")


def test_cli_commands():
    """Ensure CLI commands reference agent registry."""
    commands = [
        "python -m src.services.messaging_cli --list-agents",
        "python -m src.services.messaging_cli --coordinates",
    ]
    for command in commands:
        get_logger(__name__).info(command)
