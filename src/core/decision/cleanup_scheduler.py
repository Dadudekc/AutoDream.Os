#!/usr/bin/env python3
"""Scheduling logic for decision cleanup."""

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Optional

from .cleanup_resources import CleanupResources, CleanupSchedule
from .cleanup_executor import CleanupExecutor


class CleanupScheduler:
    """Handles scheduling and execution timing for cleanup tasks."""

    def __init__(
        self,
        resources: CleanupResources,
        executor: CleanupExecutor,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.resources = resources
        self.executor = executor
        self.logger = logger or logging.getLogger(f"{__name__}.CleanupScheduler")
        self.cleanup_thread: Optional[threading.Thread] = None
        self.scheduler_running = False
        self.stop_event = threading.Event()

    def start(self) -> None:
        """Start the scheduler loop."""
        if self.scheduler_running:
            self.logger.info("Cleanup scheduler already running")
            return
        self.stop_event.clear()
        self.scheduler_running = True
        self.cleanup_thread = threading.Thread(
            target=self._scheduler_loop,
            daemon=True,
            name="DecisionCleanupScheduler",
        )
        self.cleanup_thread.start()
        self.logger.info("Cleanup scheduler started successfully")

    def stop(self) -> None:
        """Stop the scheduler loop."""
        if not self.scheduler_running:
            self.logger.info("Cleanup scheduler not running")
            return
        self.stop_event.set()
        self.scheduler_running = False
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            self.cleanup_thread.join(timeout=5.0)
        self.logger.info("Cleanup scheduler stopped successfully")

    def _scheduler_loop(self) -> None:
        """Main scheduler loop."""
        self.logger.info("Cleanup scheduler loop started")
        while not self.stop_event.is_set():
            try:
                self._check_scheduled_cleanups()
                time.sleep(30)
            except Exception as exc:  # pragma: no cover - defensive logging
                self.logger.error("Error in cleanup scheduler loop: %s", exc)
                time.sleep(60)
        self.logger.info("Cleanup scheduler loop stopped")

    def _check_scheduled_cleanups(self) -> None:
        """Check and execute due schedules."""
        current_time = datetime.now()
        for schedule in self.resources.cleanup_schedules.values():
            if not schedule.is_active:
                continue
            if self._should_execute_schedule(schedule, current_time):
                self._execute_scheduled_cleanup(schedule)

    def _should_execute_schedule(
        self, schedule: CleanupSchedule, current_time: datetime
    ) -> bool:
        if not schedule.last_execution:
            return True
        last_execution = datetime.fromisoformat(schedule.last_execution)
        time_since_last = current_time - last_execution
        return time_since_last.total_seconds() >= (schedule.interval_minutes * 60)

    def _execute_scheduled_cleanup(self, schedule: CleanupSchedule) -> None:
        self.logger.info("Executing scheduled cleanup: %s", schedule.name)
        for task_id in schedule.tasks:
            if task_id in self.resources.cleanup_tasks:
                self.executor.execute_cleanup_task(task_id)
        schedule.last_execution = datetime.now().isoformat()
        schedule.next_execution = (
            datetime.now() + timedelta(minutes=schedule.interval_minutes)
        ).isoformat()
        self.logger.info("Scheduled cleanup completed: %s", schedule.name)

    def should_perform_cleanup(self) -> bool:
        """Determine if any schedule is due for execution."""
        current_time = datetime.now()
        for schedule in self.resources.cleanup_schedules.values():
            if not schedule.is_active:
                continue
            if self._should_execute_schedule(schedule, current_time):
                return True
        return False
