from pathlib import Path
import os
import sys

import unittest

from src.core.tasks.execution import TaskExecutor
from src.core.tasks.monitoring import TaskMonitor
from src.core.tasks.recovery import TaskRecovery
from src.core.tasks.scheduler import TaskScheduler, Task, TaskPriority, TaskStatus
from unittest.mock import Mock, MagicMock, patch

#!/usr/bin/env python3
"""
Test Task Modules - Agent Cellphone V2
=====================================

Tests for extracted task management modules.
"""


# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestTaskScheduler(unittest.TestCase):
    """Test TaskScheduler module."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_workspace_manager = Mock()
        self.mock_workspace_manager.get_all_workspaces.return_value = []
        self.scheduler = TaskScheduler(self.mock_workspace_manager)

    @patch("builtins.open")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.mkdir")
    def test_task_creation(self, mock_mkdir, mock_exists, mock_open):
        """Test task creation functionality."""
        # Mock file operations
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = Mock()

        # Mock workspace info
        mock_workspace = Mock()
        mock_workspace.tasks_path = "/tmp/test"
        self.mock_workspace_manager.get_workspace_info.return_value = mock_workspace

        # Test task creation
        task_id = self.scheduler.create_task(
            "Test Task", "Test Description", "Agent-1", "TestAgent", TaskPriority.HIGH
        )

        self.assertIsNotNone(task_id)
        self.assertIn(task_id, self.scheduler.tasks)

    @patch("builtins.open")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.unlink")
    def test_task_assignment(self, mock_unlink, mock_exists, mock_open):
        """Test task assignment functionality."""
        # Mock file operations
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = Mock()

        # Mock workspace info
        mock_workspace = Mock()
        mock_workspace.tasks_path = "/tmp/test"
        self.mock_workspace_manager.get_workspace_info.return_value = mock_workspace

        # Create a task first
        task_id = self.scheduler.create_task(
            "Test Task", "Test Description", "Agent-1", "TestAgent"
        )

        # Test reassignment
        success = self.scheduler.assign_task(task_id, "Agent-2")
        self.assertTrue(success)

        # Verify task was reassigned
        task = self.scheduler.get_task(task_id)
        self.assertEqual(task.assigned_to, "Agent-2")

    @patch("builtins.open")
    @patch("pathlib.Path.exists")
    def test_task_retrieval(self, mock_exists, mock_open):
        """Test task retrieval functionality."""
        # Mock file operations
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = Mock()

        # Mock workspace info
        mock_workspace = Mock()
        mock_workspace.tasks_path = "/tmp/test"
        self.mock_workspace_manager.get_workspace_info.return_value = mock_workspace

        self.scheduler.create_task(
            "Task 1", "Desc 1", "Agent-1", "TestAgent", TaskPriority.HIGH
        )
        self.scheduler.create_task(
            "Task 2", "Desc 2", "Agent-1", "TestAgent", TaskPriority.LOW
        )

        # Test retrieval
        tasks = self.scheduler.get_tasks("Agent-1")
        self.assertEqual(len(tasks), 2)

        # Test priority filtering
        high_priority_tasks = self.scheduler.get_tasks(
            "Agent-1", priority=TaskPriority.HIGH
        )
        self.assertEqual(len(high_priority_tasks), 1)


class TestTaskExecutor(unittest.TestCase):
    """Test TaskExecutor module."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock the autonomous_development imports to avoid dependency issues
        with patch.dict(
            "sys.modules",
            {
                "autonomous_development.core.models": Mock(),
                "autonomous_development.core.enums": Mock(),
            },
        ):
            self.executor = TaskExecutor()

    def test_development_task_creation(self):
        """Test development task creation."""
        # Mock the DevelopmentTask class
        mock_dev_task = Mock()
        mock_dev_task.task_id = "task_0001"

        with patch(
            "src.core.tasks.execution.DevelopmentTask", return_value=mock_dev_task
        ):
            task_id = self.executor.create_task(
                "Test Dev Task",
                "Test Description",
                "medium",  # Use lowercase to match enum values
                "HIGH",
                2.0,
                ["python", "testing"],
            )

            self.assertIsNotNone(task_id)
            self.assertIn(task_id, self.executor.tasks)

    def test_task_claiming(self):
        """Test task claiming functionality."""
        # Mock the DevelopmentTask class and its methods
        mock_dev_task = Mock()
        mock_dev_task.task_id = "task_0001"
        mock_dev_task.claim.return_value = True
        mock_dev_task.claimed_by = "Agent-1"

        with patch(
            "src.core.tasks.execution.DevelopmentTask", return_value=mock_dev_task
        ):
            # Create a task
            task_id = self.executor.create_task(
                "Test Task",
                "Test Description",
                "medium",  # Use lowercase to match enum values
                "HIGH",
                2.0,
                ["python"],
            )

            # Test claiming
            success = self.executor.claim_task(task_id, "Agent-1")
            self.assertTrue(success)

            # Verify task was claimed
            task = self.executor.get_task(task_id)
            self.assertEqual(task.claimed_by, "Agent-1")

    def test_task_statistics(self):
        """Test task statistics functionality."""
        # Mock the DevelopmentTask class
        mock_dev_task1 = Mock()
        mock_dev_task1.task_id = "task_0001"
        mock_dev_task1.is_available.return_value = True

        mock_dev_task2 = Mock()
        mock_dev_task2.task_id = "task_0002"
        mock_dev_task2.is_available.return_value = True

        with patch(
            "src.core.tasks.execution.DevelopmentTask", return_value=mock_dev_task1
        ):
            # Create some tasks
            self.executor.create_task(
                "Task 1", "Desc 1", "medium", "HIGH", 2.0, ["python"]
            )
            self.executor.create_task(
                "Task 2", "Desc 2", "low", "MEDIUM", 1.0, ["python"]
            )

            # Test statistics - account for the 5 sample tasks created in setUp
            stats = self.executor.get_task_statistics()
            self.assertEqual(stats["total_tasks"], 7)  # 5 sample + 2 created
            self.assertEqual(stats["available_tasks"], 7)


