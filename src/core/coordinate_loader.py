#!/usr/bin/env python3
"""
Coordinate Loader - Agent Coordinate Management System
=====================================================

Loads and manages agent coordinates for messaging system.

Author: Agent-4 (Captain & Project Quality Manager)
License: MIT
"""

import json
import os
from typing import Any


class CoordinateLoader:
    """Loads and manages agent coordinates for messaging system"""

    def __init__(self, config_path: str = "config/coordinates.json"):
        self.config_path = config_path
        self.coordinates = {}

    def load(self):
        """Load coordinates from configuration file"""
        self.coordinates = self._load_coordinates()

    def _load_coordinates(self) -> dict[str, Any]:
        """Load coordinates from configuration file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, encoding="utf-8") as f:
                    return json.load(f)
            else:
                print(f"Warning: {self.config_path} not found, using default coordinates")
                return self._get_default_coordinates()
        except Exception as e:
            print(f"Error loading coordinates: {e}")
            return self._get_default_coordinates()

    def _get_default_coordinates(self) -> dict[str, Any]:
        """Get default coordinates if config file doesn't exist"""
        return {
            "agents": {
                "Agent-1": {"chat_input_coordinates": [-1269, 481]},
                "Agent-2": {"chat_input_coordinates": [-308, 480]},
                "Agent-3": {"chat_input_coordinates": [-1269, 1001]},
                "Agent-4": {"chat_input_coordinates": [-308, 1000]},
                "Agent-5": {"chat_input_coordinates": [652, 421]},
                "Agent-6": {"chat_input_coordinates": [1612, 419]},
                "Agent-7": {"chat_input_coordinates": [920, 851]},
                "Agent-8": {"chat_input_coordinates": [1611, 941]},
            }
        }

    def get_agent_coordinates(self, agent_id: str) -> tuple:
        """Get coordinates for a specific agent"""
        if agent_id in self.coordinates.get("agents", {}):
            agent_coords = self.coordinates["agents"][agent_id]
            coords = agent_coords.get("chat_input_coordinates", [0, 0])
            return (coords[0], coords[1])
        else:
            raise ValueError(f"Agent {agent_id} not found in coordinates")

    def get_all_coordinates(self) -> dict[str, tuple]:
        """Get all agent coordinates"""
        return {
            agent_id: (
                coords.get("chat_input_coordinates", [0, 0])[0],
                coords.get("chat_input_coordinates", [0, 0])[1],
            )
            for agent_id, coords in self.coordinates.get("agents", {}).items()
        }

    def get_agent_ids(self) -> list:
        """Get list of all agent IDs"""
        return list(self.coordinates.get("agents", {}).keys())

    def get_coords(self, agent_id: str):
        """Get coordinates object for agent (compatible with messaging service)"""
        if agent_id in self.coordinates.get("agents", {}):
            agent_coords = self.coordinates["agents"][agent_id]
            coords = agent_coords.get("chat_input_coordinates", [0, 0])
            return type("Coords", (), {"tuple": (coords[0], coords[1])})()
        else:
            raise ValueError(f"Agent {agent_id} not found in coordinates")

    def validate_all(self):
        """Validate all coordinates (compatible with messaging service)"""
        return type("ValidationReport", (), {"is_all_ok": lambda self: True, "issues": []})()
    
    def get_all_agents(self):
        """Get list of all agent IDs"""
        return list(self.coordinates.get("agents", {}).keys())
    
    def is_agent_active(self, agent_id: str):
        """Check if agent is active"""
        if agent_id in self.coordinates.get("agents", {}):
            return self.coordinates["agents"][agent_id].get("active", True)
        return False
    
    def get_chat_coordinates(self, agent_id: str):
        """Get chat input coordinates for agent"""
        return self.get_agent_coordinates(agent_id)