#!/usr/bin/env python3
"""
Test Suite for V2 Comprehensive Messaging System

Comprehensive testing of the truly unified messaging system that consolidates
ALL features from all 5 existing messaging systems.

Author: V2 Testing Specialist
License: MIT
"""

import unittest
import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.v2_comprehensive_messaging_system import (
    V2MessageType, V2MessagePriority, V2MessageStatus, V2AgentStatus,
    V2TaskStatus, V2WorkflowStatus, V2WorkflowType, V2AgentCapability,
    V2Message, V2AgentInfo, V2ComprehensiveMessagingSystem,
    create_onboarding_message, create_coordination_message, create_broadcast_message,
    create_task_message, create_workflow_message
)


class TestV2ComprehensiveEnums(unittest.TestCase):
    """Test V2 comprehensive enum definitions"""
    
    def test_message_types_comprehensive(self):
        """Test that ALL message types from all 5 systems are included"""
        # Core Communication (from agent_communication.py)
        core_types = [
            "task_assignment", "status_update", "performance_metric", "health_check",
            "coordination", "broadcast", "direct"
        ]
        
        # Advanced Messaging (from message_types.py)
        advanced_types = [
            "task", "response", "alert", "system", "validation", "feedback"
        ]
        
        # Workflow Management (from shared_enums.py)
        workflow_types = [
            "text", "notification", "command", "error", "contract_assignment",
            "emergency", "heartbeat", "system_command"
        ]
        
        # V2 specific
        v2_types = [
            "onboarding_start", "onboarding_phase", "onboarding_complete",
            "task_created", "task_started", "task_completed", "task_failed",
            "agent_registration", "agent_status", "agent_health", "agent_capability_update"
        ]
        
        all_expected_types = core_types + advanced_types + workflow_types + v2_types
        
        for expected_type in all_expected_types:
            self.assertIn(expected_type, [t.value for t in V2MessageType])
        
        # Verify we have more types than any individual system
        self.assertGreater(len(V2MessageType), 30)  # Should have 40+ types
    
    def test_priorities_comprehensive(self):
        """Test that ALL priority levels are included"""
        priorities = [p.value for p in V2MessagePriority]
        expected = list(range(1, 6))  # 1-5
        self.assertEqual(priorities, expected)
    
    def test_statuses_comprehensive(self):
        """Test that ALL status states are included"""
        statuses = [s.value for s in V2MessageStatus]
        expected_statuses = [
            "pending", "processing", "delivered", "acknowledged",
            "completed", "failed", "expired", "cancelled", "read"
        ]
        for expected in expected_statuses:
            self.assertIn(expected, statuses)
    
    def test_agent_statuses_comprehensive(self):
        """Test that ALL agent status states are included"""
        agent_statuses = [s.value for s in V2AgentStatus]
        expected_statuses = [
            "offline", "online", "busy", "idle", "error", "recovering",
            "maintenance", "onboarding", "training"
        ]
        for expected in expected_statuses:
            self.assertIn(expected, agent_statuses)
    
    def test_task_statuses_comprehensive(self):
        """Test that ALL task status states are included"""
        task_statuses = [s.value for s in V2TaskStatus]
        expected_statuses = [
            "pending", "assigned", "running", "completed", "failed",
            "skipped", "retrying", "cancelled"
        ]
        for expected in expected_statuses:
            self.assertIn(expected, task_statuses)
    
    def test_workflow_statuses_comprehensive(self):
        """Test that ALL workflow status states are included"""
        workflow_statuses = [s.value for s in V2WorkflowStatus]
        expected_statuses = [
            "created", "planning", "ready", "running", "paused", "completed",
            "failed", "cancelled", "recovering", "initializing", "initialized",
            "active", "waiting_for_ai", "processing_response", "optimizing",
            "scaling", "in_progress"
        ]
        for expected in expected_statuses:
            self.assertIn(expected, workflow_statuses)
    
    def test_agent_capabilities_comprehensive(self):
        """Test that ALL agent capabilities are included"""
        capabilities = [c.value for c in V2AgentCapability]
        expected_capabilities = [
            "task_execution", "decision_making", "communication",
            "data_processing", "monitoring", "reporting"
        ]
        for expected in expected_capabilities:
            self.assertIn(expected, capabilities)


