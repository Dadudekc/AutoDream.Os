from datetime import datetime
from typing import Dict, List, Any, Optional, Callable, Tuple
from typing import TYPE_CHECKING
import logging
import threading

    from ...core.autonomous_development import DevelopmentAction
from ...core.base_manager import BaseManager, ManagerStatus, ManagerPriority
from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
import time

"""
Task Manager - Extracted from autonomous_development.py

This module handles task management including:
- Task scheduling and execution
- Task lifecycle management
- Task dependencies and coordination
- Task performance monitoring

Now inherits from BaseManager for unified functionality.

Original file: src/core/autonomous_development.py
Extraction date: 2024-12-19
V2 Standards: ≤200 LOC, SRP, OOP principles, BaseManager inheritance
"""



# Configure logging
logger = logging.getLogger(__name__)

# Import from main file - using type hints to avoid circular imports
if TYPE_CHECKING:


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


class TaskManager(BaseManager):
    """
    Task manager - SRP: Manage task scheduling and execution
    
    Now inherits from BaseManager for unified functionality
    """
    
    def __init__(self):
        """Initialize task manager with BaseManager"""
        super().__init__(
            manager_id="task_manager",
            name="Task Manager",
            description="Manages task scheduling and execution"
        )
        
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
        
        self.logger.info("Task Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize task management system"""
        try:
            self.logger.info("Starting Task Manager...")
            
            # Clear task data
            self.tasks.clear()
            self.running_tasks.clear()
            self.completed_tasks.clear()
            self.failed_tasks.clear()
            
            # Reset metrics
            self.total_tasks_processed = 0
            self.successful_tasks = 0
            self.failed_tasks_count = 0
            self.start_time = None
            
            # Start task execution
            if not self.start_task_manager():
                raise RuntimeError("Failed to start task execution")
            
            self.logger.info("Task Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Task Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup task management system"""
        try:
            self.logger.info("Stopping Task Manager...")
            
            # Stop task execution
            self.stop_task_manager()
            
            # Save task data
            self._save_task_data()
            
            # Clear data
            self.tasks.clear()
            self.running_tasks.clear()
            self.completed_tasks.clear()
            self.failed_tasks.clear()
            
            self.logger.info("Task Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Task Manager: {e}")
    
    def _on_heartbeat(self):
        """Task manager heartbeat"""
        try:
            # Check task health
            self._check_task_health()
            
            # Process available tasks
            if self.is_running:
                self._process_available_tasks()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize task manager resources"""
        try:
            # Initialize data structures
            self.tasks = {}
            self.task_queue = PriorityQueue()
            self.running_tasks = {}
            self.completed_tasks = []
            self.failed_tasks = []
            
            # Initialize execution state
            self.is_running = False
            self.execution_thread = None
            self.task_lock = threading.RLock()
            
            # Initialize metrics
            self.total_tasks_processed = 0
            self.successful_tasks = 0
            self.failed_tasks_count = 0
            self.start_time = None
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup task manager resources"""
        try:
            # Clear data
            self.tasks.clear()
            self.running_tasks.clear()
            self.completed_tasks.clear()
            self.failed_tasks.clear()
            
            # Stop execution thread
            if self.execution_thread and self.execution_thread.is_alive():
                self.is_running = False
                self.execution_thread.join(timeout=5)
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reset task state
            self.tasks.clear()
            self.running_tasks.clear()
            self.completed_tasks.clear()
            self.failed_tasks.clear()
            
            # Reset metrics
            self.total_tasks_processed = 0
            self.successful_tasks = 0
            self.failed_tasks_count = 0
            
            # Restart task execution if needed
            if "task" in context.lower():
                self.logger.info("Attempting to restart task execution...")
                return self.start_task_manager()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Task Management Methods
    # ============================================================================
    
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
            
            # Record operation
            self.record_operation("start_task_manager", True, 0.0)
            
            self.logger.info("🚀 Task Manager Started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start task manager: {e}")
            self.record_operation("start_task_manager", False, 0.0)
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
            
            # Record operation
            self.record_operation("stop_task_manager", True, 0.0)
            
            self.logger.info("⏹️ Task Manager Stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop task manager: {e}")
            self.record_operation("stop_task_manager", False, 0.0)
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
            
            # Record operation
            self.record_operation("create_task", True, 0.0)
            
            self.logger.info(f"Created task: {task_id} - {task.name}")
            return task_id
            
        except Exception as e:
            self.logger.error(f"Failed to create task: {e}")
            self.record_operation("create_task", False, 0.0)
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
            
            # Record operation
            self.record_operation("complete_task", True, 0.0)
            
            self.logger.info(f"Completed task: {task.task_id}")
            
            # Check for dependent tasks
            self._check_dependent_tasks(task.task_id)
            
        except Exception as e:
            self.logger.error(f"Failed to complete task {task.task_id}: {e}")
            self.record_operation("complete_task", False, 0.0)
    
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
                self.failed_tasks.append(task)
                
                # Remove from running tasks
                if task.task_id in self.running_tasks:
                    del self.running_tasks[task.task_id]
                
                # Update metrics
                self.total_tasks_processed += 1
                self.failed_tasks_count += 1
                
                # Record operation
                self.record_operation("handle_task_failure", True, 0.0)
                
                self.logger.error(f"Task {task.task_id} failed permanently after {task.max_retries} retries")
            
        except Exception as e:
            self.logger.error(f"Failed to handle task failure for {task.task_id}: {e}")
            self.record_operation("handle_task_failure", False, 0.0)
    
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
            status = {
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
            
            # Record operation
            self.record_operation("get_task_status", True, 0.0)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to get task status: {e}")
            self.record_operation("get_task_status", False, 0.0)
            return None
    
    def get_task_manager_stats(self) -> Dict[str, Any]:
        """Get task manager statistics"""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            
            stats = {
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
            
            # Record operation
            self.record_operation("get_task_manager_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get task manager stats: {e}")
            self.record_operation("get_task_manager_stats", False, 0.0)
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
                    
                    # Record operation
                    self.record_operation("cancel_task", True, 0.0)
                    
                    self.logger.info(f"Cancelled task: {task_id}")
                    return True
                
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to cancel task {task_id}: {e}")
            self.record_operation("cancel_task", False, 0.0)
            return False
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_task_data(self):
        """Save task data (placeholder for future persistence)"""
        try:
            # TODO: Implement persistence to database/file
            self.logger.debug("Task data saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save task data: {e}")
    
    def _check_task_health(self):
        """Check task health status"""
        try:
            # Check for stuck tasks
            current_time = datetime.now()
            
            for task_id, task in self.running_tasks.items():
                if task.started_at:
                    runtime = (current_time - task.started_at).total_seconds()
                    if runtime > task.timeout:
                        self.logger.warning(f"Task {task_id} has exceeded timeout ({runtime}s > {task.timeout}s)")
            
            # Check queue health
            if self.task_queue.qsize() > 100:
                self.logger.warning(f"Task queue is large: {self.task_queue.qsize()} tasks")
                
        except Exception as e:
            self.logger.error(f"Failed to check task health: {e}")
    
    def get_task_manager_performance(self) -> Dict[str, Any]:
        """Get task manager performance metrics"""
        try:
            performance = {
                "total_tasks_processed": self.total_tasks_processed,
                "successful_tasks": self.successful_tasks,
                "failed_tasks_count": self.failed_tasks_count,
                "success_rate": (self.successful_tasks / max(self.total_tasks_processed, 1)) * 100,
                "failure_rate": (self.failed_tasks_count / max(self.total_tasks_processed, 1)) * 100,
                "queue_size": self.task_queue.qsize(),
                "running_tasks_count": len(self.running_tasks),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_task_manager_performance", True, 0.0)
            
            return performance
            
        except Exception as e:
            self.logger.error(f"Failed to get task manager performance: {e}")
            self.record_operation("get_task_manager_performance", False, 0.0)
            return {"error": str(e)}
