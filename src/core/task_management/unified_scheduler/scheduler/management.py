from __future__ import annotations

import logging
import threading
import time

logger = logging.getLogger(__name__)


class SchedulerManagementMixin:
    """Start/stop lifecycle management for the scheduler."""

    async def start(self):
        """Start the task scheduler."""
        if self._running:
            logger.warning("Task scheduler already running")
            return

        self._running = True
        self._scheduler_thread = threading.Thread(
            target=self._scheduler_loop, daemon=True
        )
        self._scheduler_thread.start()

        logger.info("🚀 Unified Task Scheduler started")

    async def stop(self):
        """Stop the task scheduler."""
        if not self._running:
            return

        self._running = False
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)

        logger.info("⏹️ Unified Task Scheduler stopped")

    def _scheduler_loop(self):
        """Main scheduler loop for processing tasks."""
        while self._running:
            try:
                with self._lock:
                    self._process_pending_tasks()
                    self._check_expired_tasks()
                    self._cleanup_old_tasks()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)

    def shutdown(self):
        """Shutdown the task scheduler."""
        self.stop()
        logger.info("🔄 Unified Task Scheduler shutdown complete")
