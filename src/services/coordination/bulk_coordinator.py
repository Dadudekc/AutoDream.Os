import logging

logger = logging.getLogger(__name__)
"""
Bulk Coordinator - V2 Compliant Module
=====================================

Handles bulk message coordination and grouping.
Extracted from messaging_coordination_handler.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Any

from ..models.messaging_models import UnifiedMessage, UnifiedMessagePriority
from .strategy_coordinator import StrategyCoordinator


class BulkCoordinator:
    """Handles bulk message coordination and grouping.

        Manages bulk message processing, grouping by strategy, and batch coordination.

    EXAMPLE USAGE:
    ==============

    # Import the service
    from src.services.coordination.bulk_coordinator import Bulk_CoordinatorService

    # Initialize service
    service = Bulk_CoordinatorService()

    # Basic service operation
    response = service.handle_request(request_data)
    logger.info(f"Service response: {response}")

    # Service with dependency injection
    from src.core.dependency_container import Container

    container = Container()
    service = container.get(Bulk_CoordinatorService)

    # Execute service method
    result = service.execute_operation(input_data, context)
    logger.info(f"Operation result: {result}")

    """

    def __init__(self):
        """Initialize bulk coordinator."""
        self.strategy_coordinator = StrategyCoordinator()

    def coordinate_bulk_messages(self, messages: list[UnifiedMessage]) -> dict[str, Any]:
        """Coordinate multiple messages for efficient delivery.

        Args:
            messages: List of messages to coordinate

        Returns:
            Bulk coordination result dictionary
        """
        start_time = time.time()
        results = []
        successful = 0
        failed = 0

        # Group messages by coordination strategy
        grouped_messages = self._group_messages_by_strategy(messages)

        for strategy, message_group in grouped_messages.items():
            for message in message_group:
                result = self._coordinate_single_message(message)
                results.append(result)

                if result["success"]:
                    successful += 1
                else:
                    failed += 1

        execution_time = time.time() - start_time

        return {
            "success": True,
            "total_messages": len(messages),
            "successful": successful,
            "failed": failed,
            "execution_time": execution_time,
            "results": results,
            "grouped_by_strategy": len(grouped_messages),
        }

    def _coordinate_single_message(self, message: UnifiedMessage) -> dict[str, Any]:
        """Coordinate a single message."""
        try:
            strategy = self.strategy_coordinator.determine_coordination_strategy(message)
            coordination_result = self.strategy_coordinator.apply_coordination_rules(
                message, strategy
            )

            return {
                "success": True,
                "strategy": strategy,
                "coordination_result": coordination_result,
                "message_id": message.message_id,
                "recipient": message.recipient,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "message_id": message.message_id}

    def _group_messages_by_strategy(
        self, messages: list[UnifiedMessage]
    ) -> dict[str, list[UnifiedMessage]]:
        """Group messages by coordination strategy."""
        grouped = {}

        for message in messages:
            strategy = self.strategy_coordinator.determine_coordination_strategy(message)
            if strategy not in grouped:
                grouped[strategy] = []
            grouped[strategy].append(message)

        return grouped

    def coordinate_messages_by_priority(self, messages: list[UnifiedMessage]) -> dict[str, Any]:
        """Coordinate messages grouped by priority."""
        priority_groups = {
            UnifiedMessagePriority.URGENT: [],
            UnifiedMessagePriority.REGULAR: [],
        }

        for message in messages:
            priority_groups[message.priority].append(message)

        results = {}
        for priority, message_group in priority_groups.items():
            if message_group:
                results[priority.value] = self.coordinate_bulk_messages(message_group)

        return {
            "success": True,
            "priority_groups": results,
            "total_messages": len(messages),
        }

    def coordinate_messages_by_type(self, messages: list[UnifiedMessage]) -> dict[str, Any]:
        """Coordinate messages grouped by type."""
        type_groups = {}

        for message in messages:
            message_type = message.message_type
            if message_type not in type_groups:
                type_groups[message_type] = []
            type_groups[message_type].append(message)

        results = {}
        for message_type, message_group in type_groups.items():
            results[message_type.value] = self.coordinate_bulk_messages(message_group)

        return {
            "success": True,
            "type_groups": results,
            "total_messages": len(messages),
        }

    def coordinate_messages_by_sender(self, messages: list[UnifiedMessage]) -> dict[str, Any]:
        """Coordinate messages grouped by sender type."""
        sender_groups = {}

        for message in messages:
            sender_type = message.sender_type
            if sender_type not in sender_groups:
                sender_groups[sender_type] = []
            sender_groups[sender_type].append(message)

        results = {}
        for sender_type, message_group in sender_groups.items():
            results[sender_type.value] = self.coordinate_bulk_messages(message_group)

        return {
            "success": True,
            "sender_groups": results,
            "total_messages": len(messages),
        }

    def get_bulk_coordinator_status(self) -> dict[str, Any]:
        """Get bulk coordinator status."""
        return {
            "strategy_coordinator_status": (self.strategy_coordinator.get_coordinator_status()),
            "available_grouping_methods": ["strategy", "priority", "type", "sender"],
        }
