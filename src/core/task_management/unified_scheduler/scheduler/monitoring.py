from __future__ import annotations

import logging
from datetime import datetime
from typing import Callable, Dict, Optional

from ..enums import TaskPriority
from ..metrics import SchedulingMetrics
from ..models import Task

logger = logging.getLogger(__name__)


class MonitoringMixin:
    """Metrics tracking and callback management."""

    def _update_metrics(self, task: Task, action: str):
        """Update scheduling metrics."""
        if action == "submitted":
            self._metrics.total_tasks_scheduled += 1
            self._metrics.tasks_by_priority[task.priority] = (
                self._metrics.tasks_by_priority.get(task.priority, 0) + 1
            )
            self._metrics.tasks_by_type[task.task_type] = (
                self._metrics.tasks_by_type.get(task.task_type, 0) + 1
            )
        elif action == "completed":
            self._metrics.total_tasks_completed += 1
        elif action == "failed":
            self._metrics.total_tasks_failed += 1

        self._metrics.last_update = datetime.now()

    def get_metrics(self) -> SchedulingMetrics:
        """Get current scheduling metrics."""
        return self._metrics

    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get status of a specific task."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> Dict[str, Task]:
        """Get all tasks in the system."""
        return self._tasks.copy()

    def get_running_tasks(self) -> Dict[str, Task]:
        """Get all currently running tasks."""
        return self._running_tasks.copy()

    def get_completed_tasks(self) -> Dict[str, Task]:
        """Get all completed tasks."""
        return self._completed_tasks.copy()

    def get_failed_tasks(self) -> Dict[str, Task]:
        """Get all failed tasks."""
        return self._failed_tasks.copy()

    def add_task_callback(self, event: str, callback: Callable):
        """Add a callback for task events."""
        self._task_callbacks[event].append(callback)

    def remove_task_callback(self, event: str, callback: Callable):
        """Remove a callback for task events."""
        if event in self._task_callbacks and callback in self._task_callbacks[event]:
            self._task_callbacks[event].remove(callback)

    def _trigger_task_callbacks(self, event: str, task: Task):
        """Trigger callbacks for a task event."""
        if event in self._task_callbacks:
            for callback in self._task_callbacks[event]:
                try:
                    callback(task)
                except Exception as e:
                    logger.error(f"Error in task callback for event {event}: {e}")

    def run_smoke_test(self) -> bool:
        """Run smoke test for unified task scheduler."""
        try:
            logger.info("🧪 Running Unified Task Scheduler smoke test...")

            # Test basic initialization
            assert len(self._tasks) == 0
            assert len(self._priority_queues) == len(TaskPriority)
            logger.info("✅ Basic initialization passed")

            # Test task creation and submission
            test_task = Task(
                name="Test Task", content="Test content", priority=TaskPriority.NORMAL
            )

            # Test task validation
            assert self._validate_task(test_task)
            logger.info("✅ Task validation passed")

            # Test priority score calculation
            score = self._calculate_priority_score(test_task)
            assert score >= 0
            logger.info("✅ Priority score calculation passed")

            logger.info("🎯 Unified Task Scheduler smoke test PASSED")
            return True

        except Exception as exc:
            logger.error(f"❌ Unified Task Scheduler smoke test FAILED: {exc}")
            return False
