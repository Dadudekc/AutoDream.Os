"""
TDD Test Suite for Message Queue System - Agent Cellphone V2
===========================================================

PHASE 2: TDD Modular Decomposition - Test-First Development
Following Red → Green → Refactor cycle for message queue components

Test Priority: CRITICAL - Core messaging infrastructure
Component: src/core/messaging/message_queue.py (587 lines)
TDD Status: RED - Tests written first, implementation to follow
"""

import pytest
import json
import time
import threading
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Test target imports
from src.core.messaging.message_queue import MessageQueue, PersistentMessageQueue
from src.core.messaging.message_types import Message, MessagePriority, MessageStatus


class TestMessageQueueTDD:
    """
    TDD Test Suite for Abstract Message Queue
    
    Test Strategy: RED → GREEN → REFACTOR
    1. Write failing tests first
    2. Implement minimal code to pass
    3. Refactor for quality
    """
    
    def test_message_queue_initialization_tdd(self):
        """RED: Test message queue initialization - TDD First"""
        # This test defines expected behavior BEFORE implementation
        queue = PersistentMessageQueue("test_queue", max_size=100)
        
        assert queue.name == "test_queue"
        assert queue.max_size == 100
        assert queue._metrics['enqueue_count'] == 0
        assert queue._metrics['dequeue_count'] == 0
        assert queue._metrics['current_size'] == 0
        assert queue.is_empty() is True
        assert queue.is_full() is False
    
    def test_message_enqueue_basic_tdd(self):
        """RED: Test basic message enqueue - TDD First"""
        queue = PersistentMessageQueue("test_queue")
        message = Message(
            id="msg_001",
            content="Test message",
            priority=MessagePriority.NORMAL,
            sender="test_agent",
            recipient="target_agent"
        )
        
        # Expected behavior: successful enqueue
        result = queue.enqueue(message)
        assert result is True
        assert queue.size() == 1
        assert queue._metrics['enqueue_count'] == 1
        assert queue.is_empty() is False
    
    def test_message_dequeue_basic_tdd(self):
        """RED: Test basic message dequeue - TDD First"""
        queue = PersistentMessageQueue("test_queue")
        message = Message(
            id="msg_001",
            content="Test message",
            priority=MessagePriority.NORMAL,
            sender="test_agent",
            recipient="target_agent"
        )
        
        # Setup: enqueue first
        queue.enqueue(message)
        
        # Expected behavior: successful dequeue
        dequeued_message = queue.dequeue()
        assert dequeued_message is not None
        assert dequeued_message.id == "msg_001"
        assert queue.size() == 0
        assert queue._metrics['dequeue_count'] == 1
        assert queue.is_empty() is True
    
    def test_message_priority_ordering_tdd(self):
        """RED: Test priority-based message ordering - TDD First"""
        queue = PersistentMessageQueue("test_queue")
        
        # Create messages with different priorities
        low_msg = Message("low", "Low priority", MessagePriority.LOW, "agent1", "target")
        normal_msg = Message("normal", "Normal priority", MessagePriority.NORMAL, "agent2", "target")
        high_msg = Message("high", "High priority", MessagePriority.HIGH, "agent3", "target")
        critical_msg = Message("critical", "Critical priority", MessagePriority.CRITICAL, "agent4", "target")
        
        # Enqueue in random order
        queue.enqueue(normal_msg)
        queue.enqueue(low_msg)
        queue.enqueue(critical_msg)
        queue.enqueue(high_msg)
        
        # Expected behavior: dequeue in priority order
        first = queue.dequeue()
        second = queue.dequeue()
        third = queue.dequeue()
        fourth = queue.dequeue()
        
        assert first.priority == MessagePriority.CRITICAL
        assert second.priority == MessagePriority.HIGH
        assert third.priority == MessagePriority.NORMAL
        assert fourth.priority == MessagePriority.LOW
    
    def test_message_queue_max_size_enforcement_tdd(self):
        """RED: Test queue size limits - TDD First"""
        queue = PersistentMessageQueue("test_queue", max_size=2)
        
        msg1 = Message("msg1", "Message 1", MessagePriority.NORMAL, "agent", "target")
        msg2 = Message("msg2", "Message 2", MessagePriority.NORMAL, "agent", "target")
        msg3 = Message("msg3", "Message 3", MessagePriority.NORMAL, "agent", "target")
        
        # Expected behavior: first two messages succeed
        assert queue.enqueue(msg1) is True
        assert queue.enqueue(msg2) is True
        assert queue.is_full() is True
        
        # Expected behavior: third message fails (queue full)
        assert queue.enqueue(msg3) is False
        assert queue.size() == 2
        assert queue._metrics['error_count'] > 0
    
    def test_message_acknowledgment_tdd(self):
        """RED: Test message acknowledgment system - TDD First"""
        queue = PersistentMessageQueue("test_queue")
        message = Message("msg_001", "Test message", MessagePriority.NORMAL, "agent", "target")
        
        # Enqueue and dequeue
        queue.enqueue(message)
        dequeued_msg = queue.dequeue()
        
        # Expected behavior: message needs acknowledgment
        assert dequeued_msg.status == MessageStatus.DELIVERED
        
        # Expected behavior: successful acknowledgment
        result = queue.ack_message(dequeued_msg.id)
        assert result is True
        assert queue._metrics['ack_count'] == 1
        
        # Message should be marked as processed
        processed_msg = queue.get_message_by_id(dequeued_msg.id)
        assert processed_msg.status == MessageStatus.PROCESSED
    
    def test_message_persistence_tdd(self):
        """RED: Test message persistence to disk - TDD First"""
        temp_dir = Path("/tmp/test_message_queue")
        queue = PersistentMessageQueue("test_queue", storage_dir=temp_dir)
        
        message = Message("msg_001", "Test message", MessagePriority.NORMAL, "agent", "target")
        queue.enqueue(message)
        
        # Expected behavior: message persisted to disk
        queue_file = temp_dir / "test_queue.json"
        assert queue_file.exists()
        
        # Expected behavior: can read persisted data
        with open(queue_file, 'r') as f:
            data = json.load(f)
            assert len(data['messages']) == 1
            assert data['messages'][0]['id'] == "msg_001"
        
        # Cleanup
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)
    
    def test_message_queue_thread_safety_tdd(self):
        """RED: Test thread-safe operations - TDD First"""
        queue = PersistentMessageQueue("test_queue")
        results = []
        errors = []
        
        def enqueue_messages(start_id: int, count: int):
            """Thread worker for enqueuing messages"""
            try:
                for i in range(count):
                    msg = Message(
                        id=f"msg_{start_id + i}",
                        content=f"Message {start_id + i}",
                        priority=MessagePriority.NORMAL,
                        sender="thread_agent",
                        recipient="target"
                    )
                    results.append(queue.enqueue(msg))
            except Exception as e:
                errors.append(e)
        
        # Expected behavior: concurrent operations work correctly
        threads = []
        for i in range(3):
            thread = threading.Thread(target=enqueue_messages, args=(i * 10, 5))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verify thread safety
        assert len(errors) == 0
        assert queue.size() == 15  # 3 threads × 5 messages
        assert all(results)  # All enqueue operations succeeded
    
    def test_message_queue_metrics_tracking_tdd(self):
        """RED: Test comprehensive metrics tracking - TDD First"""
        queue = PersistentMessageQueue("test_queue")
        
        # Create test messages
        messages = [
            Message(f"msg_{i}", f"Message {i}", MessagePriority.NORMAL, "agent", "target")
            for i in range(3)
        ]
        
        # Expected behavior: metrics track all operations
        for msg in messages:
            queue.enqueue(msg)
        
        assert queue._metrics['enqueue_count'] == 3
        assert queue._metrics['current_size'] == 3
        
        # Dequeue messages
        for _ in range(2):
            msg = queue.dequeue()
            queue.ack_message(msg.id)
        
        assert queue._metrics['dequeue_count'] == 2
        assert queue._metrics['ack_count'] == 2
        assert queue._metrics['current_size'] == 1
        
        # Get comprehensive metrics
        metrics = queue.get_metrics()
        expected_metrics = {
            'enqueue_count', 'dequeue_count', 'ack_count', 
            'error_count', 'current_size', 'queue_name'
        }
        assert all(key in metrics for key in expected_metrics)


