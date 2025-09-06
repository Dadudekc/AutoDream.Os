#!/usr/bin/env python3
"""
Unit Tests for Messaging Models - Agent Cellphone V2
====================================================

Comprehensive unit tests for messaging model components.
V2 Compliance: 85%+ test coverage requirement.

Author: Agent-6 (Gaming & Entertainment Specialist)
"""

from src.services.models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageStatus,
    UnifiedMessageTag,
)


class TestUnifiedMessageType:
    """Test cases for UnifiedMessageType enum."""

    def test_text_type_value(self):
        """Test TEXT message type value."""
        assert UnifiedMessageType.TEXT.value == "text"

    def test_broadcast_type_value(self):
        """Test BROADCAST message type value."""
        assert UnifiedMessageType.BROADCAST.value == "broadcast"

    def test_onboarding_type_value(self):
        """Test ONBOARDING message type value."""
        assert UnifiedMessageType.ONBOARDING.value == "onboarding"

    def test_all_types_defined(self):
        """Test all message types are properly defined."""
        expected_types = ["text", "broadcast", "onboarding"]
        actual_types = [msg_type.value for msg_type in UnifiedMessageType]
        assert set(actual_types) == set(expected_types)


class TestUnifiedMessagePriority:
    """Test cases for UnifiedMessagePriority enum."""

    def test_regular_priority_value(self):
        """Test REGULAR priority value."""
        assert UnifiedMessagePriority.REGULAR.value == "regular"

    def test_urgent_priority_value(self):
        """Test URGENT priority value."""
        assert UnifiedMessagePriority.URGENT.value == "urgent"

    def test_all_priorities_defined(self):
        """Test all priorities are properly defined."""
        expected_priorities = ["regular", "urgent"]
        actual_priorities = [priority.value for priority in UnifiedMessagePriority]
        assert set(actual_priorities) == set(expected_priorities)


class TestUnifiedMessageStatus:
    """Test cases for UnifiedMessageStatus enum."""

    def test_sent_status_value(self):
        """Test SENT status value."""
        assert UnifiedMessageStatus.SENT.value == "sent"

    def test_delivered_status_value(self):
        """Test DELIVERED status value."""
        assert UnifiedMessageStatus.DELIVERED.value == "delivered"

    def test_all_statuses_defined(self):
        """Test all statuses are properly defined."""
        expected_statuses = ["sent", "delivered"]
        actual_statuses = [status.value for status in UnifiedMessageStatus]
        assert set(actual_statuses) == set(expected_statuses)


class TestUnifiedMessageTag:
    """Test cases for UnifiedMessageTag enum."""

    def test_captain_tag_value(self):
        """Test CAPTAIN tag value."""
        assert UnifiedMessageTag.CAPTAIN.value == "captain"

    def test_onboarding_tag_value(self):
        """Test ONBOARDING tag value."""
        assert UnifiedMessageTag.ONBOARDING.value == "onboarding"

    def test_wrapup_tag_value(self):
        """Test WRAPUP tag value."""
        assert UnifiedMessageTag.WRAPUP.value == "wrapup"

    def test_all_tags_defined(self):
        """Test all tags are properly defined."""
        expected_tags = ["captain", "onboarding", "wrapup"]
        actual_tags = [tag.value for tag in UnifiedMessageTag]
        assert set(actual_tags) == set(expected_tags)


class TestUnifiedMessage:
    """Test cases for UnifiedMessage dataclass."""

    def test_message_creation_with_defaults(self):
        """Test creating message with default values."""
        message = UnifiedMessage(
            content="Test message", sender="Agent-1", recipient="Agent-2"
        )

        assert message.content == "Test message"
        assert message.sender == "Agent-1"
        assert message.recipient == "Agent-2"
        assert message.message_type == UnifiedMessageType.TEXT
        assert message.priority == UnifiedMessagePriority.REGULAR
        assert message.tags == []
        assert message.metadata == {}
        assert get_unified_validator().validate_type(message.timestamp, datetime)
        assert message.message_id is not None

    def test_message_creation_with_custom_values(self):
        """Test creating message with custom values."""
        custom_timestamp = datetime(2024, 1, 1, 12, 0, 0)
        custom_metadata = {"test": "value"}
        custom_tags = [UnifiedMessageTag.CAPTAIN]

        message = UnifiedMessage(
            content="Custom test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.URGENT,
            tags=custom_tags,
            metadata=custom_metadata,
            timestamp=custom_timestamp,
        )

        assert message.message_type == UnifiedMessageType.BROADCAST
        assert message.priority == UnifiedMessagePriority.URGENT
        assert message.tags == custom_tags
        assert message.metadata == custom_metadata
        assert message.timestamp == custom_timestamp

    @patch("src.services.models.messaging_models.datetime")
    def test_message_id_generation(self, mock_datetime):
        """Test message ID generation with timestamp."""
        mock_now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now

        message = UnifiedMessage(content="Test", sender="Agent-1", recipient="Agent-2")

        expected_prefix = "msg_20240101_120000"
        assert message.message_id.startswith(expected_prefix)

    def test_message_with_none_values(self):
        """Test message creation with None values (should be converted to defaults)."""
        message = UnifiedMessage(
            content="Test",
            sender="Agent-1",
            recipient="Agent-2",
            tags=None,
            metadata=None,
            timestamp=None,
            message_id=None,
        )

        assert message.tags == []
        assert message.metadata == {}
        assert get_unified_validator().validate_type(message.timestamp, datetime)
        assert message.message_id is not None

    def test_message_equality(self):
        """Test message equality comparison."""
        message1 = UnifiedMessage(content="Test", sender="Agent-1", recipient="Agent-2")

        message2 = UnifiedMessage(content="Test", sender="Agent-1", recipient="Agent-2")

        # Different instances should not be equal due to different timestamps/message_ids
        assert message1 != message2

        # Same instance should be equal to itself
        assert message1 == message1

    def test_message_string_representation(self):
        """Test string representation of message."""
        message = UnifiedMessage(
            content="Test message",
            sender="Agent-1",
            recipient="Agent-2",
            message_type=UnifiedMessageType.BROADCAST,
        )

        str_repr = str(message)
        assert "UnifiedMessage" in str_repr
        assert "Test message" in str_repr
        assert "Agent-1" in str_repr
        assert "Agent-2" in str_repr


if __name__ == "__main__":
    pytest.main([__file__])
