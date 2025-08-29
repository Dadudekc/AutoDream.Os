#!/usr/bin/env python3
"""
FSM Core - Core Finite State Machine Logic

Single Responsibility: Core FSM state management and transitions.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""

import logging
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union, Set
from collections import defaultdict, deque

from fsm.states import StateStatus, TransitionType, WorkflowPriority
from fsm_models import StateDefinition, TransitionDefinition, WorkflowInstance


class FSMStateManager:
    """Manages FSM state transitions and execution."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.states: Dict[str, StateDefinition] = {}
        self.transitions: Dict[str, TransitionDefinition] = {}
        self.workflows: Dict[str, WorkflowInstance] = {}
        self.state_handlers: Dict[str, Callable] = {}
        
    def add_state(self, state: StateDefinition) -> bool:
        """Add a new state definition."""
        try:
            self.states[state.name] = state
            self.logger.info(f"Added state: {state.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add state {state.name}: {e}")
            return False
    
    def add_transition(self, transition: TransitionDefinition) -> bool:
        """Add a new transition definition."""
        try:
            key = f"{transition.from_state}->{transition.to_state}"
            self.transitions[key] = transition
            self.logger.info(f"Added transition: {key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add transition {key}: {e}")
            return False
    
    def get_available_transitions(self, current_state: str) -> List[TransitionDefinition]:
        """Get available transitions from current state."""
        available = []
        for key, transition in self.transitions.items():
            if transition.from_state == current_state:
                available.append(transition)
        return available
    
    def can_transition(self, from_state: str, to_state: str) -> bool:
        """Check if transition is allowed."""
        key = f"{from_state}->{to_state}"
        return key in self.transitions
    
    def execute_transition(self, workflow_id: str, to_state: str) -> bool:
        """Execute state transition for workflow."""
        try:
            if workflow_id not in self.workflows:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False
            
            workflow = self.workflows[workflow_id]
            current_state = workflow.current_state
            
            if not self.can_transition(current_state, to_state):
                self.logger.error(f"Invalid transition: {current_state} -> {to_state}")
                return False
            
            # Execute exit actions for current state
            if current_state in self.states:
                self._execute_actions(workflow_id, self.states[current_state].exit_actions)
            
            # Update workflow state
            workflow.current_state = to_state
            workflow.last_transition = datetime.now()
            
            # Execute entry actions for new state
            if to_state in self.states:
                self._execute_actions(workflow_id, self.states[to_state].entry_actions)
            
            self.logger.info(f"Transitioned workflow {workflow_id}: {current_state} -> {to_state}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to execute transition: {e}")
            return False
    
    def _execute_actions(self, workflow_id: str, actions: List[str]) -> None:
        """Execute a list of actions for a workflow."""
        for action in actions:
            try:
                if action in self.state_handlers:
                    self.state_handlers[action](workflow_id)
                else:
                    self.logger.warning(f"Action handler not found: {action}")
            except Exception as e:
                self.logger.error(f"Failed to execute action {action}: {e}")
    
    def register_state_handler(self, action_name: str, handler: Callable) -> None:
        """Register a handler for a specific action."""
        self.state_handlers[action_name] = handler
        self.logger.info(f"Registered handler for action: {action_name}")
    
    def get_current_time(self) -> datetime:
        """Get current time for workflow timestamps."""
        return datetime.now()


