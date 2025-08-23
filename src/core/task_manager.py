#!/usr/bin/env python3
"""
Task Manager - Agent Cellphone V2
================================

Manages agent task management with strict OOP design.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

# Development task dependencies
from autonomous_development.core.models import DevelopmentTask
from autonomous_development.core.enums import (
    TaskPriority as DevTaskPriority,
    TaskComplexity,
    TaskStatus as DevTaskStatus,
)


class TaskPriority(Enum):
    """Task priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(Enum):
    """Task status states."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Task data structure."""

    task_id: str
    title: str
    description: str
    assigned_to: str
    created_by: str
    priority: TaskPriority
    status: TaskStatus
    created_at: str
    due_date: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    dependencies: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class TaskManager:
    """
    Task Manager - Single responsibility: Agent task management.

    This service manages:
    - Task creation and assignment
    - Task status tracking
    - Task dependencies and relationships
    - Task prioritization and scheduling
    """

    def __init__(self, workspace_manager):
        """Initialize Task Manager with workspace manager."""
        self.workspace_manager = workspace_manager
        self.logger = self._setup_logging()
        self.tasks: Dict[str, Task] = {}
        self.status = "initialized"

        # Load existing tasks
        self._load_tasks()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("TaskManager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_tasks(self):
        """Load existing tasks from all workspaces."""
        try:
            for workspace in self.workspace_manager.get_all_workspaces():
                tasks_path = Path(workspace.tasks_path)
                if tasks_path.exists():
                    for task_file in tasks_path.glob("*.json"):
                        try:
                            with open(task_file, "r") as f:
                                task_data = json.load(f)
                                task = Task(**task_data)
                                self.tasks[task.task_id] = task
                        except Exception as e:
                            self.logger.error(
                                f"Failed to load task from {task_file}: {e}"
                            )

            self.logger.info(f"Loaded {len(self.tasks)} existing tasks")
        except Exception as e:
            self.logger.error(f"Failed to load tasks: {e}")

    def _generate_task_id(self, title: str, assigned_to: str) -> str:
        """Generate unique task ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe_title = "".join(
            c for c in title if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_title = safe_title.replace(" ", "_")[:20]
        return f"{safe_title}_{assigned_to}_{timestamp}"

    def create_task(
        self,
        title: str,
        description: str,
        assigned_to: str,
        created_by: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        due_date: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Create a new task."""
        try:
            # Generate task ID
            task_id = self._generate_task_id(title, assigned_to)

            # Create task
            task = Task(
                task_id=task_id,
                title=title,
                description=description,
                assigned_to=assigned_to,
                created_by=created_by,
                priority=priority,
                status=TaskStatus.PENDING,
                created_at=datetime.now().isoformat(),
                due_date=due_date,
                dependencies=dependencies or [],
                metadata=metadata or {},
            )

            # Store task
            self.tasks[task_id] = task

            # Save to assigned agent's workspace
            assigned_workspace = self.workspace_manager.get_workspace_info(assigned_to)
            if assigned_workspace:
                tasks_path = Path(assigned_workspace.tasks_path)
                task_file = tasks_path / f"{task_id}.json"

                with open(task_file, "w") as f:
                    json.dump(task.__dict__, f, indent=2, default=str)

                self.logger.info(f"Task created: {task_id} assigned to {assigned_to}")
                return task_id
            else:
                self.logger.error(f"Assigned agent workspace not found: {assigned_to}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to create task: {e}")
            return None

    def get_tasks(
        self,
        agent_id: str,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> List[Task]:
        """Get tasks for an agent with optional filtering."""
        try:
            tasks = []
            for task in self.tasks.values():
                if task.assigned_to == agent_id:
                    if status and task.status != status:
                        continue
                    if priority and task.priority != priority:
                        continue
                    tasks.append(task)

            # Sort by priority and creation time
            priority_order = {
                TaskPriority.CRITICAL: 0,
                TaskPriority.HIGH: 1,
                TaskPriority.NORMAL: 2,
                TaskPriority.LOW: 3,
            }

            tasks.sort(key=lambda t: (priority_order[t.priority], t.created_at))
            return tasks

        except Exception as e:
            self.logger.error(f"Failed to get tasks for {agent_id}: {e}")
            return []

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        return self.tasks.get(task_id)

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                old_status = task.status
                task.status = status

                # Update timestamps
                if status == TaskStatus.IN_PROGRESS and not task.started_at:
                    task.started_at = datetime.now().isoformat()
                elif status == TaskStatus.COMPLETED:
                    task.completed_at = datetime.now().isoformat()

                # Update file
                assigned_workspace = self.workspace_manager.get_workspace_info(
                    task.assigned_to
                )
                if assigned_workspace:
                    tasks_path = Path(assigned_workspace.tasks_path)
                    task_file = tasks_path / f"{task_id}.json"

                    with open(task_file, "w") as f:
                        json.dump(task.__dict__, f, indent=2, default=str)

                    self.logger.info(
                        f"Task status updated: {task_id} {old_status.value} -> {status.value}"
                    )
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update task status: {e}")
            return False

    def assign_task(self, task_id: str, new_agent: str) -> bool:
        """Reassign a task to a different agent."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                old_agent = task.assigned_to

                # Check if new agent workspace exists
                new_workspace = self.workspace_manager.get_workspace_info(new_agent)
                if not new_workspace:
                    self.logger.error(f"New agent workspace not found: {new_agent}")
                    return False

                # Remove from old workspace
                old_workspace = self.workspace_manager.get_workspace_info(old_agent)
                if old_workspace:
                    old_task_file = Path(old_workspace.tasks_path) / f"{task_id}.json"
                    if old_task_file.exists():
                        old_task_file.unlink()

                # Update task
                task.assigned_to = new_agent
                task.status = TaskStatus.PENDING  # Reset status for new agent

                # Save to new workspace
                new_task_file = Path(new_workspace.tasks_path) / f"{task_id}.json"
                with open(new_task_file, "w") as f:
                    json.dump(task.__dict__, f, indent=2, default=str)

                self.logger.info(
                    f"Task reassigned: {task_id} {old_agent} -> {new_agent}"
                )
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to reassign task: {e}")
            return False

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]

                # Remove from file system
                assigned_workspace = self.workspace_manager.get_workspace_info(
                    task.assigned_to
                )
                if assigned_workspace:
                    tasks_path = Path(assigned_workspace.tasks_path)
                    task_file = tasks_path / f"{task_id}.json"

                    if task_file.exists():
                        task_file.unlink()

                # Remove from memory
                del self.tasks[task_id]

                self.logger.info(f"Task deleted: {task_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete task: {e}")
            return False

    def get_task_status(self, agent_id: str) -> Dict[str, Any]:
        """Get task status for an agent."""
        try:
            tasks = self.get_tasks(agent_id)

            status_counts = {}
            for status in TaskStatus:
                status_counts[status.value] = len(
                    [t for t in tasks if t.status == status]
                )

            priority_counts = {}
            for priority in TaskPriority:
                priority_counts[priority.value] = len(
                    [t for t in tasks if t.priority == priority]
                )

            pending_tasks = [t for t in tasks if t.status == TaskStatus.PENDING]
            critical_tasks = [t for t in tasks if t.priority == TaskPriority.CRITICAL]

            return {
                "agent_id": agent_id,
                "total_tasks": len(tasks),
                "status_counts": status_counts,
                "priority_counts": priority_counts,
                "pending_count": len(pending_tasks),
                "critical_count": len(critical_tasks),
                "overdue_count": len(
                    [
                        t
                        for t in tasks
                        if t.due_date and t.due_date < datetime.now().isoformat()
                    ]
                ),
            }

        except Exception as e:
            self.logger.error(f"Failed to get task status for {agent_id}: {e}")
            return {"agent_id": agent_id, "error": str(e)}

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall task system status."""
        try:
            total_tasks = len(self.tasks)
            pending_tasks = len(
                [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
            )
            critical_tasks = len(
                [t for t in self.tasks.values() if t.priority == TaskPriority.CRITICAL]
            )
            overdue_tasks = len(
                [
                    t
                    for t in self.tasks.values()
                    if t.due_date and t.due_date < datetime.now().isoformat()
                ]
            )

            return {
                "status": self.status,
                "total_tasks": total_tasks,
                "pending_tasks": pending_tasks,
                "critical_tasks": critical_tasks,
                "overdue_tasks": overdue_tasks,
                "active_agents": len(set(t.assigned_to for t in self.tasks.values())),
            }

        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"status": "error", "error": str(e)}


class DevelopmentTaskManager:
    """Manages development tasks and autonomous workflow"""

    def __init__(self):
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
        sample_tasks = [
            {
                "title": "Repository Cleanup and Optimization",
                "description": "Clean up unused files, optimize imports, and improve code structure",
                "complexity": TaskComplexity.MEDIUM,
                "priority": DevTaskPriority.HIGH,
                "estimated_hours": 2.0,
                "required_skills": ["git", "code_analysis", "optimization"],
            },
            {
                "title": "Documentation Update",
                "description": "Update README files, add inline comments, and improve API documentation",
                "complexity": TaskComplexity.LOW,
                "priority": DevTaskPriority.MEDIUM,
                "estimated_hours": 1.5,
                "required_skills": ["documentation", "markdown", "api_design"],
            },
            {
                "title": "Test Coverage Improvement",
                "description": "Increase test coverage, add missing unit tests, and improve test quality",
                "complexity": TaskComplexity.MEDIUM,
                "priority": DevTaskPriority.HIGH,
                "estimated_hours": 3.0,
                "required_skills": ["testing", "unittest", "coverage"],
            },
            {
                "title": "Performance Optimization",
                "description": "Identify and fix performance bottlenecks, optimize algorithms",
                "complexity": TaskComplexity.HIGH,
                "priority": DevTaskPriority.MEDIUM,
                "estimated_hours": 4.0,
                "required_skills": ["profiling", "optimization", "algorithms"],
            },
            {
                "title": "Security Audit",
                "description": "Review code for security vulnerabilities and implement fixes",
                "complexity": TaskComplexity.HIGH,
                "priority": DevTaskPriority.CRITICAL,
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
        complexity: TaskComplexity | str,
        priority: DevTaskPriority | int | str,
        estimated_hours: float,
        required_skills: List[str],
        tags: Optional[List[str]] = None,
    ) -> str:
        """Create a new development task"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter:04d}"

        if isinstance(complexity, str):
            complexity = TaskComplexity(complexity)
        if isinstance(priority, int):
            priority = DevTaskPriority(priority)
        elif isinstance(priority, str):
            priority = DevTaskPriority[priority.upper()]

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
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[DevelopmentTask]:
        return list(self.tasks.values())

    def get_available_tasks(self) -> List[DevelopmentTask]:
        return [task for task in self.tasks.values() if task.is_available()]

    def get_tasks_by_status(self, status: DevTaskStatus) -> List[DevelopmentTask]:
        return [task for task in self.tasks.values() if task.status == status]

    def get_tasks_by_priority(self, min_priority: int = DevTaskPriority.MINIMAL.value) -> List[DevelopmentTask]:
        return [
            task
            for task in self.tasks.values()
            if task.status == DevTaskStatus.AVAILABLE and task.priority.value >= min_priority
        ]

    def get_tasks_by_complexity(self, complexity: TaskComplexity) -> List[DevelopmentTask]:
        return [task for task in self.tasks.values() if task.complexity == complexity]

    def get_tasks_by_agent(self, agent_id: str) -> List[DevelopmentTask]:
        return [task for task in self.tasks.values() if task.claimed_by == agent_id]

    def claim_task(self, task_id: str, agent_id: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False

        if task.claim(agent_id):
            self.workflow_stats["total_tasks_claimed"] += 1
            self.logger.info(f"Agent {agent_id} claimed task {task_id}")
            return True
        return False

    def start_task_work(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        return task.start_work()

    def update_task_progress(self, task_id: str, percentage: float) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        return task.update_progress(percentage)

    def complete_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        if task.complete():
            self.workflow_stats["total_tasks_completed"] += 1
            self.logger.info(f"Task {task_id} completed by {task.claimed_by}")
            return True
        return False

    def block_task(self, task_id: str, reason: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        return task.block(reason)

    def unblock_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        return task.unblock()

    def cancel_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        return task.cancel()

    def get_task_statistics(self) -> Dict[str, any]:
        total_tasks = len(self.tasks)
        available_tasks = len(self.get_available_tasks())
        claimed_tasks = len(self.get_tasks_by_status(DevTaskStatus.CLAIMED))
        in_progress_tasks = len(self.get_tasks_by_status(DevTaskStatus.IN_PROGRESS))
        completed_tasks = len(self.get_tasks_by_status(DevTaskStatus.COMPLETED))
        blocked_tasks = len(self.get_tasks_by_status(DevTaskStatus.BLOCKED))

        completed_task_times = []
        for task in self.get_tasks_by_status(DevTaskStatus.COMPLETED):
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
        stats = self.get_task_statistics()
        total = stats["total_tasks"]
        completed = stats["completed_tasks"]
        stats["completion_rate"] = (completed / total * 100) if total else 0
        return stats

    def get_priority_distribution(self) -> Dict[str, int]:
        distribution = {}
        for priority in DevTaskPriority:
            distribution[priority.name] = len(
                [t for t in self.tasks.values() if t.priority == priority]
            )
        return distribution

    def get_complexity_distribution(self) -> Dict[str, int]:
        distribution = {}
        for complexity in TaskComplexity:
            distribution[complexity.name] = len(
                [t for t in self.tasks.values() if t.complexity == complexity]
            )
        return distribution

    def cleanup_completed_tasks(self, days_old: int = 30) -> int:
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
        return [task.to_dict() for task in self.tasks.values()]

    def import_tasks(self, tasks_data: List[Dict[str, any]]) -> int:
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


def main():
    """CLI interface for Task Manager testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Task Manager Testing Interface")
    parser.add_argument("--init", action="store_true", help="Initialize task manager")
    parser.add_argument(
        "--create",
        nargs=5,
        metavar=("TITLE", "DESCRIPTION", "ASSIGNED_TO", "CREATED_BY", "PRIORITY"),
        help="Create task",
    )
    parser.add_argument(
        "--status", metavar="AGENT_ID", help="Show task status for agent"
    )
    parser.add_argument("--tasks", metavar="AGENT_ID", help="Show tasks for agent")
    parser.add_argument(
        "--update", nargs=2, metavar=("TASK_ID", "STATUS"), help="Update task status"
    )
    parser.add_argument("--test", action="store_true", help="Run task manager tests")

    args = parser.parse_args()

    # Create workspace manager first
    from workspace_manager import WorkspaceManager

    workspace_manager = WorkspaceManager()

    # Create task manager
    task_manager = TaskManager(workspace_manager)

    if args.init or not any(
        [args.init, args.create, args.status, args.tasks, args.update, args.test]
    ):
        print("📋 Task Manager - Agent Cellphone V2")
        print("Manager initialized successfully")

    if args.create:
        title, description, assigned_to, created_by, priority = args.create
        task_priority = (
            TaskPriority(priority.lower())
            if priority.lower() in [p.value for p in TaskPriority]
            else TaskPriority.NORMAL
        )
        task_id = task_manager.create_task(
            title, description, assigned_to, created_by, task_priority
        )
        if task_id:
            print(f"✅ Task created successfully: {task_id}")
        else:
            print("❌ Failed to create task")

    if args.status:
        status = task_manager.get_task_status(args.status)
        print(f"📊 Task Status for {args.status}:")
        for key, value in status.items():
            print(f"  {key}: {value}")

    if args.tasks:
        tasks = task_manager.get_tasks(args.tasks)
        print(f"📋 Tasks for {args.tasks}:")
        for task in tasks:
            print(
                f"  {task.task_id}: {task.title} (Priority: {task.priority.value}, Status: {task.status.value})"
            )

    if args.update:
        task_id, status = args.update
        task_status = (
            TaskStatus(status.lower())
            if status.lower() in [s.value for s in TaskStatus]
            else TaskStatus.PENDING
        )
        success = task_manager.update_task_status(task_id, task_status)
        print(f"Task status update: {'✅ Success' if success else '❌ Failed'}")

    if args.test:
        print("🧪 Running task manager tests...")
        try:
            # Test task creation
            task_id = task_manager.create_task(
                "Test Task",
                "Test description",
                "Agent-1",
                "TestAgent",
                TaskPriority.HIGH,
            )
            print(f"Task creation test: {'✅ Success' if task_id else '❌ Failed'}")

            # Test task retrieval
            tasks = task_manager.get_tasks("Agent-1")
            print(f"Task retrieval test: {'✅ Success' if tasks else '❌ Failed'}")

            # Test status update
            if task_id:
                success = task_manager.update_task_status(
                    task_id, TaskStatus.IN_PROGRESS
                )
                print(f"Status update test: {'✅ Success' if success else '❌ Failed'}")

        except Exception as e:
            print(f"❌ Task manager test failed: {e}")


if __name__ == "__main__":
    main()
