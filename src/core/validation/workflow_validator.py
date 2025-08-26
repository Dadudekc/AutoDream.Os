"""
Workflow Validator - Unified Validation Framework

This module provides workflow validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

from typing import Dict, List, Any, Optional
from .base_validator import BaseValidator, ValidationRule, ValidationSeverity, ValidationStatus, ValidationResult


class WorkflowValidator(BaseValidator):
    """Validates workflow data and structure using unified validation framework"""
    
    def __init__(self):
        """Initialize workflow validator"""
        super().__init__("WorkflowValidator")
    
    def _setup_default_rules(self) -> None:
        """Setup default workflow validation rules"""
        default_rules = [
            ValidationRule(
                rule_id="workflow_structure",
                rule_name="Workflow Structure",
                rule_type="workflow",
                description="Validate workflow structure and format",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="required_workflow_fields",
                rule_name="Required Workflow Fields",
                rule_type="workflow",
                description="Ensure all required workflow fields are present",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="step_validation",
                rule_name="Step Validation",
                rule_type="workflow",
                description="Validate workflow steps and transitions",
                severity=ValidationSeverity.ERROR
            ),
            ValidationRule(
                rule_id="workflow_consistency",
                rule_name="Workflow Consistency",
                rule_type="workflow",
                description="Check for workflow consistency and logic",
                severity=ValidationSeverity.WARNING
            )
        ]
        
        for rule in default_rules:
            self.add_validation_rule(rule)
    
    def validate(self, workflow_data: Dict[str, Any], **kwargs) -> List[ValidationResult]:
        """Validate workflow data and return validation results"""
        results = []
        
        try:
            # Validate workflow structure
            structure_results = self._validate_workflow_structure(workflow_data)
            results.extend(structure_results)
            
            # Validate required fields
            required_fields = ["name", "description", "steps", "transitions"]
            field_results = self._validate_required_fields(workflow_data, required_fields)
            results.extend(field_results)
            
            # Validate workflow steps if present
            if "steps" in workflow_data:
                step_results = self._validate_workflow_steps(workflow_data["steps"])
                results.extend(step_results)
            
            # Validate transitions if present
            if "transitions" in workflow_data:
                transition_results = self._validate_workflow_transitions(workflow_data["transitions"])
                results.extend(transition_results)
            
            # Check workflow consistency
            consistency_results = self._validate_workflow_consistency(workflow_data)
            results.extend(consistency_results)
            
            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_workflow_validation",
                    rule_name="Overall Workflow Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Workflow validation passed successfully",
                    details={"total_checks": len(results)}
                )
                results.append(success_result)
            
        except Exception as e:
            error_result = self._create_result(
                rule_id="workflow_validation_error",
                rule_name="Workflow Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Workflow validation error: {str(e)}",
                details={"error_type": type(e).__name__}
            )
            results.append(error_result)
        
        return results
    
    def _validate_workflow_structure(self, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate workflow structure and format"""
        results = []
        
        if not isinstance(workflow_data, dict):
            result = self._create_result(
                rule_id="workflow_type",
                rule_name="Workflow Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Workflow data must be a dictionary",
                actual_value=type(workflow_data).__name__,
                expected_value="dict"
            )
            results.append(result)
            return results
        
        if len(workflow_data) == 0:
            result = self._create_result(
                rule_id="workflow_empty",
                rule_name="Workflow Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="Workflow data is empty",
                actual_value=workflow_data,
                expected_value="non-empty workflow"
            )
            results.append(result)
        
        return results
    
    def _validate_workflow_steps(self, steps: Any) -> List[ValidationResult]:
        """Validate workflow steps"""
        results = []
        
        if not isinstance(steps, list):
            result = self._create_result(
                rule_id="steps_type",
                rule_name="Steps Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Workflow steps must be a list",
                field_path="steps",
                actual_value=type(steps).__name__,
                expected_value="list"
            )
            results.append(result)
            return results
        
        if len(steps) == 0:
            result = self._create_result(
                rule_id="steps_empty",
                rule_name="Steps Empty Check",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Workflow must have at least one step",
                field_path="steps",
                actual_value=steps,
                expected_value="non-empty list"
            )
            results.append(result)
            return results
        
        # Validate each step
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                result = self._create_result(
                    rule_id=f"step_{i}_type",
                    rule_name=f"Step {i} Type Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Step {i} must be a dictionary",
                    field_path=f"steps[{i}]",
                    actual_value=type(step).__name__,
                    expected_value="dict"
                )
                results.append(result)
                continue
            
            # Validate required step fields
            step_required_fields = ["id", "name", "type"]
            step_field_results = self._validate_required_fields(step, step_required_fields)
            for step_result in step_field_results:
                step_result.field_path = f"steps[{i}].{step_result.field_path}"
            results.extend(step_field_results)
            
            # Validate step type
            if "type" in step:
                step_type_result = self._validate_step_type(step["type"], i)
                if step_type_result:
                    results.append(step_type_result)
        
        return results
    
    def _validate_workflow_transitions(self, transitions: Any) -> List[ValidationResult]:
        """Validate workflow transitions"""
        results = []
        
        if not isinstance(transitions, list):
            result = self._create_result(
                rule_id="transitions_type",
                rule_name="Transitions Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Workflow transitions must be a list",
                field_path="transitions",
                actual_value=type(transitions).__name__,
                expected_value="list"
            )
            results.append(result)
            return results
        
        # Validate each transition
        for i, transition in enumerate(transitions):
            if not isinstance(transition, dict):
                result = self._create_result(
                    rule_id=f"transition_{i}_type",
                    rule_name=f"Transition {i} Type Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Transition {i} must be a dictionary",
                    field_path=f"transitions[{i}]",
                    actual_value=type(transition).__name__,
                    expected_value="dict"
                )
                results.append(result)
                continue
            
            # Validate required transition fields
            transition_required_fields = ["from_step", "to_step", "condition"]
            transition_field_results = self._validate_required_fields(transition, transition_required_fields)
            for transition_result in transition_field_results:
                transition_result.field_path = f"transitions[{i}].{transition_result.field_path}"
            results.extend(transition_field_results)
        
        return results
    
    def _validate_step_type(self, step_type: Any, step_index: int) -> Optional[ValidationResult]:
        """Validate step type value"""
        valid_step_types = ["start", "process", "decision", "end", "parallel", "subprocess"]
        
        if not isinstance(step_type, str):
            return self._create_result(
                rule_id=f"step_{step_index}_type_value",
                rule_name=f"Step {step_index} Type Value Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Step {step_index} type must be a string",
                field_path=f"steps[{step_index}].type",
                actual_value=type(step_type).__name__,
                expected_value="str"
            )
        
        if step_type not in valid_step_types:
            return self._create_result(
                rule_id=f"step_{step_index}_type_invalid",
                rule_name=f"Step {step_index} Type Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid step type '{step_type}' for step {step_index}",
                field_path=f"steps[{step_index}].type",
                actual_value=step_type,
                expected_value=f"one of {valid_step_types}"
            )
        
        return None
    
    def _validate_workflow_consistency(self, workflow_data: Dict[str, Any]) -> List[ValidationResult]:
        """Check for workflow consistency and logic"""
        results = []
        
        # Check if steps and transitions are consistent
        if "steps" in workflow_data and "transitions" in workflow_data:
            steps = workflow_data["steps"]
            transitions = workflow_data["transitions"]
            
            if isinstance(steps, list) and isinstance(transitions, list):
                # Get all step IDs
                step_ids = set()
                for step in steps:
                    if isinstance(step, dict) and "id" in step:
                        step_ids.add(step["id"])
                
                # Check if transition references exist in steps
                for i, transition in enumerate(transitions):
                    if isinstance(transition, dict):
                        from_step = transition.get("from_step")
                        to_step = transition.get("to_step")
                        
                        if from_step and from_step not in step_ids:
                            result = self._create_result(
                                rule_id=f"transition_{i}_from_invalid",
                                rule_name=f"Transition {i} From Step Invalid",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=f"Transition {i} references non-existent step '{from_step}'",
                                field_path=f"transitions[{i}].from_step",
                                actual_value=from_step,
                                expected_value=f"one of {list(step_ids)}"
                            )
                            results.append(result)
                        
                        if to_step and to_step not in step_ids:
                            result = self._create_result(
                                rule_id=f"transition_{i}_to_invalid",
                                rule_name=f"Transition {i} To Step Invalid",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=f"Transition {i} references non-existent step '{to_step}'",
                                field_path=f"transitions[{i}].to_step",
                                actual_value=to_step,
                                expected_value=f"one of {list(step_ids)}"
                            )
                            results.append(result)
                
                # Check for orphaned steps (steps with no incoming transitions)
                if len(step_ids) > 1:  # More than just start step
                    incoming_steps = set()
                    for transition in transitions:
                        if isinstance(transition, dict) and "to_step" in transition:
                            incoming_steps.add(transition["to_step"])
                    
                    orphaned_steps = step_ids - incoming_steps
                    if orphaned_steps:
                        result = self._create_result(
                            rule_id="orphaned_steps",
                            rule_name="Orphaned Steps Check",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=f"Steps with no incoming transitions: {list(orphaned_steps)}",
                            details={"orphaned_steps": list(orphaned_steps)}
                        )
                        results.append(result)
        
        return results

    # Advanced Workflow Validation functionality integration
    def validate_workflow_execution_state(self, execution: Dict[str, Any]) -> List[ValidationResult]:
        """Validate workflow execution state for consistency (from advanced workflow validation)"""
        results = []
        
        try:
            # Check execution ID
            if not execution.get("execution_id"):
                result = self._create_result(
                    rule_id="execution_id_missing",
                    rule_name="Execution ID Missing",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Execution ID is required",
                    field_path="execution_id",
                    actual_value=execution.get("execution_id"),
                    expected_value="non-empty string"
                )
                results.append(result)
            
            # Check workflow ID
            if not execution.get("workflow_id"):
                result = self._create_result(
                    rule_id="workflow_id_missing",
                    rule_name="Workflow ID Missing",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Workflow ID is required",
                    field_path="workflow_id",
                    actual_value=execution.get("workflow_id"),
                    expected_value="non-empty string"
                )
                results.append(result)
            
            # Check status consistency
            status = execution.get("status")
            if status == "completed" and not execution.get("actual_completion"):
                result = self._create_result(
                    rule_id="completion_timestamp_missing",
                    rule_name="Completion Timestamp Missing",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Completed workflow must have completion timestamp",
                    field_path="actual_completion",
                    actual_value=execution.get("actual_completion"),
                    expected_value="timestamp"
                )
                results.append(result)
            
            if status == "failed" and not execution.get("failed_steps"):
                result = self._create_result(
                    rule_id="failed_steps_missing",
                    rule_name="Failed Steps Missing",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message="Failed workflow has no failed steps recorded",
                    field_path="failed_steps",
                    actual_value=execution.get("failed_steps"),
                    expected_value="list of failed steps"
                )
                results.append(result)
            
            # Check step consistency
            completed_steps = execution.get("completed_steps", [])
            failed_steps = execution.get("failed_steps", [])
            
            if completed_steps and failed_steps:
                # Check for overlap between completed and failed steps
                overlap = set(completed_steps) & set(failed_steps)
                if overlap:
                    result = self._create_result(
                        rule_id="step_status_conflict",
                        rule_name="Step Status Conflict",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Steps cannot be both completed and failed: {list(overlap)}",
                        field_path="step_status",
                        actual_value=f"overlap: {list(overlap)}",
                        expected_value="steps cannot be both completed and failed"
                    )
                    results.append(result)
            
            # Check timestamps
            start_time = execution.get("start_time")
            if start_time:
                try:
                    from datetime import datetime
                    start_dt = datetime.fromisoformat(start_time)
                    if start_dt > datetime.now():
                        result = self._create_result(
                            rule_id="start_time_future",
                            rule_name="Start Time in Future",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message="Start time is in the future",
                            field_path="start_time",
                            actual_value=start_time,
                            expected_value="past or current timestamp"
                        )
                        results.append(result)
                except ValueError:
                    result = self._create_result(
                        rule_id="start_time_invalid",
                        rule_name="Start Time Invalid Format",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Invalid start time format",
                        field_path="start_time",
                        actual_value=start_time,
                        expected_value="ISO format timestamp"
                    )
                    results.append(result)
            
            actual_completion = execution.get("actual_completion")
            if actual_completion and start_time:
                try:
                    from datetime import datetime
                    completion_dt = datetime.fromisoformat(actual_completion)
                    start_dt = datetime.fromisoformat(start_time)
                    if completion_dt < start_dt:
                        result = self._create_result(
                            rule_id="completion_before_start",
                            rule_name="Completion Before Start",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message="Completion time cannot be before start time",
                            field_path="actual_completion",
                            actual_value=actual_completion,
                            expected_value="timestamp after start_time"
                        )
                        results.append(result)
                except ValueError:
                    result = self._create_result(
                        rule_id="completion_time_invalid",
                        rule_name="Completion Time Invalid Format",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Invalid completion time format",
                        field_path="actual_completion",
                        actual_value=actual_completion,
                        expected_value="ISO format timestamp"
                    )
                    results.append(result)
            
        except Exception as e:
            result = self._create_result(
                rule_id="execution_validation_error",
                rule_name="Execution Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Execution validation error: {str(e)}",
                details={"error": str(e)}
            )
            results.append(result)
        
        return results
    
    def validate_performance_metrics(self, metrics: Dict[str, float]) -> List[ValidationResult]:
        """Validate performance metrics for reasonableness (from advanced workflow validation)"""
        results = []
        
        try:
            # Performance thresholds
            PERFORMANCE_THRESHOLDS = {
                "execution_time": 3600000,  # 1000 hours
                "memory_usage": 10000,      # 10GB
                "cpu_usage": 100,           # 100%
                "response_time": 1000       # 1 second
            }
            
            for metric_name, value in metrics.items():
                if not isinstance(value, (int, float)):
                    result = self._create_result(
                        rule_id=f"metric_{metric_name}_type",
                        rule_name=f"Metric {metric_name} Type Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Metric {metric_name}: value must be numeric",
                        field_path=f"metrics.{metric_name}",
                        actual_value=type(value).__name__,
                        expected_value="numeric"
                    )
                    results.append(result)
                    continue
                
                # Check for negative values where inappropriate
                if metric_name in ["execution_time", "memory_usage", "cpu_usage", "response_time"]:
                    if value < 0:
                        result = self._create_result(
                            rule_id=f"metric_{metric_name}_negative",
                            rule_name=f"Metric {metric_name} Negative Value",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Metric {metric_name}: cannot be negative",
                            field_path=f"metrics.{metric_name}",
                            actual_value=value,
                            expected_value=">= 0"
                        )
                        results.append(result)
                        continue
                
                # Check against thresholds
                if metric_name in PERFORMANCE_THRESHOLDS:
                    threshold = PERFORMANCE_THRESHOLDS[metric_name]
                    if value > threshold:
                        result = self._create_result(
                            rule_id=f"metric_{metric_name}_threshold",
                            rule_name=f"Metric {metric_name} Threshold Exceeded",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=f"Metric {metric_name}: {value} exceeds threshold {threshold}",
                            field_path=f"metrics.{metric_name}",
                            actual_value=value,
                            expected_value=f"<= {threshold}"
                        )
                        results.append(result)
                
                # Check for unreasonably high values
                if metric_name == "execution_time" and value > 3600000:  # 1000 hours
                    result = self._create_result(
                        rule_id=f"metric_{metric_name}_unreasonable",
                        rule_name=f"Metric {metric_name} Unreasonable Value",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Metric {metric_name}: value seems unreasonably high",
                        field_path=f"metrics.{metric_name}",
                        actual_value=value,
                        expected_value="reasonable execution time"
                    )
                    results.append(result)
                elif metric_name == "memory_usage" and value > 10000:  # 10GB
                    result = self._create_result(
                        rule_id=f"metric_{metric_name}_unreasonable",
                        rule_name=f"Metric {metric_name} Unreasonable Value",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Metric {metric_name}: value seems unreasonably high",
                        field_path=f"metrics.{metric_name}",
                        actual_value=value,
                        expected_value="reasonable memory usage"
                    )
                    results.append(result)
                elif metric_name == "cpu_usage" and value > 100:  # 100%
                    result = self._create_result(
                        rule_id=f"metric_{metric_name}_unreasonable",
                        rule_name=f"Metric {metric_name} Unreasonable Value",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Metric {metric_name}: value exceeds 100%",
                        field_path=f"metrics.{metric_name}",
                        actual_value=value,
                        expected_value="<= 100%"
                    )
                    results.append(result)
            
        except Exception as e:
            result = self._create_result(
                rule_id="performance_validation_error",
                rule_name="Performance Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Performance validation error: {str(e)}",
                details={"error": str(e)}
            )
            results.append(result)
        
        return results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of validation results (from advanced workflow validation)"""
        from datetime import datetime
        
        return {
            "total_errors": len([r for r in self.validation_history if r.severity.value == "error"]),
            "total_warnings": len([r for r in self.validation_history if r.severity.value == "warning"]),
            "total_passed": len([r for r in self.validation_history if r.status.value == "passed"]),
            "total_failed": len([r for r in self.validation_history if r.status.value == "failed"]),
            "validation_timestamp": datetime.now().isoformat(),
            "validation_history_count": len(self.validation_history)
        }
    
    def clear_validation_results(self):
        """Clear validation results (from advanced workflow validation)"""
        self.validation_history.clear()
