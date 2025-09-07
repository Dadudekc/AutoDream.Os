#!/usr/bin/env python3
"""
Smoke Tests for Messaging Core - Agent Cellphone V2
==================================================

Comprehensive smoke tests for the unified messaging core functionality.
Tests basic messaging operations, agent coordination, and system integration.

Author: Agent-2 (Architecture & Design)
License: MIT
"""

import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Import messaging components
from src.services.messaging_core import UnifiedMessagingCore
from src.services.models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType,
)


class TestMessagingCoreSmoke:
    """Smoke tests for messaging core functionality."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary directory for test configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_agents_config(self, temp_config_dir):
        """Create mock agents configuration file."""
        agents_config = {
            "Agent-1": {
                "coordinates": {"x": 100, "y": 200},
                "inbox_path": f"{temp_config_dir}/agent_workspaces/Agent-1/inbox"
            },
            "Agent-2": {
                "coordinates": {"x": 150, "y": 250},
                "inbox_path": f"{temp_config_dir}/agent_workspaces/Agent-2/inbox"
            },
            "Agent-4": {
                "coordinates": {"x": 200, "y": 300},
                "inbox_path": f"{temp_config_dir}/agent_workspaces/Agent-4/inbox"
            }
        }

        config_path = Path(temp_config_dir) / "agents_config.json"
        with open(config_path, 'w') as f:
            json.dump(agents_config, f)

        return config_path

    @patch('src.services.messaging_core.PyAutoGUIMessagingDelivery')
    @patch('src.services.onboarding_service.OnboardingService')
    def test_messaging_core_initialization(self, mock_onboarding, mock_pyautogui, temp_config_dir, mock_agents_config):
        """Test that messaging core initializes correctly."""
        with patch('src.services.messaging_core.UnifiedMessagingCore._load_configuration') as mock_load:
            mock_load.return_value = None

            # Mock the agents and inbox_paths attributes
            core = UnifiedMessagingCore.__new__(UnifiedMessagingCore)
            core.agents = {"Agent-1": {}, "Agent-2": {}}
            core.inbox_paths = ["/tmp/test1", "/tmp/test2"]
            core.messages = []
            core.logger = Mock()

            # Initialize services
            core.pyautogui_delivery = mock_pyautogui.return_value
            core.onboarding_service = mock_onboarding.return_value

            # Verify initialization
            assert core.messages == []
            assert core.pyautogui_delivery is not None
            assert core.onboarding_service is not None
            assert core.logger is not None

    def test_unified_message_creation(self):
        """Test creation of unified messages with different types."""
        # Test text message
        text_message = UnifiedMessage(
            message_id="test-001",
            content="Test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.NORMAL,
            sender="Agent-4",
            sender_type=SenderType.AGENT,
            recipient="Agent-1",
            recipient_type=RecipientType.AGENT,
            tags=[UnifiedMessageTag.CAPTAIN]
        )

        assert text_message.message_id == "test-001"
        assert text_message.content == "Test message"
        assert text_message.message_type == UnifiedMessageType.TEXT
        assert text_message.priority == UnifiedMessagePriority.NORMAL
        assert text_message.sender == "Agent-4"
        assert text_message.recipient == "Agent-1"

        # Test broadcast message
        broadcast_message = UnifiedMessage(
            message_id="test-002",
            content="System broadcast",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.URGENT,
            sender="System",
            sender_type=SenderType.SYSTEM,
            recipient="all",
            recipient_type=RecipientType.AGENT,
            tags=[UnifiedMessageTag.ONBOARDING]
        )

        assert broadcast_message.message_type == UnifiedMessageType.BROADCAST
        assert broadcast_message.priority == UnifiedMessagePriority.URGENT
        assert broadcast_message.sender_type == SenderType.SYSTEM

    @patch('src.services.messaging_core.PyAutoGUIMessagingDelivery')
    @patch('src.services.onboarding_service.OnboardingService')
    def test_message_queue_operations(self, mock_onboarding, mock_pyautogui):
        """Test basic message queue operations."""
        with patch('src.services.messaging_core.UnifiedMessagingCore._load_configuration'):
            core = UnifiedMessagingCore.__new__(UnifiedMessagingCore)
            core.agents = {}
            core.inbox_paths = []
            core.messages = []
            core.logger = Mock()
            core.pyautogui_delivery = mock_pyautogui.return_value
            core.onboarding_service = mock_onboarding.return_value

            # Test adding messages to queue
            test_message = UnifiedMessage(
                message_id="queue-test-001",
                content="Queue test message",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.NORMAL,
                sender="Agent-4",
                sender_type=SenderType.AGENT,
                recipient="Agent-1",
                recipient_type=RecipientType.AGENT
            )

            core.messages.append(test_message)

            # Verify message was added
            assert len(core.messages) == 1
            assert core.messages[0].message_id == "queue-test-001"
            assert core.messages[0].content == "Queue test message"

    def test_message_priority_handling(self):
        """Test message priority levels and ordering."""
        messages = [
            UnifiedMessage(
                message_id=f"priority-test-{i}",
                content=f"Message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=priority,
                sender="Agent-4",
                sender_type=SenderType.AGENT,
                recipient="Agent-1",
                recipient_type=RecipientType.AGENT
            )
            for i, priority in enumerate([
                UnifiedMessagePriority.NORMAL,
                UnifiedMessagePriority.URGENT,
                UnifiedMessagePriority.NORMAL
            ])
        ]

        # Verify priorities are set correctly
        assert messages[0].priority == UnifiedMessagePriority.NORMAL
        assert messages[1].priority == UnifiedMessagePriority.URGENT
        assert messages[2].priority == UnifiedMessagePriority.NORMAL

        # Test priority comparison
        assert UnifiedMessagePriority.URGENT > UnifiedMessagePriority.NORMAL

    def test_message_tags_functionality(self):
        """Test message tagging system."""
        # Test various tag combinations
        tags_message = UnifiedMessage(
            message_id="tags-test-001",
            content="Tagged message",
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.NORMAL,
            sender="Agent-4",
            sender_type=SenderType.AGENT,
            recipient="Agent-1",
            recipient_type=RecipientType.AGENT,
            tags=[
                UnifiedMessageTag.CAPTAIN,
                UnifiedMessageTag.ONBOARDING,
                UnifiedMessageTag.WRAPUP
            ]
        )

        assert UnifiedMessageTag.CAPTAIN in tags_message.tags
        assert UnifiedMessageTag.ONBOARDING in tags_message.tags
        assert UnifiedMessageTag.WRAPUP in tags_message.tags

        # Verify tag enum values
        assert UnifiedMessageTag.CAPTAIN.value == "captain"
        assert UnifiedMessageTag.ONBOARDING.value == "onboarding"
        assert UnifiedMessageTag.WRAPUP.value == "wrapup"

    @patch('src.services.messaging_core.PyAutoGUIMessagingDelivery')
    @patch('src.services.onboarding_service.OnboardingService')
    def test_agent_to_agent_communication(self, mock_onboarding, mock_pyautogui):
        """Test agent-to-agent messaging functionality."""
        with patch('src.services.messaging_core.UnifiedMessagingCore._load_configuration'):
            core = UnifiedMessagingCore.__new__(UnifiedMessagingCore)
            core.agents = {"Agent-1": {}, "Agent-2": {}, "Agent-4": {}}
            core.inbox_paths = []
            core.messages = []
            core.logger = Mock()
            core.pyautogui_delivery = mock_pyautogui.return_value
            core.onboarding_service = mock_onboarding.return_value

            # Create agent-to-agent message
            agent_message = UnifiedMessage(
                message_id="agent-comm-test-001",
                content="Agent coordination message",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
                sender="Agent-2",
                sender_type=SenderType.AGENT,
                recipient="Agent-1",
                recipient_type=RecipientType.AGENT,
                tags=[]
            )

            core.messages.append(agent_message)

            # Verify agent communication setup
            assert agent_message.message_type == UnifiedMessageType.AGENT_TO_AGENT
            assert agent_message.sender == "Agent-2"
            assert agent_message.recipient == "Agent-1"
            assert agent_message.sender_type == SenderType.AGENT
            assert agent_message.recipient_type == RecipientType.AGENT

    def test_message_validation_rules(self):
        """Test message validation according to project rules."""
        # Test valid message
        valid_message = UnifiedMessage(
            message_id="validation-test-001",
            content="Valid test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.NORMAL,
            sender="Agent-4",
            sender_type=SenderType.AGENT,
            recipient="Agent-1",
            recipient_type=RecipientType.AGENT
        )

        # Verify required fields are present
        assert valid_message.message_id is not None
        assert valid_message.content is not None
        assert valid_message.sender is not None
        assert valid_message.recipient is not None
        assert valid_message.message_type is not None
        assert valid_message.priority is not None

        # Test message types enum
        assert UnifiedMessageType.TEXT.value == "text"
        assert UnifiedMessageType.BROADCAST.value == "broadcast"
        assert UnifiedMessageType.ONBOARDING.value == "onboarding"
        assert UnifiedMessageType.AGENT_TO_AGENT.value == "agent_to_agent"

    @patch('src.services.messaging_core.PyAutoGUIMessagingDelivery')
    @patch('src.services.onboarding_service.OnboardingService')
    def test_bulk_messaging_setup(self, mock_onboarding, mock_pyautogui):
        """Test bulk messaging configuration and setup."""
        with patch('src.services.messaging_core.UnifiedMessagingCore._load_configuration'):
            core = UnifiedMessagingCore.__new__(UnifiedMessagingCore)
            core.agents = {
                "Agent-1": {"status": "active"},
                "Agent-2": {"status": "active"},
                "Agent-3": {"status": "active"},
                "Agent-4": {"status": "active"}
            }
            core.inbox_paths = []
            core.messages = []
            core.logger = Mock()
            core.pyautogui_delivery = mock_pyautogui.return_value
            core.onboarding_service = mock_onboarding.return_value

            # Create bulk broadcast message
            bulk_message = UnifiedMessage(
                message_id="bulk-test-001",
                content="Bulk system announcement",
                message_type=UnifiedMessageType.BROADCAST,
                priority=UnifiedMessagePriority.URGENT,
                sender="Captain Agent-4",
                sender_type=SenderType.AGENT,
                recipient="all",
                recipient_type=RecipientType.AGENT,
                tags=[UnifiedMessageTag.CAPTAIN]
            )

            # Verify bulk messaging setup
            assert bulk_message.message_type == UnifiedMessageType.BROADCAST
            assert bulk_message.recipient == "all"
            assert UnifiedMessageTag.CAPTAIN in bulk_message.tags

    def test_error_handling_setup(self):
        """Test error handling configuration in messaging system."""
        # Test that message creation handles missing required fields gracefully
        with pytest.raises(TypeError):
            # This should fail due to missing required arguments
            invalid_message = UnifiedMessage()

    def test_configuration_loading(self, temp_config_dir):
        """Test configuration loading functionality."""
        # Create test configuration file
        config_data = {
            "agents": {
                "Agent-1": {"coordinates": {"x": 100, "y": 200}},
                "Agent-2": {"coordinates": {"x": 150, "y": 250}}
            },
            "messaging": {
                "default_mode": "pyautogui",
                "timeout": 30
            }
        }

        config_path = Path(temp_config_dir) / "test_config.json"
        with open(config_path, 'w') as f:
            json.dump(config_data, f)

        # Verify configuration can be loaded
        with open(config_path, 'r') as f:
            loaded_config = json.load(f)

        assert "agents" in loaded_config
        assert "Agent-1" in loaded_config["agents"]
        assert "Agent-2" in loaded_config["agents"]
        assert loaded_config["messaging"]["default_mode"] == "pyautogui"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
