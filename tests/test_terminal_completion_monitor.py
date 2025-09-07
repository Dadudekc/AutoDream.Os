import sqlite3
from pathlib import Path

from src.services.cursor_db import CursorTaskRepository
from src.services.terminal_completion_monitor import TerminalCompletionMonitor


def setup_db(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE agent_tasks (task_id TEXT, agent_id TEXT, signal TEXT)"
    )
    cursor.executemany(
        "INSERT INTO agent_tasks VALUES (?, ?, ?)",
        [("t1", "agent1", "sig1"), ("t2", "agent1", "sig2")],
    )
    conn.commit()
    cursor.close()
    conn.close()


def test_check_signals_flags_mismatches(tmp_path, monkeypatch):
    db_file = tmp_path / "cursor.db"
    setup_db(db_file)
    monkeypatch.setenv("CURSOR_DB_PATH", str(db_file))
    repo = CursorTaskRepository()
    monitor = TerminalCompletionMonitor(repo)
    result = monitor.check_signals("agent1", ["sig1", "sig3"])
    assert result["unexpected"] == {"sig3"}
    assert result["missing"] == {"sig2"}
