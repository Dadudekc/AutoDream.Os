"""
Agent Repository Port - Domain Interface
========================================

Defines the contract for agent persistence operations.
This is a port in the hexagonal architecture.
"""

from collections.abc import Iterable
from typing import Protocol

from ..entities.agent import Agent
from ..value_objects.ids import AgentId


class AgentRepository(Protocol):
    """
    Port for agent persistence operations.

    This protocol defines the interface that any agent repository
    implementation must provide.
    """

    def get(self, agent_id: AgentId) -> Agent | None:
        """
        Retrieve an agent by its identifier.

        Args:
            agent_id: The unique identifier of the agent

        Returns:
            The agent if found, None otherwise
        """
        ...

    def get_by_capability(self, capability: str) -> Iterable[Agent]:
        """
        Retrieve agents that have a specific capability.

        Args:
            capability: The capability to search for

        Returns:
            Iterable of agents with the specified capability
        """
        ...

    def get_active(self) -> Iterable[Agent]:
        """
        Retrieve all active agents.

        Returns:
            Iterable of active agents
        """
        ...

    def get_available(self) -> Iterable[Agent]:
        """
        Retrieve agents that can accept more tasks.

        Returns:
            Iterable of available agents
        """
        ...

    def add(self, agent: Agent) -> None:
        """
        Add a new agent to the repository.

        Args:
            agent: The agent to add

        Raises:
            ValueError: If agent with same ID already exists
        """
        ...

    def save(self, agent: Agent) -> None:
        """
        Save an existing agent (create or update).

        Args:
            agent: The agent to save
        """
        ...

    def delete(self, agent_id: AgentId) -> bool:
        """
        Delete an agent from the repository.

        Args:
            agent_id: The identifier of the agent to delete

        Returns:
            True if agent was deleted, False if not found
        """
        ...

    def list_all(self) -> Iterable[Agent]:
        """
        List all agents in the repository.

        Returns:
            Iterable of all agents
        """
        ...
