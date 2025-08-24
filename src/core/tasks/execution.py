#!/usr/bin/env python3
"""
Task Executor - Agent Cellphone V2
=================================

Handles task execution, workflow management, and development task operations.
Single responsibility: Task execution and workflow management.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
import json

from src.utils.stability_improvements import stability_manager, safe_import

# Development task dependencies - Mocked to avoid circular imports
# from autonomous_development.core.models import DevelopmentTask
# from autonomous_development.core.enums import (
#     TaskPriority as DevTaskPriority,
#     TaskComplexity,
#     TaskStatus as DevTaskStatus,
# )

# Mock classes to avoid circular imports
class DevelopmentTask:
    """Mock DevelopmentTask class to avoid circular imports."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.status = MockTaskStatus.AVAILABLE
        self.claimed_by = None
        self.completed_at = None
        self.started_at = None
        self.metadata = {}
    
    def is_available(self):
        return self.status == MockTaskStatus.AVAILABLE
    
    def claim(self, agent_id):
        if self.is_available():
            self.claimed_by = agent_id
            self.status = MockTaskStatus.CLAIMED
            return True
        return False
    
    def start_work(self):
        if self.status == MockTaskStatus.CLAIMED:
            self.status = MockTaskStatus.IN_PROGRESS
            self.started_at = datetime.now().isoformat()
            return True
        return False
    
    def complete(self):
        if self.status in [MockTaskStatus.IN_PROGRESS, MockTaskStatus.CLAIMED]:
            self.status = MockTaskStatus.COMPLETED
            self.completed_at = datetime.now().isoformat()
            return True
        return False
    
    def block(self, reason):
        if self.status != MockTaskStatus.COMPLETED:
            self.status = MockTaskStatus.BLOCKED
            if not self.metadata:
                self.metadata = {}
            self.metadata['block_reason'] = reason
            return True
        return False
    
    def unblock(self):
        if self.status == MockTaskStatus.BLOCKED:
            self.status = MockTaskStatus.CLAIMED
            return True
        return False
    
    def cancel(self):
        if self.status != MockTaskStatus.COMPLETED:
            self.status = MockTaskStatus.CANCELLED
            return True
        return False
    
    def update_progress(self, percentage):
        if hasattr(self, 'progress'):
            self.progress = max(0, min(100, percentage))
            return True
        return False
    
    def get_elapsed_time(self):
        if self.started_at and self.completed_at:
            start = datetime.fromisoformat(self.started_at)
            end = datetime.fromisoformat(self.completed_at)
            return (end - start).total_seconds() / 3600  # hours
        return None
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class MockTaskStatus:
    """Mock TaskStatus enum to avoid circular imports."""
    AVAILABLE = "available"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class MockTaskPriority:
    """Mock TaskPriority enum to avoid circular imports."""
    MINIMAL = type('MockPriority', (), {'value': 1})()
    LOW = type('MockPriority', (), {'value': 2})()
    MEDIUM = type('MockPriority', (), {'value': 3})()
    HIGH = type('MockPriority', (), {'value': 4})()
    CRITICAL = type('MockPriority', (), {'value': 5})()
    
    def __new__(cls, value):
        """Make the class callable to simulate enum behavior."""
        if value == 1:
            return cls.MINIMAL
        elif value == 2:
            return cls.LOW
        elif value == 3:
            return cls.MEDIUM
        elif value == 4:
            return cls.HIGH
        elif value == 5:
            return cls.CRITICAL
        else:
            raise ValueError(f"'{value}' is not a valid MockTaskPriority")
    
    def __getitem__(cls, key):
        """Make the class subscriptable to simulate enum behavior."""
        if key == 'MINIMAL':
            return cls.MINIMAL
        elif key == 'LOW':
            return cls.LOW
        elif key == 'MEDIUM':
            return cls.MEDIUM
        elif key == 'HIGH':
            return cls.HIGH
        elif key == 'CRITICAL':
            return cls.CRITICAL
        else:
            raise KeyError(f"'{key}' is not a valid MockTaskPriority key")

