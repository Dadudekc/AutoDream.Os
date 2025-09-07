from datetime import datetime
from queue import PriorityQueue
from typing import Dict

from src.core.managers.task_lifecycle_services import (
    TaskCancellationService,
    TaskCreationService,
    TaskMonitoringService,
)
from src.core.managers.task_manager import TaskManager
from src.core.managers.task_models import Task, TaskPriority, TaskStatus, TaskType


class DummyPersistence:
    def __init__(self):
        self.called = False

    def persist(self, tasks, queue):  # type: ignore[override]
        self.called = True


class DummyHealth:
    def is_healthy(self) -> bool:  # type: ignore[override]
        return True


def _sample_task(task_id: str = "t1", status: TaskStatus = TaskStatus.PENDING) -> Task:
    return Task(
        id=task_id,
        name="task",
        description="desc",
        task_type=TaskType.CUSTOM,
        priority=TaskPriority.NORMAL,
        status=status,
        created_at=datetime.now().isoformat(),
        started_at=None,
        completed_at=None,
        duration=None,
        result=None,
        error=None,
        metadata={},
        dependencies=[],
        retry_count=0,
        max_retries=3,
        timeout=60,
        tags=[],
    )


def test_creation_service_creates_and_persists():
    tasks: Dict[str, Task] = {}
    queue: PriorityQueue = PriorityQueue()
    persistence = DummyPersistence()
    health = DummyHealth()
    service = TaskCreationService(persistence, health)
    task = _sample_task()
    service._create(tasks, queue, task)
    assert task.id in tasks
    assert not queue.empty()
    assert persistence.called
    assert service.check_health()


def test_cancellation_service_cancels_task():
    task = _sample_task()
    tasks: Dict[str, Task] = {task.id: task}
    queue: PriorityQueue = PriorityQueue()
    persistence = DummyPersistence()
    health = DummyHealth()
    service = TaskCancellationService(persistence, health)
    assert service._cancel(task.id, tasks, queue) is True
    assert tasks[task.id].status == TaskStatus.CANCELLED
    assert persistence.called
    assert service.check_health()


def test_monitoring_service_counts_statuses():
    t1 = _sample_task("t1", TaskStatus.PENDING)
    t2 = _sample_task("t2", TaskStatus.CANCELLED)
    tasks = {t1.id: t1, t2.id: t2}
    health = DummyHealth()
    service = TaskMonitoringService(health)
    stats = service._monitor(tasks)
    assert stats[TaskStatus.PENDING.value] == 1
    assert stats[TaskStatus.CANCELLED.value] == 1
    assert service.check_health()


