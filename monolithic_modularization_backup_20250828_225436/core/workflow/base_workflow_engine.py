#!/usr/bin/env python3
"""
Base Workflow Engine - Unified Workflow System

Unified base workflow engine for all workflow types following V2 standards.
Uses orchestrator pattern for component management.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

import logging
import uuid
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from .orchestration.workflow_orchestrator import WorkflowOrchestrator
from .types.workflow_enums import WorkflowType, WorkflowStatus, TaskStatus
from .types.workflow_models import (
    WorkflowDefinition, WorkflowExecution, WorkflowTask, 
    WorkflowStep, ResourceRequirement, AgentCapabilityInfo
)


class BaseWorkflowEngine:
    """
    Unified base workflow engine for all workflow types.
    
    Single responsibility: Provide unified interface for all workflow operations
    using orchestrator pattern for component management.
    """
    
    def __init__(self):
        """Initialize unified workflow engine with orchestrator."""
        self.logger = logging.getLogger(f"{__name__}.BaseWorkflowEngine")
        
        # Use orchestrator for component management
        self.orchestrator = WorkflowOrchestrator()
        
        # Access components through orchestrator
        self.workflow_engine = self.orchestrator.workflow_engine
        self.workflow_monitor = self.orchestrator.workflow_monitor
        self.workflow_manager = self.orchestrator.workflow_manager
        self.task_manager = self.orchestrator.task_manager
        self.resource_manager = self.orchestrator.resource_manager
        
        self.logger.info("✅ Base Workflow Engine initialized with orchestrator")
    
    def create_workflow(self, workflow_type: Union[str, WorkflowType], 
                       definition: Dict[str, Any]) -> str:
        """Create a new workflow."""
        try:
            workflow_id = str(uuid.uuid4())
            
            # Register workflow with orchestrator
            workflow_data = {
                "workflow_id": workflow_id,
                "type": workflow_type,
                "definition": definition,
                "status": WorkflowStatus.CREATED,
                "created_at": datetime.now().isoformat()
            }
            
            self.orchestrator.register_workflow(workflow_id, workflow_data)
            
            self.logger.info(f"✅ Created workflow: {workflow_id}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create workflow: {e}")
            raise
    
    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a workflow."""
        try:
            workflow_status = self.orchestrator.get_workflow_status(workflow_id)
            if not workflow_status:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False
            
            # Update status to executing
            if workflow_id in self.orchestrator.active_workflows:
                self.orchestrator.active_workflows[workflow_id]["status"] = WorkflowStatus.EXECUTING
            
            self.logger.info(f"✅ Executing workflow: {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to execute workflow {workflow_id}: {e}")
            return False
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow status."""
        return self.orchestrator.get_workflow_status(workflow_id)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status."""
        return self.orchestrator.get_system_health()
    
    def list_workflows(self) -> List[str]:
        """List all active workflows."""
        return self.orchestrator.list_active_workflows()
    
    def cleanup_workflows(self) -> int:
        """Clean up completed workflows."""
        return self.orchestrator.cleanup_completed_workflows()
