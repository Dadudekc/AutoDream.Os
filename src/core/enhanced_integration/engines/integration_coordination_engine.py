#!/usr/bin/env python3
"""
Integration Coordination Engine
===============================

Handles coordination of multiple integration tasks.
Extracted from enhanced_integration_orchestrator.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional
from datetime import datetime
from queue import Queue, Empty

from ..integration_models import (
    IntegrationTask, CoordinationStrategy, ResourceAllocationStrategy,
    IntegrationStatus, IntegrationType
)


class IntegrationCoordinationEngine:
    """Handles coordination of multiple integration tasks."""
    
    def __init__(self, max_workers: int = 4):
        """Initialize integration coordination engine."""
        self.logger = logging.getLogger(__name__)
        self.max_workers = max_workers
        self.task_queue: Queue = Queue()
        self.active_tasks: Dict[str, IntegrationTask] = {}
        self.completed_tasks: List[IntegrationTask] = []
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
    async def coordinate_integrations(self, tasks: List[IntegrationTask],
                                    strategy: CoordinationStrategy = CoordinationStrategy.PARALLEL) -> Dict[str, Any]:
        """Coordinate multiple integration tasks."""
        try:
            self.logger.info(f"Coordinating {len(tasks)} integration tasks with strategy: {strategy}")
            
            # Add tasks to queue
            for task in tasks:
                self.task_queue.put(task)
            
            # Execute based on strategy
            if strategy == CoordinationStrategy.PARALLEL:
                results = await self._execute_parallel(tasks)
            elif strategy == CoordinationStrategy.SEQUENTIAL:
                results = await self._execute_sequential(tasks)
            elif strategy == CoordinationStrategy.PRIORITY_BASED:
                results = await self._execute_priority_based(tasks)
            else:
                self.logger.warning(f"Unknown coordination strategy: {strategy}")
                results = await self._execute_parallel(tasks)  # Default fallback
            
            self.logger.info(f"Coordination completed: {results['completed']}/{results['total']} tasks successful")
            return results
            
        except Exception as e:
            self.logger.error(f"Integration coordination failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "completed": 0,
                "total": len(tasks)
            }
    
    async def _execute_parallel(self, tasks: List[IntegrationTask]) -> Dict[str, Any]:
        """Execute tasks in parallel."""
        try:
            # Create coroutines for all tasks
            coroutines = [self._execute_single_task(task) for task in tasks]
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*coroutines, return_exceptions=True)
            
            # Count successful completions
            successful = sum(1 for result in results if result is True)
            
            return {
                "status": "completed",
                "strategy": "parallel",
                "completed": successful,
                "failed": len(tasks) - successful,
                "total": len(tasks),
                "execution_time": max(task.execution_time for task in tasks if task.execution_time) if tasks else 0
            }
            
        except Exception as e:
            self.logger.error(f"Parallel execution failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _execute_sequential(self, tasks: List[IntegrationTask]) -> Dict[str, Any]:
        """Execute tasks sequentially."""
        try:
            successful = 0
            total_time = 0
            
            for task in tasks:
                start_time = datetime.now()
                success = await self._execute_single_task(task)
                end_time = datetime.now()
                
                execution_time = (end_time - start_time).total_seconds()
                total_time += execution_time
                
                if success:
                    successful += 1
                else:
                    # In sequential mode, we might want to stop on failure
                    # For now, continue with other tasks
                    pass
            
            return {
                "status": "completed",
                "strategy": "sequential",
                "completed": successful,
                "failed": len(tasks) - successful,
                "total": len(tasks),
                "execution_time": total_time
            }
            
        except Exception as e:
            self.logger.error(f"Sequential execution failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _execute_priority_based(self, tasks: List[IntegrationTask]) -> Dict[str, Any]:
        """Execute tasks based on priority."""
        try:
            # Sort tasks by priority (assuming higher priority = higher value)
            sorted_tasks = sorted(tasks, key=lambda t: getattr(t, 'priority', 0), reverse=True)
            
            # Execute high priority tasks first, then parallel execution for the rest
            high_priority_tasks = [t for t in sorted_tasks if getattr(t, 'priority', 0) > 5]
            normal_tasks = [t for t in sorted_tasks if getattr(t, 'priority', 0) <= 5]
            
            results = {"status": "completed", "strategy": "priority_based", "completed": 0, "failed": 0, "total": len(tasks)}
            
            # Execute high priority tasks sequentially
            if high_priority_tasks:
                high_priority_result = await self._execute_sequential(high_priority_tasks)
                results["completed"] += high_priority_result.get("completed", 0)
                results["failed"] += high_priority_result.get("failed", 0)
            
            # Execute normal tasks in parallel
            if normal_tasks:
                normal_result = await self._execute_parallel(normal_tasks)
                results["completed"] += normal_result.get("completed", 0)
                results["failed"] += normal_result.get("failed", 0)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Priority-based execution failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def _execute_single_task(self, task: IntegrationTask) -> bool:
        """Execute a single integration task."""
        try:
            self.logger.debug(f"Executing task: {task.task_id}")
            
            # Add to active tasks
            self.active_tasks[task.task_id] = task
            task.status = IntegrationStatus.RUNNING
            task.start_time = datetime.now()
            
            # Simulate task execution based on integration type
            success = await self._simulate_task_execution(task)
            
            # Update task completion
            task.end_time = datetime.now()
            task.execution_time = (task.end_time - task.start_time).total_seconds()
            task.status = IntegrationStatus.COMPLETED if success else IntegrationStatus.FAILED
            
            # Move from active to completed
            self.active_tasks.pop(task.task_id, None)
            self.completed_tasks.append(task)
            
            # Keep only last 100 completed tasks
            if len(self.completed_tasks) > 100:
                self.completed_tasks = self.completed_tasks[-100:]
            
            return success
            
        except Exception as e:
            self.logger.error(f"Task execution failed for {task.task_id}: {e}")
            task.status = IntegrationStatus.FAILED
            task.error_message = str(e)
            self.active_tasks.pop(task.task_id, None)
            self.completed_tasks.append(task)
            return False
    
    async def _simulate_task_execution(self, task: IntegrationTask) -> bool:
        """Simulate task execution based on integration type."""
        try:
            # Different execution times based on integration type
            if task.integration_type == IntegrationType.VECTOR_DATABASE:
                await asyncio.sleep(0.2)  # Vector DB operations
            elif task.integration_type == IntegrationType.MESSAGING:
                await asyncio.sleep(0.1)  # Messaging operations
            elif task.integration_type == IntegrationType.VALIDATION:
                await asyncio.sleep(0.15)  # Validation operations
            else:
                await asyncio.sleep(0.1)  # Default
            
            # Simulate 90% success rate
            import random
            return random.random() > 0.1
            
        except Exception as e:
            self.logger.error(f"Task simulation failed: {e}")
            return False
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get current coordination status."""
        try:
            return {
                "active_tasks": len(self.active_tasks),
                "completed_tasks": len(self.completed_tasks),
                "queued_tasks": self.task_queue.qsize(),
                "max_workers": self.max_workers,
                "active_task_ids": list(self.active_tasks.keys())
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get coordination status: {e}")
            return {"status": "error", "message": str(e)}
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel an active task."""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task.status = IntegrationStatus.CANCELLED
            self.active_tasks.pop(task_id, None)
            self.completed_tasks.append(task)
            self.logger.info(f"Cancelled task: {task_id}")
            return True
        return False
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        try:
            self.executor.shutdown(wait=True)
            self.logger.info("Integration coordination engine cleaned up")
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
