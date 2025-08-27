from __future__ import annotations

from .base import BaseScheduler
from .management import SchedulerManagementMixin
from .task_ops import TaskOperationsMixin
from .scheduling import SchedulingMixin
from .monitoring import MonitoringMixin


class UnifiedTaskScheduler(
    BaseScheduler,
    SchedulerManagementMixin,
    TaskOperationsMixin,
    SchedulingMixin,
    MonitoringMixin,
):
    """Unified Task Scheduler composed from modular mixins."""

    pass


__all__ = ["UnifiedTaskScheduler"]
