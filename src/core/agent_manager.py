from __future__ import annotations

"""Compatibility wrapper combining registration and lifecycle management."""

from .agent_registration import AgentRegistry
from .agent_lifecycle import AgentLifecycle
from .agent_utils import AgentCapability, AgentInfo


class AgentManager(AgentRegistry, AgentLifecycle):
    """Stores registered agents and tracks their lifecycle."""

    def __init__(self, agents: dict[str, AgentInfo] | None = None) -> None:
        AgentRegistry.__init__(self, agents)
        AgentLifecycle.__init__(self)


__all__ = ["AgentManager", "AgentCapability", "AgentInfo"]
