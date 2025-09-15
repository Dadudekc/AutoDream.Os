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
    """Coordinate loader class with validation and routing safeguards."""
    
    def __init__(self):
        self._coordinates = load_coordinates_from_json()
        self._validated_agents = set()
        self._validation_errors = {}
    
    def validate_coordinates(self, agent_id: str) -> Tuple[bool, str]:
        """Validate coordinates for a specific agent."""
        if agent_id not in self._coordinates:
            return False, f"Agent {agent_id} not found in coordinate file"
        
        coords = self._coordinates[agent_id]
        if not coords or len(coords) < 2:
            return False, f"Invalid coordinates for {agent_id}: {coords}"
        
        x, y = coords[0], coords[1]
        
        # Check for valid coordinate ranges (basic screen bounds)
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            return False, f"Non-numeric coordinates for {agent_id}: {coords}"
        
        if x < -10000 or x > 10000 or y < -10000 or y > 10000:
            return False, f"Coordinates out of reasonable range for {agent_id}: ({x}, {y})"
        
        # Check for default/invalid coordinates
        if x == 0 and y == 0:
            return False, f"Default coordinates (0,0) for {agent_id} - likely not configured"
        
        return True, "Valid coordinates"
    
    def get_chat_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get chat coordinates for a specific agent with validation."""
        # Validate coordinates before returning
        is_valid, error_msg = self.validate_coordinates(agent_id)
        if not is_valid:
            logger.error(f"❌ Coordinate validation failed for {agent_id}: {error_msg}")
            self._validation_errors[agent_id] = error_msg
            return None
        
        coords = self._coordinates.get(agent_id)
        if coords and len(coords) >= 2:
            self._validated_agents.add(agent_id)
            return (coords[0], coords[1])
        return None
    
    def get_all_coordinates(self) -> Dict[str, List[int]]:
        """Get all coordinates."""
        return self._coordinates
    
    def get_all_agents(self) -> List[str]:
        """Get all agent IDs."""
        return list(self._coordinates.keys())
    
    def get_valid_agents(self) -> List[str]:
        """Get list of agents with valid coordinates."""
        valid_agents = []
        for agent_id in self._coordinates.keys():
            is_valid, _ = self.validate_coordinates(agent_id)
            if is_valid:
                valid_agents.append(agent_id)
        return valid_agents
    
    def is_agent_active(self, agent_id: str) -> bool:
        """Check if an agent has valid coordinates."""
        is_valid, _ = self.validate_coordinates(agent_id)
        return is_valid
    
    def get_validation_report(self) -> Dict[str, any]:
        """Get a comprehensive validation report."""
        report = {
            "total_agents": len(self._coordinates),
            "valid_agents": [],
            "invalid_agents": [],
            "validation_errors": self._validation_errors.copy()
        }
        
        for agent_id in self._coordinates.keys():
            is_valid, error_msg = self.validate_coordinates(agent_id)
            if is_valid:
                report["valid_agents"].append(agent_id)
            else:
                report["invalid_agents"].append(agent_id)
                if agent_id not in report["validation_errors"]:
                    report["validation_errors"][agent_id] = error_msg
        
        return report


def get_coordinate_loader():
    """Get the coordinate loader instance."""
    return CoordinateLoader()
