from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

    from src.autonomous_development.core import DevelopmentTask
from unittest.mock import Mock, patch
import importlib.util

#!/usr/bin/env python3
"""
Tests for Autonomous Development Reporting Module
===============================================

Tests the reporting and status management functionality for autonomous development.
"""


module_path = (
    Path(__file__).resolve().parents[1]
    / "src/autonomous_development/reporting/manager.py"
)
spec = importlib.util.spec_from_file_location("reporting_manager", module_path)
reporting_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reporting_module)

ReportingManager = reporting_module.ReportingManager
InMemoryReportStorage = reporting_module.InMemoryReportStorage

# Use type hints with strings to avoid circular imports

if TYPE_CHECKING:  # pragma: no cover - for type checking only


class DevelopmentTask:  # pragma: no cover - minimal stub for tests
    pass


class TestReportingManager:
    """Test cases for ReportingManager"""

    @pytest.fixture
    def mock_task_manager(self):
        """Create a mock task manager"""
        mock_manager = Mock()
        mock_manager.get_task_summary.return_value = {
            "total_tasks": 5,
            "available_tasks": 2,
            "claimed_tasks": 1,
            "in_progress_tasks": 1,
            "completed_tasks": 1,
            "completion_rate": 20.0,
            "workflow_stats": {
                "overnight_cycles": 3,
                "autonomous_hours": 3,
                "total_tasks_completed": 1,
            },
        }
        mock_manager.tasks = {}
        return mock_manager

    @pytest.fixture
    def reporting_manager(self, mock_task_manager):
        """Create a reporting manager instance for testing"""
        return ReportingManager(mock_task_manager)

    @pytest.fixture
    def mock_task(self):
        """Create a mock development task"""
        task = Mock(spec=DevelopmentTask)
        task.task_id = "TASK-001"
        task.title = "Test Task"
        task.priority = 8
        task.complexity = "high"
        task.estimated_hours = 4.0
        task.required_skills = ["python", "testing"]
        task.description = "A test task"
        return task

    def test_init(self, reporting_manager, mock_task_manager):
        """Test reporting manager initialization"""
        assert reporting_manager.task_manager is mock_task_manager
        assert reporting_manager.logger is not None

    def test_format_task_list_for_agents_with_tasks(self, reporting_manager):
        """Test task list formatting for agents with tasks"""
        tasks = [
            Mock(
                spec=DevelopmentTask,
                priority=8,
                complexity="high",
                estimated_hours=4.0,
                required_skills=["python", "testing"],
                title="High Priority Task",
                description="A high priority task",
                task_id="TASK-001",
            ),
            Mock(
                spec=DevelopmentTask,
                priority=5,
                complexity="medium",
                estimated_hours=2.0,
                required_skills=["git"],
                title="Medium Priority Task",
                description="A medium priority task",
                task_id="TASK-002",
            ),
        ]

        formatted = reporting_manager.format_task_list_for_agents(tasks)

        # Verify formatting
        assert "High Priority Task" in formatted
        assert "Medium Priority Task" in formatted
        assert "Priority: 8" in formatted
        assert "Priority: 5" in formatted
        assert "Complexity: High" in formatted
        assert "Complexity: Medium" in formatted
        assert "python, testing" in formatted
        assert "git" in formatted

    def test_format_task_list_for_agents_empty(self, reporting_manager):
        """Test task list formatting with empty task list"""
        formatted = reporting_manager.format_task_list_for_agents([])
        assert formatted == "No tasks available for claiming."

    def test_format_progress_summary_with_active_tasks(
        self, reporting_manager, mock_task_manager
    ):
        """Test progress summary formatting with active tasks"""
        # Create mock active tasks
        mock_tasks = {
            "task1": Mock(
                spec=DevelopmentTask,
                status="claimed",
                title="Task 1",
                claimed_by="Agent-2",
                progress_percentage=0.0,
                blockers=[],
            ),
            "task2": Mock(
                spec=DevelopmentTask,
                status="in_progress",
                title="Task 2",
                claimed_by="Agent-3",
                progress_percentage=75.0,
                blockers=["Waiting for review"],
            ),
        }
        mock_task_manager.tasks = mock_tasks

        formatted = reporting_manager.format_progress_summary()

        # Verify formatting
        assert "Task 1" in formatted
        assert "Task 2" in formatted
        assert "Agent: Agent-2" in formatted
        assert "Agent: Agent-3" in formatted
        assert "Progress: 0.0%" in formatted
        assert "Progress: 75.0%" in formatted
        assert "Blockers: Waiting for review" in formatted

    def test_format_progress_summary_no_active_tasks(
        self, reporting_manager, mock_task_manager
    ):
        """Test progress summary formatting with no active tasks"""
        mock_task_manager.tasks = {}

        formatted = reporting_manager.format_progress_summary()
        assert formatted == "No active tasks to report progress on."

    def test_format_cycle_summary(self, reporting_manager, mock_task_manager):
        """Test cycle summary formatting"""
        formatted = reporting_manager.format_cycle_summary()

        # Verify summary contains expected information
        assert "CYCLE COMPLETE - SUMMARY" in formatted
        assert "Total Tasks: 5" in formatted
        assert "Available: 2" in formatted
        assert "Claimed: 1" in formatted
        assert "In Progress: 1" in formatted
        assert "Completed: 1" in formatted
        assert "Completion Rate: 20.0%" in formatted
        assert "Overnight Cycles: 3" in formatted
        assert "Autonomous Hours: 3" in formatted
        assert "Total Tasks Completed: 1" in formatted

    def test_format_workflow_start_message(self, reporting_manager):
        """Test workflow start message formatting"""
        formatted = reporting_manager.format_workflow_start_message()

        # Verify message contains expected content
        assert "AUTONOMOUS OVERNIGHT DEVELOPMENT WORKFLOW STARTED" in formatted
        assert "AGENT-1: Task Manager Role" in formatted
        assert "AGENTS 2-8: Autonomous Workforce" in formatted
        assert "WORKFLOW CYCLE" in formatted
        assert "CYCLE DURATION: 1 hour" in formatted
        assert "OPERATION: Continuous overnight" in formatted

    def test_format_agent1_message(self, reporting_manager):
        """Test Agent-1 message formatting"""
        formatted = reporting_manager.format_agent1_message()

        # Verify message contains expected content
        assert "AGENT-1: You are now the Task Manager" in formatted
        assert "Monitor task list and create new tasks as needed" in formatted
        assert "Track progress and identify bottlenecks" in formatted
        assert "Coordinate workflow and resolve conflicts" in formatted
        assert "Optimize task distribution and priorities" in formatted
        assert "Handle emergencies and blocked tasks" in formatted

    def test_format_no_tasks_message(self, reporting_manager):
        """Test no tasks available message formatting"""
        formatted = reporting_manager.format_no_tasks_message()

        # Verify message contains expected content
        assert "NO TASKS AVAILABLE" in formatted
        assert "All current tasks have been claimed or completed" in formatted
        assert "Waiting for Agent-1 to create new tasks" in formatted
        assert "Next cycle will focus on" in formatted

    def test_format_task_claimed_message(self, reporting_manager, mock_task):
        """Test task claimed message formatting"""
        formatted = reporting_manager.format_task_claimed_message(mock_task)

        # Verify message contains expected content
        assert "TASK CLAIMED: Test Task" in formatted
        assert "ID: TASK-001" in formatted
        assert "Priority: 8" in formatted
        assert "Complexity: high" in formatted
        assert "Estimated Time: 4.0h" in formatted

    def test_history_storage_and_retrieval(self, mock_task_manager):
        """Reports and metadata are saved and retrievable from the backend."""
        backend = InMemoryReportStorage()
        manager = ReportingManager(mock_task_manager, storage_backend=backend)
        manager.report_history.append({"report": "sample"})
        manager.reports_generated = 1
        manager.last_report_time = datetime(2024, 1, 1)

        manager._save_report_history()

        history = manager.get_report_history()
        assert history[0]["reports"][0]["report"] == "sample"
        assert history[0]["metadata"]["reports_generated"] == 1
        assert (
            history[0]["metadata"]["last_report_time"]
            == datetime(2024, 1, 1).isoformat()
        )
        assert manager.get_last_report() == history[0]

    def test_format_progress_update_message_with_blockers(
        self, reporting_manager, mock_task
    ):
        """Test progress update message formatting with blockers"""
        blockers = ["Waiting for review", "Need clarification"]
        formatted = reporting_manager.format_progress_update_message(
            mock_task, 75.0, blockers
        )

        # Verify message contains expected content
        assert "PROGRESS UPDATE - BLOCKERS DETECTED" in formatted
        assert "Task: Test Task" in formatted
        assert "Progress: 75.0%" in formatted
        assert "Blockers: Waiting for review, Need clarification" in formatted
        assert "Action Required: Address blockers before continuing" in formatted

    def test_format_progress_update_message_no_blockers(
        self, reporting_manager, mock_task
    ):
        """Test progress update message formatting without blockers"""
        formatted = reporting_manager.format_progress_update_message(mock_task, 75.0)

        # Verify message contains expected content
        assert "PROGRESS UPDATE" in formatted
        assert "Task: Test Task" in formatted
        assert "Progress: 75.0%" in formatted
        assert "Status: Making good progress" in formatted
        assert "Continue autonomous development" in formatted

    def test_format_workflow_complete_message(
        self, reporting_manager, mock_task_manager
    ):
        """Test workflow completion message formatting"""
        formatted = reporting_manager.format_workflow_complete_message()

        # Verify message contains expected content
        assert "OVERNIGHT WORKFLOW COMPLETE" in formatted
        assert "Total Cycles: 3" in formatted
        assert "Autonomous Hours: 3" in formatted
        assert "Tasks Completed: 1" in formatted
        assert "Great work on autonomous development" in formatted
        assert "System ready for next overnight session" in formatted

    def test_format_remaining_tasks_message(self, reporting_manager):
        """Test remaining tasks message formatting"""
        formatted = reporting_manager.format_remaining_tasks_message(3)
        assert formatted == "📋 3 tasks still available for claiming in next cycle."

    def test_format_detailed_task_status(self, reporting_manager, mock_task_manager):
        """Test detailed task status formatting"""
        # Create mock tasks
        mock_tasks = {
            "task1": Mock(
                spec=DevelopmentTask,
                task_id="TASK-001",
                title="Task 1",
                status="available",
                claimed_by=None,
                progress_percentage=0.0,
            ),
            "task2": Mock(
                spec=DevelopmentTask,
                task_id="TASK-002",
                title="Task 2",
                status="claimed",
                claimed_by="Agent-2",
                progress_percentage=0.0,
            ),
            "task3": Mock(
                spec=DevelopmentTask,
                task_id="TASK-003",
                title="Task 3",
                status="in_progress",
                claimed_by="Agent-3",
                progress_percentage=50.0,
            ),
        }
        mock_task_manager.tasks = mock_tasks

        formatted = reporting_manager.format_detailed_task_status()

        # Verify formatting
        assert "Current Development Task Status" in formatted
        assert "Total Tasks: 5" in formatted
        assert "Available: 2" in formatted
        assert "In Progress: 1" in formatted
        assert "Completed: 1" in formatted
        assert "Completion Rate: 20.0%" in formatted
        assert "TASK-001: Task 1" in formatted
        assert "TASK-002: Task 2" in formatted
        assert "TASK-003: Task 3" in formatted

    def test_format_workflow_statistics(self, reporting_manager, mock_task_manager):
        """Test workflow statistics formatting"""
        formatted = reporting_manager.format_workflow_statistics()

        # Verify formatting
        assert "Autonomous Development Workflow Statistics" in formatted
        assert "Total Tasks Created: 5" in formatted
        assert "Total Tasks Completed: 1" in formatted
        assert "Total Tasks Claimed: 1" in formatted
        assert "Overnight Cycles: 3" in formatted
        assert "Autonomous Hours: 3" in formatted

    def test_get_priority_icon_high(self, reporting_manager):
        """Test priority icon for high priority tasks"""
        icon = reporting_manager._get_priority_icon(8)
        assert icon == "🔴"

    def test_get_priority_icon_medium(self, reporting_manager):
        """Test priority icon for medium priority tasks"""
        icon = reporting_manager._get_priority_icon(5)
        assert icon == "🟡"

    def test_get_priority_icon_low(self, reporting_manager):
        """Test priority icon for low priority tasks"""
        icon = reporting_manager._get_priority_icon(3)
        assert icon == "🟢"

    def test_get_complexity_icon_high(self, reporting_manager):
        """Test complexity icon for high complexity tasks"""
        icon = reporting_manager._get_complexity_icon("high")
        assert icon == "🔥"

    def test_get_complexity_icon_medium(self, reporting_manager):
        """Test complexity icon for medium complexity tasks"""
        icon = reporting_manager._get_complexity_icon("medium")
        assert icon == "⚡"

    def test_get_complexity_icon_low(self, reporting_manager):
        """Test complexity icon for low complexity tasks"""
        icon = reporting_manager._get_complexity_icon("low")
        assert icon == "💡"

    def test_get_status_icon_available(self, reporting_manager):
        """Test status icon for available tasks"""
        icon = reporting_manager._get_status_icon("available")
        assert icon == "🟢"

    def test_get_status_icon_claimed(self, reporting_manager):
        """Test status icon for claimed tasks"""
        icon = reporting_manager._get_status_icon("claimed")
        assert icon == "🟡"

    def test_get_status_icon_in_progress(self, reporting_manager):
        """Test status icon for in-progress tasks"""
        icon = reporting_manager._get_status_icon("in_progress")
        assert icon == "🔄"

    def test_get_status_icon_completed(self, reporting_manager):
        """Test status icon for completed tasks"""
        icon = reporting_manager._get_status_icon("completed")
        assert icon == "✅"

    def test_get_status_icon_blocked(self, reporting_manager):
        """Test status icon for blocked tasks"""
        icon = reporting_manager._get_status_icon("blocked")
        assert icon == "🚫"

    def test_get_status_icon_unknown(self, reporting_manager):
        """Test status icon for unknown status"""
        icon = reporting_manager._get_status_icon("unknown_status")
        assert icon == "❓"

    def test_generate_performance_report_success(
        self, reporting_manager, mock_task_manager
    ):
        """Test successful performance report generation"""
        report = reporting_manager.generate_performance_report()

        assert isinstance(report, dict)
        assert "summary" in report
        assert "workflow_stats" in report
        assert "performance_metrics" in report

        metrics = report["performance_metrics"]
        assert "efficiency_score" in metrics
        assert "avg_cycle_efficiency" in metrics
        assert "task_completion_rate" in metrics
        assert "autonomous_productivity" in metrics

    def test_generate_performance_report_exception(
        self, reporting_manager, mock_task_manager
    ):
        """Test performance report generation with exception"""
        # Mock the get_task_summary to raise an exception
        mock_task_manager.get_task_summary.side_effect = Exception("Database error")

        report = reporting_manager.generate_performance_report()

        # Should return empty dict on error
        assert report == {}

    def test_generate_performance_report_zero_tasks(
        self, reporting_manager, mock_task_manager
    ):
        """Test performance report generation with zero tasks"""
        # Mock zero tasks
        mock_task_manager.get_task_summary.return_value = {
            "total_tasks": 0,
            "available_tasks": 0,
            "claimed_tasks": 0,
            "in_progress_tasks": 0,
            "completed_tasks": 0,
            "completion_rate": 0.0,
            "workflow_stats": {
                "overnight_cycles": 0,
                "autonomous_hours": 0,
                "total_tasks_completed": 0,
            },
        }

        report = reporting_manager.generate_performance_report()

        # Should handle zero tasks gracefully
        assert report["performance_metrics"]["efficiency_score"] == 0.0
        assert report["performance_metrics"]["avg_cycle_efficiency"] == 0.0


if __name__ == "__main__":
    pytest.main([__file__])
