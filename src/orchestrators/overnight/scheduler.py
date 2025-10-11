"""
Task Scheduler - V2 Compliant
=============================

Cycle-based task scheduling for overnight autonomous operations.
Implements priority queues and load balancing across agents.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Autonomous Operations Specialist
License: MIT
"""

import asyncio
import heapq
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging

# V2 Integration imports
try:
    from ...core.unified_config import get_unified_config
    from ...core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)


@dataclass
class Task:
    """Task representation for scheduling."""
    id: str
    type: str
    priority: int  # Lower number = higher priority
    agent_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    created_time: float = field(default_factory=time.time)
    scheduled_cycle: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: float = 300.0  # seconds
    retry_count: int = 0
    max_retries: int = 3
    
    def __lt__(self, other):
        """Priority queue ordering (lower priority number = higher priority)."""
        return self.priority < other.priority


class TaskScheduler:
    """
    Cycle-based task scheduler for overnight operations.
    
    Provides:
    - Priority-based task queuing
    - Load balancing across agents
    - Dependency management
    - Retry logic
    - Cycle-based scheduling (V2 requirement)
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize task scheduler.
        
        Args:
            config: Configuration dictionary (uses config/orchestration.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Scheduling settings
        scheduling_config = self.config.get('overnight', {}).get('scheduling', {})
        self.strategy = scheduling_config.get('strategy', 'cycle_based')
        self.priority_queue = scheduling_config.get('priority_queue', True)
        self.load_balancing = scheduling_config.get('load_balancing', True)
        self.max_tasks_per_cycle = scheduling_config.get('max_tasks_per_cycle', 5)
        
        # State
        self.task_queue = []  # Priority queue
        self.task_registry = {}  # Task ID -> Task mapping
        self.agent_load = {}  # Agent ID -> current load
        self.completed_tasks = set()
        self.failed_tasks = set()
        self.current_cycle = 0
        
        # Task types and priorities
        self.task_priorities = {
            'system_health': 1,
            'agent_recovery': 2,
            'workflow_execution': 3,
            'monitoring': 4,
            'cleanup': 5,
            'maintenance': 6,
        }
        
        self.logger.info("Task Scheduler initialized")

    async def initialize(self) -> None:
        """Initialize scheduler components."""
        try:
            # Initialize agent load tracking
            self.agent_load = {f"Agent-{i}": 0 for i in range(1, 9)}
            
            # Load any persisted tasks
            await self._load_persisted_tasks()
            
            self.logger.info("Task scheduler initialized")
            
        except Exception as e:
            self.logger.error(f"Scheduler initialization failed: {e}")
            raise

    def add_task(
        self,
        task_id: str,
        task_type: str,
        agent_id: str,
        data: Dict[str, Any],
        priority: Optional[int] = None,
        scheduled_cycle: Optional[int] = None,
        dependencies: Optional[List[str]] = None,
        estimated_duration: float = 300.0
    ) -> bool:
        """
        Add a task to the scheduler.
        
        Args:
            task_id: Unique task identifier
            task_type: Type of task
            agent_id: Target agent
            data: Task data
            priority: Task priority (uses default if None)
            scheduled_cycle: Specific cycle to run (None for next available)
            dependencies: List of task IDs this task depends on
            estimated_duration: Estimated duration in seconds
            
        Returns:
            True if task added successfully
        """
        try:
            # Use default priority if not specified
            if priority is None:
                priority = self.task_priorities.get(task_type, 5)
            
            # Create task
            task = Task(
                id=task_id,
                type=task_type,
                priority=priority,
                agent_id=agent_id,
                data=data,
                scheduled_cycle=scheduled_cycle,
                dependencies=dependencies or [],
                estimated_duration=estimated_duration
            )
            
            # Add to registry
            self.task_registry[task_id] = task
            
            # Add to priority queue
            heapq.heappush(self.task_queue, task)
            
            self.logger.info(f"Task added: {task_id} (type: {task_type}, priority: {priority})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add task {task_id}: {e}")
            return False

    async def get_cycle_tasks(self, cycle_number: int) -> List[Dict[str, Any]]:
        """
        Get tasks for a specific cycle.
        
        Args:
            cycle_number: Cycle number
            
        Returns:
            List of task dictionaries for execution
        """
        self.current_cycle = cycle_number
        
        try:
            # Get available tasks
            available_tasks = self._get_available_tasks(cycle_number)
            
            # Apply load balancing
            if self.load_balancing:
                available_tasks = self._balance_agent_load(available_tasks)
            
            # Limit tasks per cycle
            if len(available_tasks) > self.max_tasks_per_cycle:
                available_tasks = available_tasks[:self.max_tasks_per_cycle]
            
            # Convert to execution format
            cycle_tasks = []
            for task in available_tasks:
                task_dict = {
                    'id': task.id,
                    'type': task.type,
                    'agent_id': task.agent_id,
                    'data': task.data,
                    'priority': task.priority,
                    'estimated_duration': task.estimated_duration,
                    'retry_count': task.retry_count,
                    'scheduled_cycle': cycle_number
                }
                cycle_tasks.append(task_dict)
                
                # Update agent load
                self.agent_load[task.agent_id] += task.estimated_duration
            
            self.logger.info(f"Cycle {cycle_number}: {len(cycle_tasks)} tasks scheduled")
            return cycle_tasks
            
        except Exception as e:
            self.logger.error(f"Failed to get cycle tasks: {e}")
            return []

    def _get_available_tasks(self, cycle_number: int) -> List[Task]:
        """Get tasks available for execution in this cycle."""
        available_tasks = []
        temp_queue = []
        
        # Process priority queue
        while self.task_queue:
            task = heapq.heappop(self.task_queue)
            
            # Check if task is ready for this cycle
            if self._is_task_ready(task, cycle_number):
                available_tasks.append(task)
            else:
                temp_queue.append(task)
        
        # Restore tasks not ready for this cycle
        for task in temp_queue:
            heapq.heappush(self.task_queue, task)
        
        return available_tasks

    def _is_task_ready(self, task: Task, cycle_number: int) -> bool:
        """Check if a task is ready for execution."""
        # Check if task is scheduled for this cycle or later
        if task.scheduled_cycle and task.scheduled_cycle > cycle_number:
            return False
        
        # Check dependencies
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
        
        # Check if task has exceeded max retries
        if task.retry_count >= task.max_retries:
            self.failed_tasks.add(task.id)
            return False
        
        return True

    def _balance_agent_load(self, tasks: List[Task]) -> List[Task]:
        """Balance task load across agents."""
        if not self.load_balancing:
            return tasks
        
        # Sort tasks by priority first
        tasks.sort(key=lambda t: t.priority)
        
        # Distribute tasks to balance load
        balanced_tasks = []
        agent_loads = self.agent_load.copy()
        
        for task in tasks:
            # Find agent with lowest current load
            target_agent = min(agent_loads.keys(), key=lambda a: agent_loads[a])
            
            # Update task agent if different
            if task.agent_id != target_agent:
                task.agent_id = target_agent
                self.logger.info(f"Rebalanced task {task.id} to {target_agent}")
            
            # Update load tracking
            agent_loads[target_agent] += task.estimated_duration
            balanced_tasks.append(task)
        
        return balanced_tasks

    def mark_task_completed(self, task_id: str) -> None:
        """Mark a task as completed."""
        if task_id in self.task_registry:
            self.completed_tasks.add(task_id)
            
            # Remove from queue if still there
            self._remove_task_from_queue(task_id)
            
            # Update agent load
            task = self.task_registry[task_id]
            self.agent_load[task.agent_id] = max(0, self.agent_load[task.agent_id] - task.estimated_duration)
            
            self.logger.info(f"Task completed: {task_id}")

    def mark_task_failed(self, task_id: str, retry: bool = True) -> None:
        """Mark a task as failed and optionally retry."""
        if task_id not in self.task_registry:
            return
        
        task = self.task_registry[task_id]
        
        if retry and task.retry_count < task.max_retries:
            # Retry task
            task.retry_count += 1
            task.priority += 1  # Lower priority for retry
            task.scheduled_cycle = self.current_cycle + 1  # Schedule for next cycle
            
            # Re-add to queue
            heapq.heappush(self.task_queue, task)
            
            self.logger.info(f"Task retry scheduled: {task_id} (attempt {task.retry_count})")
        else:
            # Mark as permanently failed
            self.failed_tasks.add(task_id)
            self._remove_task_from_queue(task_id)
            
            # Update agent load
            self.agent_load[task.agent_id] = max(0, self.agent_load[task.agent_id] - task.estimated_duration)
            
            self.logger.error(f"Task permanently failed: {task_id}")

    def _remove_task_from_queue(self, task_id: str) -> None:
        """Remove task from priority queue."""
        temp_queue = []
        
        while self.task_queue:
            task = heapq.heappop(self.task_queue)
            if task.id != task_id:
                temp_queue.append(task)
        
        # Restore remaining tasks
        for task in temp_queue:
            heapq.heappush(self.task_queue, task)

    async def _load_persisted_tasks(self) -> None:
        """Load persisted tasks from storage."""
        # This would load tasks from disk/database
        # For now, just log the intention
        self.logger.info("Loading persisted tasks")

    def get_scheduler_status(self) -> Dict[str, Any]:
        """Get current scheduler status."""
        return {
            "strategy": self.strategy,
            "priority_queue": self.priority_queue,
            "load_balancing": self.load_balancing,
            "max_tasks_per_cycle": self.max_tasks_per_cycle,
            "current_cycle": self.current_cycle,
            "queue_size": len(self.task_queue),
            "registered_tasks": len(self.task_registry),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "agent_loads": self.agent_load,
            "task_priorities": self.task_priorities,
        }
