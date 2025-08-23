#!/usr/bin/env python3
"""
Advanced Workflow Automation Engine
===================================

Enterprise-grade workflow automation with:
- Multi-agent task orchestration
- Conditional workflow branching
- Error handling and recovery
- Dynamic workflow generation
- Performance optimization
- Real-time monitoring

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Callable, Any, Union
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from .shared_enums import WorkflowStatus, TaskStatus, TaskPriority, WorkflowType


@dataclass
class WorkflowTask:
    """Individual workflow task"""

    task_id: str
    name: str
    description: str
    agent_id: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_duration: int = 60  # seconds
    actual_duration: Optional[int] = None
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    required_resources: List[str] = field(default_factory=list)
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowCondition:
    """Conditional workflow logic"""

    condition_id: str
    name: str
    condition_type: str  # "if", "while", "for", "switch"
    condition_expression: str
    true_branch: List[str]  # Task IDs to execute if true
    false_branch: List[str] = field(
        default_factory=list
    )  # Task IDs to execute if false
    loop_condition: Optional[str] = None  # For loop workflows
    max_iterations: int = 100  # Prevent infinite loops
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExecution:
    """Workflow execution instance"""

    execution_id: str
    workflow_id: str
    workflow_name: str
    status: WorkflowStatus = WorkflowStatus.CREATED
    tasks: List[WorkflowTask] = field(default_factory=list)
    conditions: List[WorkflowCondition] = field(default_factory=list)
    current_task_index: int = 0
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[str] = field(default_factory=list)
    execution_path: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_duration: Optional[int] = None
    error_count: int = 0
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentCapability:
    """Agent capability definition"""

    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    current_load: int = 0
    max_concurrent_tasks: int = 5
    performance_score: float = 1.0
    availability: bool = True
    last_heartbeat: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceRequirement:
    """Resource requirement definition"""

    resource_id: str
    resource_type: str  # "cpu", "memory", "storage", "network", "custom"
    required_amount: float
    unit: str
    priority: TaskPriority = TaskPriority.MEDIUM
    current_availability: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class AdvancedWorkflowAutomation:
    """
    Enterprise-grade advanced workflow automation engine

    Features:
    - Multi-agent task orchestration
    - Conditional workflow branching
    - Error handling and recovery
    - Dynamic workflow generation
    - Performance optimization
    - Real-time monitoring
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the workflow automation engine"""
        self.config_path = config_path or "workflow_config.json"
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.agents: Dict[str, AgentCapability] = {}
        self.resources: Dict[str, ResourceRequirement] = {}
        self.execution_thread = None
        self.running = False
        self.max_concurrent_executions = 10
        self.active_executions: Set[str] = set()

        # Load configuration
        self.config = self._load_configuration()

        # Initialize default resources
        self._initialize_default_resources()

        logger.info("Advanced Workflow Automation Engine initialized")

    def _load_configuration(self) -> Dict[str, Any]:
        """Load workflow automation configuration"""
        default_config = {
            "max_concurrent_executions": 10,
            "default_task_timeout": 300,  # 5 minutes
            "retry_delay_base": 5,  # seconds
            "max_retry_delay": 300,  # 5 minutes
            "heartbeat_interval": 30,  # seconds
            "resource_check_interval": 60,  # seconds
            "performance_thresholds": {
                "task_completion_rate": 0.95,
                "average_execution_time": 300,
                "error_rate": 0.05,
            },
        }

        try:
            if Path(self.config_path).exists():
                with open(self.config_path, "r") as f:
                    config_data = json.load(f)
                    default_config.update(config_data)
                    logger.info("Loaded workflow configuration")
            else:
                logger.info("Using default workflow configuration")
        except Exception as e:
            logger.warning(f"Failed to load configuration: {e}, using defaults")

        return default_config

    def _initialize_default_resources(self):
        """Initialize default system resources"""
        default_resources = {
            "cpu": ResourceRequirement(
                "cpu", "cpu", 100.0, "percent", TaskPriority.HIGH
            ),
            "memory": ResourceRequirement(
                "memory", "memory", 100.0, "percent", TaskPriority.HIGH
            ),
            "storage": ResourceRequirement(
                "storage", "storage", 100.0, "percent", TaskPriority.MEDIUM
            ),
            "network": ResourceRequirement(
                "network", "network", 100.0, "percent", TaskPriority.MEDIUM
            ),
        }

        for resource_id, resource in default_resources.items():
            self.resources[resource_id] = resource

        logger.info(f"Initialized {len(self.resources)} default resources")

    def register_agent(
        self, agent_id: str, capabilities: List[str], max_concurrent_tasks: int = 5
    ) -> bool:
        """Register an agent with the workflow engine"""
        try:
            agent = AgentCapability(
                agent_id=agent_id,
                capabilities=capabilities,
                max_concurrent_tasks=max_concurrent_tasks,
            )

            self.agents[agent_id] = agent
            logger.info(
                f"Registered agent {agent_id} with {len(capabilities)} capabilities"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            return False

    def create_workflow(
        self,
        workflow_id: str,
        name: str,
        workflow_type: WorkflowType,
        tasks: List[Dict[str, Any]],
        conditions: List[Dict[str, Any]] = None,
    ) -> bool:
        """Create a new workflow definition"""
        try:
            workflow = {
                "workflow_id": workflow_id,
                "name": name,
                "type": workflow_type,
                "tasks": tasks,
                "conditions": conditions or [],
                "created_at": datetime.now().isoformat(),
                "version": "1.0",
            }

            self.workflows[workflow_id] = workflow
            logger.info(f"Created workflow: {name} ({workflow_type.value})")
            return True

        except Exception as e:
            logger.error(f"Failed to create workflow {workflow_id}: {e}")
            return False

    def start_workflow_execution(
        self, workflow_id: str, input_data: Dict[str, Any] = None
    ) -> str:
        """Start execution of a workflow"""
        try:
            if workflow_id not in self.workflows:
                raise ValueError(f"Workflow {workflow_id} not found")

            if len(self.active_executions) >= self.max_concurrent_executions:
                raise RuntimeError("Maximum concurrent executions reached")

            workflow = self.workflows[workflow_id]

            # Create execution instance
            execution = WorkflowExecution(
                execution_id=f"exec_{uuid.uuid4().hex[:8]}",
                workflow_id=workflow_id,
                workflow_name=workflow["name"],
            )
            # Store input data in metadata for now
            execution.metadata["input_data"] = input_data or {}

            # Create tasks from workflow definition
            execution.tasks = self._create_tasks_from_definition(workflow["tasks"])

            # Create conditions from workflow definition
            execution.conditions = self._create_conditions_from_definition(
                workflow["conditions"]
            )

            # Store execution
            self.executions[execution.execution_id] = execution
            self.active_executions.add(execution.execution_id)

            # Start execution
            self._start_execution(execution)

            logger.info(f"Started workflow execution: {execution.execution_id}")
            return execution.execution_id

        except Exception as e:
            logger.error(f"Failed to start workflow execution: {e}")
            return ""

    def _create_tasks_from_definition(
        self, task_definitions: List[Dict[str, Any]]
    ) -> List[WorkflowTask]:
        """Create WorkflowTask objects from task definitions"""
        tasks = []

        for task_def in task_definitions:
            task = WorkflowTask(
                task_id=task_def.get("task_id", f"task_{uuid.uuid4().hex[:8]}"),
                name=task_def.get("name", "Unnamed Task"),
                description=task_def.get("description", ""),
                priority=TaskPriority(task_def.get("priority", "medium")),
                estimated_duration=task_def.get("estimated_duration", 60),
                dependencies=task_def.get("dependencies", []),
                required_resources=task_def.get("required_resources", []),
                input_data=task_def.get("input_data", {}),
            )
            tasks.append(task)

        return tasks

    def _create_conditions_from_definition(
        self, condition_definitions: List[Dict[str, Any]]
    ) -> List[WorkflowCondition]:
        """Create WorkflowCondition objects from condition definitions"""
        conditions = []

        for cond_def in condition_definitions:
            condition = WorkflowCondition(
                condition_id=cond_def.get(
                    "condition_id", f"cond_{uuid.uuid4().hex[:8]}"
                ),
                name=cond_def.get("name", "Unnamed Condition"),
                condition_type=cond_def.get("condition_type", "if"),
                condition_expression=cond_def.get("condition_expression", "True"),
                true_branch=cond_def.get("true_branch", []),
                false_branch=cond_def.get("false_branch", []),
                loop_condition=cond_def.get("loop_condition"),
                max_iterations=cond_def.get("max_iterations", 100),
            )
            conditions.append(condition)

        return conditions

    def _start_execution(self, execution: WorkflowExecution):
        """Start workflow execution"""
        try:
            execution.status = WorkflowStatus.PLANNING
            execution.start_time = datetime.now()

            # Plan execution
            self._plan_execution(execution)

            # Start task execution
            execution.status = WorkflowStatus.RUNNING
            self._execute_tasks(execution)

        except Exception as e:
            logger.error(f"Failed to start execution {execution.execution_id}: {e}")
            execution.status = WorkflowStatus.FAILED

    def _plan_execution(self, execution: WorkflowExecution):
        """Plan the workflow execution"""
        try:
            logger.info(f"Planning execution {execution.execution_id}")

            # Analyze dependencies and create execution plan
            execution_plan = self._create_execution_plan(execution)
            execution.execution_path = execution_plan

            # Validate resource requirements
            if not self._validate_resource_requirements(execution):
                raise RuntimeError("Insufficient resources for workflow execution")

            execution.status = WorkflowStatus.READY
            logger.info(f"Execution {execution.execution_id} planned successfully")

        except Exception as e:
            logger.error(f"Failed to plan execution {execution.execution_id}: {e}")
            raise

    def _create_execution_plan(self, execution: WorkflowExecution) -> List[str]:
        """Create execution plan based on workflow type and dependencies"""
        workflow = self.workflows[execution.workflow_id]
        workflow_type = workflow["type"]

        if workflow_type == WorkflowType.SEQUENTIAL:
            return self._plan_sequential_execution(execution)
        elif workflow_type == WorkflowType.PARALLEL:
            return self._plan_parallel_execution(execution)
        elif workflow_type == WorkflowType.CONDITIONAL:
            return self._plan_conditional_execution(execution)
        elif workflow_type == WorkflowType.LOOP:
            return self._plan_loop_execution(execution)
        elif workflow_type == WorkflowType.PARALLEL_BATCH:
            return self._plan_parallel_batch_execution(execution)
        elif workflow_type == WorkflowType.PIPELINE:
            return self._plan_pipeline_execution(execution)
        else:
            # Default to sequential
            return self._plan_sequential_execution(execution)

    def _plan_sequential_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan sequential task execution"""
        # Simple sequential execution - tasks in order
        return [task.task_id for task in execution.tasks]

    def _plan_parallel_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan parallel task execution"""
        # All tasks can run in parallel (no dependencies)
        return [task.task_id for task in execution.tasks]

    def _plan_conditional_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan conditional task execution"""
        # For conditional workflows, we'll evaluate conditions at runtime
        # Return all possible task IDs
        all_task_ids = set()
        for condition in execution.conditions:
            all_task_ids.update(condition.true_branch)
            all_task_ids.update(condition.false_branch)

        return list(all_task_ids)

    def _plan_loop_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan loop task execution"""
        # For loop workflows, return the loop body tasks
        loop_tasks = []
        for condition in execution.conditions:
            if condition.condition_type == "for" or condition.condition_type == "while":
                loop_tasks.extend(condition.true_branch)

        return loop_tasks if loop_tasks else [task.task_id for task in execution.tasks]

    def _plan_parallel_batch_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan parallel batch execution"""
        # Group tasks into batches for parallel execution
        batch_size = 3  # Default batch size
        all_tasks = [task.task_id for task in execution.tasks]

        batches = []
        for i in range(0, len(all_tasks), batch_size):
            batch = all_tasks[i : i + batch_size]
            batches.append(batch)

        # Flatten batches into execution plan
        execution_plan = []
        for batch in batches:
            execution_plan.extend(batch)

        return execution_plan

    def _plan_pipeline_execution(self, execution: WorkflowExecution) -> List[str]:
        """Plan pipeline execution"""
        # Pipeline execution - tasks form a processing chain
        # For now, use sequential order
        return [task.task_id for task in execution.tasks]

    def _validate_resource_requirements(self, execution: WorkflowExecution) -> bool:
        """Validate that required resources are available"""
        try:
            for task in execution.tasks:
                for resource_id in task.required_resources:
                    if resource_id not in self.resources:
                        logger.warning(
                            f"Resource {resource_id} not found for task {task.task_id}"
                        )
                        continue

                    resource = self.resources[resource_id]
                    if resource.current_availability < resource.required_amount:
                        logger.warning(
                            f"Insufficient {resource_id} for task {task.task_id}"
                        )
                        return False

            return True

        except Exception as e:
            logger.error(f"Failed to validate resource requirements: {e}")
            return False

    def _execute_tasks(self, execution: WorkflowExecution):
        """Execute workflow tasks"""
        try:
            workflow = self.workflows[execution.workflow_id]
            workflow_type = workflow["type"]

            if workflow_type == WorkflowType.SEQUENTIAL:
                self._execute_sequential(execution)
            elif workflow_type == WorkflowType.PARALLEL:
                self._execute_parallel(execution)
            elif workflow_type == WorkflowType.CONDITIONAL:
                self._execute_conditional(execution)
            elif workflow_type == WorkflowType.LOOP:
                self._execute_loop(execution)
            elif workflow_type == WorkflowType.PARALLEL_BATCH:
                self._execute_parallel_batch(execution)
            elif workflow_type == WorkflowType.PIPELINE:
                self._execute_pipeline(execution)
            else:
                self._execute_sequential(execution)

        except Exception as e:
            logger.error(f"Failed to execute tasks for {execution.execution_id}: {e}")
            execution.status = WorkflowStatus.FAILED

    def _execute_sequential(self, execution: WorkflowExecution):
        """Execute tasks sequentially"""
        try:
            for task_id in execution.execution_path:
                task = self._find_task_by_id(execution, task_id)
                if not task:
                    continue

                # Execute task
                success = self._execute_single_task(execution, task)
                if not success:
                    execution.status = WorkflowStatus.FAILED
                    return

                execution.completed_tasks.append(task_id)

            # All tasks completed
            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = datetime.now()
            if execution.start_time:
                execution.total_duration = int(
                    (execution.end_time - execution.start_time).total_seconds()
                )

            logger.info(f"Sequential execution {execution.execution_id} completed")

        except Exception as e:
            logger.error(f"Failed to execute sequential workflow: {e}")
            execution.status = WorkflowStatus.FAILED

    def _execute_parallel(self, execution: WorkflowExecution):
        """Execute tasks in parallel"""
        try:
            # Create tasks for parallel execution
            tasks_to_execute = []
            for task_id in execution.execution_path:
                task = self._find_task_by_id(execution, task_id)
                if task:
                    tasks_to_execute.append(task)

            # Execute all tasks in parallel
            with ThreadPoolExecutor(max_workers=len(tasks_to_execute)) as executor:
                future_to_task = {
                    executor.submit(self._execute_single_task, execution, task): task
                    for task in tasks_to_execute
                }

                for future in as_completed(future_to_task):
                    task = future_to_task[future]
                    try:
                        success = future.result()
                        if success:
                            execution.completed_tasks.append(task.task_id)
                        else:
                            execution.failed_tasks.append(task.task_id)
                    except Exception as e:
                        logger.error(f"Task {task.task_id} failed: {e}")
                        execution.failed_tasks.append(task.task_id)

            # Check execution status
            if execution.failed_tasks:
                execution.status = WorkflowStatus.FAILED
            else:
                execution.status = WorkflowStatus.COMPLETED
                execution.end_time = datetime.now()
                if execution.start_time:
                    execution.total_duration = int(
                        (execution.end_time - execution.start_time).total_seconds()
                    )

            logger.info(f"Parallel execution {execution.execution_id} completed")

        except Exception as e:
            logger.error(f"Failed to execute parallel workflow: {e}")
            execution.status = WorkflowStatus.FAILED

    def _execute_conditional(self, execution: WorkflowExecution):
        """Execute conditional workflow"""
        try:
            for condition in execution.conditions:
                # Evaluate condition
                condition_result = self._evaluate_condition(condition, execution)

                # Execute appropriate branch
                if condition_result:
                    task_ids = condition.true_branch
                else:
                    task_ids = condition.false_branch

                # Execute tasks in the selected branch
                for task_id in task_ids:
                    task = self._find_task_by_id(execution, task_id)
                    if task:
                        success = self._execute_single_task(execution, task)
                        if success:
                            execution.completed_tasks.append(task_id)
                        else:
                            execution.failed_tasks.append(task_id)

            # Set final status
            if execution.failed_tasks:
                execution.status = WorkflowStatus.FAILED
            else:
                execution.status = WorkflowStatus.COMPLETED
                execution.end_time = datetime.now()
                if execution.start_time:
                    execution.total_duration = int(
                        (execution.end_time - execution.start_time).total_seconds()
                    )

            logger.info(f"Conditional execution {execution.execution_id} completed")

        except Exception as e:
            logger.error(f"Failed to execute conditional workflow: {e}")
            execution.status = WorkflowStatus.FAILED

    def _evaluate_condition(
        self, condition: WorkflowCondition, execution: WorkflowExecution
    ) -> bool:
        """Evaluate a workflow condition"""
        try:
            # Simple condition evaluation
            # In a real implementation, this would use a proper expression evaluator
            if condition.condition_expression.lower() == "true":
                return True
            elif condition.condition_expression.lower() == "false":
                return False
            else:
                # Default to True for now
                return True

        except Exception as e:
            logger.error(f"Failed to evaluate condition {condition.condition_id}: {e}")
            return False

    def _execute_loop(self, execution: WorkflowExecution):
        """Execute loop workflow"""
        try:
            for condition in execution.conditions:
                if condition.condition_type in ["for", "while"]:
                    iteration_count = 0

                    while iteration_count < condition.max_iterations:
                        # Evaluate loop condition
                        should_continue = self._evaluate_condition(condition, execution)
                        if not should_continue:
                            break

                        # Execute loop body
                        for task_id in condition.true_branch:
                            task = self._find_task_by_id(execution, task_id)
                            if task:
                                success = self._execute_single_task(execution, task)
                                if not success:
                                    execution.failed_tasks.append(task_id)

                        iteration_count += 1

                        # Check if we should break the loop
                        if execution.failed_tasks:
                            break

            # Set final status
            if execution.failed_tasks:
                execution.status = WorkflowStatus.FAILED
            else:
                execution.status = WorkflowStatus.COMPLETED
                execution.end_time = datetime.now()
                if execution.start_time:
                    execution.total_duration = int(
                        (execution.end_time - execution.start_time).total_seconds()
                    )

            logger.info(f"Loop execution {execution.execution_id} completed")

        except Exception as e:
            logger.error(f"Failed to execute loop workflow: {e}")
            execution.status = WorkflowStatus.FAILED

    def _execute_parallel_batch(self, execution: WorkflowExecution):
        """Execute parallel batch workflow"""
        try:
            # Group tasks into batches
            batch_size = 3
            all_tasks = [
                self._find_task_by_id(execution, task_id)
                for task_id in execution.execution_path
            ]
            all_tasks = [task for task in all_tasks if task]  # Remove None tasks

            batches = []
            for i in range(0, len(all_tasks), batch_size):
                batch = all_tasks[i : i + batch_size]
                batches.append(batch)

            # Execute batches sequentially, but tasks within each batch in parallel
            for batch in batches:
                with ThreadPoolExecutor(max_workers=len(batch)) as executor:
                    future_to_task = {
                        executor.submit(
                            self._execute_single_task, execution, task
                        ): task
                        for task in batch
                    }

                    for future in as_completed(future_to_task):
                        task = future_to_task[future]
                        try:
                            success = future.result()
                            if success:
                                execution.completed_tasks.append(task.task_id)
                            else:
                                execution.failed_tasks.append(task.task_id)
                        except Exception as e:
                            logger.error(f"Task {task.task_id} failed: {e}")
                            execution.failed_tasks.append(task.task_id)

                # Check if we should continue with next batch
                if execution.failed_tasks:
                    break

            # Set final status
            if execution.failed_tasks:
                execution.status = WorkflowStatus.FAILED
            else:
                execution.status = WorkflowStatus.COMPLETED
                execution.end_time = datetime.now()
                if execution.start_time:
                    execution.total_duration = int(
                        (execution.end_time - execution.start_time).total_seconds()
                    )

            logger.info(f"Parallel batch execution {execution.execution_id} completed")

        except Exception as e:
            logger.error(f"Failed to execute parallel batch workflow: {e}")
            execution.status = WorkflowStatus.FAILED

    def _execute_pipeline(self, execution: WorkflowExecution):
        """Execute pipeline workflow"""
        try:
            # Pipeline execution - tasks form a processing chain
            # Each task's output becomes the next task's input
            current_input = execution.input_data

            for task_id in execution.execution_path:
                task = self._find_task_by_id(execution, task_id)
                if not task:
                    continue

                # Set task input
                task.input_data = current_input

                # Execute task
                success = self._execute_single_task(execution, task)
                if success:
                    execution.completed_tasks.append(task_id)
                    # Update input for next task
                    current_input = task.output_data
                else:
                    execution.failed_tasks.append(task_id)
                    break

            # Set final status
            if execution.failed_tasks:
                execution.status = WorkflowStatus.FAILED
            else:
                execution.status = WorkflowStatus.COMPLETED
                execution.end_time = datetime.now()
                if execution.start_time:
                    execution.total_duration = int(
                        (execution.end_time - execution.start_time).total_seconds()
                    )

            logger.info(f"Pipeline execution {execution.execution_id} completed")

        except Exception as e:
            logger.error(f"Failed to execute pipeline workflow: {e}")
            execution.status = WorkflowStatus.FAILED

    def _execute_single_task(
        self, execution: WorkflowExecution, task: WorkflowTask
    ) -> bool:
        """Execute a single workflow task"""
        try:
            logger.info(f"Executing task: {task.name} ({task.task_id})")

            # Update task status
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()

            # Assign agent if not already assigned
            if not task.agent_id:
                assigned_agent = self._assign_agent_to_task(task)
                if assigned_agent:
                    task.agent_id = assigned_agent
                else:
                    logger.error(f"No available agent for task {task.task_id}")
                    task.status = TaskStatus.FAILED
                    return False

            # Simulate task execution
            # In a real implementation, this would send the task to the assigned agent
            success = self._simulate_task_execution(task)

            if success:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                if task.started_at:
                    task.actual_duration = int(
                        (task.completed_at - task.started_at).total_seconds()
                    )

                logger.info(f"Task {task.name} completed successfully")
                return True
            else:
                task.status = TaskStatus.FAILED
                task.error_message = "Task execution failed"

                # Handle retry logic
                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    task.status = TaskStatus.RETRYING
                    logger.info(
                        f"Task {task.name} will be retried ({task.retry_count}/{task.max_retries})"
                    )

                    # Schedule retry
                    asyncio.create_task(self._schedule_task_retry(execution, task))
                    return True  # Return True to prevent workflow failure
                else:
                    logger.error(
                        f"Task {task.name} failed after {task.max_retries} retries"
                    )
                    return False

        except Exception as e:
            logger.error(f"Failed to execute task {task.task_id}: {e}")
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            return False

    def _assign_agent_to_task(self, task: WorkflowTask) -> Optional[str]:
        """Assign an available agent to a task"""
        try:
            available_agents = []

            for agent_id, agent in self.agents.items():
                if (
                    agent.availability
                    and agent.current_load < agent.max_concurrent_tasks
                    and self._agent_can_handle_task(agent, task)
                ):
                    available_agents.append((agent_id, agent))

            if not available_agents:
                return None

            # Select best agent based on performance score and current load
            best_agent = min(
                available_agents,
                key=lambda x: (x[1].current_load, -x[1].performance_score),
            )

            # Update agent load
            best_agent[1].current_load += 1

            return best_agent[0]

        except Exception as e:
            logger.error(f"Failed to assign agent to task: {e}")
            return None

    def _agent_can_handle_task(
        self, agent: AgentCapability, task: WorkflowTask
    ) -> bool:
        """Check if an agent can handle a specific task"""
        # Simple capability check - in real implementation, this would be more sophisticated
        return True  # For now, assume all agents can handle all tasks

    def _simulate_task_execution(self, task: WorkflowTask) -> bool:
        """Simulate task execution for demo purposes"""
        try:
            # Simulate work
            time.sleep(1)  # Simulate 1 second of work

            # Generate some output data
            task.output_data = {
                "result": "success",
                "timestamp": datetime.now().isoformat(),
                "task_id": task.task_id,
                "execution_time": 1.0,
            }

            # Simulate occasional failures for testing
            if task.name.lower().contains("fail"):
                return False

            return True

        except Exception as e:
            logger.error(f"Task execution simulation failed: {e}")
            return False

    async def _schedule_task_retry(
        self, execution: WorkflowExecution, task: WorkflowTask, delay_seconds: int = 5
    ):
        """Schedule a task retry"""
        await asyncio.sleep(delay_seconds)

        # Reset task status
        task.status = TaskStatus.PENDING
        task.started_at = None
        task.completed_at = None

        # Re-execute task
        success = self._execute_single_task(execution, task)
        if not success:
            execution.failed_tasks.append(task.task_id)

    def _find_task_by_id(
        self, execution: WorkflowExecution, task_id: str
    ) -> Optional[WorkflowTask]:
        """Find a task by ID in an execution"""
        for task in execution.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a workflow execution"""
        try:
            if execution_id not in self.executions:
                return None

            execution = self.executions[execution_id]

            status = {
                "execution_id": execution.execution_id,
                "workflow_name": execution.workflow_name,
                "status": execution.status.value,
                "progress": {
                    "total_tasks": len(execution.tasks),
                    "completed_tasks": len(execution.completed_tasks),
                    "failed_tasks": len(execution.failed_tasks),
                    "pending_tasks": len(execution.tasks)
                    - len(execution.completed_tasks)
                    - len(execution.failed_tasks),
                },
                "timing": {
                    "start_time": execution.start_time.isoformat()
                    if execution.start_time
                    else None,
                    "end_time": execution.end_time.isoformat()
                    if execution.end_time
                    else None,
                    "total_duration": execution.total_duration,
                },
                "errors": execution.error_count,
                "retries": execution.retry_count,
            }

            return status

        except Exception as e:
            logger.error(f"Failed to get execution status: {e}")
            return None

    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get a summary of all workflows and executions"""
        try:
            summary = {
                "total_workflows": len(self.workflows),
                "total_executions": len(self.executions),
                "active_executions": len(self.active_executions),
                "execution_status_counts": {},
                "recent_executions": [],
                "agent_summary": {
                    "total_agents": len(self.agents),
                    "available_agents": len(
                        [a for a in self.agents.values() if a.availability]
                    ),
                    "total_capabilities": sum(
                        len(a.capabilities) for a in self.agents.values()
                    ),
                },
                "resource_summary": {
                    "total_resources": len(self.resources),
                    "resource_types": list(
                        set(r.resource_type for r in self.resources.values())
                    ),
                },
            }

            # Count execution statuses
            for execution in self.executions.values():
                status = execution.status.value
                summary["execution_status_counts"][status] = (
                    summary["execution_status_counts"].get(status, 0) + 1
                )

            # Get recent executions
            recent_executions = sorted(
                self.executions.values(),
                key=lambda x: x.start_time or datetime.min,
                reverse=True,
            )[:5]

            summary["recent_executions"] = [
                {
                    "execution_id": e.execution_id,
                    "workflow_name": e.workflow_name,
                    "status": e.status.value,
                    "start_time": e.start_time.isoformat() if e.start_time else None,
                }
                for e in recent_executions
            ]

            return summary

        except Exception as e:
            logger.error(f"Failed to get workflow summary: {e}")
            return {"error": str(e)}

    def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running workflow execution"""
        try:
            if execution_id not in self.executions:
                return False

            execution = self.executions[execution_id]

            if execution.status in [
                WorkflowStatus.COMPLETED,
                WorkflowStatus.FAILED,
                WorkflowStatus.CANCELLED,
            ]:
                return False

            # Cancel execution
            execution.status = WorkflowStatus.CANCELLED
            execution.end_time = datetime.now()

            # Cancel all running tasks
            for task in execution.tasks:
                if task.status == TaskStatus.RUNNING:
                    task.status = TaskStatus.CANCELLED

            # Remove from active executions
            self.active_executions.discard(execution_id)

            logger.info(f"Cancelled execution {execution_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to cancel execution {execution_id}: {e}")
            return False

    def shutdown(self):
        """Shutdown the workflow automation engine"""
        try:
            self.running = False

            # Cancel all active executions
            for execution_id in list(self.active_executions):
                self.cancel_execution(execution_id)

            logger.info("Advanced Workflow Automation Engine shutdown complete")

        except Exception as e:
            logger.error(f"Failed to shutdown workflow engine: {e}")


def main():
    """Main function for standalone testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Advanced Workflow Automation Engine")
    parser.add_argument("--demo", action="store_true", help="Run demo scenario")
    parser.add_argument(
        "--workflow", type=str, help="Create and run specific workflow type"
    )

    args = parser.parse_args()

    engine = AdvancedWorkflowAutomation()

    try:
        if args.demo:
            print("🚀 Running Advanced Workflow Automation Demo...")

            # Register some demo agents
            engine.register_agent("agent_1", ["task_execution", "data_processing"], 3)
            engine.register_agent("agent_2", ["task_execution", "validation"], 2)
            engine.register_agent("agent_3", ["task_execution", "reporting"], 2)

            # Create demo workflows
            sequential_tasks = [
                {
                    "task_id": "task_1",
                    "name": "Data Collection",
                    "description": "Collect input data",
                },
                {
                    "task_id": "task_2",
                    "name": "Data Processing",
                    "description": "Process collected data",
                },
                {
                    "task_id": "task_3",
                    "name": "Data Validation",
                    "description": "Validate processed data",
                },
                {
                    "task_id": "task_4",
                    "name": "Report Generation",
                    "description": "Generate final report",
                },
            ]

            engine.create_workflow(
                "demo_sequential",
                "Demo Sequential Workflow",
                WorkflowType.SEQUENTIAL,
                sequential_tasks,
            )

            # Start execution
            execution_id = engine.start_workflow_execution(
                "demo_sequential", {"demo": True}
            )

            if execution_id:
                print(f"✅ Started workflow execution: {execution_id}")

                # Wait for completion
                import time

                while True:
                    status = engine.get_execution_status(execution_id)
                    if status and status["status"] in [
                        "completed",
                        "failed",
                        "cancelled",
                    ]:
                        break
                    time.sleep(1)

                print(f"📊 Final Status: {status}")
            else:
                print("❌ Failed to start workflow execution")

        elif args.workflow:
            print(f"🔧 Creating and running {args.workflow} workflow...")

            # Create workflow based on type
            if args.workflow == "parallel":
                tasks = [
                    {
                        "task_id": "p1",
                        "name": "Parallel Task 1",
                        "description": "First parallel task",
                    },
                    {
                        "task_id": "p2",
                        "name": "Parallel Task 2",
                        "description": "Second parallel task",
                    },
                    {
                        "task_id": "p3",
                        "name": "Parallel Task 3",
                        "description": "Third parallel task",
                    },
                ]

                engine.create_workflow(
                    "demo_parallel",
                    "Demo Parallel Workflow",
                    WorkflowType.PARALLEL,
                    tasks,
                )

                execution_id = engine.start_workflow_execution("demo_parallel")
                print(f"✅ Started parallel workflow: {execution_id}")

            else:
                print(f"❌ Unknown workflow type: {args.workflow}")

        else:
            print("🔧 Advanced Workflow Automation Engine ready")
            print(
                "Use --demo to run demo scenario or --workflow <type> to test specific workflow types"
            )

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        traceback.print_exc()
        exit(1)

    finally:
        engine.shutdown()


if __name__ == "__main__":
    main()
