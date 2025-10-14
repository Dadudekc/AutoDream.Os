"""
Coordinate Management Utilities
==============================

Utility functions for loading and managing agent coordinates.
"""

import json
from pathlib import Path
from typing import Any


def load_coords_file() -> dict[str, Any]:
    """
    Load agent coordinates from cursor_agent_coords.json.

    Returns:
        Dictionary of agent coordinates
    """
    try:
        coord_file = Path("cursor_agent_coords.json")
        if not coord_file.exists():
            return {}

        data = json.loads(coord_file.read_text(encoding="utf-8"))
        agents = data.get("agents", {})

        # Transform to expected format
        result = {}
        for agent_id, info in agents.items():
            chat_coords = info.get("chat_input_coordinates", [0, 0])
            result[agent_id] = {
                "x": chat_coords[0],
                "y": chat_coords[1],
                "description": info.get("description", ""),
                "active": info.get("active", True),
            }

        return result

    except Exception as e:
        print(f"Error loading coordinates: {e}")
        return {}
