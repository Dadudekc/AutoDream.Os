#!/usr/bin/env python3
"""
Captain Coordinate Manager
=========================

Manages coordinate configurations and validation for the swarm system.
Integrates with existing coordinate systems and provides validation.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# V2 Compliance: File under 400 lines, functions under 30 lines

BASE = Path(".")
CANVAS = {"min_x": 0, "max_x": 3840, "min_y": 0, "max_y": 2160}


def _load_json(p: Path) -> dict:
    """Load JSON file safely."""
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


class CoordinateManager:
    """Manages coordinate configurations and validation."""
    
    def __init__(self, base: Path = BASE):
        """Initialize coordinate manager."""
        self.base = base
        self.canonical_path = self.base / "config" / "coordinates" / "coords-8.json"
        self.active_path = self.base / "runtime" / "active_coordinates.json"
        self.legacy_path = self.base / "config" / "coordinates.json"
    
    def load_canonical_coordinates(self) -> Dict:
        """Load canonical 8-agent coordinates (SSOT)."""
        return _load_json(self.canonical_path)
    
    def load_active_coordinates(self) -> Dict:
        """Load active coordinates for current mode."""
        if self.active_path.exists():
            return _load_json(self.active_path)
        return self.load_canonical_coordinates()
    
    def load_legacy_coordinates(self) -> Dict:
        """Load legacy coordinates format for compatibility."""
        return _load_json(self.legacy_path)
    
    def validate_coordinates(self, coords: Optional[Dict] = None) -> Tuple[bool, List[str]]:
        """Validate coordinate bounds and format."""
        if coords is None:
            coords = self.load_active_coordinates()
        
        issues = []
        
        for agent_id, coord in coords.items():
            # Handle both dict and list formats
            if isinstance(coord, dict):
                x = coord.get("x", 0)
                y = coord.get("y", 0)
            elif isinstance(coord, list) and len(coord) >= 2:
                x, y = coord[0], coord[1]
            else:
                issues.append(f"Invalid coordinate format for agent {agent_id}")
                continue
            
            # Check bounds
            if not (CANVAS["min_x"] <= x <= CANVAS["max_x"] and 
                   CANVAS["min_y"] <= y <= CANVAS["max_y"]):
                issues.append(f"Coordinate out of bounds for agent {agent_id}: ({x},{y})")
        
        return len(issues) == 0, issues
    
    def get_active_coordinates(self) -> Dict:
        """Get validated active coordinates."""
        coords = self.load_active_coordinates()
        valid, issues = self.validate_coordinates(coords)
        
        if not valid:
            print(f"Coordinate validation issues: {issues}")
        
        return coords
    
    def migrate_legacy_coordinates(self) -> bool:
        """Migrate legacy coordinates to canonical format."""
        legacy = self.load_legacy_coordinates()
        
        if not legacy or "agents" not in legacy:
            return False
        
        canonical = {}
        
        for agent_id, agent_data in legacy["agents"].items():
            if isinstance(agent_data, dict) and "chat_input_coordinates" in agent_data:
                canonical[agent_id.replace("Agent-", "")] = agent_data["chat_input_coordinates"]
        
        if canonical:
            self.canonical_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.canonical_path, 'w', encoding='utf-8') as f:
                json.dump(canonical, f, indent=2)
            return True
        
        return False