"""Coordinate agent registry for system-wide coordinate constants."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def _load_coordinates() -> dict[str, dict[str, Any]]:
    """Load agent coordinates from the cursor_agent_coords.json SSOT."""
    # Try to find the coordinate file in the project root
    coord_file = Path(__file__).parent.parent / "cursor_agent_coords.json"
    if not coord_file.exists():
        # Fallback to current directory
        coord_file = Path("cursor_agent_coords.json")

    data = json.loads(coord_file.read_text(encoding="utf-8"))
    agents: dict[str, dict[str, Any]] = {}
    for agent_id, info in data.get("agents", {}).items():
        chat = info.get("chat_input_coordinates", [0, 0])
        agents[agent_id] = {
            "coords": tuple(chat),  # Store as tuple for coordinate loader
            "x": chat[0],
            "y": chat[1],
            "description": info.get("description", ""),
        }
    return agents


COORDINATES: dict[str, dict[str, Any]] = _load_coordinates()
