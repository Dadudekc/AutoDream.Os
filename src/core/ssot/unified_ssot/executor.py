"""
SSOT Executor
=============

Execution engine for SSOT operations.
V2 Compliance: < 300 lines, single responsibility, execution logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import (
    SSOTComponent, SSOTExecutionTask, SSOTIntegrationResult,
    SSOTExecutionPhase, SSOTComponentType
)


class SSOTExecutor:
    """SSOT execution engine."""
    
    def __init__(self):
        """Initialize SSOT executor."""
        self.active_tasks: Dict[str, SSOTExecutionTask] = {}
        self.completed_tasks: List[SSOTExecutionTask] = []
        self.failed_tasks: List[SSOTExecutionTask] = []
        self.execution_history: List[SSOTIntegrationResult] = []
    
    async def execute_task(self, task: SSOTExecutionTask) -> SSOTIntegrationResult:
        """Execute SSOT task."""
        try:
            # Mark task as started
            task.started_at = datetime.now()
            task.status = "running"
            self.active_tasks[task.task_id] = task
            
            # Execute based on phase
            result = await self._execute_phase(task)
            
            # Mark task as completed
            task.completed_at = datetime.now()
            task.status = "completed"
            self.completed_tasks.append(task)
            
            # Create integration result
            integration_result = SSOTIntegrationResult(
                integration_id=f"exec_{task.task_id}",
                component_id=task.component_id,
                success=True,
                result_data=result,
                execution_time=(task.completed_at - task.started_at).total_seconds(),
                timestamp=datetime.now()
            )
            
            self.execution_history.append(integration_result)
            return integration_result
            
        except Exception as e:
            # Mark task as failed
            task.status = "failed"
            task.retry_count += 1
            self.failed_tasks.append(task)
            
            # Create integration result
            integration_result = SSOTIntegrationResult(
                integration_id=f"exec_{task.task_id}",
                component_id=task.component_id,
                success=False,
                result_data={},
                error_message=str(e),
                execution_time=0.0,
                timestamp=datetime.now()
            )
            
            self.execution_history.append(integration_result)
            return integration_result
        
        finally:
            # Remove from active tasks
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
    
    async def _execute_phase(self, task: SSOTExecutionTask) -> Dict[str, Any]:
        """Execute specific phase."""
        if task.phase == SSOTExecutionPhase.INITIALIZATION:
            return await self._execute_initialization(task)
        elif task.phase == SSOTExecutionPhase.VALIDATION:
            return await self._execute_validation(task)
        elif task.phase == SSOTExecutionPhase.EXECUTION:
            return await self._execute_execution(task)
        elif task.phase == SSOTExecutionPhase.VERIFICATION:
            return await self._execute_verification(task)
        elif task.phase == SSOTExecutionPhase.COMPLETION:
            return await self._execute_completion(task)
        else:
            raise ValueError(f"Unknown execution phase: {task.phase}")
    
    async def _execute_initialization(self, task: SSOTExecutionTask) -> Dict[str, Any]:
        """Execute initialization phase."""
        await asyncio.sleep(0.1)  # Simulate work
        return {
            "phase": "initialization",
            "status": "completed",
            "initialized_components": task.data.get("components", []),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _execute_validation(self, task: SSOTExecutionTask) -> Dict[str, Any]:
        """Execute validation phase."""
        await asyncio.sleep(0.1)  # Simulate work
        return {
            "phase": "validation",
            "status": "completed",
            "validated_items": task.data.get("items", []),
            "validation_score": 0.95,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _execute_execution(self, task: SSOTExecutionTask) -> Dict[str, Any]:
        """Execute main execution phase."""
        await asyncio.sleep(0.2)  # Simulate work
        return {
            "phase": "execution",
            "status": "completed",
            "processed_items": task.data.get("items", []),
            "execution_time": 0.2,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _execute_verification(self, task: SSOTExecutionTask) -> Dict[str, Any]:
        """Execute verification phase."""
        await asyncio.sleep(0.1)  # Simulate work
        return {
            "phase": "verification",
            "status": "completed",
            "verified_items": task.data.get("items", []),
            "verification_score": 0.98,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _execute_completion(self, task: SSOTExecutionTask) -> Dict[str, Any]:
        """Execute completion phase."""
        await asyncio.sleep(0.05)  # Simulate work
        return {
            "phase": "completion",
            "status": "completed",
            "finalized_items": task.data.get("items", []),
            "completion_time": datetime.now().isoformat()
        }
    
    async def execute_batch(self, tasks: List[SSOTExecutionTask]) -> List[SSOTIntegrationResult]:
        """Execute batch of tasks."""
        results = []
        for task in tasks:
            result = await self.execute_task(task)
            results.append(result)
        return results
    
    async def retry_failed_task(self, task_id: str) -> Optional[SSOTIntegrationResult]:
        """Retry failed task."""
        # Find failed task
        failed_task = None
        for task in self.failed_tasks:
            if task.task_id == task_id:
                failed_task = task
                break
        
        if not failed_task:
            return None
        
        # Check if retries are available
        if failed_task.retry_count >= failed_task.max_retries:
            return None
        
        # Remove from failed tasks
        self.failed_tasks.remove(failed_task)
        
        # Reset status and retry
        failed_task.status = "pending"
        failed_task.started_at = None
        failed_task.completed_at = None
        
        return await self.execute_task(failed_task)
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status."""
        # Check active tasks
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            return {
                "task_id": task.task_id,
                "status": task.status,
                "phase": task.phase.value,
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "retry_count": task.retry_count
            }
        
        # Check completed tasks
        for task in self.completed_tasks:
            if task.task_id == task_id:
                return {
                    "task_id": task.task_id,
                    "status": task.status,
                    "phase": task.phase.value,
                    "started_at": task.started_at.isoformat() if task.started_at else None,
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                    "retry_count": task.retry_count
                }
        
        # Check failed tasks
        for task in self.failed_tasks:
            if task.task_id == task_id:
                return {
                    "task_id": task.task_id,
                    "status": task.status,
                    "phase": task.phase.value,
                    "started_at": task.started_at.isoformat() if task.started_at else None,
                    "retry_count": task.retry_count,
                    "can_retry": task.retry_count < task.max_retries
                }
        
        return None
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        total_tasks = len(self.completed_tasks) + len(self.failed_tasks) + len(self.active_tasks)
        completed_count = len(self.completed_tasks)
        failed_count = len(self.failed_tasks)
        active_count = len(self.active_tasks)
        
        success_rate = (completed_count / total_tasks) if total_tasks > 0 else 0.0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_count,
            "failed_tasks": failed_count,
            "active_tasks": active_count,
            "success_rate": success_rate,
            "execution_history_count": len(self.execution_history)
        }
    
    def clear_history(self):
        """Clear execution history."""
        self.completed_tasks.clear()
        self.failed_tasks.clear()
        self.execution_history.clear()
    
    def get_failed_tasks(self) -> List[SSOTExecutionTask]:
        """Get list of failed tasks."""
        return self.failed_tasks.copy()
    
    def get_completed_tasks(self) -> List[SSOTExecutionTask]:
        """Get list of completed tasks."""
        return self.completed_tasks.copy()
    
    def get_active_tasks(self) -> List[SSOTExecutionTask]:
        """Get list of active tasks."""
        return list(self.active_tasks.values())
