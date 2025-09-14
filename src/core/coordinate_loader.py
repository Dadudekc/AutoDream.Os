#!/usr/bin/env python3
"""
Coordinate Loader - Load agent coordinates from JSON files
========================================================

Loads agent coordinates from cursor_agent_coords.json or config/coordinates.json.

Author: Agent-8 (Operations & Swarm Coordinator)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def load_coordinates_from_json() -> Dict[str, List[int]]:
    """Load agent coordinates from JSON files."""
    coords = {}
    
    # Try cursor_agent_coords.json first
    cursor_file = Path("cursor_agent_coords.json")
    if cursor_file.exists():
        try:
            with open(cursor_file, 'r') as f:
                data = json.load(f)
                for agent_id, agent_data in data.get("agents", {}).items():
                    coords[agent_id] = agent_data.get("chat_input_coordinates", [0, 0])
                logger.info(f"Loaded coordinates from {cursor_file}")
                return coords
        except Exception as e:
            logger.warning(f"Failed to load coordinates from {cursor_file}: {e}")
    
    # Try config/coordinates.json as fallback
    config_file = Path("config/coordinates.json")
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                for agent_id, agent_data in data.get("agents", {}).items():
                    coords[agent_id] = agent_data.get("chat_input_coordinates", [0, 0])
                logger.info(f"Loaded coordinates from {config_file}")
                return coords
        except Exception as e:
            logger.warning(f"Failed to load coordinates from {config_file}: {e}")
    
    logger.warning("No coordinate files found")
    return coords


def get_agent_coordinates(agent_id: str) -> Optional[List[int]]:
    """Get coordinates for a specific agent."""
    coords_dict = load_coordinates_from_json()
    return coords_dict.get(agent_id)


class CoordinateLoader:
    """Coordinate loader class with get_chat_coordinates method."""
    
    def __init__(self):
        self._coordinates = load_coordinates_from_json()
    
    def get_chat_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get chat coordinates for a specific agent."""
        coords = self._coordinates.get(agent_id)
        if coords and len(coords) >= 2:
            return (coords[0], coords[1])
        return None
    
    def get_all_coordinates(self) -> Dict[str, List[int]]:
        """Get all coordinates."""
        return self._coordinates
    
    def get_all_agents(self) -> List[str]:
        """Get all agent IDs."""
        return list(self._coordinates.keys())
    
    def is_agent_active(self, agent_id: str) -> bool:
        """Check if an agent has coordinates."""
        return agent_id in self._coordinates


def get_coordinate_loader():
    """Get the coordinate loader instance."""
    return CoordinateLoader()
