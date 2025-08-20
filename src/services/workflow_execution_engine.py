#!/usr/bin/env python3
"""
Workflow Execution Engine - Agent Cellphone V2
=============================================

Executes and manages workflow instances.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import time
import threading
from typing import Dict, List, Optional, Any, Callable
import logging
from .workflow_definitions import (
    WorkflowStep, WorkflowStatus, WorkflowStepData, WorkflowExecution,
    WorkflowDefinitionManager
)


class WorkflowExecutionEngine:
    """Executes and manages workflow instances"""
    
    def __init__(self):
        self.definition_manager = WorkflowDefinitionManager()
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        self.completed_workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_handlers: Dict[WorkflowStep, List[Callable]] = {}
        self.logger = logging.getLogger(f"{__name__}.WorkflowExecutionEngine")
        
        self._initialize_workflow_handlers()
    
    def _initialize_workflow_handlers(self):
        """Initialize default workflow step handlers"""
        # Default handlers for each step type
        self.workflow_handlers = {
            WorkflowStep.INITIALIZATION: [self._default_initialization_handler],
            WorkflowStep.TRAINING: [self._default_training_handler],
            WorkflowStep.ROLE_ASSIGNMENT: [self._default_role_assignment_handler],
            WorkflowStep.CAPABILITY_GRANT: [self._default_capability_grant_handler],
            WorkflowStep.SYSTEM_INTEGRATION: [self._default_system_integration_handler],
            WorkflowStep.VALIDATION: [self._default_validation_handler],
            WorkflowStep.COMPLETION: [self._default_completion_handler]
        }
    
    def start_workflow(self, workflow_type: str, agent_id: str, 
                      workflow_id: Optional[str] = None) -> str:
        """Start a new workflow execution"""
        if not workflow_id:
            workflow_id = f"{workflow_type}_{agent_id}_{int(time.time())}"
        
        workflow_definition = self.definition_manager.get_workflow_definition(workflow_type)
        if not workflow_definition:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        # Create workflow execution instance
        workflow_execution = WorkflowExecution(
            workflow_id=workflow_id,
            agent_id=agent_id,
            status=WorkflowStatus.PENDING,
            current_step=None,
            completed_steps=[],
            start_time=time.time(),
            step_results={},
            metadata={"workflow_type": workflow_type}
        )
        
        self.active_workflows[workflow_id] = workflow_execution
        self.logger.info(f"Started workflow {workflow_id} for agent {agent_id}")
        
        return workflow_id
    
    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute a workflow to completion"""
        if workflow_id not in self.active_workflows:
            self.logger.error(f"Workflow {workflow_id} not found")
            return False
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = WorkflowStatus.IN_PROGRESS
        
        try:
            workflow_definition = self.definition_manager.get_workflow_definition(
                workflow.metadata["workflow_type"]
            )
            
            for step_data in workflow_definition:
                # Check prerequisites
                if not self._can_execute_step(step_data, workflow.completed_steps):
                    self.logger.warning(f"Prerequisites not met for step {step_data.step_id}")
                    continue
                
                # Execute step
                if self._execute_step(step_data, workflow):
                    workflow.completed_steps.append(step_data.step_id)
                    workflow.step_results[step_data.step_id] = {"status": "completed"}
                else:
                    workflow.status = WorkflowStatus.FAILED
                    self.logger.error(f"Step {step_data.step_id} failed")
                    return False
            
            # Workflow completed successfully
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completion_time = time.time()
            self.completed_workflows[workflow_id] = workflow
            del self.active_workflows[workflow_id]
            
            self.logger.info(f"Workflow {workflow_id} completed successfully")
            return True
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            self.logger.error(f"Workflow {workflow_id} failed: {e}")
            return False
    
    def _can_execute_step(self, step_data: WorkflowStepData, 
                         completed_steps: List[WorkflowStep]) -> bool:
        """Check if a step can be executed based on prerequisites"""
        if not step_data.prerequisites:
            return True
        
        return all(prereq in completed_steps for prereq in step_data.prerequisites)
    
    def _execute_step(self, step_data: WorkflowStepData, 
                     workflow: WorkflowExecution) -> bool:
        """Execute a single workflow step"""
        self.logger.info(f"Executing step {step_data.step_id} for workflow {workflow.workflow_id}")
        
        # Execute handlers for this step
        handlers = self.workflow_handlers.get(step_data.step_id, [])
        for handler in handlers:
            try:
                result = handler(step_data, workflow)
                if not result:
                    self.logger.error(f"Handler {handler.__name__} failed for step {step_data.step_id}")
                    return False
            except Exception as e:
                self.logger.error(f"Handler {handler.__name__} exception: {e}")
                return False
        
        return True
    
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowExecution]:
        """Get workflow execution status"""
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id]
        elif workflow_id in self.completed_workflows:
            return self.completed_workflows[workflow_id]
        return None
    
    def get_active_workflows(self) -> Dict[str, WorkflowExecution]:
        """Get all active workflows"""
        return self.active_workflows.copy()
    
    def get_completed_workflows(self) -> Dict[str, WorkflowExecution]:
        """Get all completed workflows"""
        return self.completed_workflows.copy()
    
    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            workflow.status = WorkflowStatus.CANCELLED
            self.completed_workflows[workflow_id] = workflow
            del self.active_workflows[workflow_id]
            self.logger.info(f"Workflow {workflow_id} cancelled")
            return True
        return False
    
    # Default step handlers
    def _default_initialization_handler(self, step_data: WorkflowStepData, 
                                      workflow: WorkflowExecution) -> bool:
        """Default initialization step handler"""
        self.logger.info(f"Initializing agent {workflow.agent_id}")
        time.sleep(0.1)  # Simulate work
        return True
    
    def _default_training_handler(self, step_data: WorkflowStepData, 
                                workflow: WorkflowExecution) -> bool:
        """Default training step handler"""
        self.logger.info(f"Training agent {workflow.agent_id}")
        time.sleep(0.1)  # Simulate work
        return True
    
    def _default_role_assignment_handler(self, step_data: WorkflowStepData, 
                                       workflow: WorkflowExecution) -> bool:
        """Default role assignment step handler"""
        self.logger.info(f"Assigning role to agent {workflow.agent_id}")
        time.sleep(0.1)  # Simulate work
        return True
    
    def _default_capability_grant_handler(self, step_data: WorkflowStepData, 
                                        workflow: WorkflowExecution) -> bool:
        """Default capability grant step handler"""
        self.logger.info(f"Granting capabilities to agent {workflow.agent_id}")
        time.sleep(0.1)  # Simulate work
        return True
    
    def _default_system_integration_handler(self, step_data: WorkflowStepData, 
                                          workflow: WorkflowExecution) -> bool:
        """Default system integration step handler"""
        self.logger.info(f"Integrating agent {workflow.agent_id} into system")
        time.sleep(0.1)  # Simulate work
        return True
    
    def _default_validation_handler(self, step_data: WorkflowStepData, 
                                  workflow: WorkflowExecution) -> bool:
        """Default validation step handler"""
        self.logger.info(f"Validating agent {workflow.agent_id}")
        time.sleep(0.1)  # Simulate work
        return True
    
    def _default_completion_handler(self, step_data: WorkflowStepData, 
                                  workflow: WorkflowExecution) -> bool:
        """Default completion step handler"""
        self.logger.info(f"Completing workflow for agent {workflow.agent_id}")
        time.sleep(0.1)  # Simulate work
        return True


