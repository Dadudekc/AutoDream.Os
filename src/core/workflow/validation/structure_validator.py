"""Workflow structure validation logic."""

from typing import List

from src.core.validation import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from ..types.workflow_enums import WorkflowType
from ..types.workflow_models import WorkflowDefinition, WorkflowStep


class WorkflowStructureValidator(BaseValidator):
    """Validate workflow definitions and step dependencies."""

    def __init__(self) -> None:
        super().__init__("WorkflowStructureValidator")

    def validate(self, workflow_def: WorkflowDefinition, **_) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        try:
            if not workflow_def.workflow_id or not workflow_def.name:
                results.append(
                    self._create_result(
                        rule_id="workflow_structure",
                        rule_name="Workflow Structure Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Workflow must have valid ID and name",
                        details={
                            "workflow_id": workflow_def.workflow_id,
                            "name": workflow_def.name,
                        },
                    )
                )

            if not workflow_def.steps:
                results.append(
                    self._create_result(
                        rule_id="workflow_structure",
                        rule_name="Workflow Structure Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Workflow must have at least one step",
                        details={"step_count": len(workflow_def.steps)},
                    )
                )
            else:
                results.extend(self._validate_workflow_steps(workflow_def.steps))
                results.extend(self._validate_step_dependencies(workflow_def.steps))

            if workflow_def.workflow_type not in WorkflowType:
                results.append(
                    self._create_result(
                        rule_id="workflow_structure",
                        rule_name="Workflow Structure Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Invalid workflow type",
                        details={
                            "workflow_type": workflow_def.workflow_type,
                            "valid_types": [t.value for t in WorkflowType],
                        },
                    )
                )

            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                results.append(
                    self._create_result(
                        rule_id="workflow_structure",
                        rule_name="Workflow Structure Validation",
                        status=ValidationStatus.PASSED,
                        severity=ValidationSeverity.INFO,
                        message="Workflow definition validation passed",
                        details={
                            "step_count": len(workflow_def.steps),
                            "workflow_type": workflow_def.workflow_type.value,
                        },
                    )
                )
        except Exception as e:  # pragma: no cover - defensive
            results.append(
                self._create_result(
                    rule_id="workflow_structure",
                    rule_name="Workflow Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.CRITICAL,
                    message=f"Workflow validation error: {e}",
                    details={"error_type": type(e).__name__},
                )
            )

        return results

    def _validate_workflow_steps(
        self, steps: List[WorkflowStep]
    ) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        for i, step in enumerate(steps):
            if not step.step_id or not step.step_id.strip():
                results.append(
                    self._create_result(
                        rule_id="workflow_structure",
                        rule_name="Workflow Structure Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Step {i} must have valid ID",
                        details={"step_index": i, "step_id": step.step_id},
                    )
                )

            if not step.name or not step.name.strip():
                results.append(
                    self._create_result(
                        rule_id="workflow_structure",
                        rule_name="Workflow Structure Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Step {i} must have valid name",
                        details={"step_index": i, "step_name": step.name},
                    )
                )

            if not step.step_type or not step.step_type.strip():
                results.append(
                    self._create_result(
                        rule_id="workflow_structure",
                        rule_name="Workflow Structure Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Step {i} must have valid type",
                        details={"step_index": i, "step_type": step.step_type},
                    )
                )

            if step.estimated_duration < 0:
                results.append(
                    self._create_result(
                        rule_id="workflow_structure",
                        rule_name="Workflow Structure Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message=f"Step {i} has negative estimated duration",
                        details={
                            "step_index": i,
                            "estimated_duration": step.estimated_duration,
                        },
                    )
                )

        return results

    def _validate_step_dependencies(
        self, steps: List[WorkflowStep]
    ) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        step_ids = {step.step_id for step in steps}

        for i, step in enumerate(steps):
            for dep in step.dependencies:
                if dep not in step_ids:
                    results.append(
                        self._create_result(
                            rule_id="step_dependencies",
                            rule_name="Step Dependencies Validation",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Step {i} references non-existent dependency: {dep}",
                            details={
                                "step_index": i,
                                "step_id": step.step_id,
                                "invalid_dependency": dep,
                            },
                        )
                    )

            if step.step_id in step.dependencies:
                results.append(
                    self._create_result(
                        rule_id="step_dependencies",
                        rule_name="Step Dependencies Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Step {i} has self-dependency",
                        details={"step_index": i, "step_id": step.step_id},
                    )
                )

        results.extend(self._detect_dependency_cycles(steps))
        return results

    def _detect_dependency_cycles(
        self, steps: List[WorkflowStep]
    ) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        for i, step in enumerate(steps):
            visited = set()
            if self._has_cycle_recursive(step, steps, visited, set()):
                results.append(
                    self._create_result(
                        rule_id="step_dependencies",
                        rule_name="Step Dependencies Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Circular dependency detected involving step {i}",
                        details={"step_index": i, "step_id": step.step_id},
                    )
                )

        return results

    def _has_cycle_recursive(
        self, step: WorkflowStep, all_steps: List[WorkflowStep], visited: set, path: set
    ) -> bool:
        if step.step_id in path:
            return True
        if step.step_id in visited:
            return False

        visited.add(step.step_id)
        path.add(step.step_id)

        for dep_id in step.dependencies:
            dep_step = next((s for s in all_steps if s.step_id == dep_id), None)
            if dep_step and self._has_cycle_recursive(
                dep_step, all_steps, visited, path
            ):
                return True

        path.remove(step.step_id)
        return False
