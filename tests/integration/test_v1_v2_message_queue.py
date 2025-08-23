#!/usr/bin/env python3
"""
V1-V2 Message Queue System Test Suite
=====================================

Comprehensive testing for the integrated V1 PyAutoGUI + V2 architecture message queue.
"""

import pytest
import time
import threading
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# Import the message queue system
from src.services.v1_v2_message_queue_system import (
    V1V2MessageQueueSystem,
    MessageQueueManager,
    QueuedMessage,
    AgentConnection,
    MessageQueuePriority,
    MessageDeliveryMethod,
)
from src.services.cdp_message_delivery import (
    CDPMessageDelivery,
    CDPTarget,
    send_message_to_cursor,
    broadcast_message_to_cursor,
)
from src.core.v2_comprehensive_messaging_system import V2AgentStatus, V2AgentCapability, V2MessageStatus


class TestV1V2MessageQueueSystem:
    """Test suite for the main V1-V2 message queue system."""

    def setup_method(self):
        """Setup test environment before each test."""
        # Mock configuration
        self.mock_config = {
            "pyautogui_settings": {"failsafe": True, "pause": 0.1, "confidence": 0.9},
            "delivery_methods": {"default": "hybrid", "fallback": "pyautogui"},
            "high_priority": {"ctrl_enter_threshold": 2, "timeout_ms": 5000},
        }

        # Create message queue system with mocked config
        with patch(
            "src.services.v1_v2_message_queue_system.V1V2MessageQueueSystem._load_config",
            return_value=self.mock_config,
        ):
            self.queue_system = V1V2MessageQueueSystem()

    def teardown_method(self):
        """Cleanup test environment after each test."""
        if hasattr(self, "queue_system"):
            self.queue_system.stop()

    @pytest.mark.unit
    def test_message_queue_initialization(self):
        """Test message queue system initialization."""
        assert self.queue_system.is_running is True
        assert self.queue_system.message_queue.qsize() == 0
        assert len(self.queue_system.agent_connections) == 0

    @pytest.mark.unit
    def test_agent_registration(self):
        """Test agent registration functionality."""
        # Create test agent connection
        agent_conn = AgentConnection(
            agent_id="test_agent_001",
            agent_name="Test Agent",
            status=V2AgentStatus.ONLINE,
            capabilities=[V2AgentCapability.TASK_EXECUTION],
            delivery_methods=[MessageDeliveryMethod.PYAUTOGUI],
        )

        # Register agent
        self.queue_system.register_agent(agent_conn)

        # Verify registration
        assert "test_agent_001" in self.queue_system.agent_connections
        assert len(self.queue_system.delivery_workers) == 1
        assert (
            self.queue_system.agent_connections["test_agent_001"].agent_name
            == "Test Agent"
        )

    @pytest.mark.unit
    def test_message_queuing(self):
        """Test message queuing functionality."""
        # Register test agent
        agent_conn = AgentConnection(
            agent_id="test_agent_001",
            agent_name="Test Agent",
            status=V2AgentStatus.ONLINE,
            capabilities=[V2AgentCapability.TASK_EXECUTION],
            delivery_methods=[MessageDeliveryMethod.PYAUTOGUI],
        )
        self.queue_system.register_agent(agent_conn)

        # Send test message
        message_id = self.queue_system.send_message(
            source_agent="test_agent_001",
            target_agent="test_agent_002",
            content="Test message content",
            priority=MessageQueuePriority.HIGH,
        )

        # Verify message queued
        assert message_id is not None
        assert self.queue_system.message_queue.qsize() == 1

    @pytest.mark.unit
    def test_priority_scoring(self):
        """Test message priority scoring system."""
        # Create test messages with different priorities
        high_priority_msg = QueuedMessage(
            message_id="msg_001",
            source_agent="agent_1",
            target_agent="agent_2",
            content="High priority message",
            priority=MessageQueuePriority.HIGH,
            delivery_method=MessageDeliveryMethod.PYAUTOGUI,
            timestamp=time.time(),
        )

        normal_priority_msg = QueuedMessage(
            message_id="msg_002",
            source_agent="agent_1",
            target_agent="agent_2",
            content="Normal priority message",
            priority=MessageQueuePriority.NORMAL,
            delivery_method=MessageDeliveryMethod.PYAUTOGUI,
            timestamp=time.time(),
        )

        # Calculate priority scores
        high_score = self.queue_system._calculate_priority_score(high_priority_msg)
        normal_score = self.queue_system._calculate_priority_score(normal_priority_msg)

        # Verify priority ordering
        assert high_score > normal_score

        # Test high-priority flag boost
        high_priority_msg.high_priority_flag = True
        boosted_score = self.queue_system._calculate_priority_score(high_priority_msg)
        assert boosted_score > high_score

    @pytest.mark.unit
    def test_high_priority_flag_system(self):
        """Test high-priority flag system with Ctrl+Enter x2 detection."""
        # Test initial state
        assert self.queue_system.ctrl_enter_count == 0

        # Simulate Ctrl+Enter x2
        self.queue_system.ctrl_enter_count = 2
        self.queue_system.last_ctrl_enter_time = time.time()

        # Test threshold detection
        assert (
            self.queue_system.ctrl_enter_count
            >= self.queue_system.high_priority_timeout
        )

        # Test high-priority mode activation
        with patch.object(
            self.queue_system, "_process_high_priority_messages"
        ) as mock_process:
            self.queue_system._activate_high_priority_mode()
            mock_process.assert_called_once()

    @pytest.mark.unit
    def test_message_delivery_methods(self):
        """Test different message delivery methods."""
        # Test PyAutoGUI delivery method
        with patch("pyautogui.typewrite") as mock_typewrite, patch(
            "pyautogui.press"
        ) as mock_press:
            message = QueuedMessage(
                message_id="msg_001",
                source_agent="agent_1",
                target_agent="agent_2",
                content="Test message",
                priority=MessageQueuePriority.NORMAL,
                delivery_method=MessageDeliveryMethod.PYAUTOGUI,
                timestamp=time.time(),
            )

            # Mock agent connection
            self.queue_system.agent_connections["agent_2"] = AgentConnection(
                agent_id="agent_2",
                agent_name="Test Agent 2",
                status=V2AgentStatus.ONLINE,
                capabilities=[V2AgentCapability.TASK_EXECUTION],
                delivery_methods=[MessageDeliveryMethod.PYAUTOGUI],
                window_title="Test Window",
            )

            # Test delivery
            self.queue_system._deliver_via_pyautogui(message)

            # Verify PyAutoGUI was called
            mock_typewrite.assert_called_once_with("Test message", interval=0.01)
            mock_press.assert_called_once_with("enter")

    @pytest.mark.unit
    def test_hybrid_delivery_fallback(self):
        """Test hybrid delivery with fallback to PyAutoGUI."""
        message = QueuedMessage(
            message_id="msg_001",
            source_agent="agent_1",
            target_agent="agent_2",
            content="Test message",
            priority=MessageQueuePriority.NORMAL,
            delivery_method=MessageDeliveryMethod.HYBRID,
            timestamp=time.time(),
        )

        # Mock agent connection
        self.queue_system.agent_connections["agent_2"] = AgentConnection(
            agent_id="agent_2",
            agent_name="Test Agent 2",
            status=V2AgentStatus.ONLINE,
            capabilities=[V2AgentCapability.TASK_EXECUTION],
            delivery_methods=[MessageDeliveryMethod.HYBRID],
            window_title="Test Window",
        )

        # Test hybrid delivery with fallback
        with patch.object(
            self.queue_system, "_deliver_via_cdp", side_effect=NotImplementedError
        ), patch.object(self.queue_system, "_deliver_via_pyautogui") as mock_pyautogui:
            self.queue_system._deliver_via_hybrid(message)

            # Verify fallback to PyAutoGUI
            mock_pyautogui.assert_called_once_with(message)

    @pytest.mark.unit
    def test_queue_status_reporting(self):
        """Test queue status and statistics reporting."""
        # Register test agents
        agent_conn1 = AgentConnection(
            agent_id="agent_1",
            agent_name="Agent 1",
            status=V2AgentStatus.ONLINE,
            capabilities=[V2AgentCapability.TASK_EXECUTION],
            delivery_methods=[MessageDeliveryMethod.PYAUTOGUI],
        )

        agent_conn2 = AgentConnection(
            agent_id="agent_2",
            agent_name="Agent 2",
            status=V2AgentStatus.BUSY,
            capabilities=[V2AgentCapability.MONITORING],
            delivery_methods=[MessageDeliveryMethod.CDP_PROTOCOL],
        )

        self.queue_system.register_agent(agent_conn1)
        self.queue_system.register_agent(agent_conn2)

        # Get status
        status = self.queue_system.get_queue_status()

        # Verify status structure
        assert "queue_size" in status
        assert "is_running" in status
        assert "agent_connections" in status
        assert "high_priority_active" in status
        assert "delivery_workers" in status

        # Verify agent information
        assert "agent_1" in status["agent_connections"]
        assert "agent_2" in status["agent_connections"]
        assert status["agent_connections"]["agent_1"]["name"] == "Agent 1"
        assert status["agent_connections"]["agent_2"]["status"] == "busy"


