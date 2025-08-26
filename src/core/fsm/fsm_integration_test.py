#!/usr/bin/env python3
"""
FSM Integration Tests - Comprehensive Testing for FSM Core V2

Tests all FSM functionality including state management, transitions, workflows,
and system operations to ensure Phase 2 workflow management works correctly.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import unittest
import time
import json
from unittest.mock import Mock, patch
from datetime import datetime

# Import FSM system
from fsm_core import (
    FSMCore as FSMCoreV2,
    StateDefinition,
    TransitionDefinition,
    WorkflowInstance,
    StateStatus,
    TransitionType,
    WorkflowPriority,
    StateHandler,
    TransitionHandler,
    StateExecutionResult,
)


class MockStateHandler(StateHandler):
    """Mock state handler for testing."""
    
    def __init__(self, should_succeed: bool = True, execution_time: float = 0.1):
        self.should_succeed = should_succeed
        self.execution_time = execution_time
    
    def execute(self, context):
        time.sleep(self.execution_time)
        
        if self.should_succeed:
            return StateExecutionResult(
                state_name=context.get("current_state", "unknown"),
                execution_time=self.execution_time,
                status=StateStatus.COMPLETED,
                output={"result": "success", "context": context},
                error_message=None,
                metadata={"test": True},
                timestamp=datetime.now()
            )
        else:
            return StateExecutionResult(
                state_name=context.get("current_state", "unknown"),
                execution_time=self.execution_time,
                status=StateStatus.FAILED,
                output={},
                error_message="Mock failure for testing",
                metadata={"test": True},
                timestamp=datetime.now()
            )
    
    def can_transition(self, context):
        return True


class MockTransitionHandler(TransitionHandler):
    """Mock transition handler for testing."""
    
    def __init__(self, should_allow: bool = True):
        self.should_allow = should_allow
    
    def evaluate(self, context):
        return self.should_allow
    
    def execute(self, context):
        return {"transition_executed": True, "context": context}


class FSMIntegrationTest(unittest.TestCase):
    """Comprehensive FSM integration tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.fsm = FSMCoreV2()
        self.fsm.start_system()
        
        # Create test states
        self.start_state = StateDefinition(
            name="start",
            description="Starting state",
            entry_actions=["log_start"],
            exit_actions=["log_exit"],
            timeout_seconds=10.0,
            retry_count=2,
            retry_delay=1.0,
            required_resources=[],
            dependencies=[],
            metadata={"test": True}
        )
        
        self.process_state = StateDefinition(
            name="process",
            description="Processing state",
            entry_actions=["begin_processing"],
            exit_actions=["end_processing"],
            timeout_seconds=30.0,
            retry_count=3,
            retry_delay=2.0,
            required_resources=["cpu", "memory"],
            dependencies=["start"],
            metadata={"test": True}
        )
        
        self.complete_state = StateDefinition(
            name="complete",
            description="Completion state",
            entry_actions=["finalize"],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=["process"],
            metadata={"test": True}
        )
        
        # Add states to FSM
        self.fsm.add_state(self.start_state)
        self.fsm.add_state(self.process_state)
        self.fsm.add_state(self.complete_state)
        
        # Create test transitions
        self.start_to_process = TransitionDefinition(
            from_state="start",
            to_state="process",
            transition_type=TransitionType.AUTOMATIC,
            condition=None,
            priority=1,
            timeout_seconds=5.0,
            actions=["validate_start"],
            metadata={"test": True}
        )
        
        self.process_to_complete = TransitionDefinition(
            from_state="process",
            to_state="complete",
            transition_type=TransitionType.CONDITIONAL,
            condition="status==success",
            priority=1,
            timeout_seconds=5.0,
            actions=["validate_process"],
            metadata={"test": True}
        )
        
        # Add transitions to FSM
        self.fsm.add_transition(self.start_to_process)
        self.fsm.add_transition(self.process_to_complete)
    
    def tearDown(self):
        """Clean up test environment."""
        self.fsm.stop_system()
    
    def test_fsm_initialization(self):
        """Test FSM system initialization."""
        self.assertTrue(self.fsm.is_running)
        self.assertEqual(len(self.fsm.states), 3)
        self.assertEqual(len(self.fsm.transitions), 2)
        self.assertEqual(self.fsm.max_concurrent_workflows, 10)
    
    def test_state_management(self):
        """Test state addition, removal, and retrieval."""
        # Test state addition
        self.assertTrue("start" in self.fsm.states)
        self.assertTrue("process" in self.fsm.states)
        self.assertTrue("complete" in self.fsm.states)
        
        # Test state retrieval
        start_state = self.fsm.get_state("start")
        self.assertEqual(start_state.name, "start")
        self.assertEqual(start_state.description, "Starting state")
        
        # Test state listing
        states = self.fsm.list_states()
        self.assertEqual(len(states), 3)
        self.assertIn("start", states)
        self.assertIn("process", states)
        self.assertIn("complete", states)
    
    def test_transition_management(self):
        """Test transition addition, removal, and retrieval."""
        # Test transition addition
        start_transitions = self.fsm.get_transitions("start")
        self.assertEqual(len(start_transitions), 1)
        self.assertEqual(start_transitions[0].to_state, "process")
        
        # Test transition retrieval
        transitions = self.fsm.get_transitions("process")
        self.assertEqual(len(transitions), 1)
        self.assertEqual(transitions[0].to_state, "complete")
        
        # Test available transitions
        context = {"status": "success"}
        available = self.fsm.get_available_transitions("start", context)
        self.assertEqual(len(available), 1)
        self.assertEqual(available[0].to_state, "process")
    
    def test_workflow_creation(self):
        """Test workflow creation and management."""
        # Create workflow
        workflow_id = self.fsm.create_workflow(
            workflow_name="test_workflow",
            initial_state="start",
            priority=WorkflowPriority.HIGH,
            metadata={"test": True}
        )
        
        self.assertIsNotNone(workflow_id)
        self.assertTrue(workflow_id in self.fsm.workflows)
        
        # Get workflow
        workflow = self.fsm.get_workflow(workflow_id)
        self.assertIsNotNone(workflow)
        self.assertEqual(workflow.workflow_name, "test_workflow")
        self.assertEqual(workflow.current_state, "start")
        self.assertEqual(workflow.priority, WorkflowPriority.HIGH)
        self.assertEqual(workflow.status, StateStatus.PENDING)
    
    def test_workflow_execution(self):
        """Test workflow execution flow."""
        # Create and start workflow
        workflow_id = self.fsm.create_workflow("test_execution", "start")
        self.assertTrue(self.fsm.start_workflow(workflow_id))
        
        # Wait for execution
        time.sleep(2)
        
        # Check workflow status
        workflow = self.fsm.get_workflow(workflow_id)
        self.assertIsNotNone(workflow)
        
        # Should have moved to process state
        self.assertEqual(workflow.current_state, "process")
        self.assertEqual(workflow.status, StateStatus.ACTIVE)
    
    def test_conditional_transitions(self):
        """Test conditional transition evaluation."""
        # Test condition evaluation
        context_success = {"status": "success"}
        context_failure = {"status": "failure"}
        
        # Should allow transition with success status
        available_success = self.fsm.get_available_transitions("process", context_success)
        self.assertEqual(len(available_success), 1)
        
        # Should not allow transition with failure status
        available_failure = self.fsm.get_available_transitions("process", context_failure)
        self.assertEqual(len(available_failure), 0)
    
    def test_workflow_timeout(self):
        """Test workflow timeout handling."""
        # Create state with short timeout
        timeout_state = StateDefinition(
            name="timeout_test",
            description="Timeout test state",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=0.1,  # Very short timeout
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={"test": True}
        )
        
        self.fsm.add_state(timeout_state)
        
        # Create workflow with timeout state
        workflow_id = self.fsm.create_workflow("timeout_test", "timeout_test")
        self.assertTrue(self.fsm.start_workflow(workflow_id))
        
        # Wait for timeout
        time.sleep(1)
        
        # Check workflow status
        workflow = self.fsm.get_workflow(workflow_id)
        self.assertEqual(workflow.status, StateStatus.TIMEOUT)
    
    def test_workflow_retry(self):
        """Test workflow retry mechanism."""
        # Create failing state handler
        failing_handler = MockStateHandler(should_succeed=False)
        self.fsm.state_handlers["start"] = failing_handler
        
        # Create workflow
        workflow_id = self.fsm.create_workflow("retry_test", "start")
        self.assertTrue(self.fsm.start_workflow(workflow_id))
        
        # Wait for retries
        time.sleep(5)
        
        # Check workflow status
        workflow = self.fsm.get_workflow(workflow_id)
        self.assertEqual(workflow.status, StateStatus.FAILED)
        self.assertEqual(workflow.retry_count, 2)  # Max retries reached
    
    def test_concurrent_workflows(self):
        """Test concurrent workflow execution."""
        # Create multiple workflows
        workflow_ids = []
        for i in range(5):
            workflow_id = self.fsm.create_workflow(f"concurrent_{i}", "start")
            workflow_ids.append(workflow_id)
        
        # Start all workflows
        for workflow_id in workflow_ids:
            self.assertTrue(self.fsm.start_workflow(workflow_id))
        
        # Wait for execution
        time.sleep(3)
        
        # Check active workflows
        active_workflows = self.fsm.list_workflows(StateStatus.ACTIVE)
        self.assertLessEqual(len(active_workflows), self.fsm.max_concurrent_workflows)
    
    def test_system_statistics(self):
        """Test system statistics collection."""
        # Create and execute some workflows
        for i in range(3):
            workflow_id = self.fsm.create_workflow(f"stats_test_{i}", "start")
            self.fsm.start_workflow(workflow_id)
        
        # Wait for execution
        time.sleep(3)
        
        # Get system stats
        stats = self.fsm.get_system_stats()
        
        self.assertIn("total_workflows", stats)
        self.assertIn("active_workflows", stats)
        self.assertIn("successful_workflows", stats)
        self.assertIn("failed_workflows", stats)
        self.assertIn("total_state_transitions", stats)
        
        # Verify stats are reasonable
        self.assertGreaterEqual(stats["total_workflows"], 3)
        self.assertGreaterEqual(stats["total_state_transitions"], 0)
    
    def test_workflow_reporting(self):
        """Test workflow report generation."""
        # Create workflow
        workflow_id = self.fsm.create_workflow("report_test", "start")
        self.fsm.start_workflow(workflow_id)
        
        # Wait for execution
        time.sleep(2)
        
        # Generate report
        report = self.fsm.export_workflow_report(workflow_id, "json")
        self.assertIsNotNone(report)
        
        # Parse report
        report_data = json.loads(report)
        self.assertEqual(report_data["workflow_name"], "report_test")
        self.assertIn("current_state", report_data)
        self.assertIn("state_history", report_data)
    
    def test_system_control(self):
        """Test system start/stop functionality."""
        # Stop system
        self.assertTrue(self.fsm.stop_system())
        self.assertFalse(self.fsm.is_running)
        self.assertFalse(self.fsm.monitoring_active)
        
        # Start system again
        self.assertTrue(self.fsm.start_system())
        self.assertTrue(self.fsm.is_running)
        self.assertTrue(self.fsm.monitoring_active)
    
    def test_error_handling(self):
        """Test error handling and recovery."""
        # Test invalid state
        workflow_id = self.fsm.create_workflow("error_test", "invalid_state")
        self.assertIsNone(workflow_id)
        
        # Test invalid transition
        invalid_transition = TransitionDefinition(
            from_state="nonexistent",
            to_state="start",
            transition_type=TransitionType.AUTOMATIC,
            condition=None,
            priority=1,
            timeout_seconds=5.0,
            actions=[],
            metadata={}
        )
        
        self.assertFalse(self.fsm.add_transition(invalid_transition))
    
    def test_metadata_handling(self):
        """Test metadata handling throughout the system."""
        # Create workflow with metadata
        metadata = {"user": "test_user", "priority": "high", "tags": ["test", "integration"]}
        workflow_id = self.fsm.create_workflow("metadata_test", "start", metadata=metadata)
        
        # Verify metadata is stored
        workflow = self.fsm.get_workflow(workflow_id)
        self.assertEqual(workflow.metadata, metadata)
        
        # Verify metadata in context
        context = self.fsm._build_context(workflow)
        self.assertEqual(context["metadata"], metadata)


