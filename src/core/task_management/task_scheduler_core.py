"""Core helper methods for the task scheduler."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

from .task_types import Task, TaskPriority, TaskStatus


logger = logging.getLogger(__name__)


class TaskSchedulerCore:
    """Low level utilities and metric handling for the scheduler."""

    def _validate_task(self, task: Task) -> bool:
        """Validate a task before scheduling."""
        if not task.name:
            return False

        if not task.content:
            return False

        # Check for circular dependencies
        if self._has_circular_dependencies(task):
            return False

        return True

    def _calculate_priority_score(self, task: Task) -> float:
        """Calculate priority score for task ordering."""
        base_score = task.priority.value

        # Factor in deadline urgency
        if task.constraints.deadline:
            time_until_deadline = (
                task.constraints.deadline - datetime.now()
            ).total_seconds()
            if time_until_deadline > 0:
                base_score += 10.0 / (time_until_deadline + 1)

        # Factor in retry count (failed tasks get higher priority)
        base_score += task.retry_count * 2.0

        return base_score

    def _update_dependency_graph(self, task: Task):
        """Update the dependency graph when a task is added."""
        # Add task to graph
        self._dependency_graph[task.task_id] = set()

        # Add dependencies
        for dependency in task.dependencies:
            self._dependency_graph[task.task_id].add(dependency.task_id)
            self._reverse_dependencies[dependency.task_id].add(task.task_id)

    def _has_circular_dependencies(self, task: Task) -> bool:
        """Check if adding a task would create circular dependencies."""
        visited = set()
        rec_stack = set()

        def has_cycle(node_id: str) -> bool:
            if node_id in rec_stack:
                return True
            if node_id in visited:
                return False

            visited.add(node_id)
            rec_stack.add(node_id)

            for dep_id in self._dependency_graph.get(node_id, set()):
                if has_cycle(dep_id):
                    return True

            rec_stack.remove(node_id)
            return False

        return has_cycle(task.task_id)

    def _allocate_agent_resources(self, agent_id: str, task: Task):
        """Allocate resources for a task on an agent."""
        # Simplified resource allocation - placeholder for future logic
        pass

    def _release_agent_resources(self, agent_id: str, task: Task):
        """Release resources allocated to a task on an agent."""
        # Simplified resource release - placeholder for future logic
        pass

    def _handle_task_completion(self, task_id: str):
        """Handle completion of a task and update dependent tasks."""
        for dependent_id in self._reverse_dependencies.get(task_id, set()):
            dependent_task = self._tasks.get(dependent_id)
            if dependent_task:
                if self._are_all_dependencies_satisfied(dependent_task):
                    dependent_task.status = TaskStatus.PENDING

    def _handle_task_cancellation(self, task_id: str):
        """Handle cancellation of a task and update dependent tasks."""
        # Similar to completion handling - placeholder for future logic
        pass

    def _are_all_dependencies_satisfied(self, task: Task) -> bool:
        """Check if all dependencies for a task are satisfied."""
        for dependency in task.dependencies:
            if not self._is_dependency_satisfied(dependency):
                return False
        return True

    def _is_dependency_satisfied(self, dependency: Any) -> bool:
        """Check if a specific dependency is satisfied."""
        # Simplified dependency checking - placeholder for real logic
        return True

    async def _retry_task(self, task: Task):
        """Retry a failed task."""
        task.status = TaskStatus.PENDING
        task.error_message = None
        priority_score = self._calculate_priority_score(task)
        self._priority_queues[task.priority].put((priority_score, task))
        logger.info(f"Task {task.task_id} scheduled for retry")

    def _update_metrics(self, task: Task, action: str):
        """Update scheduler metrics."""
        self._metrics.last_update = datetime.now()

        if action == "submitted":
            self._metrics.total_tasks_scheduled += 1
            self._metrics.tasks_by_priority[task.priority] = (
                self._metrics.tasks_by_priority.get(task.priority, 0) + 1
            )
            self._metrics.tasks_by_type[task.type] = (
                self._metrics.tasks_by_type.get(task.type, 0) + 1
            )
        elif action == "completed":
            self._metrics.total_tasks_completed += 1
        elif action == "failed":
            self._metrics.total_tasks_failed += 1

    async def _trigger_task_callbacks(self, event_type: str, task: Task):
        """Trigger callbacks for task events."""
        callbacks = self._task_callbacks.get(event_type, [])

        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(task)
                else:
                    callback(task)
            except Exception as e:
                logger.error(f"Error in task callback {event_type}: {e}")

    def __str__(self) -> str:
        """String representation of the scheduler."""
        return f"TaskScheduler(running={self._running}, tasks={len(self._tasks)})"

