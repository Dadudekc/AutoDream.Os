"""
Task Manager - V2 Compliant Module
=================================

Handles integration task management.
Extracted from coordinator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from ..models import (
    IntegrationType, IntegrationConfig, IntegrationTask,
    IntegrationStatus, IntegrationModels
)


class TaskManager:
    """
    Handles integration task management.
    
    Manages task creation, execution, status tracking,
    and cleanup operations.
    """
    
    def __init__(self, config: IntegrationConfig):
        """Initialize task manager."""
        self.config = config
        self.active_tasks: Dict[str, IntegrationTask] = {}
        self.integration_handlers: Dict[IntegrationType, Callable] = {}
    
    def create_task(
        self,
        integration_type: IntegrationType,
        operation: str,
        data: Any,
        priority: int = 1,
        timeout: int = 30
    ) -> IntegrationTask:
        """Create new integration task."""
        task_id = f"{integration_type.value}_{operation}_{int(time.time())}"
        
        task = IntegrationTask(
            task_id=task_id,
            integration_type=integration_type,
            operation=operation,
            data=data,
            priority=priority,
            timeout=timeout,
            status=IntegrationStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.active_tasks[task_id] = task
        return task
    
    def execute_task(
        self,
        task: IntegrationTask
    ) -> Dict[str, Any]:
        """Execute integration task."""
        start_time = time.time()
        
        try:
            # Get handler for integration type
            handler = self.integration_handlers.get(
                task.integration_type, 
                self._default_handler
            )
            
            # Execute operation
            result = handler(
                task.integration_type,
                task.operation,
                task.data
            )
            
            success = True
            error_message = None
            
        except Exception as e:
            result = None
            success = False
            error_message = str(e)
        
        execution_time = time.time() - start_time
        
        # Update task status
        task.status = IntegrationStatus.ACTIVE if success else IntegrationStatus.ERROR
        
        return {
            'success': success,
            'result': result,
            'execution_time': execution_time,
            'task_id': task.task_id,
            'integration_type': task.integration_type.value,
            'error': error_message
        }
    
    async def execute_task_async(
        self,
        task: IntegrationTask
    ) -> Dict[str, Any]:
        """Execute integration task asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.execute_task,
            task
        )
    
    def register_integration_handler(
        self, 
        integration_type: IntegrationType, 
        handler: Callable
    ) -> None:
        """Register integration handler."""
        self.integration_handlers[integration_type] = handler
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status."""
        task = self.active_tasks.get(task_id)
        if not task:
            return None
        
        return {
            'task_id': task.task_id,
            'integration_type': task.integration_type.value,
            'operation': task.operation,
            'status': task.status.value,
            'priority': task.priority,
            'created_at': task.created_at.isoformat(),
            'timeout': task.timeout
        }
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Get all active tasks."""
        return [
            self.get_task_status(task_id) 
            for task_id in self.active_tasks.keys()
        ]
    
    def cleanup_completed_tasks(self) -> int:
        """Clean up completed tasks."""
        completed_tasks = [
            task_id for task_id, task in self.active_tasks.items()
            if task.status in [IntegrationStatus.COMPLETED, IntegrationStatus.ERROR]
        ]
        
        for task_id in completed_tasks:
            del self.active_tasks[task_id]
        
        return len(completed_tasks)
    
    def _default_handler(
        self, 
        integration_type: IntegrationType, 
        operation: str, 
        data: Any
    ) -> Any:
        """Default handler for integration operations."""
        return {
            'integration_type': integration_type.value,
            'operation': operation,
            'data': data,
            'status': 'processed',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get task manager status."""
        return {
            'active_tasks_count': len(self.active_tasks),
            'registered_handlers': len(self.integration_handlers),
            'task_statuses': {
                status.value: len([
                    task for task in self.active_tasks.values()
                    if task.status == status
                ]) for status in IntegrationStatus
            }
        }
