from datetime import datetime
from typing import Dict, Optional

from __future__ import annotations


"""Agent lifecycle tracking utilities."""



class AgentLifecycle:
    """Tracks basic lifecycle information for agents."""

    def __init__(self) -> None:
        self._last_active: Dict[str, datetime] = {}

    def update_heartbeat(self, agent_id: str) -> None:
        """Record the last active time for an agent."""
        self._last_active[agent_id] = datetime.utcnow()

    def deactivate_agent(self, agent_id: str) -> None:
        """Remove an agent from lifecycle tracking."""
        self._last_active.pop(agent_id, None)

    def get_last_active(self, agent_id: str) -> Optional[datetime]:
        """Get the last recorded active time for an agent."""
        return self._last_active.get(agent_id)
