"""
SSOT Executor - V2 Compliance Refactored
========================================

Execution engine for SSOT operations.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

from .models import (
    SSOTComponent, SSOTExecutionTask, SSOTIntegrationResult,
    SSOTExecutionPhase, SSOTComponentType
)

# Import modular components
from .execution.task_executor import TaskExecutor
from .execution.execution_manager import ExecutionManager


class SSOTExecutor:
    """SSOT execution engine - V2 compliant."""
    
    def __init__(self):
        """Initialize SSOT executor."""
        self.task_executor = TaskExecutor()
        self.execution_manager = ExecutionManager()
    
    async def execute_task(self, task: SSOTExecutionTask) -> SSOTIntegrationResult:
        """Execute SSOT task."""
        result = await self.task_executor.execute_task(task)
        self.execution_manager.add_execution_result(result)
        return result
    
    async def execute_batch(self, tasks: List[SSOTExecutionTask]) -> List[SSOTIntegrationResult]:
        """Execute multiple tasks in parallel."""
        results = await asyncio.gather(*[self.execute_task(task) for task in tasks])
        return results
    
    def get_execution_history(self, limit: int = 100) -> List[SSOTIntegrationResult]:
        """Get execution history."""
        return self.execution_manager.get_execution_history(limit)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        return self.execution_manager.get_performance_metrics()
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        return self.execution_manager.get_execution_summary()
    
    def get_active_tasks(self) -> List[SSOTExecutionTask]:
        """Get currently active tasks."""
        return list(self.task_executor.active_tasks.values())
    
    def get_completed_tasks(self) -> List[SSOTExecutionTask]:
        """Get completed tasks."""
        return self.task_executor.completed_tasks
    
    def get_failed_tasks(self) -> List[SSOTExecutionTask]:
        """Get failed tasks."""
        return self.task_executor.failed_tasks
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status by ID."""
        # Check active tasks
        if task_id in self.task_executor.active_tasks:
            task = self.task_executor.active_tasks[task_id]
            return {
                "task_id": task.task_id,
                "status": task.status,
                "phase": task.phase.value if hasattr(task.phase, 'value') else str(task.phase),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "is_active": True
            }
        
        # Check completed tasks
        for task in self.task_executor.completed_tasks:
            if task.task_id == task_id:
                return {
                    "task_id": task.task_id,
                    "status": task.status,
                    "phase": task.phase.value if hasattr(task.phase, 'value') else str(task.phase),
                    "started_at": task.started_at.isoformat() if task.started_at else None,
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                    "is_active": False
                }
        
        # Check failed tasks
        for task in self.task_executor.failed_tasks:
            if task.task_id == task_id:
                return {
                    "task_id": task.task_id,
                    "status": task.status,
                    "phase": task.phase.value if hasattr(task.phase, 'value') else str(task.phase),
                    "started_at": task.started_at.isoformat() if task.started_at else None,
                    "error_message": task.error_message,
                    "is_active": False
                }
        
        return None
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task."""
        if task_id in self.task_executor.active_tasks:
            task = self.task_executor.active_tasks[task_id]
            task.status = "cancelled"
            task.completed_at = datetime.now()
            self.task_executor.failed_tasks.append(task)
            del self.task_executor.active_tasks[task_id]
            return True
        return False
    
    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_manager.clear_history()
        self.task_executor.completed_tasks.clear()
        self.task_executor.failed_tasks.clear()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        return {
            "active_tasks": len(self.task_executor.active_tasks),
            "completed_tasks": len(self.task_executor.completed_tasks),
            "failed_tasks": len(self.task_executor.failed_tasks),
            "total_executions": len(self.execution_manager.execution_history),
            "performance_metrics": self.get_performance_metrics()
        }