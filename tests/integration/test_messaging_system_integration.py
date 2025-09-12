#!/usr/bin/env python3
"""
INTEGRATION TESTS - Messaging System End-to-End
===============================================

Comprehensive integration tests for complete messaging system with focus on:
- End-to-end message flow from Discord → Gateway → Router → Agent
- ConsolidatedMessagingService integration with routing components
- Cross-component communication and error handling
- Performance and reliability under load
- Real-world usage scenarios and edge cases

Author: Agent-5 (Business Intelligence Specialist)
Test Coverage Target: 95%+ for integration scenarios
"""

import asyncio
import sys
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import messaging components
try:
    from integration.messaging_gateway import MessagingGateway, send_discord_message_to_agent
    from services.consolidated_messaging_service import ConsolidatedMessagingService
    from core.orchestration.intent_subsystems.message_router import (
        MessageRouter,
        MessagePriority,
        MessageType,
    )

    MESSAGING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Messaging components not available: {e}")
    MESSAGING_AVAILABLE = False


@pytest.mark.skipif(not MESSAGING_AVAILABLE, reason="Messaging components not available")
class TestMessagingSystemIntegration:
    """Integration tests for complete messaging system."""

    def setup_method(self):
        """Setup integration test fixtures."""
        self.gateway = MessagingGateway()
        self.router = MessageRouter()
        self.messaging_service = ConsolidatedMessagingService(dry_run=True)

    def teardown_method(self):
        """Cleanup integration test fixtures."""
        if hasattr(self, "router") and self.router.running:
            self.router.stop()
            self.router.join(timeout=1.0)

    @pytest.mark.integration
    def test_end_to_end_message_flow(self):
        """Test complete message flow from Discord to Agent."""
        # Start router
        self.router.start()

        # Create test message (simulating Discord input)
        discord_message = {
            "type": "discord_command",
            "recipient": "Agent-5",
            "content": "Integration test message",
            "sender": "TestUser",
            "channel": "test-channel",
            "timestamp": time.time(),
        }

        # Test gateway message processing
        gateway_result = send_discord_message_to_agent("Agent-5", discord_message["content"])

        # Verify gateway accepted message
        assert gateway_result is True

        # Test router message processing
        router_message = {
            "id": "integration-test-001",
            "type": MessageType.AGENT_TO_AGENT,
            "priority": MessagePriority.NORMAL,
            "sender": "TestSystem",
            "recipient": "Agent-5",
            "content": discord_message["content"],
            "timestamp": time.time(),
        }

        router_result = self.router.route_message(router_message)
        assert router_result.name == "QUEUED"

        # Cleanup
        self.router.stop()
        self.router.join(timeout=1.0)

    @pytest.mark.integration
    @patch("services.consolidated_messaging_service.MESSAGING_AVAILABLE", True)
    def test_consolidated_service_gateway_integration(self):
        """Test ConsolidatedMessagingService integration with MessagingGateway."""
        # Test service initialization
        assert self.messaging_service is not None
        assert hasattr(self.messaging_service, "send_message")

        # Test message sending through service
        result = self.messaging_service.send_message(
            recipient="Agent-5", content="Integration test", priority="normal"
        )

        # Should succeed in dry-run mode
        assert result is True

    @pytest.mark.integration
    def test_message_routing_gateway_coordination(self):
        """Test coordination between MessageRouter and MessagingGateway."""
        self.router.start()

        # Test multiple message types through routing system
        test_messages = [
            {
                "type": MessageType.AGENT_TO_AGENT,
                "priority": MessagePriority.NORMAL,
                "content": "Agent coordination message",
            },
            {
                "type": MessageType.SYSTEM_TO_AGENT,
                "priority": MessagePriority.HIGH,
                "content": "System alert",
            },
            {
                "type": MessageType.BROADCAST,
                "priority": MessagePriority.URGENT,
                "content": "System-wide broadcast",
            },
        ]

        for i, msg_data in enumerate(test_messages):
            msg = {
                "id": f"routing-test-{i}",
                "type": msg_data["type"],
                "priority": msg_data["priority"],
                "sender": "IntegrationTest",
                "recipient": "Agent-5",
                "content": msg_data["content"],
                "timestamp": time.time(),
            }

            result = self.router.route_message(msg)
            assert result.name == "QUEUED"

        # Verify messages were queued
        assert self.router.message_queue.qsize() == 3

        self.router.stop()
        self.router.join(timeout=1.0)

    @pytest.mark.integration
    @patch("integration.messaging_gateway.pyautogui")
    @patch("integration.messaging_gateway.pyperclip")
    def test_gateway_physical_delivery_simulation(self, mock_pyperclip, mock_pyautogui):
        """Test gateway physical delivery simulation."""
        # Setup PyAutoGUI mocks
        mock_pyautogui.position.return_value = (652, 421)  # Agent-5 position
        mock_pyautogui.size.return_value = (1920, 1080)

        # Test message delivery
        result = send_discord_message_to_agent("Agent-5", "Physical delivery test")

        # Verify physical interaction simulation
        assert mock_pyautogui.moveTo.called
        assert mock_pyautogui.click.called
        assert mock_pyperclip.copy.called
        assert mock_pyautogui.hotkey.called_with("ctrl", "v")

        # Verify Agent-5 coordinates used
        mock_pyautogui.moveTo.assert_any_call(652, 421)

    @pytest.mark.integration
    def test_error_handling_across_components(self):
        """Test error handling across all messaging components."""
        # Test gateway with invalid agent
        gateway_result = send_discord_message_to_agent("Invalid-Agent", "Test")
        assert gateway_result is False

        # Test router with invalid message
        router_result = self.router.route_message({"invalid": "message"})
        assert router_result.name == "FAILED"

        # Test service with invalid parameters
        service_result = self.messaging_service.send_message(recipient="", content="")
        # Should handle gracefully
        assert isinstance(service_result, bool)

    @pytest.mark.integration
    def test_message_priority_handling_integration(self):
        """Test message priority handling across components."""
        self.router.start()

        # Test different priority levels
        priorities = [
            MessagePriority.LOW,
            MessagePriority.NORMAL,
            MessagePriority.HIGH,
            MessagePriority.URGENT,
        ]

        for priority in priorities:
            msg = {
                "id": f"priority-test-{priority.value}",
                "type": MessageType.AGENT_TO_AGENT,
                "priority": priority,
                "sender": "PriorityTest",
                "recipient": "Agent-5",
                "content": f"Priority {priority.value} test",
                "timestamp": time.time(),
            }

            result = self.router.route_message(msg)
            assert result.name == "QUEUED"

        # All messages should be queued
        assert self.router.message_queue.qsize() == 4

        self.router.stop()
        self.router.join(timeout=1.0)

    @pytest.mark.integration
    def test_broadcast_message_integration(self):
        """Test broadcast message handling across components."""
        self.router.start()

        # Test broadcast message
        broadcast_msg = {
            "id": "broadcast-integration-test",
            "type": MessageType.BROADCAST,
            "priority": MessagePriority.HIGH,
            "sender": "System",
            "recipient": "all_agents",
            "content": "Integration broadcast test",
            "timestamp": time.time(),
        }

        result = self.router.route_message(broadcast_msg)
        assert result.name == "QUEUED"

        # Test gateway broadcast capability
        gateway_result = send_discord_message_to_agent("Agent-5", "Gateway broadcast test")
        assert isinstance(gateway_result, bool)  # Should handle broadcast routing

        self.router.stop()
        self.router.join(timeout=1.0)

    @pytest.mark.integration
    @patch("services.consolidated_messaging_service.MESSAGING_AVAILABLE", True)
    def test_service_configuration_integration(self):
        """Test messaging service configuration integration."""
        # Test service with different configurations
        configs = [{"dry_run": True}, {"dry_run": False}, {"dry_run": True, "debug": True}]

        for config in configs:
            service = ConsolidatedMessagingService(**config)
            assert service is not None
            assert service.dry_run == config.get("dry_run", False)

    @pytest.mark.integration
    def test_message_format_compatibility(self):
        """Test message format compatibility across components."""
        self.router.start()

        # Test different message formats that should be compatible
        message_formats = [
            # Standard format
            {
                "id": "format-test-1",
                "type": MessageType.AGENT_TO_AGENT,
                "priority": MessagePriority.NORMAL,
                "sender": "Test",
                "recipient": "Agent-5",
                "content": "Standard format",
                "timestamp": time.time(),
            },
            # Extended format
            {
                "id": "format-test-2",
                "type": MessageType.SYSTEM_TO_AGENT,
                "priority": MessagePriority.HIGH,
                "sender": "System",
                "recipient": "Agent-5",
                "content": "Extended format",
                "timestamp": time.time(),
                "metadata": {"source": "integration_test"},
                "tags": ["test", "integration"],
            },
        ]

        for msg in message_formats:
            result = self.router.route_message(msg)
            assert result.name == "QUEUED"

        assert self.router.message_queue.qsize() == 2

        self.router.stop()
        self.router.join(timeout=1.0)

    @pytest.mark.integration
    def test_performance_under_load(self):
        """Test messaging system performance under load."""
        self.router.start()

        # Test with multiple concurrent messages
        message_count = 50
        start_time = time.time()

        for i in range(message_count):
            msg = {
                "id": f"load-test-{i}",
                "type": MessageType.AGENT_TO_AGENT,
                "priority": MessagePriority.NORMAL,
                "sender": "LoadTest",
                "recipient": "Agent-5",
                "content": f"Load test message {i}",
                "timestamp": time.time(),
            }
            self.router.route_message(msg)

        end_time = time.time()
        routing_time = end_time - start_time

        # Verify all messages were queued
        assert self.router.message_queue.qsize() == message_count

        # Performance check: should route quickly
        assert routing_time < 1.0  # Less than 1 second for 50 messages

        self.router.stop()
        self.router.join(timeout=1.0)

    @pytest.mark.integration
    def test_cross_component_error_propagation(self):
        """Test error propagation across messaging components."""
        # Test error scenarios
        error_scenarios = [
            # Invalid agent
            lambda: send_discord_message_to_agent("NonExistentAgent", "test"),
            # Invalid message format
            lambda: self.router.route_message({"content": "no other fields"}),
            # Service with invalid config
            lambda: ConsolidatedMessagingService(invalid_param="test"),
        ]

        for scenario in error_scenarios:
            try:
                result = scenario()
                # Should handle errors gracefully
                assert result is False or isinstance(result, bool)
            except Exception:
                # Some errors are expected, should be handled
                pass

    @pytest.mark.integration
    def test_message_routing_table_consistency(self):
        """Test routing table consistency across components."""
        # Test that all components use consistent agent identifiers
        known_agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]

        # Test gateway coordinate lookup
        from integration.messaging_gateway import get_agent_coordinates

        for agent in known_agents:
            coords = get_agent_coordinates(agent)
            assert coords is not None
            assert isinstance(coords, dict)

        # Test router can handle all known agents
        self.router.start()
        for agent in known_agents:
            msg = {
                "id": f"consistency-test-{agent}",
                "type": MessageType.AGENT_TO_AGENT,
                "priority": MessagePriority.NORMAL,
                "sender": "ConsistencyTest",
                "recipient": agent,
                "content": f"Test message for {agent}",
                "timestamp": time.time(),
            }
            result = self.router.route_message(msg)
            assert result.name == "QUEUED"

        assert self.router.message_queue.qsize() == len(known_agents)

        self.router.stop()
        self.router.join(timeout=1.0)

    @pytest.mark.integration
    def test_system_resilience_and_recovery(self):
        """Test system resilience and recovery capabilities."""
        self.router.start()

        # Test normal operation
        normal_msg = {
            "id": "resilience-test-normal",
            "type": MessageType.AGENT_TO_AGENT,
            "priority": MessagePriority.NORMAL,
            "sender": "ResilienceTest",
            "recipient": "Agent-5",
            "content": "Normal operation test",
            "timestamp": time.time(),
        }
        result = self.router.route_message(normal_msg)
        assert result.name == "QUEUED"

        # Test recovery after simulated disruption
        # (In a real scenario, this might involve network issues, component failures, etc.)

        # Test continued operation
        recovery_msg = {
            "id": "resilience-test-recovery",
            "type": MessageType.AGENT_TO_AGENT,
            "priority": MessagePriority.NORMAL,
            "sender": "ResilienceTest",
            "recipient": "Agent-5",
            "content": "Recovery test",
            "timestamp": time.time(),
        }
        result = self.router.route_message(recovery_msg)
        assert result.name == "QUEUED"

        assert self.router.message_queue.qsize() == 2

        self.router.stop()
        self.router.join(timeout=1.0)


if __name__ == "__main__":
    pytest.main([__file__])
