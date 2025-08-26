#!/usr/bin/env python3
"""
Workflow Orchestrator - Workflow Coordination Engine
===================================================

Coordinates workflow execution and management operations.
Follows V2 standards: ≤200 LOC, single responsibility.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..core.workflow_engine import WorkflowEngine
from ..core.workflow_monitor import WorkflowMonitor
from ..managers.workflow_manager import WorkflowManager
from ..managers.task_manager import TaskManager
from ..managers.resource_manager import ResourceManager
from ..types.workflow_enums import WorkflowType, WorkflowStatus, TaskStatus
from ..types.workflow_models import WorkflowExecution


class WorkflowOrchestrator:
    """
    Orchestrates workflow execution and management operations.
    
    Single responsibility: Coordinate workflow operations and component management
    following V2 standards.
    """
    
    def __init__(self):
        """Initialize workflow orchestrator."""
        self.logger = logging.getLogger(f"{__name__}.WorkflowOrchestrator")
        
        # Core workflow components
        self.workflow_engine = self._initialize_component("WorkflowEngine", WorkflowEngine)
        self.workflow_monitor = self._initialize_component("WorkflowMonitor", WorkflowMonitor)
        
        # Specialized managers
        self.workflow_manager = self._initialize_component("WorkflowManager", WorkflowManager)
        self.task_manager = self._initialize_component("TaskManager", TaskManager)
        self.resource_manager = self._initialize_component("ResourceManager", ResourceManager)
        
        # Workflow state
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        
        # Performance tracking
        self.total_workflows_created = 0
        self.total_workflows_executed = 0
        self.total_workflows_completed = 0
        self.total_workflows_failed = 0
        self.startup_time = datetime.now()
        
        self.logger.info("✅ Workflow Orchestrator initialized")
    
    def _initialize_component(self, component_name: str, component_class) -> Optional[Any]:
        """Initialize a workflow component with error handling."""
        try:
            component = component_class()
            self.logger.info(f"✅ {component_name} initialized")
            return component
        except Exception as e:
            self.logger.warning(f"⚠️ {component_name} initialization failed: {e}")
            return None
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        return {
            "system_status": "HEALTHY" if self._check_components() else "DEGRADED",
            "components": {
                "workflow_engine": bool(self.workflow_engine),
                "workflow_monitor": bool(self.workflow_monitor),
                "workflow_manager": bool(self.workflow_manager),
                "task_manager": bool(self.task_manager),
                "resource_manager": bool(self.resource_manager)
            },
            "workflows": {
                "total_created": self.total_workflows_created,
                "total_executed": self.total_workflows_executed,
                "total_completed": self.total_workflows_completed,
                "total_failed": self.total_workflows_failed,
                "active": len(self.active_workflows)
            },
            "uptime": (datetime.now() - self.startup_time).total_seconds()
        }
    
    def _check_components(self) -> bool:
        """Check if core components are available."""
        return bool(
            self.workflow_manager and 
            self.task_manager and 
            self.resource_manager
        )
    
    def register_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> bool:
        """Register a new workflow."""
        try:
            if workflow_id in self.active_workflows:
                self.logger.warning(f"Workflow {workflow_id} already registered")
                return False
            
            self.active_workflows[workflow_id] = workflow_data
            self.total_workflows_created += 1
            
            self.logger.info(f"✅ Workflow {workflow_id} registered")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to register workflow {workflow_id}: {e}")
            return False
    
    def unregister_workflow(self, workflow_id: str) -> bool:
        """Unregister a workflow."""
        try:
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
                self.logger.info(f"✅ Workflow {workflow_id} unregistered")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Failed to unregister workflow {workflow_id}: {e}")
            return False
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow status."""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": workflow.get("status", "UNKNOWN"),
                "active": True
            }
        return None
    
    def list_active_workflows(self) -> List[str]:
        """List all active workflow IDs."""
        return list(self.active_workflows.keys())
    
    def cleanup_completed_workflows(self) -> int:
        """Clean up completed workflows."""
        completed_count = 0
        
        for workflow_id, workflow_data in list(self.active_workflows.items()):
            if workflow_data.get("status") in ["COMPLETED", "FAILED", "CANCELLED"]:
                self.unregister_workflow(workflow_id)
                completed_count += 1
        
        if completed_count > 0:
            self.logger.info(f"✅ Cleaned up {completed_count} completed workflows")
        
        return completed_count
