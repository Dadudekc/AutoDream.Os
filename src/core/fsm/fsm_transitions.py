#!/usr/bin/env python3
"""
FSM Transitions - State transition management for FSM system

Single Responsibility: Manage state transitions and transition logic.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""

import logging
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from fsm.states import TransitionType, TransitionDefinition, TransitionResult, StateStatus


class TransitionManager:
    """Manages state transitions and transition logic."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.transitions: Dict[str, TransitionDefinition] = {}
        self.transition_handlers: Dict[str, Callable] = {}
        self.transition_history: List[TransitionResult] = []
        
    def add_transition(self, transition: TransitionDefinition) -> bool:
        """Add a new transition definition."""
        try:
            key = self._get_transition_key(transition.from_state, transition.to_state)
            self.transitions[key] = transition
            self.logger.info(f"Added transition: {key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add transition: {e}")
            return False
    
    def get_transition(self, from_state: str, to_state: str) -> Optional[TransitionDefinition]:
        """Get transition definition between two states."""
        key = self._get_transition_key(from_state, to_state)
        return self.transitions.get(key)
    
    def get_available_transitions(self, from_state: str) -> List[TransitionDefinition]:
        """Get all available transitions from a state."""
        available = []
        for transition in self.transitions.values():
            if transition.from_state == from_state:
                available.append(transition)
        return available
    
    def can_transition(self, from_state: str, to_state: str) -> bool:
        """Check if transition is allowed."""
        key = self._get_transition_key(from_state, to_state)
        return key in self.transitions
    
    def execute_transition(self, from_state: str, to_state: str, 
                          workflow_id: str, context: Dict[str, Any] = None) -> TransitionResult:
        """Execute a state transition."""
        start_time = time.time()
        
        try:
            # Validate transition
            if not self.can_transition(from_state, to_state):
                error_msg = f"Invalid transition: {from_state} -> {to_state}"
                self.logger.error(error_msg)
                return TransitionResult(
                    from_state=from_state,
                    to_state=to_state,
                    success=False,
                    transition_time=time.time() - start_time,
                    error_message=error_msg
                )
            
            # Get transition definition
            transition = self.get_transition(from_state, to_state)
            if not transition:
                error_msg = f"Transition definition not found: {from_state} -> {to_state}"
                self.logger.error(error_msg)
                return TransitionResult(
                    from_state=from_state,
                    to_state=to_state,
                    success=False,
                    transition_time=time.time() - start_time,
                    error_message=error_msg
                )
            
            # Check transition conditions
            if not self._evaluate_conditions(transition, context):
                error_msg = f"Transition conditions not met: {from_state} -> {to_state}"
                self.logger.warning(error_msg)
                return TransitionResult(
                    from_state=from_state,
                    to_state=to_state,
                    success=False,
                    transition_time=time.time() - start_time,
                    error_message=error_msg
                )
            
            # Execute transition actions
            executed_actions = self._execute_transition_actions(transition, workflow_id, context)
            
            # Record transition
            transition_time = time.time() - start_time
            result = TransitionResult(
                from_state=from_state,
                to_state=to_state,
                success=True,
                transition_time=transition_time,
                executed_actions=executed_actions,
                metadata={"workflow_id": workflow_id, "context": context}
            )
            
            self.transition_history.append(result)
            self.logger.info(f"Transition executed: {from_state} -> {to_state} in {transition_time:.3f}s")
            
            return result
            
        except Exception as e:
            error_msg = f"Transition execution failed: {e}"
            self.logger.error(error_msg)
            return TransitionResult(
                from_state=from_state,
                to_state=to_state,
                success=False,
                transition_time=time.time() - start_time,
                error_message=error_msg
            )
    
    def _get_transition_key(self, from_state: str, to_state: str) -> str:
        """Generate transition key."""
        return f"{from_state}->{to_state}"
    
    def _evaluate_conditions(self, transition: TransitionDefinition, context: Dict[str, Any]) -> bool:
        """Evaluate transition conditions."""
        if not transition.condition:
            return True
        
        try:
            # Simple condition evaluation (can be extended with more sophisticated logic)
            if context and transition.condition in context:
                return bool(context[transition.condition])
            return True
        except Exception as e:
            self.logger.warning(f"Failed to evaluate condition {transition.condition}: {e}")
            return True
    
    def _execute_transition_actions(self, transition: TransitionDefinition, 
                                  workflow_id: str, context: Dict[str, Any]) -> List[str]:
        """Execute transition actions."""
        executed_actions = []
        
        for action in transition.actions:
            try:
                if action in self.transition_handlers:
                    self.transition_handlers[action](workflow_id, context)
                    executed_actions.append(action)
                    self.logger.debug(f"Executed action: {action}")
                else:
                    self.logger.warning(f"Action handler not found: {action}")
            except Exception as e:
                self.logger.error(f"Failed to execute action {action}: {e}")
        
        return executed_actions
    
    def register_transition_handler(self, action_name: str, handler: Callable) -> None:
        """Register a handler for a specific transition action."""
        self.transition_handlers[action_name] = handler
        self.logger.info(f"Registered transition handler for action: {action_name}")
    
    def get_transition_history(self, workflow_id: Optional[str] = None) -> List[TransitionResult]:
        """Get transition history, optionally filtered by workflow."""
        if workflow_id:
            return [t for t in self.transition_history 
                   if t.metadata and t.metadata.get("workflow_id") == workflow_id]
        return self.transition_history
    
    def clear_transition_history(self) -> None:
        """Clear transition history."""
        self.transition_history.clear()
        self.logger.info("Transition history cleared")


