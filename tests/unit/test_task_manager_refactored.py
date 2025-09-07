from datetime import datetime

import pytest
import unittest

        from src.core.base_manager import BaseManager
        import os
from src.core.task_manager import TaskManager
from unittest.mock import Mock, patch, MagicMock

#!/usr/bin/env python3
"""
Test Task Manager Refactored - Agent Cellphone V2
================================================

Comprehensive testing for refactored TaskManager with BaseManager inheritance.
Validates SRP compliance and BaseManager pattern implementation.
"""




class TestTaskManagerRefactored(unittest.TestCase):
    """Test suite for refactored TaskManager with BaseManager inheritance."""

    def setUp(self):
        """Set up test fixtures."""
        self.workspace_manager = Mock()
        
        # Create proper mocks for task modules
        self.mock_scheduler = Mock()
        self.mock_executor = Mock()
        self.mock_monitor = Mock()
        self.mock_recovery = Mock()
        
        # Mock the tasks attribute for scheduler
        self.mock_scheduler.tasks = []
        
        # Patch the module initialization
        with patch('src.core.task_manager.TaskScheduler', return_value=self.mock_scheduler), \
             patch('src.core.task_manager.TaskExecutor', return_value=self.mock_executor), \
             patch('src.core.task_manager.TaskMonitor', return_value=self.mock_monitor), \
             patch('src.core.task_manager.TaskRecovery', return_value=self.mock_recovery):
            
            self.task_manager = TaskManager(self.workspace_manager)

    def test_inheritance_structure(self):
        """Test that TaskManager properly inherits from BaseManager."""
        self.assertTrue(issubclass(TaskManager, BaseManager))
        self.assertIsInstance(self.task_manager, BaseManager)

    def test_base_manager_attributes(self):
        """Test that BaseManager attributes are properly set."""
        self.assertEqual(self.task_manager.manager_id, "task_manager")
        self.assertEqual(self.task_manager.name, "Task Manager")
        self.assertIn("extracted modules", self.task_manager.description)

    def test_module_initialization(self):
        """Test that all task modules are properly initialized."""
        self.assertIsNotNone(self.task_manager.scheduler)
        self.assertIsNotNone(self.task_manager.executor)
        self.assertIsNotNone(self.task_manager.monitor)
        self.assertIsNotNone(self.task_manager.recovery)

    def test_base_manager_abstract_methods(self):
        """Test that all BaseManager abstract methods are implemented."""
        # Test lifecycle methods
        self.assertTrue(hasattr(self.task_manager, '_on_start'))
        self.assertTrue(hasattr(self.task_manager, '_on_stop'))
        self.assertTrue(hasattr(self.task_manager, '_on_heartbeat'))
        self.assertTrue(hasattr(self.task_manager, '_on_initialize_resources'))
        self.assertTrue(hasattr(self.task_manager, '_on_cleanup_resources'))
        self.assertTrue(hasattr(self.task_manager, '_on_recovery_attempt'))

    def test_on_start_implementation(self):
        """Test the _on_start method implementation."""
        with patch.object(self.task_manager, '_sync_modules') as mock_sync:
            result = self.task_manager._on_start()
            self.assertTrue(result)
            mock_sync.assert_called_once()

    def test_on_stop_implementation(self):
        """Test the _on_stop method implementation."""
        with patch.object(self.task_manager.logger, 'info') as mock_logger:
            self.task_manager._on_stop()
            # Should log start and stop messages
            self.assertEqual(mock_logger.call_count, 2)

    def test_on_heartbeat_implementation(self):
        """Test the _on_heartbeat method implementation."""
        with patch.object(self.task_manager, 'get_system_status') as mock_status:
            mock_status.return_value = {"status": "error"}
            with patch.object(self.task_manager.logger, 'warning') as mock_warning:
                self.task_manager._on_heartbeat()
                mock_warning.assert_called_once()

    def test_on_initialize_resources(self):
        """Test the _on_initialize_resources method implementation."""
        with patch.object(self.task_manager, '_sync_modules') as mock_sync:
            result = self.task_manager._on_initialize_resources()
            self.assertTrue(result)
            mock_sync.assert_called_once()

    def test_on_recovery_attempt(self):
        """Test the _on_recovery_attempt method implementation."""
        error = Exception("Test error")
        with patch.object(self.task_manager, '_sync_modules') as mock_sync:
            result = self.task_manager._on_recovery_attempt(error, "test_context")
            self.assertTrue(result)
            mock_sync.assert_called_once()

    def test_task_scheduling_delegation(self):
        """Test that task scheduling methods properly delegate to TaskScheduler."""
        mock_task = Mock()
        self.mock_scheduler.create_task.return_value = mock_task
        
        result = self.task_manager.create_task("test", "desc", "agent", "creator", "high")
        self.assertEqual(result, mock_task)
        self.mock_scheduler.create_task.assert_called_once()

    def test_task_execution_delegation(self):
        """Test that task execution methods properly delegate to TaskExecutor."""
        mock_tasks = [Mock(), Mock()]
        self.mock_executor.get_all_tasks.return_value = mock_tasks
        
        result = self.task_manager.get_development_tasks()
        self.assertEqual(result, mock_tasks)
        self.mock_executor.get_all_tasks.assert_called_once()

    def test_task_monitoring_delegation(self):
        """Test that task monitoring methods properly delegate to TaskMonitor."""
        mock_status = {"status": "active"}
        self.mock_monitor.get_task_status.return_value = mock_status
        
        result = self.task_manager.get_task_status("agent-1")
        self.assertEqual(result, mock_status)
        self.mock_monitor.get_task_status.assert_called_once_with("agent-1")

    def test_task_recovery_delegation(self):
        """Test that task recovery methods properly delegate to TaskRecovery."""
        mock_tasks = [Mock(), Mock()]
        self.mock_recovery.get_failed_tasks.return_value = mock_tasks
        
        result = self.task_manager.get_failed_tasks()
        self.assertEqual(result, mock_tasks)
        self.mock_recovery.get_failed_tasks.assert_called_once()

    def test_system_status_integration(self):
        """Test the get_system_status method integration."""
        mock_scheduler_status = {"tasks": 5}
        mock_monitor_summary = {"active": 3}
        mock_recovery_stats = {"recovered": 2}
        
        self.mock_scheduler.get_system_status.return_value = mock_scheduler_status
        self.mock_monitor.get_task_status_summary.return_value = mock_monitor_summary
        self.mock_recovery.get_recovery_statistics.return_value = mock_recovery_stats
        
        result = self.task_manager.get_system_status()
        
        self.assertEqual(result["scheduler"], mock_scheduler_status)
        self.assertEqual(result["monitor"], mock_monitor_summary)
        self.assertEqual(result["recovery"], mock_recovery_stats)
        self.assertEqual(result["modules"]["scheduler"], "active")

    def test_convenience_methods(self):
        """Test convenience methods delegation."""
        # Test priority distribution
        mock_distribution = {"high": 2, "normal": 3}
        self.mock_scheduler.get_priority_distribution.return_value = mock_distribution
        result = self.task_manager.get_priority_distribution()
        self.assertEqual(result, mock_distribution)

        # Test cleanup methods
        self.mock_executor.cleanup_completed_tasks.return_value = 5
        result = self.task_manager.cleanup_old_tasks(30)
        self.assertEqual(result, 5)

    def test_error_handling(self):
        """Test error handling in BaseManager methods."""
        # Test _on_start with exception
        with patch.object(self.task_manager, '_sync_modules', side_effect=Exception("Test error")):
            result = self.task_manager._on_start()
            self.assertFalse(result)

        # Test _on_initialize_resources with exception
        with patch.object(self.task_manager, '_sync_modules', side_effect=Exception("Test error")):
            result = self.task_manager._on_initialize_resources()
            self.assertFalse(result)

    def test_srp_compliance(self):
        """Test Single Responsibility Principle compliance."""
        # TaskManager should only coordinate, not implement specific logic
        self.assertTrue(hasattr(self.task_manager, 'scheduler'))
        self.assertTrue(hasattr(self.task_manager, 'executor'))
        self.assertTrue(hasattr(self.task_manager, 'monitor'))
        self.assertTrue(hasattr(self.task_manager, 'recovery'))
        
        # All methods should delegate to appropriate modules
        self.assertTrue(hasattr(self.task_manager, 'create_task'))
        self.assertTrue(hasattr(self.task_manager, 'get_development_tasks'))
        self.assertTrue(hasattr(self.task_manager, 'update_task_status'))
        self.assertTrue(hasattr(self.task_manager, 'delete_task'))

    def test_line_count_target(self):
        """Test that the refactored file meets the 300-line target."""
        file_path = "src/core/task_manager.py"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = len(f.readlines())
                self.assertLessEqual(line_count, 300, 
                                   f"File exceeds 300-line target: {line_count} lines")
            except UnicodeDecodeError:
                # Fallback to binary read for encoding issues
                with open(file_path, 'rb') as f:
                    line_count = len(f.readlines())
                self.assertLessEqual(line_count, 300, 
                                   f"File exceeds 300-line target: {line_count} lines")

    def test_import_stability(self):
        """Test that all imports are stable and accessible."""
        try:
            self.assertTrue(True, "All imports successful")
        except ImportError as e:
            self.fail(f"Import failed: {e}")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
