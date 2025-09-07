"""Workflow performance validation logic."""

from typing import List

from src.core.validation import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from ..types.workflow_models import WorkflowDefinition, WorkflowExecution


class WorkflowPerformanceValidator(BaseValidator):
    """Validate workflow performance metrics."""

    def __init__(self) -> None:
        super().__init__("WorkflowPerformanceValidator")

    def validate(
        self, workflow_def: WorkflowDefinition, execution: WorkflowExecution, **_
    ) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        try:
            total_estimated = sum(
                step.estimated_duration for step in workflow_def.steps
            )

            if execution.start_time and execution.end_time:
                actual_duration = (
                    execution.end_time - execution.start_time
                ).total_seconds()
                variance_threshold = total_estimated * 0.2
                if abs(actual_duration - total_estimated) > variance_threshold:
                    results.append(
                        self._create_result(
                            rule_id="performance_metrics",
                            rule_name="Performance Metrics Validation",
                            status=ValidationStatus.PASSED,
                            severity=ValidationSeverity.WARNING,
                            message="Workflow execution time differs significantly from estimate",
                            details={
                                "estimated_duration": total_estimated,
                                "actual_duration": actual_duration,
                                "variance": abs(actual_duration - total_estimated),
                                "threshold": variance_threshold,
                            },
                        )
                    )

            long_steps = [
                step for step in workflow_def.steps if step.estimated_duration > 300
            ]
            if long_steps:
                results.append(
                    self._create_result(
                        rule_id="performance_metrics",
                        rule_name="Performance Metrics Validation",
                        status=ValidationStatus.PASSED,
                        severity=ValidationSeverity.INFO,
                        message="Long-running steps detected - consider optimization",
                        details={
                            "long_steps": [
                                {"step_id": s.step_id, "duration": s.estimated_duration}
                                for s in long_steps
                            ]
                        },
                    )
                )
        except Exception as e:  # pragma: no cover - defensive
            results.append(
                self._create_result(
                    rule_id="performance_metrics",
                    rule_name="Performance Metrics Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message=f"Performance validation error: {e}",
                    details={"error_type": type(e).__name__},
                )
            )

        return results
