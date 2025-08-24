#!/usr/bin/env python3
"""
Workflow Planner - V2 Core Workflow Planning and Optimization

This module handles workflow execution planning and optimization.
Follows V2 standards: ≤200 lines, single responsibility, clean OOP design.

Author: Agent-4 (Quality Assurance)
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Set
from datetime import datetime

try:
    from .workflow_types import (
        WorkflowExecution, WorkflowTask, WorkflowCondition, 
        WorkflowType, TaskPriority, AgentCapability
    )
except ImportError:
    # Fallback for standalone usage
    from workflow_types import (
        WorkflowExecution, WorkflowTask, WorkflowCondition, 
        WorkflowType, TaskPriority, AgentCapability
    )

logger = logging.getLogger(__name__)


class WorkflowPlanner:
    """
    Workflow execution planning and optimization engine
    
    Responsibilities:
    - Execution planning and scheduling
    - Resource optimization
    - Agent assignment optimization
    - Performance optimization
    """

    def __init__(self):
        """Initialize the workflow planner"""
        self.optimization_strategies = {
            "performance": self._optimize_for_performance,
            "resource_efficiency": self._optimize_for_resource_efficiency,
            "cost": self._optimize_for_cost,
            "latency": self._optimize_for_latency
        }
        logger.info("Workflow Planner initialized")

    def plan_execution(self, execution: WorkflowExecution, strategy: str = "performance") -> List[str]:
        """Plan workflow execution based on strategy"""
        try:
            if strategy in self.optimization_strategies:
                return self.optimization_strategies[strategy](execution)
            else:
                logger.warning(f"Unknown optimization strategy: {strategy}, using default")
                return self._plan_sequential_execution(execution)
                
        except Exception as e:
            logger.error(f"Execution planning failed: {e}")
            return self._plan_sequential_execution(execution)

    def _plan_sequential_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan sequential task execution"""
        plan = []
        completed = set()
        
        # Simple dependency-based planning
        for task in execution.tasks:
            if all(dep in completed for dep in task.dependencies):
                plan.append(task.task_id)
                completed.add(task.task_id)
        
        return plan

    def _plan_parallel_execution(self, execution: WorkflowExecution) -> List[List[str]]:
        """Plan parallel task execution"""
        parallel_groups = []
        completed = set()
        current_group = []
        
        for task in execution.tasks:
            if all(dep in completed for dep in task.dependencies):
                current_group.append(task.task_id)
                completed.add(task.task_id)
                
                # Start new group if current is large enough
                if len(current_group) >= 3:
                    parallel_groups.append(current_group)
                    current_group = []
        
        # Add remaining tasks
        if current_group:
            parallel_groups.append(current_group)
        
        return parallel_groups

    def _plan_conditional_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan conditional workflow execution"""
        plan = []
        
        # Process conditions first
        for condition in execution.conditions:
            if condition.condition_type == "if":
                # Add condition evaluation task
                plan.append(f"eval_{condition.condition_id}")
                
                # Add conditional tasks
                if condition.true_branch:
                    plan.extend(condition.true_branch)
                if condition.false_branch:
                    plan.extend(condition.false_branch)
        
        # Add remaining tasks
        for task in execution.tasks:
            if task.task_id not in plan:
                plan.append(task.task_id)
        
        return plan

    def _plan_loop_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan loop workflow execution"""
        plan = []
        
        for condition in execution.conditions:
            if condition.condition_type in ["while", "for"]:
                # Add loop initialization
                plan.append(f"init_{condition.condition_id}")
                
                # Add loop body tasks
                plan.extend(condition.true_branch)
                
                # Add loop control
                plan.append(f"control_{condition.condition_id}")
        
        # Add remaining tasks
        for task in execution.tasks:
            if task.task_id not in plan:
                plan.append(task.task_id)
        
        return plan

    def _plan_pipeline_execution(self, execution: WorkflowExecution) -> List[List[str]]:
        """Plan pipeline workflow execution"""
        pipeline_stages = []
        current_stage = []
        
        # Group tasks by dependencies
        for task in execution.tasks:
            if not task.dependencies:
                current_stage.append(task.task_id)
            else:
                # Start new stage
                if current_stage:
                    pipeline_stages.append(current_stage)
                    current_stage = []
                current_stage.append(task.task_id)
        
        # Add final stage
        if current_stage:
            pipeline_stages.append(current_stage)
        
        return pipeline_stages

    def _plan_parallel_batch_execution(self, execution: WorkflowExecution) -> List[List[str]]:
        """Plan parallel batch execution"""
        batches = []
        current_batch = []
        max_batch_size = 5
        
        for task in execution.tasks:
            current_batch.append(task.task_id)
            
            if len(current_batch) >= max_batch_size:
                batches.append(current_batch)
                current_batch = []
        
        # Add remaining tasks
        if current_batch:
            batches.append(current_batch)
        
        return batches

    def _optimize_for_performance(self, execution: WorkflowExecution) -> List[str]:
        """Optimize execution for maximum performance"""
        try:
            # Sort tasks by priority and estimated duration
            sorted_tasks = sorted(
                execution.tasks,
                key=lambda t: (t.priority.value, t.estimated_duration),
                reverse=True
            )
            
            plan = []
            completed = set()
            
            for task in sorted_tasks:
                if all(dep in completed for dep in task.dependencies):
                    plan.append(task.task_id)
                    completed.add(task.task_id)
            
            return plan
            
        except Exception as e:
            logger.error(f"Performance optimization failed: {e}")
            return self._plan_sequential_execution(execution)

    def _optimize_for_resource_efficiency(self, execution: WorkflowExecution) -> List[str]:
        """Optimize execution for resource efficiency"""
        try:
            # Group tasks by resource requirements
            resource_groups = {}
            
            for task in execution.tasks:
                for resource in task.required_resources:
                    if resource not in resource_groups:
                        resource_groups[resource] = []
                    resource_groups[resource].append(task.task_id)
            
            # Execute resource groups sequentially
            plan = []
            for resource, tasks in resource_groups.items():
                plan.extend(tasks)
            
            return plan
            
        except Exception as e:
            logger.error(f"Resource efficiency optimization failed: {e}")
            return self._plan_sequential_execution(execution)

    def _optimize_for_cost(self, execution: WorkflowExecution) -> List[str]:
        """Optimize execution for minimum cost"""
        try:
            # Sort tasks by estimated duration (shorter tasks first)
            sorted_tasks = sorted(
                execution.tasks,
                key=lambda t: t.estimated_duration
            )
            
            plan = []
            completed = set()
            
            for task in sorted_tasks:
                if all(dep in completed for dep in task.dependencies):
                    plan.append(task.task_id)
                    completed.add(task.task_id)
            
            return plan
            
        except Exception as e:
            logger.error(f"Cost optimization failed: {e}")
            return self._plan_sequential_execution(execution)

    def _optimize_for_latency(self, execution: WorkflowExecution) -> List[str]:
        """Optimize execution for minimum latency"""
        try:
            # Sort tasks by dependencies (fewer dependencies first)
            sorted_tasks = sorted(
                execution.tasks,
                key=lambda t: len(t.dependencies)
            )
            
            plan = []
            completed = set()
            
            for task in sorted_tasks:
                if all(dep in completed for dep in task.dependencies):
                    plan.append(task.task_id)
                    completed.add(task.task_id)
            
            return plan
            
        except Exception as e:
            logger.error(f"Latency optimization failed: {e}")
            return self._plan_sequential_execution(execution)

    def validate_execution_plan(self, execution: WorkflowExecution, plan: List[str]) -> bool:
        """Validate that execution plan is feasible"""
        try:
            # Check that all tasks are included
            planned_tasks = set(plan)
            execution_tasks = {task.task_id for task in execution.tasks}
            
            if planned_tasks != execution_tasks:
                logger.error("Execution plan missing tasks")
                return False
            
            # Check dependencies
            completed = set()
            for task_id in plan:
                task = self._find_task_by_id(execution, task_id)
                if task and not all(dep in completed for dep in task.dependencies):
                    logger.error(f"Task {task_id} dependencies not satisfied")
                    return False
                completed.add(task_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Execution plan validation failed: {e}")
            return False

    def _find_task_by_id(self, execution: WorkflowExecution, task_id: str) -> Optional[WorkflowTask]:
        """Find a task by its ID in an execution"""
        for task in execution.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_planning_metrics(self, execution: WorkflowExecution, plan: List[str]) -> Dict[str, Any]:
        """Get metrics about the execution plan"""
        try:
            total_tasks = len(execution.tasks)
            planned_tasks = len(plan)
            
            # Calculate estimated duration
            estimated_duration = sum(
                task.estimated_duration 
                for task in execution.tasks 
                if task.task_id in plan
            )
            
            # Calculate resource requirements
            total_resources = set()
            for task in execution.tasks:
                total_resources.update(task.required_resources)
            
            return {
                "total_tasks": total_tasks,
                "planned_tasks": planned_tasks,
                "planning_efficiency": planned_tasks / total_tasks if total_tasks > 0 else 0,
                "estimated_duration": estimated_duration,
                "total_resources": len(total_resources),
                "plan_complexity": len(plan)
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate planning metrics: {e}")
            return {}
