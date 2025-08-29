#!/usr/bin/env python3
"""
Test Task Modules - Agent Cellphone V2
=====================================

Tests for extracted task management modules.
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.core.tasks.executor import TaskExecutor
from src.core.tasks.monitoring import TaskMonitor
from src.core.tasks.recovery import TaskRecovery
from src.core.tasks.scheduler import TaskScheduler, Task, TaskPriority, TaskStatus


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
            "Task 2", "Desc 2", "Agent-2", "TestAgent", TaskPriority.MEDIUM
        )

        # Test retrieval
        tasks = self.scheduler.get_all_tasks()
        self.assertEqual(len(tasks), 2)

        # Test filtering
        high_priority_tasks = self.scheduler.get_tasks_by_priority(TaskPriority.HIGH)
        self.assertEqual(len(high_priority_tasks), 1)
        self.assertEqual(high_priority_tasks[0].title, "Task 1")


class TestTaskExecutor(unittest.TestCase):
    """Test TaskExecutor module."""

    def setUp(self):
        """Set up test fixtures."""
        self.executor = TaskExecutor()

    def test_executor_initialization(self):
        """Test executor initialization."""
        self.assertIsNotNone(self.executor)
        self.assertEqual(self.executor.name, "TaskExecutor")


class TestTaskMonitor(unittest.TestCase):
    """Test TaskMonitor module."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_workspace_manager = Mock()
        self.monitor = TaskMonitor(self.mock_workspace_manager)

    def test_monitor_initialization(self):
        """Test monitor initialization."""
        self.assertIsNotNone(self.monitor)
        self.assertEqual(self.monitor.name, "TaskMonitor")


class TestTaskRecovery(unittest.TestCase):
    """Test TaskRecovery module."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_workspace_manager = Mock()
        self.recovery = TaskRecovery(self.mock_workspace_manager)

    def test_recovery_initialization(self):
        """Test recovery initialization."""
        self.assertIsNotNone(self.recovery)
        self.assertEqual(self.recovery.name, "TaskRecovery")


if __name__ == "__main__":
    unittest.main()
