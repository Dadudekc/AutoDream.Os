from typing import Dict, TYPE_CHECKING

    from .unified_financial_api import AgentRegistration
from __future__ import annotations


"""Authentication component for UnifiedFinancialAPI.

Provides simple authorization checks for agents requesting services.
"""


if TYPE_CHECKING:  # pragma: no cover - for type hints only


class APIAuthenticator:
    """Validates whether an agent can access a service."""

    def authorize(
        self,
        source_agent: str,
        target_service: str,
        registered_agents: Dict[str, "AgentRegistration"],
    ) -> None:
        """Ensure agent is registered and allowed to access service.

        Args:
            source_agent: Identifier of the requesting agent.
            target_service: Service the agent wishes to access.
            registered_agents: Mapping of registered agents.

        Raises:
            ValueError: If the agent is not registered or service not allowed.
        """
        if source_agent not in registered_agents:
            raise ValueError(f"Agent {source_agent} not registered")

        if target_service not in registered_agents[source_agent].required_services:
            raise ValueError(
                f"Service {target_service} not available for agent {source_agent}"
            )
