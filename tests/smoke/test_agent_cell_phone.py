#!/usr/bin/env python3
"""Smoke Test - AgentCellPhone
===============================
Basic smoke test for the canonical AgentCellPhone service to ensure it
initializes correctly and exposes system status and conversation history.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from services.agent_cell_phone import AgentCellPhone


def test_history_accessible():
    """AgentCellPhone should expose conversation history list."""
    system = AgentCellPhone(test=True)
    history = system.get_conversation_history()
    assert isinstance(history, list)