class TransitionValidator:
    """Validates transition definitions and logic."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_errors: List[str] = []
    
    def validate_transition(self, transition: TransitionDefinition) -> bool:
        """Validate a single transition definition."""
        self.validation_errors.clear()
        
        # Check required fields
        if not transition.from_state:
            self.validation_errors.append("from_state is required")
        
        if not transition.to_state:
            self.validation_errors.append("to_state is required")
        
        if transition.from_state == transition.to_state:
            self.validation_errors.append("from_state and to_state cannot be the same")
        
        # Check transition type
        if not isinstance(transition.transition_type, TransitionType):
            self.validation_errors.append("Invalid transition_type")
        
        # Check priority
        if transition.priority < 0:
            self.validation_errors.append("Priority must be non-negative")
        
        # Check timeout
        if transition.timeout_seconds is not None and transition.timeout_seconds < 0:
            self.validation_errors.append("Timeout must be non-negative")
        
        return len(self.validation_errors) == 0
    
    def validate_transition_set(self, transitions: List[TransitionDefinition]) -> bool:
        """Validate a set of transitions for consistency."""
        self.validation_errors.clear()
        
        # Check for duplicate transitions
        transition_keys = set()
        for transition in transitions:
            key = f"{transition.from_state}->{transition.to_state}"
            if key in transition_keys:
                self.validation_errors.append(f"Duplicate transition: {key}")
            transition_keys.add(key)
        
        # Check for circular references
        if self._has_circular_references(transitions):
            self.validation_errors.append("Circular references detected in transitions")
        
        return len(self.validation_errors) == 0
    
    def _has_circular_references(self, transitions: List[TransitionDefinition]) -> bool:
        """Check for circular references in transitions."""
        # Simple cycle detection using DFS
        graph = {}
        for transition in transitions:
            if transition.from_state not in graph:
                graph[transition.from_state] = []
            graph[transition.from_state].append(transition.to_state)
        
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return True
        
        return False
    
    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors."""
        return self.validation_errors.copy()


def main():
    """CLI interface for FSM Transitions testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="FSM Transitions - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for FSM Transitions."""
    print("🧪 Running FSM Transitions smoke tests...")
    
    # Test transition manager
    manager = TransitionManager()
    assert manager is not None
    print("✅ TransitionManager creation test passed")
    
    # Test transition validator
    validator = TransitionValidator()
    assert validator is not None
    print("✅ TransitionValidator creation test passed")
    
    # Test transition key generation
    key = manager._get_transition_key("state1", "state2")
    assert key == "state1->state2"
    print("✅ Transition key generation test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