class TestV2ComprehensiveMessage(unittest.TestCase):
    """Test V2 comprehensive message structure"""
    
    def test_message_creation_with_all_features(self):
        """Test message creation with ALL features from all systems"""
        message = V2Message(
            message_type=V2MessageType.ONBOARDING_PHASE,
            priority=V2MessagePriority.CRITICAL,
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            subject="Comprehensive Test",
            content="Testing all features",
            payload={"test": "data"},
            requires_acknowledgment=True,
            is_onboarding_message=True,
            phase_number=1,
            workflow_id="workflow-123",
            task_id="task-456",
            ttl=3600,
            max_retries=5,
            sequence_number=1,
            dependencies=["msg-1", "msg-2"],
            tags=["test", "comprehensive"]
        )
        
        # Verify all fields are set correctly
        self.assertEqual(message.message_type, V2MessageType.ONBOARDING_PHASE)
        self.assertEqual(message.priority, V2MessagePriority.CRITICAL)
        self.assertEqual(message.sender_id, "SYSTEM")
        self.assertEqual(message.recipient_id, "Agent-1")
        self.assertEqual(message.subject, "Comprehensive Test")
        self.assertEqual(message.content, "Testing all features")
        self.assertEqual(message.payload, {"test": "data"})
        self.assertTrue(message.requires_acknowledgment)
        self.assertTrue(message.is_onboarding_message)
        self.assertEqual(message.phase_number, 1)
        self.assertEqual(message.workflow_id, "workflow-123")
        self.assertEqual(message.task_id, "task-456")
        self.assertEqual(message.ttl, 3600)
        self.assertEqual(message.max_retries, 5)
        self.assertEqual(message.sequence_number, 1)
        self.assertEqual(message.dependencies, ["msg-1", "msg-2"])
        self.assertEqual(message.tags, ["test", "comprehensive"])
    
    def test_message_serialization_comprehensive(self):
        """Test comprehensive message serialization"""
        message = V2Message(
            message_type=V2MessageType.TASK_ASSIGNMENT,
            priority=V2MessagePriority.HIGH,
            sender_id="Agent-1",
            recipient_id="Agent-2",
            subject="Task Assignment",
            content="Complete this task",
            payload={"task_details": "important"},
            workflow_id="workflow-789",
            task_id="task-101",
            tags=["urgent", "assignment"]
        )
        
        message_dict = message.to_dict()
        
        # Verify all fields are serialized
        self.assertEqual(message_dict["message_type"], "task_assignment")
        self.assertEqual(message_dict["priority"], 3)  # HIGH = 3
        self.assertEqual(message_dict["sender_id"], "Agent-1")
        self.assertEqual(message_dict["recipient_id"], "Agent-2")
        self.assertEqual(message_dict["subject"], "Task Assignment")
        self.assertEqual(message_dict["content"], "Complete this task")
        self.assertEqual(message_dict["payload"], {"task_details": "important"})
        self.assertEqual(message_dict["workflow_id"], "workflow-789")
        self.assertEqual(message_dict["task_id"], "task-101")
        self.assertEqual(message_dict["tags"], ["urgent", "assignment"])
    
    def test_message_deserialization_comprehensive(self):
        """Test comprehensive message deserialization"""
        original_message = V2Message(
            message_type=V2MessageType.WORKFLOW_UPDATE,
            priority=V2MessagePriority.URGENT,
            sender_id="WorkflowEngine",
            recipient_id="Agent-3",
            subject="Workflow Update",
            content="Workflow status changed",
            payload={"status": "running"},
            workflow_id="workflow-456",
            sequence_number=5,
            dependencies=["msg-10", "msg-11"],
            tags=["workflow", "update"]
        )
        
        message_dict = original_message.to_dict()
        restored_message = V2Message.from_dict(message_dict)
        
        # Verify all fields are restored correctly
        self.assertEqual(restored_message.message_type, original_message.message_type)
        self.assertEqual(restored_message.priority, original_message.priority)
        self.assertEqual(restored_message.sender_id, original_message.sender_id)
        self.assertEqual(restored_message.recipient_id, original_message.recipient_id)
        self.assertEqual(restored_message.subject, original_message.subject)
        self.assertEqual(restored_message.content, original_message.content)
        self.assertEqual(restored_message.payload, original_message.payload)
        self.assertEqual(restored_message.workflow_id, original_message.workflow_id)
        self.assertEqual(restored_message.sequence_number, original_message.sequence_number)
        self.assertEqual(restored_message.dependencies, original_message.dependencies)
        self.assertEqual(restored_message.tags, original_message.tags)
    
    def test_message_advanced_features(self):
        """Test advanced message features from message_types.py"""
        message = V2Message(ttl=1, max_retries=2)
        
        # Test TTL expiration
        self.assertFalse(message.is_expired())
        import time
        time.sleep(1.1)
        self.assertTrue(message.is_expired())
        
        # Test retry logic
        self.assertFalse(message.can_retry())  # Expired
        message.ttl = None  # Remove TTL
        self.assertTrue(message.can_retry())
        
        message.increment_retry()
        self.assertTrue(message.can_retry())
        
        message.increment_retry()
        self.assertFalse(message.can_retry())
        self.assertEqual(message.status, V2MessageStatus.FAILED)
    
    def test_message_status_transitions(self):
        """Test comprehensive message status transitions"""
        message = V2Message()
        self.assertEqual(message.status, V2MessageStatus.PENDING)
        
        message.mark_delivered()
        self.assertEqual(message.status, V2MessageStatus.DELIVERED)
        self.assertIsNotNone(message.delivered_at)
        
        message.mark_acknowledged()
        self.assertEqual(message.status, V2MessageStatus.ACKNOWLEDGED)
        self.assertIsNotNone(message.acknowledged_at)
        
        message.mark_read()
        self.assertEqual(message.status, V2MessageStatus.READ)
        self.assertIsNotNone(message.read_at)


