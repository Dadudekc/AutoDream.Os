"""Tests for the terminal completion monitor."""

import json
import queue
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.terminal_completion_monitor import (  # noqa: E402
    COMPLETION_SIGNAL,
    TerminalCompletionMonitor,
)


def test_emits_event_when_signal_detected(tmp_path):
    log = tmp_path / "test.log"
    log.write_text("start\n", encoding="utf-8")
    event_queue: queue.Queue = queue.Queue()
    monitor = TerminalCompletionMonitor([log], event_queue=event_queue)

    monitor.poll()
    assert event_queue.empty()

    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"running {COMPLETION_SIGNAL} done\n")

    monitor.poll()
    event = event_queue.get_nowait()
    assert event.source == str(log)
    assert COMPLETION_SIGNAL in event.line


def test_writes_event_to_output_file(tmp_path):
    log = tmp_path / "run.log"
    output = tmp_path / "events.jsonl"
    log.write_text(f"before {COMPLETION_SIGNAL} after\n", encoding="utf-8")

    monitor = TerminalCompletionMonitor([log], output_path=output)
    monitor.poll()

    content = output.read_text(encoding="utf-8").strip().splitlines()
    assert len(content) == 1
    data = json.loads(content[0])
    assert data["source"] == str(log)
    assert COMPLETION_SIGNAL in data["line"]
