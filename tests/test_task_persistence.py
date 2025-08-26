import json
from queue import PriorityQueue

import importlib.util
import types
import sys
from pathlib import Path


package = types.ModuleType("src.core.managers")
package.__path__ = [str(Path("src/core/managers"))]
sys.modules["src.core.managers"] = package

spec_models = importlib.util.spec_from_file_location(
    "src.core.managers.task_models",
    Path("src/core/managers/task_models.py"),
    submodule_search_locations=package.__path__,
)
task_models = importlib.util.module_from_spec(spec_models)
spec_models.loader.exec_module(task_models)  # type: ignore
sys.modules["src.core.managers.task_models"] = task_models

spec = importlib.util.spec_from_file_location(
    "src.core.managers.task_persistence",
    Path("src/core/managers/task_persistence.py"),
)
task_persistence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_persistence)  # type: ignore

TaskStatePersister = task_persistence.TaskStatePersister
TaskStorageInterface = task_persistence.TaskStorageInterface


class MemoryStorage(TaskStorageInterface):
    def __init__(self):
        self.saved = None

    def save_state(self, data: str) -> bool:  # pragma: no cover - simple storage
        self.saved = data
        return True


def test_persist_success(tmp_path, monkeypatch):
    storage = MemoryStorage()
    persister = TaskStatePersister(storage=storage)
    tasks = {}
    queue = PriorityQueue()

    # change to tmp directory for fallback file
    monkeypatch.chdir(tmp_path)

    persister.persist(tasks, queue)

    assert storage.saved is not None
    # Ensure fallback file not created when storage succeeds
    assert not (tmp_path / "task_state_backup.json").exists()


class FailingStorage(TaskStorageInterface):
    def save_state(self, data: str) -> bool:  # pragma: no cover - failure simulation
        raise RuntimeError("fail")


def test_persist_fallback(tmp_path, monkeypatch):
    storage = FailingStorage()
    persister = TaskStatePersister(storage=storage)
    tasks = {}
    queue = PriorityQueue()

    monkeypatch.chdir(tmp_path)

    persister.persist(tasks, queue)

    assert (tmp_path / "task_state_backup.json").exists()
    with open(tmp_path / "task_state_backup.json") as f:
        data = json.load(f)
        assert data["tasks"] == {}
