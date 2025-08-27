"""Task Manager - orchestrates task lifecycle and scheduling."""
import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from threading import Event, Lock, Thread
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional
from ..base_manager import BaseManager
from .task_models import Task, TaskPriority, TaskStatus, TaskType, Workflow, TaskResult
from .task_persistence import TaskStatePersister, TaskStorageInterface
from .task_lifecycle_services import (
    TaskCancellationService,
    TaskCreationService,
    TaskMonitoringService,
)
from .task_execution_service import TaskExecutionService
from .task_query_service import TaskQueryService
from .workflow_service import WorkflowService
logger = logging.getLogger(__name__)

class TaskManager(BaseManager):
    """Core manager responsible for task and workflow orchestration."""

    def __init__(
        self,
        config_path: str = "config/task_manager.json",
        storage: Optional[TaskStorageInterface] = None,
    ) -> None:
        super().__init__(manager_id="task_manager", name="TaskManager")
        self.config_path = config_path
        self.tasks: Dict[str, Task] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.task_queue: PriorityQueue = PriorityQueue()
        self.running_tasks: Dict[str, Thread] = {}
        self.completed_tasks: Dict[str, TaskResult] = {}
        self.task_lock = Lock()
        self.workflow_lock = Lock()
        self.shutdown_event = Event()

        self._persistence = TaskStatePersister(storage)
        self._creator = TaskCreationService(self._persistence, self)
        self._canceller = TaskCancellationService(self._persistence, self)
        self._monitor = TaskMonitoringService(self)
        self._executor = TaskExecutionService(self._persistence, self)
        self._query = TaskQueryService(self)
        self._workflow = WorkflowService(self)

        self.max_concurrent_tasks = 10
        self.task_timeout_default = 300
        self.retry_delay = 5

        self._load_manager_config()
        self._executor.start_processor()

    # Helpers
    def _generate_id(self) -> str:
        return str(uuid.uuid4())

    def _now_iso(self) -> str:
        return datetime.now().isoformat()

    def _load_manager_config(self) -> None:
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                self.max_concurrent_tasks = config.get("max_concurrent_tasks", 10)
                self.task_timeout_default = config.get("task_timeout_default", 300)
                self.retry_delay = config.get("retry_delay", 5)
            else:
                logger.warning(f"Task config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load task config: {e}")

    # Task lifecycle
    def create_task(
        self,
        name: str,
        description: str,
        task_type: TaskType = TaskType.CUSTOM,
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        try:
            task_id = self._generate_id()
            task = Task(
                id=task_id,
                name=name,
                description=description,
                task_type=task_type,
                priority=priority,
                status=TaskStatus.PENDING,
                created_at=self._now_iso(),
                started_at=None,
                completed_at=None,
                duration=None,
                result=None,
                error=None,
                metadata=metadata or {},
                dependencies=dependencies or [],
                retry_count=0,
                max_retries=max_retries,
                timeout=timeout or self.task_timeout_default,
                tags=tags or [],
            )
            with self.task_lock:
                self._creator._create(self.tasks, self.task_queue, task)
            self._emit_event(
                "task_created",
                {
                    "task_id": task_id,
                    "name": name,
                    "priority": priority.value,
                    "type": task_type.value,
                },
            )
            return task_id
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            return ""

    def submit_task(self, task_id: str, executor_func: Callable, *args, **kwargs) -> bool:
        return self._executor.submit(task_id, executor_func, *args, **kwargs)

    def cancel_task(self, task_id: str) -> bool:
        try:
            with self.task_lock:
                result = self._canceller._cancel(task_id, self.tasks, self.task_queue)
            if result:
                self._emit_event("task_cancelled", {"task_id": task_id})
            return result
        except Exception:
            logger.exception("Failed to cancel task")
            return False

    def monitor_tasks(self) -> Dict[str, int]:
        try:
            with self.task_lock:
                return self._monitor._monitor(self.tasks)
        except Exception:
            logger.exception("Failed to monitor tasks")
            return {}

    # Query helpers
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        return self._query.get_task_status(task_id)

    def get_task_info(self, task_id: str) -> Optional[Task]:
        return self._query.get_task_info(task_id)

    def get_running_tasks(self) -> List[str]:
        return self._query.get_running_tasks()

    def get_pending_tasks(self) -> List[Task]:
        return self._query.get_pending_tasks()

    def get_completed_tasks(self, limit: int = 100) -> List[TaskResult]:
        return self._query.get_completed_tasks(limit)

    def get_task_statistics(self) -> Dict[str, Any]:
        return self._query.get_task_statistics()

    # Workflow management
    def create_workflow(
        self,
        name: str,
        description: str,
        tasks: List[str],
        dependencies: Dict[str, List[str]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        return self._workflow.create(name, description, tasks, dependencies, metadata)

    def get_workflow_info(self, workflow_id: str) -> Optional[Workflow]:
        return self._workflow.get_info(workflow_id)

    # Cleanup
    def cleanup(self) -> None:
        try:
            self.shutdown_event.set()
            self._executor.cleanup()
            for thread in self.running_tasks.values():
                if thread.is_alive():
                    thread.join(timeout=5)
            with self.task_lock:
                self.tasks.clear()
                self.running_tasks.clear()
                self.completed_tasks.clear()
            with self.workflow_lock:
                self.workflows.clear()
            super().cleanup()
            logger.info("TaskManager cleanup completed")
        except Exception as e:
            logger.error(f"TaskManager cleanup failed: {e}")
