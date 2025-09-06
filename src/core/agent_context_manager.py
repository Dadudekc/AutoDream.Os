#!/usr/bin/env python3
"""
Agent Context Manager - KISS Compliant
======================================

Simple agent context management.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class AgentContextManager:
    """Simple agent context manager."""

    def __init__(self):
        """Initialize agent context manager."""
        self.agent_contexts: Dict[str, Dict[str, Any]] = {}
        self.logger = logger

    def set_agent_context(self, agent_id: str, context: Dict[str, Any]) -> None:
        """Set context for a specific agent."""
        try:
            self.agent_contexts[agent_id] = {
                **context,
                "last_updated": datetime.now().isoformat(),
            }
            self.logger.info(f"Set context for agent {agent_id}")
        except Exception as e:
            self.logger.error(f"Error setting context for agent {agent_id}: {e}")

    def get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """Get context for a specific agent."""
        try:
            return self.agent_contexts.get(agent_id, {})
        except Exception as e:
            self.logger.error(f"Error getting context for agent {agent_id}: {e}")
            return {}

    def update_agent_context(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Update context for a specific agent."""
        try:
            if agent_id in self.agent_contexts:
                self.agent_contexts[agent_id].update(updates)
                self.agent_contexts[agent_id][
                    "last_updated"
                ] = datetime.now().isoformat()
                self.logger.info(f"Updated context for agent {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error updating context for agent {agent_id}: {e}")
            return False

    def delete_agent_context(self, agent_id: str) -> bool:
        """Delete context for a specific agent."""
        try:
            if agent_id in self.agent_contexts:
                del self.agent_contexts[agent_id]
                self.logger.info(f"Deleted context for agent {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting context for agent {agent_id}: {e}")
            return False

    def get_all_agents(self) -> list:
        """Get all agent IDs."""
        return list(self.agent_contexts.keys())

    def get_context_count(self) -> int:
        """Get total number of contexts."""
        return len(self.agent_contexts)

    def clear_all_contexts(self) -> None:
        """Clear all contexts."""
        self.agent_contexts.clear()
        self.logger.info("Cleared all agent contexts")

    def get_status(self) -> Dict[str, Any]:
        """Get manager status."""
        return {
            "total_agents": len(self.agent_contexts),
            "agents": list(self.agent_contexts.keys()),
            "timestamp": datetime.now().isoformat(),
        }


# Simple factory function
def create_agent_context_manager() -> AgentContextManager:
    """Create agent context manager."""
    return AgentContextManager()


__all__ = ["AgentContextManager", "create_agent_context_manager"]
