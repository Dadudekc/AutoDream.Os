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

from ..agent_registry import COORDINATES


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
                print("Agent-1: Integration & Core Systems")
                print("Agent-2: Architecture & Design")
                print("Agent-3: Infrastructure & DevOps")
                print("Agent-4: Strategic Oversight & Emergency Intervention")
                print("Agent-5: Business Intelligence")
                print("Agent-6: Coordination & Communication")
                print("Agent-7: Web Development")
                print("Agent-8: SSOT & System Integration")
                return True
                
            if args.coordinates:
                print("Agent Coordinates:")
                print("=" * 40)
                for agent_id, coords in COORDINATES.items():
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
            "Agent-1: Integration & Core Systems",
            "Agent-2: Architecture & Design", 
            "Agent-3: Infrastructure & DevOps",
            "Agent-4: Strategic Oversight & Emergency Intervention",
            "Agent-5: Business Intelligence",
            "Agent-6: Coordination & Communication",
            "Agent-7: Web Development",
            "Agent-8: SSOT & System Integration"
        ]
    
    def get_coordinates(self) -> Dict[str, Any]:
        """Get agent coordinates."""
        return COORDINATES
    
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
