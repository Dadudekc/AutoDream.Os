#!/usr/bin/env python3
"""
FSM Compliance Validation Tests - Comprehensive Testing for FSM Compliance Integration

Tests all FSM compliance integration functionality including workflow creation,
compliance tracking, validation, and system health to ensure Phase 2 workflow
management and compliance tracking works correctly.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import unittest
import time
import json
from unittest.mock import Mock, patch
from datetime import datetime

# Import FSM compliance integration system
from fsm_compliance_integration import (
    FSMComplianceIntegration, create_fsm_compliance_integration, get_integration_status,
    FSMComplianceBridge, ComplianceFSMIntegration
)

# Import FSM system for testing
from fsm_core_v2 import (
    StateDefinition, TransitionDefinition, WorkflowInstance,
    StateStatus, TransitionType, WorkflowPriority, StateHandler, TransitionHandler
)


class MockFSMStateHandler(StateHandler):
    """Mock state handler for FSM testing."""
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed
        self.execution_count = 0
        self.last_context = None
    
    def execute(self, context):
        self.execution_count += 1
        self.last_context = context
        return self.should_succeed


class FSMComplianceIntegrationTest(unittest.TestCase):
    """Comprehensive tests for FSMComplianceIntegration."""
    
    def setUp(self):
        """Set up test environment."""
        self.integration = FSMComplianceIntegration()
        self.task_id = "TASK_1G_FSM_INTEGRATION"
        self.agent_id = "Agent-1"
        self.workflow_name = "FSM Compliance Integration Test"
        self.workflow_priority = WorkflowPriority.NORMAL
        
        # Test FSM components
        self.state_start = StateDefinition(
            name="start",
            description="Starting state",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        self.state_process = StateDefinition(
            name="process",
            description="Processing state",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        self.state_end = StateDefinition(
            name="end",
            description="Ending state",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        
        self.transition_start_process = TransitionDefinition(
            from_state="start", to_state="process", transition_type=TransitionType.AUTOMATIC,
            condition=None, priority=1, timeout_seconds=None, actions=[], metadata={}
        )
        self.transition_process_end = TransitionDefinition(
            from_state="process", to_state="end", transition_type=TransitionType.AUTOMATIC,
            condition=None, priority=1, timeout_seconds=None, actions=[], metadata={}
        )
    
    def tearDown(self):
        """Clean up test environment."""
        # Clean up any created workflows
        if hasattr(self.integration, 'fsm_system') and self.integration.fsm_system:
            for workflow_id in list(self.integration.fsm_system.workflows.keys()):
                try:
                    self.integration.fsm_system.stop_workflow(workflow_id)
                except:
                    pass
    
    def test_system_initialization(self):
        """Test FSM compliance integration initialization."""
        # Check integration status
        self.assertIsNotNone(self.integration.integration_status)
        self.assertIn("fsm_system", self.integration.integration_status)
        self.assertIn("compliance_system", self.integration.integration_status)
        self.assertIn("integration_active", self.integration.integration_status)
        
        # Check data structures
        self.assertIsInstance(self.integration.compliance_workflows, dict)
        self.assertIsInstance(self.integration.fsm_compliance_mapping, dict)
        self.assertIsInstance(self.integration.compliance_fsm_mapping, dict)
        
        # Check system connections
        self.assertIsNotNone(self.integration.fsm_system)
        self.assertIsNotNone(self.integration.compliance_system)
    
    def test_compliance_workflow_creation(self):
        """Test creating a compliance workflow."""
        # Create compliance workflow
        workflow_id = self.integration.create_compliance_workflow(
            self.task_id, self.agent_id, self.workflow_name,
            [self.state_start, self.state_process, self.state_end],
            [self.transition_start_process, self.transition_process_end],
            self.workflow_priority
        )
        
        # Verify workflow created
        self.assertIsNotNone(workflow_id)
        self.assertIn(workflow_id, self.integration.compliance_workflows)
        
        # Verify integration metadata
        workflow_data = self.integration.compliance_workflows[workflow_id]
        self.assertEqual(workflow_data["task_id"], self.task_id)
        self.assertEqual(workflow_data["agent_id"], self.agent_id)
        self.assertEqual(workflow_data["workflow_name"], self.workflow_name)
        self.assertEqual(workflow_data["status"], "integrated")
        
        # Verify mappings - check both directions
        self.assertIn(workflow_id, self.integration.fsm_compliance_mapping)
        compliance_task_id = self.integration.fsm_compliance_mapping[workflow_id]
        self.assertIn(compliance_task_id, self.integration.compliance_fsm_mapping)
        self.assertEqual(self.integration.compliance_fsm_mapping[compliance_task_id], workflow_id)
    
    def test_compliance_workflow_start(self):
        """Test starting a compliance workflow."""
        # Create workflow first
        workflow_id = self.integration.create_compliance_workflow(
            self.task_id, self.agent_id, self.workflow_name,
            [self.state_start, self.state_process, self.state_end],
            [self.transition_start_process, self.transition_process_end],
            self.workflow_priority
        )
        
        # Start workflow
        result = self.integration.start_compliance_workflow(workflow_id)
        self.assertTrue(result)
        
        # Verify workflow status updated
        workflow_data = self.integration.compliance_workflows[workflow_id]
        self.assertEqual(workflow_data["status"], "running")
        self.assertIn("started_at", workflow_data)
    
    def test_compliance_progress_tracking(self):
        """Test compliance progress tracking."""
        # Create workflow first
        workflow_id = self.integration.create_compliance_workflow(
            self.task_id, self.agent_id, self.workflow_name,
            [self.state_start, self.state_process, self.state_end],
            [self.transition_start_process, self.transition_process_end],
            self.workflow_priority
        )
        
        # Update progress
        result = self.integration.update_compliance_progress(
            workflow_id, 50.0, "PROCESSING",
            deliverables={"fsm_workflow": "ACTIVE", "validation": "IN_PROGRESS"},
            code_changes=["Updated workflow state"],
            devlog_entries=["Progress update: 50% complete"]
        )
        
        self.assertTrue(result)
        
        # Verify progress updated
        workflow_data = self.integration.compliance_workflows[workflow_id]
        self.assertEqual(workflow_data["current_progress"], 50.0)
        self.assertEqual(workflow_data["current_phase"], "PROCESSING")
        self.assertIn("last_progress_update", workflow_data)
    
    def test_compliance_workflow_validation(self):
        """Test compliance workflow validation."""
        # Create and start workflow
        workflow_id = self.integration.create_compliance_workflow(
            self.task_id, self.agent_id, self.workflow_name,
            [self.state_start, self.state_process, self.state_end],
            [self.transition_start_process, self.transition_process_end],
            self.workflow_priority
        )
        
        self.integration.start_compliance_workflow(workflow_id)
        
        # Validate workflow
        validation_results = self.integration.validate_compliance_workflow(workflow_id)
        
        # Verify validation results
        self.assertIsNotNone(validation_results)
        self.assertIn("workflow_id", validation_results)
        self.assertIn("task_id", validation_results)
        self.assertIn("agent_id", validation_results)
        self.assertIn("checks", validation_results)
        self.assertIn("overall_valid", validation_results)
        
        # Check FSM workflow validation
        fsm_check = validation_results["checks"].get("fsm_workflow")
        self.assertIsNotNone(fsm_check)
        self.assertEqual(fsm_check["status"], "VALID")
        
        # Check compliance tracking validation
        compliance_check = validation_results["checks"].get("compliance_tracking")
        self.assertIsNotNone(compliance_check)
        self.assertEqual(compliance_check["status"], "VALID")
    
    def test_workflow_status_retrieval(self):
        """Test retrieving comprehensive workflow status."""
        # Create and start workflow
        workflow_id = self.integration.create_compliance_workflow(
            self.task_id, self.agent_id, self.workflow_name,
            [self.state_start, self.state_process, self.state_end],
            [self.transition_start_process, self.transition_process_end],
            self.workflow_priority
        )
        
        self.integration.start_compliance_workflow(workflow_id)
        
        # Get workflow status
        status = self.integration.get_compliance_workflow_status(workflow_id)
        
        # Verify status structure
        self.assertIsNotNone(status)
        self.assertEqual(status["fsm_workflow_id"], workflow_id)
        self.assertEqual(status["task_id"], self.task_id)
        self.assertEqual(status["agent_id"], self.agent_id)
        self.assertEqual(status["workflow_name"], self.workflow_name)
        self.assertEqual(status["integration_status"], "running")
        
        # Verify FSM status
        self.assertIsNotNone(status["fsm_status"])
        self.assertIn("current_state", status["fsm_status"])
        self.assertIn("status", status["fsm_status"])
        
        # Verify compliance status
        self.assertIsNotNone(status["compliance_status"])
        self.assertIn("progress_percentage", status["compliance_status"])
        self.assertIn("current_phase", status["compliance_status"])
    
    def test_workflow_listing(self):
        """Test listing compliance workflows."""
        # Create multiple workflows with proper state setup
        # First workflow
        start_state1 = StateDefinition(
            name="start1",
            description="Starting state 1",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        end_state1 = StateDefinition(
            name="end1",
            description="Ending state 1",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        transition1 = TransitionDefinition(
            from_state="start1", to_state="end1", transition_type=TransitionType.AUTOMATIC,
            condition=None, priority=1, timeout_seconds=None, actions=[], metadata={}
        )
        
        workflow1_id = self.integration.create_compliance_workflow(
            "TASK_1", "Agent-1", "Workflow 1",
            [start_state1, end_state1],
            [transition1],
            WorkflowPriority.HIGH
        )
        
        # Second workflow
        start_state2 = StateDefinition(
            name="start2",
            description="Starting state 2",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        end_state2 = StateDefinition(
            name="end2",
            description="Ending state 2",
            entry_actions=[],
            exit_actions=[],
            timeout_seconds=None,
            retry_count=0,
            retry_delay=0.0,
            required_resources=[],
            dependencies=[],
            metadata={}
        )
        transition2 = TransitionDefinition(
            from_state="start2", to_state="end2", transition_type=TransitionType.AUTOMATIC,
            condition=None, priority=1, timeout_seconds=None, actions=[], metadata={}
        )
        
        workflow2_id = self.integration.create_compliance_workflow(
            "TASK_2", "Agent-2", "Workflow 2",
            [start_state2, end_state2],
            [transition2],
            WorkflowPriority.NORMAL
        )
        
        # List all workflows
        all_workflows = self.integration.list_compliance_workflows()
        self.assertEqual(len(all_workflows), 2)
        
        # List workflows by status
        integrated_workflows = self.integration.list_compliance_workflows("integrated")
        self.assertEqual(len(integrated_workflows), 2)
        
        # Verify workflow data
        workflow1_data = next(w for w in all_workflows if w["fsm_workflow_id"] == workflow1_id)
        self.assertEqual(workflow1_data["task_id"], "TASK_1")
        self.assertEqual(workflow1_data["agent_id"], "Agent-1")
        self.assertEqual(workflow1_data["priority"], WorkflowPriority.HIGH.value)
    
    def test_integration_health_monitoring(self):
        """Test integration health monitoring."""
        # Get integration health
        health = self.integration.get_integration_health()
        
        # Verify health structure
        self.assertIn("overall_health", health)
        self.assertIn("fsm_system", health)
        self.assertIn("compliance_system", health)
        self.assertIn("integration", health)
        self.assertIn("last_health_check", health)
        
        # Verify FSM system health
        fsm_health = health["fsm_system"]
        self.assertIn("status", fsm_health)
        self.assertIn("connected", fsm_health)
        self.assertIn("running", fsm_health)
        
        # Verify compliance system health
        compliance_health = health["compliance_system"]
        self.assertIn("status", compliance_health)
        self.assertIn("connected", compliance_health)
        
        # Verify integration health
        integration_health = health["integration"]
        self.assertIn("active", integration_health)
        self.assertIn("total_workflows", integration_health)
        self.assertIn("running_workflows", integration_health)
    
    def test_integration_report_export(self):
        """Test integration report export functionality."""
        # Create a workflow first
        workflow_id = self.integration.create_compliance_workflow(
            self.task_id, self.agent_id, self.workflow_name,
            [self.state_start, self.state_process, self.state_end],
            [self.transition_start_process, self.transition_process_end],
            self.workflow_priority
        )
        
        # Export report
        report = self.integration.export_integration_report()
        self.assertIsNotNone(report)
        
        # Parse report
        report_data = json.loads(report)
        
        # Verify report structure
        self.assertIn("integration_status", report_data)
        self.assertIn("health_status", report_data)
        self.assertIn("compliance_workflows", report_data)
        self.assertIn("mappings", report_data)
        self.assertIn("exported_at", report_data)
        
        # Verify workflows in report
        workflows = report_data["compliance_workflows"]
        self.assertGreater(len(workflows), 0)
        
        # Verify mappings in report
        mappings = report_data["mappings"]
        self.assertIn("fsm_to_compliance", mappings)
        self.assertIn("compliance_to_fsm", mappings)
    
    def test_factory_functions(self):
        """Test factory functions."""
        # Test create function
        integration = create_fsm_compliance_integration()
        self.assertIsInstance(integration, FSMComplianceIntegration)
        
        # Test status function
        status = get_integration_status()
        self.assertIsInstance(status, dict)
        self.assertIn("overall_health", status)
    
    def test_backwards_compatibility(self):
        """Test backwards compatibility aliases."""
        # Test alias imports
        from fsm_compliance_integration import FSMComplianceBridge, ComplianceFSMIntegration
        
        # Verify aliases work
        bridge = FSMComplianceBridge()
        self.assertIsInstance(bridge, FSMComplianceIntegration)
        
        integration = ComplianceFSMIntegration()
        self.assertIsInstance(integration, FSMComplianceIntegration)
    
    def test_error_handling(self):
        """Test error handling and recovery."""
        # Test creating workflow with invalid integration
        with patch.object(self.integration, 'integration_status', {"integration_active": False}):
            workflow_id = self.integration.create_compliance_workflow(
                self.task_id, self.agent_id, self.workflow_name,
                [self.state_start], [], self.workflow_priority
            )
            self.assertIsNone(workflow_id)
        
        # Test starting non-existent workflow
        result = self.integration.start_compliance_workflow("nonexistent")
        self.assertFalse(result)
        
        # Test updating progress for non-existent workflow
        result = self.integration.update_compliance_progress("nonexistent", 50.0, "TESTING")
        self.assertFalse(result)
        
        # Test validating non-existent workflow
        validation = self.integration.validate_compliance_workflow("nonexistent")
        self.assertFalse(validation.get("overall_valid", False))
        self.assertIn("error", validation)
    
    def test_workflow_lifecycle(self):
        """Test complete workflow lifecycle."""
        # Create workflow
        workflow_id = self.integration.create_compliance_workflow(
            self.task_id, self.agent_id, self.workflow_name,
            [self.state_start, self.state_process, self.state_end],
            [self.transition_start_process, self.transition_process_end],
            self.workflow_priority
        )
        
        # Verify initial state
        status = self.integration.get_compliance_workflow_status(workflow_id)
        self.assertEqual(status["integration_status"], "integrated")
        
        # Start workflow
        self.integration.start_compliance_workflow(workflow_id)
        status = self.integration.get_compliance_workflow_status(workflow_id)
        self.assertEqual(status["integration_status"], "running")
        
        # Update progress
        self.integration.update_compliance_progress(workflow_id, 75.0, "NEAR_COMPLETION")
        status = self.integration.get_compliance_workflow_status(workflow_id)
        self.assertEqual(status["current_progress"], 75.0)
        self.assertEqual(status["current_phase"], "NEAR_COMPLETION")
        
        # Validate workflow
        validation = self.integration.validate_compliance_workflow(workflow_id)
        self.assertTrue(validation["overall_valid"])
        
        # Final status check
        final_status = self.integration.get_compliance_workflow_status(workflow_id)
        self.assertIn("current_progress", final_status)
        self.assertIn("current_phase", final_status)


class FSMComplianceIntegrationPerformanceTest(unittest.TestCase):
    """Performance tests for FSM compliance integration."""
    
    def setUp(self):
        """Set up performance test environment."""
        self.integration = FSMComplianceIntegration()
    
    def tearDown(self):
        """Clean up performance test environment."""
        # Clean up workflows
        if hasattr(self.integration, 'fsm_system') and self.integration.fsm_system:
            for workflow_id in list(self.integration.fsm_system.workflows.keys()):
                try:
                    self.integration.fsm_system.stop_workflow(workflow_id)
                except:
                    pass
    
    def test_bulk_workflow_creation(self):
        """Test creating many workflows quickly."""
        start_time = time.time()
        
        # Create 10 workflows
        workflow_ids = []
        for i in range(10):
            state = StateDefinition(
                name=f"state_{i}",
                description=f"State {i}",
                entry_actions=[],
                exit_actions=[],
                timeout_seconds=None,
                retry_count=0,
                retry_delay=0.0,
                required_resources=[],
                dependencies=[],
                metadata={}
            )
            workflow_id = self.integration.create_compliance_workflow(
                f"TASK_{i}", f"Agent_{i}", f"Workflow_{i}",
                [state],
                [],
                WorkflowPriority.NORMAL
            )
            workflow_ids.append(workflow_id)
        
        creation_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(creation_time, 2.0)
        self.assertEqual(len(workflow_ids), 10)
        
        # Verify all workflows created
        for workflow_id in workflow_ids:
            self.assertIsNotNone(workflow_id)
            self.assertIn(workflow_id, self.integration.compliance_workflows)
    
    def test_concurrent_operations(self):
        """Test concurrent workflow operations."""
        # Create workflows
        workflow_ids = []
        for i in range(5):
            state = StateDefinition(
                name=f"state_{i}",
                description=f"State {i}",
                entry_actions=[],
                exit_actions=[],
                timeout_seconds=None,
                retry_count=0,
                retry_delay=0.0,
                required_resources=[],
                dependencies=[],
                metadata={}
            )
            workflow_id = self.integration.create_compliance_workflow(
                f"TASK_{i}", f"Agent_{i}", f"Workflow_{i}",
                [state],
                [],
                WorkflowPriority.NORMAL
            )
            workflow_ids.append(workflow_id)
        
        # Perform concurrent operations
        start_time = time.time()
        
        # Start all workflows
        for workflow_id in workflow_ids:
            self.integration.start_compliance_workflow(workflow_id)
        
        # Update progress for all workflows
        for i, workflow_id in enumerate(workflow_ids):
            self.integration.update_compliance_progress(workflow_id, 50.0 + i, f"PHASE_{i}")
        
        # Get status for all workflows
        for workflow_id in workflow_ids:
            self.integration.get_compliance_workflow_status(workflow_id)
        
        operation_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(operation_time, 1.0)
        
        # Verify all operations completed
        for workflow_id in workflow_ids:
            status = self.integration.get_compliance_workflow_status(workflow_id)
            self.assertEqual(status["integration_status"], "running")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
