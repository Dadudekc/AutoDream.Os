"""Task Validator - orchestrates task validation using modular components."""

from __future__ import annotations

from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from .task_validation_errors import create_error_result
from .task_validation_execution import (
    validate_task_assignment,
    validate_task_consistency,
    validate_task_dependencies,
    validate_task_priority,
    validate_task_progress,
    validate_task_status,
    validate_task_structure,
    validate_task_type,
)
from .task_validation_rules import (
    DEFAULT_TASK_RULES,
    TASK_PRIORITIES,
    TASK_STATUSES,
    TASK_TYPES,
)


class TaskValidator(BaseValidator):
    """Validates task data and assignments using the unified validation framework."""

    def __init__(self) -> None:
        super().__init__("TaskValidator")
        # Expose modifiable copies of shared constants.
        self.task_statuses = TASK_STATUSES.copy()
        self.task_priorities = TASK_PRIORITIES.copy()
        self.task_types = TASK_TYPES.copy()
        for rule in DEFAULT_TASK_RULES:
            self.add_validation_rule(rule)

    def validate(
        self, task_data: Dict[str, Any], **kwargs: Any
    ) -> List[ValidationResult]:
        """Validate task data and return validation results."""
        results: List[ValidationResult] = []
        try:
            results.extend(validate_task_structure(self, task_data))
            required_fields = ["id", "title", "description", "status", "priority"]
            results.extend(self._validate_required_fields(task_data, required_fields))
            if "status" in task_data:
                status_result = validate_task_status(self, task_data["status"])
                if status_result:
                    results.append(status_result)
            if "priority" in task_data:
                priority_result = validate_task_priority(self, task_data["priority"])
                if priority_result:
                    results.append(priority_result)
            if "type" in task_data:
                type_result = validate_task_type(self, task_data["type"])
                if type_result:
                    results.append(type_result)
            if "assignment" in task_data:
                results.extend(validate_task_assignment(self, task_data["assignment"]))
            if "dependencies" in task_data:
                results.extend(
                    validate_task_dependencies(self, task_data["dependencies"])
                )
            if "progress" in task_data:
                results.extend(validate_task_progress(self, task_data["progress"]))
            results.extend(validate_task_consistency(self, task_data))
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success = self._create_result(
                    rule_id="overall_task_validation",
                    rule_name="Overall Task Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Task validation passed successfully",
                    details={"total_checks": len(results)},
                )
                results.append(success)
        except Exception as error:  # pragma: no cover - defensive
            results.append(create_error_result(self, error))
        return results

    def add_task_status(self, status: str) -> bool:
        """Add a custom task status."""
        try:
            if status not in self.task_statuses:
                self.task_statuses.append(status)
                self.logger.info(f"Task status added: {status}")
            return True
        except Exception as exc:  # pragma: no cover - logging helper
            self.logger.error(f"Failed to add task status: {exc}")
            return False

    def add_task_priority(self, priority: str) -> bool:
        """Add a custom task priority."""
        try:
            if priority not in self.task_priorities:
                self.task_priorities.append(priority)
                self.logger.info(f"Task priority added: {priority}")
            return True
        except Exception as exc:  # pragma: no cover - logging helper
            self.logger.error(f"Failed to add task priority: {exc}")
            return False

    def add_task_type(self, task_type: str) -> bool:
        """Add a custom task type."""
        try:
            if task_type not in self.task_types:
                self.task_types.append(task_type)
                self.logger.info(f"Task type added: {task_type}")
            return True
        except Exception as exc:  # pragma: no cover - logging helper
            self.logger.error(f"Failed to add task type: {exc}")
            return False
