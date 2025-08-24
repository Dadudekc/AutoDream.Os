#!/usr/bin/env python3
"""
Core Models Tests - Agent Cellphone V2
=====================================

TDD tests for core development task models.
Tests data validation, business logic, and edge cases.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import unittest

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime, timedelta
from dataclasses import asdict
from ..core.enums import TaskPriority, TaskComplexity, TaskStatus, AgentRole
from ..core.models import DevelopmentTask


class TestTaskEnums(unittest.TestCase):
    """Test task enumeration values and behavior"""
    
    def test_task_priority_values(self):
        """Test task priority enum values"""
        self.assertEqual(TaskPriority.LOW.value, "low")
        self.assertEqual(TaskPriority.MEDIUM.value, "medium")
        self.assertEqual(TaskPriority.HIGH.value, "high")
        self.assertEqual(TaskPriority.CRITICAL.value, "critical")
    
    def test_task_complexity_values(self):
        """Test task complexity enum values"""
        self.assertEqual(TaskComplexity.SIMPLE.value, "simple")
        self.assertEqual(TaskComplexity.MODERATE.value, "moderate")
        self.assertEqual(TaskComplexity.COMPLEX.value, "complex")
        self.assertEqual(TaskComplexity.EXTREME.value, "extreme")
    
    def test_task_status_values(self):
        """Test task status enum values"""
        self.assertEqual(TaskStatus.PENDING.value, "pending")
        self.assertEqual(TaskStatus.IN_PROGRESS.value, "in_progress")
        self.assertEqual(TaskStatus.COMPLETED.value, "completed")
        self.assertEqual(TaskStatus.FAILED.value, "failed")
        self.assertEqual(TaskStatus.CANCELLED.value, "cancelled")
    
    def test_agent_role_values(self):
        """Test agent role enum values"""
        self.assertEqual(AgentRole.DEVELOPER.value, "developer")
        self.assertEqual(AgentRole.TESTER.value, "tester")
        self.assertEqual(AgentRole.REVIEWER.value, "reviewer")
        self.assertEqual(AgentRole.COORDINATOR.value, "coordinator")


class TestDevelopmentTask(unittest.TestCase):
    """Test development task model creation and validation"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_task_data = {
            "task_id": "task_001",
            "title": "Implement user authentication",
            "description": "Add secure user authentication system",
            "priority": TaskPriority.HIGH,
            "complexity": TaskComplexity.MODERATE,
            "assigned_agent": "agent_dev_001",
            "agent_role": AgentRole.DEVELOPER,
            "estimated_hours": 8,
            "deadline": datetime.now() + timedelta(days=7),
            "dependencies": ["task_002", "task_003"],
            "tags": ["security", "authentication", "backend"]
        }
    
    def test_create_valid_task(self):
        """Test creating a valid development task"""
        task = DevelopmentTask(**self.valid_task_data)
        
        self.assertEqual(task.task_id, "task_001")
        self.assertEqual(task.title, "Implement user authentication")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        self.assertEqual(task.complexity, TaskComplexity.MODERATE)
        self.assertEqual(task.assigned_agent, "agent_dev_001")
        self.assertEqual(task.agent_role, AgentRole.DEVELOPER)
        self.assertEqual(task.estimated_hours, 8)
        self.assertEqual(len(task.dependencies), 2)
        self.assertEqual(len(task.tags), 3)
    
    def test_task_default_values(self):
        """Test task default values"""
        minimal_data = {
            "task_id": "task_002",
            "title": "Simple task",
            "description": "Basic task description"
        }
        
        task = DevelopmentTask(**minimal_data)
        
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertEqual(task.complexity, TaskComplexity.SIMPLE)
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.agent_role, AgentRole.DEVELOPER)
        self.assertEqual(task.estimated_hours, 1)
        self.assertEqual(task.dependencies, [])
        self.assertEqual(task.tags, [])
        self.assertIsNotNone(task.created_at)
        self.assertIsNone(task.started_at)
        self.assertIsNone(task.completed_at)
    
    def test_task_validation(self):
        """Test task validation rules"""
        # Test invalid task_id format
        with self.assertRaises(ValueError):
            invalid_data = self.valid_task_data.copy()
            invalid_data["task_id"] = "invalid_id"
            DevelopmentTask(**invalid_data)
        
        # Test invalid estimated_hours
        with self.assertRaises(ValueError):
            invalid_data = self.valid_task_data.copy()
            invalid_data["estimated_hours"] = -1
            DevelopmentTask(**invalid_data)
        
        # Test invalid deadline (past date)
        with self.assertRaises(ValueError):
            invalid_data = self.valid_task_data.copy()
            invalid_data["deadline"] = datetime.now() - timedelta(days=1)
            DevelopmentTask(**invalid_data)
    
    def test_task_serialization(self):
        """Test task serialization to dictionary"""
        task = DevelopmentTask(**self.valid_task_data)
        task_dict = asdict(task)
        
        self.assertIsInstance(task_dict, dict)
        self.assertEqual(task_dict["task_id"], "task_001")
        self.assertEqual(task_dict["title"], "Implement user authentication")
        self.assertEqual(task_dict["priority"], "high")
        self.assertEqual(task_dict["complexity"], "moderate")
    
    def test_task_status_transitions(self):
        """Test valid task status transitions"""
        task = DevelopmentTask(**self.valid_task_data)
        
        # Pending -> In Progress
        task.start_task()
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        self.assertIsNotNone(task.started_at)
        
        # In Progress -> Completed
        task.complete_task()
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.completed_at)
    
    def test_task_status_transition_validation(self):
        """Test invalid task status transitions"""
        task = DevelopmentTask(**self.valid_task_data)
        
        # Cannot complete a pending task
        with self.assertRaises(ValueError):
            task.complete_task()
        
        # Cannot start a completed task
        task.start_task()
        task.complete_task()
        with self.assertRaises(ValueError):
            task.start_task()
    
    def test_task_dependencies(self):
        """Test task dependency management"""
        task = DevelopmentTask(**self.valid_task_data)
        
        # Add dependency
        task.add_dependency("task_004")
        self.assertIn("task_004", task.dependencies)
        self.assertEqual(len(task.dependencies), 3)
        
        # Remove dependency
        task.remove_dependency("task_002")
        self.assertNotIn("task_002", task.dependencies)
        self.assertEqual(len(task.dependencies), 2)
    
    def test_task_tags(self):
        """Test task tag management"""
        task = DevelopmentTask(**self.valid_task_data)
        
        # Add tag
        task.add_tag("frontend")
        self.assertIn("frontend", task.tags)
        self.assertEqual(len(task.tags), 4)
        
        # Remove tag
        task.remove_tag("security")
        self.assertNotIn("security", task.tags)
        self.assertEqual(len(task.tags), 3)
    
    def test_task_time_tracking(self):
        """Test task time tracking functionality"""
        task = DevelopmentTask(**self.valid_task_data)
        
        # Start task and track time
        task.start_task()
        time.sleep(0.1)  # Small delay to ensure time difference
        
        # Update progress
        task.update_progress(50, "Halfway through implementation")
        self.assertEqual(task.progress_percentage, 50)
        self.assertEqual(task.current_status_note, "Halfway through implementation")
        
        # Complete task
        task.complete_task()
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.completed_at)


if __name__ == '__main__':
    unittest.main()

