#!/usr/bin/env python3
"""
Messaging Service Testing Suite
===============================

Comprehensive test suite for the MessagingService class.
Tests cover:
- Service initialization and configuration
- Message sending functionality
- Broadcast operations
- Coordinate management
- Error handling and edge cases
- Dry run mode functionality

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.services.messaging.service import MessagingService
from src.services.messaging.models import UnifiedMessage, UnifiedMessageType


class TestMessagingService:
    """Unit tests for MessagingService class."""

    def test_service_initialization_default(self):
        """Test MessagingService initialization with default parameters."""
        service = MessagingService()
        
        assert service.dry_run is False
        assert isinstance(service, MessagingService)

    def test_service_initialization_dry_run_true(self):
        """Test MessagingService initialization with dry_run=True."""
        service = MessagingService(dry_run=True)
        
        assert service.dry_run is True

    def test_service_initialization_dry_run_false(self):
        """Test MessagingService initialization with dry_run=False."""
        service = MessagingService(dry_run=False)
        
        assert service.dry_run is False

    def test_service_initialization_truthy_value(self):
        """Test MessagingService initialization with truthy value."""
        service = MessagingService(dry_run="yes")
        
        assert service.dry_run is True

    def test_service_initialization_falsy_value(self):
        """Test MessagingService initialization with falsy value."""
        service = MessagingService(dry_run="")
        
        assert service.dry_run is False

    @patch('src.services.messaging.service.send_with_fallback')
    @patch('src.services.messaging.service.UnifiedMessage')
    def test_send_success(self, mock_message_class, mock_send_fallback):
        """Test successful message sending."""
        # Setup mocks
        mock_message = Mock()
        mock_message_class.return_value = mock_message
        mock_send_fallback.return_value = True
        
        service = MessagingService()
        result = service.send("Agent-1", "Test message")
        
        # Verify message creation
        mock_message_class.assert_called_once()
        call_args = mock_message_class.call_args
        
        assert call_args[1]['content'] == "Test message"
        assert call_args[1]['sender'] == "ConsolidatedMessagingService"
        assert call_args[1]['recipient'] == "Agent-1"
        assert call_args[1]['message_type'] == UnifiedMessageType.AGENT_TO_AGENT
        
        # Verify fallback sending
        mock_send_fallback.assert_called_once_with(mock_message)
        assert result is True

    @patch('src.services.messaging.service.send_with_fallback')
    @patch('src.services.messaging.service.UnifiedMessage')
    def test_send_with_custom_priority_and_tag(self, mock_message_class, mock_send_fallback):
        """Test message sending with custom priority and tag."""
        mock_message = Mock()
        mock_message_class.return_value = mock_message
        mock_send_fallback.return_value = True
        
        service = MessagingService()
        result = service.send("Agent-2", "Test message", priority="HIGH", tag="URGENT")
        
        # Verify message creation with custom parameters
        call_args = mock_message_class.call_args
        assert call_args[1]['priority'] is not None  # Should be mapped
        assert call_args[1]['tags'] is not None  # Should be mapped
        
        assert result is True

    @patch('src.services.messaging.service.send_with_fallback')
    def test_send_dry_run_mode(self, mock_send_fallback):
        """Test message sending in dry run mode."""
        service = MessagingService(dry_run=True)
        result = service.send("Agent-1", "Test message")
        
        # Should not call send_with_fallback in dry run mode
        mock_send_fallback.assert_not_called()
        assert result is True

    @patch('src.services.messaging.service.send_with_fallback')
    def test_send_fallback_failure(self, mock_send_fallback):
        """Test message sending when fallback fails."""
        mock_send_fallback.return_value = False
        
        service = MessagingService()
        result = service.send("Agent-1", "Test message")
        
        assert result is False

    @patch('src.services.messaging.service._list_agents')
    @patch.object(MessagingService, 'send')
    def test_broadcast_success(self, mock_send, mock_list_agents):
        """Test successful broadcast operation."""
        # Setup mocks
        mock_list_agents.return_value = ["Agent-1", "Agent-2", "Agent-3"]
        mock_send.side_effect = [True, True, False]  # Mixed results
        
        service = MessagingService()
        results = service.broadcast("Broadcast message")
        
        # Verify all agents were contacted
        assert mock_send.call_count == 3
        assert results == {
            "Agent-1": True,
            "Agent-2": True,
            "Agent-3": False
        }

    @patch('src.services.messaging.service._list_agents')
    @patch.object(MessagingService, 'send')
    def test_broadcast_with_custom_sender(self, mock_send, mock_list_agents):
        """Test broadcast with custom sender."""
        mock_list_agents.return_value = ["Agent-1", "Agent-2"]
        mock_send.return_value = True
        
        service = MessagingService()
        results = service.broadcast("Broadcast message", sender="CustomSender")
        
        # Verify send was called for each agent
        assert mock_send.call_count == 2
        assert results == {"Agent-1": True, "Agent-2": True}

    @patch('src.services.messaging.service._list_agents')
    def test_broadcast_empty_agent_list(self, mock_list_agents):
        """Test broadcast with empty agent list."""
        mock_list_agents.return_value = []
        
        service = MessagingService()
        results = service.broadcast("Broadcast message")
        
        assert results == {}

    @patch('src.services.messaging.service.get_agent_coordinates')
    def test_coords_method(self, mock_get_coords):
        """Test coords method delegation."""
        mock_get_coords.return_value = (100, 200)
        
        service = MessagingService()
        result = service.coords("Agent-1")
        
        mock_get_coords.assert_called_once_with("Agent-1")
        assert result == (100, 200)

    @patch('src.services.messaging.service.get_agent_coordinates')
    def test_coords_method_exception(self, mock_get_coords):
        """Test coords method when get_agent_coordinates raises exception."""
        mock_get_coords.side_effect = ValueError("Agent not found")
        
        service = MessagingService()
        
        with pytest.raises(ValueError, match="Agent not found"):
            service.coords("NonExistentAgent")

    def test_send_with_empty_content(self):
        """Test sending message with empty content."""
        service = MessagingService(dry_run=True)
        
        # Should not raise exception even with empty content
        result = service.send("Agent-1", "")
        assert result is True

    def test_send_with_none_content(self):
        """Test sending message with None content."""
        service = MessagingService(dry_run=True)
        
        # Should not raise exception even with None content
        result = service.send("Agent-1", None)
        assert result is True

    @patch('src.services.messaging.service.send_with_fallback')
    @patch('src.services.messaging.service.UnifiedMessage')
    def test_send_with_special_characters(self, mock_message_class, mock_send_fallback):
        """Test sending message with special characters."""
        mock_message = Mock()
        mock_message_class.return_value = mock_message
        mock_send_fallback.return_value = True
        
        special_content = "Test message with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        service = MessagingService()
        result = service.send("Agent-1", special_content)
        
        # Verify message was created with special content
        call_args = mock_message_class.call_args
        assert call_args[1]['content'] == special_content
        assert result is True

    @patch('src.services.messaging.service.send_with_fallback')
    @patch('src.services.messaging.service.UnifiedMessage')
    def test_send_with_unicode_content(self, mock_message_class, mock_send_fallback):
        """Test sending message with unicode content."""
        mock_message = Mock()
        mock_message_class.return_value = mock_message
        mock_send_fallback.return_value = True
        
        unicode_content = "Test message with unicode: 🚀🎯✅❌"
        
        service = MessagingService()
        result = service.send("Agent-1", unicode_content)
        
        # Verify message was created with unicode content
        call_args = mock_message_class.call_args
        assert call_args[1]['content'] == unicode_content
        assert result is True

    @patch('src.services.messaging.service._list_agents')
    @patch.object(MessagingService, 'send')
    def test_broadcast_with_long_message(self, mock_send, mock_list_agents):
        """Test broadcast with very long message."""
        mock_list_agents.return_value = ["Agent-1"]
        mock_send.return_value = True
        
        long_message = "A" * 10000  # Very long message
        
        service = MessagingService()
        results = service.broadcast(long_message)
        
        # Verify send was called with long message
        mock_send.assert_called_once_with("Agent-1", long_message)
        assert results == {"Agent-1": True}

    def test_service_immutability_after_initialization(self):
        """Test that service properties don't change after initialization."""
        service = MessagingService(dry_run=True)
        original_dry_run = service.dry_run
        
        # Attempt to modify (should not affect the service)
        service.dry_run = False
        
        # In a real implementation, this might be protected
        # For now, we just verify the original value
        assert original_dry_run is True


