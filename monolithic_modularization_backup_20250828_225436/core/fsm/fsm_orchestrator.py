#!/usr/bin/env python3
"""
FSM Orchestrator - Main orchestrator for FSM system

Single Responsibility: Coordinate and orchestrate all FSM components.
Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
"""

import logging
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

from fsm_core import FSMCore, FSMStateManager, FSMWorkflowManager
from fsm_states import StateDefinition, TransitionDefinition, WorkflowInstance, StateStatus
from fsm_transitions import TransitionManager, TransitionValidator
from fsm_execution import ExecutionEngine, ExecutionMonitor


class FSMOrchestrator:
    """Main orchestrator for the FSM system."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.core = FSMCore()
        self.transition_manager = TransitionManager()
        self.transition_validator = TransitionValidator()
        self.execution_engine = ExecutionEngine(self.transition_manager)
        self.execution_monitor = ExecutionMonitor(self.execution_engine)
        self.workflow_templates: Dict[str, Dict[str, Any]] = {}
        
    def initialize(self, config_path: Optional[str] = None) -> bool:
        """Initialize the FSM orchestrator system."""
        try:
            # Initialize core components
            if not self.core.initialize(config_path):
                self.logger.error("Failed to initialize FSM core")
                return False
            
            # Load workflow templates
            if config_path:
                self._load_workflow_templates(config_path)
            
            # Register default transition handlers
            self._register_default_handlers()
            
            self.logger.info("FSM Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize FSM Orchestrator: {e}")
            return False
    
    def _load_workflow_templates(self, config_path: str) -> None:
        """Load workflow templates from configuration."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self.workflow_templates = config.get('workflow_templates', {})
            self.logger.info(f"Loaded {len(self.workflow_templates)} workflow templates")
            
        except Exception as e:
            self.logger.error(f"Failed to load workflow templates: {e}")
    
    def _register_default_handlers(self) -> None:
        """Register default transition action handlers."""
        try:
            # Register basic action handlers
            self.transition_manager.register_transition_handler(
                "log_transition", self._log_transition_handler
            )
            self.transition_manager.register_transition_handler(
                "update_metadata", self._update_metadata_handler
            )
            self.transition_manager.register_transition_handler(
                "notify_completion", self._notify_completion_handler
            )
            
            self.logger.info("Registered default transition handlers")
            
        except Exception as e:
            self.logger.error(f"Failed to register default handlers: {e}")
    
    def create_workflow(self, template_name: str, workflow_id: str, 
                       initial_state: str, metadata: Dict[str, Any] = None) -> Optional[str]:
        """Create a new workflow instance."""
        try:
            # Validate template
            if template_name not in self.workflow_templates:
                self.logger.error(f"Workflow template {template_name} not found")
                return None
            
            # Create workflow instance
            workflow = WorkflowInstance(
                workflow_id=workflow_id,
                workflow_name=template_name,
                current_state=initial_state,
                created_at=self.core.get_state_manager().get_current_time(),
                last_transition=self.core.get_state_manager().get_current_time(),
                metadata=metadata or {}
            )
            
            # Add to state manager
            self.core.get_state_manager().workflows[workflow_id] = workflow
            
            self.logger.info(f"Created workflow: {workflow_id}")
            return workflow_id
            
        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            return None
    
    def start_workflow(self, workflow_id: str, initial_context: Dict[str, Any] = None) -> bool:
        """Start execution of a workflow."""
        try:
            # Get workflow instance
            workflow = self.core.get_state_manager().workflows.get(workflow_id)
            if not workflow:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False
            
            # Start execution
            if self.execution_engine.start_workflow_execution(workflow, initial_context):
                workflow.status = StateStatus.ACTIVE
                workflow.started_at = self.core.get_state_manager().get_current_time()
                self.logger.info(f"Started workflow: {workflow_id}")
                return True
            else:
                self.logger.error(f"Failed to start workflow execution: {workflow_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to start workflow {workflow_id}: {e}")
            return False
    
    def stop_workflow(self, workflow_id: str) -> bool:
        """Stop execution of a workflow."""
        try:
            if self.execution_engine.stop_workflow_execution(workflow_id):
                # Update workflow status
                workflow = self.core.get_state_manager().workflows.get(workflow_id)
                if workflow:
                    workflow.status = StateStatus.FAILED
                
                self.logger.info(f"Stopped workflow: {workflow_id}")
                return True
            else:
                self.logger.error(f"Failed to stop workflow: {workflow_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to stop workflow {workflow_id}: {e}")
            return False
    
    def get_workflow_status(self, workflow_id: str) -> Optional[StateStatus]:
        """Get current status of a workflow."""
        try:
            # Check execution engine first
            execution_status = self.execution_engine.get_workflow_status(workflow_id)
            if execution_status:
                return execution_status
            
            # Check workflow instance
            workflow = self.core.get_state_manager().workflows.get(workflow_id)
            if workflow:
                return workflow.status
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get workflow status: {e}")
            return None
    
    def add_state(self, state: StateDefinition) -> bool:
        """Add a new state definition."""
        try:
            return self.core.get_state_manager().add_state(state)
        except Exception as e:
            self.logger.error(f"Failed to add state: {e}")
            return False
    
    def add_transition(self, transition: TransitionDefinition) -> bool:
        """Add a new transition definition."""
        try:
            # Validate transition
            if not self.transition_validator.validate_transition(transition):
                errors = self.transition_validator.get_validation_errors()
                self.logger.error(f"Invalid transition: {errors}")
                return False
            
            return self.transition_manager.add_transition(transition)
            
        except Exception as e:
            self.logger.error(f"Failed to add transition: {e}")
            return False
    
    def execute_transition(self, workflow_id: str, to_state: str, 
                          context: Dict[str, Any] = None) -> bool:
        """Execute a state transition for a workflow."""
        try:
            workflow = self.core.get_state_manager().workflows.get(workflow_id)
            if not workflow:
                self.logger.error(f"Workflow {workflow_id} not found")
                return False
            
            from_state = workflow.current_state
            
            # Execute transition
            result = self.transition_manager.execute_transition(
                from_state, to_state, workflow_id, context
            )
            
            if result.success:
                # Update workflow state
                workflow.current_state = to_state
                workflow.last_transition = self.core.get_state_manager().get_current_time()
                self.logger.info(f"Transition executed: {from_state} -> {to_state}")
                return True
            else:
                self.logger.error(f"Transition failed: {result.error_message}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to execute transition: {e}")
            return False
    
    def get_available_transitions(self, workflow_id: str) -> List[TransitionDefinition]:
        """Get available transitions for a workflow."""
        try:
            workflow = self.core.get_state_manager().workflows.get(workflow_id)
            if not workflow:
                return []
            
            return self.transition_manager.get_available_transitions(workflow.current_state)
            
        except Exception as e:
            self.logger.error(f"Failed to get available transitions: {e}")
            return []
    
    def get_execution_metrics(self) -> Dict[str, Any]:
        """Get execution metrics."""
        try:
            return self.execution_monitor.get_metrics()
        except Exception as e:
            self.logger.error(f"Failed to get execution metrics: {e}")
            return {}
    
    def get_workflow_performance(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a specific workflow."""
        try:
            return self.execution_monitor.get_workflow_performance(workflow_id)
        except Exception as e:
            self.logger.error(f"Failed to get workflow performance: {e}")
            return None
    
    def shutdown(self) -> None:
        """Shutdown the FSM orchestrator."""
        try:
            self.execution_engine.shutdown()
            self.logger.info("FSM Orchestrator shutdown complete")
        except Exception as e:
            self.logger.error(f"Failed to shutdown FSM Orchestrator: {e}")
    
    # Default transition handlers
    def _log_transition_handler(self, workflow_id: str, context: Dict[str, Any]) -> None:
        """Default handler for logging transitions."""
        self.logger.info(f"Transition logged for workflow: {workflow_id}")
    
    def _update_metadata_handler(self, workflow_id: str, context: Dict[str, Any]) -> None:
        """Default handler for updating metadata."""
        workflow = self.core.get_state_manager().workflows.get(workflow_id)
        if workflow and context:
            workflow.metadata.update(context)
    
    def _notify_completion_handler(self, workflow_id: str, context: Dict[str, Any]) -> None:
        """Default handler for completion notifications."""
        self.logger.info(f"Completion notification for workflow: {workflow_id}")


def main():
    """CLI interface for FSM Orchestrator testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="FSM Orchestrator - V2 Standards Compliant")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    parser.add_argument("--config", type=str, help="Configuration file path")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_tests()
    elif args.config:
        orchestrator = FSMOrchestrator()
        if orchestrator.initialize(args.config):
            print("✅ FSM Orchestrator initialized successfully")
        else:
            print("❌ FSM Orchestrator initialization failed")
    else:
        parser.print_help()


def run_smoke_tests():
    """Run smoke tests for FSM Orchestrator."""
    print("🧪 Running FSM Orchestrator smoke tests...")
    
    # Test orchestrator creation
    orchestrator = FSMOrchestrator()
    assert orchestrator is not None
    print("✅ FSMOrchestrator creation test passed")
    
    # Test initialization
    assert orchestrator.initialize() is True
    print("✅ Initialization test passed")
    
    # Test workflow creation
    workflow_id = orchestrator.create_workflow("test_template", "test_workflow", "initial")
    assert workflow_id == "test_workflow"
    print("✅ Workflow creation test passed")
    
    # Test metrics
    metrics = orchestrator.get_execution_metrics()
    assert isinstance(metrics, dict)
    print("✅ Metrics test passed")
    
    print("🎉 All smoke tests passed!")


if __name__ == "__main__":
    main()
