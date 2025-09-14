#!/usr/bin/env python3
"""
Agent Communication Engine Base - V2 Compliance Module
======================================================

Base class for agent communication operations in Discord commander.

Author: Agent-3 (Infrastructure & DevOps) - V2 Restoration
License: MIT
"""

import logging
from abc import ABC

try:
    from ...utils.unified_utilities import get_unified_utility
except ImportError:
    # Fallback for direct execution
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from utils.unified_utilities import get_unified_utility


class AgentCommunicationEngineBase(ABC):
    """Base class for agent communication operations"""

    def __init__(self) -> None:
        """Initialize base communication engine."""
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logger for communication engine."""
        logger = logging.getLogger("discord_commander")
        logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _get_unified_utility(self):
        """Get unified utility instance."""
        return get_unified_utility()

    def validate_agent_name(self, agent: str) -> bool:
        """Validate agent name format."""
        if not agent or not isinstance(agent, str):
            return False
        return agent.startswith("Agent-") and len(agent) >= 7

    def format_timestamp(self) -> str:
        """Format current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def create_message_metadata(self, sender: str, recipient: str, priority: str = "NORMAL") -> dict:
        """Create message metadata."""
        return {
            "sender": sender,
            "recipient": recipient,
            "priority": priority,
            "timestamp": self.format_timestamp(),
            "source": "discord_commander"
        }
