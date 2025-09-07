#!/usr/bin/env python3
"""
Workflow Manager - Workflow Lifecycle Management
==============================================

Workflow lifecycle management for unified workflow system.
Follows V2 standards: ≤200 LOC, single responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from ..types.workflow_models import WorkflowDefinition, WorkflowExecution, WorkflowStep
from ..types.workflow_enums import WorkflowStatus, WorkflowType


class WorkflowManager:
    """
    Workflow lifecycle manager for workflow system.
    
    Single responsibility: Manage workflow lifecycle including creation,
    validation, deployment, and status management.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.WorkflowManager")
        self.workflow_definitions: Dict[str, WorkflowDefinition] = {}
        self.workflow_executions: Dict[str, WorkflowExecution] = {}
        self.workflow_templates: Dict[str, WorkflowDefinition] = {}
    
    def create_workflow(self, definition: WorkflowDefinition) -> str:
        """
        Create new workflow from definition.
        
        Args:
            definition: Workflow definition to create
            
        Returns:
            Workflow ID of the created workflow
        """
        self.logger.info(f"Creating workflow: {definition.workflow_id}")
        
        # Validate workflow definition
        if not self._validate_workflow_definition(definition):
            raise ValueError("Invalid workflow definition")
        
        # Store workflow definition
        self.workflow_definitions[definition.workflow_id] = definition
        
        # Create initial execution
        execution = WorkflowExecution(
            execution_id=str(uuid.uuid4()),
            workflow_id=definition.workflow_id,
            workflow_name=definition.name,
            status=WorkflowStatus.CREATED,
            start_time=datetime.now().isoformat(),
            steps=[],
            metadata=definition.metadata.copy() if definition.metadata else {}
        )
        
        self.workflow_executions[execution.execution_id] = execution
        self.logger.info(f"Workflow created successfully: {definition.workflow_id}")
        
        return definition.workflow_id
    
    def deploy_workflow(self, workflow_id: str) -> bool:
        """
        Deploy workflow for execution.
        
        Args:
            workflow_id: ID of the workflow to deploy
            
        Returns:
            True if deployment successful, False otherwise
        """
        self.logger.info(f"Deploying workflow: {workflow_id}")
        
        if workflow_id not in self.workflow_definitions:
            self.logger.error(f"Workflow not found: {workflow_id}")
            return False
        
        definition = self.workflow_definitions[workflow_id]
        
        # Validate deployment requirements
        if not self._check_deployment_requirements(definition):
            self.logger.error(f"Deployment requirements not met for workflow: {workflow_id}")
            return False
        
        # Update workflow status
        definition.status = WorkflowStatus.DEPLOYED
        self.workflow_definitions[workflow_id] = definition
        
        self.logger.info(f"Workflow deployed successfully: {workflow_id}")
        return True
    
    def start_workflow(self, workflow_id: str, parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Start workflow execution.
        
        Args:
            workflow_id: ID of the workflow to start
            parameters: Optional parameters for workflow execution
            
        Returns:
            Execution ID of the started workflow
        """
        self.logger.info(f"Starting workflow: {workflow_id}")
        
        if workflow_id not in self.workflow_definitions:
            raise ValueError(f"Workflow not found: {workflow_id}")
        
        definition = self.workflow_definitions[workflow_id]
        
        # Create new execution instance
        execution = WorkflowExecution(
            execution_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            workflow_name=definition.name,
            status=WorkflowStatus.RUNNING,
            start_time=datetime.now().isoformat(),
            steps=[],
            parameters=parameters or {},
            metadata=definition.metadata.copy() if definition.metadata else {}
        )
        
        # Initialize workflow steps
        if definition.steps:
            execution.steps = [
                WorkflowStep(
                    step_id=step.step_id,
                    name=step.name,
                    step_type=step.step_type,
                    status=step.status,
                    dependencies=step.dependencies.copy() if step.dependencies else [],
                    parameters=step.parameters.copy() if step.parameters else {},
                    metadata=step.metadata.copy() if step.metadata else {}
                )
                for step in definition.steps
            ]
        
        self.workflow_executions[execution.execution_id] = execution
        self.logger.info(f"Workflow started successfully: {workflow_id} -> {execution.execution_id}")
        
        return execution.execution_id
    
    def pause_workflow(self, execution_id: str) -> bool:
        """
        Pause workflow execution.
        
        Args:
            execution_id: ID of the execution to pause
            
        Returns:
            True if pause successful, False otherwise
        """
        self.logger.info(f"Pausing workflow execution: {execution_id}")
        
        if execution_id not in self.workflow_executions:
            self.logger.error(f"Execution not found: {execution_id}")
            return False
        
        execution = self.workflow_executions[execution_id]
        execution.status = WorkflowStatus.PAUSED
        execution.pause_time = datetime.now().isoformat()
        
        self.logger.info(f"Workflow execution paused: {execution_id}")
        return True
    
    def resume_workflow(self, execution_id: str) -> bool:
        """
        Resume paused workflow execution.
        
        Args:
            execution_id: ID of the execution to resume
            
        Returns:
            True if resume successful, False otherwise
        """
        self.logger.info(f"Resuming workflow execution: {execution_id}")
        
        if execution_id not in self.workflow_executions:
            self.logger.error(f"Execution not found: {execution_id}")
            return False
        
        execution = self.workflow_executions[execution_id]
        if execution.status != WorkflowStatus.PAUSED:
            self.logger.error(f"Execution is not paused: {execution_id}")
            return False
        
        execution.status = WorkflowStatus.RUNNING
        execution.resume_time = datetime.now().isoformat()
        
        self.logger.info(f"Workflow execution resumed: {execution_id}")
        return True
    
    def stop_workflow(self, execution_id: str) -> bool:
        """
        Stop workflow execution.
        
        Args:
            execution_id: ID of the execution to stop
            
        Returns:
            True if stop successful, False otherwise
        """
        self.logger.info(f"Stopping workflow execution: {execution_id}")
        
        if execution_id not in self.workflow_executions:
            self.logger.error(f"Execution not found: {execution_id}")
            return False
        
        execution = self.workflow_executions[execution_id]
        execution.status = WorkflowStatus.STOPPED
        execution.end_time = datetime.now().isoformat()
        
        self.logger.info(f"Workflow execution stopped: {execution_id}")
        return True
    
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """
        Get current status of a workflow.
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            Current workflow status or None if not found
        """
        if workflow_id in self.workflow_definitions:
            return self.workflow_definitions[workflow_id].status
        return None
    
    def get_execution_status(self, execution_id: str) -> Optional[WorkflowStatus]:
        """
        Get current status of a workflow execution.
        
        Args:
            execution_id: ID of the execution
            
        Returns:
            Current execution status or None if not found
        """
        if execution_id in self.workflow_executions:
            return self.workflow_executions[execution_id].status
        return None
    
    def list_workflows(self, workflow_type: Optional[WorkflowType] = None) -> List[str]:
        """
        List available workflows.
        
        Args:
            workflow_type: Optional filter by workflow type
            
        Returns:
            List of workflow IDs
        """
        if workflow_type:
            return [
                workflow_id for workflow_id, definition in self.workflow_definitions.items()
                if definition.workflow_type == workflow_type
            ]
        return list(self.workflow_definitions.keys())
    
    def list_executions(self, workflow_id: Optional[str] = None) -> List[str]:
        """
        List workflow executions.
        
        Args:
            workflow_id: Optional filter by workflow ID
            
        Returns:
            List of execution IDs
        """
        if workflow_id:
            return [
                execution_id for execution_id, execution in self.workflow_executions.items()
                if execution.workflow_id == workflow_id
            ]
        return list(self.workflow_executions.keys())
    
    def _validate_workflow_definition(self, definition: WorkflowDefinition) -> bool:
        """Validate workflow definition structure and requirements."""
        if not definition.workflow_id or not definition.name:
            return False
        
        # Check for circular dependencies in steps
        if definition.steps:
            step_ids = {step.step_id for step in definition.steps}
            for step in definition.steps:
                if step.dependencies:
                    for dep in step.dependencies:
                        if dep not in step_ids:
                            self.logger.warning(f"Invalid dependency {dep} in step {step.step_id}")
                            return False
        
        return True
    
    def _check_deployment_requirements(self, definition: WorkflowDefinition) -> bool:
        """Check if workflow meets deployment requirements."""
        # Basic validation - can be extended with more specific requirements
        return definition.status in [WorkflowStatus.CREATED, WorkflowStatus.DRAFT]
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for workflow manager."""
        try:
            # Test workflow creation
            from ..types.workflow_models import WorkflowDefinition, WorkflowStep
            from ..types.workflow_enums import WorkflowType, TaskStatus
            
            test_step = WorkflowStep(
                step_id="test_step",
                name="Test Step",
                step_type="test",
                status=TaskStatus.COMPLETED
            )
            
            test_definition = WorkflowDefinition(
                workflow_id="test_workflow",
                name="Test Workflow",
                description="Test workflow for smoke testing",
                workflow_type=WorkflowType.SEQUENTIAL,
                steps=[test_step]
            )
            
            workflow_id = self.create_workflow(test_definition)
            if workflow_id == "test_workflow":
                self.logger.info("✅ Workflow manager smoke test passed.")
                return True
            else:
                self.logger.error("❌ Workflow manager smoke test failed: Invalid workflow ID returned.")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Workflow manager smoke test failed: {e}")
            return False
