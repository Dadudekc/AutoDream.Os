#!/usr/bin/env python3
"""Resource management for decision cleanup."""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class CleanupTask:
    """Represents an individual cleanup task."""

    task_id: str
    task_type: str
    description: str
    priority: int
    scheduled_time: str
    execution_time: Optional[str] = None
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


@dataclass
class CleanupSchedule:
    """Represents a cleanup schedule configuration."""

    schedule_id: str
    name: str
    description: str
    interval_minutes: int
    last_execution: Optional[str] = None
    next_execution: Optional[str] = None
    is_active: bool = True
    tasks: List[str] = field(default_factory=list)


class CleanupResources:
    """Manages cleanup tasks, schedules, and history."""

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self.logger = logger or logging.getLogger(f"{__name__}.CleanupResources")
        self.cleanup_tasks: Dict[str, CleanupTask] = {}
        self.cleanup_schedules: Dict[str, CleanupSchedule] = {}
        self.cleanup_history: List[CleanupTask] = []
        self.default_cleanup_interval = 15  # minutes
        self.max_history_size = 1000
        self.max_cleanup_age_hours = 24

    def initialize_default_schedules(self) -> None:
        """Create default cleanup schedules."""
        try:
            regular_schedule = CleanupSchedule(
                schedule_id="regular_cleanup",
                name="Regular Cleanup Schedule",
                description="Regular cleanup of completed decisions and old data",
                interval_minutes=self.default_cleanup_interval,
                tasks=[
                    "cleanup_completed_decisions",
                    "cleanup_old_history",
                    "cleanup_expired_data",
                ],
            )
            self.cleanup_schedules["regular_cleanup"] = regular_schedule

            performance_schedule = CleanupSchedule(
                schedule_id="performance_cleanup",
                name="Performance Cleanup Schedule",
                description="Cleanup for performance optimization",
                interval_minutes=30,
                tasks=[
                    "cleanup_performance_data",
                    "cleanup_old_metrics",
                    "optimize_resources",
                ],
            )
            self.cleanup_schedules["performance_cleanup"] = performance_schedule

            maintenance_schedule = CleanupSchedule(
                schedule_id="maintenance_cleanup",
                name="Maintenance Cleanup Schedule",
                description="Maintenance cleanup tasks",
                interval_minutes=60,
                tasks=["cleanup_logs", "cleanup_temp_data", "system_maintenance"],
            )
            self.cleanup_schedules["maintenance_cleanup"] = maintenance_schedule

            self.logger.info(
                "Initialized %d default cleanup schedules",
                len(self.cleanup_schedules),
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.error("Failed to initialize default cleanup schedules: %s", exc)

    def initialize_default_tasks(self) -> None:
        """Create default cleanup tasks."""
        try:
            now = datetime.now().isoformat()
            self.cleanup_tasks["cleanup_completed_decisions"] = CleanupTask(
                task_id="cleanup_completed_decisions",
                task_type="decision_cleanup",
                description="Clean up completed decisions from active tracking",
                priority=1,
                scheduled_time=now,
            )
            self.cleanup_tasks["cleanup_old_history"] = CleanupTask(
                task_id="cleanup_old_history",
                task_type="history_cleanup",
                description="Clean up old decision history data",
                priority=2,
                scheduled_time=now,
            )
            self.cleanup_tasks["cleanup_expired_data"] = CleanupTask(
                task_id="cleanup_expired_data",
                task_type="data_cleanup",
                description="Clean up expired decision data",
                priority=3,
                scheduled_time=now,
            )
            self.cleanup_tasks["cleanup_performance_data"] = CleanupTask(
                task_id="cleanup_performance_data",
                task_type="performance_cleanup",
                description="Clean up old performance data",
                priority=2,
                scheduled_time=now,
            )
            self.cleanup_tasks["cleanup_old_metrics"] = CleanupTask(
                task_id="cleanup_old_metrics",
                task_type="metrics_cleanup",
                description="Clean up old metrics data",
                priority=2,
                scheduled_time=now,
            )
            self.cleanup_tasks["optimize_resources"] = CleanupTask(
                task_id="optimize_resources",
                task_type="resource_optimization",
                description="Optimize resource usage and allocation",
                priority=1,
                scheduled_time=now,
            )
            self.cleanup_tasks["cleanup_logs"] = CleanupTask(
                task_id="cleanup_logs",
                task_type="log_cleanup",
                description="Clean up old log files and data",
                priority=3,
                scheduled_time=now,
            )
            self.cleanup_tasks["cleanup_temp_data"] = CleanupTask(
                task_id="cleanup_temp_data",
                task_type="temp_cleanup",
                description="Clean up temporary data and files",
                priority=3,
                scheduled_time=now,
            )
            self.cleanup_tasks["system_maintenance"] = CleanupTask(
                task_id="system_maintenance",
                task_type="maintenance",
                description="Perform system maintenance tasks",
                priority=2,
                scheduled_time=now,
            )
            self.logger.info(
                "Initialized %d default cleanup tasks", len(self.cleanup_tasks)
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            self.logger.error("Failed to initialize default cleanup tasks: %s", exc)

    def clear(self) -> None:
        """Remove all tasks, schedules, and history."""
        self.cleanup_tasks.clear()
        self.cleanup_schedules.clear()
        self.cleanup_history.clear()
