"""
Task Manager - Extracted from autonomous_development.py

This module handles task management including:
- Task scheduling and execution
- Task lifecycle management
- Task dependencies and coordination
- Task performance monitoring

Original file: src/core/autonomous_development.py
Extraction date: 2024-12-19
"""

import time
import threading
import logging
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from queue import PriorityQueue

# Configure logging
logger = logging.getLogger(__name__)

# Import from main file - using type hints to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...core.autonomous_development import DevelopmentAction


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskPriority(Enum):
    """Task priority enumeration"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


@dataclass
class Task:
    """Task definition"""
    task_id: str
    name: str
    description: str
    action_type: str
    target_element: str
    action_data: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout: float = 30.0
    cooldown: float = 1.0


class TaskManager:
    """Task manager - SRP: Manage task scheduling and execution"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.TaskManager")
        
        # Task storage
        self.tasks: Dict[str, Task] = {}
        self.task_queue: PriorityQueue = PriorityQueue()
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = {}
        
        # Task execution
        self.is_running = False
        self.execution_thread: Optional[threading.Thread] = None
        self.task_lock = threading.RLock()
        
        # Performance tracking
        self.total_tasks_processed = 0
        self.successful_tasks = 0
        self.failed_tasks_count = 0
        self.start_time: Optional[datetime] = None
        
    def start_task_manager(self) -> bool:
        """Start the task manager"""
        try:
            if self.is_running:
                self.logger.warning("Task manager already running")
                return False
            
            self.is_running = True
            self.start_time = datetime.now()
            
            # Start task execution thread
            self.execution_thread = threading.Thread(
                target=self._task_execution_loop, daemon=True
            )
            self.execution_thread.start()
            
            self.logger.info("🚀 Task Manager Started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start task manager: {e}")
            return False
    
    def stop_task_manager(self) -> bool:
        """Stop the task manager"""
        try:
            if not self.is_running:
                return True
            
            self.is_running = False
            
            # Wait for execution thread to finish
            if self.execution_thread and self.execution_thread.is_alive():
                self.execution_thread.join(timeout=5)
            
            self.logger.info("⏹️ Task Manager Stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop task manager: {e}")
            return False
    
    def create_task(self, task_config: Dict[str, Any]) -> Optional[str]:
        """Create a new task"""
        try:
            task_id = task_config.get('task_id') or f"task_{int(time.time())}"
            
            # Create task object
            task = Task(
                task_id=task_id,
                name=task_config.get('name', 'Unnamed Task'),
                description=task_config.get('description', ''),
                action_type=task_config.get('action_type', 'unknown'),
                target_element=task_config.get('target_element', ''),
                action_data=task_config.get('action_data', {}),
                priority=TaskPriority(task_config.get('priority', TaskPriority.NORMAL.value)),
                dependencies=task_config.get('dependencies', []),
                timeout=task_config.get('timeout', 30.0),
                cooldown=task_config.get('cooldown', 1.0),
                max_retries=task_config.get('max_retries', 3)
            )
            
            with self.task_lock:
                self.tasks[task_id] = task
                
                # Add to priority queue if no dependencies
                if not task.dependencies:
                    self._schedule_task(task)
            
            self.logger.info(f"Created task: {task_id} - {task.name}")
            return task_id
            
        except Exception as e:
            self.logger.error(f"Failed to create task: {e}")
            return None
    
    def _schedule_task(self, task: Task):
        """Schedule a task for execution"""
        try:
            # Calculate priority score (higher priority = lower score for PriorityQueue)
            priority_score = (TaskPriority.CRITICAL.value - task.priority.value, 
                            task.created_at.timestamp())
            
            self.task_queue.put((priority_score, task))
            task.status = TaskStatus.SCHEDULED
            task.scheduled_at = datetime.now()
            
            self.logger.debug(f"Scheduled task: {task.task_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to schedule task {task.task_id}: {e}")
    
    def _task_execution_loop(self):
        """Main task execution loop"""
        try:
            while self.is_running:
                # Process available tasks
                self._process_available_tasks()
                
                # Check for completed dependencies
                self._check_dependencies()
                
                # Brief pause
                time.sleep(0.1)
                
        except Exception as e:
            self.logger.error(f"Task execution loop error: {e}")
    
    def _process_available_tasks(self):
        """Process available tasks from the queue"""
        try:
            while not self.task_queue.empty() and len(self.running_tasks) < 5:  # Max 5 concurrent tasks
                priority_score, task = self.task_queue.get_nowait()
                
                if task.status == TaskStatus.SCHEDULED:
                    self._execute_task(task)
                    
        except Exception as e:
            self.logger.error(f"Failed to process available tasks: {e}")
    
    def _execute_task(self, task: Task):
        """Execute a single task"""
        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            self.running_tasks[task.task_id] = task
            
            self.logger.info(f"Executing task: {task.task_id} - {task.name}")
            
            # Execute task action (placeholder for now)
            success = self._execute_task_action(task)
            
            if success:
                self._complete_task(task)
            else:
                self._handle_task_failure(task)
                
        except Exception as e:
            self.logger.error(f"Task execution error for {task.task_id}: {e}")
            self._handle_task_failure(task)
    
    def _execute_task_action(self, task: Task) -> bool:
        """Execute the actual task action"""
        try:
            # Placeholder for task execution logic
            # In real implementation, this would execute the specific action
            time.sleep(0.1)  # Simulate work
            
            # For now, return success
            return True
            
        except Exception as e:
            self.logger.error(f"Task action execution failed: {e}")
            return False
    
    def _complete_task(self, task: Task):
        """Mark task as completed"""
        try:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            # Remove from running tasks
            if task.task_id in self.running_tasks:
                del self.running_tasks[task.task_id]
            
            # Add to completed tasks
            self.completed_tasks.append(task)
            
            # Update metrics
            self.total_tasks_processed += 1
            self.successful_tasks += 1
            
            self.logger.info(f"Completed task: {task.task_id}")
            
            # Check for dependent tasks
            self._check_dependent_tasks(task.task_id)
            
        except Exception as e:
            self.logger.error(f"Failed to complete task {task.task_id}: {e}")
    
    def _handle_task_failure(self, task: Task):
        """Handle task failure"""
        try:
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.RETRYING
                
                # Reschedule task after cooldown
                threading.Timer(task.cooldown, lambda: self._reschedule_task(task)).start()
                
                self.logger.warning(f"Task {task.task_id} failed, retrying ({task.retry_count}/{task.max_retries})")
                
            else:
                task.status = TaskStatus.FAILED
                self.failed_tasks[task.task_id] = task
                
                # Remove from running tasks
                if task.task_id in self.running_tasks:
                    del self.running_tasks[task.task_id]
                
                # Update metrics
                self.total_tasks_processed += 1
                self.failed_tasks_count += 1
                
                self.logger.error(f"Task {task.task_id} failed permanently after {task.max_retries} retries")
            
        except Exception as e:
            self.logger.error(f"Failed to handle task failure for {task.task_id}: {e}")
    
    def _reschedule_task(self, task: Task):
        """Reschedule a failed task"""
        try:
            task.status = TaskStatus.SCHEDULED
            self._schedule_task(task)
            
        except Exception as e:
            self.logger.error(f"Failed to reschedule task {task.task_id}: {e}")
    
    def _check_dependencies(self):
        """Check if any pending tasks have completed dependencies"""
        try:
            with self.task_lock:
                for task_id, task in list(self.tasks.items()):
                    if (task.status == TaskStatus.PENDING and 
                        self._are_dependencies_met(task)):
                        self._schedule_task(task)
                        
        except Exception as e:
            self.logger.error(f"Failed to check dependencies: {e}")
    
    def _are_dependencies_met(self, task: Task) -> bool:
        """Check if all dependencies for a task are met"""
        try:
            for dep_id in task.dependencies:
                if dep_id not in self.tasks:
                    return False
                
                dep_task = self.tasks[dep_id]
                if dep_task.status != TaskStatus.COMPLETED:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to check dependencies for task {task.task_id}: {e}")
            return False
    
    def _check_dependent_tasks(self, completed_task_id: str):
        """Check if any tasks depend on the completed task"""
        try:
            with self.task_lock:
                for task_id, task in list(self.tasks.items()):
                    if (task.status == TaskStatus.PENDING and 
                        completed_task_id in task.dependencies):
                        if self._are_dependencies_met(task):
                            self._schedule_task(task)
                            
        except Exception as e:
            self.logger.error(f"Failed to check dependent tasks: {e}")
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        try:
            if task_id not in self.tasks:
                return None
            
            task = self.tasks[task_id]
            return {
                "task_id": task.task_id,
                "name": task.name,
                "status": task.status.value,
                "priority": task.priority.value,
                "created_at": task.created_at.isoformat(),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "retry_count": task.retry_count,
                "dependencies": task.dependencies
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get task status: {e}")
            return None
    
    def get_task_manager_stats(self) -> Dict[str, Any]:
        """Get task manager statistics"""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            
            return {
                "is_running": self.is_running,
                "uptime_seconds": uptime,
                "total_tasks": len(self.tasks),
                "pending_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING]),
                "scheduled_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.SCHEDULED]),
                "running_tasks": len(self.running_tasks),
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "total_processed": self.total_tasks_processed,
                "successful": self.successful_tasks,
                "failed": self.failed_tasks_count
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get task manager stats: {e}")
            return {"error": str(e)}
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending or scheduled task"""
        try:
            with self.task_lock:
                if task_id not in self.tasks:
                    return False
                
                task = self.tasks[task_id]
                if task.status in [TaskStatus.PENDING, TaskStatus.SCHEDULED]:
                    task.status = TaskStatus.CANCELLED
                    self.logger.info(f"Cancelled task: {task_id}")
                    return True
                
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to cancel task {task_id}: {e}")
            return False
            
    def stop_task_manager(self):
        """Stop the task manager"""
        self.is_running = False
        self.logger.info("Task manager stopped")
        
    def get_task_manager_stats(self) -> Dict[str, Any]:
        """Get task manager statistics"""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            
            return {
                "is_running": self.is_running,
                "uptime_seconds": uptime,
                "total_tasks": len(self.tasks),
                "pending_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING]),
                "scheduled_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.SCHEDULED]),
                "running_tasks": len(self.running_tasks),
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "total_processed": self.total_tasks_processed,
                "successful": self.successful_tasks,
                "failed": self.failed_tasks_count
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get task manager stats: {e}")
            return {"error": str(e)}
