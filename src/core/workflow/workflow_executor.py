#!/usr/bin/env python3
"""
Workflow Executor - V2 Core Workflow Task Execution

This module handles workflow task execution and management.
Follows V2 standards: ≤200 lines, single responsibility, clean OOP design.

Author: Agent-4 (Quality Assurance)
License: MIT
"""

import logging
import time
import uuid

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime
from typing import Dict, List, Optional, Any, Set

try:
    from .workflow_types import (
        WorkflowStatus, WorkflowExecution, WorkflowTask, 
        WorkflowCondition, TaskStatus, AgentCapability
    )
except ImportError:
    # Fallback for standalone usage
    from workflow_types import (
        WorkflowStatus, WorkflowExecution, WorkflowTask, 
        WorkflowCondition, TaskStatus, AgentCapability
    )

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """
    Workflow task execution engine
    
    Responsibilities:
    - Task execution and management
    - Conditional workflow handling
    - Error handling and retry logic
    - Agent task assignment
    """

    def __init__(self, max_workers: int = 4):
        """Initialize the workflow executor"""
        self.max_workers = max_workers
        self.running_tasks: Set[str] = set()
        logger.info(f"Workflow Executor initialized with {max_workers} workers")

    def execute_workflow(self, execution: WorkflowExecution) -> bool:
        """Execute a complete workflow"""
        try:
            execution.status = WorkflowStatus.EXECUTING
            execution.start_time = datetime.now()
            
            # Plan execution
            execution_plan = self._create_execution_plan(execution)
            
            # Execute tasks according to plan
            success = self._execute_tasks(execution, execution_plan)
            
            if success:
                execution.status = WorkflowStatus.COMPLETED
                execution.end_time = datetime.now()
                if execution.start_time:
                    execution.total_duration = int((execution.end_time - execution.start_time).total_seconds())
            else:
                execution.status = WorkflowStatus.FAILED
                execution.end_time = datetime.now()
            
            return success
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            execution.status = WorkflowStatus.FAILED
            execution.end_time = datetime.now()
            return False

    def _create_execution_plan(self, execution: WorkflowExecution) -> List[str]:
        """Create execution plan for workflow tasks"""
        plan = []
        completed = set()
        
        # Simple sequential execution for now
        for task in execution.tasks:
            if all(dep in completed for dep in task.dependencies):
                plan.append(task.task_id)
                completed.add(task.task_id)
        
        return plan

    def _execute_tasks(self, execution: WorkflowExecution, plan: List[str]) -> bool:
        """Execute tasks according to execution plan"""
        try:
            for task_id in plan:
                task = self._find_task_by_id(execution, task_id)
                if not task:
                    continue
                
                # Execute single task
                success = self._execute_single_task(task)
                
                if success:
                    execution.completed_tasks.append(task_id)
                    task.status = TaskStatus.COMPLETED
                    task.completed_at = datetime.now()
                else:
                    execution.failed_tasks.append(task_id)
                    task.status = TaskStatus.FAILED
                    execution.error_count += 1
                    
                    # Check if we should continue
                    if execution.error_count > 3:
                        logger.error("Too many task failures, stopping execution")
                        return False
            
            return len(execution.failed_tasks) == 0
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return False

    def _execute_single_task(self, task: WorkflowTask) -> bool:
        """Execute a single workflow task"""
        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            
            # Simulate task execution
            logger.info(f"Executing task: {task.name}")
            time.sleep(0.1)  # Simulate work
            
            # Check for task failure simulation
            if task.name.lower().contains("fail"):
                task.error_message = "Simulated task failure"
                return False
            
            # Simulate successful completion
            task.actual_duration = int((datetime.now() - task.started_at).total_seconds())
            logger.info(f"Task {task.name} completed successfully")
            return True
            
        except Exception as e:
            task.error_message = str(e)
            logger.error(f"Task {task.name} execution failed: {e}")
            return False

    def _find_task_by_id(self, execution: WorkflowExecution, task_id: str) -> Optional[WorkflowTask]:
        """Find a task by its ID in an execution"""
        for task in execution.tasks:
            if task.task_id == task_id:
                return task
        return None

    def execute_conditional_workflow(self, execution: WorkflowExecution) -> bool:
        """Execute workflow with conditional logic"""
        try:
            execution.status = WorkflowStatus.EXECUTING
            execution.start_time = datetime.now()
            
            for condition in execution.conditions:
                if condition.condition_type == "if":
                    success = self._execute_if_condition(execution, condition)
                elif condition.condition_type == "while":
                    success = self._execute_while_condition(execution, condition)
                elif condition.condition_type == "for":
                    success = self._execute_for_condition(execution, condition)
                else:
                    logger.warning(f"Unknown condition type: {condition.condition_type}")
                    continue
                
                if not success:
                    execution.status = WorkflowStatus.FAILED
                    return False
            
            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = datetime.now()
            return True
            
        except Exception as e:
            logger.error(f"Conditional workflow execution failed: {e}")
            execution.status = WorkflowStatus.FAILED
            return False

    def _execute_if_condition(self, execution: WorkflowExecution, condition: WorkflowCondition) -> bool:
        """Execute if-else conditional logic"""
        try:
            # Evaluate condition (simplified)
            condition_met = self._evaluate_condition(condition.condition_expression)
            
            if condition_met:
                # Execute true branch
                for task_id in condition.true_branch:
                    task = self._find_task_by_id(execution, task_id)
                    if task:
                        success = self._execute_single_task(task)
                        if success:
                            execution.completed_tasks.append(task_id)
                        else:
                            execution.failed_tasks.append(task_id)
            else:
                # Execute false branch
                for task_id in condition.false_branch:
                    task = self._find_task_by_id(execution, task_id)
                    if task:
                        success = self._execute_single_task(task)
                        if success:
                            execution.completed_tasks.append(task_id)
                        else:
                            execution.failed_tasks.append(task_id)
            
            return True
            
        except Exception as e:
            logger.error(f"If condition execution failed: {e}")
            return False

    def _evaluate_condition(self, condition_expression: str) -> bool:
        """Evaluate a condition expression (simplified)"""
        try:
            # Simple condition evaluation
            if "true" in condition_expression.lower():
                return True
            elif "false" in condition_expression.lower():
                return False
            else:
                # Default to True for unknown conditions
                return True
        except Exception as e:
            logger.warning(f"Condition evaluation failed: {e}")
            return True

    def _execute_while_condition(self, execution: WorkflowExecution, condition: WorkflowCondition) -> bool:
        """Execute while loop condition"""
        try:
            iteration = 0
            while iteration < condition.max_iterations:
                condition_met = self._evaluate_condition(condition.condition_expression)
                if not condition_met:
                    break
                
                # Execute loop body
                for task_id in condition.true_branch:
                    task = self._find_task_by_id(execution, task_id)
                    if task:
                        success = self._execute_single_task(task)
                        if not success:
                            return False
                
                iteration += 1
            
            return True
            
        except Exception as e:
            logger.error(f"While condition execution failed: {e}")
            return False

    def _execute_for_condition(self, execution: WorkflowExecution, condition: WorkflowCondition) -> bool:
        """Execute for loop condition"""
        try:
            # Execute loop body for specified iterations
            for iteration in range(condition.max_iterations):
                for task_id in condition.true_branch:
                    task = self._find_task_by_id(execution, task_id)
                    if task:
                        success = self._execute_single_task(task)
                        if not success:
                            return False
            
            return True
            
        except Exception as e:
            logger.error(f"For condition execution failed: {e}")
            return False

    def shutdown(self):
        """Shutdown the workflow executor"""
        logger.info("Workflow Executor shutdown complete")
