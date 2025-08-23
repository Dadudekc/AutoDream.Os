#!/usr/bin/env python3
"""
Task Scheduler - Advanced Task Management System
==============================================

Provides intelligent task scheduling with priority management,
dependency resolution, and resource allocation.
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Any, Callable
from queue import PriorityQueue
from dataclasses import dataclass, field
from collections import defaultdict

from .task_types import Task, TaskPriority, TaskStatus, TaskType, TaskCategory

logger = logging.getLogger(__name__)


@dataclass
class SchedulingMetrics:
    """Metrics for monitoring scheduler performance."""

    total_tasks_scheduled: int = 0
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_scheduling_time: float = 0.0
    average_execution_time: float = 0.0
    tasks_by_priority: Dict[TaskPriority, int] = field(default_factory=dict)
    tasks_by_type: Dict[TaskType, int] = field(default_factory=dict)
    last_update: datetime = field(default_factory=datetime.now)


class TaskScheduler:
    """
    Advanced task scheduler with priority management and dependency resolution.

    Features:
    - Priority-based scheduling
    - Dependency resolution
    - Resource allocation
    - Deadline management
    - Load balancing
    - Performance monitoring
    """

    def __init__(self, max_concurrent_tasks: int = 100):
        """
        Initialize the task scheduler.

        Args:
            max_concurrent_tasks: Maximum number of tasks that can run concurrently
        """
        self.max_concurrent_tasks = max_concurrent_tasks
        self._lock = threading.RLock()

        # Task queues by priority
        self._priority_queues: Dict[TaskPriority, PriorityQueue] = {
            priority: PriorityQueue() for priority in TaskPriority
        }

        # Task storage and tracking
        self._tasks: Dict[str, Task] = {}
        self._running_tasks: Dict[str, Task] = {}
        self._completed_tasks: Dict[str, Task] = {}
        self._failed_tasks: Dict[str, Task] = {}

        # Dependency tracking
        self._dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self._reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)

        # Resource tracking
        self._agent_resources: Dict[str, Dict[str, Any]] = {}
        self._resource_locks: Dict[str, threading.Lock] = {}

        # Scheduling metrics
        self._metrics = SchedulingMetrics()

        # Event callbacks
        self._task_callbacks: Dict[str, List[Callable]] = defaultdict(list)

        # Scheduler state
        self._running = False
        self._scheduler_thread: Optional[threading.Thread] = None

        logger.info(
            f"TaskScheduler initialized with max {max_concurrent_tasks} concurrent tasks"
        )

    async def start(self):
        """Start the task scheduler."""
        if self._running:
            logger.warning("Task scheduler already running")
            return

        self._running = True
        self._scheduler_thread = threading.Thread(
            target=self._scheduler_loop, daemon=True
        )
        self._scheduler_thread.start()

        logger.info("Task scheduler started")

    async def stop(self):
        """Stop the task scheduler."""
        if not self._running:
            return

        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)

        logger.info("Task scheduler stopped")

    async def submit_task(self, task: Task) -> bool:
        """
        Submit a task for scheduling.

        Args:
            task: Task to submit

        Returns:
            True if task was successfully submitted, False otherwise
        """
        try:
            with self._lock:
                # Validate task
                if not self._validate_task(task):
                    logger.error(f"Task validation failed for {task.task_id}")
                    return False

                # Store task
                self._tasks[task.task_id] = task

                # Add to priority queue
                priority_score = self._calculate_priority_score(task)
                self._priority_queues[task.priority].put((priority_score, task))

                # Update dependency graph
                self._update_dependency_graph(task)

                # Update metrics
                self._update_metrics(task, "submitted")

                logger.info(f"Task {task.task_id} submitted successfully")
                return True

        except Exception as e:
            logger.error(f"Error submitting task {task.task_id}: {e}")
            return False

    async def get_next_task(self, agent_id: str) -> Optional[Task]:
        """
        Get the next available task for an agent.

        Args:
            agent_id: ID of the agent requesting a task

        Returns:
            Next available task, or None if no tasks available
        """
        try:
            with self._lock:
                # Check if agent can handle more tasks
                if not self._can_agent_handle_task(agent_id):
                    return None

                # Find highest priority task that agent can handle
                for priority in reversed(list(TaskPriority)):
                    task = self._get_next_task_from_priority(priority, agent_id)
                    if task:
                        return task

                return None

        except Exception as e:
            logger.error(f"Error getting next task for agent {agent_id}: {e}")
            return None

    async def complete_task(self, task_id: str, result: Any = None) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id: ID of the completed task
            result: Task execution result

        Returns:
            True if task was successfully completed, False otherwise
        """
        try:
            with self._lock:
                if task_id not in self._running_tasks:
                    logger.error(f"Task {task_id} not found in running tasks")
                    return False

                task = self._running_tasks[task_id]
                task.complete_execution(result)

                # Move to completed tasks
                del self._running_tasks[task_id]
                self._completed_tasks[task_id] = task

                # Release resources
                self._release_agent_resources(task.assigned_agent, task)

                # Update dependency graph
                self._handle_task_completion(task_id)

                # Update metrics
                self._update_metrics(task, "completed")

                # Trigger callbacks
                await self._trigger_task_callbacks("completed", task)

                logger.info(f"Task {task_id} completed successfully")
                return True

        except Exception as e:
            logger.error(f"Error completing task {task_id}: {e}")
            return False

    async def fail_task(self, task_id: str, error_message: str) -> bool:
        """
        Mark a task as failed.

        Args:
            task_id: ID of the failed task
            error_message: Error message describing the failure

        Returns:
            True if task was successfully marked as failed, False otherwise
        """
        try:
            with self._lock:
                if task_id not in self._running_tasks:
                    logger.error(f"Task {task_id} not found in running tasks")
                    return False

                task = self._running_tasks[task_id]
                task.fail_execution(error_message)

                # Handle retry logic
                if task.can_retry():
                    await self._retry_task(task)
                else:
                    # Move to failed tasks
                    del self._running_tasks[task_id]
                    self._failed_tasks[task_id] = task

                    # Release resources
                    self._release_agent_resources(task.assigned_agent, task)

                    # Update metrics
                    self._update_metrics(task, "failed")

                    # Trigger callbacks
                    await self._trigger_task_callbacks("failed", task)

                logger.info(f"Task {task_id} marked as failed: {error_message}")
                return True

        except Exception as e:
            logger.error(f"Error failing task {task_id}: {e}")
            return False

    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a pending or running task.

        Args:
            task_id: ID of the task to cancel

        Returns:
            True if task was successfully cancelled, False otherwise
        """
        try:
            with self._lock:
                # Find task in various states
                task = (
                    self._tasks.get(task_id)
                    or self._running_tasks.get(task_id)
                    or self._completed_tasks.get(task_id)
                    or self._failed_tasks.get(task_id)
                )

                if not task:
                    logger.error(f"Task {task_id} not found")
                    return False

                # Cancel the task
                task.cancel_execution()

                # Remove from appropriate collections
                self._tasks.pop(task_id, None)
                self._running_tasks.pop(task_id, None)

                # Store cancelled task for status tracking
                self._failed_tasks[task_id] = task

                # Release resources if running
                if task.assigned_agent:
                    self._release_agent_resources(task.assigned_agent, task)

                # Update dependency graph
                self._handle_task_cancellation(task_id)

                # Trigger callbacks
                await self._trigger_task_callbacks("cancelled", task)

                logger.info(f"Task {task_id} cancelled successfully")
                return True

        except Exception as e:
            logger.error(f"Error cancelling task {task_id}: {e}")
            return False

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the current status of a task."""
        with self._lock:
            task = (
                self._tasks.get(task_id)
                or self._running_tasks.get(task_id)
                or self._completed_tasks.get(task_id)
                or self._failed_tasks.get(task_id)
            )

            return task.status if task else None

    def get_scheduler_metrics(self) -> SchedulingMetrics:
        """Get current scheduler metrics."""
        with self._lock:
            return self._metrics

    def register_task_callback(self, event_type: str, callback: Callable):
        """Register a callback for task events."""
        self._task_callbacks[event_type].append(callback)

    def _scheduler_loop(self):
        """Main scheduler loop for processing tasks."""
        while self._running:
            try:
                with self._lock:
                    # Process pending tasks
                    self._process_pending_tasks()

                    # Check for expired tasks
                    self._check_expired_tasks()

                    # Clean up old completed tasks
                    self._cleanup_old_tasks()

                # Sleep before next iteration
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)  # Wait longer on error

    def _process_pending_tasks(self):
        """Process pending tasks and assign them to available agents."""
        # This is a simplified implementation
        # In a real system, this would involve complex resource allocation
        # and agent matching logic

        for priority in reversed(list(TaskPriority)):
            while not self._priority_queues[priority].empty():
                if len(self._running_tasks) >= self.max_concurrent_tasks:
                    break

                _, task = self._priority_queues[priority].get()

                if task.is_ready_to_execute():
                    # Find available agent
                    agent_id = self._find_available_agent(task)
                    if agent_id:
                        self._assign_task_to_agent(task, agent_id)

    def _check_expired_tasks(self):
        """Check for and handle expired tasks."""
        current_time = datetime.now()

        # Check running tasks for timeouts
        expired_tasks = []
        for task_id, task in self._running_tasks.items():
            if task.is_expired():
                expired_tasks.append(task_id)

        # Handle expired tasks
        for task_id in expired_tasks:
            asyncio.create_task(self.fail_task(task_id, "Task timeout exceeded"))

    def _cleanup_old_tasks(self):
        """Clean up old completed and failed tasks."""
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=24)

        # Clean up old completed tasks
        old_completed = [
            tid
            for tid, task in self._completed_tasks.items()
            if task.completed_at and task.completed_at < cutoff_time
        ]
        for tid in old_completed:
            del self._completed_tasks[tid]

        # Clean up old failed tasks
        old_failed = [
            tid
            for tid, task in self._failed_tasks.items()
            if task.completed_at and task.completed_at < cutoff_time
        ]
        for tid in old_failed:
            del self._failed_tasks[tid]

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
                base_score += 10.0 / (
                    time_until_deadline + 1
                )  # Higher score for urgent tasks

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
        # Simplified implementation - in practice, this would use a proper cycle detection algorithm
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

    def _can_agent_handle_task(self, agent_id: str) -> bool:
        """Check if an agent can handle additional tasks."""
        # Check current load
        current_tasks = sum(
            1
            for task in self._running_tasks.values()
            if task.assigned_agent == agent_id
        )

        # Simple limit - could be more sophisticated
        return current_tasks < 5

    def _get_next_task_from_priority(
        self, priority: TaskPriority, agent_id: str
    ) -> Optional[Task]:
        """Get next task from a specific priority queue that agent can handle."""
        queue = self._priority_queues[priority]

        # Check all tasks in this priority level
        checked_tasks = []

        while not queue.empty():
            _, task = queue.get()
            checked_tasks.append((priority.value, task))

            if (
                task.status == TaskStatus.PENDING
                and self._can_agent_handle_task(agent_id)
                and self._agent_can_handle_task(task, agent_id)
            ):
                # Put back other tasks
                for score, other_task in checked_tasks:
                    if other_task.task_id != task.task_id:
                        self._priority_queues[priority].put((score, other_task))

                # Mark task as running and assign to agent
                task.start_execution(agent_id)
                self._running_tasks[task.task_id] = task

                return task

        # Put back all tasks
        for score, task in checked_tasks:
            self._priority_queues[priority].put((score, task))

        return None

    def _agent_can_handle_task(self, task: Task, agent_id: str) -> bool:
        """Check if an agent can handle a specific task."""
        # Check resource requirements
        if not self._check_resource_availability(agent_id, task):
            return False

        # Check agent constraints
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
        # Simplified resource checking
        # In practice, this would involve detailed resource tracking
        return True

    def _find_available_agent(self, task: Task) -> Optional[str]:
        """Find an available agent for a task."""
        # Simplified agent selection
        # In practice, this would involve agent capability matching
        # and load balancing

        # For now, return a placeholder agent ID
        return "agent_001"

    def _assign_task_to_agent(self, task: Task, agent_id: str):
        """Assign a task to an agent."""
        task.start_execution(agent_id)
        self._running_tasks[task.task_id] = task

        # Remove from pending tasks
        self._tasks.pop(task.task_id, None)

        # Allocate resources
        self._allocate_agent_resources(agent_id, task)

        logger.info(f"Task {task.task_id} assigned to agent {agent_id}")

    def _allocate_agent_resources(self, agent_id: str, task: Task):
        """Allocate resources for a task on an agent."""
        # Simplified resource allocation
        # In practice, this would involve detailed resource tracking
        pass

    def _release_agent_resources(self, agent_id: str, task: Task):
        """Release resources allocated to a task on an agent."""
        # Simplified resource release
        # In practice, this would involve detailed resource tracking
        pass

    def _handle_task_completion(self, task_id: str):
        """Handle completion of a task and update dependent tasks."""
        # Update dependency graph
        for dependent_id in self._reverse_dependencies.get(task_id, set()):
            dependent_task = self._tasks.get(dependent_id)
            if dependent_task:
                # Check if all dependencies are satisfied
                if self._are_all_dependencies_satisfied(dependent_task):
                    # Task is now ready to execute
                    dependent_task.status = TaskStatus.PENDING

    def _handle_task_cancellation(self, task_id: str):
        """Handle cancellation of a task and update dependent tasks."""
        # Similar to completion handling
        pass

    def _are_all_dependencies_satisfied(self, task: Task) -> bool:
        """Check if all dependencies for a task are satisfied."""
        for dependency in task.dependencies:
            if not self._is_dependency_satisfied(dependency):
                return False
        return True

    def _is_dependency_satisfied(self, dependency: Any) -> bool:
        """Check if a specific dependency is satisfied."""
        # Simplified dependency checking
        # In practice, this would check actual task statuses
        return True

    async def _retry_task(self, task: Task):
        """Retry a failed task."""
        # Reset task status
        task.status = TaskStatus.PENDING
        task.error_message = None

        # Add back to priority queue
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
