#!/usr/bin/env python3
"""
Task Coordination Engine - V2 Compliance Module
==============================================

Handles task coordination and execution for swarm operations.
Extracted from swarm_coordination_orchestrator.py for V2 compliance.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import asyncio
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque
import logging

from ..coordination_models import (
    CoordinationTask, CoordinationResult, CoordinationPriority,
    create_coordination_result, create_coordination_task
)


class TaskCoordinationEngine:
    """Engine for task coordination and execution."""

    def __init__(self, config):
        """Initialize task coordination engine."""
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.active_tasks: Dict[str, CoordinationTask] = {}
        self.completed_tasks: deque = deque(maxlen=1000)
        self.task_results: Dict[str, CoordinationResult] = {}
        
        # Priority queues
        self.priority_queues: Dict[CoordinationPriority, deque] = {
            priority: deque() for priority in CoordinationPriority
        }

    async def coordinate_task(self, task: CoordinationTask) -> CoordinationResult:
        """Coordinate execution of a task."""
        try:
            start_time = time.time()
            
            # Add to active tasks
            self.active_tasks[task.task_id] = task
            
            # Execute task based on strategy
            result = await self._execute_task_strategy(task)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Update result with timing
            result.execution_time_seconds = execution_time
            result.completed_at = datetime.now()
            
            # Move to completed tasks
            self.active_tasks.pop(task.task_id, None)
            self.completed_tasks.append(task)
            self.task_results[task.task_id] = result
            
            self.logger.info(f"Task {task.task_id} coordinated successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to coordinate task {task.task_id}: {e}")
            return self._create_error_result(task, str(e))

    async def _execute_task_strategy(self, task: CoordinationTask) -> CoordinationResult:
        """Execute task using specified strategy."""
        try:
            if task.strategy == "parallel":
                return await self._execute_parallel_strategy(task)
            elif task.strategy == "sequential":
                return await self._execute_sequential_strategy(task)
            elif task.strategy == "priority_based":
                return await self._execute_priority_based_strategy(task)
            else:
                return await self._execute_default_strategy(task)
                
        except Exception as e:
            return self._create_error_result(task, str(e))

    async def _execute_parallel_strategy(self, task: CoordinationTask) -> CoordinationResult:
        """Execute task using parallel strategy."""
        try:
            # Simulate parallel execution
            await asyncio.sleep(0.1)  # Simulate processing time
            
            return create_coordination_result(
                task_id=task.task_id,
                success=True,
                result_data={"strategy": "parallel", "execution_mode": "concurrent"}
            )
            
        except Exception as e:
            return self._create_error_result(task, str(e))

    async def _execute_sequential_strategy(self, task: CoordinationTask) -> CoordinationResult:
        """Execute task using sequential strategy."""
        try:
            # Simulate sequential execution
            await asyncio.sleep(0.2)  # Simulate processing time
            
            return create_coordination_result(
                task_id=task.task_id,
                success=True,
                result_data={"strategy": "sequential", "execution_mode": "ordered"}
            )
            
        except Exception as e:
            return self._create_error_result(task, str(e))

    async def _execute_priority_based_strategy(self, task: CoordinationTask) -> CoordinationResult:
        """Execute task using priority-based strategy."""
        try:
            # Add to priority queue
            self.priority_queues[task.priority].append(task)
            
            # Simulate priority-based execution
            await asyncio.sleep(0.15)  # Simulate processing time
            
            return create_coordination_result(
                task_id=task.task_id,
                success=True,
                result_data={"strategy": "priority_based", "priority": task.priority.value}
            )
            
        except Exception as e:
            return self._create_error_result(task, str(e))

    async def _execute_default_strategy(self, task: CoordinationTask) -> CoordinationResult:
        """Execute task using default strategy."""
        try:
            # Simulate default execution
            await asyncio.sleep(0.1)  # Simulate processing time
            
            return create_coordination_result(
                task_id=task.task_id,
                success=True,
                result_data={"strategy": "default", "execution_mode": "standard"}
            )
            
        except Exception as e:
            return self._create_error_result(task, str(e))

    def _create_error_result(self, task: CoordinationTask, error_message: str) -> CoordinationResult:
        """Create error result for failed task."""
        return create_coordination_result(
            task_id=task.task_id,
            success=False,
            error_message=error_message,
            result_data={"error": error_message}
        )

    def get_task_summary(self) -> Dict[str, Any]:
        """Get task coordination summary."""
        return {
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "task_results": len(self.task_results),
            "priority_queues": {
                priority.value: len(queue) for priority, queue in self.priority_queues.items()
            }
        }

    def get_next_task(self, priority: CoordinationPriority = None) -> Optional[CoordinationTask]:
        """Get next task from priority queue."""
        if priority:
            queue = self.priority_queues.get(priority)
            if queue:
                return queue.popleft()
        else:
            # Get from highest priority queue
            for p in CoordinationPriority:
                queue = self.priority_queues.get(p)
                if queue:
                    return queue.popleft()
        
        return None

    def clear_completed_tasks(self) -> None:
        """Clear completed tasks history."""
        self.completed_tasks.clear()
        self.task_results.clear()
        self.logger.info("Completed tasks cleared")