class FSMPerformanceTest(unittest.TestCase):
    """Performance tests for FSM system."""
    
    def setUp(self):
        """Set up performance test environment."""
        self.fsm = FSMCoreV2()
        self.fsm.start_system()
        
        # Create performance test states
        for i in range(100):
            state = StateDefinition(
                name=f"state_{i}",
                description=f"Performance test state {i}",
                entry_actions=[],
                exit_actions=[],
                timeout_seconds=10.0,
                retry_count=1,
                retry_delay=0.1,
                required_resources=[],
                dependencies=[],
                metadata={"test": True}
            )
            self.fsm.add_state(state)
    
    def tearDown(self):
        """Clean up performance test environment."""
        self.fsm.stop_system()
    
    def test_bulk_workflow_creation(self):
        """Test creating many workflows quickly."""
        start_time = time.time()
        
        workflow_ids = []
        for i in range(50):
            workflow_id = self.fsm.create_workflow(f"bulk_test_{i}", "state_0")
            workflow_ids.append(workflow_id)
        
        creation_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(creation_time, 5.0)
        self.assertEqual(len(workflow_ids), 50)
    
    def test_concurrent_workflow_execution(self):
        """Test executing many workflows concurrently."""
        # Create workflows
        workflow_ids = []
        for i in range(20):
            workflow_id = self.fsm.create_workflow(f"concurrent_perf_{i}", "state_0")
            workflow_ids.append(workflow_id)
        
        # Start all workflows
        start_time = time.time()
        for workflow_id in workflow_ids:
            self.fsm.start_workflow(workflow_id)
        
        # Wait for completion
        time.sleep(10)
        
        execution_time = time.time() - start_time
        
        # Check completion
        completed = 0
        for workflow_id in workflow_ids:
            workflow = self.fsm.get_workflow(workflow_id)
            if workflow.status in [StateStatus.COMPLETED, StateStatus.FAILED]:
                completed += 1
        
        # Should complete most workflows
        self.assertGreaterEqual(completed, 15)
        self.assertLess(execution_time, 15.0)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
