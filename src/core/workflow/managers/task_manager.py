#!/usr/bin/env python3
"""
Task Manager - Unified Task Management System
============================================

Unified task management system following V2 standards.
Provides task creation, assignment, and tracking capabilities.

Author: Agent-8 (Integration Enhancement Manager)
License: MIT
"""

import logging
import time
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class Task:
    """Task representation"""
    
    # Core task information
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    
    # Assignment and execution
    assigned_agent: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Task details
    estimated_duration: Optional[int] = None  # minutes
    actual_duration: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # Performance metrics
    retry_count: int = 0
    error_messages: List[str] = field(default_factory=list)
    
    def is_active(self) -> bool:
        """Check if task is currently active"""
        return self.status in [TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]
    
    def is_completed(self) -> bool:
        """Check if task is completed"""
        return self.status == TaskStatus.COMPLETED
    
    def is_failed(self) -> bool:
        """Check if task has failed"""
        return self.status == TaskStatus.FAILED
    
    def can_start(self) -> bool:
        """Check if task can start execution"""
        return self.status == TaskStatus.ASSIGNED and not self.dependencies


class TaskManager:
    """Unified task management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.TaskManager")
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []
        self.assigned_tasks: Dict[str, List[str]] = {}  # agent_id -> task_ids
        
        # Performance tracking
        self.task_statistics = {
            "total_tasks": 0,
            "pending_tasks": 0,
            "assigned_tasks": 0,
            "in_progress_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "blocked_tasks": 0
        }
        
        # Initialize thread pool for parallel task processing
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        self.logger.info("✅ TaskManager initialized")
    
    def create_task(self, title: str, description: str, priority: TaskPriority = TaskPriority.MEDIUM,
                   estimated_duration: Optional[int] = None, tags: Optional[List[str]] = None) -> str:
        """
        Create a new task
        
        Args:
            title: Task title
            description: Task description
            priority: Task priority level
            estimated_duration: Estimated duration in minutes
            tags: Task tags
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            estimated_duration=estimated_duration,
            tags=tags or []
        )
        
        self.tasks[task_id] = task
        self.task_queue.append(task_id)
        self._update_statistics()
        
        self.logger.info(f"✅ Task created: {task_id} - {title}")
        return task_id
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """
        Assign task to agent
        
        Args:
            task_id: Task identifier
            agent_id: Agent identifier
            
        Returns:
            True if assignment successful
        """
        if task_id not in self.tasks:
            self.logger.error(f"❌ Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        if task.status != TaskStatus.PENDING:
            self.logger.warning(f"⚠️ Task {task_id} not in pending status: {task.status}")
            return False
        
        # Assign task
        task.status = TaskStatus.ASSIGNED
        task.assigned_agent = agent_id
        task.assigned_at = datetime.now()
        
        # Update agent assignment tracking
        if agent_id not in self.assigned_tasks:
            self.assigned_tasks[agent_id] = []
        self.assigned_tasks[agent_id].append(task_id)
        
        # Remove from queue
        if task_id in self.task_queue:
            self.task_queue.remove(task_id)
        
        self._update_statistics()
        
        self.logger.info(f"✅ Task {task_id} assigned to agent {agent_id}")
        return True
    
    def start_task(self, task_id: str) -> bool:
        """
        Start task execution
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if task started successfully
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        if task.status != TaskStatus.ASSIGNED:
            self.logger.warning(f"⚠️ Task {task_id} not assigned: {task.status}")
            return False
        
        if task.dependencies:
            self.logger.warning(f"⚠️ Task {task_id} has unmet dependencies")
            return False
        
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        
        self._update_statistics()
        
        self.logger.info(f"✅ Task {task_id} started execution")
        return True
    
    def complete_task(self, task_id: str, result: Optional[Dict[str, Any]] = None) -> bool:
        """
        Mark task as completed
        
        Args:
            task_id: Task identifier
            result: Task completion result
            
        Returns:
            True if task completed successfully
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        if task.status != TaskStatus.IN_PROGRESS:
            self.logger.warning(f"⚠️ Task {task_id} not in progress: {task.status}")
            return False
        
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        
        # Calculate actual duration
        if task.started_at:
            duration = (task.completed_at - task.started_at).total_seconds() / 60
            task.actual_duration = int(duration)
        
        # Remove from agent's assigned tasks
        if task.assigned_agent and task.assigned_agent in self.assigned_tasks:
            if task_id in self.assigned_tasks[task.assigned_agent]:
                self.assigned_tasks[task.assigned_agent].remove(task_id)
        
        self._update_statistics()
        
        self.logger.info(f"✅ Task {task_id} completed successfully")
        return True
    
    def fail_task(self, task_id: str, error_message: str) -> bool:
        """
        Mark task as failed
        
        Args:
            task_id: Task identifier
            error_message: Error description
            
        Returns:
            True if task marked as failed
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.FAILED
        task.error_messages.append(error_message)
        task.retry_count += 1
        
        # Remove from agent's assigned tasks
        if task.assigned_agent and task.assigned_agent in self.assigned_tasks:
            if task_id in self.assigned_tasks[task.assigned_agent]:
                self.assigned_tasks[task.assigned_agent].remove(task_id)
        
        self._update_statistics()
        
        self.logger.error(f"❌ Task {task_id} failed: {error_message}")
        return True
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """Get current task statistics"""
        return self.task_statistics.copy()
    
    def get_available_tasks(self) -> List[Task]:
        """Get list of available (pending) tasks"""
        return [self.tasks[task_id] for task_id in self.task_queue 
                if task_id in self.tasks]
    
    def get_agent_tasks(self, agent_id: str) -> List[Task]:
        """Get tasks assigned to specific agent"""
        if agent_id not in self.assigned_tasks:
            return []
        
        return [self.tasks[task_id] for task_id in self.assigned_tasks[agent_id]
                if task_id in self.tasks]
    
    def _update_statistics(self):
        """Update task statistics"""
        self.task_statistics["total_tasks"] = len(self.tasks)
        self.task_statistics["pending_tasks"] = len(self.task_queue)
        self.task_statistics["assigned_tasks"] = sum(
            1 for task in self.tasks.values() if task.status == TaskStatus.ASSIGNED
        )
        self.task_statistics["in_progress_tasks"] = sum(
            1 for task in self.tasks.values() if task.status == TaskStatus.IN_PROGRESS
        )
        self.task_statistics["completed_tasks"] = sum(
            1 for task in self.tasks.values() if task.status == TaskStatus.COMPLETED
        )
        self.task_statistics["failed_tasks"] = sum(
            1 for task in self.tasks.values() if task.status == TaskStatus.FAILED
        )
        self.task_statistics["blocked_tasks"] = sum(
            1 for task in self.tasks.values() if task.status == TaskStatus.BLOCKED
        )
