"""
Utility Handler - V2 Compliant Module
====================================

Handles utility commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional

from ..utils.agent_registry import AGENTS, list_agents


class UtilityHandler:
    """
    Handles utility commands for messaging CLI.
    
    Manages utility functions like listing agents, coordinates, and history.
    """
    
    def __init__(self):
        """Initialize utility handler."""
        self.agent_list = []
        self.history = []
    
    def handle_utility_commands(self, args) -> bool:
        """Handle utility-related commands."""
        try:
            if args.list_agents:
                print("Available Agents:")
                print("=" * 40)
                for agent_id in list_agents():
                    desc = AGENTS[agent_id]["description"]
                    print(f"{agent_id}: {desc}")
                return True
                
            if args.coordinates:
                print("Agent Coordinates:")
                print("=" * 40)
                for agent_id in list_agents():
                    coords = AGENTS[agent_id]["coords"]
                    x, y = coords["x"], coords["y"]
                    print(f"{agent_id}: ({x}, {y})")
                print("Use --agent to send messages to specific agents")
                return True
                
            if args.history:
                print("Message History:")
                print("=" * 40)
                print("No message history available yet.")
                return True
                
        except Exception as e:
            print(f"Error handling utility command: {e}")
            return False
        
        return False
    
    def list_agents(self) -> List[str]:
        """Get list of available agents."""
        return [
            f"{agent_id}: {AGENTS[agent_id]['description']}" for agent_id in list_agents()
        ]
    
    def get_coordinates(self) -> Dict[str, Any]:
        """Get agent coordinates."""
        return {agent_id: info["coords"] for agent_id, info in AGENTS.items()}
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get message history."""
        return self.history
    
    def add_to_history(self, message: Dict[str, Any]):
        """Add message to history."""
        self.history.append(message)
        
        # Keep only last 100 messages
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def clear_history(self):
        """Clear message history."""
        self.history = []
    
    def get_utility_status(self) -> Dict[str, Any]:
        """Get utility handler status."""
        return {
            "agent_count": len(self.list_agents()),
            "coordinate_count": len(self.get_coordinates()),
            "history_count": len(self.history)
        }
