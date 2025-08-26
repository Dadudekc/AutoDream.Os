#!/usr/bin/env python3
"""
FSM Core - V2 Modular Architecture
==================================

Core FSM functionality for state and transition management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4I - FSM System Modularization
License: MIT
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from collections import defaultdict

from .models import (
    StateDefinition, TransitionDefinition, WorkflowInstance,
    StateStatus, TransitionType, WorkflowPriority, StateHandler, TransitionHandler
)
from .types import FSMConfig


logger = logging.getLogger(__name__)


class FSMCore:
    """
    FSM Core - State and Transition Management
    
    Single responsibility: Manage workflow state transitions and execution
    following V2 architecture standards.
    """
    
    def __init__(self, config: Optional[FSMConfig] = None):
        """Initialize FSM core system."""
        self.logger = logging.getLogger(f"{__name__}.FSMCore")
        
        # Core data structures
        self.states: Dict[str, StateDefinition] = {}
        self.transitions: Dict[str, List[TransitionDefinition]] = defaultdict(list)
        self.workflows: Dict[str, WorkflowInstance] = {}
        self.state_handlers: Dict[str, StateHandler] = {}
        self.transition_handlers: Dict[str, TransitionHandler] = {}
        
        # System state
        self.is_running = False
        
        # Configuration
        self.config = config or FSMConfig()
        
        # Statistics
        self.total_workflows_executed = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.total_state_transitions = 0
        
        self.logger.info("✅ FSM Core initialized successfully")
    
    # ============================================================================
    # STATE MANAGEMENT
    # ============================================================================
    
    def add_state(self, state_def: StateDefinition) -> bool:
        """Add a new state to the FSM."""
        try:
            if state_def.name in self.states:
                self.logger.warning(f"State {state_def.name} already exists, updating")
            
            self.states[state_def.name] = state_def
            self.logger.info(f"✅ Added state: {state_def.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add state {state_def.name}: {e}")
            return False
    
    def remove_state(self, state_name: str) -> bool:
        """Remove a state from the FSM."""
        try:
            if state_name not in self.states:
                self.logger.warning(f"State {state_name} not found")
                return False
            
            # Check if state is in use
            for workflow in self.workflows.values():
                if workflow.current_state == state_name:
                    self.logger.error(f"Cannot remove state {state_name} - in use by workflow {workflow.workflow_id}")
                    return False
            
            del self.states[state_name]
            self.logger.info(f"✅ Removed state: {state_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove state {state_name}: {e}")
            return False
    
    def get_state(self, state_name: str) -> Optional[StateDefinition]:
        """Get state definition by name."""
        return self.states.get(state_name)
    
    def list_states(self) -> List[str]:
        """List all available states."""
        return list(self.states.keys())
    
    # ============================================================================
    # TRANSITION MANAGEMENT
    # ============================================================================
    
    def add_transition(self, transition_def: TransitionDefinition) -> bool:
        """Add a new transition to the FSM."""
        try:
            # Validate states exist
            if transition_def.from_state not in self.states:
                self.logger.error(f"From state {transition_def.from_state} not found")
                return False
            
            if transition_def.to_state not in self.states:
                self.logger.error(f"To state {transition_def.to_state} not found")
                return False
            
            # Add transition
            self.transitions[transition_def.from_state].append(transition_def)
            self.logger.info(f"✅ Added transition: {transition_def.from_state} -> {transition_def.to_state}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add transition: {e}")
            return False
    
    def remove_transition(self, from_state: str, to_state: str) -> bool:
        """Remove a transition from the FSM."""
        try:
            if from_state not in self.transitions:
                return False
            
            # Find and remove transition
            transitions = self.transitions[from_state]
            for i, transition in enumerate(transitions):
                if transition.to_state == to_state:
                    del transitions[i]
                    self.logger.info(f"✅ Removed transition: {from_state} -> {to_state}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove transition: {e}")
            return False
    
    def get_transitions(self, from_state: str) -> List[TransitionDefinition]:
        """Get all transitions from a state."""
        return self.transitions.get(from_state, [])
    
    def get_available_transitions(self, current_state: str, context: Dict[str, Any]) -> List[TransitionDefinition]:
        """Get available transitions from current state."""
        available = []
        
        for transition in self.get_transitions(current_state):
            # Check if transition is available
            if self._can_execute_transition(transition, context):
                available.append(transition)
        
        # Sort by priority
        available.sort(key=lambda t: t.priority, reverse=True)
        return available
    
    def _can_execute_transition(self, transition: TransitionDefinition, context: Dict[str, Any]) -> bool:
        """Check if a transition can be executed."""
        try:
            # Check condition if specified
            if transition.condition:
                # Simple condition evaluation (can be extended)
                return self._evaluate_condition(transition.condition, context)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate transition condition: {e}")
            return False
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a transition condition."""
        try:
            # Simple condition evaluation (can be extended with more complex logic)
            if "==" in condition:
                key, value = condition.split("==")
                return str(context.get(key.strip())) == value.strip()
            elif "!=" in condition:
                key, value = condition.split("!=")
                return str(context.get(key.strip())) != value.strip()
            elif ">" in condition:
                key, value = condition.split(">")
                return float(context.get(key.strip(), 0)) > float(value.strip())
            elif "<" in condition:
                key, value = condition.split("<")
                return float(context.get(key.strip(), 0)) < float(value.strip())
            else:
                # Simple key existence check
                return condition.strip() in context
            
        except Exception as e:
            self.logger.error(f"Failed to evaluate condition '{condition}': {e}")
            return False
    
    # ============================================================================
    # WORKFLOW MANAGEMENT
    # ============================================================================
    
    def create_workflow(self, workflow_name: str, initial_state: str, 
                       priority: WorkflowPriority = WorkflowPriority.NORMAL,
                       metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Create a new workflow instance."""
        try:
            # Validate initial state
            if initial_state not in self.states:
                self.logger.error(f"Initial state {initial_state} not found")
                return None
            
            # Generate workflow ID
            workflow_id = f"{workflow_name}_{int(time.time())}_{hash(workflow_name)}"
            
            # Create workflow instance
            workflow = WorkflowInstance(
                workflow_id=workflow_id,
                workflow_name=workflow_name,
                current_state=initial_state,
                state_history=[],
                start_time=time.time(),
                last_update=time.time(),
                status=StateStatus.PENDING,
                priority=priority,
                metadata=metadata or {},
                error_count=0,
                retry_count=0
            )
            
            # Store workflow
            self.workflows[workflow_id] = workflow
            
            self.logger.info(f"✅ Created workflow: {workflow_id} starting at {initial_state}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            return None
    
    def get_workflow(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """Get workflow instance by ID."""
        return self.workflows.get(workflow_id)
    
    def list_workflows(self, status: Optional[StateStatus] = None) -> List[WorkflowInstance]:
        """List workflows with optional status filter."""
        if status is None:
            return list(self.workflows.values())
        
        return [w for w in self.workflows.values() if w.status == status]
    
    # ============================================================================
    # HANDLER MANAGEMENT
    # ============================================================================
    
    def register_state_handler(self, state_name: str, handler: StateHandler) -> bool:
        """Register a state handler."""
        try:
            if state_name not in self.states:
                self.logger.error(f"State {state_name} not found")
                return False
            
            self.state_handlers[state_name] = handler
            self.logger.info(f"✅ Registered state handler for: {state_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register state handler: {e}")
            return False
    
    def register_transition_handler(self, transition_id: str, handler: TransitionHandler) -> bool:
        """Register a transition handler."""
        try:
            self.transition_handlers[transition_id] = handler
            self.logger.info(f"✅ Registered transition handler: {transition_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register transition handler: {e}")
            return False
    
    # ============================================================================
    # SYSTEM CONTROL
    # ============================================================================
    
    def start_system(self) -> bool:
        """Start the FSM system."""
        try:
            if self.is_running:
                self.logger.warning("FSM system is already running")
                return True
            
            self.is_running = True
            self.logger.info("✅ FSM system started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start FSM system: {e}")
            return False
    
    def stop_system(self) -> bool:
        """Stop the FSM system."""
        try:
            if not self.is_running:
                self.logger.warning("FSM system is not running")
                return True
            
            self.is_running = False
            self.logger.info("✅ FSM system stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop FSM system: {e}")
            return False
    
    # ============================================================================
    # STATISTICS AND REPORTING
    # ============================================================================
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get FSM system statistics."""
        return {
            "total_workflows": len(self.workflows),
            "total_states": len(self.states),
            "total_transitions": sum(len(transitions) for transitions in self.transitions.values()),
            "total_workflows_executed": self.total_workflows_executed,
            "successful_workflows": self.successful_workflows,
            "failed_workflows": self.failed_workflows,
            "total_state_transitions": self.total_state_transitions,
            "system_status": "running" if self.is_running else "stopped",
            "last_updated": time.time()
        }
    
    def export_workflow_report(self, workflow_id: str, format: str = "json") -> Optional[str]:
        """Export workflow execution report."""
        try:
            workflow = self.workflows.get(workflow_id)
            if not workflow:
                return None
            
            if format.lower() == "json":
                return json.dumps(workflow.__dict__, indent=2, default=str)
            else:
                return f"Report format '{format}' not supported"
                
        except Exception as e:
            self.logger.error(f"Failed to export workflow report: {e}")
            return None
    
    def clear_history(self) -> None:
        """Clear workflow history."""
        self.workflows.clear()
        self.total_workflows_executed = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.total_state_transitions = 0
        self.logger.info("✅ FSM history cleared")

