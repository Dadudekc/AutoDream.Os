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
from ...core.unified_data_processing_system import read_json


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

            if args.check_status:
                result = self.check_status(getattr(args, "status_query", None))
                print("Agent Status:")
                print("=" * 40)
                for agent_id, active in result["statuses"].items():
                    label = "ACTIVE" if active else "INACTIVE"
                    print(f"{agent_id}: {label}")
                if result["matches"]:
                    print("\nStatus Search Matches:")
                    print("=" * 40)
                    for match in result["matches"]:
                        score = f"{match['score']:.2f}"
                        print(f"{match['agent_id']} ({score}): {match['summary']}")
                return True
                
        except Exception as e:
            print(f"Error handling utility command: {e}")
            return False

        return False

    def check_status(self, query: Optional[str] = None) -> Dict[str, Any]:
        """Check agent status and search summaries."""
        from ...core.constants.paths import get_agent_status_file

        statuses: Dict[str, bool] = {}
        for agent_id in list_agents():
            status_file = get_agent_status_file(agent_id.split("-")[1])
            data = read_json(str(status_file))
            state = data.get("status", "INACTIVE")
            statuses[agent_id] = state == "ACTIVE_AGENT_MODE"

        matches: List[Dict[str, Any]] = []
        if query:
            from ..vector_database.vector_database_orchestrator import (
                get_vector_database_service,
            )
            service = get_vector_database_service()
            try:
                results = service.search_by_content(
                    query, collection_name="agent_status", limit=5
                )
                for res in results:
                    meta = res.document.metadata or {}
                    agent = meta.get("agent_id", res.document.id)
                    summary = res.document.content.replace("\n", " ")[:100]
                    matches.append(
                        {
                            "agent_id": agent,
                            "score": res.similarity_score,
                            "summary": summary,
                        }
                    )
            except Exception:
                pass

        return {"statuses": statuses, "matches": matches}
    
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
