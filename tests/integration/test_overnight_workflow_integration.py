#!/usr/bin/env python3
"""Integration test for overnight workflow."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from src.autonomous_development.agents.coordinator import AgentCoordinator


class DummyTaskManager:
    """Simple in-memory task manager for integration testing."""

    def __init__(self):
        self.tasks = {}
        self.workflow_stats = {
            "overnight_cycles": 0,
            "autonomous_hours": 0,
            "total_tasks_completed": 0,
        }

    def create_task(
        self, title, description, complexity, priority, estimated_hours, required_skills
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

    def start_task_work(self, task_id):
        task = self.tasks.get(task_id)
        if task and task.status == "claimed":
            task.status = "in_progress"

    def update_task_progress(self, task_id, progress, blockers=None):
        task = self.tasks.get(task_id)
        if task and task.status == "in_progress":
            task.progress_percentage = progress
            task.blockers = blockers or []
            if progress >= 100:
                task.status = "completed"
                self.workflow_stats["total_tasks_completed"] += 1

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


class DeterministicAgentCoordinator(AgentCoordinator):
    """Agent coordinator with deterministic skills for testing."""

    def _generate_agent_skills(self, agent_id):
        return ["git"]


@patch.dict(
    "sys.modules",
    {
        "src.core.task_manager": SimpleNamespace(
            DevelopmentTaskManager=DummyTaskManager
        ),
        "src.services.messaging": SimpleNamespace(
            UnifiedMessagingService=lambda: SimpleNamespace(
                send_message_to_all_agents_with_line_breaks=AsyncMock(),
                send_message_to_agent_with_line_breaks=AsyncMock(),
                send_message_to_agent=AsyncMock(),
            )
        ),
        "src.autonomous_development.agents.coordinator": SimpleNamespace(
            AgentCoordinator=DeterministicAgentCoordinator
        ),
    },
)
def test_overnight_workflow_cycle():
    from src.autonomous_development_system import AutonomousDevelopmentSystem

    system = AutonomousDevelopmentSystem()
    task_id = system.create_development_task("Test", "Desc", "low", 1, 1.0, ["git"])
    system.workflow_manager.cycle_duration = 0
    asyncio.run(system.workflow_manager._execute_workflow_cycle())
    summary = system.get_task_summary()
    assert summary["workflow_stats"]["overnight_cycles"] == 1
    assert task_id in system.task_manager.tasks
