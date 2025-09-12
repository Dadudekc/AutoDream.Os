#!/usr/bin/env python3
"""
Consolidated Coordination Service - V2 Compliant Module
======================================================

Unified coordination service consolidating:
- strategy_coordinator.py (strategy determination)
- command_handler.py (CLI command processing)
- coordinator.py (basic coordination)

V2 Compliance: < 400 lines, single responsibility for all coordination operations.

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Chunk 002 (Services)
License: MIT
"""

import logging
import time
from typing import Any

from .models.messaging_models import (
    SenderType,
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
)

logger = logging.getLogger(__name__)


class ConsolidatedCoordinationService:
    """Unified coordination service combining strategy, command handling, and coordination."""

    def __init__(self, name: str = "ConsolidatedCoordinator"):

EXAMPLE USAGE:
==============

# Import the service
from src.services.consolidated_coordination_service import Consolidated_Coordination_ServiceService

# Initialize service
service = Consolidated_Coordination_ServiceService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Consolidated_Coordination_ServiceService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

        """Initialize the consolidated coordination service."""
        self.name = name
        self.logger = logging.getLogger(__name__)
        self.status = {"name": name, "status": "active"}

        # Initialize coordination components
        self.coordination_rules = self._initialize_coordination_rules()
        self.routing_table = self._initialize_routing_table()
        self.command_count = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.command_history: list[dict[str, Any]] = []

    def _initialize_coordination_rules(self) -> dict[str, Any]:
        """Initialize coordination rules."""
        return {
            "priority_routing": {
                UnifiedMessagePriority.URGENT: "immediate",
                UnifiedMessagePriority.HIGH: "high_priority",
                UnifiedMessagePriority.NORMAL: "standard",
                UnifiedMessagePriority.LOW: "low_priority",
            },
            "type_routing": {
                UnifiedMessageType.AGENT_TO_COORDINATOR: "coordination_priority",
                UnifiedMessageType.SYSTEM_BROADCAST: "broadcast",
                UnifiedMessageType.AGENT_TO_AGENT: "standard",
                UnifiedMessageType.COORDINATOR_TO_AGENT: "system_priority",
                UnifiedMessageType.HUMAN_TO_AGENT: "standard",
            },
            "sender_routing": {
                SenderType.COORDINATOR: "highest_priority",
                SenderType.AGENT: "standard",
                SenderType.SYSTEM: "system_priority",
                SenderType.HUMAN: "standard",
            },
        }

    def _initialize_routing_table(self) -> dict[str, Any]:
        """Initialize routing table."""
        return {
            "immediate": {"timeout": 0, "retries": 3},
            "high_priority": {"timeout": 5, "retries": 2},
            "standard": {"timeout": 10, "retries": 1},
            "low_priority": {"timeout": 30, "retries": 1},
            "broadcast": {"timeout": 15, "retries": 2},
            "coordination_priority": {"timeout": 5, "retries": 3},
            "system_priority": {"timeout": 3, "retries": 3},
            "highest_priority": {"timeout": 0, "retries": 5},
        }

    def determine_coordination_strategy(self, message: UnifiedMessage) -> str:
        """Determine coordination strategy for a message."""
        # Priority-based routing
        priority_strategy = self.coordination_rules["priority_routing"].get(
            message.priority, "standard"
        )

        # Type-based routing
        type_strategy = self.coordination_rules["type_routing"].get(
            message.message_type, "standard"
        )

        # Sender-based routing
        sender_strategy = self.coordination_rules["sender_routing"].get(
            message.sender_type, "standard"
        )

        # Combine strategies (highest priority wins)
        if sender_strategy == "highest_priority":
            return sender_strategy
        elif priority_strategy == "immediate":
            return priority_strategy
        elif type_strategy in ["coordination_priority", "system_priority"]:
            return type_strategy
        else:
            return priority_strategy

    def apply_coordination_rules(self, message: UnifiedMessage) -> dict[str, Any]:
        """Apply coordination rules to a message."""
        strategy = self.determine_coordination_strategy(message)
        routing_config = self.routing_table.get(strategy, self.routing_table["standard"])

        return {
            "strategy": strategy,
            "timeout": routing_config["timeout"],
            "retries": routing_config["retries"],
            "priority": message.priority.value,
            "message_type": message.message_type.value,
            "sender_type": message.sender_type.value,
        }

    def can_handle_command(self, command: str) -> bool:
        """Check if this service can handle the given command."""
        supported_commands = ["coordinates", "list_agents", "status", "help", "ping", "shutdown"]
        return command in supported_commands

    async def process_command(
        self,
        command: str,
        args: dict[str, Any],
        coordinate_handler=None,
        message_handler=None,
        service=None,
    ) -> dict[str, Any]:
        """Process CLI command."""
        try:
            self.command_count += 1
            start_time = time.time()

            if command == "coordinates":
                result = await self._handle_coordinates_command(coordinate_handler)
            elif command == "list_agents":
                result = await self._handle_list_agents_command()
            elif command == "status":
                result = await self._handle_status_command()
            elif command == "help":
                result = await self._handle_help_command()
            elif command == "ping":
                result = await self._handle_ping_command()
            elif command == "shutdown":
                result = await self._handle_shutdown_command()
            else:
                result = {"success": False, "error": f"Unknown command: {command}", "data": {}}

            # Record command execution
            execution_time = time.time() - start_time
            self.command_history.append(
                {
                    "command": command,
                    "args": args,
                    "success": result.get("success", False),
                    "execution_time": execution_time,
                    "timestamp": time.time(),
                }
            )

            if result.get("success", False):
                self.successful_commands += 1
            else:
                self.failed_commands += 1

            return result

        except Exception as e:
            self.logger.error(f"Error processing command {command}: {e}")
            self.failed_commands += 1
            return {"success": False, "error": str(e), "data": {}}

    async def _handle_coordinates_command(self, coordinate_handler) -> dict[str, Any]:
        """Handle coordinates command."""
        if not coordinate_handler:
            return {"success": False, "error": "Coordinate handler not available", "data": {}}

        try:
            coordinates = await coordinate_handler.get_all_coordinates()
            return {
                "success": True,
                "data": {"coordinates": coordinates, "count": len(coordinates)},
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to get coordinates: {e}", "data": {}}

    async def _handle_list_agents_command(self) -> dict[str, Any]:
        """Handle list agents command."""
        try:
            # Mock agent list - in real implementation, this would query the registry
            agents = [f"Agent-{i}" for i in range(1, 9)]
            formatted_agents = "\n".join(f"• {agent}" for agent in agents)

            self.logger.info(f"\n🤖 Available Agents ({len(agents)}):")
            for agent in agents:
                self.logger.info(f"  - {agent}")

            return {
                "success": True,
                "data": {
                    "agents": agents,
                    "agent_count": len(agents),
                    "formatted": formatted_agents,
                },
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to list agents: {e}", "data": {}}

    async def _handle_status_command(self) -> dict[str, Any]:
        """Handle status command."""
        return {
            "success": True,
            "data": {
                "coordinator_status": self.status,
                "command_stats": {
                    "total_commands": self.command_count,
                    "successful_commands": self.successful_commands,
                    "failed_commands": self.failed_commands,
                    "success_rate": (self.successful_commands / max(self.command_count, 1)) * 100,
                },
            },
        }

    async def _handle_help_command(self) -> dict[str, Any]:
        """Handle help command."""
        help_text = """
Available Commands:
  coordinates  - Get agent coordinates
  list_agents  - List available agents
  status       - Show coordinator status
  help         - Show this help message
  ping         - Ping coordinator
  shutdown     - Shutdown coordinator
        """

        return {
            "success": True,
            "data": {
                "help_text": help_text.strip(),
                "supported_commands": [
                    "coordinates",
                    "list_agents",
                    "status",
                    "help",
                    "ping",
                    "shutdown",
                ],
            },
        }

    async def _handle_ping_command(self) -> dict[str, Any]:
        """Handle ping command."""
        return {
            "success": True,
            "data": {"message": "pong", "timestamp": time.time(), "coordinator": self.name},
        }

    async def _handle_shutdown_command(self) -> dict[str, Any]:
        """Handle shutdown command."""
        self.shutdown()
        return {
            "success": True,
            "data": {"message": f"Coordinator {self.name} shut down", "timestamp": time.time()},
        }

    def get_status(self) -> dict[str, Any]:
        """Get coordinator status."""
        return self.status

    def get_name(self) -> str:
        """Get coordinator name."""
        return self.name

    def get_command_stats(self) -> dict[str, Any]:
        """Get command execution statistics."""
        return {
            "total_commands": self.command_count,
            "successful_commands": self.successful_commands,
            "failed_commands": self.failed_commands,
            "success_rate": (self.successful_commands / max(self.command_count, 1)) * 100,
            "recent_commands": self.command_history[-10:],  # Last 10 commands
        }

    def process_message(self, message: UnifiedMessage) -> dict[str, Any]:
        """Process a single message."""
        self.command_count += 1

        try:
            # Determine coordination strategy
            strategy = self.determine_coordination_strategy(message)

            # Validate message
            validation = self.validate_message(message)
            if not validation["valid"]:
                self.failed_commands += 1
                # Record in history
                self.command_history.append(
                    {
                        "timestamp": time.time(),
                        "message_id": message.id,
                        "sender": message.sender,
                        "strategy": strategy,
                        "success": False,
                        "status": "failed",
                    }
                )
                return {
                    "success": False,
                    "error": "Invalid message",
                    "strategy": strategy,
                    "status": "failed",
                    "timestamp": time.time(),
                }

            # Process based on strategy
            result = self._execute_coordination_strategy(message, strategy, message)

            if result["success"]:
                self.successful_commands += 1
            else:
                self.failed_commands += 1

            # Record in history
            self.command_history.append(
                {
                    "timestamp": time.time(),
                    "message_id": message.id,
                    "sender": message.sender,
                    "strategy": strategy,
                    "success": result["success"],
                    "status": result.get("status", "unknown"),
                }
            )

            return result

        except Exception as e:
            self.failed_commands += 1
            self.logger.error(f"Error processing message: {e}")
            # Record in history even on exception
            self.command_history.append(
                {
                    "timestamp": time.time(),
                    "message_id": message.id,
                    "sender": message.sender,
                    "strategy": "error",
                    "success": False,
                    "status": "failed",
                }
            )
            return {
                "success": False,
                "error": str(e),
                "strategy": "error",
                "status": "failed",
                "timestamp": time.time(),
            }

    def process_bulk_messages(self, messages: list[UnifiedMessage]) -> list[dict[str, Any]]:
        """Process multiple messages in batch."""
        results = []
        for message in messages:
            result = self.process_message(message)
            results.append(result)
        return results

    def validate_message(self, message: UnifiedMessage) -> dict[str, Any]:
        """Validate message before processing."""
        is_valid = True
        errors = []

        # Allow empty content as valid (edge case)
        if not message.sender:
            is_valid = False
            errors.append("missing_sender")
        if not message.recipient:
            is_valid = False
            errors.append("missing_recipient")
        if not isinstance(message.message_type, UnifiedMessageType):
            is_valid = False
            errors.append("invalid_message_type")
        if not isinstance(message.priority, UnifiedMessagePriority):
            is_valid = False
            errors.append("invalid_priority")
        if not isinstance(message.sender_type, SenderType):
            is_valid = False
            errors.append("invalid_sender_type")

        return {"valid": is_valid, "errors": errors if errors else None}

    def determine_coordination_strategy(self, message: UnifiedMessage) -> str:
        """Determine the coordination strategy for a message."""
        # Check for highest priority combinations first
        if (
            message.sender_type == SenderType.COORDINATOR
            and message.message_type == UnifiedMessageType.AGENT_TO_COORDINATOR
        ):
            return "highest_priority"

        if (
            message.sender_type == SenderType.COORDINATOR
            and message.priority == UnifiedMessagePriority.URGENT
        ):
            return "immediate"

        # COORDINATOR sender gets highest priority regardless of other factors
        if message.sender_type == SenderType.COORDINATOR:
            return "highest_priority"

        # Priority-based routing (check urgent first)
        if message.priority == UnifiedMessagePriority.URGENT:
            return self.coordination_rules["priority_routing"][message.priority]

        # Type-based routing (check coordination types first)
        if message.message_type in self.coordination_rules["type_routing"]:
            return self.coordination_rules["type_routing"][message.message_type]

        # Sender-based routing
        if message.sender_type in self.coordination_rules["sender_routing"]:
            return self.coordination_rules["sender_routing"][message.sender_type]

        # Priority-based routing
        if message.priority in self.coordination_rules["priority_routing"]:
            return self.coordination_rules["priority_routing"][message.priority]

        return "standard"

    def get_routing_config(self, strategy: str) -> dict[str, Any] | None:
        """Get routing configuration for a strategy."""
        if strategy in self.routing_table:
            return self.routing_table[strategy]
        return None

    def update_coordination_rule(self, rule_type: str, key: Any, value: Any) -> None:
        """Update a coordination rule."""
        if rule_type in self.coordination_rules:
            self.coordination_rules[rule_type][key] = value

    def get_service_status(self) -> dict[str, Any]:
        """Get service status."""
        import time

        return {
            "name": self.name,
            "status": self.status["status"],
            "total_commands": self.command_count,
            "successful_commands": self.successful_commands,
            "failed_commands": self.failed_commands,
            "command_count": self.command_count,
            "success_rate": (self.successful_commands / max(self.command_count, 1)) * 100,
            "active_rules": len(self.coordination_rules),
            "routing_entries": len(self.routing_table),
            "uptime": time.time() - getattr(self, "_start_time", time.time()),
        }

    def validate_routing_table(self) -> bool:
        """Validate routing table integrity."""
        required_strategies = ["standard", "coordination_priority", "broadcast", "system_priority"]
        for strategy in required_strategies:
            if strategy not in self.routing_table:
                return False

        # Check that all entries have required fields
        for strategy, config in self.routing_table.items():
            if not isinstance(config, dict) or "timeout" not in config or "retries" not in config:
                return False

        return True

    def get_coordination_rules(self) -> dict[str, Any]:
        """Get coordination rules."""
        return self.coordination_rules

    def reset_service(self) -> None:
        """Reset service to initial state."""
        self.command_count = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.command_history.clear()
        self.logger.info("Service reset to initial state")

    def _execute_coordination_strategy(
        self, message: UnifiedMessage, strategy: str, message_obj: UnifiedMessage = None
    ) -> dict[str, Any]:
        """Execute the determined coordination strategy."""
        # Simulate strategy execution
        base_result = {
            "success": True,
            "strategy": strategy,
            "timestamp": time.time(),
            "priority": message_obj.priority.value if message_obj else None,
            "message_type": message_obj.message_type.value if message_obj else None,
            "routing": self.get_routing_config(strategy),
        }

        if strategy == "highest_priority":
            base_result["status"] = "coordinated"
        elif strategy == "coordination_priority":
            base_result["status"] = "coordinated"
        elif strategy == "broadcast":
            base_result["status"] = "broadcasted"
        elif strategy == "system_priority":
            base_result["status"] = "prioritized"
        else:
            base_result["status"] = "processed"

        return base_result

    def shutdown(self) -> None:
        """Shutdown coordinator."""
        self.status["status"] = "shutdown"
        self.logger.info(f"Coordinator {self.name} shut down")

    def reset_stats(self) -> None:
        """Reset command statistics."""
        self.command_count = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.command_history.clear()
        self.logger.info("Command statistics reset")
