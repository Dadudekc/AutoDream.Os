"""
Messaging Validation Utilities - V2 Compliant Shared Validation Logic
Eliminates DRY violations across messaging system validation methods
V2 Compliance: Under 300-line limit with focused functionality

@Author: Agent-6 - Gaming & Entertainment Specialist (Coordination & Communication V2 Compliance)
@Version: 1.0.0 - Messaging Validation DRY Elimination
@License: MIT
"""

from src.services.models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType,
)


class MessagingValidationUtils:
    """Shared messaging validation utilities to eliminate DRY violations.

    Provides common validation functionality for:
    - Message structure validation
    - Configuration validation
    - Content validation
    - Agent ID validation
    """

    @staticmethod
    def validate_message_structure(message: UnifiedMessage) -> Dict[str, Any]:
        """Validate UnifiedMessage structure and content.

        Args:
            message: Message to validate

        Returns:
            Dict containing validation results with errors and warnings
        """
        errors = []
        warnings = []

        # Validate required fields
        if not message.content or not message.content.strip():
            errors.append("Missing or empty message content")
        if not message.sender or not message.sender.strip():
            errors.append("Missing or empty sender")
        if not message.recipient or not message.recipient.strip():
            errors.append("Missing or empty recipient")

        # Validate content length
        if message.content and len(message.content) > 10000:  # 10KB limit
            errors.append("Message content too long (max 10KB)")

        # Validate message type
        if (
            message.message_type
            and not MessagingValidationUtils._is_valid_message_type(
                message.message_type
            )
        ):
            errors.append(f"Invalid message type: {message.message_type}")

        # Validate priority
        if message.priority and not MessagingValidationUtils._is_valid_priority(
            message.priority
        ):
            errors.append(f"Invalid priority: {message.priority}")

        # Validate tags
        if message.tags:
            for tag in message.tags:
                if not MessagingValidationUtils._is_valid_tag(tag):
                    warnings.append(f"Unknown tag: {tag}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings),
        }

    @staticmethod
    def validate_message_config(message_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate message configuration parameters.

        Args:
            message_config: Message configuration to validate

        Returns:
            Dict containing validation results
        """
        errors = []
        warnings = []

        # Validate required fields
        required_fields = ["sender", "recipient", "message_type"]
        for field in required_fields:
            if field not in message_config:
                errors.append(f"Missing required field: {field}")

        # Validate sender and recipient
        if "sender" in message_config:
            if not MessagingValidationUtils.validate_agent_id(message_config["sender"]):
                errors.append(f"Invalid sender: {message_config['sender']}")

        if "recipient" in message_config:
            if not MessagingValidationUtils.validate_agent_id(
                message_config["recipient"]
            ):
                errors.append(f"Invalid recipient: {message_config['recipient']}")

        # Validate message type
        if "message_type" in message_config:
            if not MessagingValidationUtils._is_valid_message_type(
                message_config["message_type"]
            ):
                errors.append(f"Invalid message type: {message_config['message_type']}")

        # Validate priority
        if "priority" in message_config:
            if not MessagingValidationUtils._is_valid_priority(
                message_config["priority"]
            ):
                errors.append(f"Invalid priority: {message_config['priority']}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings),
        }

    @staticmethod
    def validate_agent_id(agent_id: str) -> bool:
        """Validate agent ID format and existence.

        Args:
            agent_id: Agent ID to validate

        Returns:
            True if valid, False otherwise
        """
        if not agent_id or not get_unified_validator().validate_type(agent_id, str):
            return False

        # Check if it's a valid agent format (Agent-X or system)
        valid_agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
            "system",
            "Captain Agent-4",
        ]

        return agent_id in valid_agents

    @staticmethod
    def validate_content_length(content: str, max_length: int = 10000) -> bool:
        """Validate content length.

        Args:
            content: Content to validate
            max_length: Maximum allowed length

        Returns:
            True if valid, False otherwise
        """
        if not get_unified_validator().validate_required(content):
            return False
        return len(content) <= max_length

    @staticmethod
    def _is_valid_message_type(message_type: Any) -> bool:
        """Check if message type is valid."""
        if get_unified_validator().validate_type(message_type, str):
            valid_types = [
                "text",
                "broadcast",
                "onboarding",
                "agent_to_agent",
                "system_to_agent",
                "human_to_agent",
            ]
            return message_type in valid_types
        elif get_unified_validator().validate_hasattr(message_type, "value"):
            return message_type in UnifiedMessageType
        return False

    @staticmethod
    def _is_valid_priority(priority: Any) -> bool:
        """Check if priority is valid."""
        if get_unified_validator().validate_type(priority, str):
            valid_priorities = ["normal", "urgent"]
            return priority in valid_priorities
        elif get_unified_validator().validate_hasattr(priority, "value"):
            return priority in UnifiedMessagePriority
        return False

    @staticmethod
    def _is_valid_tag(tag: Any) -> bool:
        """Check if tag is valid."""
        if get_unified_validator().validate_type(tag, str):
            valid_tags = ["captain", "onboarding", "wrapup", "coordination", "swarm"]
            return tag in valid_tags
        elif get_unified_validator().validate_hasattr(tag, "value"):
            return tag in UnifiedMessageTag
        return False

    @staticmethod
    def get_validation_summary(validation_result: Dict[str, Any]) -> str:
        """Get a human-readable validation summary.

        Args:
            validation_result: Result from validation methods

        Returns:
            Summary string
        """
        if validation_result["valid"]:
            if validation_result["warning_count"] > 0:
                return f"✅ Valid with {validation_result['warning_count']} warnings"
            else:
                return "✅ Valid"
        else:
            return f"❌ Invalid: {validation_result['error_count']} errors"

    @staticmethod
    def validate_coordinates_async(service) -> Dict[str, Any]:
        """Reusable helper function for async coordinate loading.

        Eliminates DRY violation by providing a single implementation
        for the async coordinate loading pattern used in multiple places.

        Args:
            service: Messaging service instance

        Returns:
            Dict containing coordinate data and success status
        """

        try:
            if sys.version_info >= (3, 7):
                result = asyncio.run(service.show_coordinates())
            else:
                # Fallback for older Python versions
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(service.show_coordinates())
        except RuntimeError:
            # Handle case where event loop is already running
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Create new task in existing loop
                    task = asyncio.create_task(service.show_coordinates())
                    result = loop.run_until_complete(task)
                else:
                    result = loop.run_until_complete(service.show_coordinates())
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to load coordinates: {str(e)}",
                    "coordinates": {},
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to load coordinates: {str(e)}",
                "coordinates": {},
            }

        return {"success": True, "coordinates": result, "error": None}


# Export main interface
__all__ = ["MessagingValidationUtils"]
