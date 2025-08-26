"""Workflow execution validation logic."""

from typing import List

from src.core.validation import (
    BaseValidator,
    ValidationResult,
    ValidationRule,
    ValidationSeverity,
    ValidationStatus,
)
from ..types.workflow_enums import WorkflowStatus, TaskStatus
from ..types.workflow_models import WorkflowExecution, WorkflowStep


class WorkflowExecutionValidator(BaseValidator):
    """Validate workflow execution state and transitions."""

    def __init__(self) -> None:
        super().__init__("WorkflowExecutionValidator")

    def _setup_default_rules(self) -> None:  # pragma: no cover - simple rule setup
        self.add_validation_rule(
            ValidationRule(
                rule_id="workflow_execution",
                rule_name="Workflow Execution Validation",
                rule_type="workflow",
                description="Validate workflow execution state and transitions",
                severity=ValidationSeverity.ERROR,
            )
        )

    def validate(self, execution: WorkflowExecution, **_) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        try:
            if execution.status not in WorkflowStatus:
                results.append(
                    self._create_result(
                        rule_id="workflow_execution",
                        rule_name="Workflow Execution Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Invalid workflow execution status",
                        details={
                            "status": execution.status,
                            "valid_statuses": [s.value for s in WorkflowStatus],
                        },
                    )
                )

            if execution.steps:
                results.extend(self._validate_step_execution_states(execution.steps))

            if execution.start_time and execution.end_time:
                results.extend(self._validate_execution_timing(execution))

            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                results.append(
                    self._create_result(
                        rule_id="workflow_execution",
                        rule_name="Workflow Execution Validation",
                        status=ValidationStatus.PASSED,
                        severity=ValidationSeverity.INFO,
                        message="Workflow execution validation passed",
                        details={
                            "status": execution.status.value,
                            "step_count": len(execution.steps),
                        },
                    )
                )
        except Exception as e:  # pragma: no cover - defensive
            results.append(
                self._create_result(
                    rule_id="workflow_execution",
                    rule_name="Workflow Execution Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.CRITICAL,
                    message=f"Execution validation error: {e}",
                    details={"error_type": type(e).__name__},
                )
            )

        return results

    def _validate_step_execution_states(self, steps: List[WorkflowStep]) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        for i, step in enumerate(steps):
            if step.status not in TaskStatus:
                results.append(
                    self._create_result(
                        rule_id="workflow_execution",
                        rule_name="Workflow Execution Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Step {i} has invalid execution status",
                        details={
                            "step_index": i,
                            "step_id": step.step_id,
                            "status": step.status,
                        },
                    )
                )

            if step.start_time and step.end_time and step.start_time > step.end_time:
                results.append(
                    self._create_result(
                        rule_id="workflow_execution",
                        rule_name="Workflow Execution Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message=f"Step {i} has inconsistent timing",
                        details={
                            "step_index": i,
                            "step_id": step.step_id,
                            "start_time": step.start_time,
                            "end_time": step.end_time,
                        },
                    )
                )

        return results

    def _validate_execution_timing(self, execution: WorkflowExecution) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        if execution.start_time > execution.end_time:
            results.append(
                self._create_result(
                    rule_id="workflow_execution",
                    rule_name="Workflow Execution Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message="Workflow execution has inconsistent timing",
                    details={
                        "start_time": execution.start_time,
                        "end_time": execution.end_time,
                    },
                )
            )

        return results
