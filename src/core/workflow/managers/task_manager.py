#!/usr/bin/env python3
"""
Task Manager - Task Management Engine
===================================

Task management for unified workflow system.
Follows V2 standards: ≤200 LOC, single responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from ..types.workflow_models import WorkflowTask, WorkflowStep, AgentCapabilityInfo
from ..types.workflow_enums import TaskStatus, TaskPriority, TaskType


class TaskManager:
    """
    Task manager for workflow system.
    
    Single responsibility: Manage task lifecycle including creation,
    assignment, execution tracking, and dependency management.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.TaskManager")
        self.tasks: Dict[str, WorkflowTask] = {}
        self.task_assignments: Dict[str, str] = {}  # task_id -> agent_id
        self.task_dependencies: Dict[str, List[str]] = {}  # task_id -> [dependency_ids]
        self.agent_capabilities: Dict[str, AgentCapabilityInfo] = {}
    
    def create_task(self, task: WorkflowTask) -> str:
        """
        Create new task.
        
        Args:
            task: Task definition to create
            
        Returns:
            Task ID of the created task
        """
        self.logger.info(f"Creating task: {task.task_id}")
        
        # Validate task definition
        if not self._validate_task_definition(task):
            raise ValueError("Invalid task definition")
        
        # Store task
        self.tasks[task.task_id] = task
        
        # Initialize dependencies
        if task.dependencies:
            self.task_dependencies[task.task_id] = task.dependencies.copy()
        
        self.logger.info(f"Task created successfully: {task.task_id}")
        return task.task_id
    
    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """
        Assign task to an agent.
        
        Args:
            task_id: ID of the task to assign
            agent_id: ID of the agent to assign to
            
        Returns:
            True if assignment successful, False otherwise
        """
        self.logger.info(f"Assigning task {task_id} to agent {agent_id}")
        
        if task_id not in self.tasks:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        if not self._check_agent_capability(agent_id, task_id):
            self.logger.error(f"Agent {agent_id} lacks capability for task {task_id}")
            return False
        
        # Check if task is already assigned
        if task_id in self.task_assignments:
            self.logger.warning(f"Task {task_id} is already assigned to {self.task_assignments[task_id]}")
            return False
        
        # Assign task
        self.task_assignments[task_id] = agent_id
        self.tasks[task_id].status = TaskStatus.ASSIGNED
        self.tasks[task_id].assigned_agent = agent_id
        self.tasks[task_id].assignment_time = datetime.now().isoformat()
        
        self.logger.info(f"Task {task_id} assigned to agent {agent_id}")
        return True
    
    def start_task(self, task_id: str) -> bool:
        """
        Start task execution.
        
        Args:
            task_id: ID of the task to start
            
        Returns:
            True if start successful, False otherwise
        """
        self.logger.info(f"Starting task: {task_id}")
        
        if task_id not in self.tasks:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        # Check if task is assigned
        if task_id not in self.task_assignments:
            self.logger.error(f"Task {task_id} is not assigned")
            return False
        
        # Check dependencies
        if not self._check_dependencies_completed(task_id):
            self.logger.error(f"Task {task_id} dependencies not completed")
            return False
        
        # Start task
        task.status = TaskStatus.RUNNING
        task.start_time = datetime.now().isoformat()
        
        self.logger.info(f"Task {task_id} started successfully")
        return True
    
    def complete_task(self, task_id: str, result: Optional[Dict[str, Any]] = None) -> bool:
        """
        Mark task as completed.
        
        Args:
            task_id: ID of the task to complete
            result: Optional result data from task execution
            
        Returns:
            True if completion successful, False otherwise
        """
        self.logger.info(f"Completing task: {task_id}")
        
        if task_id not in self.tasks:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        if task.status != TaskStatus.RUNNING:
            self.logger.error(f"Task {task_id} is not running")
            return False
        
        # Complete task
        task.status = TaskStatus.COMPLETED
        task.end_time = datetime.now().isoformat()
        if result:
            task.result = result
        
        self.logger.info(f"Task {task_id} completed successfully")
        return True
    
    def fail_task(self, task_id: str, error_message: str) -> bool:
        """
        Mark task as failed.
        
        Args:
            task_id: ID of the task to fail
            error_message: Error message describing the failure
            
        Returns:
            True if failure marking successful, False otherwise
        """
        self.logger.info(f"Marking task as failed: {task_id}")
        
        if task_id not in self.tasks:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        # Mark task as failed
        task.status = TaskStatus.FAILED
        task.end_time = datetime.now().isoformat()
        task.error_message = error_message
        
        self.logger.info(f"Task {task_id} marked as failed: {error_message}")
        return True
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """
        Get current status of a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Current task status or None if not found
        """
        if task_id in self.tasks:
            return self.tasks[task_id].status
        return None
    
    def get_task_assignee(self, task_id: str) -> Optional[str]:
        """
        Get the agent assigned to a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Agent ID assigned to the task or None if not assigned
        """
        return self.task_assignments.get(task_id)
    
    def get_ready_tasks(self) -> List[str]:
        """
        Get list of tasks ready for execution.
        
        Returns:
            List of task IDs that are ready to execute
        """
        ready_tasks = []
        
        for task_id, task in self.tasks.items():
            if (task.status == TaskStatus.ASSIGNED and 
                self._check_dependencies_completed(task_id)):
                ready_tasks.append(task_id)
        
        return ready_tasks
    
    def get_blocked_tasks(self) -> List[str]:
        """
        Get list of tasks blocked by dependencies.
        
        Returns:
            List of task IDs that are blocked
        """
        blocked_tasks = []
        
        for task_id, task in self.tasks.items():
            if (task.status == TaskStatus.ASSIGNED and 
                not self._check_dependencies_completed(task_id)):
                blocked_tasks.append(task_id)
        
        return blocked_tasks
    
    def add_agent_capability(self, agent_id: str, capability: AgentCapabilityInfo):
        """
        Add agent capability information.
        
        Args:
            agent_id: ID of the agent
            capability: Capability information for the agent
        """
        self.agent_capabilities[agent_id] = capability
        self.logger.info(f"Added capabilities for agent: {agent_id}")
    
    def _validate_task_definition(self, task: WorkflowTask) -> bool:
        """Validate task definition structure and requirements."""
        if not task.task_id or not task.name:
            return False
        
        # Check for valid task type
        if task.task_type not in ["general", TaskType.COMPUTATION.value, TaskType.DATA_PROCESSING.value, 
                                 TaskType.DECISION.value, TaskType.INTEGRATION.value]:
            return False
        
        return True
    
    def _check_agent_capability(self, agent_id: str, task_id: str) -> bool:
        """Check if agent has capability to execute the task."""
        if agent_id not in self.agent_capabilities:
            return False
        
        task = self.tasks[task_id]
        agent_capability = self.agent_capabilities[agent_id]
        
        # Check if agent supports the required task type
        if task.task_type not in agent_capability.supported_task_types:
            return False
        
        # Check if agent meets resource requirements
        if task.resource_requirements:
            for req in task.resource_requirements:
                if not self._check_resource_requirement(agent_capability, req):
                    return False
        
        return True
    
    def _check_resource_requirement(self, agent_capability: AgentCapabilityInfo, 
                                  requirement: Any) -> bool:
        """Check if agent meets resource requirement."""
        # Basic implementation - can be extended with more sophisticated resource checking
        return True
    
    def _check_dependencies_completed(self, task_id: str) -> bool:
        """Check if all dependencies for a task are completed."""
        if task_id not in self.task_dependencies:
            return True  # No dependencies
        
        for dep_id in self.task_dependencies[task_id]:
            if dep_id not in self.tasks:
                self.logger.warning(f"Dependency {dep_id} not found for task {task_id}")
                return False
            
            if self.tasks[dep_id].status != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for task manager."""
        try:
            # Test task creation
            from ..types.workflow_models import WorkflowTask
            from ..types.workflow_enums import TaskType, TaskPriority
            
            test_task = WorkflowTask(
                task_id="test_task",
                name="Test Task",
                description="Test task for smoke testing"
            )
            
            task_id = self.create_task(test_task)
            if task_id == "test_task":
                self.logger.info("✅ Task manager smoke test passed.")
                return True
            else:
                self.logger.error("❌ Task manager smoke test failed: Invalid task ID returned.")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Task manager smoke test failed: {e}")
            return False
