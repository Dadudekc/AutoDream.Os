"""Task coordination and assignment helpers for the scheduler."""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Optional

from .task_types import Task, TaskPriority, TaskStatus


logger = logging.getLogger(__name__)


class TaskSchedulerCoordinator:
    """Methods responsible for coordinating task execution."""

    def _scheduler_loop(self):
        """Main scheduler loop for processing tasks."""
        while self._running:
            try:
                with self._lock:
                    self._process_pending_tasks()
                    self._check_expired_tasks()
                    self._cleanup_old_tasks()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)

    def _process_pending_tasks(self):
        """Process pending tasks and assign them to available agents."""
        for priority in reversed(list(TaskPriority)):
            while not self._priority_queues[priority].empty():
                if len(self._running_tasks) >= self.max_concurrent_tasks:
                    break

                _, task = self._priority_queues[priority].get()

                if task.is_ready_to_execute():
                    agent_id = self._find_available_agent(task)
                    if agent_id:
                        self._assign_task_to_agent(task, agent_id)

    def _check_expired_tasks(self):
        """Check for and handle expired tasks."""
        current_time = datetime.now()

        expired_tasks = []
        for task_id, task in self._running_tasks.items():
            if task.is_expired():
                expired_tasks.append(task_id)

        for task_id in expired_tasks:
            asyncio.create_task(self.fail_task(task_id, "Task timeout exceeded"))

    def _cleanup_old_tasks(self):
        """Clean up old completed and failed tasks."""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=24)

        old_completed = [
            tid
            for tid, task in self._completed_tasks.items()
            if task.completed_at and task.completed_at < cutoff_time
        ]
        for tid in old_completed:
            del self._completed_tasks[tid]

        old_failed = [
            tid
            for tid, task in self._failed_tasks.items()
            if task.completed_at and task.completed_at < cutoff_time
        ]
        for tid in old_failed:
            del self._failed_tasks[tid]

    def _can_agent_handle_task(self, agent_id: str) -> bool:
        """Check if an agent can handle additional tasks."""
        current_tasks = sum(
            1
            for task in self._running_tasks.values()
            if task.assigned_agent == agent_id
        )
        return current_tasks < 5

    def _get_next_task_from_priority(
        self, priority: TaskPriority, agent_id: str
    ) -> Optional[Task]:
        """Get next task from a specific priority queue that agent can handle."""
        queue = self._priority_queues[priority]

        checked_tasks = []

        while not queue.empty():
            _, task = queue.get()
            checked_tasks.append((priority.value, task))

            if (
                task.status == TaskStatus.PENDING
                and self._can_agent_handle_task(agent_id)
                and self._agent_can_handle_task(task, agent_id)
            ):
                for score, other_task in checked_tasks:
                    if other_task.task_id != task.task_id:
                        self._priority_queues[priority].put((score, other_task))

                task.start_execution(agent_id)
                self._running_tasks[task.task_id] = task

                return task

        for score, task in checked_tasks:
            self._priority_queues[priority].put((score, task))

        return None

    def _agent_can_handle_task(self, task: Task, agent_id: str) -> bool:
        """Check if an agent can handle a specific task."""
        if not self._check_resource_availability(agent_id, task):
            return False

        if agent_id in task.constraints.excluded_agents:
            return False

        if (
            task.constraints.required_agents
            and agent_id not in task.constraints.required_agents
        ):
            return False

        return True

    def _check_resource_availability(self, agent_id: str, task: Task) -> bool:
        """Check if required resources are available for a task."""
        return True

    def _find_available_agent(self, task: Task) -> Optional[str]:
        """Find an available agent for a task."""
        return "agent_001"

    def _assign_task_to_agent(self, task: Task, agent_id: str):
        """Assign a task to an agent."""
        task.start_execution(agent_id)
        self._running_tasks[task.task_id] = task

        self._tasks.pop(task.task_id, None)

        self._allocate_agent_resources(agent_id, task)

        logger.info(f"Task {task.task_id} assigned to agent {agent_id}")

