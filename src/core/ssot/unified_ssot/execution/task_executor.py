"""
SSOT Task Executor - V2 Compliance Module
========================================

Task execution functionality for SSOT operations.

V2 Compliance: < 300 lines, single responsibility, task execution.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..models import (
    SSOTExecutionTask, SSOTIntegrationResult, SSOTExecutionPhase
)


class TaskExecutor:
    """SSOT task execution functionality."""
    
    def __init__(self):
        """Initialize task executor."""
        self.active_tasks: Dict[str, SSOTExecutionTask] = {}
        self.completed_tasks: List[SSOTExecutionTask] = []
        self.failed_tasks: List[SSOTExecutionTask] = []
    
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
                phase=task.phase,
                status="completed",
                result_data=result,
                execution_time=(task.completed_at - task.started_at).total_seconds(),
                created_at=datetime.now()
            )
            
            return integration_result
            
        except Exception as e:
            # Mark task as failed
            task.status = "failed"
            task.error_message = str(e)
            self.failed_tasks.append(task)
            
            # Create failed integration result
            return SSOTIntegrationResult(
                integration_id=f"exec_{task.task_id}",
                component_id=task.component_id,
                phase=task.phase,
                status="failed",
                error_message=str(e),
                created_at=datetime.now()
            )
        finally:
            # Remove from active tasks
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
    
    async def _execute_phase(self, task: SSOTExecutionTask) -> Dict[str, Any]:
        """Execute task based on phase."""
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
            raise ValueError(f"Unknown phase: {task.phase}")
    
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
            "timestamp": datetime.now().isoformat()
        }
