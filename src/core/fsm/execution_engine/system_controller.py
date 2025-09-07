#!/usr/bin/env python3
"""System control and monitoring mixin for FSM core."""

import threading
import time
from datetime import datetime


class SystemController:
    """Provides system lifecycle management."""

    def start_system(self) -> bool:
        """Start FSM system."""
        try:
            if self.is_running:
                return True

            self.is_running = True
            self._start_monitoring()
            self.logger.info("✅ FSM system started successfully")
            return True

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to start FSM system: {e}")
            return False

    def stop_system(self) -> bool:
        """Stop FSM system."""
        try:
            if not self.is_running:
                return True

            self.is_running = False
            self._stop_monitoring()

            for workflow_id in list(self.active_workflows):
                self.stop_workflow(workflow_id)

            self.logger.info("✅ FSM system stopped successfully")
            return True

        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to stop FSM system: {e}")
            return False

    def _start_monitoring(self) -> None:
        """Start FSM monitoring thread."""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitoring_thread.start()
        self.logger.info("✅ FSM monitoring started")

    def _stop_monitoring(self) -> None:
        """Stop FSM monitoring thread."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        self.logger.info("✅ FSM monitoring stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring_active and self.is_running:
            try:
                self._process_workflow_queue()
                self._check_timeouts()
                interval = self.config.get("monitoring", {}).get("interval", 1.0)
                time.sleep(interval)
            except Exception as e:  # pragma: no cover - defensive
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(1.0)

    def _process_workflow_queue(self) -> None:
        """Process pending workflows in queue."""
        while (
            self.workflow_queue
            and len(self.active_workflows) < self.max_concurrent_workflows
        ):
            workflow_id = self.workflow_queue.popleft()
            self.start_workflow(workflow_id)

    def _check_timeouts(self) -> None:
        """Check for workflow timeouts."""
        current_time = datetime.now()

        for workflow_id in list(self.active_workflows):
            workflow = self.workflows[workflow_id]
            state_def = self.states.get(workflow.current_state)

            if state_def and state_def.timeout_seconds:
                elapsed = (current_time - workflow.last_update).total_seconds()
                if elapsed > state_def.timeout_seconds:
                    self.logger.warning(
                        f"Workflow {workflow_id} timed out in state {workflow.current_state}"
                    )
                    self._handle_state_timeout(
                        workflow_id, workflow.current_state, None
                    )


__all__ = ["SystemController"]
