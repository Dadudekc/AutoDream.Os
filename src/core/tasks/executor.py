#!/usr/bin/env python3
"""Task execution engine for development tasks."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from .definitions import (
    DevelopmentTask,
    MockTaskStatus,
    MockTaskPriority,
    MockTaskComplexity,
)
from .logger import get_task_logger
from .results import (
    get_task_statistics as _get_task_statistics,
    get_task_summary as _get_task_summary,
    get_priority_distribution as _get_priority_distribution,
    get_complexity_distribution as _get_complexity_distribution,
)


class TaskExecutor:
    """Manage task lifecycle and workflow operations."""

    def __init__(self):
        """Initialize Task Executor."""
        self.tasks: Dict[str, DevelopmentTask] = {}
        self.task_counter = 0
        self.logger = get_task_logger(__name__)
        self.workflow_stats = {
            "total_tasks_created": 0,
            "total_tasks_completed": 0,
            "total_tasks_claimed": 0,
            "overnight_cycles": 0,
            "autonomous_hours": 0,
        }

        # Initialize with sample tasks for development
        self._initialize_sample_tasks()

    def _initialize_sample_tasks(self):
        """Initialize with sample development tasks."""
        sample_tasks = [
            {
                "title": "Repository Cleanup and Optimization",
                "description": "Clean up unused files, optimize imports, and improve code structure",
                "complexity": MockTaskComplexity.MEDIUM,
                "priority": MockTaskPriority.HIGH,
                "estimated_hours": 2.0,
                "required_skills": ["git", "code_analysis", "optimization"],
            },
            {
                "title": "Documentation Update",
                "description": "Update README files, add inline comments, and improve API documentation",
                "complexity": MockTaskComplexity.LOW,
                "priority": MockTaskPriority.MEDIUM,
                "estimated_hours": 1.5,
                "required_skills": ["documentation", "markdown", "api_design"],
            },
            {
                "title": "Test Coverage Improvement",
                "description": "Increase test coverage, add missing unit tests, and improve test quality",
                "complexity": MockTaskComplexity.MEDIUM,
                "priority": MockTaskPriority.HIGH,
                "estimated_hours": 3.0,
                "required_skills": ["testing", "unittest", "coverage"],
            },
            {
                "title": "Performance Optimization",
                "description": "Identify and fix performance bottlenecks, optimize algorithms",
                "complexity": MockTaskComplexity.HIGH,
                "priority": MockTaskPriority.MEDIUM,
                "estimated_hours": 4.0,
                "required_skills": ["profiling", "optimization", "algorithms"],
            },
            {
                "title": "Security Audit",
                "description": "Review code for security vulnerabilities and implement fixes",
                "complexity": MockTaskComplexity.HIGH,
                "priority": MockTaskPriority.CRITICAL,
                "estimated_hours": 5.0,
                "required_skills": [
                    "security",
                    "code_review",
                    "vulnerability_assessment",
                ],
            },
        ]

        for task_data in sample_tasks:
            self.create_task(**task_data)

    def create_task(
        self,
        title: str,
        description: str,
        complexity: MockTaskComplexity | str,
        priority: MockTaskPriority | int | str,
        estimated_hours: float,
        required_skills: List[str],
        tags: Optional[List[str]] = None,
    ) -> str:
        """Create a new development task."""
        self.task_counter += 1
        task_id = f"task_{self.task_counter:04d}"

        if isinstance(complexity, str):
            complexity = MockTaskComplexity(complexity)
        if isinstance(priority, int):
            priority = MockTaskPriority(priority)
        elif isinstance(priority, str):
            priority = MockTaskPriority[priority.upper()]

        task = DevelopmentTask(
            task_id=task_id,
            title=title,
            description=description,
            complexity=complexity,
            priority=priority,
            estimated_hours=estimated_hours,
            required_skills=required_skills,
            tags=tags or [],
        )

        self.tasks[task_id] = task
        self.workflow_stats["total_tasks_created"] += 1
        self.logger.info(f"Created task {task_id}: {title}")
        return task_id

    def get_task(self, task_id: str) -> Optional[DevelopmentTask]:
        """Get a specific development task by ID."""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[DevelopmentTask]:
        """Get all development tasks."""
        return list(self.tasks.values())

    def get_available_tasks(self) -> List[DevelopmentTask]:
        """Get all available development tasks."""
        return [task for task in self.tasks.values() if task.is_available()]

    def get_tasks_by_status(self, status: MockTaskStatus) -> List[DevelopmentTask]:
        """Get development tasks by status."""
        return [task for task in self.tasks.values() if task.status == status]

    def get_tasks_by_priority(
        self, min_priority: int = MockTaskPriority.MINIMAL.value
    ) -> List[DevelopmentTask]:
        """Get development tasks by minimum priority."""
        return [
            task
            for task in self.tasks.values()
            if task.status == MockTaskStatus.AVAILABLE
            and task.priority.value >= min_priority
        ]

    def get_tasks_by_complexity(
        self, complexity: MockTaskComplexity
    ) -> List[DevelopmentTask]:
        """Get development tasks by complexity."""
        return [task for task in self.tasks.values() if task.complexity == complexity]

    def get_tasks_by_agent(self, agent_id: str) -> List[DevelopmentTask]:
        """Get development tasks claimed by a specific agent."""
        return [task for task in self.tasks.values() if task.claimed_by == agent_id]

    def claim_task(self, task_id: str, agent_id: str) -> bool:
        """Claim a development task for an agent."""
        task = self.get_task(task_id)
        if not task:
            return False

        if task.claim(agent_id):
            self.workflow_stats["total_tasks_claimed"] += 1
            self.logger.info(f"Agent {agent_id} claimed task {task_id}")
            return True
        return False

    def start_task_work(self, task_id: str) -> bool:
        """Start work on a development task."""
        task = self.get_task(task_id)
        if not task:
            return False
        return task.start_work()

    def update_task_progress(self, task_id: str, percentage: float) -> bool:
        """Update progress on a development task."""
        task = self.get_task(task_id)
        if not task:
            return False
        return task.update_progress(percentage)

    def complete_task(self, task_id: str) -> bool:
        """Complete a development task."""
        task = self.get_task(task_id)
        if not task:
            return False
        if task.complete():
            self.workflow_stats["total_tasks_completed"] += 1
            self.logger.info(f"Task {task_id} completed by {task.claimed_by}")
            return True
        return False

    def block_task(self, task_id: str, reason: str) -> bool:
        """Block a development task."""
        task = self.get_task(task_id)
        if not task:
            return False
        return task.block(reason)

    def unblock_task(self, task_id: str) -> bool:
        """Unblock a development task."""
        task = self.get_task(task_id)
        if not task:
            return False
        return task.unblock()

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a development task."""
        task = self.get_task(task_id)
        if not task:
            return False
        return task.cancel()

    def get_task_statistics(self) -> Dict[str, Any]:
        """Aggregate statistics for current tasks."""
        return _get_task_statistics(self.tasks, self.workflow_stats)

    def get_task_summary(self) -> Dict[str, Any]:
        """Task statistics with completion rate."""
        return _get_task_summary(self.tasks, self.workflow_stats)

    def get_priority_distribution(self) -> Dict[str, int]:
        """Distribution of tasks by priority."""
        return _get_priority_distribution(self.tasks)

    def get_complexity_distribution(self) -> Dict[str, int]:
        """Distribution of tasks by complexity."""
        return _get_complexity_distribution(self.tasks)

    def cleanup_completed_tasks(self, days_old: int = 30) -> int:
        """Clean up old completed tasks."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        removed_count = 0
        to_remove = []
        for task_id, task in self.tasks.items():
            if (
                task.is_completed()
                and task.completed_at
                and task.completed_at < cutoff_date
            ):
                to_remove.append(task_id)
        for task_id in to_remove:
            del self.tasks[task_id]
            removed_count += 1
        self.logger.info(f"Removed {removed_count} old completed tasks")
        return removed_count

    def export_tasks(self) -> List[Dict[str, Any]]:
        """Export all tasks to dictionary format."""
        return [task.to_dict() for task in self.tasks.values()]

    def import_tasks(self, tasks_data: List[Dict[str, Any]]) -> int:
        """Import tasks from dictionary format."""
        imported_count = 0
        for task_data in tasks_data:
            try:
                task = DevelopmentTask.from_dict(task_data)
                self.tasks[task.task_id] = task
                imported_count += 1
            except Exception as e:
                self.logger.error(f"Failed to import task: {e}")
        self.logger.info(f"Imported {imported_count} tasks")
        return imported_count