class TestDecisionCoreTDD:
    """
    TDD Test Suite for Decision Making Engine
    
    CRITICAL COMPONENT: No existing tests found
    TDD Status: RED - Writing complete test coverage first
    """
    
    def test_decision_engine_initialization_tdd(self):
        """RED: Test decision engine initialization - TDD First"""
        # Import will be available after implementation
        from src.core.decision.decision_core import DecisionMakingEngine
        
        engine = DecisionMakingEngine()
        
        assert engine.workspace_path.exists()
        assert len(engine.pending_decisions) == 0
        assert len(engine.completed_decisions) == 0
        assert len(engine.decision_algorithms) > 0
        assert engine.logger is not None
    
    def test_decision_request_processing_tdd(self):
        """RED: Test decision request processing - TDD First"""
        from src.core.decision.decision_core import DecisionMakingEngine
        from src.core.decision.decision_types import DecisionRequest, DecisionType
        
        engine = DecisionMakingEngine()
        
        # Create decision request
        request = DecisionRequest(
            id="decision_001",
            type=DecisionType.TASK_ASSIGNMENT,
            context={"agent_id": "agent_1", "task_type": "coordination"},
            requester="coordinator_agent",
            priority=1
        )
        
        # Expected behavior: request processed successfully
        result = engine.process_decision_request(request)
        assert result is not None
        assert result.request_id == "decision_001"
        assert result.status == "completed"
        assert request.id in engine.completed_decisions
    
    def test_collaborative_decision_making_tdd(self):
        """RED: Test collaborative decision algorithms - TDD First"""
        from src.core.decision.decision_core import DecisionMakingEngine
        from src.core.decision.decision_types import DecisionType, DecisionContext
        
        engine = DecisionMakingEngine()
        
        # Expected behavior: collaborative decision with multiple agents
        context = DecisionContext(
            participating_agents=["agent_1", "agent_2", "agent_3"],
            decision_data={"resource_allocation": "high_priority_task"},
            consensus_threshold=0.67
        )
        
        result = engine.make_collaborative_decision(
            DecisionType.RESOURCE_ALLOCATION, 
            context
        )
        
        assert result is not None
        assert result.consensus_reached is True
        assert len(result.participating_agents) == 3
        assert result.decision_confidence >= 0.67


