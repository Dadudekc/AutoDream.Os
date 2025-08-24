"""
Workflow Validation Logic - V2 Compliant Validation System

This module contains workflow validation logic, error handling, and integrity checks.
Follows V2 standards with ≤200 LOC and single responsibility for validation.
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from .workflow_types import WorkflowStatus, WorkflowType, AgentCapability, PERFORMANCE_THRESHOLDS
from .workflow_core import WorkflowStep, V2Workflow, WorkflowExecution


class WorkflowValidator:
    """Validates workflow definitions, executions, and performance metrics"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.WorkflowValidator")
        self.validation_errors: List[str] = []
        self.validation_warnings: List[str] = []
    
    def validate_workflow_definition(self, workflow: V2Workflow) -> Tuple[bool, List[str]]:
        """Validate a workflow definition for integrity and correctness"""
        self.validation_errors = []
        self.validation_warnings = []
        
        try:
            # Basic workflow validation
            if not self._validate_basic_workflow(workflow):
                return False, self.validation_errors
            
            # Step validation
            if not self._validate_workflow_steps(workflow.steps):
                return False, self.validation_errors
            
            # Dependency validation
            if not self._validate_step_dependencies(workflow.steps):
                return False, self.validation_errors
            
            # Capability validation
            if not self._validate_agent_capabilities(workflow.steps):
                self.validation_warnings.append("Some agent capabilities may not be available")
            
            # Performance validation
            if not self._validate_performance_estimates(workflow.steps):
                self.validation_warnings.append("Performance estimates may be inaccurate")
            
            return len(self.validation_errors) == 0, self.validation_errors + self.validation_warnings
        
        except Exception as e:
            self.logger.error(f"Workflow validation failed: {e}")
            self.validation_errors.append(f"Validation error: {str(e)}")
            return False, self.validation_errors
    
    def _validate_basic_workflow(self, workflow: V2Workflow) -> bool:
        """Validate basic workflow properties"""
        if not workflow.workflow_id:
            self.validation_errors.append("Workflow ID is required")
            return False
        
        if not workflow.name or len(workflow.name.strip()) == 0:
            self.validation_errors.append("Workflow name is required")
            return False
        
        if not workflow.description or len(workflow.description.strip()) == 0:
            self.validation_warnings.append("Workflow description is empty")
        
        if not workflow.steps or len(workflow.steps) == 0:
            self.validation_errors.append("Workflow must have at least one step")
            return False
        
        if not workflow.created_at:
            self.validation_errors.append("Workflow creation timestamp is required")
            return False
        
        return True
    
    def _validate_workflow_steps(self, steps: List[WorkflowStep]) -> bool:
        """Validate individual workflow steps"""
        step_ids = set()
        
        for i, step in enumerate(steps):
            # Check for duplicate step IDs
            if step.step_id in step_ids:
                self.validation_errors.append(f"Duplicate step ID: {step.step_id}")
                return False
            step_ids.add(step.step_id)
            
            # Validate step properties
            if not step.name or len(step.name.strip()) == 0:
                self.validation_errors.append(f"Step {step.step_id}: name is required")
                return False
            
            if not step.step_type or len(step.step_type.strip()) == 0:
                self.validation_errors.append(f"Step {step.step_id}: step type is required")
                return False
            
            # Validate timeouts
            if step.timeout <= 0:
                self.validation_errors.append(f"Step {step.step_id}: timeout must be positive")
                return False
            
            if step.timeout > 3600:  # 1 hour max
                self.validation_warnings.append(f"Step {step.step_id}: timeout is very long ({step.timeout}s)")
            
            # Validate estimated duration
            if step.estimated_duration < 0:
                self.validation_errors.append(f"Step {step.step_id}: estimated duration cannot be negative")
                return False
        
        return True
    
    def _validate_step_dependencies(self, steps: List[WorkflowStep]) -> bool:
        """Validate step dependencies for circular references and validity"""
        step_ids = {step.step_id for step in steps}
        
        for step in steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    self.validation_errors.append(f"Step {step.step_id}: dependency '{dep}' does not exist")
                    return False
        
        # Check for circular dependencies (simple check)
        for step in steps:
            if step.step_id in step.dependencies:
                self.validation_errors.append(f"Step {step.step_id}: cannot depend on itself")
                return False
        
        return True
    
    def _validate_agent_capabilities(self, steps: List[WorkflowStep]) -> bool:
        """Validate agent capability requirements"""
        for step in steps:
            for capability in step.required_capabilities:
                if not isinstance(capability, AgentCapability):
                    self.validation_warnings.append(f"Step {step.step_id}: invalid capability type")
        
        return True
    
    def _validate_performance_estimates(self, steps: List[WorkflowStep]) -> bool:
        """Validate performance estimates for reasonableness"""
        total_estimated_time = sum(step.estimated_duration for step in steps)
        
        if total_estimated_time > 3600:  # 1 hour total
            self.validation_warnings.append("Total estimated workflow time exceeds 1 hour")
        
        if total_estimated_time < 1:  # Less than 1 second total
            self.validation_warnings.append("Total estimated workflow time seems too low")
        
        return True
    
    def validate_execution_state(self, execution: WorkflowExecution) -> Tuple[bool, List[str]]:
        """Validate workflow execution state for consistency"""
        self.validation_errors = []
        self.validation_warnings = []
        
        try:
            # Check execution ID
            if not execution.execution_id:
                self.validation_errors.append("Execution ID is required")
                return False, self.validation_errors
            
            # Check workflow ID
            if not execution.workflow_id:
                self.validation_errors.append("Workflow ID is required")
                return False, self.validation_errors
            
            # Check status consistency
            if execution.status == WorkflowStatus.COMPLETED and not execution.actual_completion:
                self.validation_errors.append("Completed workflow must have completion timestamp")
                return False, self.validation_errors
            
            if execution.status == WorkflowStatus.FAILED and not execution.failed_steps:
                self.validation_warnings.append("Failed workflow has no failed steps recorded")
            
            # Check step consistency
            if execution.completed_steps and execution.failed_steps:
                # Check for overlap between completed and failed steps
                overlap = set(execution.completed_steps) & set(execution.failed_steps)
                if overlap:
                    self.validation_errors.append(f"Steps cannot be both completed and failed: {overlap}")
                    return False, self.validation_errors
            
            # Check timestamps
            if execution.start_time:
                try:
                    start_time = datetime.fromisoformat(execution.start_time)
                    if start_time > datetime.now():
                        self.validation_warnings.append("Start time is in the future")
                except ValueError:
                    self.validation_errors.append("Invalid start time format")
                    return False, self.validation_errors
            
            if execution.actual_completion:
                try:
                    completion_time = datetime.fromisoformat(execution.actual_completion)
                    if execution.start_time:
                        start_time = datetime.fromisoformat(execution.start_time)
                        if completion_time < start_time:
                            self.validation_errors.append("Completion time cannot be before start time")
                            return False, self.validation_errors
                except ValueError:
                    self.validation_errors.append("Invalid completion time format")
                    return False, self.validation_errors
            
            return len(self.validation_errors) == 0, self.validation_errors + self.validation_warnings
        
        except Exception as e:
            self.logger.error(f"Execution validation failed: {e}")
            self.validation_errors.append(f"Validation error: {str(e)}")
            return False, self.validation_errors
    
    def validate_performance_metrics(self, metrics: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Validate performance metrics for reasonableness"""
        self.validation_errors = []
        self.validation_warnings = []
        
        try:
            for metric_name, value in metrics.items():
                if not isinstance(value, (int, float)):
                    self.validation_errors.append(f"Metric {metric_name}: value must be numeric")
                    continue
                
                # Check for negative values where inappropriate
                if metric_name in ["execution_time", "memory_usage", "cpu_usage", "response_time"]:
                    if value < 0:
                        self.validation_errors.append(f"Metric {metric_name}: cannot be negative")
                        continue
                
                # Check against thresholds
                if metric_name in PERFORMANCE_THRESHOLDS:
                    threshold = PERFORMANCE_THRESHOLDS[metric_name]
                    if value > threshold:
                        self.validation_warnings.append(f"Metric {metric_name}: {value} exceeds threshold {threshold}")
                
                # Check for unreasonably high values
                if metric_name == "execution_time" and value > 3600000:  # 1000 hours
                    self.validation_warnings.append(f"Metric {metric_name}: value seems unreasonably high")
                elif metric_name == "memory_usage" and value > 10000:  # 10GB
                    self.validation_warnings.append(f"Metric {metric_name}: value seems unreasonably high")
                elif metric_name == "cpu_usage" and value > 100:  # 100%
                    self.validation_warnings.append(f"Metric {metric_name}: value exceeds 100%")
            
            return len(self.validation_errors) == 0, self.validation_errors + self.validation_warnings
        
        except Exception as e:
            self.logger.error(f"Performance validation failed: {e}")
            self.validation_errors.append(f"Validation error: {str(e)}")
            return False, self.validation_errors
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of validation results"""
        return {
            "total_errors": len(self.validation_errors),
            "total_warnings": len(self.validation_warnings),
            "errors": self.validation_errors.copy(),
            "warnings": self.validation_warnings.copy(),
            "validation_timestamp": datetime.now().isoformat(),
        }
    
    def clear_validation_results(self):
        """Clear validation results"""
        self.validation_errors.clear()
        self.validation_warnings.clear()

