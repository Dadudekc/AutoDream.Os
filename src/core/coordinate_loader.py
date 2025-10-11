#!/usr/bin/env python3
"""
Coordinate Loader - Agent Coordinate Management System
=====================================================

Loads and manages agent coordinates for messaging system.

Author: Agent-4 (Captain & Project Quality Manager)
License: MIT
"""

import json
<<<<<<< HEAD
import os
from typing import Dict, Any
=======
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

>>>>>>> origin/agent-3-v2-infrastructure-optimization

class CoordinateLoader:
    """Loads and manages agent coordinates for messaging system"""
    
    def __init__(self, config_path: str = "config/canonical_coordinates.json"):
        self.config_path = config_path
        self.canonical_path = "config/canonical_coordinates.json"
        self.coordinates = {}
    
    def load(self):
        """Load coordinates from configuration file"""
        self.coordinates = self._load_coordinates()
    
    def _load_coordinates(self) -> Dict[str, Any]:
        """Load coordinates preferring canonical SSOT; fallback to provided or defaults."""
        try:
            # Prefer canonical SSOT
            if os.path.exists(self.canonical_path):
                with open(self.canonical_path, 'r', encoding='utf-8') as f:
                    canonical = json.load(f)
            else:
                canonical = None

            # Load provided path if not canonical or for compatibility
            provided = None
            if self.config_path and os.path.exists(self.config_path) and self.config_path != self.canonical_path:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    provided = json.load(f)

            # Choose canonical if available; otherwise provided; otherwise defaults
            data = canonical if canonical is not None else (provided if provided is not None else self._get_default_coordinates())

            # If both exist, ensure no drift for agents present in canonical
            if canonical is not None and provided is not None:
                try:
                    for agent_key, coords in canonical.items():
                        if agent_key in provided and provided[agent_key] != coords:
                            print(f"Warning: coordinate drift detected for agent {agent_key}; using canonical value")
                            provided[agent_key] = coords
                    data = provided
                except Exception:
                    # If any issue, stick to canonical
                    data = canonical

            return {
                "agents": {
                    f"Agent-{k}": {"chat_input_coordinates": v} for k, v in data.items()
                }
            } if "agents" not in data else data
        except Exception as e:
            print(f"Error loading coordinates: {e}")
            return self._get_default_coordinates()
    
    def _get_default_coordinates(self) -> Dict[str, Any]:
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
                "Agent-8": {"chat_input_coordinates": [1611, 941]}
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
    
    def get_all_coordinates(self) -> Dict[str, tuple]:
        """Get all agent coordinates"""
        return {
            agent_id: (coords.get("chat_input_coordinates", [0, 0])[0], coords.get("chat_input_coordinates", [0, 0])[1])
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
            return type('Coords', (), {'tuple': (coords[0], coords[1])})()
        else:
            raise ValueError(f"Agent {agent_id} not found in coordinates")
    
    def validate_all(self):
        """Validate all coordinates (compatible with messaging service)"""
        issues = []
        try:
            # Basic shape and bounds validation
            for agent_id, data in self.coordinates.get("agents", {}).items():
                coords = data.get("chat_input_coordinates")
                if not isinstance(coords, list) or len(coords) < 2:
                    issues.append(f"Invalid format for {agent_id}")
                    continue
                x, y = coords[0], coords[1]
                if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                    issues.append(f"Non-numeric coordinates for {agent_id}")
                    continue
        except Exception as e:
            issues.append(f"Validation error: {e}")

<<<<<<< HEAD
        return type('ValidationReport', (), {
            'is_all_ok': lambda self: len(issues) == 0,
            'issues': issues
        })()
=======
    def get_onboarding_coordinates(self, agent_id: str) -> Tuple[int, int]:
        """Get onboarding coordinates for agent."""
        if agent_id in self.coordinates:
            return self.coordinates[agent_id]["onboarding_coords"]
        raise ValueError(f"No onboarding coordinates found for agent {agent_id}")
>>>>>>> origin/agent-3-v2-infrastructure-optimization

    def assert_canonical_consistency(self) -> None:
        """Raise if loaded coordinates drift from canonical SSOT where applicable."""
        try:
            if os.path.exists(self.canonical_path):
                with open(self.canonical_path, 'r', encoding='utf-8') as f:
                    canonical = json.load(f)
                for k, v in canonical.items():
                    agent_id = f"Agent-{k}"
                    cur = self.coordinates.get("agents", {}).get(agent_id, {})
                    if cur.get("chat_input_coordinates") != v:
                        raise AssertionError(f"Coordinate drift for {agent_id}: {cur.get('chat_input_coordinates')} != {v}")
        except AssertionError:
            raise
        except Exception:
            # Do not raise for missing canon or parsing issues, loader already warns
            pass