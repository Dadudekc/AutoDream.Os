"""Shared agent registry for system-wide constants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load_coordinates() -> dict[str, dict[str, Any]]:
    """Load agent coordinates from the coordinates.json SSOT."""
    coord_file = Path("config/coordinates.json")
    data = json.loads(coord_file.read_text(encoding="utf-8"))
    agents: dict[str, dict[str, Any]] = {}
    for agent_id, info in data.get("agents", {}).items():
        chat = info.get("chat_input_coordinates", [0, 0])
        agents[agent_id] = {
            "x": chat[0],
            "y": chat[1],
            "description": info.get("description", ""),
        }
    return agents


COORDINATES: dict[str, dict[str, Any]] = _load_coordinates()
