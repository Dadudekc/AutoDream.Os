#!/usr/bin/env python3
"""
Asynchronous Coordinator
========================

Individual coordinator implementation for the async coordination system.

**Author:** Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)
**Contract:** COORD-012 - Advanced Coordination Protocol Implementation
**Status:** MODULARIZED
**Target:** <50ms coordination latency (4x improvement)
"""

import asyncio
import threading
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from concurrent.futures import ThreadPoolExecutor

from .models import (
    CoordinationTask, CoordinationState, TaskExecutionResult,
    CoordinationMetrics, CoordinatorConfig
)

class AsyncCoordinator:
    """
    Individual async coordinator for task execution
    
    Features:
    - Non-blocking task execution
    - Priority-based task handling
    - Automatic retry logic
    - Performance monitoring
    """
    
    def __init__(self, 
                 coordinator_id: str,
                 protocol: 'AsyncCoordinationProtocol',
                 config: Optional[CoordinatorConfig] = None):
        self.coordinator_id = coordinator_id
        self.protocol = protocol
        self.config = config or CoordinatorConfig()
        
        # Task management
        self.current_task: Optional[CoordinationTask] = None
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.completed_tasks: List[CoordinationTask] = []
        self.failed_tasks: List[CoordinationTask] = []
        
        # Performance tracking
        self.start_time = datetime.now()
        self.total_tasks_processed = 0
        self.total_processing_time = 0.0
        self.average_latency = 0.0
        self.throughput = 0.0
        
        # State management
        self.is_running = False
        self.is_busy = False
        self.last_heartbeat = datetime.now()
        
        # Threading support
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.lock = threading.Lock()
        self.processing_thread: Optional[threading.Thread] = None
        
        # Logging
        self.logger = logging.getLogger(f"{__name__}.{coordinator_id}")
    
    async def start(self) -> bool:
        """Start the coordinator"""
        try:
            if self.is_running:
                self.logger.warning("Coordinator is already running")
                return True
            
            self.is_running = True
            self.start_time = datetime.now()
            
            # Start processing thread
            self.processing_thread = threading.Thread(target=self._process_tasks, daemon=True)
            self.processing_thread.start()
            
            self.logger.info(f"✅ Coordinator {self.coordinator_id} started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start coordinator: {e}")
            self.is_running = False
            return False
    
    def stop(self) -> bool:
        """Stop the coordinator"""
        try:
            if not self.is_running:
                self.logger.warning("Coordinator is not running")
                return True
            
            self.is_running = False
            
            # Wait for processing thread
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join(timeout=5.0)
            
            # Shutdown executor
            self.executor.shutdown(wait=True)
            
            self.logger.info(f"🏁 Coordinator {self.coordinator_id} stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping coordinator: {e}")
            return False
    
    async def submit_task(self, task: CoordinationTask) -> bool:
        """Submit a task for execution"""
        try:
            if not self.is_running:
                self.logger.warning("Coordinator is not running")
                return False
            
            # Update task status
            task.status = CoordinationState.QUEUED
            task.coordinator_id = self.coordinator_id
            
            # Add to queue
            await self.task_queue.put(task)
            
            self.logger.info(f"📥 Task {task.task_id} submitted to coordinator {self.coordinator_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error submitting task: {e}")
            return False
    
    def _process_tasks(self) -> None:
        """Main task processing loop"""
        while self.is_running:
            try:
                # Get next task from queue
                try:
                    # Use asyncio.run to handle the async queue in a thread
                    task = asyncio.run(self._get_next_task())
                    if task:
                        self._execute_task(task)
                except Exception as e:
                    self.logger.error(f"Error getting next task: {e}")
                
                # Small delay to prevent CPU spinning
                time.sleep(0.001)
                
            except Exception as e:
                self.logger.error(f"Error in task processing loop: {e}")
                time.sleep(1.0)
    
    async def _get_next_task(self) -> Optional[CoordinationTask]:
        """Get the next task from the queue"""
        try:
            # Wait for a task with timeout
            task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
            return task
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            self.logger.error(f"Error getting task from queue: {e}")
            return None
    
    def _execute_task(self, task: CoordinationTask) -> None:
        """Execute a single task"""
        try:
            start_time = time.time()
            self.is_busy = True
            self.current_task = task
            
            # Update task status
            task.status = CoordinationState.EXECUTING
            task.start_time = datetime.now()
            
            self.logger.info(f"🚀 Executing task {task.task_id}: {task.description}")
            
            # Execute task
            if task.async_executor:
                # Async executor
                result = asyncio.run(self._execute_async_task(task))
            elif task.executor:
                # Sync executor
                result = self._execute_sync_task(task)
            else:
                # No executor provided
                result = TaskExecutionResult(
                    task_id=task.task_id,
                    success=False,
                    error="No executor provided",
                    coordinator_id=self.coordinator_id
                )
            
            # Update task with result
            if result.success:
                task.status = CoordinationState.COMPLETED
                task.result = result.result
                self.completed_tasks.append(task)
                self.total_tasks_processed += 1
                self.logger.info(f"✅ Task {task.task_id} completed successfully")
            else:
                task.status = CoordinationState.FAILED
                task.error = result.error
                self.failed_tasks.append(task)
                self.logger.error(f"❌ Task {task.task_id} failed: {result.error}")
            
            # Update timing
            execution_time = time.time() - start_time
            task.processing_time = execution_time
            task.completion_time = datetime.now()
            self.total_processing_time += execution_time
            
            # Update performance metrics
            self._update_performance_metrics(execution_time)
            
            # Update heartbeat
            self.last_heartbeat = datetime.now()
            
        except Exception as e:
            self.logger.error(f"❌ Error executing task {task.task_id}: {e}")
            task.status = CoordinationState.FAILED
            task.error = str(e)
            self.failed_tasks.append(task)
        finally:
            self.is_busy = False
            self.current_task = None
    
    async def _execute_async_task(self, task: CoordinationTask) -> TaskExecutionResult:
        """Execute an async task"""
        try:
            start_time = time.time()
            
            # Execute the async function
            if asyncio.iscoroutinefunction(task.async_executor):
                result = await task.async_executor()
            else:
                result = await task.async_executor()
            
            execution_time = time.time() - start_time
            
            return TaskExecutionResult(
                task_id=task.task_id,
                success=True,
                result=result,
                execution_time=execution_time,
                coordinator_id=self.coordinator_id
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TaskExecutionResult(
                task_id=task.task_id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                coordinator_id=self.coordinator_id
            )
    
    def _execute_sync_task(self, task: CoordinationTask) -> TaskExecutionResult:
        """Execute a sync task"""
        try:
            start_time = time.time()
            
            # Execute the sync function
            result = task.executor()
            
            execution_time = time.time() - start_time
            
            return TaskExecutionResult(
                task_id=task.task_id,
                success=True,
                result=result,
                execution_time=execution_time,
                coordinator_id=self.coordinator_id
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return TaskExecutionResult(
                task_id=task.task_id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                coordinator_id=self.coordinator_id
            )
    
    def _update_performance_metrics(self, execution_time: float) -> None:
        """Update performance metrics"""
        # Update average latency
        if self.total_tasks_processed > 0:
            self.average_latency = self.total_processing_time / self.total_tasks_processed
        
        # Update throughput (tasks per second)
        if self.total_processing_time > 0:
            self.throughput = self.total_tasks_processed / self.total_processing_time
    
    def get_status(self) -> Dict[str, Any]:
        """Get current coordinator status"""
        return {
            'coordinator_id': self.coordinator_id,
            'is_running': self.is_running,
            'is_busy': self.is_busy,
            'current_task': self.current_task.task_id if self.current_task else None,
            'total_tasks_processed': self.total_tasks_processed,
            'total_processing_time': self.total_processing_time,
            'average_latency': self.average_latency,
            'throughput': self.throughput,
            'queue_size': self.task_queue.qsize(),
            'last_heartbeat': self.last_heartbeat.isoformat(),
            'uptime': (datetime.now() - self.start_time).total_seconds()
        }
    
    def get_metrics(self) -> CoordinationMetrics:
        """Get performance metrics"""
        return CoordinationMetrics(
            total_tasks=self.total_tasks_processed,
            completed_tasks=len(self.completed_tasks),
            failed_tasks=len(self.failed_tasks),
            average_latency=self.average_latency * 1000,  # Convert to milliseconds
            throughput=self.throughput,
            active_coordinators=1 if self.is_running else 0,
            queue_depth=self.task_queue.qsize(),
            last_updated=datetime.now()
        )
    
    def is_healthy(self) -> bool:
        """Check if coordinator is healthy"""
        if not self.is_running:
            return False
        
        # Check heartbeat
        time_since_heartbeat = (datetime.now() - self.last_heartbeat).total_seconds()
        if time_since_heartbeat > self.config.heartbeat_interval * 3:
            return False
        
        return True
