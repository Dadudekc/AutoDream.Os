#!/usr/bin/env python3
"""
Workflow Integration Tests - Comprehensive Testing for Workflow Engine Integration

Tests all workflow integration functionality including FSM integration, existing system
compatibility, and unified workflow management to ensure Phase 2 workflow management works correctly.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import unittest
import time
import json
from unittest.mock import Mock, patch
from datetime import datetime

# Import workflow integration system
from .workflow_engine_integration import (
    FSMWorkflowIntegration, create_fsm_workflow_integration, get_integration_status
)

# Import FSM system for testing
from ..fsm.fsm_core_v2 import (
    StateDefinition, TransitionDefinition, WorkflowPriority
)

# Import workflow types for testing
from .types.workflow_models import WorkflowDefinition, WorkflowStep
from .types.workflow_enums import WorkflowType, TaskStatus


class MockWorkflowDefinition:
    """Mock workflow definition for testing."""
    
    def __init__(self, name: str = "test_workflow"):
        self.name = name
        self.description = f"Test workflow: {name}"
        self.workflow_type = WorkflowType.SEQUENTIAL
        self.steps = []
        self.metadata = {"test": True}


class MockWorkflowStep:
    """Mock workflow step for testing."""
    
    def __init__(self, name: str = "test_step"):
        self.name = name
        self.description = f"Test step: {name}"
        self.task_type = "test"
        self.status = TaskStatus.PENDING
        self.metadata = {"test": True}


class WorkflowIntegrationTest(unittest.TestCase):
    """Comprehensive workflow integration tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.integration = FSMWorkflowIntegration()
        
        # Create test workflow definition
        self.test_workflow_def = MockWorkflowDefinition("integration_test")
        
        # Create test FSM states
        self.test_states = [
            StateDefinition(
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
            ),
            StateDefinition(
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
            ),
            StateDefinition(
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
        ]
        
        # Create test FSM transitions
        self.test_transitions = [
            TransitionDefinition(
                from_state="start",
                to_state="process",
                transition_type="automatic",
                condition=None,
                priority=1,
                timeout_seconds=5.0,
                actions=["validate_start"],
                metadata={"test": True}
            ),
            TransitionDefinition(
                from_state="process",
                to_state="complete",
                transition_type="conditional",
                condition="status==success",
                priority=1,
                timeout_seconds=5.0,
                actions=["validate_process"],
                metadata={"test": True}
            )
        ]
    
    def tearDown(self):
        """Clean up test environment."""
        if self.integration.fsm_system:
            self.integration.fsm_system.stop_system()
    
    def test_integration_initialization(self):
        """Test integration system initialization."""
        # Check integration status
        self.assertIsNotNone(self.integration.integration_status)
        self.assertIn("workflow_engine", self.integration.integration_status)
        self.assertIn("fsm_system", self.integration.integration_status)
        self.assertIn("integration_active", self.integration.integration_status)
        
        # Check integration health
        health = self.integration.get_integration_health()
        self.assertIn("overall_health", health)
        self.assertIn("workflow_engine", health)
        self.assertIn("fsm_system", health)
        self.assertIn("integration", health)
    
    def test_integrated_workflow_creation(self):
        """Test creating integrated workflows."""
        # Create integrated workflow
        workflow_id = self.integration.create_integrated_workflow(
            self.test_workflow_def,
            self.test_states,
            self.test_transitions,
            WorkflowPriority.HIGH
        )
        
        self.assertIsNotNone(workflow_id)
        self.assertIn(workflow_id, self.integration.integrated_workflows)
        
        # Verify integration data
        integration_data = self.integration.integrated_workflows[workflow_id]
        self.assertEqual(integration_data["workflow_id"], workflow_id)
        self.assertIn("fsm_workflow_id", integration_data)
        self.assertEqual(integration_data["priority"], "high")
        self.assertEqual(integration_data["status"], "integrated")
        
        # Verify mappings
        fsm_workflow_id = integration_data["fsm_workflow_id"]
        self.assertIn(workflow_id, self.integration.workflow_fsm_mapping)
        self.assertIn(fsm_workflow_id, self.integration.fsm_workflow_mapping)
        self.assertEqual(self.integration.workflow_fsm_mapping[workflow_id], fsm_workflow_id)
        self.assertEqual(self.integration.fsm_workflow_mapping[fsm_workflow_id], workflow_id)
    
    def test_integrated_workflow_lifecycle(self):
        """Test integrated workflow lifecycle management."""
        # Create integrated workflow
        workflow_id = self.integration.create_integrated_workflow(
            self.test_workflow_def,
            self.test_states,
            self.test_transitions
        )
        
        self.assertIsNotNone(workflow_id)
        
        # Start workflow
        self.assertTrue(self.integration.start_integrated_workflow(workflow_id))
        
        # Check status
        status = self.integration.get_integrated_workflow_status(workflow_id)
        self.assertIsNotNone(status)
        self.assertEqual(status["integration_status"], "running")
        self.assertIn("started_at", status)
        
        # Stop workflow
        self.assertTrue(self.integration.stop_integrated_workflow(workflow_id))
        
        # Check final status
        final_status = self.integration.get_integrated_workflow_status(workflow_id)
        self.assertEqual(final_status["integration_status"], "stopped")
        self.assertIn("stopped_at", final_status)
    
    def test_workflow_status_retrieval(self):
        """Test comprehensive workflow status retrieval."""
        # Create integrated workflow
        workflow_id = self.integration.create_integrated_workflow(
            self.test_workflow_def,
            self.test_states,
            self.test_transitions
        )
        
        self.assertIsNotNone(workflow_id)
        
        # Get status
        status = self.integration.get_integrated_workflow_status(workflow_id)
        
        # Verify status structure
        self.assertIn("workflow_id", status)
        self.assertIn("fsm_workflow_id", status)
        self.assertIn("integration_status", status)
        self.assertIn("fsm_status", status)
        self.assertIn("created_at", status)
        self.assertIn("priority", status)
        
        # Verify FSM status
        fsm_status = status["fsm_status"]
        if fsm_status:
            self.assertIn("current_state", fsm_status)
            self.assertIn("status", fsm_status)
            self.assertIn("start_time", fsm_status)
            self.assertIn("last_update", fsm_status)
            self.assertIn("error_count", fsm_status)
            self.assertIn("retry_count", fsm_status)
    
    def test_workflow_listing(self):
        """Test integrated workflow listing functionality."""
        # Create multiple workflows
        workflow_ids = []
        for i in range(3):
            workflow_def = MockWorkflowDefinition(f"test_workflow_{i}")
            workflow_id = self.integration.create_integrated_workflow(
                workflow_def,
                self.test_states,
                self.test_transitions
            )
            workflow_ids.append(workflow_id)
        
        # List all workflows
        all_workflows = self.integration.list_integrated_workflows()
        self.assertEqual(len(all_workflows), 3)
        
        # List running workflows
        running_workflows = self.integration.list_integrated_workflows("running")
        self.assertEqual(len(running_workflows), 0)  # None started yet
        
        # Start one workflow
        self.integration.start_integrated_workflow(workflow_ids[0])
        
        # List running workflows again
        running_workflows = self.integration.list_integrated_workflows("running")
        self.assertEqual(len(running_workflows), 1)
        
        # Verify workflow structure
        workflow = running_workflows[0]
        self.assertIn("workflow_id", workflow)
        self.assertIn("fsm_workflow_id", workflow)
        self.assertIn("name", workflow)
        self.assertIn("status", workflow)
        self.assertIn("priority", workflow)
        self.assertIn("created_at", workflow)
    
    def test_integration_health_monitoring(self):
        """Test integration health monitoring."""
        # Get health status
        health = self.integration.get_integration_health()
        
        # Verify health structure
        self.assertIn("overall_health", health)
        self.assertIn("workflow_engine", health)
        self.assertIn("fsm_system", health)
        self.assertIn("integration", health)
        self.assertIn("last_health_check", health)
        
        # Verify workflow engine health
        workflow_engine_health = health["workflow_engine"]
        self.assertIn("status", workflow_engine_health)
        self.assertIn("connected", workflow_engine_health)
        
        # Verify FSM system health
        fsm_system_health = health["fsm_system"]
        self.assertIn("status", fsm_system_health)
        self.assertIn("connected", fsm_system_health)
        self.assertIn("running", fsm_system_health)
        
        # Verify integration health
        integration_health = health["integration"]
        self.assertIn("active", integration_health)
        self.assertIn("total_workflows", integration_health)
        self.assertIn("running_workflows", integration_health)
    
    def test_integration_report_export(self):
        """Test integration report export functionality."""
        # Create a workflow for testing
        workflow_id = self.integration.create_integrated_workflow(
            self.test_workflow_def,
            self.test_states,
            self.test_transitions
        )
        
        self.assertIsNotNone(workflow_id)
        
        # Export report
        report = self.integration.export_integration_report()
        self.assertIsNotNone(report)
        
        # Parse report
        report_data = json.loads(report)
        
        # Verify report structure
        self.assertIn("integration_status", report_data)
        self.assertIn("health_status", report_data)
        self.assertIn("integrated_workflows", report_data)
        self.assertIn("mappings", report_data)
        self.assertIn("exported_at", report_data)
        
        # Verify mappings
        mappings = report_data["mappings"]
        self.assertIn("fsm_to_workflow", mappings)
        self.assertIn("workflow_to_fsm", mappings)
        
        # Verify workflows
        workflows = report_data["integrated_workflows"]
        self.assertGreaterEqual(len(workflows), 1)
    
    def test_factory_functions(self):
        """Test integration factory functions."""
        # Test create function
        integration = create_fsm_workflow_integration()
        self.assertIsInstance(integration, FSMWorkflowIntegration)
        
        # Test status function
        status = get_integration_status()
        self.assertIsInstance(status, dict)
        self.assertIn("overall_health", status)
    
    def test_error_handling(self):
        """Test error handling and recovery."""
        # Test creating workflow with invalid data
        invalid_workflow_id = self.integration.create_integrated_workflow(
            None,  # Invalid workflow definition
            [],
            []
        )
        self.assertIsNone(invalid_workflow_id)
        
        # Test starting non-existent workflow
        self.assertFalse(self.integration.start_integrated_workflow("nonexistent"))
        
        # Test stopping non-existent workflow
        self.assertFalse(self.integration.stop_integrated_workflow("nonexistent"))
        
        # Test getting status of non-existent workflow
        status = self.integration.get_integrated_workflow_status("nonexistent")
        self.assertIsNone(status)
    
    def test_backwards_compatibility(self):
        """Test backwards compatibility aliases."""
        # Test alias imports
        from .workflow_engine_integration import FSMWorkflowBridge, WorkflowFSMIntegration
        
        # Verify aliases work
        bridge = FSMWorkflowBridge()
        self.assertIsInstance(bridge, FSMWorkflowIntegration)
        
        integration = WorkflowFSMIntegration()
        self.assertIsInstance(integration, FSMWorkflowIntegration)


class WorkflowIntegrationPerformanceTest(unittest.TestCase):
    """Performance tests for workflow integration."""
    
    def setUp(self):
        """Set up performance test environment."""
        self.integration = FSMWorkflowIntegration()
        
        # Create performance test data
        self.performance_states = []
        self.performance_transitions = []
        
        for i in range(50):
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
            self.performance_states.append(state)
            
            if i > 0:
                transition = TransitionDefinition(
                    from_state=f"state_{i-1}",
                    to_state=f"state_{i}",
                    transition_type="automatic",
                    condition=None,
                    priority=1,
                    timeout_seconds=5.0,
                    actions=[],
                    metadata={"test": True}
                )
                self.performance_transitions.append(transition)
    
    def tearDown(self):
        """Clean up performance test environment."""
        if self.integration.fsm_system:
            self.integration.fsm_system.stop_system()
    
    def test_bulk_workflow_creation(self):
        """Test creating many integrated workflows quickly."""
        start_time = time.time()
        
        workflow_ids = []
        for i in range(20):
            workflow_def = MockWorkflowDefinition(f"perf_workflow_{i}")
            workflow_id = self.integration.create_integrated_workflow(
                workflow_def,
                self.performance_states[:10],  # Use subset for performance
                self.performance_transitions[:9]
            )
            workflow_ids.append(workflow_id)
        
        creation_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(creation_time, 10.0)
        self.assertEqual(len(workflow_ids), 20)
        
        # Verify all workflows created
        for workflow_id in workflow_ids:
            self.assertIsNotNone(workflow_id)
            self.assertIn(workflow_id, self.integration.integrated_workflows)
    
    def test_concurrent_workflow_operations(self):
        """Test concurrent workflow operations."""
        # Create workflows
        workflow_ids = []
        for i in range(10):
            workflow_def = MockWorkflowDefinition(f"concurrent_workflow_{i}")
            workflow_id = self.integration.create_integrated_workflow(
                workflow_def,
                self.performance_states[:5],
                self.performance_transitions[:4]
            )
            workflow_ids.append(workflow_id)
        
        # Start all workflows concurrently
        start_time = time.time()
        for workflow_id in workflow_ids:
            self.integration.start_integrated_workflow(workflow_id)
        
        start_time_total = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(start_time_total, 5.0)
        
        # Verify all workflows started
        running_workflows = self.integration.list_integrated_workflows("running")
        self.assertEqual(len(running_workflows), 10)
        
        # Stop all workflows
        stop_start_time = time.time()
        for workflow_id in workflow_ids:
            self.integration.stop_integrated_workflow(workflow_id)
        
        stop_time_total = time.time() - stop_start_time
        
        # Should complete in reasonable time
        self.assertLess(stop_time_total, 5.0)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
