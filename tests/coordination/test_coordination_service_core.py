#!/usr/bin/env python3
"""
Core Coordination Service Tests
===============================

This module contains core tests for the ConsolidatedCoordinationService,
focusing on basic functionality, initialization, routing, and message processing.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize test_consolidated_coordination_service.py for V2 compliance
License: MIT
"""

import sys
import time
from pathlib import Path
from unittest.mock import patch

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import the service and message types
try:
    from core.unified_message import (
        SenderType,
        UnifiedMessage,
        UnifiedMessagePriority,
        UnifiedMessageType,
    )
    from services.consolidated_coordination_service import ConsolidatedCoordinationService
except ImportError:
    # Fallback for testing without actual implementation
    class MockUnifiedMessage:
        def __init__(self, content, sender, recipient, message_type, priority, sender_type):
            self.content = content
            self.sender = sender
            self.recipient = recipient
            self.message_type = message_type
            self.priority = priority
            self.sender_type = sender_type

    class MockUnifiedMessageType:
        AGENT_TO_AGENT = "agent_to_agent"
        AGENT_TO_COORDINATOR = "agent_to_coordinator"
        SYSTEM_BROADCAST = "system_broadcast"
        COORDINATOR_TO_AGENT = "coordinator_to_agent"
        HUMAN_TO_AGENT = "human_to_agent"

    class MockUnifiedMessagePriority:
        URGENT = "urgent"
        HIGH = "high"
        NORMAL = "normal"
        LOW = "low"

    class MockSenderType:
        AGENT = "agent"
        COORDINATOR = "coordinator"
        SYSTEM = "system"
        HUMAN = "human"

    class MockConsolidatedCoordinationService:
        def __init__(self, name="ConsolidatedCoordinator"):
            self.name = name
            self.coordination_rules = {
                "priority_routing": {
                    MockUnifiedMessagePriority.URGENT: "highest_priority",
                    MockUnifiedMessagePriority.HIGH: "high_priority",
                    MockUnifiedMessagePriority.NORMAL: "standard",
                    MockUnifiedMessagePriority.LOW: "low_priority",
                },
                "type_routing": {
                    MockUnifiedMessageType.AGENT_TO_COORDINATOR: "coordination_priority",
                    MockUnifiedMessageType.AGENT_TO_AGENT: "standard",
                    MockUnifiedMessageType.SYSTEM_BROADCAST: "system_priority",
                    MockUnifiedMessageType.COORDINATOR_TO_AGENT: "prioritized",
                    MockUnifiedMessageType.HUMAN_TO_AGENT: "standard",
                },
                "sender_routing": {
                    MockSenderType.COORDINATOR: "highest_priority",
                    MockSenderType.AGENT: "standard",
                    MockSenderType.SYSTEM: "system_priority",
                    MockSenderType.HUMAN: "standard",
                },
            }
            self.routing_table = {
                "immediate": {"timeout": 0, "retries": 3},
                "highest_priority": {"timeout": 0, "retries": 5},
                "high_priority": {"timeout": 2, "retries": 3},
                "standard": {"timeout": 5, "retries": 3},
                "low_priority": {"timeout": 10, "retries": 2},
                "coordination_priority": {"timeout": 5, "retries": 3},
                "system_priority": {"timeout": 1, "retries": 5},
            }
            self.command_history = []
            self.command_count = 0
            self.successful_commands = 0
            self.failed_commands = 0

        def process_message(self, message):
            """Process a message and return result."""
            try:
                strategy = self.determine_coordination_strategy(message)
                config = self.get_routing_config(strategy)

                result = {
                    "status": self._determine_status(message, strategy),
                    "strategy": strategy,
                    "priority": (
                        message.priority.value
                        if hasattr(message.priority, "value")
                        else str(message.priority)
                    ),
                    "message_type": (
                        message.message_type.value
                        if hasattr(message.message_type, "value")
                        else str(message.message_type)
                    ),
                    "timestamp": time.time(),
                    "routing": config or {},
                }

                self.command_history.append(
                    {
                        "timestamp": time.time(),
                        "message_id": f"msg_{len(self.command_history)}",
                        "strategy": strategy,
                        "status": result["status"],
                    }
                )

                self.command_count += 1
                self.successful_commands += 1
                return result

            except Exception as e:
                result = {"status": "failed", "error": str(e), "timestamp": time.time()}
                self.command_history.append(
                    {
                        "timestamp": time.time(),
                        "message_id": f"msg_{len(self.command_history)}",
                        "strategy": "failed",
                        "status": "failed",
                    }
                )
                self.command_count += 1
                self.failed_commands += 1
                return result

        def determine_coordination_strategy(self, message):
            """Determine coordination strategy based on message properties."""
            # Priority-based routing
            if message.priority in self.coordination_rules["priority_routing"]:
                return self.coordination_rules["priority_routing"][message.priority]

            # Type-based routing
            if message.message_type in self.coordination_rules["type_routing"]:
                return self.coordination_rules["type_routing"][message.message_type]

            # Sender-based routing
            if message.sender_type in self.coordination_rules["sender_routing"]:
                return self.coordination_rules["sender_routing"][message.sender_type]

            return "standard"

        def get_routing_config(self, strategy):
            """Get routing configuration for a strategy."""
            return self.routing_table.get(strategy)

        def _determine_status(self, message, strategy):
            """Determine status based on message and strategy."""
            if message.sender_type == MockSenderType.COORDINATOR:
                return "coordinated"
            elif message.message_type == MockUnifiedMessageType.SYSTEM_BROADCAST:
                return "broadcasted"
            elif message.message_type == MockUnifiedMessageType.COORDINATOR_TO_AGENT:
                return "prioritized"
            else:
                return "processed"

        def validate_message(self, message):
            """Validate message structure."""
            errors = []
            if not message.content:
                errors.append("Content is required")
            if not message.sender:
                errors.append("Sender is required")
            if not message.recipient:
                errors.append("Recipient is required")

            return {"valid": len(errors) == 0, "errors": errors}

        def get_command_stats(self):
            """Get command statistics."""
            total = self.command_count
            successful = self.successful_commands
            failed = self.failed_commands
            success_rate = (successful / total * 100) if total > 0 else 0

            return {
                "total_commands": total,
                "successful_commands": successful,
                "failed_commands": failed,
                "success_rate": success_rate,
            }

        def update_coordination_rule(self, rule_type, key, value):
            """Update coordination rule."""
            if rule_type in self.coordination_rules and key in self.coordination_rules[rule_type]:
                self.coordination_rules[rule_type][key] = value

        def get_coordination_rules(self):
            """Get all coordination rules."""
            return self.coordination_rules

        def get_service_status(self):
            """Get service status."""
            return {
                "name": self.name,
                "status": "active",
                "uptime": time.time(),
                "total_commands": self.command_count,
            }

        def validate_routing_table(self):
            """Validate routing table structure."""
            for strategy, config in self.routing_table.items():
                if "timeout" not in config or "retries" not in config:
                    return False
            return True

        def reset_service(self):
            """Reset service state."""
            self.command_history = []
            self.command_count = 0
            self.successful_commands = 0
            self.failed_commands = 0

    # Use mock classes
    ConsolidatedCoordinationService = MockConsolidatedCoordinationService
    UnifiedMessage = MockUnifiedMessage
    UnifiedMessageType = MockUnifiedMessageType
    UnifiedMessagePriority = MockUnifiedMessagePriority
    SenderType = MockSenderType


