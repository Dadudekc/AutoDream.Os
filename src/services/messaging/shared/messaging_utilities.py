#!/usr/bin/env python3
"""
Messaging Shared Utilities - V2 Compliant
==========================================

Shared utility functions for common messaging operations.
Consolidates duplicated logic across 79+ files.

V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class MessagingUtilities:
    """Shared utilities for common messaging operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._coordinates_cache: Optional[Dict[str, Any]] = None
    
    def load_coordinates_from_json(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Load agent coordinates from JSON file.
        
        Args:
            file_path: Optional path to coordinates file
            
        Returns:
            Dictionary of agent coordinates
        """
        if self._coordinates_cache is not None:
            return self._coordinates_cache
        
        if file_path is None:
            # Try multiple possible locations
            possible_paths = [
                "config/coordinates.json",
                "cursor_agent_coords.json",
                "config/cursor_agent_coords.json"
            ]
            
            for path in possible_paths:
                if Path(path).exists():
                    file_path = path
                    break
        
        if not file_path or not Path(file_path).exists():
            self.logger.warning("No coordinates file found, using empty coordinates")
            self._coordinates_cache = {}
            return self._coordinates_cache
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._coordinates_cache = data
                self.logger.info(f"Loaded coordinates from {file_path}")
                return data
        except Exception as e:
            self.logger.error(f"Failed to load coordinates from {file_path}: {e}")
            self._coordinates_cache = {}
            return {}
    
    def list_agents(self, coordinates_file: Optional[str] = None) -> List[str]:
        """List all available agents from coordinates.
        
        Args:
            coordinates_file: Optional path to coordinates file
            
        Returns:
            List of agent IDs
        """
        coords = self.load_coordinates_from_json(coordinates_file)
        
        # Extract agent IDs from various possible structures
        agents = []
        
        if "agents" in coords:
            agents.extend(coords["agents"].keys())
        elif isinstance(coords, dict):
            # Assume keys are agent IDs
            agents.extend(coords.keys())
        
        self.logger.info(f"Found {len(agents)} agents: {agents}")
        return agents
    
    def get_agent_coordinates(self, agent_id: str, coordinates_file: Optional[str] = None) -> Optional[Tuple[int, int]]:
        """Get coordinates for a specific agent.
        
        Args:
            agent_id: Agent identifier
            coordinates_file: Optional path to coordinates file
            
        Returns:
            Tuple of (x, y) coordinates or None if not found
        """
        coords = self.load_coordinates_from_json(coordinates_file)
        
        # Try different possible structures
        if "agents" in coords and agent_id in coords["agents"]:
            agent_data = coords["agents"][agent_id]
            if "chat_input_coordinates" in agent_data:
                coords_tuple = tuple(agent_data["chat_input_coordinates"])
                return coords_tuple
            elif "coordinates" in agent_data:
                coords_tuple = tuple(agent_data["coordinates"])
                return coords_tuple
        
        elif agent_id in coords:
            # Direct agent ID mapping
            agent_coords = coords[agent_id]
            if isinstance(agent_coords, (list, tuple)) and len(agent_coords) >= 2:
                return tuple(agent_coords[:2])
        
        self.logger.warning(f"No coordinates found for agent {agent_id}")
        return None
    
    def send_message_pyautogui(self, agent_id: str, message: str, 
                              coordinates_file: Optional[str] = None) -> bool:
        """Send message to agent using PyAutoGUI.
        
        Args:
            agent_id: Target agent identifier
            message: Message content
            coordinates_file: Optional path to coordinates file
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            import pyautogui
            
            coords = self.get_agent_coordinates(agent_id, coordinates_file)
            if coords is None:
                self.logger.error(f"Cannot send message to {agent_id}: no coordinates")
                return False
            
            x, y = coords
            
            # Click on agent's input area
            pyautogui.click(x, y)
            
            # Type the message
            pyautogui.typewrite(message)
            
            # Press Enter to send
            pyautogui.press('enter')
            
            self.logger.info(f"Message sent to {agent_id} via PyAutoGUI")
            return True
            
        except ImportError:
            self.logger.error("PyAutoGUI not available")
            return False
        except Exception as e:
            self.logger.error(f"Failed to send message to {agent_id}: {e}")
            return False
    
    def broadcast_message(self, message: str, sender: str = "system",
                         coordinates_file: Optional[str] = None) -> Dict[str, bool]:
        """Broadcast message to all available agents.
        
        Args:
            message: Message content
            sender: Sender identifier
            coordinates_file: Optional path to coordinates file
            
        Returns:
            Dictionary mapping agent IDs to success status
        """
        agents = self.list_agents(coordinates_file)
        results = {}
        
        for agent_id in agents:
            try:
                success = self.send_message_pyautogui(agent_id, message, coordinates_file)
                results[agent_id] = success
                self.logger.info(f"Broadcast to {agent_id}: {'success' if success else 'failed'}")
            except Exception as e:
                self.logger.error(f"Failed to broadcast to {agent_id}: {e}")
                results[agent_id] = False
        
        success_count = sum(1 for success in results.values() if success)
        self.logger.info(f"Broadcast complete: {success_count}/{len(agents)} agents successful")
        
        return results
    
    def validate_coordinates(self, coordinates_file: Optional[str] = None) -> Dict[str, Any]:
        """Validate coordinate file and return status.
        
        Args:
            coordinates_file: Optional path to coordinates file
            
        Returns:
            Validation status dictionary
        """
        try:
            coords = self.load_coordinates_from_json(coordinates_file)
            agents = self.list_agents(coordinates_file)
            
            validation_results = {
                "file_found": True,
                "valid_json": True,
                "agents_count": len(agents),
                "agents_with_coords": 0,
                "errors": []
            }
            
            for agent_id in agents:
                if self.get_agent_coordinates(agent_id, coordinates_file) is not None:
                    validation_results["agents_with_coords"] += 1
            
            return validation_results
            
        except Exception as e:
            return {
                "file_found": False,
                "valid_json": False,
                "agents_count": 0,
                "agents_with_coords": 0,
                "errors": [str(e)]
            }


# Global utility instance
_global_utilities: Optional[MessagingUtilities] = None


def get_messaging_utilities() -> MessagingUtilities:
    """Get or create the global messaging utilities instance."""
    global _global_utilities
    
    if _global_utilities is None:
        _global_utilities = MessagingUtilities()
    
    return _global_utilities


# Convenience functions for backward compatibility
def load_coordinates_from_json(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Load coordinates from JSON file."""
    return get_messaging_utilities().load_coordinates_from_json(file_path)


def list_agents(coordinates_file: Optional[str] = None) -> List[str]:
    """List all available agents."""
    return get_messaging_utilities().list_agents(coordinates_file)


def send_message_pyautogui(agent_id: str, message: str, 
                          coordinates_file: Optional[str] = None) -> bool:
    """Send message via PyAutoGUI."""
    return get_messaging_utilities().send_message_pyautogui(agent_id, message, coordinates_file)


def broadcast_message(message: str, sender: str = "system",
                     coordinates_file: Optional[str] = None) -> Dict[str, bool]:
    """Broadcast message to all agents."""
    return get_messaging_utilities().broadcast_message(message, sender, coordinates_file)

