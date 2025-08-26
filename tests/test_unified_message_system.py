#!/usr/bin/env python3
"""
Test Unified Message System - Agent Cellphone V2
===============================================

Comprehensive tests for the unified message system.
Verifies consolidation of all Message classes and backward compatibility.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock

from src.services.messaging.models.unified_message import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageStatus,
    UnifiedMessageTag,
    # Backward compatibility aliases
    Message,
    V2Message,
    AgentMessage,
)


class TestUnifiedMessageSystem:
    """Test suite for unified message system"""

    def test_unified_message_creation(self):
        """Test basic UnifiedMessage creation"""
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
            message_type=UnifiedMessageType.COORDINATION,
            priority=UnifiedMessagePriority.HIGH,
        )
        
        assert message.message_id is not None
        assert message.sender_id == "Agent-1"
        assert message.recipient_id == "Agent-2"
        assert message.content == "Test message"
        assert message.message_type == UnifiedMessageType.COORDINATION
        assert message.priority == UnifiedMessagePriority.HIGH
        assert message.status == UnifiedMessageStatus.PENDING
        assert message.timestamp is not None
        assert message.created_at is not None

    def test_backward_compatibility_aliases(self):
        """Test that backward compatibility aliases work correctly"""
        # Test that all aliases point to the same class
        assert Message is UnifiedMessage
        assert V2Message is UnifiedMessage
        assert AgentMessage is UnifiedMessage
        
        # Test that aliases can be instantiated
        message1 = Message(sender_id="Agent-1", recipient_id="Agent-2", content="Test")
        message2 = V2Message(sender_id="Agent-1", recipient_id="Agent-2", content="Test")
        message3 = AgentMessage(sender_id="Agent-1", recipient_id="Agent-2", content="Test")
        
        assert isinstance(message1, UnifiedMessage)
        assert isinstance(message2, UnifiedMessage)
        assert isinstance(message3, UnifiedMessage)

    def test_v1_compatibility_fields(self):
        """Test V1 compatibility fields are set correctly"""
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
        )
        
        # V1 compatibility fields should be set
        assert message.from_agent == "Agent-1"
        assert message.to_agent == "Agent-2"
        
        # Test reverse compatibility
        message2 = UnifiedMessage(
            from_agent="Agent-3",
            to_agent="Agent-4",
            content="Test message 2",
        )
        
        assert message2.sender_id == "Agent-3"
        assert message2.recipient_id == "Agent-4"

    def test_message_state_management(self):
        """Test message state management methods"""
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
        )
        
        # Test mark_delivered
        message.mark_delivered()
        assert message.status == UnifiedMessageStatus.DELIVERED
        assert message.delivered_at is not None
        
        # Test mark_acknowledged
        message.mark_acknowledged()
        assert message.status == UnifiedMessageStatus.ACKNOWLEDGED
        assert message.acknowledged_at is not None
        
        # Test mark_read
        message.mark_read()
        assert message.status == UnifiedMessageStatus.READ
        assert message.read_at is not None
        
        # Test mark_failed
        message.mark_failed("Test error")
        assert message.status == UnifiedMessageStatus.FAILED
        assert message.payload["error"] == "Test error"

    def test_retry_delivery(self):
        """Test retry delivery functionality"""
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
            max_retries=2,
        )
        
        # Test successful retry
        assert message.retry_delivery() is True
        assert message.retry_count == 1
        assert message.status == UnifiedMessageStatus.RETRYING
        
        # Test second retry
        assert message.retry_delivery() is True
        assert message.retry_count == 2
        assert message.status == UnifiedMessageStatus.RETRYING
        
        # Test max retries exceeded
        assert message.retry_delivery() is False
        assert message.status == UnifiedMessageStatus.FAILED
        assert message.payload["error"] == "Max retries exceeded"

    def test_expiration_checking(self):
        """Test message expiration functionality"""
        # Test non-expired message
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
            expires_at=datetime.now() + timedelta(hours=1),
        )
        assert message.is_expired() is False
        
        # Test expired message
        message.expires_at = datetime.now() - timedelta(hours=1)
        assert message.is_expired() is True
        
        # Test message without expiration
        message.expires_at = None
        assert message.is_expired() is False

    def test_delivery_readiness(self):
        """Test message delivery readiness checking"""
        # Test ready message
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
        )
        assert message.is_ready_for_delivery() is True
        
        # Test failed message
        message.status = UnifiedMessageStatus.FAILED
        assert message.is_ready_for_delivery() is False
        
        # Test expired message
        message.status = UnifiedMessageStatus.PENDING
        message.expires_at = datetime.now() - timedelta(hours=1)
        assert message.is_ready_for_delivery() is False
        
        # Test max retries exceeded
        message.expires_at = None
        message.retry_count = 3
        message.max_retries = 3
        assert message.is_ready_for_delivery() is False

    def test_serialization(self):
        """Test message serialization to/from dictionary"""
        original_message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
            message_type=UnifiedMessageType.COORDINATION,
            priority=UnifiedMessagePriority.HIGH,
            payload={"key": "value"},
        )
        
        # Test to_dict
        message_dict = original_message.to_dict()
        assert isinstance(message_dict, dict)
        assert message_dict["sender_id"] == "Agent-1"
        assert message_dict["recipient_id"] == "Agent-2"
        assert message_dict["content"] == "Test message"
        assert message_dict["message_type"] == "coordination"
        assert message_dict["priority"] == "high"
        assert message_dict["payload"] == {"key": "value"}
        
        # Test from_dict
        restored_message = UnifiedMessage.from_dict(message_dict)
        assert restored_message.sender_id == original_message.sender_id
        assert restored_message.recipient_id == original_message.recipient_id
        assert restored_message.content == original_message.content
        assert restored_message.message_type == original_message.message_type
        assert restored_message.priority == original_message.priority
        assert restored_message.payload == original_message.payload

    def test_v1_format_compatibility(self):
        """Test V1 format compatibility methods"""
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
            tag=UnifiedMessageTag.COORDINATE,
        )
        
        # Test to_v1_format
        v1_format = message.to_v1_format()
        assert v1_format["from_agent"] == "Agent-1"
        assert v1_format["to_agent"] == "Agent-2"
        assert v1_format["content"] == "Test message"
        assert v1_format["tag"] == "[COORDINATE]"
        assert v1_format["timestamp"] is not None
        
        # Test from_v1_format
        v1_data = {
            "from_agent": "Agent-3",
            "to_agent": "Agent-4",
            "content": "V1 test message",
            "tag": "[NORMAL]",
            "timestamp": datetime.now().timestamp(),
        }
        
        v1_message = UnifiedMessage.from_v1_format(v1_data)
        assert v1_message.sender_id == "Agent-3"
        assert v1_message.recipient_id == "Agent-4"
        assert v1_message.content == "V1 test message"
        assert v1_message.tag == UnifiedMessageTag.NORMAL

    def test_dependency_management(self):
        """Test dependency management functionality"""
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
        )
        
        # Test adding dependencies
        message.add_dependency("dep1")
        message.add_dependency("dep2")
        assert "dep1" in message.dependencies
        assert "dep2" in message.dependencies
        assert message.has_dependencies() is True
        
        # Test removing dependencies
        message.remove_dependency("dep1")
        assert "dep1" not in message.dependencies
        assert "dep2" in message.dependencies
        
        # Test dependency satisfaction checking
        assert message.are_dependencies_satisfied(["dep2"]) is True
        assert message.are_dependencies_satisfied(["dep1"]) is False

    def test_utility_methods(self):
        """Test utility methods"""
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test message",
            message_type=UnifiedMessageType.SYSTEM,
        )
        
        # Test string representation
        str_repr = str(message)
        assert "Agent-1 → Agent-2" in str_repr
        assert "Test message" in str_repr
        
        # Test detailed representation
        repr_str = repr(message)
        assert "UnifiedMessage" in repr_str
        assert message.message_id in repr_str
        
        # Test cloning
        cloned_message = message.clone()
        assert cloned_message.message_id == message.message_id
        assert cloned_message.content == message.content
        assert cloned_message is not message  # Different instance
        
        # Test system message detection
        assert message.is_system_message() is True
        assert message.is_coordination_message() is False
        
        # Test coordination message detection
        coord_message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Coord message",
            message_type=UnifiedMessageType.COORDINATION,
        )
        assert coord_message.is_coordination_message() is True

    def test_enum_values(self):
        """Test all enum values are accessible"""
        # Test message types
        assert UnifiedMessageType.COORDINATION.value == "coordination"
        assert UnifiedMessageType.TASK.value == "task"
        assert UnifiedMessageType.SYSTEM.value == "system"
        assert UnifiedMessageType.ONBOARDING.value == "onboarding"
        
        # Test priorities
        assert UnifiedMessagePriority.LOW.value == "low"
        assert UnifiedMessagePriority.NORMAL.value == "normal"
        assert UnifiedMessagePriority.HIGH.value == "high"
        assert UnifiedMessagePriority.CRITICAL.value == "critical"
        
        # Test statuses
        assert UnifiedMessageStatus.PENDING.value == "pending"
        assert UnifiedMessageStatus.DELIVERED.value == "delivered"
        assert UnifiedMessageStatus.FAILED.value == "failed"
        
        # Test tags
        assert UnifiedMessageTag.NORMAL.value == "[NORMAL]"
        assert UnifiedMessageTag.COORDINATE.value == "[COORDINATE]"
        assert UnifiedMessageTag.RESCUE.value == "[RESCUE]"

    def test_error_handling(self):
        """Test error handling in edge cases"""
        # Test with minimal data
        message = UnifiedMessage()
        assert message.message_id is not None
        assert message.timestamp is not None
        assert message.created_at is not None
        
        # Test with None values
        message = UnifiedMessage(
            sender_id="Agent-1",
            recipient_id="Agent-2",
            content="Test",
            payload=None,
            dependencies=None,
            tags=None,
        )
        assert message.payload == {}
        assert message.dependencies == []
        assert message.tags == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