class TestMessageQueueManager:
    """Test suite for the high-level message queue manager."""

    def setup_method(self):
        """Setup test environment before each test."""
        with patch(
            "src.services.v1_v2_message_queue_system.V1V2MessageQueueSystem._load_config",
            return_value={},
        ):
            self.manager = MessageQueueManager()

    def teardown_method(self):
        """Cleanup test environment after each test."""
        if hasattr(self, "manager"):
            self.manager.queue_system.stop()

    @pytest.mark.unit
    def test_agent_registration(self):
        """Test agent registration through the manager."""
        # Register test agent
        success = self.manager.register_agent(
            agent_id="test_agent",
            agent_name="Test Agent",
            capabilities=[V2AgentCapability.TASK_EXECUTION, V2AgentCapability.MONITORING],
            window_title="Test Window",
        )

        # Verify registration
        assert success is True
        assert "test_agent" in self.manager.agent_registry
        assert self.manager.agent_registry["test_agent"].agent_name == "Test Agent"
        assert len(self.manager.agent_registry["test_agent"].capabilities) == 2

    @pytest.mark.unit
    def test_message_sending(self):
        """Test message sending through the manager."""
        # Register source and target agents
        self.manager.register_agent(
            agent_id="source_agent",
            agent_name="Source Agent",
            capabilities=[V2AgentCapability.TASK_EXECUTION],
        )

        self.manager.register_agent(
            agent_id="target_agent",
            agent_name="Target Agent",
            capabilities=[V2AgentCapability.MONITORING],
        )

        # Send message
        message_id = self.manager.send_message(
            source_agent="source_agent",
            target_agent="target_agent",
            content="Test message from manager",
            priority=MessageQueuePriority.HIGH,
        )

        # Verify message sent
        assert message_id is not None
        assert self.manager.queue_system.message_queue.qsize() == 1

    @pytest.mark.unit
    def test_broadcast_messaging(self):
        """Test broadcast messaging to all agents."""
        # Register multiple agents
        self.manager.register_agent(
            agent_id="agent_1",
            agent_name="Agent 1",
            capabilities=[V2AgentCapability.TASK_EXECUTION],
        )

        self.manager.register_agent(
            agent_id="agent_2",
            agent_name="Agent 2",
            capabilities=[V2AgentCapability.MONITORING],
        )

        self.manager.register_agent(
            agent_id="agent_3",
            agent_name="Agent 3",
            capabilities=[V2AgentCapability.DECISION_MAKING],
        )

        # Broadcast message
        message_ids = self.manager.broadcast_message(
            source_agent="agent_1",
            content="Broadcast message to all agents",
            priority=MessageQueuePriority.NORMAL,
        )

        # Verify broadcast
        assert len(message_ids) == 2  # Should send to 2 other agents (not self)
        assert self.manager.queue_system.message_queue.qsize() == 2

    @pytest.mark.unit
    def test_system_status_reporting(self):
        """Test comprehensive system status reporting."""
        # Register test agents
        self.manager.register_agent(
            agent_id="agent_1",
            agent_name="Agent 1",
            capabilities=[V2AgentCapability.TASK_EXECUTION],
            window_title="Window 1",
        )

        self.manager.register_agent(
            agent_id="agent_2",
            agent_name="Agent 2",
            capabilities=[V2AgentCapability.MONITORING],
            window_title="Window 2",
        )

        # Get system status
        status = self.manager.get_system_status()

        # Verify status structure
        assert "queue_system" in status
        assert "registered_agents" in status
        assert "agent_details" in status

        # Verify agent details
        assert status["registered_agents"] == 2
        assert "agent_1" in status["agent_details"]
        assert "agent_2" in status["agent_details"]
        assert status["agent_details"]["agent_1"]["name"] == "Agent 1"
        assert status["agent_details"]["agent_2"]["window_title"] == "Window 2"


