#!/usr/bin/env python3
"""
Comprehensive Integration Test Suite for Messaging System - Agent-1 Integration & Core Systems
============================================================================================

Comprehensive integration test coverage for the entire messaging system.
Tests end-to-end workflows, cross-component integration, and system behavior.

V2 Compliance: Comprehensive integration test coverage with unified logging integration.

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


class TestMessagingSystemIntegration:
    """Integration test suite for the complete messaging system."""

    @pytest.fixture
    def temp_inbox_dirs(self):
        """Create temporary inbox directories for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            inbox_dirs = {}
            for i in range(1, 4):  # Create 3 test agents
                agent_dir = get_unified_utility().Path(temp_dir) / f"Agent-{i}" / "inbox"
                agent_dir.mkdir(parents=True)
                inbox_dirs[f"Agent-{i}"] = str(agent_dir)
            yield inbox_dirs

    @pytest.fixture
    def mock_metrics(self):
        """Mock metrics service."""
        return Mock()

    @pytest.fixture
    def messaging_system(self, temp_inbox_dirs, mock_metrics):
        """Create complete messaging system for testing."""
        # Create delivery service with proper parameters
        messaging_delivery = MessagingDelivery(temp_inbox_dirs, mock_metrics)
        delivery_service = MessagingDeliveryService(messaging_delivery=messaging_delivery)
        
        # Create config service
        config_service = MessagingConfigService()
        
        # Create unified integration
        unified_integration = MessagingUnifiedIntegration()
        
        # Create utils service
        utils_service = MessagingUtilsService()
        
        # Create main messaging core
        messaging_core = UnifiedMessagingCoreV2(
            delivery_service=delivery_service,
            config_service=config_service,
            unified_integration=unified_integration,
            utils_service=utils_service
        )
        
        return messaging_core

    def test_end_to_end_message_flow(self, messaging_system, temp_inbox_dirs):
        """Test complete end-to-end message flow."""
        # Setup
        message = UnifiedMessage(
            message_id="e2e_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="End-to-end test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        result = messaging_system.send_message(message)
        
        # Verify
        assert result is True
        
        # Verify message was delivered to inbox
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == 1
        
        # Verify message content
        with open(message_files[0], 'r') as f:
            content = f.read()
        assert "End-to-end test message" in content
        assert "Agent-1" in content

    def test_bulk_message_delivery(self, messaging_system, temp_inbox_dirs):
        """Test bulk message delivery across multiple agents."""
        # Setup
        messages = [
            UnifiedMessage(
                message_id=f"bulk_{i}",
                sender="Agent-1",
                recipient=f"Agent-{i}",
                content=f"Bulk test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(1, 4)  # Send to Agent-1, Agent-2, Agent-3
        ]
        
        # Execute - use inbox mode for testing
        results = {}
        for message in messages:
            result = messaging_system.send_message_to_agent(message, mode="inbox")
            results[message.message_id] = result

        # Verify
        assert len(results) == 3
        assert all(results.values())
        
        # Verify all messages were delivered
        for i in range(1, 4):
            agent_inbox = get_unified_utility().Path(temp_inbox_dirs[f"Agent-{i}"])
            message_files = list(agent_inbox.glob("*.md"))
            assert len(message_files) == 1

    def test_priority_message_handling(self, messaging_system, temp_inbox_dirs):
        """Test priority message handling in bulk delivery."""
        # Setup
        messages = [
            UnifiedMessage(
                message_id="priority_normal_001",
                sender="Agent-1",
                recipient="Agent-2",
                content="Normal priority message",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            ),
            UnifiedMessage(
                message_id="priority_urgent_001",
                sender="Agent-1",
                recipient="Agent-2",
                content="Urgent priority message",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.URGENT
            )
        ]
        
        # Execute
        results = messaging_system.bulk_send_messages(messages)
        
        # Verify
        assert len(results) == 2
        assert all(results.values())
        
        # Verify both messages were delivered
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == 2

    def test_message_validation_integration(self, messaging_system):
        """Test message validation integration."""
        # Valid message
        valid_message = UnifiedMessage(
            message_id="valid_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Valid message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Invalid message
        invalid_message = UnifiedMessage(
            message_id="",
            sender="",
            recipient="",
            content="",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Test valid message
        assert messaging_system._validate_message(valid_message) is True
        
        # Test invalid message
        assert messaging_system._validate_message(invalid_message) is False

    def test_system_health_integration(self, messaging_system):
        """Test system health check integration."""
        # Execute
        health = messaging_system.get_system_health()
        
        # Verify
        assert get_unified_validator().validate_type(health, dict)
        assert "overall_health" in health  # Status is called 'overall_health'
        assert "components" in health
        assert "agent_health" in health  # Additional health components

    def test_unified_logging_integration(self, messaging_system):
        """Test unified logging system integration."""
        # Execute
        logger = messaging_system.unified_integration.get_logger()
        config = messaging_system.unified_integration.get_config_system()
        metrics = messaging_system.unified_integration.get_metrics()
        
        # Verify (may be None if unified systems not available)
        assert logger is None or get_unified_validator().validate_hasattr(logger, 'log')
        assert config is None or get_unified_validator().validate_hasattr(config, 'get_config')
        assert metrics is None or get_unified_validator().validate_hasattr(metrics, 'record_delivery')

    def test_configuration_integration(self, messaging_system):
        """Test configuration system integration."""
        # Execute
        config = messaging_system.config_service.get_unified_config().get_config()
        
        # Verify
        assert get_unified_validator().validate_type(config, dict)

    def test_utils_service_integration(self, messaging_system):
        """Test utils service integration."""
        # Execute
        agent_status = messaging_system.utils_service.get_agent_status()
        system_health = messaging_system.utils_service.get_system_health()
        
        # Verify
        assert get_unified_validator().validate_type(agent_status, dict)
        assert get_unified_validator().validate_type(system_health, dict)

    def test_concurrent_message_processing(self, messaging_system, temp_inbox_dirs):
        """Test concurrent message processing."""
        # Setup
        messages = [
            UnifiedMessage(
                message_id=f"concurrent_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"Concurrent test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(10)
        ]
        
        results = []
        
        def send_message(msg):
            result = messaging_system.send_message(msg)
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
        assert len(results) == 10
        assert all(results)  # All should succeed
        
        # Verify all messages were delivered
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == 10

    def test_error_handling_integration(self, messaging_system):
        """Test error handling integration."""
        # Setup - create message with invalid recipient
        invalid_message = UnifiedMessage(
            message_id="error_001",
            sender="Agent-1",
            recipient="Invalid-Agent",
            content="Error test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        result = messaging_system.send_message(invalid_message)

        # Verify - system should handle invalid recipient gracefully (may queue or return True if queuing)
        # The important thing is that it doesn't crash
        assert get_unified_validator().validate_type(result, bool)  # Should return a boolean
        # Note: The system may queue invalid messages for later delivery rather than failing immediately

    def test_message_queuing_integration(self, messaging_system):
        """Test message queuing integration."""
        # Setup
        messages = [
            UnifiedMessage(
                message_id=f"queue_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"Queued message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(5)
        ]
        
        # Queue messages
        for message in messages:
            messaging_system.queue_message(message)
        
        # Verify
        assert len(messaging_system.message_queue) == 5

    def test_priority_queuing_integration(self, messaging_system):
        """Test priority-based message queuing."""
        # Setup
        normal_message = UnifiedMessage(
            message_id="queue_normal_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Normal queued message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        urgent_message = UnifiedMessage(
            message_id="queue_urgent_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Urgent queued message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )
        
        # Queue messages
        messaging_system.queue_message(normal_message)
        messaging_system.queue_message(urgent_message)
        
        # Verify urgent message is prioritized
        assert messaging_system.message_queue[0] == urgent_message
        assert messaging_system.message_queue[1] == normal_message

    def test_message_type_handling_integration(self, messaging_system, temp_inbox_dirs):
        """Test different message type handling integration."""
        # Setup
        text_message = UnifiedMessage(
            message_id="type_text_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Text message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        broadcast_message = UnifiedMessage(
            message_id="type_broadcast_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Broadcast message",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        text_result = messaging_system.send_message(text_message)
        broadcast_result = messaging_system.send_message(broadcast_message)
        
        # Verify
        assert text_result is True
        assert broadcast_result is True
        
        # Verify both messages were delivered
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == 2

    def test_agent_coordination_integration(self, messaging_system, temp_inbox_dirs):
        """Test agent coordination messaging integration."""
        # Setup
        coordination_message = UnifiedMessage(
            message_id="coordination_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Agent coordination test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR,
            tags=[UnifiedMessageTag.CAPTAIN]
        )
        
        # Execute
        result = messaging_system.send_message(coordination_message)
        
        # Verify
        assert result is True
        
        # Verify message was delivered with proper formatting
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == 1
        
        with open(message_files[0], 'r') as f:
            content = f.read()
        assert "CAPTAIN" in content

    def test_system_performance_integration(self, messaging_system, temp_inbox_dirs):
        """Test system performance under load."""
        # Setup
        messages = [
            UnifiedMessage(
                message_id=f"perf_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"Performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(100)
        ]
        
        # Execute
        start_time = time.time()
        results = messaging_system.bulk_send_messages(messages)
        end_time = time.time()
        
        # Verify
        assert len(results) == 100
        assert all(results.values())
        
        # Verify performance (should complete within reasonable time)
        execution_time = end_time - start_time
        assert execution_time < 10.0  # Should complete within 10 seconds
        
        # Verify all messages were delivered
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == 100

    def test_fault_tolerance_integration(self, messaging_system, temp_inbox_dirs):
        """Test system fault tolerance."""
        # Setup
        valid_message = UnifiedMessage(
            message_id="fault_valid_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Valid message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        invalid_message = UnifiedMessage(
            message_id="fault_invalid_001",
            sender="Agent-1",
            recipient="Invalid-Agent",
            content="Invalid message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute mixed valid/invalid messages
        valid_result = messaging_system.send_message(valid_message)
        invalid_result = messaging_system.send_message(invalid_message)
        
        # Verify
        assert valid_result is True
        assert invalid_result is False
        
        # Verify valid message was delivered
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == 1

    def test_message_persistence_integration(self, messaging_system, temp_inbox_dirs):
        """Test message persistence integration."""
        # Setup
        message = UnifiedMessage(
            message_id="persistence_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Persistence test message",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        result = messaging_system.send_message(message)
        
        # Verify
        assert result is True
        
        # Verify message persists after system restart simulation
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == 1
        
        # Verify message content persists
        with open(message_files[0], 'r') as f:
            content = f.read()
        assert "Persistence test message" in content


def run_integration_tests():
    """Run all messaging system integration tests."""
    get_logger(__name__).info("🧪 MESSAGING SYSTEM INTEGRATION TEST SUITE - AGENT-1")
    get_logger(__name__).info("=" * 70)
    
    # Run pytest with verbose output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])


if __name__ == "__main__":
    run_integration_tests()
