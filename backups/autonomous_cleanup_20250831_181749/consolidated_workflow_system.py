"""
Consolidated Workflow System
Unified workflow management infrastructure for the entire project.
V2 Compliance: Under 400 lines, SSOT principles, object-oriented design.
"""

import asyncio
import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable
from concurrent.futures import ThreadPoolExecutor


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class WorkflowTask:
    """Individual workflow task definition."""
    id: str
    name: str
    action: Callable
    dependencies: List[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.NORMAL
    timeout: int = 300
    retry_count: int = 3
    retry_delay: int = 5
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """Workflow execution instance."""
    id: str
    workflow_id: str
    status: WorkflowStatus
    start_time: float
    end_time: Optional[float] = None
    tasks_completed: List[str] = field(default_factory=list)
    tasks_failed: List[str] = field(default_factory=list)
    current_task: Optional[str] = None
    progress: float = 0.0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class WorkflowEngine(ABC):
    """Abstract workflow execution engine."""
    
    @abstractmethod
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute a workflow."""
        pass
    
    @abstractmethod
    async def cancel_workflow(self, execution_id: str) -> bool:
        """Cancel workflow execution."""
        pass
    
    @abstractmethod
    async def pause_workflow(self, execution_id: str) -> bool:
        """Pause workflow execution."""
        pass
    
    @abstractmethod
    async def resume_workflow(self, execution_id: str) -> bool:
        """Resume workflow execution."""
        pass


class SequentialWorkflowEngine(WorkflowEngine):
    """Sequential workflow execution engine."""
    
    def __init__(self):
        self.workflows: Dict[str, List[WorkflowTask]] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self._lock = threading.Lock()
    
    def register_workflow(self, workflow_id: str, tasks: List[WorkflowTask]):
        """Register a workflow definition."""
        with self._lock:
            self.workflows[workflow_id] = tasks
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute workflow sequentially."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        execution = WorkflowExecution(
            id=f"{workflow_id}_{int(time.time())}",
            workflow_id=workflow_id,
            status=WorkflowStatus.RUNNING,
            start_time=time.time()
        )
        
        self.executions[execution.id] = execution
        
        try:
            tasks = self.workflows[workflow_id]
            total_tasks = len(tasks)
            
            for i, task in enumerate(tasks):
                execution.current_task = task.id
                execution.progress = (i / total_tasks) * 100
                
                # Check dependencies
                if not all(dep in execution.tasks_completed for dep in task.dependencies):
                    raise Exception(f"Task {task.id} dependencies not met")
                
                # Execute task with retry logic
                success = False
                for attempt in range(task.retry_count + 1):
                    try:
                        if asyncio.iscoroutinefunction(task.action):
                            result = await asyncio.wait_for(task.action(**parameters), timeout=task.timeout)
                        else:
                            result = task.action(**parameters)
                        
                        execution.tasks_completed.append(task.id)
                        success = True
                        break
                    except Exception as e:
                        if attempt < task.retry_count:
                            await asyncio.sleep(task.retry_delay)
                        else:
                            execution.tasks_failed.append(task.id)
                            raise e
                
                if not success:
                    break
            
            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = time.time()
            execution.progress = 100.0
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.end_time = time.time()
            execution.error = str(e)
        
        return execution
    
    async def cancel_workflow(self, execution_id: str) -> bool:
        """Cancel workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.RUNNING:
                execution.status = WorkflowStatus.CANCELLED
                execution.end_time = time.time()
                return True
        return False
    
    async def pause_workflow(self, execution_id: str) -> bool:
        """Pause workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.RUNNING:
                execution.status = WorkflowStatus.PAUSED
                return True
        return False
    
    async def resume_workflow(self, execution_id: str) -> bool:
        """Resume workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.PAUSED:
                execution.status = WorkflowStatus.RUNNING
                return True
        return False


class ParallelWorkflowEngine(WorkflowEngine):
    """Parallel workflow execution engine."""
    
    def __init__(self, max_workers: int = 4):
        self.workflows: Dict[str, List[WorkflowTask]] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.max_workers = max_workers
        self._lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def register_workflow(self, workflow_id: str, tasks: List[WorkflowTask]):
        """Register a workflow definition."""
        with self._lock:
            self.workflows[workflow_id] = tasks
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute workflow with parallel task execution."""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        execution = WorkflowExecution(
            id=f"{workflow_id}_{int(time.time())}",
            workflow_id=workflow_id,
            status=WorkflowStatus.RUNNING,
            start_time=time.time()
        )
        
        self.executions[execution.id] = execution
        
        try:
            tasks = self.workflows[workflow_id]
            completed_tasks = set()
            failed_tasks = set()
            
            # Execute tasks in parallel where possible
            while len(completed_tasks) + len(failed_tasks) < len(tasks):
                ready_tasks = [
                    task for task in tasks
                    if task.id not in completed_tasks and task.id not in failed_tasks
                    and all(dep in completed_tasks for dep in task.dependencies)
                ]
                
                if not ready_tasks:
                    break
                
                # Execute ready tasks in parallel
                task_futures = []
                for task in ready_tasks:
                    future = asyncio.create_task(self._execute_task(task, parameters))
                    task_futures.append((task.id, future))
                
                # Wait for all tasks to complete
                for task_id, future in task_futures:
                    try:
                        await future
                        completed_tasks.add(task_id)
                        execution.tasks_completed.append(task_id)
                    except Exception as e:
                        failed_tasks.add(task_id)
                        execution.tasks_failed.append(task_id)
            
            execution.status = WorkflowStatus.COMPLETED if not failed_tasks else WorkflowStatus.FAILED
            execution.end_time = time.time()
            execution.progress = 100.0
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.end_time = time.time()
            execution.error = str(e)
        
        return execution
    
    async def _execute_task(self, task: WorkflowTask, parameters: Dict[str, Any]):
        """Execute individual task with retry logic."""
        for attempt in range(task.retry_count + 1):
            try:
                if asyncio.iscoroutinefunction(task.action):
                    result = await asyncio.wait_for(task.action(**parameters), timeout=task.timeout)
                else:
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.executor, task.action, **parameters
                    )
                return result
            except Exception as e:
                if attempt < task.retry_count:
                    await asyncio.sleep(task.retry_delay)
                else:
                    raise e
    
    async def cancel_workflow(self, execution_id: str) -> bool:
        """Cancel workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.RUNNING:
                execution.status = WorkflowStatus.CANCELLED
                execution.end_time = time.time()
                return True
        return False
    
    async def pause_workflow(self, execution_id: str) -> bool:
        """Pause workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.RUNNING:
                execution.status = WorkflowStatus.PAUSED
                return True
        return False
    
    async def resume_workflow(self, execution_id: str) -> bool:
        """Resume workflow execution."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            if execution.status == WorkflowStatus.PAUSED:
                execution.status = WorkflowStatus.RUNNING
                return True
        return False


class WorkflowManager:
    """Centralized workflow management system."""
    
    def __init__(self):
        self.sequential_engine = SequentialWorkflowEngine()
        self.parallel_engine = ParallelWorkflowEngine()
        self.workflow_registry: Dict[str, Dict[str, Any]] = {}
    
    def register_workflow(self, workflow_id: str, tasks: List[WorkflowTask], parallel: bool = False):
        """Register workflow with appropriate engine."""
        if parallel:
            self.parallel_engine.register_workflow(workflow_id, tasks)
        else:
            self.sequential_engine.register_workflow(workflow_id, tasks)
        
        self.workflow_registry[workflow_id] = {
            'tasks': tasks,
            'parallel': parallel,
            'created_at': time.time()
        }
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute workflow using appropriate engine."""
        if workflow_id not in self.workflow_registry:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow_info = self.workflow_registry[workflow_id]
        if workflow_info['parallel']:
            return await self.parallel_engine.execute_workflow(workflow_id, parameters)
        else:
            return await self.sequential_engine.execute_workflow(workflow_id, parameters)
    
    def get_workflow_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get workflow execution status."""
        execution = self.sequential_engine.executions.get(execution_id)
        if not execution:
            execution = self.parallel_engine.executions.get(execution_id)
        return execution


class ConsolidatedWorkflowSystem:
    """Main consolidated workflow system."""
    
    def __init__(self):
        self.manager = WorkflowManager()
        self._initialized = False
    
    def initialize(self, config: Dict[str, Any]):
        """Initialize workflow system with configuration."""
        if self._initialized:
            return
        
        # Register default workflows if specified in config
        if 'default_workflows' in config:
            for workflow_config in config['default_workflows']:
                tasks = [
                    WorkflowTask(**task_config)
                    for task_config in workflow_config['tasks']
                ]
                self.manager.register_workflow(
                    workflow_config['id'],
                    tasks,
                    workflow_config.get('parallel', False)
                )
        
        self._initialized = True
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> WorkflowExecution:
        """Execute a workflow."""
        if not self._initialized:
            raise RuntimeError("Workflow system not initialized")
        return await self.manager.execute_workflow(workflow_id, parameters)
    
    def register_workflow(self, workflow_id: str, tasks: List[WorkflowTask], parallel: bool = False):
        """Register a new workflow."""
        self.manager.register_workflow(workflow_id, tasks, parallel)
    
    def get_execution_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get workflow execution status."""
        return self.manager.get_workflow_status(execution_id)
    
    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel workflow execution."""
        return await self.manager.sequential_engine.cancel_workflow(execution_id) or \
               await self.manager.parallel_engine.cancel_workflow(execution_id)


# Global workflow system instance
workflow_system = ConsolidatedWorkflowSystem()
