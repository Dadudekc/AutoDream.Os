from datetime import datetime, timezone
from typing import Any, Dict

from .models import WorkflowExecution, WorkflowStep


class WorkflowValidationSystem:
    """System for validating workflow steps and results"""

    def __init__(self) -> None:
        self.validation_rules = {}
        self._initialize_validation_rules()

    def _initialize_validation_rules(self) -> None:
        """Initialize validation rules for different step types"""
        self.validation_rules = {
            "structure_valid": lambda result: result.get("structure_analyzed", False),
            "patterns_found": lambda result: result.get("patterns_found", 0) >= 1,
            "recommendations_generated": lambda result: result.get(
                "recommendations_generated", 0
            )
            >= 1,
            "complexity_analyzed": lambda result: result.get(
                "complexity_analyzed", False
            ),
            "structure_designed": lambda result: result.get(
                "structure_designed", False
            ),
            "modularization_implemented": lambda result: result.get(
                "modularization_implemented", False
            ),
        }

    def validate_step(
        self, step: WorkflowStep, result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate a workflow step result"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        for rule in step.validation_rules:
            rule_type = rule["type"]
            if rule_type in self.validation_rules:
                try:
                    if not self.validation_rules[rule_type](result):
                        validation_result["valid"] = False
                        validation_result["errors"].append(
                            f"Validation rule failed: {rule_type}"
                        )
                except Exception as exc:  # pragma: no cover - defensive
                    validation_result["valid"] = False
                    validation_result["errors"].append(
                        f"Validation error for {rule_type}: {exc}"
                    )
            else:
                validation_result["warnings"].append(
                    f"Unknown validation rule: {rule_type}"
                )

        return validation_result

    def validate_workflow(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Validate complete workflow execution"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        expected_steps = len(execution.steps_completed)

        if len(execution.steps_completed) < expected_steps:
            validation_result["valid"] = False
            validation_result["errors"].append(
                f"Not all steps completed: {len(execution.steps_completed)}/{expected_steps}"
            )

        if execution.error_log:
            validation_result["valid"] = False
            validation_result["errors"].extend(execution.error_log)

        return validation_result
