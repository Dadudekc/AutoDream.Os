"""Coordinator for workflow validation."""

from typing import Any, Dict, List

from src.core.validation import BaseValidator, ValidationResult

from .structure_validator import WorkflowStructureValidator
from .execution_validator import WorkflowExecutionValidator
from .performance_validator import WorkflowPerformanceValidator
from ..types.workflow_models import WorkflowDefinition, WorkflowExecution


class WorkflowValidator(BaseValidator):
    """Aggregate workflow validator that delegates to specialized validators."""

    def __init__(self) -> None:
        self.structure_validator = WorkflowStructureValidator()
        self.execution_validator = WorkflowExecutionValidator()
        self.performance_validator = WorkflowPerformanceValidator()
        super().__init__("WorkflowValidator")
        for validator in (
            self.structure_validator,
            self.execution_validator,
            self.performance_validator,
        ):
            for rule in validator.get_validation_rules().values():
                self.add_validation_rule(rule)

    def validate(self, data: Dict[str, Any], **_) -> List[ValidationResult]:
        results: List[ValidationResult] = []

        definition: WorkflowDefinition | None = data.get("definition")
        execution: WorkflowExecution | None = data.get("execution")

        if definition is not None:
            results.extend(self.structure_validator.validate(definition))
        if execution is not None:
            results.extend(self.execution_validator.validate(execution))
        if definition is not None and execution is not None:
            results.extend(self.performance_validator.validate(definition, execution))

        self.validation_history.extend(results)
        if len(self.validation_history) > 1000:
            self.validation_history = self.validation_history[-1000:]

        return results
