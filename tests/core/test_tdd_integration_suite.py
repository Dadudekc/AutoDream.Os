"""
TDD Integration Test Suite - Agent Cellphone V2 
==============================================

PHASE 2: TDD Integration Testing - Red → Green → Refactor
Comprehensive integration tests for all TDD refactored components

Components Under Test:
- Message Queue System (587 lines)
- Decision Making Engine (279 lines) 
- Swarm Coordination System (283 lines)

TDD Status: RED - Integration tests first, system integration follows
"""

import pytest
import asyncio
import json

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

# Import TDD components (will fail initially - RED phase)
try:
    from src.core.messaging.message_queue import PersistentMessageQueue
    from src.core.messaging.message_types import Message, MessagePriority, MessageStatus
    from src.core.decision.decision_core import DecisionMakingEngine
    from src.core.decision.decision_types import DecisionRequest, DecisionType
    from src.core.swarm_coordination_system import SwarmCoordinationSystem
    TDD_IMPORTS_AVAILABLE = True
except ImportError as e:
    TDD_IMPORTS_AVAILABLE = False
    IMPORT_ERROR = str(e)


class TestTDDSystemIntegration:
    """
    TDD Integration Test Suite
    
    Tests the complete integrated system after TDD refactoring:
    1. Message Queue ↔ Decision Engine
    2. Decision Engine ↔ Swarm Coordination  
    3. Swarm Coordination ↔ Message Queue
    4. Complete System Workflow
    """
    
    @pytest.fixture
    def tdd_system_setup(self):
        """Setup integrated TDD system components"""
        if not TDD_IMPORTS_AVAILABLE:
            pytest.skip(f"TDD components not yet implemented: {IMPORT_ERROR}")
        
        # Initialize TDD components
        message_queue = PersistentMessageQueue("integration_queue")
        decision_engine = DecisionMakingEngine()
        swarm_coordinator = SwarmCoordinationSystem()
        
        return {
            'message_queue': message_queue,
            'decision_engine': decision_engine,
            'swarm_coordinator': swarm_coordinator
        }
    
    def test_message_queue_decision_integration_tdd(self, tdd_system_setup):
        """RED: Test Message Queue → Decision Engine integration"""
        queue = tdd_system_setup['message_queue']
        engine = tdd_system_setup['decision_engine']
        
        # Create decision request message
        decision_message = Message(
            id="decision_msg_001",
            content=json.dumps({
                "type": "decision_request",
                "decision_type": "TASK_ASSIGNMENT",
                "context": {"agent_id": "agent_1", "task": "coordination"}
            }),
            priority=MessagePriority.HIGH,
            sender="coordinator_agent",
            recipient="decision_engine"
        )
        
        # Expected behavior: message queue feeds decision engine
        queue.enqueue(decision_message)
        received_message = queue.dequeue()
        
        # Process message through decision engine
        decision_request = DecisionRequest.from_message(received_message)
        result = engine.process_decision_request(decision_request)
        
        assert result is not None
        assert result.request_id == decision_request.id
        assert result.status in ["completed", "processing"]
        
        # Expected behavior: result flows back through queue
        result_message = result.to_message()
        queue.enqueue(result_message)
        queue.ack_message(received_message.id)
        
        assert queue._metrics['ack_count'] > 0
    
    def test_decision_swarm_integration_tdd(self, tdd_system_setup):
        """RED: Test Decision Engine → Swarm Coordination integration"""
        engine = tdd_system_setup['decision_engine']
        coordinator = tdd_system_setup['swarm_coordinator']
        
        # Create multi-agent decision requiring swarm coordination
        decision_request = DecisionRequest(
            id="swarm_decision_001",
            type=DecisionType.MULTI_AGENT_COORDINATION,
            context={
                "participating_agents": ["agent_1", "agent_2", "agent_3"],
                "coordination_type": "consensus_building",
                "task_distribution": True
            },
            requester="system_coordinator",
            priority=1
        )
        
        # Expected behavior: decision engine delegates to swarm coordinator
        if coordinator.swarm_available:
            result = engine.process_decision_with_swarm_coordination(decision_request)
            
            assert result is not None
            assert result.coordination_status == "completed"
            assert len(result.participating_agents) >= 3
            assert result.consensus_reached is True
        else:
            # Fallback behavior when SWARM unavailable
            result = engine.process_decision_request(decision_request)
            assert result.fallback_mode is True
    
    def test_swarm_message_queue_integration_tdd(self, tdd_system_setup):
        """RED: Test Swarm Coordination → Message Queue integration"""
        coordinator = tdd_system_setup['swarm_coordinator']
        queue = tdd_system_setup['message_queue']
        
        if coordinator.swarm_available:
            # Register agents in swarm
            agents = ["agent_1", "agent_2", "agent_3"]
            for agent_id in agents:
                agent_info = {
                    "id": agent_id,
                    "capabilities": ["messaging", "coordination"],
                    "message_queue": queue.name
                }
                coordinator.register_agent(agent_info)
            
            # Expected behavior: swarm coordinates message distribution
            coordination_task = {
                "type": "message_broadcast",
                "message": "System coordination update",
                "priority": "HIGH",
                "target_agents": agents
            }
            
            result = coordinator.coordinate_message_distribution(coordination_task)
            
            assert result is not None
            assert result['messages_queued'] == len(agents)
            assert queue.size() >= len(agents)
            
            # Verify messages in queue
            queued_messages = []
            while not queue.is_empty():
                msg = queue.dequeue()
                queued_messages.append(msg)
            
            assert len(queued_messages) == len(agents)
            assert all(msg.priority == MessagePriority.HIGH for msg in queued_messages)
    
    def test_complete_tdd_system_workflow_tdd(self, tdd_system_setup):
        """RED: Test complete integrated TDD system workflow"""
        queue = tdd_system_setup['message_queue']
        engine = tdd_system_setup['decision_engine']
        coordinator = tdd_system_setup['swarm_coordinator']
        
        # WORKFLOW: Incoming request → Queue → Decision → Swarm → Response → Queue
        
        # Step 1: System receives coordination request
        initial_request = Message(
            id="workflow_001",
            content=json.dumps({
                "type": "system_coordination_request",
                "priority": "CRITICAL",
                "agents_needed": ["agent_1", "agent_2", "agent_3", "agent_4"],
                "task_type": "collaborative_problem_solving",
                "deadline": (datetime.now() + timedelta(hours=1)).isoformat()
            }),
            priority=MessagePriority.CRITICAL,
            sender="external_system",
            recipient="coordination_system"
        )
        
        queue.enqueue(initial_request)
        
        # Step 2: Message processed by decision engine
        received_request = queue.dequeue()
        decision_request = DecisionRequest.from_message(received_request)
        
        # Step 3: Decision engine coordinates with swarm
        if coordinator.swarm_available:
            decision_result = engine.process_decision_with_swarm_coordination(decision_request)
            
            # Step 4: Swarm executes coordination
            coordination_result = coordinator.execute_coordination_plan(decision_result.plan)
            
            # Step 5: Results flow back through system
            response_message = Message(
                id="workflow_response_001",
                content=json.dumps({
                    "status": "completed",
                    "original_request_id": initial_request.id,
                    "agents_coordinated": coordination_result['agents'],
                    "execution_time": coordination_result['duration'],
                    "success": coordination_result['success']
                }),
                priority=MessagePriority.NORMAL,
                sender="coordination_system",
                recipient="external_system"
            )
            
            queue.enqueue(response_message)
            
            # Verify complete workflow
            assert decision_result.status == "completed"
            assert coordination_result['success'] is True
            assert len(coordination_result['agents']) >= 4
            
            # Verify response in queue
            response = queue.dequeue()
            response_data = json.loads(response.content)
            assert response_data['status'] == "completed"
            assert response_data['original_request_id'] == initial_request.id
        
        else:
            # Test fallback workflow when SWARM unavailable
            decision_result = engine.process_decision_request(decision_request)
            assert decision_result.fallback_mode is True
            
            fallback_response = Message(
                id="workflow_fallback_001",
                content=json.dumps({
                    "status": "fallback_completed",
                    "original_request_id": initial_request.id,
                    "fallback_reason": "SWARM_UNAVAILABLE"
                }),
                priority=MessagePriority.NORMAL,
                sender="coordination_system",
                recipient="external_system"
            )
            
            queue.enqueue(fallback_response)
            response = queue.dequeue()
            response_data = json.loads(response.content)
            assert response_data['status'] == "fallback_completed"


