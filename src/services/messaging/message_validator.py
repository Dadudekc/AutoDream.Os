#!/usr/bin/env python3
"""
Message Validator - Validate messages and parameters
==================================================

Message validation functionality extracted from consolidated_messaging_service.py
for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging

logger = logging.getLogger(__name__)


class MessageValidator:
    """Validate messages and parameters for messaging service."""

    def __init__(self) -> None:
        """Initialize message validator."""
        self.valid_priorities = ["NORMAL", "HIGH", "URGENT"]
        self.valid_message_types = ["text", "broadcast", "onboarding"]
        self.valid_tags = ["GENERAL", "COORDINATION", "TASK", "STATUS", "VALIDATION"]

    def validate_agent_id(self, agent_id: str, available_agents: list[str]) -> bool:
        """Validate agent ID exists."""
        if not agent_id:
            logger.error("Agent ID cannot be empty")
            return False

        if agent_id not in available_agents:
            logger.error(f"Agent ID '{agent_id}' not found in available agents")
            return False

        return True

    def validate_message_content(self, message: str) -> bool:
        """Validate message content."""
        if not message:
            logger.error("Message content cannot be empty")
            return False

        if len(message.strip()) < 1:
            logger.error("Message content cannot be empty after stripping")
            return False

        if len(message) > 10000:  # Reasonable limit
            logger.error("Message content too long (max 10000 characters)")
            return False

        return True

    def validate_priority(self, priority: str) -> bool:
        """Validate message priority."""
        if priority not in self.valid_priorities:
            logger.error(f"Invalid priority '{priority}'. Valid: {self.valid_priorities}")
            return False

        return True

    def validate_from_agent(self, from_agent: str) -> bool:
        """Validate from_agent parameter."""
        if not from_agent:
            logger.error("from_agent is required")
            return False

        if not isinstance(from_agent, str):
            logger.error("from_agent must be a string")
            return False

        return True

    def validate_coordinates(self, coordinates: list[int]) -> bool:
        """Validate agent coordinates."""
        if not coordinates:
            logger.error("Coordinates cannot be empty")
            return False

        if not isinstance(coordinates, list):
            logger.error("Coordinates must be a list")
            return False

        if len(coordinates) != 2:
            logger.error("Coordinates must have exactly 2 elements [x, y]")
            return False

        try:
            x, y = coordinates
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                logger.error("Coordinates must be numbers")
                return False

            if x < 0 or y < 0:
                logger.error("Coordinates must be positive")
                return False

        except Exception as e:
            logger.error(f"Error validating coordinates: {e}")
            return False

        return True

    def validate_send_message_params(
        self,
        agent_id: str,
        message: str,
        from_agent: str,
        priority: str = "NORMAL",
        available_agents: list[str] | None = None,
    ) -> dict:
        """Validate all parameters for send_message."""
        validation_result = {"valid": True, "errors": []}

        # Validate agent_id
        if available_agents and not self.validate_agent_id(agent_id, available_agents):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid agent_id")

        # Validate message content
        if not self.validate_message_content(message):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid message content")

        # Validate from_agent
        if not self.validate_from_agent(from_agent):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid from_agent")

        # Validate priority
        if not self.validate_priority(priority):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid priority")

        return validation_result

    def validate_broadcast_params(
        self, message: str, from_agent: str, priority: str = "NORMAL"
    ) -> dict:
        """Validate parameters for broadcast message."""
        validation_result = {"valid": True, "errors": []}

        # Validate message content
        if not self.validate_message_content(message):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid message content")

        # Validate from_agent
        if not self.validate_from_agent(from_agent):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid from_agent")

        # Validate priority
        if not self.validate_priority(priority):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid priority")

        return validation_result

    def validate_onboarding_params(
        self, message: str = None, from_agent: str = "Captain Agent-4"
    ) -> dict:
        """Validate parameters for onboarding message."""
        validation_result = {"valid": True, "errors": []}

        # Validate from_agent
        if not self.validate_from_agent(from_agent):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid from_agent")

        # Message is optional for onboarding
        if message and not self.validate_message_content(message):
            validation_result["valid"] = False
            validation_result["errors"].append("Invalid message content")

        return validation_result

    def sanitize_message(self, message: str) -> str:
        """Sanitize message content."""
        # Remove potentially harmful characters
        sanitized = message.replace("\x00", "")  # Remove null bytes
        sanitized = sanitized.replace("\r\n", "\n")  # Normalize line endings

        # Truncate if too long
        if len(sanitized) > 10000:
            sanitized = sanitized[:10000] + "... [TRUNCATED]"

        return sanitized

    def get_validation_summary(self, validation_result: dict) -> str:
        """Get human-readable validation summary."""
        if validation_result["valid"]:
            return "✅ Validation passed"
        else:
            errors = ", ".join(validation_result["errors"])
            return f"❌ Validation failed: {errors}"
