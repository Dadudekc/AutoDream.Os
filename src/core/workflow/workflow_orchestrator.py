#!/usr/bin/env python3
"""
Workflow Orchestrator - V2 Core Workflow Orchestration

This module handles workflow lifecycle management and coordination.
Follows V2 standards: ≤200 lines, single responsibility, clean OOP design.

Author: Agent-4 (Quality Assurance)
License: MIT
"""

import json
import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from .workflow_types import (
        WorkflowStatus, WorkflowExecution, WorkflowTask, 
        WorkflowCondition, AgentCapability, ResourceRequirement
    )
except ImportError:
    # Fallback for standalone usage
    from workflow_types import (
        WorkflowStatus, WorkflowExecution, WorkflowTask, 
        WorkflowCondition, AgentCapability, ResourceRequirement
    )

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """
    Main workflow orchestration and lifecycle management
    
    Responsibilities:
    - Workflow creation and management
    - Agent registration and coordination
    - Resource management and allocation
    - Configuration management
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the workflow orchestrator"""
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

        logger.info("Workflow Orchestrator initialized")

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
        try:
            from .workflow_types import TaskPriority
        except ImportError:
            # Fallback for standalone usage
            from workflow_types import TaskPriority
        
        default_resources = {
            "cpu": ResourceRequirement(
                "cpu", "cpu", 100.0, "percent", TaskPriority.HIGH
            ),
            "memory": ResourceRequirement(
                "memory", "memory", 100.0, "percent", TaskPriority.HIGH
            ),
            "storage": ResourceRequirement(
                "storage", "storage", 100.0, "gb", TaskPriority.MEDIUM
            ),
            "network": ResourceRequirement(
                "network", "network", 100.0, "mbps", TaskPriority.MEDIUM
            ),
        }

        self.resources.update(default_resources)
        logger.info("Default resources initialized")

    def register_agent(
        self, 
        agent_id: str, 
        capabilities: List[str], 
        max_concurrent_tasks: int = 5,
        performance_score: float = 1.0
    ) -> bool:
        """Register an agent with the workflow system"""
        try:
            agent = AgentCapability(
                agent_id=agent_id,
                capabilities=capabilities,
                max_concurrent_tasks=max_concurrent_tasks,
                performance_score=performance_score
            )
            self.agents[agent_id] = agent
            logger.info(f"Agent {agent_id} registered with capabilities: {capabilities}")
            return True
        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            return False

    def create_workflow(
        self, 
        workflow_id: str, 
        name: str, 
        description: str,
        task_definitions: List[Dict[str, Any]],
        condition_definitions: List[Dict[str, Any]] = None
    ) -> bool:
        """Create a new workflow definition"""
        try:
            workflow = {
                "workflow_id": workflow_id,
                "name": name,
                "description": description,
                "task_definitions": task_definitions,
                "condition_definitions": condition_definitions or [],
                "created_at": str(Path().cwd()),
                "status": "active"
            }
            
            self.workflows[workflow_id] = workflow
            logger.info(f"Workflow {workflow_id} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create workflow {workflow_id}: {e}")
            return False

    def start_workflow_execution(self, workflow_id: str) -> Optional[str]:
        """Start execution of a workflow"""
        try:
            if workflow_id not in self.workflows:
                logger.error(f"Workflow {workflow_id} not found")
                return None

            if len(self.active_executions) >= self.max_concurrent_executions:
                logger.warning("Maximum concurrent executions reached")
                return None

            # Create execution instance
            execution = WorkflowExecution(
                execution_id=f"exec_{workflow_id}_{len(self.executions)}",
                workflow_id=workflow_id,
                workflow_name=self.workflows[workflow_id]["name"]
            )

            # Create tasks and conditions
            execution.tasks = self._create_tasks_from_definition(
                self.workflows[workflow_id]["task_definitions"]
            )
            
            if self.workflows[workflow_id]["condition_definitions"]:
                execution.conditions = self._create_conditions_from_definition(
                    self.workflows[workflow_id]["condition_definitions"]
                )

            # Store execution
            self.executions[execution.execution_id] = execution
            self.active_executions.add(execution.execution_id)

            logger.info(f"Workflow execution {execution.execution_id} started")
            return execution.execution_id

        except Exception as e:
            logger.error(f"Failed to start workflow execution: {e}")
            return None

    def _create_tasks_from_definition(self, task_definitions: List[Dict[str, Any]]) -> List[WorkflowTask]:
        """Create workflow tasks from definition"""
        tasks = []
        for task_def in task_definitions:
            task = WorkflowTask(**task_def)
            tasks.append(task)
        return tasks

    def _create_conditions_from_definition(self, condition_definitions: List[Dict[str, Any]]) -> List[WorkflowCondition]:
        """Create workflow conditions from definition"""
        conditions = []
        for cond_def in condition_definitions:
            condition = WorkflowCondition(**cond_def)
            conditions.append(condition)
        return conditions

    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a workflow execution"""
        if execution_id not in self.executions:
            return None

        execution = self.executions[execution_id]
        return {
            "execution_id": execution.execution_id,
            "workflow_id": execution.workflow_id,
            "status": execution.status.value,
            "completed_tasks": len(execution.completed_tasks),
            "total_tasks": len(execution.tasks),
            "error_count": execution.error_count,
            "start_time": execution.start_time.isoformat() if execution.start_time else None,
            "end_time": execution.end_time.isoformat() if execution.end_time else None
        }

    def get_workflow_summary(self) -> Dict[str, Any]:
        """Get summary of all workflows and executions"""
        return {
            "total_workflows": len(self.workflows),
            "total_executions": len(self.executions),
            "active_executions": len(self.active_executions),
            "registered_agents": len(self.agents),
            "available_resources": len(self.resources)
        }

    def shutdown(self):
        """Shutdown the workflow orchestrator"""
        self.running = False
        if self.execution_thread and self.execution_thread.is_alive():
            self.execution_thread.join()
        logger.info("Workflow Orchestrator shutdown complete")
