#!/usr/bin/env python3
"""
PyAutoGUI Message Delivery Provider - V2 Compliant Module
========================================================

PyAutoGUI-based message delivery provider for messaging system.
V2 COMPLIANT: Focused delivery provider under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import json
import os
from pathlib import Path
from typing import Dict, List

try:
    from ..models.messaging_models import UnifiedMessage, AgentCoordinates
    from ..interfaces.messaging_interfaces import PyAutoGUIDeliveryProvider
except ImportError:
    # Fallback for direct execution
    from models.messaging_models import UnifiedMessage, AgentCoordinates
    from interfaces.messaging_interfaces import PyAutoGUIDeliveryProvider


class PyAutoGUIMessageDelivery(PyAutoGUIDeliveryProvider):
    """PyAutoGUI-based message delivery provider."""

    def __init__(self, coordinates_file: str = "cursor_agent_coords.json"):
        self.coordinates_file = Path(coordinates_file)
        self.agent_coordinates: Dict[str, AgentCoordinates] = {}
        self._load_coordinates()

    def _load_coordinates(self) -> None:
        """Load agent coordinates from JSON file."""
        try:
            if self.coordinates_file.exists():
                with open(self.coordinates_file, 'r', encoding='utf-8') as f:
                    coords_data = json.load(f)
                
                # Handle nested structure with 'agents' key
                agents_data = coords_data.get('agents', coords_data)
                
                for agent_id, agent_info in agents_data.items():
                    if isinstance(agent_info, dict):
                        # Look for chat_input_coordinates first, then fallback to direct coordinates
                        coords = agent_info.get('chat_input_coordinates', agent_info)
                        
                        if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                            self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, coords)
                        elif isinstance(coords, dict):
                            self.agent_coordinates[agent_id] = AgentCoordinates(
                                agent_id=agent_id,
                                x=coords.get('x', 0),
                                y=coords.get('y', 0),
                                monitor=coords.get('monitor', 1)
                            )
                    elif isinstance(agent_info, (list, tuple)) and len(agent_info) >= 2:
                        # Direct coordinate tuple
                        self.agent_coordinates[agent_id] = AgentCoordinates.from_tuple(agent_id, agent_info)
                        
        except Exception as e:
            print(f"❌ Failed to load coordinates: {e}")

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send message via PyAutoGUI automation."""
        try:
            if not self.is_available():
                return False
            
            # Get agent coordinates
            agent_coords = self.agent_coordinates.get(message.recipient)
            if not agent_coords:
                print(f"❌ No coordinates found for {message.recipient}")
                return False
            
            # Import PyAutoGUI
            import pyautogui
            
            # Move to agent coordinates
            pyautogui.moveTo(agent_coords.x, agent_coords.y)
            
            # Click to focus
            pyautogui.click()
            
            # Type the message
            formatted_message = f"[{message.sender}] {message.content}"
            pyautogui.typewrite(formatted_message)
            
            # Send with Enter key
            pyautogui.press('enter')
            
            print(f"✅ Message sent via PyAutoGUI to {message.recipient} at ({agent_coords.x}, {agent_coords.y})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send message via PyAutoGUI to {message.recipient}: {e}")
            return False

    def is_available(self) -> bool:
        """Check if PyAutoGUI is available."""
        try:
            import pyautogui
            # Check if we have coordinates loaded
            return len(self.agent_coordinates) > 0
        except ImportError:
            return False

    def _load_coordinates_from_json(self) -> Dict[str, tuple]:
        """Load coordinates from JSON file and return as dict of tuples."""
        coords_dict = {}
        try:
            if self.coordinates_file.exists():
                with open(self.coordinates_file, 'r', encoding='utf-8') as f:
                    coords_data = json.load(f)
                
                for agent_id, coords in coords_data.items():
                    if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                        coords_dict[agent_id] = tuple(coords[:3])  # x, y, monitor
                    elif isinstance(coords, dict):
                        coords_dict[agent_id] = (
                            coords.get('x', 0),
                            coords.get('y', 0),
                            coords.get('monitor', 1)
                        )
                        
        except Exception as e:
            print(f"❌ Failed to load coordinates from JSON: {e}")
        
        return coords_dict

    def get_agent_coordinates(self, agent_id: str) -> AgentCoordinates | None:
        """Get coordinates for a specific agent."""
        return self.agent_coordinates.get(agent_id)

    def list_available_agents(self) -> List[str]:
        """List all agents with coordinates."""
        return list(self.agent_coordinates.keys())

    def add_agent_coordinates(self, agent_id: str, x: int, y: int, monitor: int = 1) -> bool:
        """Add or update agent coordinates."""
        try:
            self.agent_coordinates[agent_id] = AgentCoordinates(agent_id, x, y, monitor)
            self._save_coordinates()
            return True
        except Exception as e:
            print(f"❌ Failed to add coordinates for {agent_id}: {e}")
            return False

    def _save_coordinates(self) -> bool:
        """Save coordinates to JSON file."""
        try:
            coords_data = {}
            for agent_id, coords in self.agent_coordinates.items():
                coords_data[agent_id] = coords.to_tuple()
            
            with open(self.coordinates_file, 'w', encoding='utf-8') as f:
                json.dump(coords_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Failed to save coordinates: {e}")
            return False