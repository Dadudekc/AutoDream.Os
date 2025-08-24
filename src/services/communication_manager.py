"""Communication module for coordinator."""
from __future__ import annotations
from typing import Dict, List, Any


class CommunicationManager:
    """Stores messages sent to agents."""

    def __init__(self) -> None:
        self._messages: Dict[str, List[Any]] = {}

    def send_message(self, agent_id: str, message: Any) -> None:
        self._messages.setdefault(agent_id, []).append(message)

    def get_messages(self, agent_id: str) -> List[Any]:
        return list(self._messages.get(agent_id, []))