class TestCDPMessageDelivery:
    """Test suite for CDP message delivery system."""

    def setup_method(self):
        """Setup test environment before each test."""
        self.cdp_delivery = CDPMessageDelivery(cdp_port=9222)

    @pytest.mark.unit
    def test_cdp_target_creation(self):
        """Test CDP target creation and validation."""
        target = CDPTarget(
            id="target_001",
            title="Test Target",
            url="http://localhost:3000",
            type="page",
            web_socket_debugger_url="ws://localhost:9222/devtools/page/target_001",
        )

        assert target.id == "target_001"
        assert target.title == "Test Target"
        assert target.url == "http://localhost:3000"
        assert target.type == "page"
        assert (
            target.web_socket_debugger_url
            == "ws://localhost:9222/devtools/page/target_001"
        )

    @pytest.mark.unit
    def test_js_template_generation(self):
        """Test JavaScript template generation."""
        js_template = self.cdp_delivery._get_js_template()

        # Verify template contains key components
        assert "findInput()" in js_template
        assert "candidates" in js_template
        assert "sendButtonSelectors" in js_template
        assert "synthetic Enter key" in js_template
        assert "returnByValue" in js_template

    @pytest.mark.unit
    def test_cursor_target_detection(self):
        """Test Cursor-specific target detection."""
        # Mock targets data
        mock_targets_data = [
            {
                "id": "target_1",
                "title": "Cursor - Agent Project",
                "url": "http://localhost:3000",
                "type": "page",
                "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/target_1",
            },
            {
                "id": "target_2",
                "title": "DevTools",
                "url": "devtools://devtools/bundled/devtools_app.html",
                "type": "page",
                "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/target_2",
            },
            {
                "id": "target_3",
                "title": "Regular Web Page",
                "url": "http://example.com",
                "type": "page",
                "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/target_3",
            },
        ]

        with patch.object(
            self.cdp_delivery,
            "get_targets",
            return_value=[CDPTarget(**target) for target in mock_targets_data],
        ):
            cursor_targets = self.cdp_delivery.find_cursor_targets()

            # Should find Cursor target, exclude DevTools, include regular pages
            assert len(cursor_targets) >= 1
            assert any("cursor" in target.title.lower() for target in cursor_targets)
            assert not any(
                "devtools" in target.title.lower() for target in cursor_targets
            )


