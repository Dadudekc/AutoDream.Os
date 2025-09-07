#!/usr/bin/env python3
"""Smoke Test - AgentCellPhone
===============================
Basic smoke test for the canonical AgentCellPhone service to ensure it
initializes correctly and exposes system status and conversation history.
"""

import os
import sys

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from services.agent_cell_phone import AgentCellPhone


def test_agent_cell_phone_cleanup():
    """Ensure AgentCellPhone stops all resources when test finishes."""
    os.environ["ACP_HEARTBEAT_SEC"] = "0"
    system = AgentCellPhone(test=True)
    try:
        # basic check to ensure system initialized
        assert system.agent_manager is not None
    finally:
        system.stop()
        os.environ.pop("ACP_HEARTBEAT_SEC", None)

    # Ensure background threads have stopped
    assert system._hb_thread is None or not system._hb_thread.is_alive()
    assert system._listener_thread is None or not system._listener_thread.is_alive()


def test_history_accessible():
    """AgentCellPhone should expose conversation history list."""
    system = AgentCellPhone(test=True)
    history = system.get_conversation_history()
    assert isinstance(history, list)
