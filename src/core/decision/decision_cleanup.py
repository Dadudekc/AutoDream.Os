#!/usr/bin/env python3
"""Decision cleanup orchestrator."""

import logging
from typing import Any, Dict

from .cleanup_executor import CleanupExecutor
from .cleanup_resources import CleanupResources
from .cleanup_scheduler import CleanupScheduler


class DecisionCleanupManager:
    """Orchestrates cleanup scheduling, execution, and resources."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.DecisionCleanupManager")
        self.resources = CleanupResources(self.logger)
        self.executor = CleanupExecutor(self.resources, self.logger)
        self.scheduler = CleanupScheduler(self.resources, self.executor, self.logger)
        self.initialized = False
        self.logger.info("DecisionCleanupManager initialized")

    def initialize(self) -> None:
        if self.initialized:
            self.logger.info("Cleanup manager already initialized")
            return
        self.resources.initialize_default_schedules()
        self.resources.initialize_default_tasks()
        self.initialized = True
        self.logger.info("Cleanup manager initialized successfully")

    def shutdown(self) -> None:
        self.scheduler.stop()
        self.resources.clear()
        self.initialized = False
        self.logger.info("Cleanup manager shutdown successfully")

    def schedule_cleanup(self) -> None:
        if not self.initialized:
            self.logger.warning("Cleanup manager not initialized, skipping scheduler")
            return
        self.scheduler.start()

    def stop_cleanup_scheduler(self) -> None:
        self.scheduler.stop()

    def should_perform_cleanup(self) -> bool:
        if not self.initialized:
            return False
        return self.scheduler.should_perform_cleanup()

    def cleanup_completed_decisions(self) -> None:
        if not self.initialized:
            self.logger.warning("Cleanup manager not initialized, skipping cleanup")
            return
        self.executor.execute_cleanup_task("cleanup_completed_decisions")

    def get_cleanup_status(self) -> Dict[str, Any]:
        return {
            "initialized": self.initialized,
            "scheduler_running": self.scheduler.scheduler_running,
            "total_schedules": len(self.resources.cleanup_schedules),
            "active_schedules": len(
                [s for s in self.resources.cleanup_schedules.values() if s.is_active]
            ),
            "total_tasks": len(self.resources.cleanup_tasks),
            "pending_tasks": len(
                [
                    t
                    for t in self.resources.cleanup_tasks.values()
                    if t.status == "pending"
                ]
            ),
            "executing_tasks": len(
                [
                    t
                    for t in self.resources.cleanup_tasks.values()
                    if t.status == "executing"
                ]
            ),
            "completed_tasks": len(
                [t for t in self.resources.cleanup_history if t.status == "completed"]
            ),
            "failed_tasks": len(
                [t for t in self.resources.cleanup_history if t.status == "failed"]
            ),
            "total_history": len(self.resources.cleanup_history),
        }

    get_status = get_cleanup_status
