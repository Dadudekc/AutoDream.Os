#!/usr/bin/env python3
"""
Comprehensive Test Suite for Messaging Delivery Service - Agent-1 Integration & Core Systems
=========================================================================================

Comprehensive test coverage for the messaging delivery service components.
Tests delivery methods, retry mechanisms, and error handling.

V2 Compliance: Comprehensive test coverage with unified logging integration.

Author: Agent-1 - Integration & Core Systems Specialist
License: MIT
"""

import pytest

# Import messaging components
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType
)


class TestMessagingDeliveryService:
    """Test suite for MessagingDeliveryService."""

    @pytest.fixture
    def temp_inbox_dir(self):
        """Create temporary inbox directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            inbox_dir = get_unified_utility().Path(temp_dir) / "inbox"
            inbox_dir.mkdir()
            yield str(inbox_dir)

    @pytest.fixture
    def mock_metrics(self):
        """Mock metrics service."""
        return Mock()

    @pytest.fixture
    def delivery_service(self, temp_inbox_dir, mock_metrics):
        """Create MessagingDeliveryService instance."""
        inbox_paths = {"Agent-Test": temp_inbox_dir}
        # Create MessagingDelivery with proper parameters
        messaging_delivery = MessagingDelivery(inbox_paths, mock_metrics)
        
        return MessagingDeliveryService(messaging_delivery=messaging_delivery)

    def test_initialization(self, delivery_service):
        """Test MessagingDeliveryService initialization."""
        assert delivery_service is not None
        assert delivery_service.messaging_delivery is not None
        assert delivery_service.pyautogui_delivery is not None
        assert delivery_service.bulk_service is not None

    def test_send_message_to_inbox_success(self, delivery_service, temp_inbox_dir):
        """Test successful message sending to inbox."""
        # Setup
        message = UnifiedMessage(
            message_id="inbox_success_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Successful inbox test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        result = delivery_service.send_message_to_inbox(message)
        
        # Verify
        assert result is True
        
        # Check if message file was created
        inbox_path = get_unified_utility().Path(temp_inbox_dir)
        message_files = list(inbox_path.glob("*.md"))
        assert len(message_files) == 1
        
        # Verify message content
        with open(message_files[0], 'r') as f:
            content = f.read()
        assert "Successful inbox test message" in content
        assert "Agent-1" in content
        assert "Agent-Test" in content

    def test_send_message_to_inbox_invalid_recipient(self, delivery_service):
        """Test message sending with invalid recipient."""
        # Setup
        message = UnifiedMessage(
            message_id="invalid_recipient_001",
            sender="Agent-1",
            recipient="Invalid-Agent",
            content="Test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        result = delivery_service.send_message_to_inbox(message)
        
        # Verify
        assert result is False

    def test_send_message_to_inbox_directory_creation(self, delivery_service, temp_inbox_dir):
        """Test inbox directory creation."""
        # Setup - remove inbox directory
        inbox_path = get_unified_utility().Path(temp_inbox_dir)
        inbox_path.rmdir()
        
        message = UnifiedMessage(
            message_id="dir_creation_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Directory creation test",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        result = delivery_service.send_message_to_inbox(message)
        
        # Verify
        assert result is True
        assert inbox_path.exists()
        assert inbox_path.is_dir()

    def test_send_message_pyautogui_success(self, delivery_service):
        """Test successful PyAutoGUI message sending."""
        # Setup
        message = UnifiedMessage(
            message_id="pyautogui_success_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="PyAutoGUI success test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Mock PyAutoGUI functions
        with patch('src.services.messaging_delivery_service.pyautogui') as mock_pyautogui:
            mock_pyautogui.click.return_value = None
            mock_pyautogui.typewrite.return_value = None
            mock_pyautogui.press.return_value = None
            
            # Execute
            result = delivery_service.send_message_pyautogui(message)
            
            # Verify
            assert result is True
            mock_pyautogui.click.assert_called()
            mock_pyautogui.typewrite.assert_called()

    def test_send_message_pyautogui_failure(self, delivery_service):
        """Test PyAutoGUI message sending failure."""
        # Setup
        message = UnifiedMessage(
            message_id="pyautogui_failure_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="PyAutoGUI failure test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Mock PyAutoGUI functions to raise exception
        with patch('src.services.messaging_delivery_service.pyautogui') as mock_pyautogui:
            mock_pyautogui.click.side_effect = Exception("PyAutoGUI failed")
            
            # Execute
            result = delivery_service.send_message_pyautogui(message)
            
            # Verify
            assert result is False

    def test_retry_mechanism_success(self, delivery_service, temp_inbox_dir):
        """Test message delivery retry mechanism with eventual success."""
        # Setup
        message = UnifiedMessage(
            message_id="retry_success_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Retry success test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Mock first attempt failure, second success
        with patch.object(delivery_service, '_write_message_file') as mock_write:
            mock_write.side_effect = [Exception("Write failed"), None]
            
            # Execute
            result = delivery_service.send_message_to_inbox(message, max_retries=2)
            
            # Verify
            assert result is True
            assert mock_write.call_count == 2

    def test_retry_mechanism_failure(self, delivery_service, temp_inbox_dir):
        """Test message delivery retry mechanism with eventual failure."""
        # Setup
        message = UnifiedMessage(
            message_id="retry_failure_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Retry failure test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Mock all attempts failure
        with patch.object(delivery_service, '_write_message_file') as mock_write:
            mock_write.side_effect = Exception("Write failed")
            
            # Execute
            result = delivery_service.send_message_to_inbox(message, max_retries=3)
            
            # Verify
            assert result is False
            assert mock_write.call_count == 3

    def test_metrics_recording_success(self, delivery_service, mock_metrics, temp_inbox_dir):
        """Test metrics recording for successful delivery."""
        # Setup
        message = UnifiedMessage(
            message_id="metrics_success_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Metrics success test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        delivery_service.send_message_to_inbox(message)
        
        # Verify metrics were recorded
        mock_metrics.record_delivery.assert_called()

    def test_metrics_recording_failure(self, delivery_service, mock_metrics):
        """Test metrics recording for failed delivery."""
        # Setup
        message = UnifiedMessage(
            message_id="metrics_failure_001",
            sender="Agent-1",
            recipient="Invalid-Agent",
            content="Metrics failure test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        delivery_service.send_message_to_inbox(message)
        
        # Verify error metrics were recorded
        mock_metrics.record_error.assert_called()

    def test_message_file_formatting(self, delivery_service, temp_inbox_dir):
        """Test message file formatting."""
        # Setup
        message = UnifiedMessage(
            message_id="format_test_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Format test message with special characters: @#$%^&*()",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN]
        )
        
        # Execute
        delivery_service.send_message_to_inbox(message)
        
        # Verify message file content
        inbox_path = get_unified_utility().Path(temp_inbox_dir)
        message_files = list(inbox_path.glob("*.md"))
        assert len(message_files) == 1
        
        with open(message_files[0], 'r') as f:
            content = f.read()
        
        # Check for proper formatting
        assert "#" in content  # Markdown header
        assert "Agent-1" in content  # Sender
        assert "Agent-Test" in content  # Recipient
        assert "URGENT" in content  # Priority
        assert "CAPTAIN" in content  # Tag

    def test_concurrent_message_delivery(self, delivery_service, temp_inbox_dir):
        """Test concurrent message delivery."""
        
        # Setup
        messages = [
            UnifiedMessage(
                message_id=f"concurrent_{i}",
                sender="Agent-1",
                recipient="Agent-Test",
                content=f"Concurrent test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(5)
        ]
        
        results = []
        
        def send_message(msg):
            result = delivery_service.send_message_to_inbox(msg)
            results.append(result)
        
        # Execute concurrently
        threads = []
        for message in messages:
            thread = threading.Thread(target=send_message, args=(message,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify
        assert len(results) == 5
        assert all(results)  # All should succeed
        
        # Verify all message files were created
        inbox_path = get_unified_utility().Path(temp_inbox_dir)
        message_files = list(inbox_path.glob("*.md"))
        assert len(message_files) == 5

    def test_message_priority_handling(self, delivery_service, temp_inbox_dir):
        """Test message priority handling."""
        # Setup
        urgent_message = UnifiedMessage(
            message_id="priority_urgent_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Urgent priority message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )
        
        normal_message = UnifiedMessage(
            message_id="priority_normal_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Normal priority message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        delivery_service.send_message_to_inbox(normal_message)
        delivery_service.send_message_to_inbox(urgent_message)
        
        # Verify both messages were delivered
        inbox_path = get_unified_utility().Path(temp_inbox_dir)
        message_files = list(inbox_path.glob("*.md"))
        assert len(message_files) == 2
        
        # Verify priority is reflected in file content
        urgent_files = [f for f in message_files if "URGENT" in f.read_text()]
        assert len(urgent_files) == 1

    def test_message_type_handling(self, delivery_service, temp_inbox_dir):
        """Test different message type handling."""
        # Setup
        text_message = UnifiedMessage(
            message_id="type_text_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Text message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        broadcast_message = UnifiedMessage(
            message_id="type_broadcast_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Broadcast message",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        delivery_service.send_message_to_inbox(text_message)
        delivery_service.send_message_to_inbox(broadcast_message)
        
        # Verify both messages were delivered
        inbox_path = get_unified_utility().Path(temp_inbox_dir)
        message_files = list(inbox_path.glob("*.md"))
        assert len(message_files) == 2

    def test_error_handling_invalid_message(self, delivery_service):
        """Test error handling with invalid message."""
        # Setup - create invalid message
        invalid_message = None
        
        # Execute and verify exception handling
        with pytest.raises((TypeError, AttributeError)):
            delivery_service.send_message_to_inbox(invalid_message)

    def test_error_handling_permission_denied(self, delivery_service, temp_inbox_dir):
        """Test error handling with permission denied."""
        # Setup
        message = UnifiedMessage(
            message_id="permission_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Permission test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Make inbox directory read-only
        inbox_path = get_unified_utility().Path(temp_inbox_dir)
        inbox_path.chmod(0o444)
        
        try:
            # Execute
            result = delivery_service.send_message_to_inbox(message)
            
            # Verify
            assert result is False
        finally:
            # Restore permissions
            inbox_path.chmod(0o755)

    def test_delivery_statistics(self, delivery_service):
        """Test delivery statistics tracking."""
        # Verify delivery stats exist
        assert get_unified_validator().validate_hasattr(delivery_service, 'delivery_stats')
        assert get_unified_validator().validate_type(delivery_service.delivery_stats, dict)
        assert 'inbox_deliveries' in delivery_service.delivery_stats
        assert 'agent_deliveries' in delivery_service.delivery_stats
        assert 'bulk_deliveries' in delivery_service.delivery_stats

    def test_service_components(self, delivery_service):
        """Test service component initialization."""
        # Verify all service components are initialized
        assert delivery_service.messaging_delivery is not None
        assert delivery_service.pyautogui_delivery is not None
        assert delivery_service.bulk_service is not None

    def test_delivery_methods(self, delivery_service):
        """Test delivery method availability."""
        # Verify delivery methods exist
        assert get_unified_validator().validate_hasattr(delivery_service, 'send_message_to_inbox')
        assert get_unified_validator().validate_hasattr(delivery_service, 'send_message_pyautogui')
        assert get_unified_validator().validate_hasattr(delivery_service, 'send_bulk_messages')

    def test_delivery_statistics_update(self, delivery_service):
        """Test delivery statistics update functionality."""
        # Verify initial stats
        initial_stats = delivery_service.delivery_stats.copy()
        
        # Verify stats structure
        assert get_unified_validator().validate_type(initial_stats, dict)
        assert 'inbox_deliveries' in initial_stats
        assert 'agent_deliveries' in initial_stats
        assert 'bulk_deliveries' in initial_stats

    def test_delivery_service_interface(self, delivery_service):
        """Test delivery service interface compliance."""
        # Verify service implements expected interface
        required_methods = [
            'send_message_to_inbox',
            'send_message_pyautogui', 
            'send_bulk_messages',
            'get_delivery_stats'
        ]
        
        for method in required_methods:
            assert get_unified_validator().validate_hasattr(delivery_service, method), f"Missing method: {method}"


def run_delivery_service_tests():
    """Run all messaging delivery service tests."""
    get_logger(__name__).info("🧪 MESSAGING DELIVERY SERVICE COMPREHENSIVE TEST SUITE - AGENT-1")
    get_logger(__name__).info("=" * 70)
    
    # Run pytest with verbose output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])


if __name__ == "__main__":
    run_delivery_service_tests()