def main():
    """CLI interface for testing the Workflow Execution Engine"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Workflow Execution Engine CLI")
    parser.add_argument("--test", "-t", action="store_true", help="Test workflow execution")
    parser.add_argument("--start", "-s", help="Start workflow for agent")
    parser.add_argument("--execute", "-e", help="Execute workflow by ID")
    parser.add_argument("--status", help="Get workflow status")
    
    args = parser.parse_args()
    
    engine = WorkflowExecutionEngine()
    
    if args.test:
        print("🧪 Testing Workflow Execution Engine...")
        
        # Test workflow creation and execution
        workflow_id = engine.start_workflow("quick", "test-agent")
        print(f"✅ Started workflow: {workflow_id}")
        
        success = engine.execute_workflow(workflow_id)
        print(f"✅ Workflow execution: {'Success' if success else 'Failed'}")
        
        status = engine.get_workflow_status(workflow_id)
        print(f"✅ Final status: {status.status.value}")
    
    elif args.start:
        workflow_id = engine.start_workflow("standard", args.start)
        print(f"🚀 Started workflow {workflow_id} for agent {args.start}")
    
    elif args.execute:
        success = engine.execute_workflow(args.execute)
        print(f"⚡ Workflow execution: {'✅ Success' if success else '❌ Failed'}")
    
    elif args.status:
        status = engine.get_workflow_status(args.status)
        if status:
            print(f"📊 Workflow {args.status}:")
            print(f"  Status: {status.status.value}")
            print(f"  Agent: {status.agent_id}")
            print(f"  Steps completed: {len(status.completed_steps)}")
        else:
            print(f"❌ Workflow {args.status} not found")
    
    else:
        print("Workflow Execution Engine - Use --help for options")


if __name__ == "__main__":
    main()
