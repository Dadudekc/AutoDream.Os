#!/usr/bin/env python3
"""
Messaging Service Core Tests - Modular Test Suite
=================================================

Core functionality tests for messaging service.
Tests initialization, validation, and basic operations.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from unittest.mock import patch

import pytest

from tests.utils.test_base_classes import MessagingServiceTestBase
from tests.utils.test_fixtures import TestDataFactory


class TestMessagingServiceInitialization(MessagingServiceTestBase):
    """Test messaging service initialization."""

    @pytest.mark.unit
    def test_messaging_service_initialization(self, temp_coordinates_file):
        """Test messaging service initialization."""
        from services.messaging.core.messaging_service import MessagingService

        service = MessagingService(temp_coordinates_file)
        assert service.coords_file == temp_coordinates_file
        assert service.loader is not None
        assert service.validation_report is not None

    @pytest.mark.unit
    def test_messaging_service_default_initialization(self):
        """Test messaging service with default coordinate path."""
        from services.messaging.core.messaging_service import MessagingService

        service = MessagingService()
        assert service.coords_file == "config/coordinates.json"
        assert service.loader is not None

    @pytest.mark.unit
    def test_messaging_service_custom_coordinates(self, temp_dir):
        """Test messaging service with custom coordinates."""
        from services.messaging.core.messaging_service import MessagingService

        # Create custom coordinates
        custom_coords = TestDataFactory.create_coordinates_data()
        custom_coords["agents"]["CustomAgent-1"] = {
            "active": True,
            "chat_input_coordinates": [100, 200],
            "onboarding_coordinates": [150, 250],
            "description": "Custom Agent 1",
        }

        temp_path = TestDataFactory.create_temp_json_file(custom_coords)
        try:
            service = MessagingService(temp_path)

            # Test with custom agent
            assert service._is_agent_active("CustomAgent-1") == True
            assert service._is_agent_active("Agent-1") == True  # Defaults to True if not found

            # Test message formatting
            formatted = service._format_a2a_message(
                "Discord-Commander", "CustomAgent-1", "Test", "NORMAL"
            )
            assert "TO: CustomAgent-1" in formatted

        finally:
            TestFileManager.cleanup_file(temp_path)


class TestMessagingServiceValidation(MessagingServiceTestBase):
    """Test messaging service validation."""

    @pytest.mark.unit
    def test_agent_validation(self, messaging_service):
        """Test agent validation."""
        # Test valid agents
        for agent_id in self.test_agents:
            assert messaging_service._is_agent_active(agent_id) == True

        # Test invalid agent (defaults to True if not found)
        assert messaging_service._is_agent_active("InvalidAgent") == True

        # Test empty agent ID (defaults to True if not found)
        assert messaging_service._is_agent_active("") == True

        # Test None agent ID (defaults to True if not found)
        assert messaging_service._is_agent_active(None) == True

    @pytest.mark.unit
    def test_coordinate_loading_validation(self, coordinate_loader):
        """Test coordinate loading validation."""
        # Test coordinate loading
        agent_ids = coordinate_loader.get_agent_ids()
        assert len(agent_ids) == 8
        assert set(agent_ids) == set(self.test_agents)

        # Test coordinate retrieval
        for agent_id, expected_coords in self.expected_coordinates.items():
            coords = coordinate_loader.get_agent_coordinates(agent_id)
            assert coords == expected_coords

    @pytest.mark.unit
    def test_validation_report(self, messaging_service):
        """Test messaging service validation report."""
        assert messaging_service.validation_report is not None
        assert hasattr(messaging_service.validation_report, "is_all_ok")
        assert hasattr(messaging_service.validation_report, "issues")


class TestMessagingServiceFormatting(MessagingServiceTestBase):
    """Test messaging service message formatting."""

    @pytest.mark.unit
    def test_message_formatting_basic(self, messaging_service):
        """Test basic message formatting."""
        formatted = messaging_service._format_a2a_message(
            "Discord-Commander", "Agent-1", "Test message", "NORMAL"
        )

        self.assert_message_formatting(
            formatted, "Discord-Commander", "Agent-1", "Test message", "NORMAL"
        )

    @pytest.mark.unit
    def test_message_formatting_different_priorities(self, messaging_service):
        """Test message formatting with different priorities."""
        priorities = ["NORMAL", "HIGH", "URGENT"]
        for priority in priorities:
            formatted = messaging_service._format_a2a_message(
                "Discord-Commander", "Agent-1", "Test", priority
            )
            assert f"Priority: {priority}" in formatted

    @pytest.mark.unit
    def test_message_formatting_different_senders(self, messaging_service):
        """Test message formatting with different senders."""
        senders = ["Discord-Commander", "Agent-1", "Agent-2", "Test-Sender"]
        for sender in senders:
            formatted = messaging_service._format_a2a_message(sender, "Agent-1", "Test", "NORMAL")
            assert f"FROM: {sender}" in formatted

    @pytest.mark.unit
    def test_message_formatting_special_characters(self, messaging_service):
        """Test message formatting with special characters."""
        special_messages = [
            "Message with émojis 🚀",
            "Message with newlines\nand tabs\t",
            "Message with quotes \"test\" and 'single'",
            "Message with symbols @#$%^&*()",
            "Message with unicode: 中文测试",
        ]

        for message in special_messages:
            formatted = messaging_service._format_a2a_message(
                "Discord-Commander", "Agent-1", message, "NORMAL"
            )
            assert message in formatted

    @pytest.mark.unit
    def test_message_formatting_long_message(self, messaging_service):
        """Test message formatting with long message."""
        long_message = "A" * 2000
        formatted = messaging_service._format_a2a_message(
            "Discord-Commander", "Agent-1", long_message, "NORMAL"
        )
        assert long_message in formatted

    @pytest.mark.unit
    def test_message_formatting_edge_cases(self, messaging_service):
        """Test message formatting edge cases."""
        # Test with empty message
        formatted = messaging_service._format_a2a_message(
            "Discord-Commander", "Agent-1", "", "NORMAL"
        )
        assert "FROM: Discord-Commander" in formatted
        assert "TO: Agent-1" in formatted

        # Test with None message
        formatted = messaging_service._format_a2a_message(
            "Discord-Commander", "Agent-1", None, "NORMAL"
        )
        assert "FROM: Discord-Commander" in formatted
        assert "TO: Agent-1" in formatted

        # Test with very long sender name
        long_sender = "A" * 100
        formatted = messaging_service._format_a2a_message(long_sender, "Agent-1", "Test", "NORMAL")
        assert f"FROM: {long_sender}" in formatted


class TestMessagingServiceErrorHandling(MessagingServiceTestBase):
    """Test messaging service error handling."""

    @pytest.mark.unit
    def test_error_handling_invalid_coordinate_file(self):
        """Test error handling with invalid coordinate file."""
        from services.messaging.core.messaging_service import MessagingService

        # Test with invalid coordinate file
        service = MessagingService("invalid/path/coordinates.json")

        # Should handle gracefully (falls back to default coordinates)
        result = service.send_message("Agent-1", "Test", "Discord-Commander")
        # Result depends on whether PyAutoGUI is available
        assert isinstance(result, bool)

    @pytest.mark.unit
    def test_send_message_invalid_agent(self, messaging_service):
        """Test message sending to invalid agent."""
        # Invalid agent will default to active=True, so it will try to send
        # but fail at coordinate retrieval
        result = messaging_service.send_message(
            "InvalidAgent", "Test message", "Discord-Commander", "NORMAL"
        )
        assert result == False

    @pytest.mark.unit
    def test_send_message_inactive_agent(self, messaging_service):
        """Test message sending to inactive agent."""
        # Mock inactive agent
        with patch.object(messaging_service, "_is_agent_active", return_value=False):
            result = messaging_service.send_message(
                "Agent-1", "Test message", "Discord-Commander", "NORMAL"
            )
            assert result == False
