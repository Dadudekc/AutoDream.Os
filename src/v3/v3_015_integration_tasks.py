#!/usr/bin/env python3
"""
V3-015: Integration Tasks
=========================

Integration task management for Phase 3 Dream.OS integration.
V2 compliant with focus on task orchestration.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from v3.v3_015_integration_components import IntegrationStatus


@dataclass
class IntegrationTask:
    """Integration task structure."""
    task_id: str
    name: str
    description: str
    components: List[str]
    priority: int
    status: IntegrationStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class TaskManager:
    """Manages integration tasks."""
    
    def __init__(self):
        self.tasks = {}
        self.task_queue = []
        self.completed_tasks = []
        self.failed_tasks = []
    
    def create_task(self, task_id: str, name: str, description: str, 
                   components: List[str], priority: int = 1) -> IntegrationTask:
        """Create a new integration task."""
        task = IntegrationTask(
            task_id=task_id,
            name=name,
            description=description,
            components=components,
            priority=priority,
            status=IntegrationStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.tasks[task_id] = task
        self.task_queue.append(task_id)
        self._sort_queue_by_priority()
        
        print(f"📋 Created task: {name} (Priority: {priority})")
        return task
    
    def _sort_queue_by_priority(self):
        """Sort task queue by priority (higher priority first)."""
        self.task_queue.sort(key=lambda tid: self.tasks[tid].priority, reverse=True)
    
    def get_next_task(self) -> Optional[IntegrationTask]:
        """Get next task from queue."""
        if not self.task_queue:
            return None
        
        task_id = self.task_queue.pop(0)
        return self.tasks[task_id]
    
    def start_task(self, task_id: str) -> bool:
        """Start a task."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status != IntegrationStatus.PENDING:
            return False
        
        task.status = IntegrationStatus.IN_PROGRESS
        task.started_at = datetime.now()
        
        print(f"🚀 Started task: {task.name}")
        return True
    
    def complete_task(self, task_id: str) -> bool:
        """Mark task as completed."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status != IntegrationStatus.IN_PROGRESS:
            return False
        
        task.status = IntegrationStatus.COMPLETED
        task.completed_at = datetime.now()
        
        self.completed_tasks.append(task_id)
        print(f"✅ Completed task: {task.name}")
        return True
    
    def fail_task(self, task_id: str, error_message: str) -> bool:
        """Mark task as failed."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = IntegrationStatus.FAILED
        task.error_message = error_message
        
        self.failed_tasks.append(task_id)
        print(f"❌ Failed task: {task.name} - {error_message}")
        return True
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status information."""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return {
            "task_id": task.task_id,
            "name": task.name,
            "status": task.status.value,
            "priority": task.priority,
            "components": task.components,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "error_message": task.error_message,
            "duration_seconds": (
                (task.completed_at or datetime.now()) - (task.started_at or task.created_at)
            ).total_seconds() if task.started_at else None
        }
    
    def get_task_summary(self) -> Dict[str, Any]:
        """Get summary of all tasks."""
        status_counts = {}
        for task in self.tasks.values():
            status = task.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_tasks": len(self.tasks),
            "pending_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "status_counts": status_counts,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_high_priority_tasks(self) -> List[IntegrationTask]:
        """Get high priority tasks (priority >= 3)."""
        return [
            task for task in self.tasks.values()
            if task.priority >= 3 and task.status == IntegrationStatus.PENDING
        ]
    
    def retry_failed_task(self, task_id: str) -> bool:
        """Retry a failed task."""
        if task_id not in self.failed_tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = IntegrationStatus.PENDING
        task.error_message = None
        task.started_at = None
        task.completed_at = None
        
        self.failed_tasks.remove(task_id)
        self.task_queue.append(task_id)
        self._sort_queue_by_priority()
        
        print(f"🔄 Retrying task: {task.name}")
        return True


class TaskExecutor:
    """Executes integration tasks."""
    
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.execution_log = []
    
    def execute_next_task(self) -> Dict[str, Any]:
        """Execute the next task in queue."""
        task = self.task_manager.get_next_task()
        if not task:
            return {"error": "No tasks available"}
        
        # Start task
        if not self.task_manager.start_task(task.task_id):
            return {"error": f"Could not start task {task.task_id}"}
        
        # Simulate task execution
        execution_result = self._simulate_task_execution(task)
        
        # Log execution
        self.execution_log.append({
            "task_id": task.task_id,
            "executed_at": datetime.now().isoformat(),
            "result": execution_result
        })
        
        # Complete or fail task based on result
        if execution_result.get("success", False):
            self.task_manager.complete_task(task.task_id)
        else:
            self.task_manager.fail_task(task.task_id, execution_result.get("error", "Unknown error"))
        
        return {
            "task_id": task.task_id,
            "task_name": task.name,
            "execution_result": execution_result
        }
    
    def _simulate_task_execution(self, task: IntegrationTask) -> Dict[str, Any]:
        """Simulate task execution (replace with real logic)."""
        # Simulate different success rates based on priority
        success_rate = 0.9 if task.priority >= 3 else 0.7
        
        import random
        if random.random() < success_rate:
            return {
                "success": True,
                "message": f"Successfully executed {task.name}",
                "components_processed": len(task.components)
            }
        else:
            return {
                "success": False,
                "error": f"Simulated failure in {task.name}",
                "components_processed": 0
            }
    
    def get_execution_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get execution log."""
        return self.execution_log[-limit:]
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics."""
        if not self.execution_log:
            return {"error": "No execution history"}
        
        total_executions = len(self.execution_log)
        successful_executions = sum(1 for log in self.execution_log if log["result"].get("success", False))
        success_rate = successful_executions / total_executions if total_executions > 0 else 0
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": total_executions - successful_executions,
            "success_rate": success_rate,
            "last_execution": self.execution_log[-1]["executed_at"] if self.execution_log else None
        }


def main():
    """Main execution function."""
    print("📋 V3-015 Integration Tasks - Testing...")
    
    # Initialize task manager and executor
    task_manager = TaskManager()
    executor = TaskExecutor(task_manager)
    
    # Create sample tasks
    task1 = task_manager.create_task(
        "task_001", "Database Setup", "Initialize database components", 
        ["db_main", "db_backup"], priority=3
    )
    
    task2 = task_manager.create_task(
        "task_002", "API Integration", "Integrate API components", 
        ["api_gateway", "api_auth"], priority=2
    )
    
    task3 = task_manager.create_task(
        "task_003", "Performance Monitoring", "Setup performance monitoring", 
        ["perf_monitor", "perf_dashboard"], priority=1
    )
    
    # Execute tasks
    print("\n🚀 Executing tasks...")
    for i in range(3):
        result = executor.execute_next_task()
        print(f"   Task {i+1}: {result.get('task_name', 'Unknown')} - {'✅' if result.get('execution_result', {}).get('success') else '❌'}")
    
    # Get summaries
    task_summary = task_manager.get_task_summary()
    execution_stats = executor.get_execution_stats()
    
    print(f"\n📊 Task Summary:")
    print(f"   Total Tasks: {task_summary['total_tasks']}")
    print(f"   Completed: {task_summary['completed_tasks']}")
    print(f"   Failed: {task_summary['failed_tasks']}")
    print(f"   Status Counts: {task_summary['status_counts']}")
    
    print(f"\n📈 Execution Stats:")
    print(f"   Total Executions: {execution_stats['total_executions']}")
    print(f"   Success Rate: {execution_stats['success_rate']:.2%}")
    
    print("\n✅ V3-015 Integration Tasks completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())

