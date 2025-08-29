from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.models import AIAgent


class AgentManagerInterface(ABC):
    """Interface for AI agent coordination operations."""

    @abstractmethod
    def register_agent(self, agent: AIAgent) -> bool:
        """Register an AI agent."""

    @abstractmethod
    def get_agent(self, agent_id: str) -> Optional[AIAgent]:
        """Retrieve an AI agent by ID."""

    @abstractmethod
    def list_agents(self, agent_type: Optional[str] = None) -> List[AIAgent]:
        """List registered agents with optional filtering."""
