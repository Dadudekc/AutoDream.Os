#!/usr/bin/env python3
"""
Base Workflow Engine - Unified Workflow System

Unified base workflow engine for all workflow types following V2 standards.
NO duplicate implementations - unified architecture only.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

import logging
import uuid
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from .core.workflow_engine import WorkflowEngine
# from .core.workflow_executor import WorkflowExecutor  # REMOVED - module deleted
# from .core.workflow_planner import WorkflowPlanner    # REMOVED - module deleted
from .core.workflow_monitor import WorkflowMonitor
from .managers.workflow_manager import WorkflowManager
from .managers.task_manager import TaskManager
from .managers.resource_manager import ResourceManager
from .types.workflow_enums import WorkflowType, WorkflowStatus, TaskStatus
from .types.workflow_models import (
    WorkflowDefinition, WorkflowExecution, WorkflowTask, 
    WorkflowStep, ResourceRequirement, AgentCapabilityInfo
)


class BaseWorkflowEngine:
    """
    Unified base workflow engine for all workflow types.
    
    Single responsibility: Provide unified interface for all workflow operations
    across business processes, task workflows, automation workflows, and FSM workflows.
    
    Consolidates functionality from 15+ duplicate implementations.
    """
    
    def __init__(self):
        """Initialize unified workflow engine with all components."""
        self.logger = logging.getLogger(f"{__name__}.BaseWorkflowEngine")
        
        # Core workflow components - Initialize with error handling
        try:
            self.workflow_engine = WorkflowEngine()
            self.logger.info("✅ WorkflowEngine initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ WorkflowEngine initialization failed: {e}")
            self.workflow_engine = None
        
        # try:
        #     self.workflow_executor = WorkflowExecutor()  # REMOVED - module deleted
        #     self.logger.info("✅ WorkflowExecutor initialized")
        # except Exception as e:
        #     self.logger.warning(f"⚠️ WorkflowExecutor initialization failed: {e}")
        #     self.workflow_executor = None
        
        # try:
        #     self.workflow_planner = WorkflowPlanner()  # REMOVED - module deleted
        #     self.logger.info("✅ WorkflowPlanner initialized")
        # except Exception as e:
        #     self.logger.warning(f"⚠️ WorkflowPlanner initialization failed: {e}")
        #     self.workflow_planner = None
        
        try:
            self.workflow_monitor = WorkflowMonitor()
            self.logger.info("✅ WorkflowMonitor initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ WorkflowMonitor initialization failed: {e}")
            self.workflow_monitor = None
        
        # Specialized managers
        try:
            self.workflow_manager = WorkflowManager()
            self.logger.info("✅ WorkflowManager initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ WorkflowManager initialization failed: {e}")
            self.workflow_manager = None
        
        try:
            self.task_manager = TaskManager()
            self.logger.info("✅ TaskManager initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ TaskManager initialization failed: {e}")
            self.task_manager = None
        
        try:
            self.resource_manager = ResourceManager()
            self.logger.info("✅ ResourceManager initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ ResourceManager initialization failed: {e}")
            self.resource_manager = None
        
        # Workflow registry
        self.workflow_registry: Dict[str, Dict[str, Any]] = {}
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        
        # Check if core components are available
        if self.workflow_manager and self.task_manager and self.resource_manager:
            self.logger.info("🚀 Base Workflow Engine initialized - Unified workflow system ready")
        else:
            self.logger.warning("⚠️ Base Workflow Engine initialized with limited functionality - Some components failed to initialize")
    
    def create_workflow(self, workflow_type: Union[str, WorkflowType], 
                       definition: Dict[str, Any]) -> str:
        """
        Create workflow of specified type with unified interface.
        
        Args:
            workflow_type: Type of workflow to create
            definition: Workflow definition dictionary
            
        Returns:
            Workflow ID of created workflow
        """
        try:
            if not self.workflow_manager:
                raise RuntimeError("WorkflowManager not available - component initialization failed")
            
            # Convert string to enum if needed
            if isinstance(workflow_type, str):
                workflow_type = WorkflowType(workflow_type)
            
            # Create workflow definition
            workflow_def = self._create_workflow_definition(workflow_type, definition)
            
            # Register workflow
            workflow_id = self.workflow_manager.create_workflow(workflow_def)
            
            # Store in registry
            self.workflow_registry[workflow_id] = {
                "type": workflow_type,
                "definition": workflow_def,
                "created_at": datetime.now().isoformat(),
                "status": WorkflowStatus.CREATED
            }
            
            self.logger.info(f"✅ Created {workflow_type.value} workflow: {workflow_id}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create workflow: {e}")
            raise
    
    def execute_workflow(self, workflow_id: str, 
                        parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute workflow with unified orchestration.
        
        Args:
            workflow_id: ID of workflow to execute
            parameters: Optional execution parameters
            
        Returns:
            Execution ID of started workflow
        """
        try:
            if not self.workflow_manager:
                raise RuntimeError("WorkflowManager not available - component initialization failed")
            
            if workflow_id not in self.workflow_registry:
                raise ValueError(f"Workflow not found: {workflow_id}")
            
            # Start workflow execution
            execution_id = self.workflow_manager.start_workflow(workflow_id, parameters)
            
            # Store active execution
            execution = self.workflow_manager.workflow_executions[execution_id]
            self.active_workflows[execution_id] = execution
            
            # Update registry status
            self.workflow_registry[workflow_id]["status"] = WorkflowStatus.RUNNING
            
            self.logger.info(f"🚀 Executing workflow {workflow_id} -> {execution_id}")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to execute workflow {workflow_id}: {e}")
            raise
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get unified workflow status and metrics.
        
        Args:
            workflow_id: ID of workflow
            
        Returns:
            Comprehensive workflow status dictionary
        """
        try:
            if workflow_id not in self.workflow_registry:
                return {"error": "Workflow not found"}
            
            registry_info = self.workflow_registry[workflow_id]
            workflow_status = self.workflow_manager.get_workflow_status(workflow_id)
            
            # Get active executions
            active_executions = [
                exec_id for exec_id, execution in self.active_workflows.items()
                if execution.workflow_id == workflow_id
            ]
            
            # Get monitoring data if available
            monitoring_data = {}
            if active_executions:
                latest_execution = self.active_workflows[active_executions[-1]]
                monitoring_data = self.workflow_monitor.monitor_workflow(latest_execution)
            
            return {
                "workflow_id": workflow_id,
                "type": registry_info["type"].value,
                "status": workflow_status.value if workflow_status else "unknown",
                "created_at": registry_info["created_at"],
                "active_executions": len(active_executions),
                "execution_ids": active_executions,
                "monitoring_data": monitoring_data
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get status for workflow {workflow_id}: {e}")
            return {"error": str(e)}
    
    def list_workflows(self, workflow_type: Optional[Union[str, WorkflowType]] = None) -> List[str]:
        """
        List available workflows with optional type filtering.
        
        Args:
            workflow_type: Optional filter by workflow type
            
        Returns:
            List of workflow IDs
        """
        try:
            if workflow_type:
                if isinstance(workflow_type, str):
                    workflow_type = WorkflowType(workflow_type)
                
                return [
                    workflow_id for workflow_id, info in self.workflow_registry.items()
                    if info["type"] == workflow_type
                ]
            
            return list(self.workflow_registry.keys())
            
        except Exception as e:
            self.logger.error(f"❌ Failed to list workflows: {e}")
            return []
    
    def stop_workflow(self, workflow_id: str) -> bool:
        """
        Stop workflow execution.
        
        Args:
            workflow_id: ID of workflow to stop
            
        Returns:
            True if stopped successfully
        """
        try:
            # Find active executions
            executions_to_stop = [
                exec_id for exec_id, execution in self.active_workflows.items()
                if execution.workflow_id == workflow_id
            ]
            
            # Stop all executions
            for exec_id in executions_to_stop:
                self.workflow_manager.stop_workflow(exec_id)
                del self.active_workflows[exec_id]
            
            # Update registry status
            if workflow_id in self.workflow_registry:
                self.workflow_registry[workflow_id]["status"] = WorkflowStatus.STOPPED
            
            self.logger.info(f"⏹️ Stopped workflow {workflow_id} ({len(executions_to_stop)} executions)")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to stop workflow {workflow_id}: {e}")
            return False
    
    def get_system_health(self) -> Dict[str, Any]:
        """
        Get overall workflow system health and metrics.
        
        Returns:
            System health status dictionary
        """
        try:
            total_workflows = len(self.workflow_registry)
            active_workflows = len(self.active_workflows)
            
            # Get resource utilization if available
            resource_utilization = 0.0
            if self.resource_manager:
                resource_metrics = self.resource_manager.optimize_resource_allocation()
                resource_utilization = resource_metrics.get("overall_utilization", 0.0)
            
            # Get task statistics if available
            ready_tasks = 0
            blocked_tasks = 0
            if self.task_manager:
                ready_tasks = len(self.task_manager.get_ready_tasks())
                blocked_tasks = len(self.task_manager.get_blocked_tasks())
            
            return {
                "system_status": "healthy" if total_workflows > 0 else "initializing",
                "total_workflows": total_workflows,
                "active_workflows": active_workflows,
                "ready_tasks": ready_tasks,
                "blocked_tasks": blocked_tasks,
                "resource_utilization": resource_utilization,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get system health: {e}")
            return {"error": str(e), "system_status": "error"}
    
    def _create_workflow_definition(self, workflow_type: WorkflowType, 
                                   definition: Dict[str, Any]) -> WorkflowDefinition:
        """Create WorkflowDefinition from dictionary data."""
        try:
            # Extract required fields
            workflow_id = definition.get("workflow_id", f"workflow_{datetime.now().timestamp()}")
            name = definition.get("name", f"Unnamed {workflow_type.value} Workflow")
            description = definition.get("description", "")
            
            # Create steps if provided
            steps = []
            if "steps" in definition:
                for step_data in definition["steps"]:
                    step = WorkflowStep(
                        step_id=step_data.get("step_id", f"step_{len(steps)}"),
                        name=step_data.get("name", "Unnamed Step"),
                        step_type=step_data.get("step_type", "general")
                    )
                    steps.append(step)
            
            return WorkflowDefinition(
                workflow_id=workflow_id,
                workflow_type=workflow_type,
                name=name,
                description=description,
                steps=steps,
                metadata=definition.get("metadata", {})
            )
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create workflow definition: {e}")
            raise
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for base workflow engine."""
        try:
            # Test workflow creation
            test_definition = {
                "name": "Test Workflow",
                "description": "Smoke test workflow",
                "steps": [
                    {
                        "step_id": "test_step",
                        "name": "Test Step",
                        "step_type": "test"
                    }
                ]
            }
            
            workflow_id = self.create_workflow(WorkflowType.SEQUENTIAL, test_definition)
            
            if workflow_id and workflow_id in self.workflow_registry:
                self.logger.info("✅ Base workflow engine smoke test passed")
                return True
            else:
                self.logger.error("❌ Base workflow engine smoke test failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Base workflow engine smoke test failed: {e}")
            return False
