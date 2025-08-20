#!/usr/bin/env python3
"""
Test Sprint Integration - Agent Cellphone V2
===========================================

Tests the integration of ai-task-organizer sprint system with V2.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.services.sprint_management_service import SprintManagementService, Sprint, SprintStatus
from src.services.sprint_workflow_service import SprintWorkflowService, WorkflowStage
from src.core.workspace_manager import WorkspaceManager
from src.core.task_manager import TaskManager


class TestSprintIntegration(unittest.TestCase):
    """Test sprint integration functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.test_dir) / "agent_workspaces"
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize managers
        self.workspace_manager = WorkspaceManager(str(self.workspace_path))
        self.task_manager = TaskManager(self.workspace_manager)
        
        # Initialize sprint services
        self.sprint_manager = SprintManagementService(self.workspace_manager, self.task_manager)
        self.workflow_service = SprintWorkflowService(self.sprint_manager, self.task_manager)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_sprint_creation(self):
        """Test sprint creation with 10-task limit."""
        sprint = self.sprint_manager.create_sprint(
            name="Test Sprint",
            description="Test sprint for integration testing",
            duration_days=14
        )
        
        self.assertIsNotNone(sprint)
        self.assertEqual(sprint.name, "Test Sprint")
        self.assertEqual(sprint.max_tasks, 10)
        self.assertEqual(len(sprint.tasks), 0)
        self.assertEqual(sprint.status, SprintStatus.PLANNING)
    
    def test_task_addition_to_sprint(self):
        """Test adding tasks to sprint with 10-task limit enforcement."""
        # Create sprint
        sprint = self.sprint_manager.create_sprint("Test Sprint", "Test description")
        
        # Add tasks (should succeed)
        task_ids = [f"task_{i}" for i in range(5)]
        for task_id in task_ids:
            success = self.sprint_manager.add_task_to_sprint(sprint.sprint_id, task_id)
            self.assertTrue(success)
        
        # Verify 5 tasks added
        self.assertEqual(len(sprint.tasks), 5)
        
        # Try to add more than 10 tasks (should fail)
        extra_tasks = [f"extra_task_{i}" for i in range(10)]
        for task_id in extra_tasks:
            success = self.sprint_manager.add_task_to_sprint(sprint.sprint_id, task_id)
            if len(sprint.tasks) >= 10:
                self.assertFalse(success)
            else:
                self.assertTrue(success)
        
        # Verify max 10 tasks
        self.assertLessEqual(len(sprint.tasks), 10)
    
    def test_sprint_workflow_stages(self):
        """Test sprint workflow stage transitions."""
        # Create sprint
        sprint = self.sprint_manager.create_sprint("Workflow Test", "Test workflow")
        
        # Start planning workflow
        workflow = self.workflow_service.start_sprint_planning(sprint.sprint_id)
        self.assertEqual(workflow.stage, WorkflowStage.SPRINT_PLANNING)
        
        # Plan tasks
        task_ids = ["task1", "task2", "task3"]
        success = self.workflow_service.plan_sprint_tasks(sprint.sprint_id, task_ids)
        self.assertTrue(success)
        self.assertEqual(workflow.stage, WorkflowStage.TASK_ESTIMATION)
        
        # Start execution
        success = self.workflow_service.start_sprint_execution(sprint.sprint_id)
        self.assertTrue(success)
        self.assertEqual(workflow.stage, WorkflowStage.SPRINT_EXECUTION)
    
    def test_sprint_completion(self):
        """Test sprint completion workflow."""
        # Create and start sprint
        sprint = self.sprint_manager.create_sprint("Completion Test", "Test completion")
        task_ids = ["task1", "task2"]
        self.workflow_service.plan_sprint_tasks(sprint.sprint_id, task_ids)
        self.workflow_service.start_sprint_execution(sprint.sprint_id)
        
        # Complete sprint
        retrospective = self.workflow_service.complete_sprint_workflow(sprint.sprint_id)
        
        self.assertIsNotNone(retrospective)
        self.assertEqual(retrospective['sprint_name'], sprint.name)
        self.assertEqual(retrospective['total_tasks'], 2)
        self.assertIn('success_rate', retrospective)
    
    def test_daily_progress_tracking(self):
        """Test daily progress tracking functionality."""
        # Create and start sprint
        sprint = self.sprint_manager.create_sprint("Progress Test", "Test progress")
        task_ids = ["task1", "task2", "task3"]
        self.workflow_service.plan_sprint_tasks(sprint.sprint_id, task_ids)
        self.workflow_service.start_sprint_execution(sprint.sprint_id)
        
        # Update daily progress
        progress = self.workflow_service.update_daily_progress(sprint.sprint_id)
        
        self.assertIsNotNone(progress)
        self.assertEqual(progress['sprint_name'], sprint.name)
        self.assertEqual(progress['total_tasks'], 3)
        self.assertIn('completion_percentage', progress)
    
    def test_sprint_status_management(self):
        """Test sprint status transitions."""
        # Create sprint
        sprint = self.sprint_manager.create_sprint("Status Test", "Test status")
        
        # Verify initial status
        self.assertEqual(sprint.status, SprintStatus.PLANNING)
        
        # Start sprint
        success = self.sprint_manager.start_sprint(sprint.sprint_id)
        self.assertTrue(success)
        self.assertEqual(sprint.status, SprintStatus.ACTIVE)
        
        # Complete sprint
        success = self.sprint_manager.complete_sprint(sprint.sprint_id)
        self.assertTrue(success)
        self.assertEqual(sprint.status, SprintStatus.COMPLETED)


if __name__ == "__main__":
    unittest.main()
