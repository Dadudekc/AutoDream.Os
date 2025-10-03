#!/usr/bin/env python3
"""
Agent Validation Module
=======================

Agent validation for devlog posting system.
V2 Compliant: Simple validation with clear error messages.
"""

import logging

from .models import DevlogType

logger = logging.getLogger(__name__)


class AgentValidator:
    """Simple agent validation for devlog system."""

    def __init__(self):
        """Initialize agent validator."""
        self.valid_agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
            "Agent-9",
            "Agent-10",
        ]
        self.logger = logger

    def validate_agent(self, agent_id: str) -> bool:
        """Validate agent ID format."""
        if not agent_id:
            self.logger.error("Agent ID cannot be empty")
            return False

        if agent_id not in self.valid_agents:
            self.logger.warning(f"Agent {agent_id} not in standard list")
            return True  # Allow custom agents

        return True

    def validate_agent_flag(self, agent_flag: str) -> bool:
        """Validate agent flag (alias for validate_agent)."""
        return self.validate_agent(agent_flag)

    def validate_action(self, action: str) -> bool:
        """Validate action description."""
        if not action:
            self.logger.error("Action cannot be empty")
            return False

        if len(action) < 3:
            self.logger.error("Action too short")
            return False

        return True

    def validate_status(self, status: str) -> bool:
        """Validate status."""
        valid_statuses = ["completed", "in_progress", "pending", "failed"]
        if status not in valid_statuses:
            self.logger.warning(f"Status {status} not in standard list")
            return True  # Allow custom statuses

        return True

    def validate_all(self, agent_id: str, action: str, status: str) -> dict[str, bool]:
        """Validate all inputs."""
        return {
            "agent": self.validate_agent(agent_id),
            "action": self.validate_action(action),
            "status": self.validate_status(status),
        }

    def validate_details(self, details: str) -> bool:
        """Validate details (optional field)."""
        if details is None:
            return True  # Details are optional
        return len(details) <= 1000  # Reasonable limit

    def get_agent_info(self, agent_id: str) -> dict[str, str]:
        """Get agent information."""
        return {"id": agent_id, "name": agent_id, "role": "AGENT", "status": "active"}

    def suggest_devlog_type(self, action: str, status: str) -> DevlogType:
        """Suggest devlog type based on action and status."""
        if "error" in action.lower() or "fix" in action.lower():
            return DevlogType.ERROR_REPORT
        elif "complete" in status.lower():
            return DevlogType.ACTION
        elif "progress" in status.lower():
            return DevlogType.STATUS_UPDATE
        else:
            return DevlogType.ACTION

    def is_captain_agent(self, agent_id: str) -> bool:
        """Check if agent is captain."""
        return agent_id == "Agent-4"

    def get_all_agents(self) -> list[str]:
        """Get all agent IDs."""
        return self.valid_agents

    def get_agent_statistics(self) -> dict[str, int]:
        """Get agent statistics."""
        return {agent: 0 for agent in self.valid_agents}
