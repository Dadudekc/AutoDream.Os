#!/usr/bin/env python3
"""
Comprehensive Performance Test Suite for Messaging System - Agent-1 Integration & Core Systems
============================================================================================

Comprehensive performance test coverage for the messaging system.
Tests system performance, scalability, and resource usage under various loads.

V2 Compliance: Comprehensive performance test coverage with unified logging integration.

Author: Agent-1 - Integration & Core Systems Specialist
License: MIT
"""

import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import messaging components
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType
)


class TestMessagingSystemPerformance:
    """Performance test suite for the messaging system."""

    @pytest.fixture
    def temp_inbox_dirs(self):
        """Create temporary inbox directories for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            inbox_dirs = {}
            for i in range(1, 9):  # Create 8 test agents
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

    def test_single_message_performance(self, messaging_system):
        """Test single message delivery performance."""
        # Setup
        message = UnifiedMessage(
            message_id="perf_single_001",
            sender="Agent-1",
            recipient="Agent-2",
            content="Single message performance test",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        start_time = time.time()
        result = messaging_system.send_message(message)
        end_time = time.time()
        
        # Verify
        assert result is True
        execution_time = end_time - start_time
        assert execution_time < 1.0  # Should complete within 1 second

    def test_bulk_message_performance(self, messaging_system, temp_inbox_dirs):
        """Test bulk message delivery performance."""
        # Setup
        message_count = 100
        messages = [
            UnifiedMessage(
                message_id=f"perf_bulk_{i}",
                sender="Agent-1",
                recipient=f"Agent-{(i % 8) + 1}",  # Distribute across 8 agents
                content=f"Bulk performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(message_count)
        ]
        
        # Execute
        start_time = time.time()
        results = messaging_system.bulk_send_messages(messages)
        end_time = time.time()
        
        # Verify
        assert len(results) == message_count
        assert all(results.values())
        
        execution_time = end_time - start_time
        messages_per_second = message_count / execution_time
        
        # Performance assertions
        assert execution_time < 10.0  # Should complete within 10 seconds
        assert messages_per_second > 10  # Should process at least 10 messages per second
        
        # Verify all messages were delivered
        total_delivered = 0
        for i in range(1, 9):
            agent_inbox = get_unified_utility().Path(temp_inbox_dirs[f"Agent-{i}"])
            message_files = list(agent_inbox.glob("*.md"))
            total_delivered += len(message_files)
        
        assert total_delivered == message_count

    def test_concurrent_message_performance(self, messaging_system, temp_inbox_dirs):
        """Test concurrent message delivery performance."""
        # Setup
        message_count = 50
        messages = [
            UnifiedMessage(
                message_id=f"perf_concurrent_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"Concurrent performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(message_count)
        ]
        
        # Execute concurrently
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(messaging_system.send_message, msg) for msg in messages]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        
        # Verify
        assert len(results) == message_count
        assert all(results)
        
        execution_time = end_time - start_time
        messages_per_second = message_count / execution_time
        
        # Performance assertions
        assert execution_time < 5.0  # Should complete within 5 seconds
        assert messages_per_second > 10  # Should process at least 10 messages per second
        
        # Verify all messages were delivered
        agent2_inbox = get_unified_utility().Path(temp_inbox_dirs["Agent-2"])
        message_files = list(agent2_inbox.glob("*.md"))
        assert len(message_files) == message_count

    def test_memory_usage_performance(self, messaging_system):
        """Test memory usage during message processing."""
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Setup
        message_count = 1000
        messages = [
            UnifiedMessage(
                message_id=f"perf_memory_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"Memory performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(message_count)
        ]
        
        # Execute
        start_time = time.time()
        results = messaging_system.bulk_send_messages(messages)
        end_time = time.time()
        
        # Get final memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Verify
        assert len(results) == message_count
        assert all(results.values())
        
        # Memory usage assertions
        memory_per_message = memory_increase / message_count
        assert memory_per_message < 1024  # Should use less than 1KB per message
        
        # Force garbage collection
        gc.collect()
        
        # Verify memory is cleaned up
        cleaned_memory = process.memory_info().rss
        memory_cleanup = final_memory - cleaned_memory
        assert memory_cleanup > 0  # Some memory should be cleaned up

    def test_cpu_usage_performance(self, messaging_system):
        """Test CPU usage during message processing."""
        # Setup
        message_count = 100
        messages = [
            UnifiedMessage(
                message_id=f"perf_cpu_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"CPU performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(message_count)
        ]
        
        # Execute
        start_time = time.time()
        results = messaging_system.bulk_send_messages(messages)
        end_time = time.time()
        
        # Verify
        assert len(results) == message_count
        assert all(results.values())
        
        execution_time = end_time - start_time
        messages_per_second = message_count / execution_time
        
        # CPU efficiency assertions
        assert messages_per_second > 50  # Should process at least 50 messages per second

    def test_large_message_performance(self, messaging_system):
        """Test performance with large messages."""
        # Setup
        large_content = "Large message content " * 1000  # ~20KB message
        message = UnifiedMessage(
            message_id="perf_large_001",
            sender="Agent-1",
            recipient="Agent-2",
            content=large_content,
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.REGULAR
        )
        
        # Execute
        start_time = time.time()
        result = messaging_system.send_message(message)
        end_time = time.time()
        
        # Verify
        assert result is True
        execution_time = end_time - start_time
        assert execution_time < 2.0  # Should complete within 2 seconds

    def test_priority_message_performance(self, messaging_system):
        """Test performance with priority message handling."""
        # Setup
        message_count = 50
        messages = []
        
        # Create mix of normal and urgent messages
        for i in range(message_count):
            priority = UnifiedMessagePriority.URGENT if i % 5 == 0 else UnifiedMessagePriority.REGULAR
            message = UnifiedMessage(
                message_id=f"perf_priority_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"Priority performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=priority
            )
            messages.append(message)
        
        # Execute
        start_time = time.time()
        results = messaging_system.bulk_send_messages(messages)
        end_time = time.time()
        
        # Verify
        assert len(results) == message_count
        assert all(results.values())
        
        execution_time = end_time - start_time
        messages_per_second = message_count / execution_time
        
        # Performance assertions
        assert execution_time < 5.0  # Should complete within 5 seconds
        assert messages_per_second > 10  # Should process at least 10 messages per second

    def test_message_queuing_performance(self, messaging_system):
        """Test message queuing performance."""
        # Setup
        message_count = 1000
        messages = [
            UnifiedMessage(
                message_id=f"perf_queue_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"Queue performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(message_count)
        ]
        
        # Execute - queue messages
        start_time = time.time()
        for message in messages:
            messaging_system.queue_message(message)
        end_time = time.time()
        
        # Verify
        assert len(messaging_system.message_queue) == message_count
        
        execution_time = end_time - start_time
        queue_operations_per_second = message_count / execution_time
        
        # Performance assertions
        assert execution_time < 1.0  # Should complete within 1 second
        assert queue_operations_per_second > 1000  # Should queue at least 1000 messages per second

    def test_system_health_performance(self, messaging_system):
        """Test system health check performance."""
        # Execute multiple health checks
        start_time = time.time()
        health_checks = []
        
        for _ in range(100):
            health = messaging_system.get_system_health()
            health_checks.append(health)
        
        end_time = time.time()
        
        # Verify
        assert len(health_checks) == 100
        assert all(get_unified_validator().validate_type(health, dict) for health in health_checks)
        
        execution_time = end_time - start_time
        health_checks_per_second = 100 / execution_time
        
        # Performance assertions
        assert execution_time < 1.0  # Should complete within 1 second
        assert health_checks_per_second > 100  # Should perform at least 100 health checks per second

    def test_error_handling_performance(self, messaging_system):
        """Test error handling performance."""
        # Setup
        message_count = 100
        messages = [
            UnifiedMessage(
                message_id=f"perf_error_{i}",
                sender="Agent-1",
                recipient="Invalid-Agent",  # Invalid recipient
                content=f"Error performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(message_count)
        ]
        
        # Execute
        start_time = time.time()
        results = messaging_system.bulk_send_messages(messages)
        end_time = time.time()
        
        # Verify
        assert len(results) == message_count
        assert not any(results.values())  # All should fail
        
        execution_time = end_time - start_time
        error_handling_per_second = message_count / execution_time
        
        # Performance assertions
        assert execution_time < 2.0  # Should complete within 2 seconds
        assert error_handling_per_second > 50  # Should handle at least 50 errors per second

    def test_scalability_performance(self, messaging_system, temp_inbox_dirs):
        """Test system scalability with increasing load."""
        # Test different message counts
        message_counts = [10, 50, 100, 500, 1000]
        performance_results = {}
        
        for count in message_counts:
            # Setup
            messages = [
                UnifiedMessage(
                    message_id=f"perf_scale_{count}_{i}",
                    sender="Agent-1",
                    recipient=f"Agent-{(i % 8) + 1}",
                    content=f"Scalability test message {i}",
                    message_type=UnifiedMessageType.TEXT,
                    priority=UnifiedMessagePriority.REGULAR
                )
                for i in range(count)
            ]
            
            # Execute
            start_time = time.time()
            results = messaging_system.bulk_send_messages(messages)
            end_time = time.time()
            
            # Record performance
            execution_time = end_time - start_time
            messages_per_second = count / execution_time
            performance_results[count] = {
                'execution_time': execution_time,
                'messages_per_second': messages_per_second,
                'success_rate': sum(results.values()) / len(results)
            }
            
            # Verify
            assert len(results) == count
            assert all(results.values())
        
        # Verify scalability
        for count in message_counts:
            perf = performance_results[count]
            assert perf['success_rate'] == 1.0  # 100% success rate
            assert perf['messages_per_second'] > 10  # Minimum throughput

    def test_resource_cleanup_performance(self, messaging_system):
        """Test resource cleanup performance."""
        # Setup
        message_count = 100
        messages = [
            UnifiedMessage(
                message_id=f"perf_cleanup_{i}",
                sender="Agent-1",
                recipient="Agent-2",
                content=f"Cleanup performance test message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(message_count)
        ]
        
        # Execute
        start_time = time.time()
        results = messaging_system.bulk_send_messages(messages)
        end_time = time.time()
        
        # Force garbage collection
        gc_start = time.time()
        gc.collect()
        gc_end = time.time()
        
        # Verify
        assert len(results) == message_count
        assert all(results.values())
        
        # Resource cleanup assertions
        cleanup_time = gc_end - gc_start
        assert cleanup_time < 0.1  # Garbage collection should be fast

    def test_throughput_benchmark(self, messaging_system, temp_inbox_dirs):
        """Test system throughput benchmark."""
        # Setup
        message_count = 1000
        messages = [
            UnifiedMessage(
                message_id=f"perf_throughput_{i}",
                sender="Agent-1",
                recipient=f"Agent-{(i % 8) + 1}",
                content=f"Throughput benchmark message {i}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            for i in range(message_count)
        ]
        
        # Execute
        start_time = time.time()
        results = messaging_system.bulk_send_messages(messages)
        end_time = time.time()
        
        # Calculate throughput
        execution_time = end_time - start_time
        throughput = message_count / execution_time
        
        # Verify
        assert len(results) == message_count
        assert all(results.values())
        
        # Throughput assertions
        assert throughput > 100  # Should achieve at least 100 messages per second
        assert execution_time < 10.0  # Should complete within 10 seconds
        
        # Verify all messages were delivered
        total_delivered = 0
        for i in range(1, 9):
            agent_inbox = get_unified_utility().Path(temp_inbox_dirs[f"Agent-{i}"])
            message_files = list(agent_inbox.glob("*.md"))
            total_delivered += len(message_files)
        
        assert total_delivered == message_count


def run_performance_tests():
    """Run all messaging system performance tests."""
    get_logger(__name__).info("🧪 MESSAGING SYSTEM PERFORMANCE TEST SUITE - AGENT-1")
    get_logger(__name__).info("=" * 70)
    
    # Run pytest with verbose output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])


if __name__ == "__main__":
    run_performance_tests()
