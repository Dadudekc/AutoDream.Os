#!/usr/bin/env python3
"""
Workflow Validation Manager - Real-time Validation Coordination

This module provides real-time validation coordination during workflow execution,
integrating the workflow validator with the workflow engine for continuous
validation and performance monitoring.

Author: Agent-1 (Core Engine Development)
License: MIT
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging

# Add the src directory to the Python path for validation framework access
current_dir = Path.cwd()
sys.path.insert(0, str(current_dir))

# Import validation types directly to avoid circular imports
from src.core.validation.base_validator import ValidationResult, ValidationSeverity, ValidationStatus
from .workflow_validator import WorkflowValidator
from ..types.workflow_enums import WorkflowStatus, TaskStatus
from ..types.workflow_models import WorkflowDefinition, WorkflowExecution, WorkflowStep


class WorkflowValidationManager:
    """Real-time workflow validation coordination and management"""
    
    def __init__(self):
        """Initialize workflow validation manager"""
        self.logger = logging.getLogger(f"{__name__}.WorkflowValidationManager")
        
        # Core validation components
        self.workflow_validator = WorkflowValidator()
        # Note: ValidationManager removed to avoid circular imports
        
        # Validation tracking
        self.validation_history: List[ValidationResult] = []
        self.workflow_validation_cache: Dict[str, List[ValidationResult]] = {}
        
        # Performance monitoring
        self.performance_metrics = {
            "total_validations": 0,
            "validation_time_avg": 0.0,
            "validation_success_rate": 0.0,
            "performance_issues_detected": 0
        }
        
        # Real-time validation hooks
        self.validation_hooks: Dict[str, List[Callable]] = {
            "workflow_created": [],
            "workflow_started": [],
            "step_started": [],
            "step_completed": [],
            "workflow_completed": [],
            "workflow_failed": []
        }
        
        self._setup_validation_hooks()
    
    def _setup_validation_hooks(self) -> None:
        """Setup default validation hooks for workflow events"""
        # Workflow creation validation
        self.add_validation_hook("workflow_created", self._validate_workflow_creation)
        
        # Workflow execution validation
        self.add_validation_hook("workflow_started", self._validate_workflow_execution_start)
        self.add_validation_hook("step_started", self._validate_step_execution_start)
        self.add_validation_hook("step_completed", self._validate_step_execution_completion)
        
        # Workflow completion validation
        self.add_validation_hook("workflow_completed", self._validate_workflow_completion)
        self.add_validation_hook("workflow_failed", self._validate_workflow_failure)
    
    def add_validation_hook(self, event: str, hook: Callable) -> None:
        """Add validation hook for specific workflow event"""
        if event in self.validation_hooks:
            self.validation_hooks[event].append(hook)
            self.logger.info(f"Added validation hook for event: {event}")
        else:
            self.logger.warning(f"Unknown validation hook event: {event}")
    
    def remove_validation_hook(self, event: str, hook: Callable) -> None:
        """Remove validation hook for specific workflow event"""
        if event in self.validation_hooks and hook in self.validation_hooks[event]:
            self.validation_hooks[event].remove(hook)
            self.logger.info(f"Removed validation hook for event: {event}")
    
    def trigger_validation_hooks(self, event: str, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Trigger validation hooks for specific workflow event"""
        results = []
        
        if event in self.validation_hooks:
            for hook in self.validation_hooks[event]:
                try:
                    hook_results = hook(workflow_data)
                    if hook_results:
                        results.extend(hook_results)
                except Exception as e:
                    self.logger.error(f"Validation hook error for event {event}: {e}")
                    error_result = ValidationResult(
                        rule_id="validation_hook_error",
                        rule_name="Validation Hook Error",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Validation hook error: {str(e)}",
                        details={"event": event, "error_type": type(e).__name__}
                    )
                    results.append(error_result)
        
        # Store results in history
        if results:
            self.validation_history.extend(results)
            self._update_performance_metrics(results)
        
        return results
    
    def _validate_workflow_creation(self, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate workflow during creation phase"""
        try:
            workflow_def = workflow_data.get("workflow_definition")
            if workflow_def:
                return self.workflow_validator.validate_workflow_definition(workflow_def)
        except Exception as e:
            self.logger.error(f"Workflow creation validation error: {e}")
        
        return []
    
    def _validate_workflow_execution_start(self, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate workflow when execution starts"""
        try:
            execution = workflow_data.get("workflow_execution")
            if execution:
                return self.workflow_validator.validate_workflow_execution(execution)
        except Exception as e:
            self.logger.error(f"Workflow execution start validation error: {e}")
        
        return []
    
    def _validate_step_execution_start(self, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate step when execution starts"""
        try:
            step = workflow_data.get("step")
            execution = workflow_data.get("workflow_execution")
            
            if step and execution:
                # Validate step readiness
                results = []
                
                # Check if step dependencies are satisfied
                completed_steps = {s.step_id for s in execution.steps if s.status == TaskStatus.COMPLETED}
                if not step.is_ready(completed_steps):
                    results.append(ValidationResult(
                        rule_id="step_dependencies",
                        rule_name="Step Dependencies Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Step {step.step_id} dependencies not satisfied",
                        details={
                            "step_id": step.step_id,
                            "dependencies": step.dependencies,
                            "completed_steps": list(completed_steps)
                        }
                    ))
                
                return results
        except Exception as e:
            self.logger.error(f"Step execution start validation error: {e}")
        
        return []
    
    def _validate_step_execution_completion(self, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate step when execution completes"""
        try:
            step = workflow_data.get("step")
            execution = workflow_data.get("workflow_execution")
            
            if step and execution:
                results = []
                
                # Validate step completion
                if step.status == TaskStatus.COMPLETED:
                    # Check if step has result
                    if not step.result:
                        results.append(ValidationResult(
                            rule_id="step_completion",
                            rule_name="Step Completion Validation",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.WARNING,
                            message=f"Step {step.step_id} completed without result",
                            details={"step_id": step.step_id, "status": step.status.value}
                        ))
                    
                    # Validate timing
                    if step.start_time and step.end_time:
                        duration = (step.end_time - step.start_time).total_seconds()
                        if duration > step.timeout:
                            results.append(ValidationResult(
                                rule_id="step_performance",
                                rule_name="Step Performance Validation",
                                status=ValidationStatus.PASSED,
                                severity=ValidationSeverity.WARNING,
                                message=f"Step {step.step_id} exceeded timeout",
                                details={
                                    "step_id": step.step_id,
                                    "duration": duration,
                                    "timeout": step.timeout
                                }
                            ))
                
                return results
        except Exception as e:
            self.logger.error(f"Step execution completion validation error: {e}")
        
        return []
    
    def _validate_workflow_completion(self, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate workflow when execution completes"""
        try:
            workflow_def = workflow_data.get("workflow_definition")
            execution = workflow_data.get("workflow_execution")
            
            if workflow_def and execution:
                results = []
                
                # Validate overall workflow completion
                results.extend(self.workflow_validator.validate_workflow_execution(execution))
                
                # Validate performance metrics
                results.extend(self.workflow_validator.validate_workflow_performance(workflow_def, execution))
                
                return results
        except Exception as e:
            self.logger.error(f"Workflow completion validation error: {e}")
        
        return []
    
    def _validate_workflow_failure(self, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate workflow when execution fails"""
        try:
            execution = workflow_data.get("workflow_execution")
            error_info = workflow_data.get("error_info", {})
            
            if execution:
                results = []
                
                # Validate failure state
                if execution.status != WorkflowStatus.FAILED:
                    results.append(ValidationResult(
                        rule_id="workflow_failure_state",
                        rule_name="Workflow Failure State Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Workflow failure state inconsistent",
                        details={
                            "expected_status": WorkflowStatus.FAILED.value,
                            "actual_status": execution.status.value
                        }
                    ))
                
                # Validate error information
                if not error_info:
                    results.append(ValidationResult(
                        rule_id="workflow_failure_info",
                        rule_name="Workflow Failure Info Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message="Workflow failure missing error information",
                        details={"execution_id": execution.execution_id}
                    ))
                
                return results
        except Exception as e:
            self.logger.error(f"Workflow failure validation error: {e}")
        
        return []
    
    def validate_workflow_real_time(self, workflow_def: WorkflowDefinition, execution: WorkflowExecution) -> List[ValidationResult]:
        """Perform real-time validation during workflow execution"""
        start_time = datetime.now()
        
        try:
            results = []
            
            # Validate workflow definition
            def_results = self.workflow_validator.validate_workflow_definition(workflow_def)
            results.extend(def_results)
            
            # Validate current execution state
            exec_results = self.workflow_validator.validate_workflow_execution(execution)
            results.extend(exec_results)
            
            # Validate performance if workflow is running
            if execution.status in [WorkflowStatus.RUNNING, WorkflowStatus.ACTIVE]:
                perf_results = self.workflow_validator.validate_workflow_performance(workflow_def, execution)
                results.extend(perf_results)
            
            # Cache results for this workflow
            self.workflow_validation_cache[execution.execution_id] = results
            
            # Update performance metrics
            validation_time = (datetime.now() - start_time).total_seconds()
            self._update_validation_performance(validation_time, results)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Real-time validation error: {e}")
            error_result = ValidationResult(
                rule_id="real_time_validation_error",
                rule_name="Real-time Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Real-time validation error: {str(e)}",
                details={"error_type": type(e).__name__}
            )
            return [error_result]
    
    def get_workflow_validation_summary(self, execution_id: str) -> Dict[str, Any]:
        """Get validation summary for specific workflow execution"""
        if execution_id in self.workflow_validation_cache:
            results = self.workflow_validation_cache[execution_id]
            
            summary = {
                "execution_id": execution_id,
                "total_validations": len(results),
                "passed": len([r for r in results if r.status == ValidationStatus.PASSED]),
                "failed": len([r for r in results if r.status == ValidationStatus.FAILED]),
                "warnings": len([r for r in results if r.severity == ValidationSeverity.WARNING]),
                "errors": len([r for r in results if r.severity == ValidationSeverity.ERROR]),
                "critical": len([r for r in results if r.severity == ValidationSeverity.CRITICAL]),
                "success_rate": 0.0
            }
            
            if summary["total_validations"] > 0:
                summary["success_rate"] = (summary["passed"] / summary["total_validations"]) * 100
            
            return summary
        
        return {"execution_id": execution_id, "error": "No validation data found"}
    
    def get_validation_performance_metrics(self) -> Dict[str, Any]:
        """Get overall validation performance metrics"""
        return self.performance_metrics.copy()
    
    def _update_performance_metrics(self, results: List[ValidationResult]) -> None:
        """Update performance metrics based on validation results"""
        self.performance_metrics["total_validations"] += len(results)
        
        # Calculate success rate
        successful = len([r for r in results if r.status == ValidationStatus.PASSED])
        if len(results) > 0:
            current_success_rate = (successful / len(results)) * 100
            total_validations = self.performance_metrics["total_validations"]
            
            # Update average success rate
            if total_validations > 0:
                current_avg = self.performance_metrics["validation_success_rate"]
                self.performance_metrics["validation_success_rate"] = (
                    (current_avg * (total_validations - len(results)) + current_success_rate * len(results)) / total_validations
                )
        
        # Count performance issues
        performance_issues = len([r for r in results if "performance" in r.rule_name.lower()])
        self.performance_metrics["performance_issues_detected"] += performance_issues
    
    def _update_validation_performance(self, validation_time: float, results: List[ValidationResult]) -> None:
        """Update validation performance timing metrics"""
        current_avg = self.performance_metrics["validation_time_avg"]
        total_validations = self.performance_metrics["total_validations"]
        
        if total_validations > 0:
            self.performance_metrics["validation_time_avg"] = (
                (current_avg * (total_validations - 1) + validation_time) / total_validations
            )
    
    def clear_validation_cache(self, execution_id: Optional[str] = None) -> None:
        """Clear validation cache for specific workflow or all workflows"""
        if execution_id:
            if execution_id in self.workflow_validation_cache:
                del self.workflow_validation_cache[execution_id]
                self.logger.info(f"Cleared validation cache for workflow: {execution_id}")
        else:
            self.workflow_validation_cache.clear()
            self.logger.info("Cleared all validation caches")
    
    def export_validation_report(self, execution_id: str) -> Dict[str, Any]:
        """Export comprehensive validation report for workflow execution"""
        summary = self.get_workflow_validation_summary(execution_id)
        
        if "error" in summary:
            return summary
        
        # Get detailed results
        results = self.workflow_validation_cache.get(execution_id, [])
        
        report = {
            "execution_id": execution_id,
            "summary": summary,
            "validation_timestamp": datetime.now().isoformat(),
            "detailed_results": [
                {
                    "rule_id": r.rule_id,
                    "rule_name": r.rule_name,
                    "status": r.status.value,
                    "severity": r.severity.value,
                    "message": r.message,
                    "details": r.details
                }
                for r in results
            ],
            "performance_metrics": self.get_validation_performance_metrics()
        }
        
        return report