class TestTDDPerformanceIntegration:
    """
    TDD Performance Integration Tests
    
    Tests system performance after TDD refactoring
    """
    
    @pytest.fixture
    def performance_system_setup(self):
        """Setup system for performance testing"""
        if not TDD_IMPORTS_AVAILABLE:
            pytest.skip(f"TDD components not yet implemented: {IMPORT_ERROR}")
        
        # Large-capacity components for performance testing
        message_queue = PersistentMessageQueue("perf_queue", max_size=10000)
        decision_engine = DecisionMakingEngine()
        swarm_coordinator = SwarmCoordinationSystem()
        
        return {
            'message_queue': message_queue,
            'decision_engine': decision_engine,
            'swarm_coordinator': swarm_coordinator
        }
    
    def test_high_throughput_message_processing_tdd(self, performance_system_setup):
        """RED: Test high-throughput message processing performance"""
        queue = performance_system_setup['message_queue']
        engine = performance_system_setup['decision_engine']
        
        # Generate high-volume message load
        messages = [
            Message(
                id=f"perf_msg_{i}",
                content=json.dumps({"type": "performance_test", "sequence": i}),
                priority=MessagePriority.NORMAL,
                sender=f"agent_{i % 10}",
                recipient="performance_processor"
            )
            for i in range(1000)
        ]
        
        # Expected behavior: system handles high throughput efficiently
        start_time = datetime.now()
        
        # Enqueue all messages
        for msg in messages:
            queue.enqueue(msg)
        
        # Process messages through decision engine
        processed_count = 0
        while not queue.is_empty() and processed_count < 1000:
            msg = queue.dequeue()
            # Simulate processing
            decision_request = DecisionRequest(
                id=f"perf_decision_{processed_count}",
                type=DecisionType.TASK_PROCESSING,
                context=json.loads(msg.content),
                requester=msg.sender,
                priority=1
            )
            result = engine.process_decision_request(decision_request)
            queue.ack_message(msg.id)
            processed_count += 1
        
        end_time = datetime.now()
        processing_duration = (end_time - start_time).total_seconds()
        
        # Performance assertions
        assert processed_count == 1000
        assert processing_duration < 30  # Should process 1000 messages in under 30 seconds
        assert queue._metrics['enqueue_count'] == 1000
        assert queue._metrics['dequeue_count'] == 1000
        assert queue._metrics['ack_count'] == 1000
        
        # Throughput calculation
        throughput = processed_count / processing_duration
        assert throughput > 33  # At least 33 messages per second
    
    def test_concurrent_system_operations_tdd(self, performance_system_setup):
        """RED: Test concurrent operations across all TDD components"""
        import threading
        import concurrent.futures
        
        queue = performance_system_setup['message_queue']
        engine = performance_system_setup['decision_engine']
        coordinator = performance_system_setup['swarm_coordinator']
        
        results = []
        errors = []
        
        def worker_task(worker_id: int):
            """Concurrent worker performing integrated operations"""
            try:
                for i in range(10):
                    # Message operations
                    msg = Message(
                        id=f"concurrent_msg_{worker_id}_{i}",
                        content=json.dumps({"worker": worker_id, "sequence": i}),
                        priority=MessagePriority.NORMAL,
                        sender=f"worker_{worker_id}",
                        recipient="concurrent_processor"
                    )
                    queue.enqueue(msg)
                    
                    # Decision operations
                    decision_request = DecisionRequest(
                        id=f"concurrent_decision_{worker_id}_{i}",
                        type=DecisionType.CONCURRENT_PROCESSING,
                        context={"worker_id": worker_id, "sequence": i},
                        requester=f"worker_{worker_id}",
                        priority=1
                    )
                    decision_result = engine.process_decision_request(decision_request)
                    
                    results.append({
                        'worker_id': worker_id,
                        'sequence': i,
                        'success': True
                    })
                    
            except Exception as e:
                errors.append({'worker_id': worker_id, 'error': str(e)})
        
        # Expected behavior: system handles concurrent load
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(worker_task, i) for i in range(5)]
            concurrent.futures.wait(futures)
        
        # Verify concurrent operations success
        assert len(errors) == 0
        assert len(results) == 50  # 5 workers × 10 operations each
        assert queue.size() >= 50  # All messages queued
        
        # Verify no thread safety issues
        metrics = queue.get_metrics()
        assert metrics['enqueue_count'] >= 50
        assert metrics['error_count'] == 0