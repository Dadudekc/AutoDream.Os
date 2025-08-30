#!/usr/bin/env python3
"""
V2 Workflow Engine Definitions - Consolidated Workflow Configuration
==================================================================

Consolidated workflow engine definitions extracted from agent_workspaces/workflows.
Integrates valuable workflow engine configuration into main workflow systems.

Author: Agent-1 (PERPETUAL MOTION LEADER - WORKFLOWS INTEGRATION SPECIALIST)
License: MIT
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

from ..types.workflow_enums import WorkflowStatus, TaskStatus
from ..types.workflow_models import WorkflowDefinition, WorkflowExecution


@dataclass
class V2WorkflowEngineConfig:
    """V2 Workflow Engine configuration extracted from workflows workspace"""
    
    max_concurrent_workflows: int = 100
    max_workflow_duration_hours: int = 168
    auto_cleanup_enabled: bool = True
    cleanup_interval_hours: int = 24
    performance_monitoring: bool = True
    error_handling: str = "graceful_degradation"
    
    # State management
    persistence: str = "database"
    checkpointing: bool = True
    checkpoint_interval_minutes: int = 5
    recovery_enabled: bool = True
    rollback_support: bool = True
    
    # Performance requirements
    max_workflow_startup_time_ms: int = 1000
    max_state_transition_time_ms: int = 500
    max_task_execution_time_ms: int = 30000
    throughput_workflows_per_minute: int = 60
    availability_percentage: float = 99.9
    error_rate_threshold: float = 0.01


@dataclass
class V2WorkflowState:
    """V2 Workflow state definition"""
    
    state_id: str
    state_name: str
    state_type: str
    allowed_transitions: List[str]
    actions: List[str]


@dataclass
class V2WorkflowComponent:
    """V2 Workflow component definition"""
    
    component_id: str
    component_name: str
    component_type: str
    responsibilities: List[str]
    dependencies: List[str]


class V2WorkflowEngineDefinitions:
    """
    Consolidated V2 Workflow Engine definitions.
    
    Single Responsibility: Provide unified access to V2 workflow engine
    configurations extracted from agent_workspaces/workflows.
    """
    
    def __init__(self):
        self.config = V2WorkflowEngineConfig()
        self.workflow_states = self._initialize_workflow_states()
        self.workflow_components = self._initialize_workflow_components()
        self.execution_modes = [
            "synchronous", "asynchronous", "parallel", 
            "sequential", "conditional"
        ]
        self.integration_points = {
            "messaging_system": "v2_message_queue",
            "task_manager": "v2_task_manager",
            "agent_coordinator": "v2_agent_coordinator",
            "performance_monitor": "v2_performance_monitor",
            "database_system": "v2_database",
            "logging_system": "v2_logging",
            "alert_system": "v2_alert_manager"
        }
        self.security_settings = {
            "authentication_required": True,
            "authorization_enabled": True,
            "audit_logging": True,
            "encryption_level": "standard",
            "access_control": "role_based"
        }
    
    def _initialize_workflow_states(self) -> List[V2WorkflowState]:
        """Initialize workflow states from V2 configuration"""
        return [
            V2WorkflowState(
                state_id="initialized",
                state_name="Initialized",
                state_type="start",
                allowed_transitions=["active", "cancelled"],
                actions=["validate_inputs", "allocate_resources", "initialize_agents"]
            ),
            V2WorkflowState(
                state_id="active",
                state_name="Active",
                state_type="processing",
                allowed_transitions=["paused", "completed", "failed", "cancelled"],
                actions=["execute_tasks", "monitor_progress", "handle_events"]
            ),
            V2WorkflowState(
                state_id="paused",
                state_name="Paused",
                state_type="waiting",
                allowed_transitions=["active", "cancelled"],
                actions=["save_state", "notify_stakeholders", "wait_for_resume"]
            ),
            V2WorkflowState(
                state_id="completed",
                state_name="Completed",
                state_type="final",
                allowed_transitions=[],
                actions=["generate_report", "cleanup_resources", "notify_completion"]
            ),
            V2WorkflowState(
                state_id="failed",
                state_name="Failed",
                state_type="final",
                allowed_transitions=["retry", "cancelled"],
                actions=["log_error", "notify_failure", "initiate_recovery"]
            ),
            V2WorkflowState(
                state_id="cancelled",
                state_name="Cancelled",
                state_type="final",
                allowed_transitions=[],
                actions=["cleanup_resources", "notify_cancellation", "log_reason"]
            )
        ]
    
    def _initialize_workflow_components(self) -> List[V2WorkflowComponent]:
        """Initialize workflow components from V2 configuration"""
        return [
            V2WorkflowComponent(
                component_id="workflow_scheduler",
                component_name="Workflow Scheduler",
                component_type="scheduler",
                responsibilities=[
                    "workflow_prioritization",
                    "resource_allocation",
                    "execution_timing",
                    "load_balancing"
                ],
                dependencies=["task_manager", "resource_monitor"]
            ),
            V2WorkflowComponent(
                component_id="workflow_executor",
                component_name="Workflow Executor",
                component_type="executor",
                responsibilities=[
                    "task_execution",
                    "state_transitions",
                    "error_handling",
                    "performance_monitoring"
                ],
                dependencies=["agent_coordinator", "messaging_system"]
            ),
            V2WorkflowComponent(
                component_id="workflow_monitor",
                component_name="Workflow Monitor",
                component_type="monitor",
                responsibilities=[
                    "progress_tracking",
                    "performance_metrics",
                    "alert_generation",
                    "health_monitoring"
                ],
                dependencies=["performance_monitor", "alert_system"]
            ),
            V2WorkflowComponent(
                component_id="workflow_persister",
                component_name="Workflow Persister",
                component_type="persistence",
                responsibilities=[
                    "state_persistence",
                    "checkpoint_management",
                    "recovery_support",
                    "audit_logging"
                ],
                dependencies=["database_system", "logging_system"]
            )
        ]
    
    def get_workflow_state(self, state_id: str) -> Optional[V2WorkflowState]:
        """Get workflow state by ID"""
        for state in self.workflow_states:
            if state.state_id == state_id:
                return state
        return None
    
    def get_workflow_component(self, component_id: str) -> Optional[V2WorkflowComponent]:
        """Get workflow component by ID"""
        for component in self.workflow_components:
            if component.component_id == component_id:
                return component
        return None
    
    def get_allowed_transitions(self, current_state: str) -> List[str]:
        """Get allowed transitions from current state"""
        state = self.get_workflow_state(current_state)
        return state.allowed_transitions if state else []
    
    def get_state_actions(self, state_id: str) -> List[str]:
        """Get actions for a specific state"""
        state = self.get_workflow_state(state_id)
        return state.actions if state else []
    
    def validate_state_transition(self, from_state: str, to_state: str) -> bool:
        """Validate if state transition is allowed"""
        allowed = self.get_allowed_transitions(from_state)
        return to_state in allowed
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary for integration"""
        return {
            "engine_config": {
                "max_concurrent_workflows": self.config.max_concurrent_workflows,
                "max_workflow_duration_hours": self.config.max_workflow_duration_hours,
                "auto_cleanup_enabled": self.config.auto_cleanup_enabled,
                "cleanup_interval_hours": self.config.cleanup_interval_hours,
                "performance_monitoring": self.config.performance_monitoring,
                "error_handling": self.config.error_handling
            },
            "state_management": {
                "persistence": self.config.persistence,
                "checkpointing": self.config.checkpointing,
                "checkpoint_interval_minutes": self.config.checkpoint_interval_minutes,
                "recovery_enabled": self.config.recovery_enabled,
                "rollback_support": self.config.rollback_support
            },
            "performance_requirements": {
                "max_workflow_startup_time_ms": self.config.max_workflow_startup_time_ms,
                "max_state_transition_time_ms": self.config.max_state_transition_time_ms,
                "max_task_execution_time_ms": self.config.max_task_execution_time_ms,
                "throughput_workflows_per_minute": self.config.throughput_workflows_per_minute,
                "availability_percentage": self.config.availability_percentage,
                "error_rate_threshold": self.config.error_rate_threshold
            },
            "total_states": len(self.workflow_states),
            "total_components": len(self.workflow_components),
            "execution_modes": self.execution_modes,
            "integration_points": self.integration_points,
            "security_settings": self.security_settings
        }


