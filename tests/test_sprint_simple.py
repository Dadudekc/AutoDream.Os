#!/usr/bin/env python3
"""
Simple Sprint Test - Agent Cellphone V2
======================================

Simple test of sprint services without complex imports.
"""

import unittest
import tempfile
import shutil

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
import sys
import os

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import sprint services directly
sys.path.insert(0, str(src_path / "services"))
from sprint_management_service import SprintManagementService, Sprint, SprintStatus
from sprint_workflow_service import SprintWorkflowService, WorkflowStage

from .utils.mock_managers import MockWorkspaceManager, MockTaskManager


class TestSprintServicesSimple(unittest.TestCase):
    """Test sprint services with mock dependencies."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace_manager = MockWorkspaceManager(self.test_dir)
        self.task_manager = MockTaskManager()

        # Initialize sprint services
        self.sprint_manager = SprintManagementService(
            self.workspace_manager, self.task_manager
        )
        self.workflow_service = SprintWorkflowService(
            self.sprint_manager, self.task_manager
        )

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def test_sprint_creation(self):
        """Test sprint creation."""
        sprint = self.sprint_manager.create_sprint(
            name="Test Sprint",
            description="Test sprint for integration testing",
            duration_days=14,
        )

        self.assertIsNotNone(sprint)
        self.assertEqual(sprint.name, "Test Sprint")
        self.assertEqual(sprint.max_tasks, 10)
        self.assertEqual(len(sprint.tasks), 0)
        self.assertEqual(sprint.status, SprintStatus.PLANNING)

    def test_10_task_limit(self):
        """Test 10-task limit enforcement."""
        sprint = self.sprint_manager.create_sprint("Limit Test", "Test limit")

        # Add 10 tasks (should succeed)
        for i in range(10):
            success = self.sprint_manager.add_task_to_sprint(
                sprint.sprint_id, f"task_{i}"
            )
            self.assertTrue(success)

        # Try to add 11th task (should fail)
        success = self.sprint_manager.add_task_to_sprint(sprint.sprint_id, "task_11")
        self.assertFalse(success)

        # Verify only 10 tasks
        self.assertEqual(len(sprint.tasks), 10)

    def test_sprint_workflow(self):
        """Test sprint workflow stages."""
        sprint = self.sprint_manager.create_sprint("Workflow Test", "Test workflow")

        # Start planning
        workflow = self.workflow_service.start_sprint_planning(sprint.sprint_id)
        self.assertEqual(workflow.stage, WorkflowStage.SPRINT_PLANNING)

        # Plan tasks
        task_ids = ["task1", "task2", "task3"]
        success = self.workflow_service.plan_sprint_tasks(sprint.sprint_id, task_ids)
        self.assertTrue(success)
        self.assertEqual(workflow.stage, WorkflowStage.TASK_ESTIMATION)

    def test_sprint_persistence(self):
        """Test sprint data persistence."""
        sprint = self.sprint_manager.create_sprint(
            "Persistence Test", "Test persistence"
        )

        # Check that sprint file exists
        sprints_path = self.workspace_manager.get_sprints_path()
        sprint_files = list(sprints_path.glob("*.json"))
        self.assertGreater(len(sprint_files), 0)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
