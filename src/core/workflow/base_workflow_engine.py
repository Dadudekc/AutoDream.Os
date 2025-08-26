#!/usr/bin/env python3
"""
Base Workflow Engine - Unified Workflow System

Unified base workflow engine for all workflow types following V2 standards.
NO duplicate implementations - unified architecture only.

Author: Agent-1 (Finalization & Completion)
License: MIT
"""

import logging
import uuid
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from .core.workflow_engine import WorkflowEngine
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
        
        # Workflow registry and state
        self.workflow_registry: Dict[str, Dict[str, Any]] = {}
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        
        # Performance tracking
        self.total_workflows_created = 0
        self.total_workflows_executed = 0
        self.total_workflows_completed = 0
        self.total_workflows_failed = 0
        self.startup_time = datetime.now()
        
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
                "status": WorkflowStatus.CREATED,
                "metadata": definition.get("metadata", {})
            }
            
            self.total_workflows_created += 1
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
            self.workflow_registry[workflow_id]["last_executed"] = datetime.now().isoformat()
            
            self.total_workflows_executed += 1
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
            if active_executions and self.workflow_monitor:
                latest_execution = self.active_workflows[active_executions[-1]]
                monitoring_data = self.workflow_monitor.monitor_workflow(latest_execution)
            
            # Get task status if available
            task_status = {}
            if self.task_manager:
                task_status = self.task_manager.get_workflow_task_status(workflow_id)
            
            return {
                "workflow_id": workflow_id,
                "type": registry_info["type"].value,
                "status": workflow_status.value if workflow_status else "unknown",
                "created_at": registry_info["created_at"],
                "last_executed": registry_info.get("last_executed"),
                "active_executions": len(active_executions),
                "execution_ids": active_executions,
                "monitoring_data": monitoring_data,
                "task_status": task_status,
                "metadata": registry_info.get("metadata", {})
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
                if self.workflow_manager:
                    self.workflow_manager.stop_workflow(exec_id)
                del self.active_workflows[exec_id]
            
            # Update registry status
            if workflow_id in self.workflow_registry:
                self.workflow_registry[workflow_id]["status"] = WorkflowStatus.STOPPED
                self.workflow_registry[workflow_id]["stopped_at"] = datetime.now().isoformat()
            
            self.logger.info(f"⏹️ Stopped workflow {workflow_id} ({len(executions_to_stop)} executions)")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to stop workflow {workflow_id}: {e}")
            return False
    
    def pause_workflow(self, workflow_id: str) -> bool:
        """
        Pause workflow execution.
        
        Args:
            workflow_id: ID of workflow to pause
            
        Returns:
            True if paused successfully
        """
        try:
            if workflow_id not in self.workflow_registry:
                return False
            
            # Find active executions
            active_executions = [
                exec_id for exec_id, execution in self.active_workflows.items()
                if execution.workflow_id == workflow_id
            ]
            
            # Pause all executions
            for exec_id in active_executions:
                if self.workflow_manager:
                    self.workflow_manager.pause_workflow(exec_id)
            
            # Update registry status
            self.workflow_registry[workflow_id]["status"] = WorkflowStatus.PAUSED
            self.workflow_registry[workflow_id]["paused_at"] = datetime.now().isoformat()
            
            self.logger.info(f"⏸️ Paused workflow {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to pause workflow {workflow_id}: {e}")
            return False
    
    def resume_workflow(self, workflow_id: str) -> bool:
        """
        Resume paused workflow execution.
        
        Args:
            workflow_id: ID of workflow to resume
            
        Returns:
            True if resumed successfully
        """
        try:
            if workflow_id not in self.workflow_registry:
                return False
            
            if self.workflow_registry[workflow_id]["status"] != WorkflowStatus.PAUSED:
                return False
            
            # Resume all paused executions
            active_executions = [
                exec_id for exec_id, execution in self.active_workflows.items()
                if execution.workflow_id == workflow_id
            ]
            
            for exec_id in active_executions:
                if self.workflow_manager:
                    self.workflow_manager.resume_workflow(exec_id)
            
            # Update registry status
            self.workflow_registry[workflow_id]["status"] = WorkflowStatus.RUNNING
            self.workflow_registry[workflow_id]["resumed_at"] = datetime.now().isoformat()
            
            self.logger.info(f"▶️ Resumed workflow {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to resume workflow {workflow_id}: {e}")
            return False
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete workflow and all associated data.
        
        Args:
            workflow_id: ID of workflow to delete
            
        Returns:
            True if deleted successfully
        """
        try:
            if workflow_id not in self.workflow_registry:
                return False
            
            # Stop any active executions
            self.stop_workflow(workflow_id)
            
            # Remove from registry
            workflow_info = self.workflow_registry.pop(workflow_id)
            
            # Add to history
            workflow_info["deleted_at"] = datetime.now().isoformat()
            self.workflow_history.append(workflow_info)
            
            # Clean up from workflow manager
            if self.workflow_manager:
                self.workflow_manager.delete_workflow(workflow_id)
            
            self.logger.info(f"🗑️ Deleted workflow {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to delete workflow {workflow_id}: {e}")
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
            
            # Calculate success rate
            total_executions = self.total_workflows_executed
            success_rate = 0.0
            if total_executions > 0:
                success_rate = (self.total_workflows_completed / total_executions) * 100.0
            
            return {
                "system_status": "healthy" if total_workflows > 0 else "initializing",
                "total_workflows": total_workflows,
                "active_workflows": active_workflows,
                "ready_tasks": ready_tasks,
                "blocked_tasks": blocked_tasks,
                "resource_utilization": resource_utilization,
                "total_executions": total_executions,
                "success_rate": success_rate,
                "uptime_seconds": (datetime.now() - self.startup_time).total_seconds(),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get system health: {e}")
            return {"error": str(e), "system_status": "error"}
    
    def get_workflow_metrics(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get detailed metrics for a specific workflow.
        
        Args:
            workflow_id: ID of workflow
            
        Returns:
            Workflow metrics dictionary
        """
        try:
            if workflow_id not in self.workflow_registry:
                return {"error": "Workflow not found"}
            
            registry_info = self.workflow_registry[workflow_id]
            
            # Get execution history
            executions = [
                exec_id for exec_id, execution in self.active_workflows.items()
                if execution.workflow_id == workflow_id
            ]
            
            # Get task metrics if available
            task_metrics = {}
            if self.task_manager:
                task_metrics = self.task_manager.get_workflow_task_metrics(workflow_id)
            
            return {
                "workflow_id": workflow_id,
                "type": registry_info["type"].value,
                "status": registry_info["status"].value,
                "created_at": registry_info["created_at"],
                "total_executions": len(executions),
                "active_executions": len([e for e in executions if e in self.active_workflows]),
                "task_metrics": task_metrics,
                "metadata": registry_info.get("metadata", {})
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get metrics for workflow {workflow_id}: {e}")
            return {"error": str(e)}
    
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
                # Test workflow execution
                execution_id = self.execute_workflow(workflow_id)
                
                if execution_id:
                    # Test workflow status
                    status = self.get_workflow_status(workflow_id)
                    
                    # Clean up test workflow
                    self.delete_workflow(workflow_id)
                    
                    self.logger.info("✅ Base workflow engine smoke test passed")
                    return True
                else:
                    self.logger.error("❌ Base workflow engine smoke test failed - execution failed")
                    return False
            else:
                self.logger.error("❌ Base workflow engine smoke test failed - creation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Base workflow engine smoke test failed: {e}")
            return False
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get comprehensive engine status and performance metrics."""
        uptime = (datetime.now() - self.startup_time).total_seconds()
        
        return {
            "engine_type": "BaseWorkflowEngine",
            "status": "active",
            "uptime_seconds": uptime,
            "total_workflows_created": self.total_workflows_created,
            "total_workflows_executed": self.total_workflows_executed,
            "total_workflows_completed": self.total_workflows_completed,
            "total_workflows_failed": self.total_workflows_failed,
            "active_workflows": len(self.active_workflows),
            "total_workflows": len(self.workflow_registry),
            "workflow_history": len(self.workflow_history),
            "components_available": {
                "workflow_engine": self.workflow_engine is not None,
                "workflow_monitor": self.workflow_monitor is not None,
                "workflow_manager": self.workflow_manager is not None,
                "task_manager": self.task_manager is not None,
                "resource_manager": self.resource_manager is not None
            },
            "startup_time": self.startup_time.isoformat(),
            "last_updated": datetime.now().isoformat()
        }
