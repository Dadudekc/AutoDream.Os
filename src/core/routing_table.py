"""Routing table management for message routing."""

from typing import Dict, Optional

from .routing_models import RoutingRule
from .shared_enums import MessageType, UnifiedMessagePriority


class RoutingTable:
    """Store and manage routing rules."""

    def __init__(self) -> None:
        self.rules: Dict[MessageType, RoutingRule] = {}
        self.initialize_default_rules()

    def initialize_default_rules(self) -> None:
        """Populate the table with default routing rules."""
        self.rules = {
            MessageType.CONTRACT_ASSIGNMENT: RoutingRule(
                message_type=MessageType.CONTRACT_ASSIGNMENT,
                priority=UnifiedMessagePriority.HIGH,
                target_agents=[],
                delivery_strategy="specific",
                retry_policy={"max_attempts": 3, "retry_delay": 5},
            ),
            MessageType.STATUS_UPDATE: RoutingRule(
                message_type=MessageType.STATUS_UPDATE,
                priority=UnifiedMessagePriority.NORMAL,
                target_agents=[],
                delivery_strategy="broadcast",
                retry_policy={"max_attempts": 1, "retry_delay": 0},
            ),
            MessageType.COORDINATION: RoutingRule(
                message_type=MessageType.COORDINATION,
                priority=UnifiedMessagePriority.NORMAL,
                target_agents=[],
                delivery_strategy="broadcast",
                retry_policy={"max_attempts": 2, "retry_delay": 10},
            ),
            MessageType.EMERGENCY: RoutingRule(
                message_type=MessageType.EMERGENCY,
                priority=UnifiedMessagePriority.URGENT,
                target_agents=[],
                delivery_strategy="broadcast",
                retry_policy={"max_attempts": 5, "retry_delay": 1},
            ),
            MessageType.HEARTBEAT: RoutingRule(
                message_type=MessageType.HEARTBEAT,
                priority=UnifiedMessagePriority.LOW,
                target_agents=[],
                delivery_strategy="broadcast",
                retry_policy={"max_attempts": 1, "retry_delay": 0},
            ),
            MessageType.SYSTEM_COMMAND: RoutingRule(
                message_type=MessageType.SYSTEM_COMMAND,
                priority=UnifiedMessagePriority.HIGH,
                target_agents=[],
                delivery_strategy="specific",
                retry_policy={"max_attempts": 3, "retry_delay": 5},
            ),
        }

    def get_rule(self, message_type: MessageType) -> Optional[RoutingRule]:
        """Retrieve routing rule for a given message type."""
        return self.rules.get(message_type)

    def set_rule(self, message_type: MessageType, rule: RoutingRule) -> None:
        """Update or add a routing rule."""
        self.rules[message_type] = rule
