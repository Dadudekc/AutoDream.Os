#!/usr/bin/env python3
"""
Workflow Validator - Unified Validation Framework Integration

This module provides workflow-specific validation by extending the existing
Unified Validation Framework. It adds workflow-specific validation rules
and integrates with the workflow engine for real-time validation.

Author: Agent-1 (Core Engine Development)
License: MIT
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the src directory to the Python path for validation framework access
current_dir = Path.cwd()
sys.path.insert(0, str(current_dir))

from src.core.validation import BaseValidator, ValidationResult, ValidationSeverity, ValidationStatus, ValidationRule
from ..types.workflow_enums import WorkflowStatus, TaskStatus, WorkflowType
from ..types.workflow_models import WorkflowDefinition, WorkflowExecution, WorkflowStep


class WorkflowValidator(BaseValidator):
    """Workflow-specific validator extending the Unified Validation Framework"""
    
    def __init__(self):
        """Initialize workflow validator"""
        super().__init__("WorkflowValidator")
        self._setup_workflow_rules()
    
    def _setup_workflow_rules(self) -> None:
        """Setup workflow-specific validation rules"""
        workflow_rules = [
            ValidationRule(
                rule_id="workflow_structure",
                rule_name="Workflow Structure Validation",
                rule_type="workflow",
                description="Validate workflow definition structure and integrity",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="step_dependencies",
                rule_name="Step Dependencies Validation",
                rule_type="workflow",
                description="Validate workflow step dependencies and cycles",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="workflow_execution",
                rule_name="Workflow Execution Validation",
                rule_type="workflow",
                description="Validate workflow execution state and transitions",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="performance_metrics",
                rule_name="Performance Metrics Validation",
                rule_type="workflow",
                description="Validate workflow performance and optimization",
                severity=ValidationSeverity.WARNING
            )
        ]
        
        for rule in workflow_rules:
            self.add_validation_rule(rule)
    
    def validate_workflow_definition(self, workflow_def: WorkflowDefinition) -> List[ValidationResult]:
        """Validate workflow definition structure and integrity"""
        results = []
        
        try:
            # Validate basic structure
            if not workflow_def.workflow_id or not workflow_def.name:
                results.append(self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Workflow must have valid ID and name",
                    details={"workflow_id": workflow_def.workflow_id, "name": workflow_def.name}
                ))
            
            # Validate steps
            if not workflow_def.steps:
                results.append(self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Workflow must have at least one step",
                    details={"step_count": len(workflow_def.steps)}
                ))
            else:
                # Validate individual steps
                step_results = self._validate_workflow_steps(workflow_def.steps)
                results.extend(step_results)
                
                # Validate step dependencies
                dependency_results = self._validate_step_dependencies(workflow_def.steps)
                results.extend(dependency_results)
            
            # Validate workflow type
            if workflow_def.workflow_type not in WorkflowType:
                results.append(self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Invalid workflow type",
                    details={"workflow_type": workflow_def.workflow_type, "valid_types": [t.value for t in WorkflowType]}
                ))
            
            # Add success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                results.append(self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Workflow definition validation passed",
                    details={"step_count": len(workflow_def.steps), "workflow_type": workflow_def.workflow_type.value}
                ))
            
        except Exception as e:
            results.append(self._create_result(
                rule_id="workflow_structure",
                rule_name="Workflow Structure Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Workflow validation error: {str(e)}",
                details={"error_type": type(e).__name__}
            ))
        
        return results
    
    def validate_workflow_execution(self, execution: WorkflowExecution) -> List[ValidationResult]:
        """Validate workflow execution state and transitions"""
        results = []
        
        try:
            # Validate execution state
            if execution.status not in WorkflowStatus:
                results.append(self._create_result(
                    rule_id="workflow_execution",
                    rule_name="Workflow Execution Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Invalid workflow execution status",
                    details={"status": execution.status, "valid_statuses": [s.value for s in WorkflowStatus]}
                ))
            
            # Validate step execution states
            if execution.steps:
                step_execution_results = self._validate_step_execution_states(execution.steps)
                results.extend(step_execution_results)
            
            # Validate execution timing
            if execution.start_time and execution.end_time:
                timing_results = self._validate_execution_timing(execution)
                results.extend(timing_results)
            
            # Add success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                results.append(self._create_result(
                    rule_id="workflow_execution",
                    rule_name="Workflow Execution Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Workflow execution validation passed",
                    details={"status": execution.status.value, "step_count": len(execution.steps)}
                ))
            
        except Exception as e:
            results.append(self._create_result(
                rule_id="workflow_execution",
                rule_name="Workflow Execution Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Execution validation error: {str(e)}",
                details={"error_type": type(e).__name__}
            ))
        
        return results
    
    def _validate_workflow_steps(self, steps: List[WorkflowStep]) -> List[ValidationResult]:
        """Validate individual workflow steps"""
        results = []
        
        for i, step in enumerate(steps):
            # Validate step ID
            if not step.step_id or not step.step_id.strip():
                results.append(self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Step {i} must have valid ID",
                    details={"step_index": i, "step_id": step.step_id}
                ))
            
            # Validate step name
            if not step.name or not step.name.strip():
                results.append(self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Step {i} must have valid name",
                    details={"step_index": i, "step_name": step.name}
                ))
            
            # Validate step type
            if not step.step_type or not step.step_type.strip():
                results.append(self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Step {i} must have valid type",
                    details={"step_index": i, "step_type": step.step_type}
                ))
            
            # Validate estimated duration
            if step.estimated_duration < 0:
                results.append(self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message=f"Step {i} has negative estimated duration",
                    details={"step_index": i, "estimated_duration": step.estimated_duration}
                ))
        
        return results
    
    def _validate_step_dependencies(self, steps: List[WorkflowStep]) -> List[ValidationResult]:
        """Validate step dependencies and detect cycles"""
        results = []
        
        # Create step ID mapping
        step_ids = {step.step_id for step in steps}
        
        for i, step in enumerate(steps):
            # Validate dependency references
            for dep in step.dependencies:
                if dep not in step_ids:
                    results.append(self._create_result(
                        rule_id="step_dependencies",
                        rule_name="Step Dependencies Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Step {i} references non-existent dependency: {dep}",
                        details={"step_index": i, "step_id": step.step_id, "invalid_dependency": dep}
                    ))
            
            # Check for self-dependencies
            if step.step_id in step.dependencies:
                results.append(self._create_result(
                    rule_id="step_dependencies",
                    rule_name="Step Dependencies Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Step {i} has self-dependency",
                    details={"step_index": i, "step_id": step.step_id}
                ))
        
        # Detect cycles (simplified cycle detection)
        cycle_results = self._detect_dependency_cycles(steps)
        results.extend(cycle_results)
        
        return results
    
    def _detect_dependency_cycles(self, steps: List[WorkflowStep]) -> List[ValidationResult]:
        """Detect circular dependencies in workflow steps"""
        results = []
        
        # Simple cycle detection - check for obvious cycles
        for i, step in enumerate(steps):
            visited = set()
            if self._has_cycle_recursive(step, steps, visited, set()):
                results.append(self._create_result(
                    rule_id="step_dependencies",
                    rule_name="Step Dependencies Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Circular dependency detected involving step {i}",
                    details={"step_index": i, "step_id": step.step_id}
                ))
        
        return results
    
    def _has_cycle_recursive(self, step: WorkflowStep, all_steps: List[WorkflowStep], visited: set, path: set) -> bool:
        """Recursively check for cycles in dependency graph"""
        if step.step_id in path:
            return True
        
        if step.step_id in visited:
            return False
        
        visited.add(step.step_id)
        path.add(step.step_id)
        
        for dep_id in step.dependencies:
            dep_step = next((s for s in all_steps if s.step_id == dep_id), None)
            if dep_step and self._has_cycle_recursive(dep_step, all_steps, visited, path):
                return True
        
        path.remove(step.step_id)
        return False
    
    def _validate_step_execution_states(self, steps: List[WorkflowStep]) -> List[ValidationResult]:
        """Validate step execution states during workflow execution"""
        results = []
        
        for i, step in enumerate(steps):
            if step.status not in TaskStatus:
                results.append(self._create_result(
                    rule_id="workflow_execution",
                    rule_name="Workflow Execution Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Step {i} has invalid execution status",
                    details={"step_index": i, "step_id": step.step_id, "status": step.status}
                ))
            
            # Validate timing consistency
            if step.start_time and step.end_time:
                if step.start_time > step.end_time:
                    results.append(self._create_result(
                        rule_id="workflow_execution",
                        rule_name="Workflow Execution Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message=f"Step {i} has inconsistent timing",
                        details={"step_index": i, "step_id": step.step_id, "start_time": step.start_time, "end_time": step.end_time}
                    ))
        
        return results
    
    def _validate_execution_timing(self, execution: WorkflowExecution) -> List[ValidationResult]:
        """Validate workflow execution timing"""
        results = []
        
        # Validate start time is before end time
        if execution.start_time > execution.end_time:
            results.append(self._create_result(
                rule_id="workflow_execution",
                rule_name="Workflow Execution Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message="Workflow execution has inconsistent timing",
                details={"start_time": execution.start_time, "end_time": execution.end_time}
            ))
        
        return results
    
    def validate_workflow_performance(self, workflow_def: WorkflowDefinition, execution: WorkflowExecution) -> List[ValidationResult]:
        """Validate workflow performance metrics"""
        results = []
        
        try:
            # Calculate total estimated duration
            total_estimated = sum(step.estimated_duration for step in workflow_def.steps)
            
            # Check if actual execution time is reasonable
            if execution.start_time and execution.end_time:
                actual_duration = (execution.end_time - execution.start_time).total_seconds()
                
                # Allow 20% variance
                variance_threshold = total_estimated * 0.2
                if abs(actual_duration - total_estimated) > variance_threshold:
                    results.append(self._create_result(
                        rule_id="performance_metrics",
                        rule_name="Performance Metrics Validation",
                        status=ValidationStatus.PASSED,
                        severity=ValidationSeverity.WARNING,
                        message="Workflow execution time differs significantly from estimate",
                        details={
                            "estimated_duration": total_estimated,
                            "actual_duration": actual_duration,
                            "variance": abs(actual_duration - total_estimated),
                            "threshold": variance_threshold
                        }
                    ))
            
            # Check for performance optimization opportunities
            long_steps = [step for step in workflow_def.steps if step.estimated_duration > 300]  # 5 minutes
            if long_steps:
                results.append(self._create_result(
                    rule_id="performance_metrics",
                    rule_name="Performance Metrics Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.LOW,
                    message="Long-running steps detected - consider optimization",
                    details={
                        "long_steps": [{"step_id": s.step_id, "duration": s.estimated_duration} for s in long_steps]
                    }
                ))
            
        except Exception as e:
            results.append(self._create_result(
                rule_id="performance_metrics",
                rule_name="Performance Metrics Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.WARNING,
                message=f"Performance validation error: {str(e)}",
                details={"error_type": type(e).__name__}
            ))
        
        return results
