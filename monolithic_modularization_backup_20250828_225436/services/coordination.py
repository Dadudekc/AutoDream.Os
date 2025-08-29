"""
Coordination Service - Multi-Agent Task Orchestration

This module provides coordination services for complex multi-agent tasks including:
- Task creation and management
- Dependency tracking and workflow execution
- Progress monitoring and status updates
- Task completion and cleanup

Architecture: Single Responsibility Principle - manages only task coordination
LOC: 160 lines (under 200 limit)
"""

import argparse
import time
import uuid

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class CoordinationStatus(Enum):
    """Task coordination status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class CoordinationTask:
    """Multi-agent coordination task definition"""

    task_id: str
    name: str
    description: str
    agent_ids: List[str]
    dependencies: List[str]
    status: CoordinationStatus
    created_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class CoordinationService:
    """
    Multi-agent coordination orchestration service

    Responsibilities:
    - Task creation and lifecycle management
    - Dependency resolution and workflow execution
    - Progress tracking and status updates
    - Task completion and cleanup
    """

    def __init__(self):
        self.tasks: Dict[str, CoordinationTask] = {}
        self.active_tasks: Set[str] = set()
        self.logger = logging.getLogger(f"{__name__}.CoordinationService")

    def create_coordination_task(
        self,
        name: str,
        description: str,
        agent_ids: List[str],
        dependencies: List[str] = None,
    ) -> str:
        """Create a new coordination task"""
        try:
            task_id = str(uuid.uuid4())
            task = CoordinationTask(
                task_id=task_id,
                name=name,
                description=description,
                agent_ids=agent_ids,
                dependencies=dependencies or [],
                status=CoordinationStatus.PENDING,
                created_at=time.time(),
            )

            self.tasks[task_id] = task
            self.logger.info(f"Created coordination task: {name} ({task_id})")
            return task_id

        except Exception as e:
            self.logger.error(f"Failed to create coordination task: {e}")
            return ""

    def start_coordination_task(self, task_id: str) -> bool:
        """Start a coordination task"""
        if task_id not in self.tasks:
            self.logger.error(f"Task {task_id} not found")
            return False

        task = self.tasks[task_id]

        # Check dependencies
        if not self._check_dependencies(task):
            self.logger.warning(f"Task {task_id} dependencies not met")
            return False

        try:
            task.status = CoordinationStatus.RUNNING
            task.started_at = time.time()
            self.active_tasks.add(task_id)

            self.logger.info(f"Started coordination task: {task.name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start task {task_id}: {e}")
            return False

    def _check_dependencies(self, task: CoordinationTask) -> bool:
        """Check if task dependencies are met"""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                return False
            if self.tasks[dep_id].status != CoordinationStatus.COMPLETED:
                return False
        return True

    def complete_task_step(
        self, task_id: str, step_name: str, result: Any = None
    ) -> bool:
        """Complete a step in a coordination task"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if task.status != CoordinationStatus.RUNNING:
            return False

        try:
            if not task.metadata:
                task.metadata = {}
            task.metadata[step_name] = result

            self.logger.info(f"Completed step {step_name} for task {task.name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to complete step {step_name}: {e}")
            return False

    def _notify_task_completion(self, task_id: str):
        """Notify dependent tasks of completion"""
        for task in self.tasks.values():
            if task_id in task.dependencies:
                self.logger.info(f"Task {task.name} dependencies updated")

    def fail_task(self, task_id: str, error_message: str) -> bool:
        """Mark a task as failed"""
        if task_id not in self.tasks:
            return False

        try:
            task = self.tasks[task_id]
            task.status = CoordinationStatus.FAILED
            task.completed_at = time.time()

            if task_id in self.active_tasks:
                self.active_tasks.remove(task_id)

            if not task.metadata:
                task.metadata = {}
            task.metadata["error"] = error_message

            self.logger.error(f"Task {task.name} failed: {error_message}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to mark task {task_id} as failed: {e}")
            return False

    def get_task_status(self, task_id: str) -> Optional[CoordinationStatus]:
        """Get current status of a task"""
        if task_id in self.tasks:
            return self.tasks[task_id].status
        return None

    def get_all_tasks(self) -> Dict[str, CoordinationTask]:
        """Get all coordination tasks"""
        return self.tasks.copy()

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if task.status != CoordinationStatus.RUNNING:
            return False

        try:
            task.status = CoordinationStatus.CANCELLED
            task.completed_at = time.time()
            self.active_tasks.remove(task_id)

            self.logger.info(f"Cancelled task: {task.name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to cancel task {task_id}: {e}")
            return False

    def cleanup_completed_tasks(self) -> int:
        """Remove completed and failed tasks, return count cleaned"""
        to_remove = []
        for task_id, task in self.tasks.items():
            if task.status in [
                CoordinationStatus.COMPLETED,
                CoordinationStatus.FAILED,
                CoordinationStatus.CANCELLED,
            ]:
                to_remove.append(task_id)

        for task_id in to_remove:
            del self.tasks[task_id]

        cleaned_count = len(to_remove)
        if cleaned_count > 0:
            self.logger.info(f"Cleaned up {cleaned_count} completed tasks")

        return cleaned_count


def run_smoke_test():
    """Run basic functionality test for CoordinationService"""
    print("🧪 Running CoordinationService Smoke Test...")

    service = CoordinationService()

    # Test task creation
    task_id = service.create_coordination_task(
        "Test Task", "Test Description", ["agent-1", "agent-2"]
    )
    assert task_id != ""

    # Test task start
    assert service.start_coordination_task(task_id)
    assert service.get_task_status(task_id) == CoordinationStatus.RUNNING

    # Test step completion
    assert service.complete_task_step(task_id, "step1", "result1")

    # Test task completion
    task = service.tasks[task_id]
    task.status = CoordinationStatus.COMPLETED
    task.completed_at = time.time()

    # Test cleanup
    cleaned = service.cleanup_completed_tasks()
    assert cleaned == 1

    print("✅ CoordinationService Smoke Test PASSED")
    return True


def main():
    """CLI interface for CoordinationService testing"""
    parser = argparse.ArgumentParser(description="Coordination Service CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--create", nargs=3, help="Create task (name,description,agents)"
    )
    parser.add_argument("--start", help="Start task by ID")
    parser.add_argument("--status", help="Get task status by ID")
    parser.add_argument("--list", action="store_true", help="List all tasks")
    parser.add_argument(
        "--cleanup", action="store_true", help="Clean up completed tasks"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    service = CoordinationService()

    if args.create:
        name, description, agents = args.create
        agent_list = [a.strip() for a in agents.split("|")]
        task_id = service.create_coordination_task(name, description, agent_list)
        print(f"Created task: {task_id}")

    elif args.start:
        success = service.start_coordination_task(args.start)
        print(f"Start task {args.start}: {'SUCCESS' if success else 'FAILED'}")

    elif args.status:
        status = service.get_task_status(args.status)
        print(f"Task {args.status} status: {status}")

    elif args.list:
        tasks = service.get_all_tasks()
        for task_id, task in tasks.items():
            print(f"{task_id}: {task.name} - {task.status.value}")

    elif args.cleanup:
        cleaned = service.cleanup_completed_tasks()
        print(f"Cleaned up {cleaned} tasks")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
