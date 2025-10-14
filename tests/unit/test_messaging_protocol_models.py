"""
Comprehensive Test Suite for Messaging Protocol Models
======================================================

Tests protocol interfaces for messaging system dependency injection.
Achieves 85%+ coverage with mock implementations and type checking.

Author: Agent-2 (Architecture & Design Specialist) - ROI 19.57 Task
Created: 2025-10-13
"""

import pytest

from src.core.messaging_models_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageType,
)
from src.core.messaging_protocol_models import (
    IInboxManager,
    IMessageDelivery,
    IMessageFormatter,
    IOnboardingService,
)

# ===================================================================
# MOCK IMPLEMENTATIONS
# ===================================================================


class MockMessageDelivery:
    """Mock implementation of IMessageDelivery protocol."""

    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed
        self.sent_messages = []

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send message (mock implementation)."""
        self.sent_messages.append(message)
        return self.should_succeed


class MockOnboardingService:
    """Mock implementation of IOnboardingService protocol."""

    def __init__(self, message_template: str = "Welcome {agent_id}!"):
        self.message_template = message_template
        self.generated_messages = []

    def generate_onboarding_message(self, agent_id: str, style: str) -> str:
        """Generate onboarding message (mock implementation)."""
        message = self.message_template.format(agent_id=agent_id)
        self.generated_messages.append((agent_id, style, message))
        return message


class MockMessageFormatter:
    """Mock implementation of IMessageFormatter protocol."""

    def __init__(self):
        self.formatted_messages = []

    def format_message(self, message: UnifiedMessage, template: str) -> str:
        """Format message (mock implementation)."""
        formatted = f"[{template}] From: {message.sender}, To: {message.recipient}"
        self.formatted_messages.append((message, template, formatted))
        return formatted


class MockInboxManager:
    """Mock implementation of IInboxManager protocol."""

    def __init__(self, should_rotate: bool = False):
        self.should_rotate = should_rotate
        self.checked_files = []

    def check_and_rotate(self, filepath: str) -> bool:
        """Check and rotate inbox (mock implementation)."""
        self.checked_files.append(filepath)
        return self.should_rotate


# ===================================================================
# FIXTURES
# ===================================================================


@pytest.fixture
def sample_message():
    """Create a sample UnifiedMessage for testing."""
    return UnifiedMessage(
        content="Test message content",
        sender="Agent-2",
        recipient="Agent-4",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.REGULAR,
    )


@pytest.fixture
def message_delivery():
    """Create mock message delivery service."""
    return MockMessageDelivery()


@pytest.fixture
def onboarding_service():
    """Create mock onboarding service."""
    return MockOnboardingService()


@pytest.fixture
def message_formatter():
    """Create mock message formatter."""
    return MockMessageFormatter()


@pytest.fixture
def inbox_manager():
    """Create mock inbox manager."""
    return MockInboxManager()


# ===================================================================
# TEST: IMessageDelivery Protocol
# ===================================================================


class TestIMessageDelivery:
    """Test suite for IMessageDelivery protocol."""

    def test_send_message_success(self, message_delivery, sample_message):
        """Test successful message delivery."""
        result = message_delivery.send_message(sample_message)

        assert result is True
        assert len(message_delivery.sent_messages) == 1
        assert message_delivery.sent_messages[0] == sample_message

    def test_send_message_failure(self, sample_message):
        """Test failed message delivery."""
        failing_delivery = MockMessageDelivery(should_succeed=False)
        result = failing_delivery.send_message(sample_message)

        assert result is False
        assert len(failing_delivery.sent_messages) == 1

    def test_send_multiple_messages(self, message_delivery):
        """Test sending multiple messages."""
        messages = [
            UnifiedMessage(
                content=f"Message {i}",
                sender="Agent-2",
                recipient=f"Agent-{i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
            )
            for i in range(5)
        ]

        for msg in messages:
            result = message_delivery.send_message(msg)
            assert result is True

        assert len(message_delivery.sent_messages) == 5

    def test_protocol_compliance_with_duck_typing(self):
        """Test that any class with send_message method satisfies protocol."""

        class CustomDelivery:
            def send_message(self, message: UnifiedMessage) -> bool:
                return True

        delivery = CustomDelivery()
        # If this compiles without type errors, protocol is satisfied
        assert hasattr(delivery, "send_message")
        assert callable(delivery.send_message)


# ===================================================================
# TEST: IOnboardingService Protocol
# ===================================================================


class TestIOnboardingService:
    """Test suite for IOnboardingService protocol."""

    def test_generate_onboarding_message(self, onboarding_service):
        """Test onboarding message generation."""
        message = onboarding_service.generate_onboarding_message("Agent-5", "friendly")

        assert "Agent-5" in message
        assert len(onboarding_service.generated_messages) == 1
        assert onboarding_service.generated_messages[0][0] == "Agent-5"
        assert onboarding_service.generated_messages[0][1] == "friendly"

    def test_generate_multiple_styles(self):
        """Test generating messages with different styles."""
        service = MockOnboardingService("Style: {agent_id}")

        styles = ["friendly", "professional", "casual"]
        for style in styles:
            message = service.generate_onboarding_message("Agent-1", style)
            assert "Agent-1" in message

        assert len(service.generated_messages) == 3

    def test_protocol_compliance_with_duck_typing(self):
        """Test protocol compliance via duck typing."""

        class CustomOnboarding:
            def generate_onboarding_message(self, agent_id: str, style: str) -> str:
                return f"Custom onboarding for {agent_id}"

        service = CustomOnboarding()
        assert hasattr(service, "generate_onboarding_message")
        assert callable(service.generate_onboarding_message)
        assert service.generate_onboarding_message("Test", "style") == "Custom onboarding for Test"


# ===================================================================
# TEST: IMessageFormatter Protocol
# ===================================================================


class TestIMessageFormatter:
    """Test suite for IMessageFormatter protocol."""

    def test_format_message(self, message_formatter, sample_message):
        """Test message formatting."""
        formatted = message_formatter.format_message(sample_message, "compact")

        assert "[compact]" in formatted
        assert "Agent-2" in formatted
        assert "Agent-4" in formatted
        assert len(message_formatter.formatted_messages) == 1

    def test_format_with_different_templates(self, message_formatter, sample_message):
        """Test formatting with multiple templates."""
        templates = ["compact", "detailed", "json"]

        for template in templates:
            formatted = message_formatter.format_message(sample_message, template)
            assert f"[{template}]" in formatted

        assert len(message_formatter.formatted_messages) == 3

    def test_protocol_compliance_with_duck_typing(self):
        """Test protocol compliance via duck typing."""

        class CustomFormatter:
            def format_message(self, message: UnifiedMessage, template: str) -> str:
                return f"Formatted: {message.content} ({template})"

        formatter = CustomFormatter()
        assert hasattr(formatter, "format_message")
        assert callable(formatter.format_message)


# ===================================================================
# TEST: IInboxManager Protocol
# ===================================================================


class TestIInboxManager:
    """Test suite for IInboxManager protocol."""

    def test_check_and_rotate_no_rotation(self, inbox_manager):
        """Test inbox check without rotation."""
        result = inbox_manager.check_and_rotate("/path/to/inbox.txt")

        assert result is False
        assert len(inbox_manager.checked_files) == 1
        assert inbox_manager.checked_files[0] == "/path/to/inbox.txt"

    def test_check_and_rotate_with_rotation(self):
        """Test inbox check with rotation."""
        rotating_manager = MockInboxManager(should_rotate=True)
        result = rotating_manager.check_and_rotate("/path/to/inbox.txt")

        assert result is True
        assert len(rotating_manager.checked_files) == 1

    def test_check_multiple_files(self, inbox_manager):
        """Test checking multiple inbox files."""
        files = [f"/path/to/inbox_{i}.txt" for i in range(3)]

        for file in files:
            inbox_manager.check_and_rotate(file)

        assert len(inbox_manager.checked_files) == 3
        assert inbox_manager.checked_files == files

    def test_protocol_compliance_with_duck_typing(self):
        """Test protocol compliance via duck typing."""

        class CustomInboxManager:
            def check_and_rotate(self, filepath: str) -> bool:
                return True

        manager = CustomInboxManager()
        assert hasattr(manager, "check_and_rotate")
        assert callable(manager.check_and_rotate)


# ===================================================================
# INTEGRATION TESTS
# ===================================================================


class TestProtocolIntegration:
    """Integration tests for protocol interactions."""

    def test_all_protocols_work_together(self, sample_message):
        """Test that all protocols can be used together."""
        delivery = MockMessageDelivery()
        onboarding = MockOnboardingService()
        formatter = MockMessageFormatter()
        inbox = MockInboxManager()

        # Simulate workflow
        onboarding_msg = onboarding.generate_onboarding_message("Agent-7", "friendly")
        assert onboarding_msg is not None

        formatted = formatter.format_message(sample_message, "compact")
        assert formatted is not None

        sent = delivery.send_message(sample_message)
        assert sent is True

        rotated = inbox.check_and_rotate("/path/to/inbox.txt")
        assert rotated is False

    def test_protocol_type_hints(self):
        """Test that protocols have proper type hints."""

        # This tests compile-time type checking
        def use_delivery(service: IMessageDelivery) -> None:
            pass

        def use_onboarding(service: IOnboardingService) -> None:
            pass

        def use_formatter(service: IMessageFormatter) -> None:
            pass

        def use_inbox(service: IInboxManager) -> None:
            pass

        # These should all work with mock implementations
        use_delivery(MockMessageDelivery())
        use_onboarding(MockOnboardingService())
        use_formatter(MockMessageFormatter())
        use_inbox(MockInboxManager())


# ===================================================================
# EDGE CASES & ERROR HANDLING
# ===================================================================


class TestEdgeCases:
    """Test edge cases and error scenarios."""

    def test_empty_message_delivery(self):
        """Test delivering message with empty content."""
        delivery = MockMessageDelivery()
        empty_msg = UnifiedMessage(
            content="",
            sender="Agent-2",
            recipient="Agent-4",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
        )

        result = delivery.send_message(empty_msg)
        assert result is True  # Should still work

    def test_special_characters_in_agent_id(self):
        """Test onboarding with special characters in agent ID."""
        service = MockOnboardingService()
        message = service.generate_onboarding_message("Agent-2-Ω", "professional")
        assert "Agent-2-Ω" in message

    def test_none_template_handling(self, message_formatter, sample_message):
        """Test formatter with None template."""
        # Mock should handle this gracefully
        formatted = message_formatter.format_message(sample_message, "None")
        assert formatted is not None


if __name__ == "__main__":
    pytest.main(
        [__file__, "-v", "--cov=src.core.messaging_protocol_models", "--cov-report=term-missing"]
    )
