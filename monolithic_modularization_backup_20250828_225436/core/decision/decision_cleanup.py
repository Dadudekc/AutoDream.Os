#!/usr/bin/env python3
"""
Decision Cleanup Manager - Agent Cellphone V2

Manages decision cleanup, maintenance, and resource optimization.
Handles cleanup scheduling, execution, and resource management.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3A - Large File Modularization
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .decision_types import DecisionStatus


@dataclass
class CleanupTask:
    """Individual cleanup task"""
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
    """Cleanup schedule configuration"""
    schedule_id: str
    name: str
    description: str
    interval_minutes: int
    last_execution: Optional[str] = None
    next_execution: Optional[str] = None
    is_active: bool = True
    tasks: List[str] = field(default_factory=list)


class DecisionCleanupManager:
    """
    Decision Cleanup Manager - TASK 3A
    
    Manages decision cleanup, maintenance, and resource optimization.
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.DecisionCleanupManager")
        
        # Cleanup tasks and schedules
        self.cleanup_tasks: Dict[str, CleanupTask] = {}
        self.cleanup_schedules: Dict[str, CleanupSchedule] = {}
        self.cleanup_history: List[CleanupTask] = []
        
        # Configuration
        self.default_cleanup_interval = 15  # minutes
        self.max_history_size = 1000
        self.max_cleanup_age_hours = 24
        
        # Cleanup scheduler
        self.cleanup_scheduler: Optional[threading.Thread] = None
        self.scheduler_running = False
        self.scheduler_stop_event = threading.Event()
        
        # Status
        self.initialized = False
        
        self.logger.info("DecisionCleanupManager initialized")

    def initialize(self):
        """Initialize the cleanup manager"""
        try:
            if self.initialized:
                self.logger.info("Cleanup manager already initialized")
                return
            
            # Initialize default cleanup schedules
            self._initialize_default_schedules()
            
            # Initialize default cleanup tasks
            self._initialize_default_tasks()
            
            self.initialized = True
            self.logger.info("Cleanup manager initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize cleanup manager: {e}")

    def shutdown(self):
        """Shutdown the cleanup manager"""
        try:
            self.initialized = False
            
            # Stop scheduler
            self.stop_cleanup_scheduler()
            
            # Clear all data
            self.cleanup_tasks.clear()
            self.cleanup_schedules.clear()
            self.cleanup_history.clear()
            
            self.logger.info("Cleanup manager shutdown successfully")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup manager shutdown: {e}")

    def is_initialized(self) -> bool:
        """Check if the manager is initialized"""
        return self.initialized

    def _initialize_default_schedules(self):
        """Initialize default cleanup schedules"""
        try:
            # Regular cleanup schedule
            regular_schedule = CleanupSchedule(
                schedule_id="regular_cleanup",
                name="Regular Cleanup Schedule",
                description="Regular cleanup of completed decisions and old data",
                interval_minutes=self.default_cleanup_interval,
                tasks=["cleanup_completed_decisions", "cleanup_old_history", "cleanup_expired_data"]
            )
            self.cleanup_schedules["regular_cleanup"] = regular_schedule
            
            # Performance cleanup schedule
            performance_schedule = CleanupSchedule(
                schedule_id="performance_cleanup",
                name="Performance Cleanup Schedule",
                description="Cleanup for performance optimization",
                interval_minutes=30,
                tasks=["cleanup_performance_data", "cleanup_old_metrics", "optimize_resources"]
            )
            self.cleanup_schedules["performance_cleanup"] = performance_schedule
            
            # Maintenance cleanup schedule
            maintenance_schedule = CleanupSchedule(
                schedule_id="maintenance_cleanup",
                name="Maintenance Cleanup Schedule",
                description="Maintenance cleanup tasks",
                interval_minutes=60,
                tasks=["cleanup_logs", "cleanup_temp_data", "system_maintenance"]
            )
            self.cleanup_schedules["maintenance_cleanup"] = maintenance_schedule
            
            self.logger.info(f"Initialized {len(self.cleanup_schedules)} default cleanup schedules")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default cleanup schedules: {e}")

    def _initialize_default_tasks(self):
        """Initialize default cleanup tasks"""
        try:
            # Cleanup completed decisions
            cleanup_completed = CleanupTask(
                task_id="cleanup_completed_decisions",
                task_type="decision_cleanup",
                description="Clean up completed decisions from active tracking",
                priority=1,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["cleanup_completed_decisions"] = cleanup_completed
            
            # Cleanup old history
            cleanup_history = CleanupTask(
                task_id="cleanup_old_history",
                task_type="history_cleanup",
                description="Clean up old decision history data",
                priority=2,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["cleanup_old_history"] = cleanup_history
            
            # Cleanup expired data
            cleanup_expired = CleanupTask(
                task_id="cleanup_expired_data",
                task_type="data_cleanup",
                description="Clean up expired decision data",
                priority=3,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["cleanup_expired_data"] = cleanup_expired
            
            # Cleanup performance data
            cleanup_performance = CleanupTask(
                task_id="cleanup_performance_data",
                task_type="performance_cleanup",
                description="Clean up old performance data",
                priority=2,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["cleanup_performance_data"] = cleanup_performance
            
            # Cleanup old metrics
            cleanup_metrics = CleanupTask(
                task_id="cleanup_old_metrics",
                task_type="metrics_cleanup",
                description="Clean up old metrics data",
                priority=2,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["cleanup_old_metrics"] = cleanup_metrics
            
            # Optimize resources
            optimize_resources = CleanupTask(
                task_id="optimize_resources",
                task_type="resource_optimization",
                description="Optimize resource usage and allocation",
                priority=1,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["optimize_resources"] = optimize_resources
            
            # Cleanup logs
            cleanup_logs = CleanupTask(
                task_id="cleanup_logs",
                task_type="log_cleanup",
                description="Clean up old log files and data",
                priority=3,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["cleanup_logs"] = cleanup_logs
            
            # Cleanup temp data
            cleanup_temp = CleanupTask(
                task_id="cleanup_temp_data",
                task_type="temp_cleanup",
                description="Clean up temporary data and files",
                priority=3,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["cleanup_temp_data"] = cleanup_temp
            
            # System maintenance
            system_maintenance = CleanupTask(
                task_id="system_maintenance",
                task_type="maintenance",
                description="Perform system maintenance tasks",
                priority=2,
                scheduled_time=datetime.now().isoformat()
            )
            self.cleanup_tasks["system_maintenance"] = system_maintenance
            
            self.logger.info(f"Initialized {len(self.cleanup_tasks)} default cleanup tasks")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize default cleanup tasks: {e}")

    def schedule_cleanup(self):
        """Schedule the cleanup scheduler"""
        try:
            if not self.initialized:
                self.logger.warning("Cleanup manager not initialized, skipping scheduler")
                return
            
            if self.scheduler_running:
                self.logger.info("Cleanup scheduler already running")
                return
            
            # Start cleanup scheduler
            self.scheduler_stop_event.clear()
            self.scheduler_running = True
            
            self.cleanup_scheduler = threading.Thread(
                target=self._cleanup_scheduler_loop,
                daemon=True,
                name="DecisionCleanupScheduler"
            )
            self.cleanup_scheduler.start()
            
            self.logger.info("Cleanup scheduler started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to schedule cleanup: {e}")

    def stop_cleanup_scheduler(self):
        """Stop the cleanup scheduler"""
        try:
            if not self.scheduler_running:
                self.logger.info("Cleanup scheduler not running")
                return
            
            # Signal scheduler to stop
            self.scheduler_stop_event.set()
            self.scheduler_running = False
            
            # Wait for scheduler to stop
            if self.cleanup_scheduler and self.cleanup_scheduler.is_alive():
                self.cleanup_scheduler.join(timeout=5.0)
            
            self.logger.info("Cleanup scheduler stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop cleanup scheduler: {e}")

    def _cleanup_scheduler_loop(self):
        """Main cleanup scheduler loop"""
        try:
            self.logger.info("Cleanup scheduler loop started")
            
            while not self.scheduler_stop_event.is_set():
                try:
                    # Check for scheduled cleanups
                    self._check_scheduled_cleanups()
                    
                    # Sleep for a short interval
                    time.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    self.logger.error(f"Error in cleanup scheduler loop: {e}")
                    time.sleep(60)  # Wait longer on error
            
            self.logger.info("Cleanup scheduler loop stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to start cleanup scheduler loop: {e}")

    def _check_scheduled_cleanups(self):
        """Check for scheduled cleanups that need to be executed"""
        try:
            current_time = datetime.now()
            
            for schedule_id, schedule in self.cleanup_schedules.items():
                if not schedule.is_active:
                    continue
                
                # Check if it's time to execute
                if self._should_execute_schedule(schedule, current_time):
                    self._execute_scheduled_cleanup(schedule)
                    
        except Exception as e:
            self.logger.error(f"Failed to check scheduled cleanups: {e}")

    def _should_execute_schedule(self, schedule: CleanupSchedule, current_time: datetime) -> bool:
        """Check if a schedule should be executed"""
        try:
            if not schedule.last_execution:
                return True
            
            last_execution = datetime.fromisoformat(schedule.last_execution)
            time_since_last = current_time - last_execution
            
            return time_since_last.total_seconds() >= (schedule.interval_minutes * 60)
            
        except Exception as e:
            self.logger.error(f"Failed to check schedule execution: {e}")
            return False

    def _execute_scheduled_cleanup(self, schedule: CleanupSchedule):
        """Execute a scheduled cleanup"""
        try:
            self.logger.info(f"Executing scheduled cleanup: {schedule.name}")
            
            # Execute all tasks in the schedule
            for task_id in schedule.tasks:
                if task_id in self.cleanup_tasks:
                    self._execute_cleanup_task(task_id)
            
            # Update schedule execution time
            schedule.last_execution = datetime.now().isoformat()
            schedule.next_execution = (
                datetime.now() + timedelta(minutes=schedule.interval_minutes)
            ).isoformat()
            
            self.logger.info(f"Scheduled cleanup completed: {schedule.name}")
            
        except Exception as e:
            self.logger.error(f"Failed to execute scheduled cleanup {schedule.name}: {e}")

    def _execute_cleanup_task(self, task_id: str):
        """Execute a specific cleanup task"""
        try:
            if task_id not in self.cleanup_tasks:
                self.logger.warning(f"Cleanup task {task_id} not found")
                return
            
            task = self.cleanup_tasks[task_id]
            if task.status != "pending":
                self.logger.debug(f"Cleanup task {task_id} not pending, skipping")
                return
            
            # Mark task as executing
            task.status = "executing"
            task.execution_time = datetime.now().isoformat()
            
            # Execute the task
            start_time = time.time()
            try:
                result = self._execute_task_logic(task)
                execution_time = time.time() - start_time
                
                # Mark task as completed
                task.status = "completed"
                task.result = {
                    "success": True,
                    "execution_time": execution_time,
                    "result": result
                }
                
                self.logger.info(f"Cleanup task {task_id} completed successfully in {execution_time:.2f}s")
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Mark task as failed
                task.status = "failed"
                task.error_message = str(e)
                task.result = {
                    "success": False,
                    "execution_time": execution_time,
                    "error": str(e)
                }
                
                self.logger.error(f"Cleanup task {task_id} failed: {e}")
            
            # Move to history
            self.cleanup_history.append(task)
            
            # Keep history size manageable
            if len(self.cleanup_history) > self.max_history_size:
                self.cleanup_history = self.cleanup_history[-self.max_history_size:]
            
        except Exception as e:
            self.logger.error(f"Failed to execute cleanup task {task_id}: {e}")

    def _execute_task_logic(self, task: CleanupTask) -> Dict[str, Any]:
        """Execute the actual cleanup task logic"""
        try:
            task_type = task.task_type
            
            if task_type == "decision_cleanup":
                return self._cleanup_completed_decisions()
            elif task_type == "history_cleanup":
                return self._cleanup_old_history()
            elif task_type == "data_cleanup":
                return self._cleanup_expired_data()
            elif task_type == "performance_cleanup":
                return self._cleanup_performance_data()
            elif task_type == "metrics_cleanup":
                return self._cleanup_old_metrics()
            elif task_type == "resource_optimization":
                return self._optimize_resources()
            elif task_type == "log_cleanup":
                return self._cleanup_logs()
            elif task_type == "temp_cleanup":
                return self._cleanup_temp_data()
            elif task_type == "maintenance":
                return self._system_maintenance()
            else:
                return {"message": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            self.logger.error(f"Failed to execute task logic: {e}")
            return {"error": str(e)}

    def _cleanup_completed_decisions(self) -> Dict[str, Any]:
        """Clean up completed decisions"""
        try:
            # Simulate cleanup of completed decisions
            cleaned_count = 50  # Simulated count
            
            return {
                "task": "cleanup_completed_decisions",
                "cleaned_count": cleaned_count,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _cleanup_old_history(self) -> Dict[str, Any]:
        """Clean up old decision history"""
        try:
            # Simulate cleanup of old history
            cleaned_count = 100  # Simulated count
            
            return {
                "task": "cleanup_old_history",
                "cleaned_count": cleaned_count,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _cleanup_expired_data(self) -> Dict[str, Any]:
        """Clean up expired decision data"""
        try:
            # Simulate cleanup of expired data
            cleaned_count = 25  # Simulated count
            
            return {
                "task": "cleanup_expired_data",
                "cleaned_count": cleaned_count,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _cleanup_performance_data(self) -> Dict[str, Any]:
        """Clean up old performance data"""
        try:
            # Simulate cleanup of performance data
            cleaned_count = 75  # Simulated count
            
            return {
                "task": "cleanup_performance_data",
                "cleaned_count": cleaned_count,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _cleanup_old_metrics(self) -> Dict[str, Any]:
        """Clean up old metrics data"""
        try:
            # Simulate cleanup of old metrics
            cleaned_count = 30  # Simulated count
            
            return {
                "task": "cleanup_old_metrics",
                "cleaned_count": cleaned_count,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _optimize_resources(self) -> Dict[str, Any]:
        """Optimize resource usage"""
        try:
            # Simulate resource optimization
            optimization_score = 0.85
            
            return {
                "task": "optimize_resources",
                "optimization_score": optimization_score,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _cleanup_logs(self) -> Dict[str, Any]:
        """Clean up old log files"""
        try:
            # Simulate log cleanup
            cleaned_count = 20  # Simulated count
            
            return {
                "task": "cleanup_logs",
                "cleaned_count": cleaned_count,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _cleanup_temp_data(self) -> Dict[str, Any]:
        """Clean up temporary data"""
        try:
            # Simulate temp data cleanup
            cleaned_count = 15  # Simulated count
            
            return {
                "task": "cleanup_temp_data",
                "cleaned_count": cleaned_count,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def _system_maintenance(self) -> Dict[str, Any]:
        """Perform system maintenance"""
        try:
            # Simulate system maintenance
            maintenance_score = 0.9
            
            return {
                "task": "system_maintenance",
                "maintenance_score": maintenance_score,
                "status": "completed"
            }
            
        except Exception as e:
            return {"error": str(e)}

    def should_perform_cleanup(self) -> bool:
        """Check if cleanup should be performed"""
        try:
            if not self.initialized:
                return False
            
            # Check if any schedule is due
            current_time = datetime.now()
            
            for schedule in self.cleanup_schedules.values():
                if not schedule.is_active:
                    continue
                
                if self._should_execute_schedule(schedule, current_time):
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to check cleanup timing: {e}")
            return False

    def cleanup_completed_decisions(self):
        """Manually trigger cleanup of completed decisions"""
        try:
            if not self.initialized:
                self.logger.warning("Cleanup manager not initialized, skipping cleanup")
                return
            
            # Execute the cleanup task directly
            self._execute_cleanup_task("cleanup_completed_decisions")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup completed decisions: {e}")

    def get_cleanup_status(self) -> Dict[str, Any]:
        """Get cleanup manager status"""
        try:
            return {
                "initialized": self.initialized,
                "scheduler_running": self.scheduler_running,
                "total_schedules": len(self.cleanup_schedules),
                "active_schedules": len([s for s in self.cleanup_schedules.values() if s.is_active]),
                "total_tasks": len(self.cleanup_tasks),
                "pending_tasks": len([t for t in self.cleanup_tasks.values() if t.status == "pending"]),
                "executing_tasks": len([t for t in self.cleanup_tasks.values() if t.status == "executing"]),
                "completed_tasks": len([t for t in self.cleanup_history if t.status == "completed"]),
                "failed_tasks": len([t for t in self.cleanup_history if t.status == "failed"]),
                "total_history": len(self.cleanup_history)
            }
        except Exception as e:
            self.logger.error(f"Failed to get cleanup status: {e}")
            return {"error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get cleanup manager status (alias for get_cleanup_status)"""
        return self.get_cleanup_status()

