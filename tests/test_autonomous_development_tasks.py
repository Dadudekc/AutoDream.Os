#!/usr/bin/env python3
"""
Tests for Autonomous Development Tasks Module
============================================

Tests the task management and execution functionality for autonomous development.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.autonomous_development.tasks.handler import TaskHandler
# Use type hints with strings to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.autonomous_development.core import DevelopmentTask


class TestTaskHandler:
    """Test cases for TaskHandler"""

    @pytest.fixture
    def mock_task_manager(self):
        """Create a mock task manager"""
        mock_manager = Mock()
        mock_manager.workflow_stats = {"total_tasks_completed": 0}
        mock_manager.tasks = {}
        return mock_manager

    @pytest.fixture
    def task_handler(self, mock_task_manager):
        """Create a task handler instance for testing"""
        return TaskHandler(mock_task_manager)

    @pytest.fixture
    def mock_task(self):
        """Create a mock development task"""
        task = Mock(spec=DevelopmentTask)
        task.task_id = "TASK-001"
        task.title = "Test Task"
        task.status = "available"
        task.progress_percentage = 0.0
        task.priority = 8
        task.complexity = "high"
        task.estimated_hours = 4.0
        task.required_skills = ["python", "testing"]
        task.description = "A test task"
        task.created_at = datetime.now()
        task.blockers = []
        task.claimed_by = None
        return task

    def test_init(self, task_handler, mock_task_manager):
        """Test task handler initialization"""
        assert task_handler.task_manager is mock_task_manager
        assert task_handler.logger is not None

    def test_create_development_task_success(self, task_handler, mock_task_manager):
        """Test successful task creation"""
        title = "Test Task"
        description = "A test task"
        complexity = "medium"
        priority = 7
        estimated_hours = 3.0
        required_skills = ["python", "testing"]
        
        mock_task_manager.create_task.return_value = "TASK-001"
        
        task_id = task_handler.create_development_task(
            title, description, complexity, priority, estimated_hours, required_skills
        )
        
        assert task_id == "TASK-001"
        mock_task_manager.create_task.assert_called_once_with(
            title=title,
            description=description,
            complexity=complexity,
            priority=priority,
            estimated_hours=estimated_hours,
            required_skills=required_skills,
        )

    def test_create_development_task_invalid_complexity(self, task_handler):
        """Test task creation with invalid complexity"""
        with pytest.raises(ValueError, match="Complexity must be 'low', 'medium', or 'high'"):
            task_handler.create_development_task(
                "Test Task", "Description", "invalid", 5, 2.0
            )

    def test_create_development_task_invalid_priority(self, task_handler):
        """Test task creation with invalid priority"""
        with pytest.raises(ValueError, match="Priority must be between 1 and 10"):
            task_handler.create_development_task(
                "Test Task", "Description", "medium", 11, 2.0
            )

    def test_create_development_task_invalid_hours(self, task_handler):
        """Test task creation with invalid hours"""
        with pytest.raises(ValueError, match="Hours must be positive"):
            task_handler.create_development_task(
                "Test Task", "Description", "medium", 5, -1.0
            )

    def test_create_development_task_generate_skills(self, task_handler, mock_task_manager):
        """Test task creation with auto-generated skills"""
        mock_task_manager.create_task.return_value = "TASK-001"
        
        task_id = task_handler.create_development_task(
            "Test Task", "Description", "high", 8, 4.0
        )
        
        assert task_id == "TASK-001"
        # Verify create_task was called with generated skills
        call_args = mock_task_manager.create_task.call_args
        assert "required_skills" in call_args.kwargs
        assert len(call_args.kwargs["required_skills"]) == 4  # high complexity = 4 skills

    def test_generate_skills_for_complexity_low(self, task_handler):
        """Test skill generation for low complexity tasks"""
        skills = task_handler._generate_skills_for_complexity("low")
        assert len(skills) == 2
        assert all(skill in ["documentation", "markdown", "testing", "git"] for skill in skills)

    def test_generate_skills_for_complexity_medium(self, task_handler):
        """Test skill generation for medium complexity tasks"""
        skills = task_handler._generate_skills_for_complexity("medium")
        assert len(skills) == 3
        assert all(skill in ["code_analysis", "optimization", "debugging", "refactoring"] for skill in skills)

    def test_generate_skills_for_complexity_high(self, task_handler):
        """Test skill generation for high complexity tasks"""
        skills = task_handler._generate_skills_for_complexity("high")
        assert len(skills) == 4
        assert all(skill in ["performance_analysis", "security_analysis", "architecture", "profiling"] for skill in skills)

    def test_claim_task_success(self, task_handler, mock_task_manager):
        """Test successful task claiming"""
        mock_task_manager.claim_task.return_value = True
        
        result = task_handler.claim_task("TASK-001", "Agent-2")
        
        assert result is True
        mock_task_manager.claim_task.assert_called_once_with("TASK-001", "Agent-2")

    def test_claim_task_failure(self, task_handler, mock_task_manager):
        """Test failed task claiming"""
        mock_task_manager.claim_task.return_value = False
        
        result = task_handler.claim_task("TASK-001", "Agent-2")
        
        assert result is False

    def test_claim_task_exception(self, task_handler, mock_task_manager):
        """Test task claiming with exception"""
        mock_task_manager.claim_task.side_effect = Exception("Database error")
        
        result = task_handler.claim_task("TASK-001", "Agent-2")
        
        assert result is False

    def test_start_task_work_success(self, task_handler, mock_task_manager, mock_task):
        """Test successful task work start"""
        mock_task.status = "claimed"
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        result = task_handler.start_task_work("TASK-001")
        
        assert result is True
        assert mock_task.status == "in_progress"
        assert mock_task.started_at is not None

    def test_start_task_work_wrong_status(self, task_handler, mock_task_manager, mock_task):
        """Test starting work on task with wrong status"""
        mock_task.status = "available"  # Not claimed
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        result = task_handler.start_task_work("TASK-001")
        
        assert result is False
        assert mock_task.status == "available"  # Should not change

    def test_start_task_work_task_not_found(self, task_handler, mock_task_manager):
        """Test starting work on non-existent task"""
        mock_task_manager.tasks = {}
        
        result = task_handler.start_task_work("TASK-001")
        
        assert result is False

    def test_start_task_work_exception(self, task_handler, mock_task_manager):
        """Test starting work with exception"""
        mock_task_manager.tasks = {"TASK-001": Mock()}
        mock_task_manager.tasks["TASK-001"].status = "claimed"
        mock_task_manager.tasks["TASK-001"].__setattr__ = Mock(side_effect=Exception("Error"))
        
        result = task_handler.start_task_work("TASK-001")
        
        assert result is False

    def test_update_task_progress_success(self, task_handler, mock_task_manager, mock_task):
        """Test successful task progress update"""
        mock_task.status = "in_progress"
        mock_task.progress_percentage = 50.0
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        result = task_handler.update_task_progress("TASK-001", 75.0)
        
        assert result is True
        assert mock_task.progress_percentage == 75.0
        assert mock_task.last_updated is not None

    def test_update_task_progress_with_blockers(self, task_handler, mock_task_manager, mock_task):
        """Test task progress update with blockers"""
        mock_task.status = "in_progress"
        mock_task.progress_percentage = 50.0
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        blockers = ["Waiting for review", "Need clarification"]
        result = task_handler.update_task_progress("TASK-001", 75.0, blockers)
        
        assert result is True
        assert mock_task.blockers == blockers
        assert mock_task.status == "blocked"

    def test_update_task_progress_clear_blockers(self, task_handler, mock_task_manager, mock_task):
        """Test clearing blockers when updating progress"""
        mock_task.status = "blocked"
        mock_task.progress_percentage = 50.0
        mock_task.blockers = ["Waiting for review"]
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        result = task_handler.update_task_progress("TASK-001", 75.0)
        
        assert result is True
        assert mock_task.blockers == []
        assert mock_task.status == "in_progress"

    def test_update_task_progress_complete(self, task_handler, mock_task_manager, mock_task):
        """Test task completion when progress reaches 100%"""
        mock_task.status = "in_progress"
        mock_task.progress_percentage = 90.0
        mock_task.started_at = datetime.now()
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        result = task_handler.update_task_progress("TASK-001", 100.0)
        
        assert result is True
        assert mock_task.status == "completed"
        assert mock_task.completed_at is not None
        assert mock_task.actual_hours is not None

    def test_update_task_progress_task_not_found(self, task_handler, mock_task_manager):
        """Test updating progress for non-existent task"""
        mock_task_manager.tasks = {}
        
        result = task_handler.update_task_progress("TASK-001", 50.0)
        
        assert result is False

    def test_update_task_progress_exception(self, task_handler, mock_task_manager):
        """Test updating progress with exception"""
        mock_task = Mock()
        mock_task.progress_percentage = 50.0
        mock_task.__setattr__ = Mock(side_effect=Exception("Error"))
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        result = task_handler.update_task_progress("TASK-001", 75.0)
        
        assert result is False

    def test_get_task_status(self, task_handler, mock_task_manager, mock_task):
        """Test getting task status"""
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        status = task_handler.get_task_status("TASK-001")
        
        assert status is not None
        assert status["task_id"] == "TASK-001"
        assert status["title"] == "Test Task"
        assert status["status"] == "available"

    def test_get_task_status_not_found(self, task_handler, mock_task_manager):
        """Test getting status for non-existent task"""
        mock_task_manager.tasks = {}
        
        status = task_handler.get_task_status("TASK-001")
        
        assert status is None

    def test_get_tasks_by_status(self, task_handler, mock_task_manager):
        """Test getting tasks by status"""
        # Create mock tasks with different statuses
        task1 = Mock(spec=DevelopmentTask)
        task1.status = "available"
        task2 = Mock(spec=DevelopmentTask)
        task2.status = "claimed"
        task3 = Mock(spec=DevelopmentTask)
        task3.status = "available"
        
        mock_task_manager.tasks = {"task1": task1, "task2": task2, "task3": task3}
        
        available_tasks = task_handler.get_tasks_by_status("available")
        
        assert len(available_tasks) == 2
        assert all(task.status == "available" for task in available_tasks)

    def test_get_tasks_by_agent(self, task_handler, mock_task_manager):
        """Test getting tasks by agent"""
        # Create mock tasks claimed by different agents
        task1 = Mock(spec=DevelopmentTask)
        task1.claimed_by = "Agent-2"
        task2 = Mock(spec=DevelopmentTask)
        task2.claimed_by = "Agent-3"
        task3 = Mock(spec=DevelopmentTask)
        task3.claimed_by = "Agent-2"
        
        mock_task_manager.tasks = {"task1": task1, "task2": task2, "task3": task3}
        
        agent2_tasks = task_handler.get_tasks_by_agent("Agent-2")
        
        assert len(agent2_tasks) == 2
        assert all(task.claimed_by == "Agent-2" for task in agent2_tasks)

    def test_get_blocked_tasks(self, task_handler, mock_task_manager):
        """Test getting blocked tasks"""
        # Create mock tasks with different statuses
        task1 = Mock(spec=DevelopmentTask)
        task1.status = "blocked"
        task2 = Mock(spec=DevelopmentTask)
        task2.status = "in_progress"
        task3 = Mock(spec=DevelopmentTask)
        task3.status = "blocked"
        
        mock_task_manager.tasks = {"task1": task1, "task2": task2, "task3": task3}
        
        blocked_tasks = task_handler.get_blocked_tasks()
        
        assert len(blocked_tasks) == 2
        assert all(task.status == "blocked" for task in blocked_tasks)

    def test_resolve_task_blocker_success(self, task_handler, mock_task_manager, mock_task):
        """Test successful blocker resolution"""
        mock_task.status = "blocked"
        mock_task.blockers = ["Waiting for review", "Need clarification"]
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        result = task_handler.resolve_task_blocker("TASK-001", "Waiting for review")
        
        assert result is True
        assert "Waiting for review" not in mock_task.blockers
        assert "Need clarification" in mock_task.blockers
        assert mock_task.status == "in_progress"  # Should be unblocked

    def test_resolve_task_blocker_not_found(self, task_handler, mock_task_manager):
        """Test resolving blocker for non-existent task"""
        mock_task_manager.tasks = {}
        
        result = task_handler.resolve_task_blocker("TASK-001", "Blocker")
        
        assert result is False

    def test_resolve_task_blocker_no_blockers(self, task_handler, mock_task_manager, mock_task):
        """Test resolving blocker when task has no blockers"""
        mock_task.blockers = []
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        result = task_handler.resolve_task_blocker("TASK-001", "Blocker")
        
        assert result is False

    def test_get_task_completion_estimate(self, task_handler, mock_task_manager, mock_task):
        """Test getting task completion estimate"""
        mock_task.status = "in_progress"
        mock_task.progress_percentage = 50.0
        mock_task.estimated_hours = 4.0
        mock_task.actual_hours = 2.0
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        estimate = task_handler.get_task_completion_estimate("TASK-001")
        
        assert estimate is not None
        assert estimate > 0.0

    def test_get_task_completion_estimate_completed(self, task_handler, mock_task_manager, mock_task):
        """Test getting completion estimate for completed task"""
        mock_task.status = "completed"
        mock_task_manager.tasks = {"TASK-001": mock_task}
        
        estimate = task_handler.get_task_completion_estimate("TASK-001")
        
        assert estimate is None

    def test_get_task_statistics(self, task_handler, mock_task_manager):
        """Test getting task statistics"""
        # Create mock tasks with different statuses
        task1 = Mock(spec=DevelopmentTask)
        task1.status = "completed"
        task1.started_at = datetime.now()
        task1.completed_at = datetime.now()
        task1.blockers = []
        
        task2 = Mock(spec=DevelopmentTask)
        task2.status = "blocked"
        task2.blockers = ["Waiting for review"]
        
        mock_task_manager.tasks = {"task1": task1, "task2": task2}
        
        stats = task_handler.get_task_statistics()
        
        assert isinstance(stats, dict)
        assert "total_tasks" in stats
        assert "tasks_by_status" in stats
        assert "blocker_statistics" in stats
        assert stats["total_tasks"] == 2


if __name__ == "__main__":
    pytest.main([__file__])