class MockTaskComplexity:
    """Mock TaskComplexity enum to avoid circular imports."""
    LOW = type('MockComplexity', (), {'value': 'low'})()
    MEDIUM = type('MockComplexity', (), {'value': 'medium'})()
    HIGH = type('MockComplexity', (), {'value': 'high'})()
    
    def __new__(cls, value):
        """Make the class callable to simulate enum behavior."""
        if value == 'low':
            return cls.LOW
        elif value == 'medium':
            return cls.MEDIUM
        elif value == 'high':
            return cls.HIGH
        else:
            raise ValueError(f"'{value}' is not a valid MockTaskComplexity")


class TaskExecutor:
    """
    Task Executor - Single responsibility: Task execution and workflow management.
    
    This service handles:
    - Task execution and workflow management
    - Development task operations
    - Task progress tracking
    - Task completion and blocking
    """

    def __init__(self):
        """Initialize Task Executor."""
        self.tasks: Dict[str, DevelopmentTask] = {}
        self.task_counter = 0
        self.logger = logging.getLogger(__name__)
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
                "required_skills": ["security", "code_review", "vulnerability_assessment"],
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

    def get_tasks_by_priority(self, min_priority: int = MockTaskPriority.MINIMAL.value) -> List[DevelopmentTask]:
        """Get development tasks by minimum priority."""
        return [
            task
            for task in self.tasks.values()
            if task.status == MockTaskStatus.AVAILABLE and task.priority.value >= min_priority
        ]

    def get_tasks_by_complexity(self, complexity: MockTaskComplexity) -> List[DevelopmentTask]:
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

    def get_task_statistics(self) -> Dict[str, any]:
        """Get comprehensive task statistics."""
        total_tasks = len(self.tasks)
        available_tasks = len(self.get_available_tasks())
        claimed_tasks = len(self.get_tasks_by_status(MockTaskStatus.CLAIMED))
        in_progress_tasks = len(self.get_tasks_by_status(MockTaskStatus.IN_PROGRESS))
        completed_tasks = len(self.get_tasks_by_status(MockTaskStatus.COMPLETED))
        blocked_tasks = len(self.get_tasks_by_status(MockTaskStatus.BLOCKED))

        completed_task_times = []
        for task in self.get_tasks_by_status(MockTaskStatus.COMPLETED):
            elapsed = task.get_elapsed_time()
            if elapsed is not None:
                completed_task_times.append(elapsed)

        avg_completion_time = (
            sum(completed_task_times) / len(completed_task_times)
            if completed_tasks > 0
            else 0
        )

        return {
            "total_tasks": total_tasks,
            "available_tasks": available_tasks,
            "claimed_tasks": claimed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "blocked_tasks": blocked_tasks,
            "avg_completion_time_hours": avg_completion_time,
            "workflow_stats": self.workflow_stats.copy(),
        }

    def get_task_summary(self) -> Dict[str, any]:
        """Get task summary with completion rate."""
        stats = self.get_task_statistics()
        total = stats["total_tasks"]
        completed = stats["completed_tasks"]
        stats["completion_rate"] = (completed / total * 100) if total else 0
        return stats

    def get_priority_distribution(self) -> Dict[str, int]:
        """Get distribution of tasks by priority."""
        distribution = {}
        for priority in MockTaskPriority:
            distribution[priority.name] = len(
                [t for t in self.tasks.values() if t.priority == priority]
            )
        return distribution

    def get_complexity_distribution(self) -> Dict[str, int]:
        """Get distribution of tasks by complexity."""
        distribution = {}
        for complexity in MockTaskComplexity:
            distribution[complexity.name] = len(
                [t for t in self.tasks.values() if t.complexity == complexity]
            )
        return distribution

    def cleanup_completed_tasks(self, days_old: int = 30) -> int:
        """Clean up old completed tasks."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        removed_count = 0
        to_remove = []
        for task_id, task in self.tasks.items():
            if task.is_completed() and task.completed_at and task.completed_at < cutoff_date:
                to_remove.append(task_id)
        for task_id in to_remove:
            del self.tasks[task_id]
            removed_count += 1
        self.logger.info(f"Removed {removed_count} old completed tasks")
        return removed_count

    def export_tasks(self) -> List[Dict[str, any]]:
        """Export all tasks to dictionary format."""
        return [task.to_dict() for task in self.tasks.values()]

    def import_tasks(self, tasks_data: List[Dict[str, any]]) -> int:
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
