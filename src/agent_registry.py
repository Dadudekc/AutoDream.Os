"""Shared agent registry for system-wide constants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


def _load_coordinates() -> Dict[str, Dict[str, Any]]:
    """Load agent coordinates from the cursor_agent_coords.json SSOT."""
    coord_file = Path("cursor_agent_coords.json")
    data = json.loads(coord_file.read_text(encoding="utf-8"))
    agents: Dict[str, Dict[str, Any]] = {}
    for agent_id, info in data.get("agents", {}).items():
        chat = info.get("chat_input_coordinates", [0, 0])
        agents[agent_id] = {
            "x": chat[0],
            "y": chat[1],
            "description": info.get("description", ""),
        }
    return agents


COORDINATES: Dict[str, Dict[str, Any]] = _load_coordinates()

