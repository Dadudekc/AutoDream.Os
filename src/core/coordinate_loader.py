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
from typing import Dict, Any

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
            # Check if we're using a custom config path (not the default)
            is_custom_config = self.config_path != "config/coordinates.json"
            
            # Prefer canonical SSOT only if not using custom config
            canonical = None
            if not is_custom_config and os.path.exists(self.canonical_path):
                with open(self.canonical_path, 'r', encoding='utf-8') as f:
                    canonical = json.load(f)

            # Load provided path
            provided = None
            if self.config_path and os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    provided = json.load(f)

            # Choose data source: custom config takes precedence, then canonical, then provided, then defaults
            if is_custom_config and provided is not None:
                data = provided
            elif canonical is not None:
                data = canonical
            elif provided is not None:
                data = provided
            else:
                data = self._get_default_coordinates()

            # If both canonical and provided exist and we're not using custom config, warn about drift
            if not is_custom_config and canonical is not None and provided is not None:
                try:
                    for agent_key, coords in canonical.items():
                        if agent_key in provided and provided[agent_key] != coords:
                            print(f"Warning: coordinate drift detected for agent {agent_key}; using canonical value")
                except Exception:
                    pass

            if "agents" not in data:
                # Convert canonical format to agents format
                return {
                    "agents": {
                        f"Agent-{k}": {"chat_input_coordinates": v} for k, v in data.items()
                    }
                }
            else:
                # Data already has agents format, return as-is
                return data
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

        return type('ValidationReport', (), {
            'is_all_ok': lambda self: len(issues) == 0,
            'issues': issues
        })()

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