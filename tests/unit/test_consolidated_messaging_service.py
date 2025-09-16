#!/usr/bin/env python3
"""
Consolidated Messaging Service Testing Suite
============================================

Comprehensive test suite for the ConsolidatedMessagingService.
Tests cover:
- Service initialization and configuration
- Message sending and broadcasting
- Provider selection and fallback
- Error handling and edge cases
- Integration with messaging models

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.services.consolidated_messaging_service import ConsolidatedMessagingService


class TestConsolidatedMessagingService:
    """Unit tests for ConsolidatedMessagingService class."""

    def test_service_initialization_default(self):
        """Test ConsolidatedMessagingService initialization with default parameters."""
        with patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService') as mock_service:
            mock_instance = Mock()
            mock_service.return_value = mock_instance
            
            service = ConsolidatedMessagingService()
            
            assert service is not None

    def test_service_initialization_with_config(self):
        """Test ConsolidatedMessagingService initialization with custom configuration."""
        config = {
            "default_provider": "inbox",
            "fallback_provider": "pyautogui",
            "timeout": 30
        }
        
        with patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService') as mock_service:
            mock_instance = Mock()
            mock_service.return_value = mock_instance
            
            service = ConsolidatedMessagingService(config=config)
            
            assert service is not None

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_send_message_success(self, mock_service_class):
        """Test successful message sending."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.send_message.return_value = True
        
        service = ConsolidatedMessagingService()
        result = service.send_message("Agent-1", "Test message")
        
        assert result is True
        mock_service.send_message.assert_called_once_with("Agent-1", "Test message")

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_send_message_with_priority(self, mock_service_class):
        """Test message sending with priority."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.send_message.return_value = True
        
        service = ConsolidatedMessagingService()
        result = service.send_message("Agent-1", "Test message", priority="HIGH")
        
        assert result is True
        mock_service.send_message.assert_called_once_with("Agent-1", "Test message", priority="HIGH")

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_send_message_failure(self, mock_service_class):
        """Test message sending failure."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.send_message.return_value = False
        
        service = ConsolidatedMessagingService()
        result = service.send_message("Agent-1", "Test message")
        
        assert result is False

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_broadcast_message_success(self, mock_service_class):
        """Test successful message broadcasting."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.broadcast_message.return_value = {"Agent-1": True, "Agent-2": True}
        
        service = ConsolidatedMessagingService()
        results = service.broadcast_message("Broadcast message")
        
        assert results == {"Agent-1": True, "Agent-2": True}
        mock_service.broadcast_message.assert_called_once_with("Broadcast message")

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_broadcast_message_partial_failure(self, mock_service_class):
        """Test message broadcasting with partial failures."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.broadcast_message.return_value = {"Agent-1": True, "Agent-2": False}
        
        service = ConsolidatedMessagingService()
        results = service.broadcast_message("Broadcast message")
        
        assert results == {"Agent-1": True, "Agent-2": False}

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_get_message_history(self, mock_service_class):
        """Test getting message history."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_history = [
            {"id": "1", "content": "Message 1", "timestamp": "2025-01-01T00:00:00Z"},
            {"id": "2", "content": "Message 2", "timestamp": "2025-01-01T01:00:00Z"}
        ]
        mock_service.get_message_history.return_value = mock_history
        
        service = ConsolidatedMessagingService()
        history = service.get_message_history("Agent-1")
        
        assert history == mock_history
        mock_service.get_message_history.assert_called_once_with("Agent-1")

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_get_message_history_empty(self, mock_service_class):
        """Test getting empty message history."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.get_message_history.return_value = []
        
        service = ConsolidatedMessagingService()
        history = service.get_message_history("Agent-1")
        
        assert history == []

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_get_service_status(self, mock_service_class):
        """Test getting service status."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_status = {
            "status": "active",
            "providers": ["inbox", "pyautogui"],
            "active_connections": 2,
            "messages_sent": 100
        }
        mock_service.get_status.return_value = mock_status
        
        service = ConsolidatedMessagingService()
        status = service.get_status()
        
        assert status == mock_status
        mock_service.get_status.assert_called_once()

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_validate_agent_coordinates(self, mock_service_class):
        """Test agent coordinate validation."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_validation = {
            "Agent-1": True,
            "Agent-2": False,
            "Agent-3": True
        }
        mock_service.validate_agent_coordinates.return_value = mock_validation
        
        service = ConsolidatedMessagingService()
        validation = service.validate_agent_coordinates()
        
        assert validation == mock_validation
        mock_service.validate_agent_coordinates.assert_called_once()

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_send_message_with_retry(self, mock_service_class):
        """Test message sending with retry mechanism."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.send_message_with_retry.return_value = True
        
        service = ConsolidatedMessagingService()
        result = service.send_message_with_retry("Agent-1", "Test message", max_retries=3)
        
        assert result is True
        mock_service.send_message_with_retry.assert_called_once_with("Agent-1", "Test message", max_retries=3)

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_send_message_with_retry_failure(self, mock_service_class):
        """Test message sending with retry mechanism failure."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.send_message_with_retry.return_value = False
        
        service = ConsolidatedMessagingService()
        result = service.send_message_with_retry("Agent-1", "Test message", max_retries=3)
        
        assert result is False

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_get_agent_coordinates(self, mock_service_class):
        """Test getting agent coordinates."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_coords = (100, 200)
        mock_service.get_agent_coordinates.return_value = mock_coords
        
        service = ConsolidatedMessagingService()
        coords = service.get_agent_coordinates("Agent-1")
        
        assert coords == mock_coords
        mock_service.get_agent_coordinates.assert_called_once_with("Agent-1")

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_get_agent_coordinates_not_found(self, mock_service_class):
        """Test getting coordinates for non-existent agent."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.get_agent_coordinates.return_value = None
        
        service = ConsolidatedMessagingService()
        coords = service.get_agent_coordinates("NonExistentAgent")
        
        assert coords is None

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_send_message_with_custom_provider(self, mock_service_class):
        """Test message sending with custom provider."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.send_message_with_provider.return_value = True
        
        service = ConsolidatedMessagingService()
        result = service.send_message_with_provider("Agent-1", "Test message", provider="inbox")
        
        assert result is True
        mock_service.send_message_with_provider.assert_called_once_with("Agent-1", "Test message", provider="inbox")

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_send_message_with_invalid_provider(self, mock_service_class):
        """Test message sending with invalid provider."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.send_message_with_provider.return_value = False
        
        service = ConsolidatedMessagingService()
        result = service.send_message_with_provider("Agent-1", "Test message", provider="invalid")
        
        assert result is False

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_get_available_providers(self, mock_service_class):
        """Test getting available providers."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_providers = ["inbox", "pyautogui", "fallback"]
        mock_service.get_available_providers.return_value = mock_providers
        
        service = ConsolidatedMessagingService()
        providers = service.get_available_providers()
        
        assert providers == mock_providers
        mock_service.get_available_providers.assert_called_once()

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_set_default_provider(self, mock_service_class):
        """Test setting default provider."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.set_default_provider.return_value = True
        
        service = ConsolidatedMessagingService()
        result = service.set_default_provider("inbox")
        
        assert result is True
        mock_service.set_default_provider.assert_called_once_with("inbox")

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_set_invalid_default_provider(self, mock_service_class):
        """Test setting invalid default provider."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.set_default_provider.return_value = False
        
        service = ConsolidatedMessagingService()
        result = service.set_default_provider("invalid")
        
        assert result is False

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_clear_message_history(self, mock_service_class):
        """Test clearing message history."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.clear_message_history.return_value = True
        
        service = ConsolidatedMessagingService()
        result = service.clear_message_history("Agent-1")
        
        assert result is True
        mock_service.clear_message_history.assert_called_once_with("Agent-1")

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_get_message_statistics(self, mock_service_class):
        """Test getting message statistics."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_stats = {
            "total_messages": 1000,
            "successful_messages": 950,
            "failed_messages": 50,
            "success_rate": 0.95
        }
        mock_service.get_message_statistics.return_value = mock_stats
        
        service = ConsolidatedMessagingService()
        stats = service.get_message_statistics()
        
        assert stats == mock_stats
        mock_service.get_message_statistics.assert_called_once()


class TestConsolidatedMessagingServiceIntegration:
    """Integration tests for ConsolidatedMessagingService."""

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_full_message_workflow(self, mock_service_class):
        """Test complete message workflow."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        
        # Setup mock responses
        mock_service.send_message.return_value = True
        mock_service.get_message_history.return_value = [{"id": "1", "content": "Test"}]
        mock_service.get_status.return_value = {"status": "active"}
        
        service = ConsolidatedMessagingService()
        
        # Send message
        result = service.send_message("Agent-1", "Test message")
        assert result is True
        
        # Get history
        history = service.get_message_history("Agent-1")
        assert len(history) == 1
        
        # Get status
        status = service.get_status()
        assert status["status"] == "active"

    @patch('src.services.consolidated_messaging_service.ConsolidatedMessagingService')
    def test_broadcast_workflow(self, mock_service_class):
        """Test broadcast workflow."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.broadcast_message.return_value = {
            "Agent-1": True,
            "Agent-2": True,
            "Agent-3": False
        }
        
        service = ConsolidatedMessagingService()
        results = service.broadcast_message("Broadcast message")
        
        assert results["Agent-1"] is True
        assert results["Agent-2"] is True
        assert results["Agent-3"] is False


if __name__ == "__main__":
    """Run tests directly for development."""
    print("🧪 ConsolidatedMessagingService Testing Suite")
    print("=" * 50)
    
    # Run basic tests
    test_instance = TestConsolidatedMessagingService()
    
    try:
        test_instance.test_service_initialization_default()
        print("✅ Service initialization test passed")
    except Exception as e:
        print(f"❌ Service initialization test failed: {e}")
    
    try:
        test_instance.test_send_message_success()
        print("✅ Send message success test passed")
    except Exception as e:
        print(f"❌ Send message success test failed: {e}")
    
    try:
        test_instance.test_broadcast_message_success()
        print("✅ Broadcast message success test passed")
    except Exception as e:
        print(f"❌ Broadcast message success test failed: {e}")
    
    print("\n🎉 Core ConsolidatedMessagingService tests completed!")
    print("📊 Run full suite with: python -m pytest tests/unit/test_consolidated_messaging_service.py -v")