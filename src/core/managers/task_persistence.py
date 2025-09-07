#!/usr/bin/env python3
"""Task state serialization and persistence utilities."""

import json
import logging
import time
from dataclasses import asdict
from typing import Dict, Optional, Any
from queue import PriorityQueue
from typing import Protocol

from .task_models import Task

logger = logging.getLogger(__name__)


class TaskStorageInterface(Protocol):
    """Storage interface for persisting task state."""

    def save_state(self, data: str) -> bool:
        """Persist serialized task state."""
        ...


class TaskStatePersister:
    """Serialize and persist task state using optional storage."""

    def __init__(self, storage: Optional[TaskStorageInterface] = None) -> None:
        self._storage = storage

    def serialize(self, tasks: Dict[str, Task], queue: PriorityQueue) -> str:
        state = {
            "tasks": {tid: asdict(task) for tid, task in tasks.items()},
            "queue": list(queue.queue),
            "statuses": {tid: task.status.value for tid, task in tasks.items()},
        }
        return json.dumps(state)

    def persist(self, tasks: Dict[str, Task], queue: PriorityQueue, retries: int = 3) -> None:
        if not self._storage:
            return

        data = self.serialize(tasks, queue)
        for attempt in range(retries):
            try:
                if self._storage.save_state(data):
                    return
            except Exception as e:
                logger.error(f"Persist attempt {attempt + 1} failed: {e}")
            time.sleep(1)

        try:
            with open("task_state_backup.json", "w") as f:
                f.write(data)
            logger.warning("State persisted to fallback storage")
        except Exception as e:
            logger.error(f"Fallback persistence failed: {e}")
