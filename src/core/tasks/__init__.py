"""
Tasks Package - Agent Cellphone V2
=================================

This package contains extracted task management modules following SRP:
- definitions: Task data structures and mock enums
- executor: Task execution and workflow management
- scheduling: Task scheduling and prioritization
- monitoring: Task monitoring and status tracking
- recovery: Task recovery and error handling
- results: Task result aggregation utilities
"""

from .definitions import (
    DevelopmentTask,
    MockTaskStatus,
    MockTaskPriority,
    MockTaskComplexity,
)
from .executor import TaskExecutor
from .scheduling import TaskScheduler
from .monitoring import TaskMonitor
from .recovery import TaskRecovery
from .results import (
    get_task_statistics,
    get_task_summary,
    get_priority_distribution,
    get_complexity_distribution,
)
from .logger import get_task_logger

__all__ = [
    "DevelopmentTask",
    "MockTaskStatus",
    "MockTaskPriority",
    "MockTaskComplexity",
    "TaskExecutor",
    "TaskScheduler",
    "TaskMonitor",
    "TaskRecovery",
    "get_task_statistics",
    "get_task_summary",
    "get_priority_distribution",
    "get_complexity_distribution",
    "get_task_logger",
]
