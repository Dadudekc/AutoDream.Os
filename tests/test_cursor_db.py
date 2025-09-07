"""Tests for the CursorTaskRepository."""

import sqlite3
from pathlib import Path

import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from services.cursor_db import CursorTaskRepository, CursorTask


def _init_db(path: Path) -> None:
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE tasks (task_id TEXT PRIMARY KEY, agent_id TEXT, status TEXT)"
    )
    conn.execute(
        "INSERT INTO tasks (task_id, agent_id, status) VALUES (?, ?, ?)",
        ("task1", "agent-1", "done"),
    )
    conn.commit()
    conn.close()


def test_get_task_returns_record() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "tasks.db"
        _init_db(db_path)
        repo = CursorTaskRepository(db_path)
        task = repo.get_task("task1")
        assert isinstance(task, CursorTask)
        assert task.agent_id == "agent-1"


def test_task_exists_false_for_missing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "tasks.db"
        _init_db(db_path)
        repo = CursorTaskRepository(db_path)
        assert repo.task_exists("missing") is False
