"""Canonical communication manager coordinating simple message storage."""
from __future__ import annotations

from typing import Any, Dict, List


class CommunicationManager:
    """Store messages for agents in memory.

    This minimal implementation replaces several ad-hoc versions scattered
    throughout the project and serves as the single source of truth for tests
    and lightweight components.
    """

    def __init__(self) -> None:
        self._messages: Dict[str, List[Any]] = {}

    def send_message(self, agent_id: str, message: Any) -> None:
        """Record a message for an agent."""
        self._messages.setdefault(agent_id, []).append(message)

    def get_messages(self, agent_id: str) -> List[Any]:
        """Return a copy of messages sent to an agent."""
        return list(self._messages.get(agent_id, []))
