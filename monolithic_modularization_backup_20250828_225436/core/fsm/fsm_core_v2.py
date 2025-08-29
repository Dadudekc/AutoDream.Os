from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

    import argparse
from fsm_core import FSMCore, FSMStateManager, FSMWorkflowManager
from fsm_execution import ExecutionEngine, ExecutionMonitor
from fsm_orchestrator import FSMOrchestrator
from fsm_states import (
from fsm_transitions import TransitionManager, TransitionValidator

#!/usr/bin/env python3
"""
FSM Core V2 - Finite State Machine System for Phase 2 Workflow Management
=======================================================================

Refactored for V2 standards compliance: ≤400 LOC, OOP design, SRP compliance.
Main functionality moved to separate modules for maintainability and standards compliance.

Author: Agent-5 (Coding Standards Implementation)
License: MIT
"""


# Import from modular components
    StateStatus, TransitionType, WorkflowPriority,
    StateDefinition, TransitionDefinition, WorkflowInstance
)


class FSMCoreV2:
    """
    FSM Core V2 - Main entry point for FSM system.
    
    Single Responsibility: Provide unified interface to modular FSM components.
    Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.orchestrator = FSMOrchestrator()
        self.initialized = False
        
    def initialize(self, config_path: Optional[str] = None) -> bool:
        """Initialize the FSM Core V2 system."""
        try:
            if self.orchestrator.initialize(config_path):
                self.initialized = True
                self.logger.info("FSM Core V2 initialized successfully")
                return True
            else:
                self.logger.error("Failed to initialize FSM Core V2")
                return False
        except Exception as e:
            self.logger.error(f"FSM Core V2 initialization failed: {e}")
            return False
    
    def create_workflow(self, template_name: str, workflow_id: str, 
                       initial_state: str, metadata: Dict[str, Any] = None) -> Optional[str]:
        """Create a new workflow instance."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return None
        
        return self.orchestrator.create_workflow(template_name, workflow_id, initial_state, metadata)
    
    def start_workflow(self, workflow_id: str, initial_context: Dict[str, Any] = None) -> bool:
        """Start execution of a workflow."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return False
        
        return self.orchestrator.start_workflow(workflow_id, initial_context)
    
    def stop_workflow(self, workflow_id: str) -> bool:
        """Stop execution of a workflow."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return False
        
        return self.orchestrator.stop_workflow(workflow_id)
    
    def get_workflow_status(self, workflow_id: str) -> Optional[StateStatus]:
        """Get current status of a workflow."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return None
        
        return self.orchestrator.get_workflow_status(workflow_id)
    
    def add_state(self, state: StateDefinition) -> bool:
        """Add a new state definition."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return False
        
        return self.orchestrator.add_state(state)
    
    def add_transition(self, transition: TransitionDefinition) -> bool:
        """Add a new transition definition."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return False
        
        return self.orchestrator.add_transition(transition)
    
    def execute_transition(self, workflow_id: str, to_state: str, 
                          context: Dict[str, Any] = None) -> bool:
        """Execute a state transition for a workflow."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return False
        
        return self.orchestrator.execute_transition(workflow_id, to_state, context)
    
    def get_available_transitions(self, workflow_id: str) -> List[TransitionDefinition]:
        """Get available transitions for a workflow."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return []
        
        return self.orchestrator.get_available_transitions(workflow_id)
    
    def get_execution_metrics(self) -> Dict[str, Any]:
        """Get execution metrics."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return {}
        
        return self.orchestrator.get_execution_metrics()
    
    def get_workflow_performance(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a specific workflow."""
        if not self.initialized:
            self.logger.error("FSM Core V2 not initialized")
            return None
        
        return self.orchestrator.get_workflow_performance(workflow_id)
    
    def shutdown(self) -> None:
        """Shutdown the FSM Core V2 system."""
        try:
            self.orchestrator.shutdown()
            self.initialized = False
            self.logger.info("FSM Core V2 shutdown complete")
        except Exception as e:
            self.logger.error(f"Failed to shutdown FSM Core V2: {e}")
    
    # Convenience methods for backward compatibility
    def get_state_manager(self):
        """Get the state manager instance."""
        return self.orchestrator.core.get_state_manager()
    
    def get_workflow_manager(self):
        """Get the workflow manager instance."""
        return self.orchestrator.core.get_workflow_manager()
    
    def get_transition_manager(self):
        """Get the transition manager instance."""
        return self.orchestrator.transition_manager
    
    def get_execution_engine(self):
        """Get the execution engine instance."""
        return self.orchestrator.execution_engine


# Legacy compatibility - maintain backward compatibility
FSMCore = FSMCoreV2


def main():
    """CLI interface for FSM Core V2 testing."""
    
    parser = argparse.ArgumentParser(description="FSM Core V2 - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    parser.add_argument("--config", type=str, help="Configuration file path")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    elif args.config:
        fsm_core = FSMCoreV2()
        if fsm_core.initialize(args.config):
            print("✅ FSM Core V2 initialized successfully")
        else:
            print("❌ FSM Core V2 initialization failed")
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for FSM Core V2."""
    print("🧪 Running FSM Core V2 smoke tests...")
    
    # Test core creation
    fsm_core = FSMCoreV2()
    assert fsm_core is not None
    print("✅ FSM Core V2 creation test passed")
    
    # Test initialization
    assert fsm_core.initialize() is True
    print("✅ Initialization test passed")
    
    # Test workflow creation (with mock template)
    # First add a mock template to the orchestrator
    fsm_core.orchestrator.workflow_templates["test_template"] = {
        "name": "test_template",
        "description": "Test workflow template"
    }
    
    workflow_id = fsm_core.create_workflow("test_template", "test_workflow", "initial")
    assert workflow_id == "test_workflow"
    print("✅ Workflow creation test passed")
    
    # Test metrics
    metrics = fsm_core.get_execution_metrics()
    assert isinstance(metrics, dict)
    print("✅ Metrics test passed")
    
    # Test shutdown
    fsm_core.shutdown()
    print("✅ Shutdown test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
