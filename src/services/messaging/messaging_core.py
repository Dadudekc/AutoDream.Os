#!/usr/bin/env python3
"""
Messaging Core - Core messaging functionality
============================================

Core messaging functionality extracted from consolidated_messaging_service.py
for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MessagingCore:
    """Core messaging functionality for agent-to-agent communication."""

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize messaging core."""
        self.coord_path = coord_path
        self.agent_data = self._load_coordinates()

    def _load_coordinates(self) -> dict:
        """Load agent coordinates from JSON file."""
        try:
            with open(self.coord_path) as f:
                data = json.load(f)
            return data.get("agents", {})
        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
            return {}

    def get_agent_coordinates(self, agent_id: str) -> list[int] | None:
        """Get coordinates for specific agent."""
        return self.agent_data.get(agent_id, {}).get("coordinates")

    def get_agent_info(self, agent_id: str) -> dict:
        """Get complete agent information."""
        return self.agent_data.get(agent_id, {})

    def list_agents(self) -> list[str]:
        """List all available agents."""
        return list(self.agent_data.keys())

    def validate_agent_id(self, agent_id: str) -> bool:
        """Validate agent ID exists."""
        return agent_id in self.agent_data

    def get_agent_status(self, agent_id: str) -> str:
        """Get agent status from workspace."""
        try:
            status_path = Path(f"agent_workspaces/{agent_id}/status.json")
            if status_path.exists():
                with open(status_path) as f:
                    status_data = json.load(f)
                return status_data.get("status", "UNKNOWN")
        except Exception as e:
            logger.error(f"Error reading agent status: {e}")
        return "UNKNOWN"

    def create_message_metadata(
        self, from_agent: str, to_agent: str, priority: str = "NORMAL"
    ) -> dict:
        """Create standardized message metadata."""
        import time

        return {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "priority": priority,
            "timestamp": time.time(),
            "message_id": f"msg_{int(time.time() * 1000)}",
        }

    def format_message(self, content: str, metadata: dict) -> str:
        """Format message with standard headers."""
        return f"""
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {metadata['from_agent']}
📥 TO: {metadata['to_agent']}
Priority: {metadata['priority']}
Message ID: {metadata['message_id']}
Timestamp: {metadata['timestamp']}
------------------------------------------------------------
{content}
------------------------------------------------------------
🐝 WE ARE SWARM - Message Complete
============================================================"""

    def log_message_delivery(self, metadata: dict, success: bool) -> None:
        """Log message delivery attempt."""
        status = "SUCCESS" if success else "FAILED"
        logger.info(
            f"Message delivery {status}: {metadata['from_agent']} -> {metadata['to_agent']}"
        )

    def get_service_status(self) -> dict:
        """Get messaging service status."""
        return {
            "service_status": "Active",
            "agents_configured": len(self.agent_data),
            "active_agents": len(
                [
                    aid
                    for aid in self.agent_data.keys()
                    if self.get_agent_status(aid) == "ACTIVE_AGENT_MODE"
                ]
            ),
        }
