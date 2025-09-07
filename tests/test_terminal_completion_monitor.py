"""Tests for TerminalCompletionMonitor cross-checking."""

import queue
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from terminal_completion_monitor import (
    COMPLETION_SIGNAL,
    TerminalCompletionMonitor,
)
from services.cursor_db import CursorTaskRepository

import sqlite3


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


def test_poll_emits_events_with_cross_check(tmp_path: Path) -> None:
    db_path = tmp_path / "tasks.db"
    _init_db(db_path)
    repo = CursorTaskRepository(db_path)
    log = tmp_path / "log.txt"
    log.write_text(
        f"nope\n{COMPLETION_SIGNAL} task1\n{COMPLETION_SIGNAL} task2\n",
        encoding="utf-8",
    )
    q: queue.Queue = queue.Queue()
    monitor = TerminalCompletionMonitor([log], event_queue=q, task_repo=repo)
    monitor.poll()
    events = [q.get_nowait() for _ in range(2)]
    assert events[0].task_id == "task1" and events[0].task_found is True
    assert events[1].task_id == "task2" and events[1].task_found is False
