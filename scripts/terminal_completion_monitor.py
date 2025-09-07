"""Monitor terminal logs for completion signals.

This module tails specified log files and emits structured events whenever the
`COMPLETION_SIGNAL` token is detected. Events can be written to an output log
file or pushed onto an in-memory queue for downstream processing.

Usage:
    python scripts/terminal_completion_monitor.py \
        -s path/to/log1 -s path/to/log2 \
        -o logs/completion_events.log -v

The script maintains a single source of truth for the `COMPLETION_SIGNAL`
constant, allowing tests and dependent modules to import it directly.
"""

from __future__ import annotations

import argparse
import json
import queue
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

COMPLETION_SIGNAL = "COMPLETION_SIGNAL"


@dataclass
class CompletionEvent:
    """Structured event emitted when a completion signal is detected."""

    timestamp: float
    source: str
    line: str

    def to_json(self) -> str:
        """Return the event serialized as a JSON string."""
        return json.dumps({
            "timestamp": self.timestamp,
            "source": self.source,
            "line": self.line,
        })


class TerminalCompletionMonitor:
    """Tail log files and emit events when completion signals appear."""

    def __init__(
        self,
        sources: Iterable[Path],
        output_path: Optional[Path] = None,
        event_queue: Optional[queue.Queue] = None,
        verbose: bool = False,
    ) -> None:
        self.sources: List[Path] = [Path(s) for s in sources]
        self.output_path = Path(output_path) if output_path else None
        self.event_queue = event_queue
        self.verbose = verbose
        self._positions: dict[Path, int] = {p: 0 for p in self.sources}

    def _emit(self, event: CompletionEvent) -> None:
        if self.output_path:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            with self.output_path.open("a", encoding="utf-8") as fh:
                fh.write(event.to_json() + "\n")
        if self.event_queue:
            self.event_queue.put(event)
        if self.verbose:
            print(event.to_json())

    def poll(self) -> None:
        """Read new lines and emit events on completion signals."""
        for source in self.sources:
            if not source.exists():
                continue
            position = self._positions.get(source, 0)
            with source.open("r", encoding="utf-8") as fh:
                fh.seek(position)
                for line in fh:
                    if COMPLETION_SIGNAL in line:
                        event = CompletionEvent(
                            time.time(),
                            str(source),
                            line.strip(),
                        )
                        self._emit(event)
                self._positions[source] = fh.tell()

    def watch(self, interval: float = 1.0) -> None:
        """Continuously poll sources at the provided interval."""
        try:
            while True:
                self.poll()
                time.sleep(interval)
        except KeyboardInterrupt:
            if self.verbose:
                print("Monitor stopped")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitor logs for completion signals",
    )
    parser.add_argument(
        "-s",
        "--source",
        action="append",
        required=True,
        help="Path to a log file to monitor. Can be used multiple times.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output file for structured events.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=1.0,
        help="Polling interval in seconds.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    monitor = TerminalCompletionMonitor(
        sources=[Path(p) for p in args.source],
        output_path=Path(args.output) if args.output else None,
        verbose=args.verbose,
    )
    monitor.watch(interval=args.interval)


if __name__ == "__main__":
    main()
