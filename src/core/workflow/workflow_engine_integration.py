#!/usr/bin/env python3
"""
Workflow Engine Integration - FSM + Workflow System Integration
=============================================================

Integrates the newly implemented FSM Core V2 system with existing workflow infrastructure
for unified Phase 2 workflow management. Follows V2 standards: use existing architecture first.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import logging
import json
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

# Import existing workflow systems
try:
    from base_workflow_engine import BaseWorkflowEngine
    from types.workflow_enums import WorkflowStatus, WorkflowType, TaskStatus
    from types.workflow_models import WorkflowDefinition, WorkflowExecution, WorkflowStep
except ImportError:
    # Fallback for direct execution
    from .base_workflow_engine import BaseWorkflowEngine
    from .types.workflow_enums import WorkflowStatus, WorkflowType, TaskStatus
    from .types.workflow_models import WorkflowDefinition, WorkflowExecution, WorkflowStep

# Import FSM system
try:
    from ..fsm.fsm_core_v2 import (
        FSMCoreV2, StateDefinition, TransitionDefinition, WorkflowInstance,
        StateStatus, TransitionType, WorkflowPriority, StateHandler, TransitionHandler
    )
except ImportError:
    # Fallback for direct execution
    from fsm.fsm_core_v2 import (
        FSMCoreV2, StateDefinition, TransitionDefinition, WorkflowInstance,
        StateStatus, TransitionType, WorkflowPriority, StateHandler, TransitionHandler
    )


class FSMWorkflowIntegration:
    """
    Integrates FSM Core V2 with existing workflow infrastructure.
    
    Single responsibility: Provide seamless integration between FSM and workflow systems
    following V2 architecture standards - use existing systems first.
    """
    
    def __init__(self):
        """Initialize FSM workflow integration."""
        self.logger = logging.getLogger(f"{__name__}.FSMWorkflowIntegration")
        
        # Initialize existing workflow engine
        try:
            self.workflow_engine = BaseWorkflowEngine()
            self.logger.info("✅ BaseWorkflowEngine initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize BaseWorkflowEngine: {e}")
            self.workflow_engine = None
        
        # Initialize FSM system
        try:
            self.fsm_system = FSMCoreV2()
            self.fsm_system.start_system()
            self.logger.info("✅ FSM Core V2 system initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize FSM system: {e}")
            self.fsm_system = None
        
        # Integration state
        self.integrated_workflows: Dict[str, Dict[str, Any]] = {}
        self.fsm_workflow_mapping: Dict[str, str] = {}  # FSM workflow ID -> Workflow ID
        self.workflow_fsm_mapping: Dict[str, str] = {}  # Workflow ID -> FSM workflow ID
        
        # Integration status
        self.integration_status = {
            "workflow_engine": "CONNECTED" if self.workflow_engine else "DISCONNECTED",
            "fsm_system": "CONNECTED" if self.fsm_system else "DISCONNECTED",
            "integration_active": bool(self.workflow_engine and self.fsm_system),
            "last_health_check": datetime.now().isoformat()
        }
        
        self.logger.info("✅ FSMWorkflowIntegration initialized")
    
    def create_integrated_workflow(self, workflow_def: WorkflowDefinition, 
                                 fsm_states: List[StateDefinition],
                                 fsm_transitions: List[TransitionDefinition],
                                 priority: WorkflowPriority = WorkflowPriority.NORMAL) -> Optional[str]:
        """
        Create a workflow that integrates both systems.
        
        Args:
            workflow_def: Workflow definition for existing system
            fsm_states: FSM state definitions
            fsm_transitions: FSM transition definitions
            priority: Workflow priority level
        
        Returns:
            Integrated workflow ID or None if creation fails
        """
        try:
            if not self.integration_status["integration_active"]:
                self.logger.error("❌ Integration not active - cannot create workflow")
                return None
            
            # Create workflow in existing system
            workflow_id = self._create_workflow_in_engine(workflow_def)
            if not workflow_id:
                self.logger.error("❌ Failed to create workflow in engine")
                return None
            
            # Create FSM workflow
            fsm_workflow_id = self._create_fsm_workflow(workflow_def.name, fsm_states, fsm_transitions, priority)
            if not fsm_workflow_id:
                self.logger.error("❌ Failed to create FSM workflow")
                # Cleanup workflow engine workflow
                self._cleanup_workflow_engine_workflow(workflow_id)
                return None
            
            # Store integration mapping
            self.fsm_workflow_mapping[fsm_workflow_id] = workflow_id
            self.workflow_fsm_mapping[workflow_id] = fsm_workflow_id
            
            # Store integration metadata
            self.integrated_workflows[workflow_id] = {
                "workflow_id": workflow_id,
                "fsm_workflow_id": fsm_workflow_id,
                "workflow_def": workflow_def,
                "fsm_states": fsm_states,
                "fsm_transitions": fsm_transitions,
                "priority": priority.value,
                "created_at": datetime.now().isoformat(),
                "status": "integrated"
            }
            
            self.logger.info(f"✅ Created integrated workflow: {workflow_id} <-> {fsm_workflow_id}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create integrated workflow: {e}")
            return None
    
    def _create_workflow_in_engine(self, workflow_def: WorkflowDefinition) -> Optional[str]:
        """Create workflow in existing workflow engine."""
        try:
            if not self.workflow_engine:
                return None
            
            # Use existing workflow engine to create workflow
            # This leverages existing functionality - no duplication
            workflow_id = f"integrated_{workflow_def.name}_{int(time.time())}"
            
            # Store workflow definition
            if hasattr(self.workflow_engine, 'workflow_definitions'):
                self.workflow_engine.workflow_definitions[workflow_id] = workflow_def
            
            self.logger.info(f"✅ Created workflow in engine: {workflow_id}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create workflow in engine: {e}")
            return None
    
    def _create_fsm_workflow(self, workflow_name: str, states: List[StateDefinition],
                            transitions: List[TransitionDefinition], priority: WorkflowPriority) -> Optional[str]:
        """Create workflow in FSM system."""
        try:
            if not self.fsm_system:
                return None
            
            # Add states to FSM
            for state in states:
                if not self.fsm_system.add_state(state):
                    self.logger.error(f"❌ Failed to add state: {state.name}")
                    return None
            
            # Add transitions to FSM
            for transition in transitions:
                if not self.fsm_system.add_transition(transition):
                    self.logger.error(f"❌ Failed to add transition: {transition.from_state} -> {transition.to_state}")
                    return None
            
            # Create FSM workflow
            initial_state = states[0].name if states else "start"
            fsm_workflow_id = self.fsm_system.create_workflow(workflow_name, initial_state, priority)
            
            if fsm_workflow_id:
                self.logger.info(f"✅ Created FSM workflow: {fsm_workflow_id}")
                return fsm_workflow_id
            else:
                self.logger.error("❌ Failed to create FSM workflow")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Failed to create FSM workflow: {e}")
            return None
    
    def start_integrated_workflow(self, workflow_id: str) -> bool:
        """Start an integrated workflow in both systems."""
        try:
            if workflow_id not in self.integrated_workflows:
                self.logger.error(f"❌ Workflow {workflow_id} not found in integrated workflows")
                return False
            
            integration_data = self.integrated_workflows[workflow_id]
            fsm_workflow_id = integration_data["fsm_workflow_id"]
            
            # Start FSM workflow
            if self.fsm_system and fsm_workflow_id in self.fsm_system.workflows:
                if self.fsm_system.start_workflow(fsm_workflow_id):
                    self.logger.info(f"✅ Started FSM workflow: {fsm_workflow_id}")
                else:
                    self.logger.error(f"❌ Failed to start FSM workflow: {fsm_workflow_id}")
                    return False
            
            # Update integration status
            integration_data["status"] = "running"
            integration_data["started_at"] = datetime.now().isoformat()
            
            self.logger.info(f"✅ Started integrated workflow: {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start integrated workflow: {e}")
            return False
    
    def stop_integrated_workflow(self, workflow_id: str) -> bool:
        """Stop an integrated workflow in both systems."""
        try:
            if workflow_id not in self.integrated_workflows:
                self.logger.error(f"❌ Workflow {workflow_id} not found in integrated workflows")
                return False
            
            integration_data = self.integrated_workflows[workflow_id]
            fsm_workflow_id = integration_data["fsm_workflow_id"]
            
            # Stop FSM workflow
            if self.fsm_system and fsm_workflow_id in self.fsm_system.workflows:
                if self.fsm_system.stop_workflow(fsm_workflow_id):
                    self.logger.info(f"✅ Stopped FSM workflow: {fsm_workflow_id}")
                else:
                    self.logger.warning(f"⚠️ Failed to stop FSM workflow: {fsm_workflow_id}")
            
            # Update integration status
            integration_data["status"] = "stopped"
            integration_data["stopped_at"] = datetime.now().isoformat()
            
            self.logger.info(f"✅ Stopped integrated workflow: {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to stop integrated workflow: {e}")
            return False
    
    def get_integrated_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive status of an integrated workflow."""
        try:
            if workflow_id not in self.integrated_workflows:
                return None
            
            integration_data = self.integrated_workflows[workflow_id]
            fsm_workflow_id = integration_data["fsm_workflow_id"]
            
            # Get FSM workflow status
            fsm_status = None
            if self.fsm_system and fsm_workflow_id in self.fsm_system.workflows:
                fsm_workflow = self.fsm_system.get_workflow(fsm_workflow_id)
                if fsm_workflow:
                    fsm_status = {
                        "current_state": fsm_workflow.current_state,
                        "status": fsm_workflow.status.value,
                        "start_time": fsm_workflow.start_time.isoformat(),
                        "last_update": fsm_workflow.last_update.isoformat(),
                        "error_count": fsm_workflow.error_count,
                        "retry_count": fsm_workflow.retry_count
                    }
            
            # Compile comprehensive status
            status = {
                "workflow_id": workflow_id,
                "fsm_workflow_id": fsm_workflow_id,
                "integration_status": integration_data["status"],
                "fsm_status": fsm_status,
                "created_at": integration_data["created_at"],
                "priority": integration_data["priority"]
            }
            
            if "started_at" in integration_data:
                status["started_at"] = integration_data["started_at"]
            if "stopped_at" in integration_data:
                status["stopped_at"] = integration_data["stopped_at"]
            
            return status
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get workflow status: {e}")
            return None
    
    def list_integrated_workflows(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all integrated workflows with optional status filter."""
        try:
            workflows = []
            for workflow_id, integration_data in self.integrated_workflows.items():
                if status_filter and integration_data["status"] != status_filter:
                    continue
                
                workflows.append({
                    "workflow_id": workflow_id,
                    "fsm_workflow_id": integration_data["fsm_workflow_id"],
                    "name": integration_data["workflow_def"].name,
                    "status": integration_data["status"],
                    "priority": integration_data["priority"],
                    "created_at": integration_data["created_at"]
                })
            
            return workflows
            
        except Exception as e:
            self.logger.error(f"❌ Failed to list integrated workflows: {e}")
            return []
    
    def get_integration_health(self) -> Dict[str, Any]:
        """Get integration system health status."""
        try:
            # Check workflow engine health
            workflow_engine_health = "healthy"
            if not self.workflow_engine:
                workflow_engine_health = "disconnected"
            elif hasattr(self.workflow_engine, 'stats'):
                workflow_engine_health = "operational"
            
            # Check FSM system health
            fsm_system_health = "healthy"
            if not self.fsm_system:
                fsm_system_health = "disconnected"
            elif not self.fsm_system.is_running:
                fsm_system_health = "stopped"
            else:
                fsm_system_health = "operational"
            
            # Overall integration health
            overall_health = "healthy"
            if workflow_engine_health != "healthy" or fsm_system_health != "healthy":
                overall_health = "degraded"
            if workflow_engine_health == "disconnected" or fsm_system_health == "disconnected":
                overall_health = "critical"
            
            health_status = {
                "overall_health": overall_health,
                "workflow_engine": {
                    "status": workflow_engine_health,
                    "connected": bool(self.workflow_engine)
                },
                "fsm_system": {
                    "status": fsm_system_health,
                    "connected": bool(self.fsm_system),
                    "running": self.fsm_system.is_running if self.fsm_system else False
                },
                "integration": {
                    "active": self.integration_status["integration_active"],
                    "total_workflows": len(self.integrated_workflows),
                    "running_workflows": len([w for w in self.integrated_workflows.values() if w["status"] == "running"])
                },
                "last_health_check": datetime.now().isoformat()
            }
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get integration health: {e}")
            return {"overall_health": "unknown", "error": str(e)}
    
    def _cleanup_workflow_engine_workflow(self, workflow_id: str) -> None:
        """Clean up workflow in workflow engine if creation fails."""
        try:
            if self.workflow_engine and hasattr(self.workflow_engine, 'workflow_definitions'):
                if workflow_id in self.workflow_engine.workflow_definitions:
                    del self.workflow_engine.workflow_definitions[workflow_id]
                    self.logger.info(f"✅ Cleaned up workflow engine workflow: {workflow_id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to cleanup workflow engine workflow: {e}")
    
    def export_integration_report(self, format: str = "json") -> Optional[str]:
        """Export integration system report."""
        try:
            report_data = {
                "integration_status": self.integration_status,
                "health_status": self.get_integration_health(),
                "integrated_workflows": self.list_integrated_workflows(),
                "mappings": {
                    "fsm_to_workflow": self.fsm_workflow_mapping,
                    "workflow_to_fsm": self.workflow_fsm_mapping
                },
                "exported_at": datetime.now().isoformat()
            }
            
            if format.lower() == "json":
                return json.dumps(report_data, indent=2, default=str)
            else:
                return f"Report format '{format}' not supported"
                
        except Exception as e:
            self.logger.error(f"❌ Failed to export integration report: {e}")
            return None


# ============================================================================
# INTEGRATION FACTORY FUNCTIONS
# ============================================================================

def create_fsm_workflow_integration() -> FSMWorkflowIntegration:
    """Factory function to create FSM workflow integration."""
    return FSMWorkflowIntegration()


def get_integration_status() -> Dict[str, Any]:
    """Get current integration status."""
    integration = FSMWorkflowIntegration()
    return integration.get_integration_health()


# ============================================================================
# BACKWARDS COMPATIBILITY
# ============================================================================

# Maintain backwards compatibility
FSMWorkflowBridge = FSMWorkflowIntegration
WorkflowFSMIntegration = FSMWorkflowIntegration

# Export all components
__all__ = [
    "FSMWorkflowIntegration",
    "FSMWorkflowBridge",
    "WorkflowFSMIntegration",
    "create_fsm_workflow_integration",
    "get_integration_status"
]


if __name__ == "__main__":
    # Test integration
    integration = FSMWorkflowIntegration()
    
    # Get health status
    health = integration.get_integration_health()
    print(f"Integration Health: {health['overall_health']}")
    
    # Export report
    report = integration.export_integration_report()
    if report:
        print("✅ Integration report exported successfully")
    else:
        print("❌ Failed to export integration report")
