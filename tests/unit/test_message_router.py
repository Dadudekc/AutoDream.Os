#!/usr/bin/env python3
"""
UNIT TESTS - Message Router Component
====================================

Comprehensive unit tests for MessageRouter component with focus on:
- Intent-oriented message routing and delivery
- Message priority and type handling
- Queue management and threading
- Error handling and edge cases
- Performance and reliability testing

Author: Agent-5 (Business Intelligence Specialist)
Test Coverage Target: 95%+
"""

import queue
import sys
import threading
import time
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.orchestration.intent_subsystems.message_router import (
    MessagePriority,
    MessageRouter,
    MessageType,
    RoutingResult,
)


class TestMessageRouterUnit:
    """Unit tests for MessageRouter component."""

    def setup_method(self):
        """Setup test fixtures."""
        self.router = MessageRouter()
        self.router.start()

    def teardown_method(self):
        """Cleanup test fixtures."""
        self.router.stop()
        self.router.join(timeout=1.0)

    @pytest.mark.unit
    def test_router_initialization(self):
        """Test MessageRouter initialization."""
        router = MessageRouter()
        assert router is not None
        assert hasattr(router, "message_queue")
        assert hasattr(router, "routing_table")
        assert hasattr(router, "worker_thread")
        assert isinstance(router.message_queue, queue.Queue)
        assert not router.running

    @pytest.mark.unit
    def test_router_start_stop(self):
        """Test router start/stop functionality."""
        router = MessageRouter()

        # Initially not running
        assert not router.running

        # Start router
        router.start()
        assert router.running
        assert router.worker_thread.is_alive()

        # Stop router
        router.stop()
        router.join(timeout=1.0)
        assert not router.running

    @pytest.mark.unit
    def test_message_priority_enum(self):
        """Test MessagePriority enum values."""
        assert MessagePriority.LOW.value == "low"
        assert MessagePriority.NORMAL.value == "normal"
        assert MessagePriority.HIGH.value == "high"
        assert MessagePriority.URGENT.value == "urgent"

        # Test all enum values
        priorities = [p.value for p in MessagePriority]
        assert "low" in priorities
        assert "normal" in priorities
        assert "high" in priorities
        assert "urgent" in priorities

    @pytest.mark.unit
    def test_message_type_enum(self):
        """Test MessageType enum values."""
        expected_types = [
            "agent_to_agent",
            "system_to_agent",
            "human_to_agent",
            "captain_to_agent",
            "broadcast",
            "onboarding",
            "coordination",
            "status",
        ]

        for msg_type in expected_types:
            assert hasattr(MessageType, msg_type.upper())
            assert getattr(MessageType, msg_type.upper()).value == msg_type

    @pytest.mark.unit
    def test_routing_result_enum(self):
        """Test RoutingResult enum values."""
        # Check that RoutingResult has expected values
        assert hasattr(RoutingResult, "SUCCESS")
        assert hasattr(RoutingResult, "FAILED")
        assert hasattr(RoutingResult, "QUEUED")
        assert hasattr(RoutingResult, "RETRY")

    @pytest.mark.unit
    def test_route_message_success(self):
        """Test successful message routing."""
        router = MessageRouter()
        router.start()

        # Create test message
        test_message = {
            "id": "test-msg-001",
            "type": MessageType.AGENT_TO_AGENT,
            "priority": MessagePriority.NORMAL,
            "sender": "Agent-1",
            "recipient": "Agent-5",
            "content": "Test message",
            "timestamp": time.time(),
        }

        # Route message
        result = router.route_message(test_message)

        # Verify result
        assert result == RoutingResult.QUEUED

        # Verify message was queued
        assert not router.message_queue.empty()

        router.stop()
        router.join(timeout=1.0)

    @pytest.mark.unit
    def test_route_message_invalid_format(self):
        """Test routing with invalid message format."""
        router = MessageRouter()

        # Test with invalid message (missing required fields)
        invalid_message = {"content": "Just content"}

        result = router.route_message(invalid_message)
        assert result == RoutingResult.FAILED

    @pytest.mark.unit
    def test_message_queue_operations(self):
        """Test message queue operations."""
        router = MessageRouter()

        # Test queue initially empty
        assert router.message_queue.empty()

        # Add message
        test_message = {
            "id": "test-msg-001",
            "type": MessageType.SYSTEM_TO_AGENT,
            "priority": MessagePriority.HIGH,
            "sender": "System",
            "recipient": "Agent-5",
            "content": "System alert",
            "timestamp": time.time(),
        }

        router.message_queue.put(test_message)
        assert not router.message_queue.empty()

        # Retrieve message
        retrieved = router.message_queue.get()
        assert retrieved == test_message

    @pytest.mark.unit
    def test_priority_based_routing(self):
        """Test priority-based message routing."""
        router = MessageRouter()

        # Create messages with different priorities
        urgent_msg = {
            "id": "urgent-msg",
            "type": MessageType.CAPTAIN_TO_AGENT,
            "priority": MessagePriority.URGENT,
            "sender": "Captain",
            "recipient": "Agent-5",
            "content": "Urgent command",
            "timestamp": time.time(),
        }

        normal_msg = {
            "id": "normal-msg",
            "type": MessageType.AGENT_TO_AGENT,
            "priority": MessagePriority.NORMAL,
            "sender": "Agent-1",
            "recipient": "Agent-5",
            "content": "Normal message",
            "timestamp": time.time(),
        }

        # Route messages
        urgent_result = router.route_message(urgent_msg)
        normal_result = router.route_message(normal_msg)

        # Both should be queued (priority handled internally)
        assert urgent_result == RoutingResult.QUEUED
        assert normal_result == RoutingResult.QUEUED

    @pytest.mark.unit
    def test_broadcast_message_routing(self):
        """Test broadcast message routing."""
        router = MessageRouter()

        broadcast_msg = {
            "id": "broadcast-msg",
            "type": MessageType.BROADCAST,
            "priority": MessagePriority.HIGH,
            "sender": "System",
            "recipient": "all_agents",
            "content": "System-wide broadcast",
            "timestamp": time.time(),
        }

        result = router.route_message(broadcast_msg)
        assert result == RoutingResult.QUEUED

    @pytest.mark.unit
    @patch("threading.Thread")
    def test_worker_thread_creation(self, mock_thread):
        """Test worker thread creation and management."""
        router = MessageRouter()

        # Mock thread creation
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance

        router.start()

        # Verify thread was created and started
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()

        router.stop()
        mock_thread_instance.join.assert_called_once_with(timeout=1.0)

    @pytest.mark.unit
    def test_router_error_handling(self):
        """Test error handling in router operations."""
        router = MessageRouter()

        # Test with None message
        result = router.route_message(None)
        assert result == RoutingResult.FAILED

        # Test with malformed message
        malformed = {"type": "invalid_type"}
        result = router.route_message(malformed)
        assert result == RoutingResult.FAILED

    @pytest.mark.unit
    def test_message_validation(self):
        """Test message validation logic."""
        router = MessageRouter()

        # Valid message
        valid_msg = {
            "id": "valid-msg",
            "type": MessageType.AGENT_TO_AGENT,
            "priority": MessagePriority.NORMAL,
            "sender": "Agent-1",
            "recipient": "Agent-5",
            "content": "Valid message",
            "timestamp": time.time(),
        }
        assert router._validate_message(valid_msg) == True

        # Invalid message - missing required field
        invalid_msg = {"content": "Missing fields", "timestamp": time.time()}
        assert router._validate_message(invalid_msg) == False

    @pytest.mark.unit
    def test_routing_table_management(self):
        """Test routing table operations."""
        router = MessageRouter()

        # Initially empty
        assert len(router.routing_table) == 0

        # Add route (this would be implementation specific)
        # router.routing_table["Agent-5"] = "some_route"

        # Test routing table access
        assert hasattr(router, "routing_table")

    @pytest.mark.unit
    def test_message_processing_worker(self):
        """Test message processing worker thread."""
        router = MessageRouter()

        # Test worker initialization
        assert router.worker_thread is None

        # Start router to create worker
        router.start()
        assert router.worker_thread is not None
        assert isinstance(router.worker_thread, threading.Thread)

        router.stop()
        router.join(timeout=1.0)

    @pytest.mark.unit
    def test_thread_safety(self):
        """Test thread safety of router operations."""
        router = MessageRouter()
        router.start()

        # Test concurrent message routing
        import threading

        results = []

        def route_test_message():
            msg = {
                "id": f"thread-msg-{threading.current_thread().ident}",
                "type": MessageType.AGENT_TO_AGENT,
                "priority": MessagePriority.NORMAL,
                "sender": "Agent-1",
                "recipient": "Agent-5",
                "content": "Thread-safe message",
                "timestamp": time.time(),
            }
            result = router.route_message(msg)
            results.append(result)

        # Create multiple threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=route_test_message)
            threads.append(t)
            t.start()

        # Wait for completion
        for t in threads:
            t.join(timeout=1.0)

        # Verify all messages were queued
        assert len(results) == 5
        assert all(r == RoutingResult.QUEUED for r in results)

        router.stop()
        router.join(timeout=1.0)

    @pytest.mark.unit
    def test_message_queue_capacity(self):
        """Test message queue capacity handling."""
        router = MessageRouter()

        # Fill queue to test capacity (if limited)
        for i in range(100):  # Test with reasonable number
            msg = {
                "id": f"capacity-test-{i}",
                "type": MessageType.STATUS,
                "priority": MessagePriority.LOW,
                "sender": "Test",
                "recipient": "Agent-5",
                "content": f"Message {i}",
                "timestamp": time.time(),
            }
            router.route_message(msg)

        # Verify messages are queued
        assert router.message_queue.qsize() >= 50  # Should have accumulated messages

    @pytest.mark.unit
    def test_router_performance_metrics(self):
        """Test router performance metrics collection."""
        router = MessageRouter()

        # Route several messages to generate metrics
        for i in range(10):
            msg = {
                "id": f"perf-test-{i}",
                "type": MessageType.COORDINATION,
                "priority": MessagePriority.NORMAL,
                "sender": "Test",
                "recipient": "Agent-5",
                "content": f"Performance test {i}",
                "timestamp": time.time(),
            }
            router.route_message(msg)

        # Check that router handled the load
        assert router.message_queue.qsize() == 10

    @pytest.mark.unit
    def test_message_type_routing_logic(self):
        """Test message type-specific routing logic."""
        router = MessageRouter()

        message_types = [
            MessageType.AGENT_TO_AGENT,
            MessageType.SYSTEM_TO_AGENT,
            MessageType.HUMAN_TO_AGENT,
            MessageType.CAPTAIN_TO_AGENT,
            MessageType.BROADCAST,
            MessageType.ONBOARDING,
            MessageType.COORDINATION,
            MessageType.STATUS,
        ]

        for msg_type in message_types:
            msg = {
                "id": f"type-test-{msg_type.value}",
                "type": msg_type,
                "priority": MessagePriority.NORMAL,
                "sender": "Test",
                "recipient": "Agent-5",
                "content": f"Type {msg_type.value} test",
                "timestamp": time.time(),
            }

            result = router.route_message(msg)
            assert result == RoutingResult.QUEUED

    @pytest.mark.unit
    def test_router_shutdown_graceful(self):
        """Test graceful router shutdown."""
        router = MessageRouter()
        router.start()

        # Add some messages before shutdown
        for i in range(3):
            msg = {
                "id": f"shutdown-test-{i}",
                "type": MessageType.STATUS,
                "priority": MessagePriority.LOW,
                "sender": "Test",
                "recipient": "Agent-5",
                "content": f"Shutdown test {i}",
                "timestamp": time.time(),
            }
            router.route_message(msg)

        # Shutdown gracefully
        router.stop()
        success = router.join(timeout=2.0)

        # Verify clean shutdown
        assert not router.running

    @pytest.mark.unit
    def test_message_retry_logic(self):
        """Test message retry logic for failed deliveries."""
        router = MessageRouter()

        # Test message that might need retry
        retry_msg = {
            "id": "retry-test",
            "type": MessageType.AGENT_TO_AGENT,
            "priority": MessagePriority.HIGH,
            "sender": "Agent-1",
            "recipient": "Agent-5",
            "content": "Retry test message",
            "timestamp": time.time(),
            "retry_count": 0,
        }

        result = router.route_message(retry_msg)
        assert result in [RoutingResult.QUEUED, RoutingResult.RETRY]


if __name__ == "__main__":
    pytest.main([__file__])