class TestSwarmCoordinationTDD:
    """
    TDD Test Suite for Swarm Coordination System
    
    Component: External SWARM integration (283 lines)
    TDD Status: RED - Writing integration tests first
    """
    
    def test_swarm_integration_status_tdd(self):
        """RED: Test SWARM integration status management - TDD First"""
        from src.core.swarm_coordination_system import SwarmCoordinationSystem
        
        coordinator = SwarmCoordinationSystem()
        
        # Expected behavior: proper status management
        assert coordinator.get_integration_status() in [
            "unavailable", "initializing", "active", "error"
        ]
        
        # Expected behavior: can initialize if SWARM available
        if coordinator.swarm_available:
            result = coordinator.initialize_swarm_integration()
            assert result is True
            assert coordinator.get_integration_status() == "active"
    
    def test_swarm_agent_coordination_tdd(self):
        """RED: Test agent coordination through SWARM - TDD First"""
        from src.core.swarm_coordination_system import SwarmCoordinationSystem
        
        coordinator = SwarmCoordinationSystem()
        
        if coordinator.swarm_available:
            # Expected behavior: successful agent registration
            agent_info = {
                "id": "test_agent_001",
                "capabilities": ["coordination", "task_management"],
                "status": "active"
            }
            
            result = coordinator.register_agent(agent_info)
            assert result is True
            
            # Expected behavior: agent coordination works
            coordination_result = coordinator.coordinate_agents([
                "test_agent_001", "test_agent_002"
            ], task_type="collaborative_decision")
            
            assert coordination_result is not None
            assert coordination_result['status'] == 'coordinated'