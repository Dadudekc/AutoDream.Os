#!/usr/bin/env python3
"""
FSM State Manager - State Definition and Management Operations
============================================================

Handles state definition, validation, and management operations.
Follows V2 standards: focused responsibility, clear state operations.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

import logging
from typing import Dict, List, Optional, Any, Set

from .fsm_data_models import StateDefinition, validate_state_definition


# ============================================================================
# STATE MANAGER CLASS
# ============================================================================


class FSMStateManager:
    """Manages FSM state definitions and operations."""

    def __init__(self):
        """Initialize state manager."""
        self.logger = logging.getLogger(f"{__name__}.FSMStateManager")
        self.states: Dict[str, StateDefinition] = {}
        self.state_dependencies: Dict[str, Set[str]] = {}
        self.state_resources: Dict[str, Set[str]] = {}

    def add_state(self, state_def: StateDefinition) -> bool:
        """Add a new state to the FSM.
        
        Args:
            state_def (StateDefinition): State definition to add.
            
        Returns:
            bool: True if state was added successfully.
        """
        try:
            # Validate state definition
            if not validate_state_definition(state_def):
                self.logger.error(f"Invalid state definition for {state_def.name}")
                return False

            # Check for existing state
            if state_def.name in self.states:
                self.logger.warning(f"State {state_def.name} already exists, updating")

            # Add state
            self.states[state_def.name] = state_def
            
            # Track dependencies
            self.state_dependencies[state_def.name] = set(state_def.dependencies)
            
            # Track resources
            self.state_resources[state_def.name] = set(state_def.required_resources)

            self.logger.info(f"✅ Added state: {state_def.name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add state {state_def.name}: {e}")
            return False

    def remove_state(self, state_name: str, force: bool = False) -> bool:
        """Remove a state from the FSM.
        
        Args:
            state_name (str): Name of state to remove.
            force (bool): Force removal even if state is in use.
            
        Returns:
            bool: True if state was removed successfully.
        """
        try:
            if state_name not in self.states:
                self.logger.warning(f"State {state_name} not found")
                return False

            # Check if state is in use (unless forced)
            if not force and self._is_state_in_use(state_name):
                self.logger.error(
                    f"Cannot remove state {state_name} - in use by active workflows"
                )
                return False

            # Remove state
            del self.states[state_name]
            
            # Clean up tracking
            self.state_dependencies.pop(state_name, None)
            self.state_resources.pop(state_name, None)

            self.logger.info(f"✅ Removed state: {state_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to remove state {state_name}: {e}")
            return False

    def get_state(self, state_name: str) -> Optional[StateDefinition]:
        """Get state definition by name.
        
        Args:
            state_name (str): Name of state to retrieve.
            
        Returns:
            Optional[StateDefinition]: State definition or None if not found.
        """
        return self.states.get(state_name)

    def list_states(self) -> List[str]:
        """Get list of all state names.
        
        Returns:
            List[str]: List of state names.
        """
        return list(self.states.keys())

    def get_states_by_resource(self, resource: str) -> List[str]:
        """Get states that require a specific resource.
        
        Args:
            resource (str): Resource name to search for.
            
        Returns:
            List[str]: List of state names requiring the resource.
        """
        return [
            state_name for state_name, resources in self.state_resources.items()
            if resource in resources
        ]

    def get_states_by_dependency(self, dependency: str) -> List[str]:
        """Get states that depend on a specific state.
        
        Args:
            dependency (str): State name to search for dependencies.
            
        Returns:
            List[str]: List of state names depending on the specified state.
        """
        return [
            state_name for state_name, deps in self.state_dependencies.items()
            if dependency in deps
        ]

    def validate_state_transition(self, from_state: str, to_state: str) -> bool:
        """Validate if a state transition is possible.
        
        Args:
            from_state (str): Source state name.
            to_state (str): Target state name.
            
        Returns:
            bool: True if transition is valid.
        """
        try:
            # Check if both states exist
            if from_state not in self.states or to_state not in self.states:
                return False

            # Check for circular dependencies
            if self._would_create_circular_dependency(from_state, to_state):
                return False

            return True

        except Exception as e:
            self.logger.error(f"Failed to validate transition {from_state} -> {to_state}: {e}")
            return False

    def get_state_statistics(self) -> Dict[str, Any]:
        """Get statistics about states.
        
        Returns:
            Dict[str, Any]: State statistics.
        """
        try:
            total_states = len(self.states)
            states_with_timeouts = sum(
                1 for state in self.states.values() 
                if state.timeout_seconds is not None
            )
            states_with_retries = sum(
                1 for state in self.states.values() 
                if state.retry_count > 0
            )
            
            return {
                "total_states": total_states,
                "states_with_timeouts": states_with_timeouts,
                "states_with_retries": states_with_retries,
                "average_retry_count": sum(
                    state.retry_count for state in self.states.values()
                ) / total_states if total_states > 0 else 0,
                "average_timeout": sum(
                    state.timeout_seconds or 0 for state in self.states.values()
                ) / total_states if total_states > 0 else 0,
            }

        except Exception as e:
            self.logger.error(f"Failed to get state statistics: {e}")
            return {}

    def export_state_definitions(self, format: str = "dict") -> Any:
        """Export all state definitions.
        
        Args:
            format (str): Export format ("dict" or "json").
            
        Returns:
            Any: Exported state definitions.
        """
        try:
            if format.lower() == "dict":
                return {
                    name: {
                        "name": state.name,
                        "description": state.description,
                        "entry_actions": state.entry_actions,
                        "exit_actions": state.exit_actions,
                        "timeout_seconds": state.timeout_seconds,
                        "retry_count": state.retry_count,
                        "retry_delay": state.retry_delay,
                        "required_resources": state.required_resources,
                        "dependencies": state.dependencies,
                        "metadata": state.metadata,
                    }
                    for name, state in self.states.items()
                }
            elif format.lower() == "json":
                import json
                return json.dumps(self.export_state_definitions("dict"), indent=2)
            else:
                self.logger.error(f"Unsupported export format: {format}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to export state definitions: {e}")
            return None

    def clear_states(self) -> None:
        """Clear all state definitions."""
        self.states.clear()
        self.state_dependencies.clear()
        self.state_resources.clear()
        self.logger.info("✅ All states cleared")

    # ============================================================================
    # PRIVATE METHODS
    # ============================================================================

    def _is_state_in_use(self, state_name: str) -> bool:
        """Check if a state is currently in use by active workflows."""
        # This would need to be implemented based on workflow tracking
        # For now, return False to allow removal
        return False

    def _would_create_circular_dependency(self, from_state: str, to_state: str) -> bool:
        """Check if adding a transition would create a circular dependency."""
        # Simple circular dependency check
        if from_state == to_state:
            return True
        
        # Check if to_state already depends on from_state
        if from_state in self.state_dependencies.get(to_state, set()):
            return True
            
        return False


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def create_state_manager() -> FSMStateManager:
    """Create a new state manager instance."""
    return FSMStateManager()


def validate_state_manager(state_manager: FSMStateManager) -> bool:
    """Validate state manager configuration."""
    try:
        # Check for basic configuration
        if not isinstance(state_manager.states, dict):
            return False
            
        # Validate all states
        for state_name, state_def in state_manager.states.items():
            if not validate_state_definition(state_def):
                return False
                
        return True
        
    except Exception:
        return False


# ============================================================================
# EXPORTS
# ============================================================================


__all__ = [
    "FSMStateManager",
    "create_state_manager",
    "validate_state_manager",
]