class FSMWorkflowManager:
    """Manages workflow instances and lifecycle."""
    
    def __init__(self, state_manager: FSMStateManager):
        self.state_manager = state_manager
        self.logger = logging.getLogger(__name__)
        self.workflow_templates: Dict[str, Dict] = {}
    
    def create_workflow(self, template_name: str, workflow_id: str, 
                       initial_state: str, metadata: Dict[str, Any] = None) -> Optional[str]:
        """Create a new workflow instance."""
        try:
            if template_name not in self.workflow_templates:
                self.logger.error(f"Workflow template {template_name} not found")
                return None
            
            workflow = WorkflowInstance(
                workflow_id=workflow_id,
                workflow_name=template_name,
                current_state=initial_state,
                created_at=datetime.now(),
                last_transition=datetime.now(),
                metadata=metadata or {}
            )
            
            self.state_manager.workflows[workflow_id] = workflow
            self.logger.info(f"Created workflow: {workflow_id}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            return None
    
    def start_workflow(self, workflow_id: str) -> bool:
        """Start a workflow execution."""
        try:
            if workflow_id not in self.state_manager.workflows:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False
            
            workflow = self.state_manager.workflows[workflow_id]
            workflow.status = StateStatus.ACTIVE
            workflow.started_at = datetime.now()
            
            # Execute entry actions for initial state
            current_state = workflow.current_state
            if current_state in self.state_manager.states:
                self.state_manager._execute_actions(
                    workflow_id, 
                    self.state_manager.states[current_state].entry_actions
                )
            
            self.logger.info(f"Started workflow: {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start workflow {workflow_id}: {e}")
            return False
    
    def complete_workflow(self, workflow_id: str) -> bool:
        """Mark workflow as completed."""
        try:
            if workflow_id not in self.state_manager.workflows:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False
            
            workflow = self.state_manager.workflows[workflow_id]
            workflow.status = StateStatus.COMPLETED
            workflow.completed_at = datetime.now()
            
            self.logger.info(f"Completed workflow: {workflow_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to complete workflow {workflow_id}: {e}")
            return False
    
    def get_workflow_status(self, workflow_id: str) -> Optional[StateStatus]:
        """Get current status of a workflow."""
        if workflow_id in self.state_manager.workflows:
            return self.state_manager.workflows[workflow_id].status
        return None


class FSMCore:
    """Main FSM Core orchestrator."""
    
    def __init__(self):
        self.state_manager = FSMStateManager()
        self.workflow_manager = FSMWorkflowManager(self.state_manager)
        self.logger = logging.getLogger(__name__)
    
    def initialize(self, config_path: Optional[str] = None) -> bool:
        """Initialize the FSM core system."""
        try:
            if config_path and Path(config_path).exists():
                self._load_configuration(config_path)
            
            self.logger.info("FSM Core initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize FSM Core: {e}")
            return False
    
    def _load_configuration(self, config_path: str) -> None:
        """Load FSM configuration from file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Load states
            for state_data in config.get('states', []):
                state = StateDefinition(**state_data)
                self.state_manager.add_state(state)
            
            # Load transitions
            for transition_data in config.get('transitions', []):
                transition = TransitionDefinition(**transition_data)
                self.state_manager.add_transition(transition)
            
            # Load workflow templates
            self.workflow_manager.workflow_templates = config.get('workflow_templates', {})
            
            self.logger.info(f"Loaded configuration from: {config_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
    
    def get_state_manager(self) -> FSMStateManager:
        """Get the state manager instance."""
        return self.state_manager
    
    def get_workflow_manager(self) -> FSMWorkflowManager:
        """Get the workflow manager instance."""
        return self.workflow_manager


def main():
    """CLI interface for FSM Core testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="FSM Core - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    parser.add_argument("--config", type=str, help="Configuration file path")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    elif args.config:
        fsm_core = FSMCore()
        if fsm_core.initialize(args.config):
            print("✅ FSM Core initialized successfully")
        else:
            print("❌ FSM Core initialization failed")
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for FSM Core."""
    print("🧪 Running FSM Core smoke tests...")
    
    # Test basic initialization
    fsm_core = FSMCore()
    assert fsm_core is not None
    print("✅ Basic initialization test passed")
    
    # Test state manager
    state_manager = fsm_core.get_state_manager()
    assert state_manager is not None
    print("✅ State manager test passed")
    
    # Test workflow manager
    workflow_manager = fsm_core.get_workflow_manager()
    assert workflow_manager is not None
    print("✅ Workflow manager test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
