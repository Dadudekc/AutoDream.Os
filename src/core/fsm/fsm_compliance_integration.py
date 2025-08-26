#!/usr/bin/env python3
"""
FSM Compliance Integration - FSM + Compliance Monitoring System Integration
=======================================================================

Integrates the FSM Core V2 system with the compliance monitoring system
for unified Phase 2 workflow management and compliance tracking.
Follows V2 standards: use existing architecture first.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import logging
import json
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

# Import FSM system
try:
    from fsm_core_v2 import (
        FSMCoreV2, StateDefinition, TransitionDefinition, WorkflowInstance,
        StateStatus, TransitionType, WorkflowPriority, StateHandler, TransitionHandler
    )
except ImportError:
    # Fallback for direct execution
    from .fsm_core_v2 import (
        FSMCoreV2, StateDefinition, TransitionDefinition, WorkflowInstance,
        StateStatus, TransitionType, WorkflowPriority, StateHandler, TransitionHandler
    )

# Import compliance monitoring system
try:
    from ..compliance_monitoring_system import (
        ComplianceMonitoringSystem, ComplianceCheck, AgentProgress
    )
except ImportError:
    try:
        # Fallback for direct execution
        from compliance_monitoring_system import (
            ComplianceMonitoringSystem, ComplianceCheck, AgentProgress
        )
    except ImportError:
        # Mock classes if compliance system not available
        class ComplianceMonitoringSystem:
            def __init__(self):
                self.agent_progress = {}
            def track_agent_progress(self, agent_id, task_id, progress_data):
                key = f"{agent_id}_{task_id}"
                self.agent_progress[key] = progress_data
            def get_compliance_report(self):
                return {"total_checks": 0}
        
        class ComplianceCheck:
            pass
        
        class AgentProgress:
            pass


class FSMComplianceIntegration:
    """
    Integrates FSM Core V2 with compliance monitoring system.
    
    Single responsibility: Provide seamless integration between FSM and compliance
    systems following V2 architecture standards - use existing systems first.
    """
    
    def __init__(self):
        """Initialize FSM compliance integration."""
        self.logger = logging.getLogger(f"{__name__}.FSMComplianceIntegration")
        
        # Initialize FSM system
        try:
            self.fsm_system = FSMCoreV2()
            self.fsm_system.start_system()
            self.logger.info("✅ FSM Core V2 system initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize FSM system: {e}")
            self.fsm_system = None
        
        # Initialize compliance monitoring system
        try:
            self.compliance_system = ComplianceMonitoringSystem()
            self.logger.info("✅ Compliance monitoring system initialized")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize compliance system: {e}")
            self.compliance_system = None
        
        # Integration state
        self.compliance_workflows: Dict[str, Dict[str, Any]] = {}
        self.fsm_compliance_mapping: Dict[str, str] = {}  # FSM workflow ID -> Compliance task ID
        self.compliance_fsm_mapping: Dict[str, str] = {}  # Compliance task ID -> FSM workflow ID
        
        # Integration status
        self.integration_status = {
            "fsm_system": "CONNECTED" if self.fsm_system else "DISCONNECTED",
            "compliance_system": "CONNECTED" if self.compliance_system else "DISCONNECTED",
            "integration_active": bool(self.fsm_system and self.compliance_system),
            "last_health_check": datetime.now().isoformat()
        }
        
        self.logger.info("✅ FSMComplianceIntegration initialized")
    
    def create_compliance_workflow(self, task_id: str, agent_id: str, 
                                   workflow_name: str, states: List[StateDefinition],
                                   transitions: List[TransitionDefinition],
                                   priority: WorkflowPriority = WorkflowPriority.NORMAL) -> Optional[str]:
        """
        Create a workflow that integrates FSM with compliance monitoring.
        
        Args:
            task_id: Compliance task identifier
            agent_id: Agent performing the task
            workflow_name: Name of the workflow
            states: FSM state definitions
            transitions: FSM transition definitions
            priority: Workflow priority level
        
        Returns:
            Integrated workflow ID or None if creation fails
        """
        try:
            if not self.integration_status["integration_active"]:
                self.logger.error("❌ Integration not active - cannot create workflow")
                return None
            
            # Create FSM workflow
            fsm_workflow_id = self._create_fsm_workflow(workflow_name, states, transitions, priority)
            if not fsm_workflow_id:
                self.logger.error("❌ Failed to create FSM workflow")
                return None
            
            # Create compliance tracking
            compliance_task_id = self._create_compliance_task(task_id, agent_id, workflow_name)
            if not compliance_task_id:
                self.logger.error("❌ Failed to create compliance task")
                # Cleanup FSM workflow
                self._cleanup_fsm_workflow(fsm_workflow_id)
                return None
            
            # Store integration mapping
            self.fsm_compliance_mapping[fsm_workflow_id] = compliance_task_id
            self.compliance_fsm_mapping[compliance_task_id] = fsm_workflow_id
            
            # Store integration metadata
            self.compliance_workflows[fsm_workflow_id] = {
                "fsm_workflow_id": fsm_workflow_id,
                "compliance_task_id": compliance_task_id,
                "task_id": task_id,
                "agent_id": agent_id,
                "workflow_name": workflow_name,
                "states": states,
                "transitions": transitions,
                "priority": priority.value,
                "created_at": datetime.now().isoformat(),
                "status": "integrated"
            }
            
            self.logger.info(f"✅ Created compliance workflow: {fsm_workflow_id} <-> {compliance_task_id}")
            return fsm_workflow_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create compliance workflow: {e}")
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
    
    def _create_compliance_task(self, task_id: str, agent_id: str, workflow_name: str) -> Optional[str]:
        """Create compliance tracking task."""
        try:
            if not self.compliance_system:
                return None
            
            # Create unique compliance task identifier
            compliance_task_id = f"compliance_{task_id}_{int(time.time())}"
            
            # Initialize progress tracking
            progress_data = {
                "percentage": 0.0,
                "phase": "INITIALIZED",
                "deliverables": {
                    "fsm_workflow": "PENDING",
                    "compliance_tracking": "ACTIVE",
                    "validation": "PENDING"
                },
                "code_changes": [f"Created compliance workflow: {workflow_name}"],
                "devlog_entries": [f"FSM compliance integration initialized for {workflow_name}"]
            }
            
            self.compliance_system.track_agent_progress(agent_id, task_id, progress_data)
            
            self.logger.info(f"✅ Created compliance task: {compliance_task_id}")
            return compliance_task_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create compliance task: {e}")
            return None
    
    def start_compliance_workflow(self, fsm_workflow_id: str) -> bool:
        """Start a compliance workflow in both systems."""
        try:
            if fsm_workflow_id not in self.compliance_workflows:
                self.logger.error(f"❌ Workflow {fsm_workflow_id} not found in compliance workflows")
                return False
            
            integration_data = self.compliance_workflows[fsm_workflow_id]
            compliance_task_id = integration_data["compliance_task_id"]
            task_id = integration_data["task_id"]
            agent_id = integration_data["agent_id"]
            
            # Start FSM workflow
            if self.fsm_system and fsm_workflow_id in self.fsm_system.workflows:
                if self.fsm_system.start_workflow(fsm_workflow_id):
                    self.logger.info(f"✅ Started FSM workflow: {fsm_workflow_id}")
                else:
                    self.logger.error(f"❌ Failed to start FSM workflow: {fsm_workflow_id}")
                    return False
            
            # Update compliance progress
            progress_data = {
                "percentage": 25.0,
                "phase": "RUNNING",
                "deliverables": {
                    "fsm_workflow": "ACTIVE",
                    "compliance_tracking": "ACTIVE",
                    "validation": "PENDING"
                },
                "code_changes": [f"Started FSM workflow: {fsm_workflow_id}"],
                "devlog_entries": [f"Compliance workflow execution started"]
            }
            
            self.compliance_system.track_agent_progress(agent_id, task_id, progress_data)
            
            # Update integration status
            integration_data["status"] = "running"
            integration_data["started_at"] = datetime.now().isoformat()
            
            self.logger.info(f"✅ Started compliance workflow: {fsm_workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start compliance workflow: {e}")
            return False
    
    def update_compliance_progress(self, fsm_workflow_id: str, progress_percentage: float, 
                                  phase: str, deliverables: Dict[str, str] = None,
                                  code_changes: List[str] = None, devlog_entries: List[str] = None) -> bool:
        """Update compliance progress for a workflow."""
        try:
            if fsm_workflow_id not in self.compliance_workflows:
                self.logger.error(f"❌ Workflow {fsm_workflow_id} not found in compliance workflows")
                return False
            
            integration_data = self.compliance_workflows[fsm_workflow_id]
            task_id = integration_data["task_id"]
            agent_id = integration_data["agent_id"]
            
            # Prepare progress data
            progress_data = {
                "percentage": progress_percentage,
                "phase": phase
            }
            
            if deliverables:
                progress_data["deliverables"] = deliverables
            
            if code_changes:
                progress_data["code_changes"] = code_changes
            
            if devlog_entries:
                progress_data["devlog_entries"] = devlog_entries
            
            # Update compliance tracking
            self.compliance_system.track_agent_progress(agent_id, task_id, progress_data)
            
            # Update integration metadata
            integration_data["last_progress_update"] = datetime.now().isoformat()
            integration_data["current_progress"] = progress_percentage
            integration_data["current_phase"] = phase
            
            self.logger.info(f"✅ Updated compliance progress: {fsm_workflow_id} - {progress_percentage}% - {phase}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update compliance progress: {e}")
            return False
    
    def validate_compliance_workflow(self, fsm_workflow_id: str) -> Dict[str, Any]:
        """Validate compliance workflow against requirements."""
        try:
            if fsm_workflow_id not in self.compliance_workflows:
                return {"valid": False, "error": "Workflow not found"}
            
            integration_data = self.compliance_workflows[fsm_workflow_id]
            task_id = integration_data["task_id"]
            agent_id = integration_data["agent_id"]
            
            validation_results = {
                "workflow_id": fsm_workflow_id,
                "task_id": task_id,
                "agent_id": agent_id,
                "validation_timestamp": datetime.now().isoformat(),
                "checks": {},
                "overall_valid": True
            }
            
            # Check FSM workflow status
            if self.fsm_system and fsm_workflow_id in self.fsm_system.workflows:
                fsm_workflow = self.fsm_system.get_workflow(fsm_workflow_id)
                if fsm_workflow:
                    validation_results["checks"]["fsm_workflow"] = {
                        "status": "VALID",
                        "current_state": fsm_workflow.current_state,
                        "workflow_status": fsm_workflow.status.value,
                        "error_count": fsm_workflow.error_count
                    }
                else:
                    validation_results["checks"]["fsm_workflow"] = {"status": "INVALID", "error": "Workflow not found"}
                    validation_results["overall_valid"] = False
            else:
                validation_results["checks"]["fsm_workflow"] = {"status": "INVALID", "error": "FSM system unavailable"}
                validation_results["overall_valid"] = False
            
            # Check compliance tracking
            if self.compliance_system:
                # Get agent progress
                progress_key = f"{agent_id}_{task_id}"
                if progress_key in self.compliance_system.agent_progress:
                    progress = self.compliance_system.agent_progress[progress_key]
                    validation_results["checks"]["compliance_tracking"] = {
                        "status": "VALID",
                        "progress_percentage": progress.get("percentage", 0.0),
                        "current_phase": progress.get("phase", "UNKNOWN"),
                        "last_update": datetime.now().isoformat()
                    }
                else:
                    validation_results["checks"]["compliance_tracking"] = {"status": "INVALID", "error": "Progress not found"}
                    validation_results["overall_valid"] = False
            else:
                validation_results["checks"]["compliance_tracking"] = {"status": "INVALID", "error": "Compliance system unavailable"}
                validation_results["overall_valid"] = False
            
            # Update compliance progress with validation results
            validation_phase = "VALIDATION_COMPLETE" if validation_results["overall_valid"] else "VALIDATION_FAILED"
            self.update_compliance_progress(
                fsm_workflow_id, 
                100.0 if validation_results["overall_valid"] else 75.0,
                validation_phase,
                deliverables={"validation": "COMPLETE" if validation_results["overall_valid"] else "FAILED"},
                devlog_entries=[f"Compliance validation: {'PASSED' if validation_results['overall_valid'] else 'FAILED'}"]
            )
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"❌ Failed to validate compliance workflow: {e}")
            return {"valid": False, "error": str(e)}
    
    def get_compliance_workflow_status(self, fsm_workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive status of a compliance workflow."""
        try:
            if fsm_workflow_id not in self.compliance_workflows:
                return None
            
            integration_data = self.compliance_workflows[fsm_workflow_id]
            compliance_task_id = integration_data["compliance_task_id"]
            task_id = integration_data["task_id"]
            agent_id = integration_data["agent_id"]
            
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
            
            # Get compliance status
            compliance_status = None
            if self.compliance_system:
                progress_key = f"{agent_id}_{task_id}"
                if progress_key in self.compliance_system.agent_progress:
                    progress = self.compliance_system.agent_progress[progress_key]
                    compliance_status = {
                        "progress_percentage": progress.get("percentage", 0.0),
                        "current_phase": progress.get("phase", "UNKNOWN"),
                        "start_time": datetime.now().isoformat(),
                        "last_update": datetime.now().isoformat(),
                        "deliverables_status": progress.get("deliverables", {}),
                        "code_changes_count": len(progress.get("code_changes", [])),
                        "devlog_entries_count": len(progress.get("devlog_entries", []))
                    }
            
            # Compile comprehensive status
            status = {
                "fsm_workflow_id": fsm_workflow_id,
                "compliance_task_id": compliance_task_id,
                "task_id": task_id,
                "agent_id": agent_id,
                "workflow_name": integration_data["workflow_name"],
                "integration_status": integration_data["status"],
                "fsm_status": fsm_status,
                "compliance_status": compliance_status,
                "created_at": integration_data["created_at"],
                "priority": integration_data["priority"]
            }
            
            if "started_at" in integration_data:
                status["started_at"] = integration_data["started_at"]
            if "last_progress_update" in integration_data:
                status["last_progress_update"] = integration_data["last_progress_update"]
            if "current_progress" in integration_data:
                status["current_progress"] = integration_data["current_progress"]
            if "current_phase" in integration_data:
                status["current_phase"] = integration_data["current_phase"]
            
            return status
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get workflow status: {e}")
            return None
    
    def list_compliance_workflows(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all compliance workflows with optional status filter."""
        try:
            workflows = []
            for fsm_workflow_id, integration_data in self.compliance_workflows.items():
                if status_filter and integration_data["status"] != status_filter:
                    continue
                
                workflows.append({
                    "fsm_workflow_id": fsm_workflow_id,
                    "compliance_task_id": integration_data["compliance_task_id"],
                    "task_id": integration_data["task_id"],
                    "agent_id": integration_data["agent_id"],
                    "workflow_name": integration_data["workflow_name"],
                    "status": integration_data["status"],
                    "priority": integration_data["priority"],
                    "created_at": integration_data["created_at"]
                })
            
            return workflows
            
        except Exception as e:
            self.logger.error(f"❌ Failed to list compliance workflows: {e}")
            return []
    
    def get_integration_health(self) -> Dict[str, Any]:
        """Get integration system health status."""
        try:
            # Check FSM system health
            fsm_system_health = "healthy"
            if not self.fsm_system:
                fsm_system_health = "disconnected"
            elif not self.fsm_system.is_running:
                fsm_system_health = "stopped"
            else:
                fsm_system_health = "operational"
            
            # Check compliance system health
            compliance_system_health = "healthy"
            if not self.compliance_system:
                compliance_system_health = "disconnected"
            else:
                compliance_system_health = "operational"
            
            # Overall integration health
            overall_health = "healthy"
            if fsm_system_health != "healthy" or compliance_system_health != "healthy":
                overall_health = "degraded"
            if fsm_system_health == "disconnected" or compliance_system_health == "disconnected":
                overall_health = "critical"
            
            health_status = {
                "overall_health": overall_health,
                "fsm_system": {
                    "status": fsm_system_health,
                    "connected": bool(self.fsm_system),
                    "running": self.fsm_system.is_running if self.fsm_system else False
                },
                "compliance_system": {
                    "status": compliance_system_health,
                    "connected": bool(self.compliance_system)
                },
                "integration": {
                    "active": self.integration_status["integration_active"],
                    "total_workflows": len(self.compliance_workflows),
                    "running_workflows": len([w for w in self.compliance_workflows.values() if w["status"] == "running"])
                },
                "last_health_check": datetime.now().isoformat()
            }
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get integration health: {e}")
            return {"overall_health": "unknown", "error": str(e)}
    
    def _cleanup_fsm_workflow(self, fsm_workflow_id: str) -> None:
        """Clean up FSM workflow if creation fails."""
        try:
            if self.fsm_system and fsm_workflow_id in self.fsm_system.workflows:
                # Stop workflow if running
                self.fsm_system.stop_workflow(fsm_workflow_id)
                # Remove workflow
                if hasattr(self.fsm_system, 'remove_workflow'):
                    self.fsm_system.remove_workflow(fsm_workflow_id)
                self.logger.info(f"✅ Cleaned up FSM workflow: {fsm_workflow_id}")
        except Exception as e:
            self.logger.error(f"❌ Failed to cleanup FSM workflow: {e}")
    
    def export_integration_report(self, format: str = "json") -> Optional[str]:
        """Export integration system report."""
        try:
            report_data = {
                "integration_status": self.integration_status,
                "health_status": self.get_integration_health(),
                "compliance_workflows": self.list_compliance_workflows(),
                "mappings": {
                    "fsm_to_compliance": self.fsm_compliance_mapping,
                    "compliance_to_fsm": self.compliance_fsm_mapping
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

def create_fsm_compliance_integration() -> FSMComplianceIntegration:
    """Factory function to create FSM compliance integration."""
    return FSMComplianceIntegration()


def get_integration_status() -> Dict[str, Any]:
    """Get current integration status."""
    integration = FSMComplianceIntegration()
    return integration.get_integration_health()


# ============================================================================
# BACKWARDS COMPATIBILITY
# ============================================================================

# Maintain backwards compatibility
FSMComplianceBridge = FSMComplianceIntegration
ComplianceFSMIntegration = FSMComplianceIntegration

# Export all components
__all__ = [
    "FSMComplianceIntegration",
    "FSMComplianceBridge",
    "ComplianceFSMIntegration",
    "create_fsm_compliance_integration",
    "get_integration_status"
]


if __name__ == "__main__":
    # Test integration
    integration = FSMComplianceIntegration()
    
    # Get health status
    health = integration.get_integration_health()
    print(f"Integration Health: {health['overall_health']}")
    
    # Export report
    report = integration.export_integration_report()
    if report:
        print("✅ Integration report exported successfully")
    else:
        print("❌ Failed to export integration report")
