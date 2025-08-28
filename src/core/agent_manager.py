"""Unified agent manager coordinating lifecycle, communication and learning."""

from typing import List, Dict, Optional
import logging

from .agent import AgentLifecycle, AgentCommunication, AgentLearning, AgentInfo


class AgentManager:
    """Coordinates agent lifecycle, communication and learning features."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.lifecycle = AgentLifecycle()
        self.communication = AgentCommunication(self.lifecycle)
        self.learning = AgentLearning()

        # initialize with a sample agent to keep tests deterministic
        self.register_agent("agent_1", "Sample Agent", ["general"])

    # ------------------------------------------------------------------
    # Lifecycle wrappers
    # ------------------------------------------------------------------
    def register_agent(self, agent_id: str, name: str, capabilities=None) -> bool:
        return self.lifecycle.register(agent_id, name, capabilities)

    def unregister_agent(self, agent_id: str) -> bool:
        return self.lifecycle.unregister(agent_id)

    def get_agent_info(self, agent_id: str) -> Optional[AgentInfo]:
        return self.lifecycle.get(agent_id)

    def get_all_agents(self) -> List[AgentInfo]:
        return self.lifecycle.all_agents()

    def get_available_agents(self) -> List[AgentInfo]:
        return self.lifecycle.available_agents()

    def get_agent_summary(self) -> Dict[str, int]:
        agents = self.lifecycle.all_agents()
        return {
            "total_agents": len(agents),
            "active_agents": len([a for a in agents if a.active]),
        }

    # ------------------------------------------------------------------
    # Communication wrappers
    # ------------------------------------------------------------------
    def send_message(self, sender: str, recipient: str, message: str) -> bool:
        return self.communication.send(sender, recipient, message)

    def get_messages(self, agent_id: str) -> List[str]:
        return self.communication.get_messages(agent_id)

    # ------------------------------------------------------------------
    # Learning wrappers
    # ------------------------------------------------------------------
    def record_experience(self, agent_id: str, experience: str) -> None:
        self.learning.record(agent_id, experience)

    def get_experiences(self, agent_id: str) -> List[str]:
        return self.learning.get_experiences(agent_id)
