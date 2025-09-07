from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

from ..enums import TaskPriority, TaskStatus
from ..models import Task

logger = logging.getLogger(__name__)


class SchedulingMixin:
    """Internal scheduling and coordination helpers."""

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
        self._dependency_graph[task.task_id] = set()

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

            if self._can_agent_handle_task(agent_id):
                for _, t in checked_tasks[:-1]:
                    self._priority_queues[priority].put((priority.value, t))
                return task

        for _, task in checked_tasks:
            self._priority_queues[priority].put((priority.value, task))

        return None

    def _find_available_agent(self, task: Task) -> Optional[str]:
        """Find an available agent for a task."""
        available_agents = [
            agent_id
            for agent_id in self._agent_resources.keys()
            if self._can_agent_handle_task(agent_id)
        ]
        return available_agents[0] if available_agents else None

    def _assign_task_to_agent(self, task: Task, agent_id: str):
        """Assign a task to an agent."""
        task.assigned_agent = agent_id
        task.status = TaskStatus.RUNNING
        task.assigned_at = datetime.now()
        task.started_at = datetime.now()

        self._running_tasks[task.task_id] = task
        self._allocate_agent_resources(agent_id, task)

        logger.info(f"Task {task.task_id} assigned to agent {agent_id}")

    def _handle_task_completion(self, task_id: str):
        """Handle completion of a task and update dependent tasks."""
        for dependent_id in self._reverse_dependencies.get(task_id, set()):
            dependent_task = self._tasks.get(dependent_id)
            if dependent_task:
                if self._are_all_dependencies_satisfied(dependent_task):
                    dependent_task.status = TaskStatus.PENDING

    def _are_all_dependencies_satisfied(self, task: Task) -> bool:
        """Check if all dependencies for a task are satisfied."""
        for dep in task.dependencies:
            if dep.task_id not in self._completed_tasks:
                return False
        return True

    def _allocate_agent_resources(self, agent_id: str, task: Task):
        """Allocate resources for a task on an agent."""
        pass

    def _release_agent_resources(self, agent_id: str, task: Task):
        """Release resources allocated to a task on an agent."""
        pass