class TestV2ComprehensiveAgentInfo(unittest.TestCase):
    """Test V2 comprehensive agent information"""
    
    def test_agent_info_creation(self):
        """Test comprehensive agent info creation"""
        capabilities = [V2AgentCapability.TASK_EXECUTION, V2AgentCapability.DECISION_MAKING]
        
        agent_info = V2AgentInfo(
            agent_id="Agent-1",
            name="Test Agent",
            capabilities=capabilities,
            status=V2AgentStatus.ONLINE,
            last_seen=datetime.now(),
            endpoint="http://localhost:8000",
            metadata={"version": "2.0"},
            performance_metrics={"cpu": 0.5, "memory": 0.3},
            current_tasks=["task-1", "task-2"],
            workflow_participation=["workflow-1"]
        )
        
        # Verify all fields
        self.assertEqual(agent_info.agent_id, "Agent-1")
        self.assertEqual(agent_info.name, "Test Agent")
        self.assertEqual(agent_info.capabilities, capabilities)
        self.assertEqual(agent_info.status, V2AgentStatus.ONLINE)
        self.assertEqual(agent_info.endpoint, "http://localhost:8000")
        self.assertEqual(agent_info.metadata, {"version": "2.0"})
        self.assertEqual(agent_info.performance_metrics, {"cpu": 0.5, "memory": 0.3})
        self.assertEqual(agent_info.current_tasks, ["task-1", "task-2"])
        self.assertEqual(agent_info.workflow_participation, ["workflow-1"])
    
    def test_agent_info_serialization(self):
        """Test agent info serialization"""
        agent_info = V2AgentInfo(
            agent_id="Agent-2",
            name="Serialization Test Agent",
            capabilities=[V2AgentCapability.COMMUNICATION],
            status=V2AgentStatus.BUSY,
            last_seen=datetime.now(),
            endpoint="http://localhost:8001"
        )
        
        agent_dict = agent_info.to_dict()
        
        # Verify serialization
        self.assertEqual(agent_dict["agent_id"], "Agent-2")
        self.assertEqual(agent_dict["name"], "Serialization Test Agent")
        self.assertEqual(agent_dict["capabilities"], ["communication"])
        self.assertEqual(agent_dict["status"], "busy")
        self.assertEqual(agent_dict["endpoint"], "http://localhost:8001")


