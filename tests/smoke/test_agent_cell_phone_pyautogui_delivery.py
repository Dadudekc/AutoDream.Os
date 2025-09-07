#!/usr/bin/env python3
"""Smoke test verifying direct PyAutoGUI delivery when available."""

import sys

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
import types

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import services.agent_cell_phone as acp


def test_pyautogui_direct_delivery(monkeypatch):
    """Ensure send uses PyAutoGUI when available."""
    events = []

    mock_pg = types.SimpleNamespace()

    def click(x, y):
        events.append(("click", x, y))

    def typewrite(text, interval=0.0):
        events.append(("type", text))

    def press(key):
        events.append(("press", key))

    def hotkey(*keys):
        events.append(("hotkey", keys))

    mock_pg.click = click
    mock_pg.typewrite = typewrite
    mock_pg.press = press
    mock_pg.hotkey = hotkey

    # Enable PyAutoGUI path
    monkeypatch.setattr(acp, "pyautogui", mock_pg)
    monkeypatch.setattr(acp, "PYAUTOGUI_AVAILABLE", True)

    system = acp.AgentCellPhone(test=True)

    # Do not allow router fallback
    router_called = {"called": False}

    def fake_send_message(*args, **kwargs):
        router_called["called"] = True
        return True

    monkeypatch.setattr(system, "send_message", fake_send_message)

    # Provide coordinates for agent
    def fake_get_config(section, key=None, default=None):
        return {
            "agent_config": {"agent_coordinates": {"agent_1": {"x": 10, "y": 20}}}
        }

    monkeypatch.setattr(system.config_manager, "get_config", fake_get_config)

    system.send("agent_1", "hello", acp.MsgTag.NORMAL)
    system.stop()

    assert ("click", 10, 20) in events
    assert ("type", "hello") in events
    assert ("press", "enter") in events
    assert not router_called["called"]
