"""
Mock Coordinate Loader for Testing
==================================

Provides mock coordinate loading functionality for smoke testing.
"""

from typing import Dict, Tuple, List, Optional, Any
import json
from pathlib import Path


def _load_coordinates() -> Dict[str, Dict[str, Any]]:
    """Load agent coordinates from the cursor_agent_coords.json SSOT."""
    coord_file = Path("cursor_agent_coords.json")
    data = json.loads(coord_file.read_text(encoding="utf-8"))
    agents: Dict[str, Dict[str, Any]] = {}
    for agent_id, info in data.get("agents", {}).items():
        chat = info.get("chat_input_coordinates", [0, 0])
        onboarding = info.get("onboarding_input_coords", chat)  # Fallback to chat if not present
        agents[agent_id] = {
            "coords": tuple(chat),  # Store as tuple for coordinate loader
            "onboarding_coords": tuple(onboarding),  # Onboarding coordinates
            "x": chat[0],
            "y": chat[1],
            "description": info.get("description", ""),
        }
    return agents


COORDINATES: Dict[str, Dict[str, Any]] = _load_coordinates()


class CoordinateLoader:
    """Mock coordinate loader for testing."""

    def __init__(self):
        """Initialize coordinate loader."""
        self.coordinates = COORDINATES.copy()

    def get_all_agents(self) -> List[str]:
        """Get all agent IDs."""
        return list(self.coordinates.keys())

    def is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        return agent_id in self.coordinates

    def get_chat_coordinates(self, agent_id: str) -> Tuple[int, int]:
        """Get chat coordinates for agent."""
        if agent_id in self.coordinates:
            return self.coordinates[agent_id]["coords"]
        raise ValueError(f"No coordinates found for agent {agent_id}")

    def get_onboarding_coordinates(self, agent_id: str) -> Tuple[int, int]:
        """Get onboarding coordinates for agent."""
        if agent_id in self.coordinates:
            return self.coordinates[agent_id]["onboarding_coords"]
        raise ValueError(f"No onboarding coordinates found for agent {agent_id}")

    def get_agent_description(self, agent_id: str) -> str:
        """Get agent description."""
        if agent_id in self.coordinates:
            return self.coordinates[agent_id].get("description", "")
        return ""

    def get_agent_info(self, agent_id: str) -> Optional[Dict]:
        """Get agent information."""
        return self.coordinates.get(agent_id)


# Global coordinate loader instance
_coordinate_loader = None


def get_coordinate_loader() -> CoordinateLoader:
    """Get global coordinate loader instance."""
    global _coordinate_loader
    if _coordinate_loader is None:
        _coordinate_loader = CoordinateLoader()
    return _coordinate_loader
