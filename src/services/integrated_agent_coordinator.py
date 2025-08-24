"""Simplified integrated agent coordinator.

This module provides an ``IntegratedAgentCoordinator`` class that delegates
responsibilities to three specialised components:

``AgentRegistry``
    Stores metadata about available agents.
``TaskAssigner``
    Tracks tasks assigned to agents.
``CommunicationManager``
    Records messages sent to agents.

The coordinator exposes a small API used by tests to manage an agent's life
cycle.  The original file in this project was very large and mixed together
registration, task assignment and communication.  The goal of this refactor is
isolation: each responsibility now lives in its own module and the coordinator
simply orchestrates between them.
"""
from __future__ import annotations

from typing import Any, Dict

from .agent_registry import AgentRegistry
from .task_assigner import TaskAssigner
from .communication_manager import CommunicationManager


class IntegratedAgentCoordinator:
    """High level façade coordinating agent operations."""

    def __init__(
        self,
        registry: AgentRegistry | None = None,
        task_assigner: TaskAssigner | None = None,
        communication: CommunicationManager | None = None,
    ) -> None:
        self.registry = registry or AgentRegistry()
        self.task_assigner = task_assigner or TaskAssigner()
        self.communication = communication or CommunicationManager()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def register_agent(self, agent_id: str, info: Dict[str, Any] | None = None) -> None:
        """Register a new agent in the system."""
        self.registry.register(agent_id, info)

    def deregister_agent(self, agent_id: str) -> None:
        """Remove an agent from the system."""
        self.registry.deregister(agent_id)

    # ------------------------------------------------------------------
    # Task assignment
    # ------------------------------------------------------------------
    def assign_task(self, agent_id: str, task: Any) -> None:
        """Assign a task to an existing agent.

        Raises
        ------
        ValueError
            If the agent has not been registered.
        """
        if self.registry.get(agent_id) is None:
            raise ValueError(f"Unknown agent: {agent_id}")
        self.task_assigner.assign_task(agent_id, task)

    def get_agent_tasks(self, agent_id: str):
        return self.task_assigner.get_tasks(agent_id)

    # ------------------------------------------------------------------
    # Communication
    # ------------------------------------------------------------------
    def send_message(self, agent_id: str, message: Any) -> None:
        """Send a message to an agent.

        For the purposes of this simplified implementation messages are merely
        recorded.  Production implementations might forward them to real
        transports such as queues or network sockets.
        """
        if self.registry.get(agent_id) is None:
            raise ValueError(f"Unknown agent: {agent_id}")
        self.communication.send_message(agent_id, message)

    def get_agent_messages(self, agent_id: str):
        return self.communication.get_messages(agent_id)

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    def agent_ids(self):
        """Return a list of registered agent identifiers."""
        return list(self.registry.all_agents().keys())