class TestMessageQueueIntegration:
    """Integration tests for the complete message queue system."""

    def setup_method(self):
        """Setup test environment before each test."""
        with patch(
            "src.services.v1_v2_message_queue_system.V1V2MessageQueueSystem._load_config",
            return_value={},
        ):
            self.manager = MessageQueueManager()

    def teardown_method(self):
        """Cleanup test environment after each test."""
        if hasattr(self, "manager"):
            self.manager.queue_system.stop()

    @pytest.mark.integration
    def test_complete_message_workflow(self):
        """Test complete message workflow from registration to delivery."""
        # Register agents
        self.manager.register_agent(
            agent_id="foundation_agent",
            agent_name="Foundation & Testing Specialist",
            capabilities=[V2AgentCapability.TASK_EXECUTION, V2AgentCapability.MONITORING],
            window_title="Cursor - Foundation Testing",
        )

        self.manager.register_agent(
            agent_id="ai_ml_agent",
            agent_name="AI/ML Specialist",
            capabilities=[
                V2AgentCapability.DECISION_MAKING,
                V2AgentCapability.DATA_PROCESSING,
            ],
            window_title="Cursor - AI ML Project",
        )

        # Send high-priority message
        message_id = self.manager.send_message(
            source_agent="foundation_agent",
            target_agent="ai_ml_agent",
            content="Agent-2: begin integration tests for services_v2/auth. Report in 60m.",
            priority=MessageQueuePriority.HIGH,
            high_priority=True,
        )

        # Verify message workflow
        assert message_id is not None

        # Get system status
        status = self.manager.get_system_status()
        assert status["registered_agents"] == 2
        assert status["queue_system"]["queue_size"] == 1

        # Verify agent capabilities
        foundation_agent = status["agent_details"]["foundation_agent"]
        ai_ml_agent = status["agent_details"]["ai_ml_agent"]

        assert V2AgentCapability.TASK_EXECUTION.value in foundation_agent["capabilities"]
        assert V2AgentCapability.MONITORING.value in foundation_agent["capabilities"]
        assert V2AgentCapability.DECISION_MAKING.value in ai_ml_agent["capabilities"]
        assert V2AgentCapability.DATA_PROCESSING.value in ai_ml_agent["capabilities"]

    @pytest.mark.integration
    def test_high_priority_broadcast(self):
        """Test high-priority broadcast messaging."""
        # Register multiple agents
        agents = ["agent_1", "agent_2", "agent_3", "agent_4"]

        for i, agent_id in enumerate(agents):
            self.manager.register_agent(
                agent_id=agent_id,
                agent_name=f"Agent {i+1}",
                capabilities=[V2AgentCapability.TASK_EXECUTION],
                window_title=f"Cursor - Project {i+1}",
            )

        # Broadcast high-priority message
        message_ids = self.manager.broadcast_message(
            source_agent="agent_1",
            content="ALL AGENTS: no acknowledgments—only diffs, commits, and checkmarks.",
            priority=MessageQueuePriority.URGENT,
            high_priority=True,
        )

        # Verify broadcast
        assert len(message_ids) == 3  # Should send to 3 other agents (not self)
        assert self.manager.queue_system.message_queue.qsize() == 3

        # Verify all messages are high priority
        for message_id in message_ids:
            # This would require accessing the actual message objects
            # For now, we'll verify the queue size
            pass


# Performance testing
@pytest.mark.performance
def test_message_queue_performance():
    """Performance test for message queue system."""
    with patch(
        "src.services.v1_v2_message_queue_system.V1V2MessageQueueSystem._load_config",
        return_value={},
    ):
        manager = MessageQueueManager()

        # Register multiple agents
        for i in range(10):
            manager.register_agent(
                agent_id=f"perf_agent_{i}",
                agent_name=f"Performance Agent {i}",
                capabilities=[V2AgentCapability.TASK_EXECUTION],
                window_title=f"Cursor - Performance Test {i}",
            )

        # Send multiple messages
        start_time = time.time()

        for i in range(100):
            manager.send_message(
                source_agent="perf_agent_0",
                target_agent=f"perf_agent_{i % 10}",
                content=f"Performance test message {i}",
                priority=MessageQueuePriority.NORMAL,
            )

        end_time = time.time()
        duration = end_time - start_time

        # Performance assertions
        assert duration < 5.0  # Should complete within 5 seconds
        assert manager.queue_system.message_queue.qsize() == 100

        # Cleanup
        manager.queue_system.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
