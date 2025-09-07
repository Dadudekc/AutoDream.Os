#!/usr/bin/env python3
"""Unit tests for autonomous development modules and orchestrator."""

import asyncio
import types
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from src.autonomous_development.agents.coordinator import AgentCoordinator
from src.autonomous_development.tasks.handler import TaskHandler
from src.autonomous_development.reporting.manager import ReportingManager
from src.autonomous_development.workflow.manager import AutonomousWorkflowManager


class DummyTaskManager:
    """Simple in-memory task manager for testing."""

    def __init__(self):
        self.tasks = {}
        self.workflow_stats = {
            "overnight_cycles": 0,
            "autonomous_hours": 0,
            "total_tasks_completed": 0,
        }

    def create_task(
        self,
        title,
        description,
        complexity,
        priority,
        estimated_hours,
        required_skills,
    ):
        task_id = f"TASK-{len(self.tasks) + 1}"
        self.tasks[task_id] = SimpleNamespace(
            task_id=task_id,
            title=title,
            description=description,
            complexity=complexity,
            priority=priority,
            estimated_hours=estimated_hours,
            required_skills=required_skills or [],
            status="available",
            claimed_by=None,
            progress_percentage=0.0,
            blockers=[],
        )
        return task_id

    def get_available_tasks(self):
        return [t for t in self.tasks.values() if t.status == "available"]

    def claim_task(self, task_id, agent_id):
        task = self.tasks.get(task_id)
        if task and task.status == "available":
            task.status = "claimed"
            task.claimed_by = agent_id
            return True
        return False

    def get_task_summary(self):
        total = len(self.tasks)
        available = len([t for t in self.tasks.values() if t.status == "available"])
        claimed = len([t for t in self.tasks.values() if t.status == "claimed"])
        in_progress = len([t for t in self.tasks.values() if t.status == "in_progress"])
        completed = len([t for t in self.tasks.values() if t.status == "completed"])
        completion_rate = (completed / total * 100) if total else 0.0
        return {
            "total_tasks": total,
            "available_tasks": available,
            "claimed_tasks": claimed,
            "in_progress_tasks": in_progress,
            "completed_tasks": completed,
            "completion_rate": completion_rate,
            "workflow_stats": self.workflow_stats,
        }

    def get_task_statistics(self):
        return self.get_task_summary()


def test_task_handler_creates_and_claims_task():
    tm = DummyTaskManager()
    handler = TaskHandler(tm)
    task_id = handler.create_development_task("Test", "Desc", "low", 1, 1.0, ["git"])
    assert task_id in tm.tasks
    assert handler.claim_task(task_id, "Agent-2")
    assert tm.tasks[task_id].claimed_by == "Agent-2"


def test_agent_coordinator_matches_and_updates_workload():
    tm = DummyTaskManager()
    handler = TaskHandler(tm)
    task_id = handler.create_development_task("Test", "Desc", "low", 1, 1.0, ["git"])
    task = tm.tasks[task_id]

    coordinator = AgentCoordinator()
    best = coordinator.find_best_task_for_agent("Agent-2", [task])
    assert best.task_id == task_id

    coordinator.update_agent_workload("Agent-2", task_id, "claim")
    summary = coordinator.get_agent_workload_summary("Agent-2")
    assert summary["current_task"] == task_id


def test_reporting_manager_generates_performance_report():
    tm = DummyTaskManager()
    handler = TaskHandler(tm)
    handler.create_development_task("Test", "Desc", "low", 1, 1.0, ["git"])

    reporting = ReportingManager(tm)
    report = reporting.generate_performance_report()
    assert "summary" in report
    assert "workflow_stats" in report
    assert "performance_metrics" in report


def test_workflow_manager_cycle_updates_stats():
    tm = DummyTaskManager()
    comm = SimpleNamespace(
        send_message_to_all_agents_with_line_breaks=AsyncMock(),
        send_message_to_agent_with_line_breaks=AsyncMock(),
    )
    manager = AutonomousWorkflowManager(
        comm,
        tm,
        AgentCoordinator(),
        TaskHandler(tm),
        ReportingManager(tm),
    )
    manager._task_review_and_claiming_phase = AsyncMock()
    manager._work_execution_phase = AsyncMock()
    manager._progress_reporting_phase = AsyncMock()
    manager._cycle_summary_phase = AsyncMock()

    asyncio.run(manager._execute_workflow_cycle())
    assert tm.workflow_stats["overnight_cycles"] == 1
    assert tm.workflow_stats["autonomous_hours"] == 1


@patch.dict(
    "sys.modules",
    {
        "src.core.task_manager": types.SimpleNamespace(
            DevelopmentTaskManager=DummyTaskManager
        ),
        "src.services.messaging": types.SimpleNamespace(
            UnifiedMessagingService=lambda: SimpleNamespace()
        ),
    },
)
def test_autonomous_system_orchestration():
    import importlib
    import src.autonomous_development_system as ads

    importlib.reload(ads)
    system = ads.AutonomousDevelopmentSystem()
    task_id = system.create_development_task("Test", "Desc", "low", 1, 1.0, ["git"])
    summary = system.get_task_summary()
    assert summary["total_tasks"] == 1
    assert system.task_manager.tasks[task_id].title == "Test"
