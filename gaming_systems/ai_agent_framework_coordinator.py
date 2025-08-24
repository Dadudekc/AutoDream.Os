"""Multi-agent coordination components for the AI Agent Framework."""

from __future__ import annotations

from typing import Callable, Dict, List, Optional

from .ai_agent_framework_config import logger
from .ai_agent_framework_core import AgentState, GameState
from .ai_agent_framework_gaming import AIGamingAgent


class MultiAgentCoordinator:
    """Coordinates multiple AI agents."""

    def __init__(self, name: str = "coordinator"):
        self.name = name
        self.agents: Dict[str, AIGamingAgent] = {}
        self.communication_channels: Dict[str, List[str]] = {}
        self.coordination_rules: List[Callable] = []

    def register_agent(self, agent: AIGamingAgent) -> None:
        self.agents[agent.name] = agent
        logger.info(f"Agent {agent.name} registered with coordinator")

    def unregister_agent(self, agent_name: str) -> None:
        if agent_name in self.agents:
            del self.agents[agent_name]
            logger.info(f"Agent {agent_name} unregistered from coordinator")

    def get_agent_by_name(self, name: str) -> Optional[AIGamingAgent]:
        return self.agents.get(name)

    def create_communication_channel(self, channel_name: str) -> bool:
        if channel_name in self.communication_channels:
            return False
        self.communication_channels[channel_name] = []
        logger.info(f"Communication channel {channel_name} created")
        return True

    def send_message(self, channel_name: str, message: str, sender: str) -> bool:
        if channel_name not in self.communication_channels:
            return False
        self.communication_channels[channel_name].append(f"{sender}: {message}")
        logger.info(f"Message sent to {channel_name}: {message}")
        return True

    def coordinate_agents(self, game_state: GameState) -> None:
        for agent in self.agents.values():
            agent.update(game_state)
        for rule in self.coordination_rules:
            try:
                rule(self.agents, game_state)
            except Exception as e:  # pragma: no cover - defensive log
                logger.error(f"Coordination rule error: {e}")

    def get_coordination_metrics(self) -> Dict[str, int]:
        total_agents = len(self.agents)
        active_agents = sum(1 for agent in self.agents.values() if agent.state == AgentState.ACTIVE)
        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "communication_channels": len(self.communication_channels),
            "coordination_rules": len(self.coordination_rules),
        }


def create_multi_agent_coordinator(name: str = "coordinator") -> MultiAgentCoordinator:
    """Factory function to create multi-agent coordinator."""
    return MultiAgentCoordinator(name)


__all__ = [
    "MultiAgentCoordinator",
    "create_multi_agent_coordinator",
]
