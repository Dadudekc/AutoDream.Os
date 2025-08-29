#!/usr/bin/env python3
"""Task scheduling utilities for decision coordination."""

import threading
import time
from typing import Callable, Dict

from .coordination_status import CoordinationStatus


class CoordinationScheduler:
    """Schedule and run coordination sessions in background threads."""

    def __init__(
        self,
        gather_inputs: Callable,
        deliberate: Callable,
        build_consensus: Callable,
        finalize: Callable,
        handle_failure: Callable,
    ):
        self.gather_inputs = gather_inputs
        self.deliberate = deliberate
        self.build_consensus = build_consensus
        self.finalize = finalize
        self.handle_failure = handle_failure

    def start(self, system, session, protocol: Dict) -> threading.Thread:
        """Start coordination process in a daemon thread."""
        thread = threading.Thread(
            target=self._run_process, args=(system, session, protocol), daemon=True
        )
        thread.start()
        return thread

    def _run_process(self, system, session, protocol: Dict) -> None:
        """Execute the coordination process."""
        try:
            self.gather_inputs(system, session)
            self.deliberate(system, session, protocol)
            if self.build_consensus(system, session, protocol):
                self.finalize(system, session)
            else:
                self.handle_failure(system, session, protocol)
        except Exception as exc:
            system.logger.error(
                f"Coordination process failed for session {session.session_id}: {exc}"
            )
            session.status = CoordinationStatus.FAILED.value
            session.end_time = time.time()