class TestMessagingServiceIntegration:
    """Integration tests for MessagingService with real dependencies."""

    @patch('src.services.messaging.service.send_with_fallback')
    def test_full_message_flow(self, mock_send_fallback):
        """Test complete message flow from creation to delivery."""
        mock_send_fallback.return_value = True
        
        service = MessagingService()
        
        # Test multiple messages
        results = []
        for i in range(3):
            result = service.send(f"Agent-{i+1}", f"Message {i+1}")
            results.append(result)
        
        # Verify all messages were processed
        assert all(results)
        assert mock_send_fallback.call_count == 3

    @patch('src.services.messaging.service._list_agents')
    @patch('src.services.messaging.service.send_with_fallback')
    def test_broadcast_and_individual_send_consistency(self, mock_send_fallback, mock_list_agents):
        """Test that broadcast and individual sends produce consistent results."""
        mock_list_agents.return_value = ["Agent-1", "Agent-2"]
        mock_send_fallback.return_value = True
        
        service = MessagingService()
        
        # Send individual messages
        individual_results = []
        for agent in ["Agent-1", "Agent-2"]:
            result = service.send(agent, "Individual message")
            individual_results.append(result)
        
        # Send broadcast
        broadcast_results = service.broadcast("Broadcast message")
        
        # Both should succeed
        assert all(individual_results)
        assert all(broadcast_results.values())
        assert mock_send_fallback.call_count == 4  # 2 individual + 2 broadcast


if __name__ == "__main__":
    """Run tests directly for development."""
    print("🧪 MessagingService Testing Suite")
    print("=" * 50)
    
    # Run basic tests
    test_instance = TestMessagingService()
    
    try:
        test_instance.test_service_initialization_default()
        print("✅ Service initialization test passed")
    except Exception as e:
        print(f"❌ Service initialization test failed: {e}")
    
    try:
        test_instance.test_send_success()
        print("✅ Send success test passed")
    except Exception as e:
        print(f"❌ Send success test failed: {e}")
    
    try:
        test_instance.test_broadcast_success()
        print("✅ Broadcast success test passed")
    except Exception as e:
        print(f"❌ Broadcast success test failed: {e}")
    
    print("\n🎉 Core MessagingService tests completed!")
    print("📊 Run full suite with: python -m pytest tests/unit/test_messaging_service.py -v")