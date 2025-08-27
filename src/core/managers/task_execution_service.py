"""Service handling task submission and execution."""
import time
from threading import Thread, Timer
from typing import Callable, Dict, Any

from .task_models import TaskStatus, TaskResult


class TaskExecutionService:
    """Handle submission and execution of tasks for the manager."""

    def __init__(self, persistence, manager) -> None:
        self._persistence = persistence
        self._manager = manager
        self._processor_thread: Thread | None = None

    # ------------------------------------------------------------------
    # Processor management
    # ------------------------------------------------------------------
    def start_processor(self) -> None:
        """Start the background task processor loop."""
        self._processor_thread = Thread(target=self._task_processor_loop, daemon=True)
        self._processor_thread.start()

    def cleanup(self) -> None:
        """Join the processor thread if running."""
        if self._processor_thread and self._processor_thread.is_alive():
            self._processor_thread.join(timeout=5)

    # ------------------------------------------------------------------
    # Public API used by TaskManager
    # ------------------------------------------------------------------
    def submit(self, task_id: str, executor_func: Callable, *args, **kwargs) -> bool:
        """Submit a task for execution."""
        try:
            with self._manager.task_lock:
                if task_id not in self._manager.tasks:
                    return False

                task = self._manager.tasks[task_id]
                if task.status != TaskStatus.PENDING:
                    return False

                if not self._check_dependencies(task_id):
                    return True

                task.status = TaskStatus.RUNNING
                task.started_at = self._manager._now_iso()

                execution_thread = Thread(
                    target=self._execute_task,
                    args=(task_id, executor_func, args, kwargs),
                    daemon=True,
                )
                self._manager.running_tasks[task_id] = execution_thread
                execution_thread.start()

                self._manager._emit_event(
                    "task_started", {"task_id": task_id, "started_at": task.started_at}
                )
                self._persistence.persist(self._manager.tasks, self._manager.task_queue)
                return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _check_dependencies(self, task_id: str) -> bool:
        try:
            task = self._manager.tasks[task_id]
            for dep_id in task.dependencies:
                if dep_id not in self._manager.tasks:
                    return False
                if self._manager.tasks[dep_id].status != TaskStatus.COMPLETED:
                    return False
            return True
        except Exception:
            return False

    def _execute_task(self, task_id: str, executor_func: Callable, args: tuple, kwargs: Dict[str, Any]) -> None:
        try:
            task = self._manager.tasks[task_id]
            start_time = time.time()
            result = executor_func(*args, **kwargs)
            execution_time = time.time() - start_time

            task_result = TaskResult(
                task_id=task_id,
                success=True,
                result=result,
                error=None,
                execution_time=execution_time,
                metadata={"executor": executor_func.__name__},
            )

            with self._manager.task_lock:
                task.status = TaskStatus.COMPLETED
                task.completed_at = self._manager._now_iso()
                task.duration = execution_time
                task.result = result
                if task_id in self._manager.running_tasks:
                    del self._manager.running_tasks[task_id]
                self._manager.completed_tasks[task_id] = task_result

            self._manager._emit_event(
                "task_completed",
                {"task_id": task_id, "execution_time": execution_time, "success": True},
            )
            self._check_dependent_tasks(task_id)
            self._persistence.persist(self._manager.tasks, self._manager.task_queue)
        except Exception as e:
            execution_time = time.time() - start_time  # type: ignore[unbound-local-variable]
            task = self._manager.tasks.get(task_id)
            if task and task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                task.error = f"Retry {task.retry_count}/{task.max_retries}: {e}"
                Timer(
                    self._manager.retry_delay, self._requeue_task, args=[task_id]
                ).start()
                self._persistence.persist(self._manager.tasks, self._manager.task_queue)
            else:
                if task:
                    with self._manager.task_lock:
                        task.status = TaskStatus.FAILED
                        task.completed_at = self._manager._now_iso()
                        task.duration = execution_time
                        task.error = str(e)
                        if task_id in self._manager.running_tasks:
                            del self._manager.running_tasks[task_id]
                    self._manager._emit_event(
                        "task_failed",
                        {
                            "task_id": task_id,
                            "error": str(e),
                            "retry_count": task.retry_count if task else 0,
                        },
                    )
                    self._persistence.persist(
                        self._manager.tasks, self._manager.task_queue
                    )

    def _requeue_task(self, task_id: str) -> None:
        try:
            with self._manager.task_lock:
                if task_id in self._manager.tasks:
                    task = self._manager.tasks[task_id]
                    self._manager.task_queue.put((task.priority.value, task_id))
                    self._persistence.persist(
                        self._manager.tasks, self._manager.task_queue
                    )
        except Exception:
            pass

    def _check_dependent_tasks(self, completed_task_id: str) -> None:
        try:
            with self._manager.task_lock:
                for task_id, task in self._manager.tasks.items():
                    if (
                        task.status == TaskStatus.PENDING
                        and completed_task_id in task.dependencies
                        and self._check_dependencies(task_id)
                    ):
                        self._manager.task_queue.put((task.priority.value, task_id))
                        self._persistence.persist(
                            self._manager.tasks, self._manager.task_queue
                        )
        except Exception:
            pass

    def _task_processor_loop(self) -> None:
        while not self._manager.shutdown_event.is_set():
            try:
                if (
                    not self._manager.task_queue.empty()
                    and len(self._manager.running_tasks)
                    < self._manager.max_concurrent_tasks
                ):
                    priority, task_id = self._manager.task_queue.get_nowait()
                    with self._manager.task_lock:
                        if (
                            task_id in self._manager.tasks
                            and self._manager.tasks[task_id].status == TaskStatus.PENDING
                            and self._check_dependencies(task_id)
                        ):
                            continue
                time.sleep(0.1)
            except Exception:
                time.sleep(1)
