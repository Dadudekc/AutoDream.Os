"""Utility Handler - V2 Compliant Module.

Handles utility commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional

from ..utils.agent_registry import list_agents


class UtilityHandler:
    """
    Handles utility commands for messaging CLI.
    
    Manages utility functions like listing agents, coordinates, and history.
    """
    
    def __init__(self):
        """Initialize utility handler."""
        self.agent_list = []
        self.coordinates = {}
        self.history = []
    
    def handle_utility_commands(self, args) -> bool:
        """Handle utility-related commands."""
        try:
            if args.list_agents:
                agents = list_agents()
                print("Available Agents:")
                print("=" * 40)
                for agent_id, info in agents.items():
                    print(f"{agent_id}: {info['description']}")
                return True

            if args.coordinates:
                agents = list_agents()
                print("Agent Coordinates:")
                print("=" * 40)
                for agent_id, info in agents.items():
                    coords = info.get("coords", {})
                    print(f"{agent_id}: {coords}")
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
        agents = list_agents()
        return [f"{aid}: {info['description']}" for aid, info in agents.items()]

    def get_coordinates(self) -> Dict[str, Any]:
        """Get agent coordinates."""
        agents = list_agents()
        return {aid: info.get("coords", {}) for aid, info in agents.items()}
    
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