class TestTaskMonitor(unittest.TestCase):
    """Test TaskMonitor module."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_workspace_manager = Mock()
        self.monitor = TaskMonitor(self.mock_workspace_manager)

    @patch("builtins.open")
    @patch("pathlib.Path.exists")
    def test_task_status_update(self, mock_exists, mock_open):
        """Test task status update functionality."""
        # Mock file operations
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = Mock()

        # Create a mock task
        mock_task = Mock()
        mock_task.task_id = "test_task"
        mock_task.assigned_to = "Agent-1"
        mock_task.status = TaskStatus.PENDING

        # Mock workspace
        mock_workspace = Mock()
        mock_workspace.tasks_path = "/tmp/test"
        self.mock_workspace_manager.get_workspace_info.return_value = mock_workspace

        # Load task into monitor
        self.monitor.tasks = {"test_task": mock_task}

        # Test status update
        success = self.monitor.update_task_status("test_task", TaskStatus.IN_PROGRESS)
        self.assertTrue(success)

    def test_task_status_summary(self):
        """Test task status summary functionality."""
        # Create mock tasks with proper status values
        mock_task1 = Mock()
        mock_task1.status = TaskStatus.PENDING
        mock_task1.priority = "high"
        mock_task1.assigned_to = "Agent-1"

        mock_task2 = Mock()
        mock_task2.status = TaskStatus.COMPLETED
        mock_task2.priority = "low"
        mock_task2.assigned_to = "Agent-2"

        self.monitor.tasks = {"task1": mock_task1, "task2": mock_task2}

        # Test summary
        summary = self.monitor.get_task_status_summary()
        self.assertEqual(summary["total_tasks"], 2)
        # Check that the status summary contains the expected counts
        self.assertIn("pending", summary["status_summary"])
        self.assertIn("completed", summary["status_summary"])


class TestTaskRecovery(unittest.TestCase):
    """Test TaskRecovery module."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_workspace_manager = Mock()
        self.recovery = TaskRecovery(self.mock_workspace_manager)

    @patch("builtins.open")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.unlink")
    def test_task_deletion_with_recovery(self, mock_unlink, mock_exists, mock_open):
        """Test task deletion with recovery backup."""
        # Mock file operations
        mock_exists.return_value = True

        # Create a mock task
        mock_task = Mock()
        mock_task.task_id = "test_task"
        mock_task.assigned_to = "Agent-1"

        # Mock workspace
        mock_workspace = Mock()
        mock_workspace.tasks_path = "/tmp/test"
        self.mock_workspace_manager.get_workspace_info.return_value = mock_workspace

        # Load task into recovery
        self.recovery.tasks = {"test_task": mock_task}

        # Test deletion
        success = self.recovery.delete_task("test_task")
        self.assertTrue(success)

        # Verify task was backed up
        self.assertIn("test_task", self.recovery.deleted_tasks)

    @patch("builtins.open")
    @patch("pathlib.Path.exists")
    def test_task_restoration(self, mock_exists, mock_open):
        """Test task restoration functionality."""
        # Mock file operations
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = Mock()

        # Create a mock task in deleted_tasks
        mock_task = Mock()
        mock_task.task_id = "test_task"
        mock_task.assigned_to = "Agent-1"

        # Mock workspace
        mock_workspace = Mock()
        mock_workspace.tasks_path = "/tmp/test"
        self.mock_workspace_manager.get_workspace_info.return_value = mock_workspace

        self.recovery.deleted_tasks = {"test_task": mock_task}

        # Test restoration
        success = self.recovery.restore_deleted_task("test_task")
        self.assertTrue(success)

        # Verify task was restored
        self.assertIn("test_task", self.recovery.tasks)
        self.assertNotIn("test_task", self.recovery.deleted_tasks)

    @patch("builtins.open")
    @patch("pathlib.Path.exists")
    def test_failed_task_handling(self, mock_exists, mock_open):
        """Test failed task handling."""
        # Mock file operations
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value = Mock()

        # Create a mock task
        mock_task = Mock()
        mock_task.task_id = "test_task"
        mock_task.assigned_to = "Agent-1"
        mock_task.status = TaskStatus.IN_PROGRESS
        mock_task.metadata = {}

        # Mock workspace
        mock_workspace = Mock()
        mock_workspace.tasks_path = "/tmp/test"
        self.mock_workspace_manager.get_workspace_info.return_value = mock_workspace

        self.recovery.tasks = {"test_task": mock_task}

        # Test failed task handling
        success = self.recovery.handle_failed_task("test_task", "Test error")
        self.assertTrue(success)

        # Verify task was marked as failed - compare the status value
        self.assertEqual(mock_task.status.value, TaskStatus.FAILED.value)
        self.assertIn("last_error", mock_task.metadata)


if __name__ == "__main__":
    unittest.main()
