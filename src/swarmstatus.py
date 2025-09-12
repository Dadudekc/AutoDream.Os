"""
Swarm Status Module

This module provides the SwarmStatus dataclass for tracking the current
status of the Agent Cellphone V2 swarm system.

Author: Agent-8 (SSOT & System Integration Specialist)
Version: 2.0
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SwarmStatus:
    """
    Represents the current swarm status.

    This dataclass tracks the overall health and status of the swarm system,
    including active agents, missions, system health, and performance metrics.

    Attributes:
        active_agents (list[str]): List of currently active agent identifiers
        total_agents (int): Total number of agents in the swarm (default: 8)
        current_cycle (int): Current operational cycle number
        active_missions (list[str]): List of currently active mission identifiers
        system_health (str): Overall system health status (HEALTHY, DEGRADED, CRITICAL)
        last_update (datetime | None): Timestamp of last status update
        efficiency_rating (float): Current efficiency rating (0.0-10.0)
        pending_tasks (list[str]): List of pending task identifiers

    Example:
        >>> status = SwarmStatus()
        >>> print(f"Active agents: {len(status.active_agents)}")
        >>> print(f"System health: {status.system_health}")
        Active agents: 8
        System health: HEALTHY
    """

    active_agents: list[str] = field(default_factory=list)
    total_agents: int = 8
    current_cycle: int = 1
    active_missions: list[str] = field(default_factory=list)
    system_health: str = "HEALTHY"
    last_update: datetime | None = None
    efficiency_rating: float = 8.0
    pending_tasks: list[str] = field(default_factory=list)

    def __post_init__(self):
        """
        Initialize default values after dataclass creation.

        Sets up default active agents list and last update timestamp
        if not explicitly provided.
        """
        if not self.active_agents:
            self.active_agents = [f"Agent-{i}" for i in range(1, 9)]
        if self.last_update is None:
            self.last_update = datetime.utcnow()
