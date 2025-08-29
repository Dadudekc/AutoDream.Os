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
"""

from .scheduler import TaskScheduler, Task, TaskPriority, TaskStatus
from .resource_manager import ResourceManager
from .tracker import TaskTracker
from .execution import TaskExecutor
from .monitoring import TaskMonitor
from .recovery import TaskRecovery
from .api import TaskService
from .logger import get_task_logger

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
    "get_task_logger",
]
