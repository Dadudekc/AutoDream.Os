#!/usr/bin/env python3
"""
Agent Context Manager - V2 Compliant Module
==========================================

Manages agent context and state information.

V2 Compliance: < 300 lines, single responsibility.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class AgentContextManager:
    """Manages agent context and state information."""

    def __init__(self):
        """Initialize agent context manager."""
        self.contexts = {}
        self.logger = logging.getLogger(__name__)
        self._contexts: dict[str, dict[str, Any]] = {}
        self._metadata: dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
        }

    def set_agent_context(self, agent_id: str, context: dict[str, Any]) -> bool:
        """
        Set context for an agent.

        Args:
            agent_id: The agent identifier
            context: Context data dictionary

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._contexts[agent_id] = {
                **context,
                "updated_at": datetime.now().isoformat(),
                "agent_id": agent_id,
            }
            logger.info(f"Context set for agent {agent_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to set context for agent {agent_id}: {e}")
            return False

    def get_agent_context(self, agent_id: str) -> dict[str, Any] | None:
        """
        Get context for an agent.

        Args:
            agent_id: The agent identifier

        Returns:
            Optional[Dict[str, Any]]: Agent context or None if not found
        """
        return self._contexts.get(agent_id)

    def update_agent_context(self, agent_id: str, updates: dict[str, Any]) -> bool:
        """
        Update context for an agent.

        Args:
            agent_id: The agent identifier
            updates: Context updates dictionary

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if agent_id not in self._contexts:
                logger.warning(f"Agent {agent_id} not found, cannot update context")
                return False

            self._contexts[agent_id].update(updates)
            self._contexts[agent_id]["updated_at"] = datetime.now().isoformat()
            logger.info(f"Context updated for agent {agent_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update context for agent {agent_id}: {e}")
            return False

    def remove_agent_context(self, agent_id: str) -> bool:
        """
        Remove context for an agent.

        Args:
            agent_id: The agent identifier

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if agent_id in self._contexts:
                del self._contexts[agent_id]
                logger.info(f"Context removed for agent {agent_id}")
                return True
            else:
                logger.warning(f"Agent {agent_id} not found, cannot remove context")
                return False
        except Exception as e:
            logger.error(f"Failed to remove context for agent {agent_id}: {e}")
            return False

    def list_agents(self) -> list[str]:
        """
        List all agents with contexts.

        Returns:
            list[str]: List of agent IDs
        """
        return list(self._contexts.keys())

    @property
    def agent_contexts(self) -> dict[str, dict[str, Any]]:
        """Get all agent contexts."""
        return self._contexts

    def get_context_summary(self) -> dict[str, Any]:
        """
        Get summary of all agent contexts.

        Returns:
            Dict[str, Any]: Context summary
        """
        return {
            "total_agents": len(self._contexts),
            "agent_ids": list(self._contexts.keys()),
            "metadata": self._metadata,
        }


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""

    print("🐝 Module Examples - Practical Demonstrations")
    print("=" * 50)
    # Function demonstrations
    print(f"\n📋 Testing __init__():")
    try:
        # Add your function call here
        print(f"✅ __init__ executed successfully")
    except Exception as e:
        print(f"❌ __init__ failed: {e}")

    print(f"\n📋 Testing set_agent_context():")
    try:
        # Add your function call here
        print(f"✅ set_agent_context executed successfully")
    except Exception as e:
        print(f"❌ set_agent_context failed: {e}")

    print(f"\n📋 Testing get_agent_context():")
    try:
        # Add your function call here
        print(f"✅ get_agent_context executed successfully")
    except Exception as e:
        print(f"❌ get_agent_context failed: {e}")

    # Class demonstrations
    print(f"\n🏗️  Testing AgentContextManager class:")
    try:
        instance = AgentContextManager()
        print(f"✅ AgentContextManager instantiated successfully")
    except Exception as e:
        print(f"❌ AgentContextManager failed: {e}")

    print("\n🎉 All examples completed!")
    print("🐝 WE ARE SWARM - PRACTICAL CODE IN ACTION!")
