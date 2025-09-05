#!/usr/bin/env python3
"""
Coordinate Handler
==================

Handles coordinate-related CLI operations.
Extracted from messaging_cli_handlers_orchestrator.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import logging
from typing import Dict, Any, List, Optional

try:
    from ...unified_messaging_imports import COORDINATE_CONFIG_FILE
    from ....core.unified_data_processing_system import read_json, write_json
except ImportError:
    # Fallback implementations
    COORDINATE_CONFIG_FILE = "config/agent_coordinates.json"
    def read_json(file_path: str) -> Dict[str, Any]:
        return {}
    def write_json(file_path: str, data: Dict[str, Any]) -> bool:
        return True


class CoordinateHandler:
    """Handles coordinate-related operations."""
    
    def __init__(self):
        """Initialize coordinate handler."""
        self.logger = logging.getLogger(__name__)
        
    def get_agent_coordinates(self) -> Dict[str, Any]:
        """Get agent coordinates from configuration."""
        try:
            coordinates = read_json(COORDINATE_CONFIG_FILE)
            
            if not coordinates:
                # Fallback coordinates
                coordinates = {
                    "Agent-1": {"x": -1269, "y": 421},
                    "Agent-2": {"x": -308, "y": 421},
                    "Agent-3": {"x": -1269, "y": 1001},
                    "Agent-4": {"x": -308, "y": 1000},
                    "Agent-5": {"x": 652, "y": 421},
                    "Agent-6": {"x": 1612, "y": 419},
                    "Agent-7": {"x": 653, "y": 940},
                    "Agent-8": {"x": 1611, "y": 941}
                }
                
                # Save fallback coordinates
                self.save_agent_coordinates(coordinates)
            
            return coordinates
            
        except Exception as e:
            self.logger.error(f"Failed to get agent coordinates: {e}")
            return {}
    
    def save_agent_coordinates(self, coordinates: Dict[str, Any]) -> bool:
        """Save agent coordinates to configuration."""
        try:
            success = write_json(COORDINATE_CONFIG_FILE, coordinates)
            if success:
                self.logger.info("Agent coordinates saved successfully")
            else:
                self.logger.error("Failed to save agent coordinates")
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to save agent coordinates: {e}")
            return False
    
    def update_agent_coordinate(self, agent_id: str, x: int, y: int) -> bool:
        """Update coordinates for a specific agent."""
        try:
            coordinates = self.get_agent_coordinates()
            coordinates[agent_id] = {"x": x, "y": y}
            
            success = self.save_agent_coordinates(coordinates)
            if success:
                self.logger.info(f"Updated coordinates for {agent_id}: ({x}, {y})")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to update coordinate for {agent_id}: {e}")
            return False
    
    def validate_agent_id(self, agent_id: str) -> bool:
        """Validate if agent ID exists in coordinates."""
        try:
            coordinates = self.get_agent_coordinates()
            return agent_id in coordinates
            
        except Exception as e:
            self.logger.error(f"Failed to validate agent ID {agent_id}: {e}")
            return False
    
    def get_agent_coordinate(self, agent_id: str) -> Optional[Dict[str, int]]:
        """Get coordinate for a specific agent."""
        try:
            coordinates = self.get_agent_coordinates()
            return coordinates.get(agent_id)
            
        except Exception as e:
            self.logger.error(f"Failed to get coordinate for {agent_id}: {e}")
            return None
    
    def list_all_agents(self) -> List[str]:
        """Get list of all agent IDs."""
        try:
            coordinates = self.get_agent_coordinates()
            return list(coordinates.keys())
            
        except Exception as e:
            self.logger.error(f"Failed to list agents: {e}")
            return []
    
    def display_coordinates(self) -> None:
        """Display agent coordinates in formatted output."""
        try:
            coordinates = self.get_agent_coordinates()
            
            if not coordinates:
                print("❌ No agent coordinates found")
                return
            
            print("\n📍 Agent Coordinates:")
            print("=" * 40)
            
            for agent_id, coord in coordinates.items():
                x = coord.get("x", 0)
                y = coord.get("y", 0)
                print(f"{agent_id:<10} -> ({x:>5}, {y:>5})")
            
            print("=" * 40)
            print(f"Total agents: {len(coordinates)}")
            
        except Exception as e:
            self.logger.error(f"Failed to display coordinates: {e}")
            print(f"❌ Error displaying coordinates: {e}")
    
    def export_coordinates(self, format_type: str = "json") -> Optional[str]:
        """Export coordinates in specified format."""
        try:
            coordinates = self.get_agent_coordinates()
            
            if format_type.lower() == "json":
                import json
                return json.dumps(coordinates, indent=2)
            elif format_type.lower() == "csv":
                lines = ["Agent,X,Y"]
                for agent_id, coord in coordinates.items():
                    lines.append(f"{agent_id},{coord.get('x', 0)},{coord.get('y', 0)}")
                return "\n".join(lines)
            else:
                self.logger.warning(f"Unsupported export format: {format_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to export coordinates: {e}")
            return None
