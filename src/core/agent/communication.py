"""Agent communication utilities."""

from typing import Dict, List

from .lifecycle import AgentLifecycle
from .utils import format_message


class AgentCommunication:
    """Basic in-memory message passing between agents."""

    def __init__(self, lifecycle: AgentLifecycle) -> None:
        self.lifecycle = lifecycle
        self.inboxes: Dict[str, List[str]] = {}

    def send(self, sender: str, recipient: str, message: str) -> bool:
        """Send a message from one agent to another."""
        if not self.lifecycle.get(recipient):
            return False
        formatted = format_message(sender, message)
        self.inboxes.setdefault(recipient, []).append(formatted)
        return True

    def get_messages(self, agent_id: str) -> List[str]:
        """Retrieve all messages for an agent."""
        return self.inboxes.get(agent_id, [])
