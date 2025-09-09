from __future__ import annotations

import logging
logger = logging.getLogger(__name__)
"""Monitor terminal logs for completion signals.

This module tails specified log files and emits structured events whenever the
`COMPLETION_SIGNAL` token is detected. Events can be written to an output log
file or pushed onto an in-memory queue for downstream processing.

Usage:
    python scripts/terminal_completion_monitor.py         -s path/to/log1 -s path/to/log2         -o logs/completion_events.log -v

The script uses the SSOT `COMPLETION_SIGNAL` from `config/messaging.yml` via
`src.core.constants`, allowing tests and dependent modules to import it
directly.
"""
import argparse
import json
import os
import queue
import sys
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from services.cursor_db import CursorTaskRepository
from core.constants.manager import COMPLETION_SIGNAL


@dataclass
class CompletionEvent:
    """Structured event emitted when a completion signal is detected."""
    timestamp: float
    source: str
    line: str
    task_id: str | None = None
    task_found: bool | None = None

    def to_json(self) ->str:
        """Return the event serialized as a JSON string."""
        return json.dumps({'timestamp': self.timestamp, 'source': self.
            source, 'line': self.line, 'task_id': self.task_id,
            'task_found': self.task_found})


class TerminalCompletionMonitor:
    """Tail log files and emit events when completion signals appear."""

    def __init__(self, sources: Iterable[Path], output_path: (Path | None)=
        None, event_queue: (queue.Queue | None)=None, verbose: bool=False,
        task_repo: (CursorTaskRepository | None)=None) ->None:
        self.sources: list[Path] = [Path(s) for s in sources]
        self.output_path = Path(output_path) if output_path else None
        self.event_queue = event_queue
        self.verbose = verbose
        self.task_repo = task_repo
        self._positions: dict[Path, int] = {p: (0) for p in self.sources}

    def _emit(self, event: CompletionEvent) ->None:
        if self.output_path:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            with self.output_path.open('a', encoding='utf-8') as fh:
                fh.write(event.to_json() + '\n')
        if self.event_queue:
            self.event_queue.put(event)
        if self.verbose:
            logger.info(event.to_json())

    def poll(self) ->None:
        """Read new lines and emit events on completion signals."""
        for source in self.sources:
            if not source.exists():
                continue
            position = self._positions.get(source, 0)
            with source.open('r', encoding='utf-8') as fh:
                fh.seek(position)
                for line in fh:
                    if COMPLETION_SIGNAL in line:
                        task_id = line.split(COMPLETION_SIGNAL, 1)[1].strip(
                            ) or None
                        task_found = None
                        if task_id and self.task_repo:
                            task_found = self.task_repo.task_exists(task_id)
                            if not task_found and self.verbose:
                                logger.info(f'Mismatch: unknown task {task_id}'
                                    )
                        event = CompletionEvent(time.time(), str(source),
                            line.strip(), task_id, task_found)
                        self._emit(event)
                self._positions[source] = fh.tell()

    def watch(self, interval: float=1.0) ->None:
        """Continuously poll sources at the provided interval."""
        try:
            while True:
                self.poll()
                time.sleep(interval)
        except KeyboardInterrupt:
            if self.verbose:
                logger.info('Monitor stopped')


def parse_args() ->argparse.Namespace:
    parser = argparse.ArgumentParser(description=
        'Monitor logs for completion signals')
    parser.add_argument('-s', '--source', action='append', required=True,
        help='Path to a log file to monitor. Can be used multiple times.')
    parser.add_argument('-o', '--output', help=
        'Path to output file for structured events.')
    parser.add_argument('-v', '--verbose', action='store_true', help=
        'Enable verbose output.')
    parser.add_argument('-i', '--interval', type=float, default=1.0, help=
        'Polling interval in seconds.')
    return parser.parse_args()


def main() ->None:
    args = parse_args()
    repo: CursorTaskRepository | None = None
    db_path = os.getenv('CURSOR_DB_PATH')
    if db_path:
        repo = CursorTaskRepository(Path(db_path))
    monitor = TerminalCompletionMonitor(sources=[Path(p) for p in args.
        source], output_path=Path(args.output) if args.output else None,
        verbose=args.verbose, task_repo=repo)
    monitor.watch(interval=args.interval)


if __name__ == '__main__':
    main()
