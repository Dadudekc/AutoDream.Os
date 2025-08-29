"""Message routing logic for the communication coordinator."""

import logging
from typing import Dict, List

from .coordinator_types import CoordinationMessage, AgentCapability

logger = logging.getLogger(__name__)


class MessageRouter:
    """Determine routing for coordination messages."""

    def route(
        self, message: CoordinationMessage, agents: Dict[str, AgentCapability]
    ) -> List[str]:
        """Return list of agent IDs that should receive the message."""
        if message.recipient_ids:
            # Respect explicitly provided recipients
            logger.debug(
                "Routing message %s to explicit recipients %s",
                message.message_id,
                message.recipient_ids,
            )
            return message.recipient_ids

        routed = [
            agent.agent_id
            for agent in agents.values()
            if "coordination" in agent.capabilities
        ]
        logger.debug("Routed message %s to %s", message.message_id, routed)
        return routed