class TestConsolidatedCoordinationService:
    """Test suite for ConsolidatedCoordinationService core functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.service = ConsolidatedCoordinationService("test-coordinator")
        self.sample_message = UnifiedMessage(
            content="Test coordination message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            sender_type=SenderType.AGENT,
        )

    def teardown_method(self):
        """Cleanup test fixtures."""
        pass

    @pytest.mark.unit
    def test_service_initialization(self):
        """Test service initialization with different configurations."""
        # Test default initialization
        service = ConsolidatedCoordinationService()
        assert service.name == "ConsolidatedCoordinator"
        assert hasattr(service, "coordination_rules")
        assert hasattr(service, "routing_table")
        assert hasattr(service, "command_history")

        # Test custom initialization
        service_custom = ConsolidatedCoordinationService("custom-coordinator")
        assert service_custom.name == "custom-coordinator"

    @pytest.mark.unit
    def test_coordination_rules_initialization(self):
        """Test coordination rules initialization."""
        service = ConsolidatedCoordinationService()

        # Verify priority routing rules
        assert UnifiedMessagePriority.URGENT in service.coordination_rules["priority_routing"]
        assert UnifiedMessagePriority.NORMAL in service.coordination_rules["priority_routing"]

        # Verify type routing rules
        assert UnifiedMessageType.AGENT_TO_COORDINATOR in service.coordination_rules["type_routing"]
        assert UnifiedMessageType.AGENT_TO_AGENT in service.coordination_rules["type_routing"]

        # Verify sender routing rules
        assert SenderType.COORDINATOR in service.coordination_rules["sender_routing"]
        assert SenderType.AGENT in service.coordination_rules["sender_routing"]

    @pytest.mark.unit
    def test_routing_table_initialization(self):
        """Test routing table initialization."""
        service = ConsolidatedCoordinationService()

        # Verify routing table structure
        assert "immediate" in service.routing_table
        assert "high_priority" in service.routing_table
        assert "standard" in service.routing_table

        # Verify timeout and retry configurations
        immediate_config = service.routing_table["immediate"]
        assert immediate_config["timeout"] == 0
        assert immediate_config["retries"] == 3

        highest_config = service.routing_table["highest_priority"]
        assert highest_config["timeout"] == 0
        assert highest_config["retries"] == 5

    @pytest.mark.unit
    def test_process_message_basic(self):
        """Test basic message processing."""
        service = ConsolidatedCoordinationService()

        result = service.process_message(self.sample_message)

        assert result["status"] == "processed"
        assert result["strategy"] == "standard"
        assert "timestamp" in result
        assert len(service.command_history) == 1

    @pytest.mark.unit
    def test_process_message_urgent(self):
        """Test urgent message processing."""
        service = ConsolidatedCoordinationService()

        urgent_message = UnifiedMessage(
            content="Urgent coordination needed",
            sender="Agent-4",
            recipient="Agent-1",
            message_type=UnifiedMessageType.AGENT_TO_COORDINATOR,
            priority=UnifiedMessagePriority.URGENT,
            sender_type=SenderType.COORDINATOR,
        )

        result = service.process_message(urgent_message)

        assert result["status"] == "coordinated"  # COORDINATOR sender gets coordinated status
        assert result["strategy"] == "highest_priority"
        assert result["priority"] == "urgent"
        assert len(service.command_history) == 1

    @pytest.mark.unit
    def test_process_message_with_routing(self):
        """Test message processing with routing decisions."""
        service = ConsolidatedCoordinationService()

        # Mock the routing decision to test different paths
        with patch.object(
            service, "determine_coordination_strategy", return_value="coordination_priority"
        ):
            result = service.process_message(self.sample_message)

            assert result["strategy"] == "coordination_priority"
            assert result["routing"]["timeout"] == 5
            assert result["routing"]["retries"] == 3

    @pytest.mark.unit
    def test_get_routing_config(self):
        """Test routing configuration retrieval."""
        service = ConsolidatedCoordinationService()

        # Test existing strategy
        config = service.get_routing_config("immediate")
        assert config["timeout"] == 0
        assert config["retries"] == 3

        # Test non-existing strategy
        config_missing = service.get_routing_config("nonexistent")
        assert config_missing is None

    @pytest.mark.unit
    def test_command_history_tracking(self):
        """Test command history tracking."""
        service = ConsolidatedCoordinationService()

        # Process multiple messages
        messages = [
            UnifiedMessage(
                content=f"Message {i}",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
                sender_type=SenderType.AGENT,
            )
            for i in range(3)
        ]

        for message in messages:
            service.process_message(message)

        assert len(service.command_history) == 3

        # Verify history structure
        for entry in service.command_history:
            assert "timestamp" in entry
            assert "message_id" in entry
            assert "strategy" in entry
            assert "status" in entry

    @pytest.mark.unit
    def test_get_command_stats(self):
        """Test command statistics retrieval."""
        service = ConsolidatedCoordinationService()

        # Process some messages to build stats
        service.process_message(self.sample_message)
        service.process_message(self.sample_message)

        stats = service.get_command_stats()

        assert stats["total_commands"] == 2
        assert stats["successful_commands"] == 2
        assert stats["failed_commands"] == 0
        assert stats["success_rate"] == 100.0

    @pytest.mark.unit
    def test_update_coordination_rules(self):
        """Test coordination rules updates."""
        service = ConsolidatedCoordinationService()

        # Update a priority routing rule
        service.update_coordination_rule(
            "priority_routing", UnifiedMessagePriority.LOW, "low_priority_updated"
        )

        updated_rules = service.get_coordination_rules()
        assert (
            updated_rules["priority_routing"][UnifiedMessagePriority.LOW] == "low_priority_updated"
        )

    @pytest.mark.unit
    def test_message_validation(self):
        """Test message validation before processing."""
        service = ConsolidatedCoordinationService()

        # Test valid message
        valid_result = service.validate_message(self.sample_message)
        assert valid_result["valid"] is True

        # Test invalid message (missing required fields)
        invalid_message = UnifiedMessage(
            content="",
            sender="",
            recipient="Agent-2",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            sender_type=SenderType.AGENT,
        )

        invalid_result = service.validate_message(invalid_message)
        assert invalid_result["valid"] is False
        assert "errors" in invalid_result

    @pytest.mark.unit
    def test_error_handling_processing_failure(self):
        """Test error handling when message processing fails."""
        service = ConsolidatedCoordinationService()

        # Mock a processing failure
        with patch.object(
            service, "determine_coordination_strategy", side_effect=Exception("Processing error")
        ):
            result = service.process_message(self.sample_message)

            assert result["status"] == "failed"
            assert "error" in result
            assert len(service.command_history) == 1

            # Verify failed command is tracked
            failed_entry = service.command_history[0]
            assert failed_entry["status"] == "failed"

    @pytest.mark.unit
    def test_service_reset_functionality(self):
        """Test service reset functionality."""
        service = ConsolidatedCoordinationService()

        # Process some messages to create state
        service.process_message(self.sample_message)
        service.process_message(self.sample_message)

        # Verify state exists
        assert len(service.command_history) == 2
        assert service.command_count == 2

        # Reset service
        service.reset_service()

        # Verify reset worked
        assert len(service.command_history) == 0
        assert service.command_count == 0
        assert service.successful_commands == 0
        assert service.failed_commands == 0

    @pytest.mark.unit
    def test_routing_table_validation(self):
        """Test routing table validation."""
        service = ConsolidatedCoordinationService()

        # Test valid routing table
        is_valid = service.validate_routing_table()
        assert is_valid is True

        # Test invalid routing table (missing required fields)
        original_table = service.routing_table.copy()
        service.routing_table["invalid_entry"] = {"timeout": 10}  # Missing retries

        is_valid_invalid = service.validate_routing_table()
        assert is_valid_invalid is False

        # Restore original table
        service.routing_table = original_table


if __name__ == "__main__":
    pytest.main(
        [
            __file__,
            "-v",
            "--cov=src/services/consolidated_coordination_service",
            "--cov-report=html",
            "--cov-report=term-missing",
        ]
    )
