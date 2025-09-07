"""
Tasks Package - Agent Cellphone V2
=================================

This package contains extracted task management modules following SRP:
- scheduler: Task scheduling and prioritization
- resource_manager: Resource allocation helpers
- tracker: Task status tracking
- execution: Task execution and workflow management
- monitoring: Task monitoring and status tracking
- recovery: Task recovery and error handling
- api: Coordinating API composing task services
- definitions: Task data structures and mock enums
- results: Task result aggregation utilities
"""

from .scheduler import TaskScheduler, Task, TaskPriority, TaskStatus
from .resource_manager import ResourceManager
from .tracker import TaskTracker
from .executor import TaskExecutor
from .monitoring import TaskMonitor
from .recovery import TaskRecovery
from .api import TaskService
from .logger import get_task_logger

# Additional imports from the refactored version
from .definitions import (
    DevelopmentTask,
    MockTaskStatus,
    MockTaskPriority,
    MockTaskComplexity,
)
from .results import (
    get_task_statistics,
    get_task_summary,
    get_priority_distribution,
    get_complexity_distribution,
)

__all__ = [
    "TaskScheduler",
    "ResourceManager",
    "TaskTracker",
    "TaskExecutor",
    "TaskMonitor",
    "TaskRecovery",
    "TaskService",
    "Task",
    "TaskPriority",
    "TaskStatus",
    "DevelopmentTask",
    "MockTaskStatus",
    "MockTaskPriority",
    "MockTaskComplexity",
    "get_task_statistics",
    "get_task_summary",
    "get_priority_distribution",
    "get_complexity_distribution",
    "get_task_logger",
]
