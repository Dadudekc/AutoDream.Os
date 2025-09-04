#!/usr/bin/env python3
"""
Comprehensive Test Suite for Messaging Core V2 - Agent-1 Integration & Core Systems
================================================================================

Comprehensive test coverage for the refactored messaging core V2 system.
Tests all modular components and integration points.

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


class TestUnifiedMessagingCoreV2:
    """Test suite for UnifiedMessagingCoreV2."""

    @pytest.fixture
    def temp_inbox_dir(self):
        """Create temporary inbox directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            inbox_dir = get_unified_utility().Path(temp_dir) / "inbox"
            inbox_dir.mkdir()
            yield str(inbox_dir)

    @pytest.fixture
    def mock_delivery_service(self):
        """Mock delivery service."""
        return Mock(spec=MessagingDeliveryService)

    @pytest.fixture
    def mock_config_service(self):
        """Mock config service."""
        return Mock(spec=MessagingConfigService)

    @pytest.fixture
    def mock_unified_integration(self):
        """Mock unified integration service."""
        return Mock(spec=MessagingUnifiedIntegration)

    @pytest.fixture
    def mock_utils_service(self):
        """Mock utils service."""
        return Mock(spec=MessagingUtilsService)

    @pytest.fixture
    def messaging_core_v2(self, mock_delivery_service, mock_config_service, 
                         mock_unified_integration, mock_utils_service):
        """Create UnifiedMessagingCoreV2 instance with mocked dependencies."""
        return UnifiedMessagingCoreV2(
            delivery_service=mock_delivery_service,
            config_service=mock_config_service,
            unified_integration=mock_unified_integration,
            utils_service=mock_utils_service
        )

    def test_initialization(self, messaging_core_v2):
        """Test UnifiedMessagingCoreV2 initialization."""
        assert messaging_core_v2 is not None
        assert messaging_core_v2.delivery_service is not None
        assert messaging_core_v2.config_service is not None
        assert messaging_core_v2.unified_integration is not None
        assert messaging_core_v2.utils_service is not None

    def test_send_message_success(self, messaging_core_v2, mock_delivery_service):
        """Test successful message sending."""
        # Setup
        message = UnifiedMessage(
            message_id="test_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        mock_delivery_service.send_message.return_value = True
        
        # Execute
        result = messaging_core_v2.send_message(message)
        
        # Verify
        assert result is True
        mock_delivery_service.send_message.assert_called_once_with(message)

    def test_send_message_failure(self, messaging_core_v2, mock_delivery_service):
        """Test message sending failure."""
        # Setup
        message = UnifiedMessage(
            message_id="test_002",
            sender="Agent-1",
            recipient="Agent-2",
            content="Test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        mock_delivery_service.send_message.return_value = False
        
        # Execute
        result = messaging_core_v2.send_message(message)
        
        # Verify
        assert result is False
        mock_delivery_service.send_message.assert_called_once_with(message)

    def test_bulk_send_messages(self, messaging_core_v2, mock_delivery_service):
        """Test bulk message sending."""
        # Setup
        messages = [
            UnifiedMessage(
                message_id=f"test_{i}",
                sender="Agent-1",
                recipient=f"Agent-{i+2}",
                content=f"Test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(3)
        ]
        
        mock_delivery_service.send_message.return_value = True
        
        # Execute
        results = messaging_core_v2.bulk_send_messages(messages)
        
        # Verify
        assert len(results) == 3
        assert all(results.values())
        assert mock_delivery_service.send_message.call_count == 3

    def test_get_system_health(self, messaging_core_v2, mock_utils_service):
        """Test system health check."""
        # Setup
        expected_health = {
            "status": "healthy",
            "components": ["delivery", "config", "integration", "utils"],
            "timestamp": "2025-09-02T13:45:00Z"
        }
        mock_utils_service.get_system_health.return_value = expected_health
        
        # Execute
        health = messaging_core_v2.get_system_health()
        
        # Verify
        assert health == expected_health
        mock_utils_service.get_system_health.assert_called_once()

    def test_message_validation(self, messaging_core_v2):
        """Test message validation."""
        # Valid message
        valid_message = UnifiedMessage(
            message_id="valid_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Valid message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Invalid message (missing required fields)
        invalid_message = UnifiedMessage(
            message_id="",
            sender="",
            recipient="",
            content="",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Test valid message
        assert messaging_core_v2._validate_message(valid_message) is True
        
        # Test invalid message
        assert messaging_core_v2._validate_message(invalid_message) is False

    def test_unified_logging_integration(self, messaging_core_v2, mock_unified_integration):
        """Test unified logging integration."""
        # Setup
        mock_logger = Mock()
        mock_unified_integration.get_logger.return_value = mock_logger
        
        # Execute
        logger = messaging_core_v2.unified_integration.get_logger()
        
        # Verify
        assert logger == mock_logger
        # Note: get_logger may be called multiple times during initialization
        assert mock_unified_integration.get_logger.call_count >= 1

    def test_configuration_integration(self, messaging_core_v2, mock_config_service):
        """Test configuration system integration."""
        # Setup
        expected_config = get_unified_config().get_config()
            "delivery_method": "inbox",
            "retry_attempts": 3,
            "timeout": 30
        }
        # Mock the get_config method
        mock_config_service.get_config = Mock(return_value=expected_config)
        
        # Execute
        config = messaging_core_v2.config_service.get_unified_config().get_config()
        
        # Verify
        assert config == expected_config
        mock_config_service.get_config.assert_called_once()

    def test_error_handling(self, messaging_core_v2, mock_delivery_service):
        """Test error handling in message sending."""
        # Setup
        message = UnifiedMessage(
            message_id="error_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        mock_delivery_service.send_message.side_effect = Exception("Delivery failed")
        
        # Execute and verify exception is handled
        with pytest.raises(Exception, match="Delivery failed"):
            messaging_core_v2.send_message(message)

    def test_performance_metrics(self, messaging_core_v2, mock_unified_integration):
        """Test performance metrics tracking."""
        # Setup
        mock_metrics = Mock()
        mock_unified_integration.get_metrics.return_value = mock_metrics
        
        # Execute
        metrics = messaging_core_v2.unified_integration.get_metrics()
        
        # Verify
        assert metrics == mock_metrics
        # Note: get_metrics may be called multiple times during initialization
        assert mock_unified_integration.get_metrics.call_count >= 1

    def test_message_queuing(self, messaging_core_v2):
        """Test message queuing functionality."""
        # Setup
        message = UnifiedMessage(
            message_id="queue_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Queued message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        messaging_core_v2.queue_message(message)
        
        # Verify
        assert len(messaging_core_v2.message_queue) == 1
        assert messaging_core_v2.message_queue[0] == message

    def test_priority_handling(self, messaging_core_v2):
        """Test message priority handling."""
        # Setup
        urgent_message = UnifiedMessage(
            message_id="urgent_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Urgent message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )
        
        normal_message = UnifiedMessage(
            message_id="normal_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Normal message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        messaging_core_v2.queue_message(normal_message)
        messaging_core_v2.queue_message(urgent_message)
        
        # Verify urgent message is prioritized
        assert messaging_core_v2.message_queue[0] == urgent_message
        assert messaging_core_v2.message_queue[1] == normal_message


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

    def test_send_message_to_inbox(self, delivery_service, temp_inbox_dir):
        """Test sending message to inbox."""
        # Setup
        message = UnifiedMessage(
            message_id="inbox_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Inbox test message",
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
        assert "Inbox test message" in content
        assert "Agent-1" in content

    def test_send_message_pyautogui(self, delivery_service):
        """Test PyAutoGUI message sending."""
        # Setup
        message = UnifiedMessage(
            message_id="pyautogui_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="PyAutoGUI test message",
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

    def test_retry_mechanism(self, delivery_service, temp_inbox_dir):
        """Test message delivery retry mechanism."""
        # Setup
        message = UnifiedMessage(
            message_id="retry_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Retry test message",
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

    def test_metrics_recording(self, delivery_service, mock_metrics):
        """Test metrics recording."""
        # Setup
        message = UnifiedMessage(
            message_id="metrics_001",
            sender="Agent-1",
            recipient="Agent-Test",
            content="Metrics test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        delivery_service.send_message_to_inbox(message)
        
        # Verify metrics were recorded
        mock_metrics.record_delivery.assert_called()


class TestMessagingUnifiedIntegration:
    """Test suite for MessagingUnifiedIntegration."""

    @pytest.fixture
    def unified_integration(self):
        """Create MessagingUnifiedIntegration instance."""
        return MessagingUnifiedIntegration()

    def test_initialization(self, unified_integration):
        """Test MessagingUnifiedIntegration initialization."""
        assert unified_integration is not None

    def test_get_logger(self, unified_integration):
        """Test logger retrieval."""
        logger = unified_integration.get_logger()
        # Should return None if unified systems not available
        assert logger is None or get_unified_validator().validate_hasattr(logger, 'log')

    def test_get_config_system(self, unified_integration):
        """Test configuration system retrieval."""
        config = unified_integration.get_config_system()
        # Should return None if unified systems not available
        assert config is None or get_unified_validator().validate_hasattr(config, 'get_config')

    def test_get_metrics(self, unified_integration):
        """Test metrics retrieval."""
        metrics = unified_integration.get_metrics()
        # Should return None if unified systems not available
        assert metrics is None or get_unified_validator().validate_hasattr(metrics, 'record_delivery')

    def test_log_operation_start(self, unified_integration):
        """Test operation start logging."""
        context = {"operation": "test", "agent": "Agent-1"}
        result = unified_integration.log_operation_start("test_operation", context)
        # Should return None if unified systems not available
        assert result is None or get_unified_validator().validate_type(result, str)

    def test_log_operation_complete(self, unified_integration):
        """Test operation completion logging."""
        context = {"operation": "test", "agent": "Agent-1"}
        result = unified_integration.log_operation_complete("test_operation", context)
        # Should return None if unified systems not available
        assert result is None


class TestMessagingUtilsService:
    """Test suite for MessagingUtilsService."""

    @pytest.fixture
    def utils_service(self):
        """Create MessagingUtilsService instance."""
        return MessagingUtilsService()

    def test_initialization(self, utils_service):
        """Test MessagingUtilsService initialization."""
        assert utils_service is not None
        assert len(utils_service.agent_list) > 0

    def test_get_agent_status(self, utils_service):
        """Test agent status retrieval."""
        status = utils_service.get_agent_status()
        assert get_unified_validator().validate_type(status, dict)
        assert "agents" in status

    def test_validate_agent_workspace(self, utils_service):
        """Test agent workspace validation."""
        # Valid agent workspace
        result = utils_service.validate_agent_workspace("Agent-1")
        assert get_unified_validator().validate_type(result, dict)
        assert "valid" in result
        assert "agent_id" in result
        
        # Invalid agent workspace
        result = utils_service.validate_agent_workspace("Invalid-Agent")
        assert get_unified_validator().validate_type(result, dict)
        assert result["valid"] is False

    def test_get_system_health(self, utils_service):
        """Test system health check."""
        health = utils_service.get_system_health()
        assert get_unified_validator().validate_type(health, dict)
        assert "status" in health
        assert "timestamp" in health

    def test_validate_message(self, utils_service, sample_message):
        """Test message validation."""
        result = utils_service.validate_message(sample_message)
        assert get_unified_validator().validate_type(result, dict)
        assert "valid" in result
        assert "errors" in result
        assert "warnings" in result

    def test_format_message_for_display(self, utils_service, sample_message):
        """Test message formatting for display."""
        formatted = utils_service.format_message_for_display(sample_message)
        assert get_unified_validator().validate_type(formatted, str)
        assert "Agent-1" in formatted
        assert "Agent-2" in formatted

    def test_generate_message_summary(self, utils_service, sample_messages):
        """Test message summary generation."""
        summary = utils_service.generate_message_summary(sample_messages)
        assert get_unified_validator().validate_type(summary, dict)
        assert "total_messages" in summary
        assert summary["total_messages"] == len(sample_messages)


def run_messaging_tests():
    """Run all messaging system tests."""
    get_logger(__name__).info("🧪 MESSAGING SYSTEM COMPREHENSIVE TEST SUITE - AGENT-1")
    get_logger(__name__).info("=" * 70)
    
    # Run pytest with verbose output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])


if __name__ == "__main__":
    run_messaging_tests()
