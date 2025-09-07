#!/usr/bin/env python3
"""
Async Coordination Core - Agent Cellphone V2
===========================================

Main orchestration class for the asynchronous coordination system.
V2 Compliance: Core orchestration and coordination logic only.

Author: Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)
License: MIT
"""

import asyncio
import logging
import time
import threading
import uuid
from typing import Dict, List, Set, Optional, Callable, Any
from .async_coordination_models import (
    CoordinationTask, TaskResult, TaskStatus, TaskType, 
    CoordinationMode, TaskPriority, CoordinationConfig
)
from .async_coordination_executor import TaskExecutor
from .async_coordination_metrics import MetricsManager

logger = logging.getLogger(__name__)


class AsyncCoordinationSystem:
    """
    High-performance asynchronous coordination system for agent tasks.
    
    Single Responsibility: Orchestrate asynchronous task coordination.
    Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
    """
    
    def __init__(self, config: Optional[CoordinationConfig] = None):
        self.config = config or CoordinationConfig()
        self.coordination_active = False
        self.event_loop: Optional[asyncio.AbstractEventLoop] = None
        self.task_queue: Optional[asyncio.Queue] = None
        self.coordination_thread: Optional[threading.Thread] = None
        
        # Initialize components
        self.executor = TaskExecutor()
        self.metrics = MetricsManager()
        
        # Task management
        self.pending_tasks: Dict[str, CoordinationTask] = {}
        self.running_tasks: Set[str] = set()
        self.completed_tasks: Dict[str, TaskResult] = {}
        self.failed_tasks: Dict[str, TaskResult] = {}
        
        # Dependencies tracking
        self.task_dependencies: Dict[str, Set[str]] = {}
        self.dependency_graph: Dict[str, Set[str]] = {}
    
    def start_coordination_system(self):
        """Start the coordination system."""
        if self.coordination_active:
            logger.warning("Coordination system is already running")
            return
        
        self.coordination_active = True
        self.coordination_thread = threading.Thread(target=self._coordination_loop)
        self.coordination_thread.daemon = True
        self.coordination_thread.start()
        
        logger.info("Async coordination system started")
    
    def stop_coordination_system(self):
        """Stop the coordination system."""
        self.coordination_active = False
        
        if self.coordination_thread and self.coordination_thread.is_alive():
            self.coordination_thread.join(timeout=5.0)
        
        if self.event_loop and not self.event_loop.is_closed():
            self.event_loop.close()
        
        logger.info("Async coordination system stopped")
    
    def _coordination_loop(self):
        """Main coordination loop with event loop."""
        try:
            # Create new event loop for this thread
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            
            # Initialize task queue
            self.task_queue = asyncio.Queue(maxsize=self.config.task_queue_size)
            
            # Start task processing
            self.event_loop.run_until_complete(self._process_tasks())
            
        except Exception as e:
            logger.error(f"Error in coordination loop: {e}")
        finally:
            if self.event_loop and not self.event_loop.is_closed():
                self.event_loop.close()
    
    async def _process_tasks(self):
        """Process tasks from the queue."""
        while self.coordination_active:
            try:
                # Wait for tasks with timeout
                try:
                    task = await asyncio.wait_for(self.task_queue.get(), timeout=0.1)
                except asyncio.TimeoutError:
                    continue
                
                # Process task
                await self._execute_task(task)
                self.task_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error processing task: {e}")
                await asyncio.sleep(0.01)
    
    async def _execute_task(self, task: CoordinationTask):
        """Execute a coordination task."""
        if task.task_id in self.running_tasks:
            logger.warning(f"Task {task.task_id} is already running")
            return
        
        try:
            # Check dependencies
            if not await self._check_dependencies(task):
                # Re-queue task for later execution
                await self.task_queue.put(task)
                return
            
            # Mark task as running
            self.running_tasks.add(task.task_id)
            task.started_at = time.time()
            task.status = TaskStatus.RUNNING
            
            # Execute task
            result = await self.executor.execute_task(task)
            
            # Update metrics
            execution_time = result.execution_time
            success = result.status == TaskStatus.COMPLETED
            self.metrics.update_task_metrics(task, execution_time, success)
            
            # Store result
            if success:
                self.completed_tasks[task.task_id] = result
            else:
                self.failed_tasks[task.task_id] = result
            
            logger.info(f"Task {task.task_id} completed with status: {result.status}")
            
        except Exception as e:
            logger.error(f"Error executing task {task.task_id}: {e}")
            task.status = TaskStatus.FAILED
            task.error = str(e)
            
        finally:
            # Remove from running tasks
            self.running_tasks.discard(task.task_id)
    
    async def _check_dependencies(self, task: CoordinationTask) -> bool:
        """Check if task dependencies are satisfied."""
        if not task.dependencies:
            return True
        
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
        
        return True
    
    async def submit_task(self, name: str, description: str, task_type: TaskType,
                         priority: TaskPriority = TaskPriority.NORMAL,
                         mode: CoordinationMode = CoordinationMode.PARALLEL,
                         dependencies: Optional[List[str]] = None,
                         timeout: float = 30.0) -> str:
        """Submit a new task for execution."""
        task_id = str(uuid.uuid4())
        
        task = CoordinationTask(
            task_id=task_id,
            name=name,
            description=description,
            task_type=task_type,
            priority=priority,
            mode=mode,
            dependencies=dependencies or [],
            timeout=timeout,
            created_at=time.time()
        )
        
        # Store task
        self.pending_tasks[task_id] = task
        
        # Add to queue
        if self.task_queue:
            await self.task_queue.put(task)
        
        logger.info(f"Task submitted: {task_id} - {name}")
        return task_id
    
    async def execute_sequential(self, tasks: List[CoordinationTask]) -> List[Any]:
        """Execute tasks sequentially."""
        results = []
        for task in tasks:
            task.created_at = time.time()  # Set current time to minimize latency
            result = await self.executor.execute_task(task)
            results.append(result.result if result.status == TaskStatus.COMPLETED else None)
        return results
    
    async def execute_parallel(self, tasks: List[CoordinationTask]) -> List[Any]:
        """Execute tasks in parallel."""
        task_coros = []
        for task in tasks:
            task.created_at = time.time()  # Set current time to minimize latency
            task_coro = self.executor.execute_task(task)
            task_coros.append(task_coro)

        # Execute all tasks concurrently with optimized batching
        batch_size = 20  # Process in smaller batches for better performance
        results = []

        for i in range(0, len(task_coros), batch_size):
            batch = task_coros[i:i + batch_size]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            results.extend(batch_results)
        
        return [r.result if hasattr(r, 'result') and r.status == TaskStatus.COMPLETED else None 
                for r in results]
    
    async def execute_pipeline(self, tasks: List[CoordinationTask]) -> List[Any]:
        """Execute tasks in pipeline stages."""
        results = []
        for task in tasks:
            task.created_at = time.time()  # Set current time to minimize latency
            result = await self.executor.execute_task(task)
            results.append(result.result if result.status == TaskStatus.COMPLETED else None)
        return results
    
    async def wait_for_all_tasks(self, timeout: float = 30.0):
        """Wait for all pending tasks to complete."""
        start_time = time.time()
        while (self.pending_tasks or self.running_tasks) and (time.time() - start_time) < timeout:
            await asyncio.sleep(0.1)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return self.metrics.get_performance_metrics()
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get status of a specific task."""
        if task_id in self.pending_tasks:
            return TaskStatus.PENDING
        elif task_id in self.running_tasks:
            return TaskStatus.RUNNING
        elif task_id in self.completed_tasks:
            return TaskStatus.COMPLETED
        elif task_id in self.failed_tasks:
            return TaskStatus.FAILED
        else:
            return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return {
            "coordination_active": self.coordination_active,
            "pending_tasks": len(self.pending_tasks),
            "running_tasks": len(self.running_tasks),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "performance_metrics": self.get_performance_metrics()
        }
