import pytest

from src.core.task_management.unified_scheduler import (
    Task,
    TaskPriority,
    UnifiedTaskScheduler,
)


@pytest.mark.asyncio
async def test_basic_task_flow():
    scheduler = UnifiedTaskScheduler(max_concurrent_tasks=1)
    task = Task(name="demo", content="run", priority=TaskPriority.HIGH)

    await scheduler.submit_task(task)
    next_task = await scheduler.get_next_task("agent-1")
    assert next_task is not None
    scheduler._running_tasks[task.task_id] = task
    assert next_task.task_id == task.task_id

    await scheduler.complete_task(task.task_id, result="done")
    completed = scheduler.get_completed_tasks()
    assert task.task_id in completed
    assert completed[task.task_id].result == "done"