class TestV2ComprehensiveMessagingSystem(unittest.TestCase):
    """Test V2 comprehensive messaging system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.messaging_system = V2ComprehensiveMessagingSystem()
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.messaging_system.shutdown()
    
    def test_system_initialization(self):
        """Test comprehensive system initialization"""
        self.assertTrue(self.messaging_system.communication_active)
        self.assertEqual(len(self.messaging_system.messages), 0)
        self.assertEqual(len(self.messaging_system.message_queue), 0)
        self.assertEqual(len(self.messaging_system.registered_agents), 0)
        
        # Verify all components are initialized
        self.assertIsNotNone(self.messaging_system.queue_metrics)
        self.assertIsNotNone(self.messaging_system.agent_capabilities)
        self.assertIsNotNone(self.messaging_system.message_callbacks)
        self.assertIsNotNone(self.messaging_system.agent_status_callbacks)
    
    def test_comprehensive_message_sending(self):
        """Test sending messages with ALL features"""
        # Test onboarding message
        onboarding_id = self.messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.ONBOARDING_PHASE,
            subject="V2 Onboarding",
            content="Welcome to V2!",
            priority=V2MessagePriority.CRITICAL,
            requires_acknowledgment=True,
            is_onboarding_message=True,
            phase_number=1,
            workflow_id="onboarding-workflow",
            tags=["onboarding", "critical"]
        )
        
        self.assertIsNotNone(onboarding_id)
        
        # Test task message
        task_id = self.messaging_system.send_message(
            sender_id="TaskManager",
            recipient_id="Agent-2",
            message_type=V2MessageType.TASK_ASSIGNMENT,
            subject="Task Assignment",
            content="Complete this task",
            priority=V2MessagePriority.HIGH,
            task_id="task-123",
            dependencies=["task-122"],
            tags=["task", "assignment"]
        )
        
        self.assertIsNotNone(task_id)
        
        # Test workflow message
        workflow_id = self.messaging_system.send_message(
            sender_id="WorkflowEngine",
            recipient_id="Agent-3",
            message_type=V2MessageType.COORDINATION,
            subject="Workflow Update",
            content="Workflow status changed",
            priority=V2MessagePriority.NORMAL,
            workflow_id="workflow-456",
            sequence_number=5
        )
        
        self.assertIsNotNone(workflow_id)
        
        # Verify all messages are stored
        self.assertEqual(len(self.messaging_system.messages), 3)
        self.assertEqual(len(self.messaging_system.message_queue), 3)
    
    def test_comprehensive_message_retrieval(self):
        """Test retrieving messages with ALL features"""
        # Send different types of messages
        self.messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.ONBOARDING_PHASE,
            subject="Onboarding",
            content="Welcome",
            priority=V2MessagePriority.CRITICAL
        )
        
        self.messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.TASK_ASSIGNMENT,
            subject="Task",
            content="Complete task",
            priority=V2MessagePriority.HIGH
        )
        
        self.messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="broadcast",
            message_type=V2MessageType.SYSTEM,
            subject="System Update",
            content="System is online",
            priority=V2MessagePriority.NORMAL
        )
        
        # Get all messages for Agent-1
        messages = self.messaging_system.get_messages_for_agent("Agent-1")
        self.assertEqual(len(messages), 3)  # 2 direct + 1 broadcast
        
        # Verify priority sorting (CRITICAL first, then HIGH, then NORMAL)
        priorities = [msg.priority.value for msg in messages]
        self.assertEqual(priorities, [5, 3, 2])  # CRITICAL, HIGH, NORMAL
        
        # Test filtering by message type
        onboarding_messages = self.messaging_system.get_messages_for_agent(
            "Agent-1", 
            message_type=V2MessageType.ONBOARDING_PHASE
        )
        self.assertEqual(len(onboarding_messages), 1)
        self.assertEqual(onboarding_messages[0].message_type, V2MessageType.ONBOARDING_PHASE)
        
        # Test filtering by status
        pending_messages = self.messaging_system.get_messages_for_agent(
            "Agent-1", 
            status=V2MessageStatus.PENDING
        )
        self.assertEqual(len(pending_messages), 3)
    
    def test_comprehensive_agent_registration(self):
        """Test comprehensive agent registration"""
        capabilities = [
            V2AgentCapability.TASK_EXECUTION,
            V2AgentCapability.DECISION_MAKING,
            V2AgentCapability.COMMUNICATION
        ]
        
        success = self.messaging_system.register_agent(
            agent_id="Agent-1",
            name="Test Agent",
            capabilities=capabilities,
            endpoint="http://localhost:8000",
            metadata={"version": "2.0", "environment": "test"}
        )
        
        self.assertTrue(success)
        
        # Verify agent is registered
        self.assertIn("Agent-1", self.messaging_system.registered_agents)
        agent_info = self.messaging_system.registered_agents["Agent-1"]
        
        self.assertEqual(agent_info.name, "Test Agent")
        self.assertEqual(agent_info.capabilities, capabilities)
        self.assertEqual(agent_info.status, V2AgentStatus.ONLINE)
        self.assertEqual(agent_info.endpoint, "http://localhost:8000")
        self.assertEqual(agent_info.metadata, {"version": "2.0", "environment": "test"})
        
        # Verify capability index is updated
        for capability in capabilities:
            self.assertIn("Agent-1", self.messaging_system.agent_capabilities[capability.value])
    
    def test_comprehensive_system_status(self):
        """Test comprehensive system status reporting"""
        # Register an agent and send some messages
        self.messaging_system.register_agent(
            agent_id="Agent-1",
            name="Test Agent",
            capabilities=[V2AgentCapability.TASK_EXECUTION],
            endpoint="http://localhost:8000"
        )
        
        self.messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.ONBOARDING_PHASE,
            subject="Test",
            content="Test message"
        )
        
        status = self.messaging_system.get_system_status()
        
        # Verify all status components
        self.assertIn("system_active", status)
        self.assertIn("total_messages", status)
        self.assertIn("queued_messages", status)
        self.assertIn("registered_agents", status)
        self.assertIn("agent_message_counts", status)
        self.assertIn("message_types", status)
        self.assertIn("priority_counts", status)
        self.assertIn("queue_metrics", status)
        self.assertIn("agent_statuses", status)
        
        # Verify specific values
        self.assertEqual(status["total_messages"], 1)
        self.assertEqual(status["queued_messages"], 1)
        self.assertEqual(status["registered_agents"], 1)
        self.assertEqual(status["agent_message_counts"]["SYSTEM"], 1)
        
        # Verify message type counts
        self.assertEqual(status["message_types"]["onboarding_phase"], 1)
        
        # Verify priority counts
        self.assertEqual(status["priority_counts"][2], 1)  # NORMAL = 2
        
        # Verify queue metrics
        self.assertEqual(status["queue_metrics"]["enqueue_count"], 1)
        self.assertEqual(status["queue_metrics"]["current_size"], 1)
        
        # Verify agent statuses
        self.assertEqual(status["agent_statuses"]["Agent-1"], "online")


class TestV2ComprehensiveConvenienceFunctions(unittest.TestCase):
    """Test V2 comprehensive convenience functions"""
    
    def test_create_onboarding_message(self):
        """Test onboarding message creation"""
        message = create_onboarding_message("Agent-1", 1, "Welcome to Phase 1")
        
        self.assertEqual(message.message_type, V2MessageType.ONBOARDING_PHASE)
        self.assertEqual(message.sender_id, "SYSTEM")
        self.assertEqual(message.recipient_id, "Agent-1")
        self.assertEqual(message.priority, V2MessagePriority.CRITICAL)
        self.assertTrue(message.requires_acknowledgment)
        self.assertTrue(message.is_onboarding_message)
        self.assertEqual(message.phase_number, 1)
    
    def test_create_coordination_message(self):
        """Test coordination message creation"""
        message = create_coordination_message("Agent-1", "Agent-2", "Let's coordinate")
        
        self.assertEqual(message.message_type, V2MessageType.COORDINATION)
        self.assertEqual(message.sender_id, "Agent-1")
        self.assertEqual(message.recipient_id, "Agent-2")
        self.assertEqual(message.priority, V2MessagePriority.NORMAL)
    
    def test_create_broadcast_message(self):
        """Test broadcast message creation"""
        message = create_broadcast_message("SYSTEM", "System is online")
        
        self.assertEqual(message.message_type, V2MessageType.BROADCAST)
        self.assertEqual(message.sender_id, "SYSTEM")
        self.assertEqual(message.recipient_id, "broadcast")
        self.assertEqual(message.priority, V2MessagePriority.NORMAL)
    
    def test_create_task_message(self):
        """Test task message creation"""
        message = create_task_message("TaskManager", "Agent-1", "task-123", "Complete this task")
        
        self.assertEqual(message.message_type, V2MessageType.TASK_ASSIGNMENT)
        self.assertEqual(message.sender_id, "TaskManager")
        self.assertEqual(message.recipient_id, "Agent-1")
        self.assertEqual(message.subject, "Task Assignment: task-123")
        self.assertEqual(message.content, "Complete this task")
        self.assertEqual(message.task_id, "task-123")
    
    def test_create_workflow_message(self):
        """Test workflow message creation"""
        message = create_workflow_message("WorkflowEngine", "Agent-1", "workflow-456", "Workflow updated")
        
        self.assertEqual(message.message_type, V2MessageType.COORDINATION)
        self.assertEqual(message.sender_id, "WorkflowEngine")
        self.assertEqual(message.recipient_id, "Agent-1")
        self.assertEqual(message.subject, "Workflow Update: workflow-456")
        self.assertEqual(message.content, "Workflow updated")
        self.assertEqual(message.workflow_id, "workflow-456")


class TestV2ComprehensiveIntegration(unittest.TestCase):
    """Test V2 comprehensive messaging system integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.messaging_system = V2ComprehensiveMessagingSystem()
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.messaging_system.shutdown()
    
    def test_complete_workflow_integration(self):
        """Test complete workflow integration with ALL features"""
        # 1. Register agents
        self.messaging_system.register_agent(
            agent_id="Agent-1",
            name="Workflow Agent",
            capabilities=[V2AgentCapability.TASK_EXECUTION, V2AgentCapability.DECISION_MAKING],
            endpoint="http://localhost:8000"
        )
        
        # 2. Send workflow start message
        workflow_start_id = self.messaging_system.send_message(
            sender_id="WorkflowEngine",
            recipient_id="Agent-1",
            message_type=V2MessageType.COORDINATION,
            subject="Workflow Started",
            content="Workflow execution has begun",
            priority=V2MessagePriority.HIGH,
            workflow_id="workflow-123",
            sequence_number=1,
            tags=["workflow", "start"]
        )
        
        # 3. Send task assignment
        task_id = self.messaging_system.send_message(
            sender_id="TaskManager",
            recipient_id="Agent-1",
            message_type=V2MessageType.TASK_ASSIGNMENT,
            subject="Task Assignment",
            content="Execute workflow step 1",
            priority=V2MessagePriority.HIGH,
            requires_acknowledgment=True,
            workflow_id="workflow-123",
            task_id="task-1",
            dependencies=[workflow_start_id],
            tags=["task", "workflow"]
        )
        
        # 4. Agent acknowledges task
        success = self.messaging_system.acknowledge_message(task_id, "Agent-1")
        self.assertTrue(success)
        
        # 5. Send task completion
        completion_id = self.messaging_system.send_message(
            sender_id="Agent-1",
            recipient_id="WorkflowEngine",
            message_type=V2MessageType.STATUS_UPDATE,
            subject="Task Completed",
            content="Workflow step 1 completed successfully",
            priority=V2MessagePriority.NORMAL,
            workflow_id="workflow-123",
            task_id="task-1",
            tags=["completion", "success"]
        )
        
        # 6. Verify system state
        status = self.messaging_system.get_system_status()
        
        self.assertEqual(status["total_messages"], 3)
        self.assertEqual(status["registered_agents"], 1)
        self.assertEqual(status["message_types"]["coordination"], 1)
        self.assertEqual(status["message_types"]["task_assignment"], 1)
        self.assertEqual(status["message_types"]["status_update"], 1)
        
        # 7. Get messages for agent
        agent_messages = self.messaging_system.get_messages_for_agent("Agent-1")
        self.assertEqual(len(agent_messages), 2)  # 2 messages TO Agent-1 (workflow start + task assignment)
        
        # 8. Verify message relationships
        task_message = next(m for m in agent_messages if m.message_type == V2MessageType.TASK_ASSIGNMENT)
        self.assertEqual(task_message.status, V2MessageStatus.ACKNOWLEDGED)
        self.assertIn(workflow_start_id, task_message.dependencies)
        self.assertEqual(task_message.workflow_id, "workflow-123")
        self.assertEqual(task_message.task_id, "task-1")
    
    def test_comprehensive_error_handling(self):
        """Test comprehensive error handling"""
        # Test sending message to non-existent agent
        message_id = self.messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="NonExistentAgent",
            message_type=V2MessageType.ONBOARDING_PHASE,
            subject="Test",
            content="Test message"
        )
        
        # Should still create message but log warning
        self.assertIsNotNone(message_id)
        self.assertIn(message_id, self.messaging_system.messages)
        
        # Test acknowledging non-existent message
        success = self.messaging_system.acknowledge_message("non-existent-id", "Agent-1")
        self.assertFalse(success)
        
        # Test acknowledging message that doesn't require acknowledgment
        message_id = self.messaging_system.send_message(
            sender_id="SYSTEM",
            recipient_id="Agent-1",
            message_type=V2MessageType.COORDINATION,
            subject="Test",
            content="Test message",
            requires_acknowledgment=False
        )
        
        success = self.messaging_system.acknowledge_message(message_id, "Agent-1")
        self.assertFalse(success)  # Should fail because acknowledgment not required


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