# Global instance for easy access
v2_workflow_definitions = V2WorkflowEngineDefinitions()


def get_v2_workflow_definitions() -> V2WorkflowEngineDefinitions:
    """Get global V2 workflow definitions instance"""
    return v2_workflow_definitions


def export_v2_config_to_json() -> Dict[str, Any]:
    """Export V2 configuration to JSON format for external use"""
    definitions = get_v2_workflow_definitions()
    return definitions.get_config_summary()


if __name__ == "__main__":
    # CLI interface for testing and validation
    definitions = get_v2_workflow_definitions()
    
    print("🚀 V2 Workflow Engine Definitions - Integration Test")
    print("=" * 60)
    
    # Test configuration access
    config_summary = definitions.get_config_summary()
    print(f"✅ Configuration loaded: {len(definitions.workflow_states)} states, {len(definitions.workflow_components)} components")
    
    # Test state validation
    print(f"✅ State transitions: initialized → active: {definitions.validate_state_transition('initialized', 'active')}")
    print(f"✅ State transitions: active → completed: {definitions.validate_state_transition('active', 'completed')}")
    
    # Test component access
    scheduler = definitions.get_workflow_component("workflow_scheduler")
    if scheduler:
        print(f"✅ Component found: {scheduler.component_name} ({scheduler.component_type})")
    
    print("🎉 V2 Workflow Engine Definitions integration test completed successfully!")
