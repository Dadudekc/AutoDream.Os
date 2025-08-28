from __future__ import annotations

"""Validation evaluation logic separated from orchestration.

This module focuses solely on evaluating contract data against
validation rules. It contains no knowledge of rule configuration or
remediation behaviour.
"""
from typing import Dict, List, Any, Callable, Tuple
import time
import logging

from .validation_rules import (
    ValidationRule,
    ValidationResult,
    ValidationSeverity,
)


class ValidationEvaluator:
    """Evaluate contract data against validation rules."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.ValidationEvaluator")
        self.handlers: Dict[
            str,
            Callable[
                [ValidationRule, Dict[str, Any]], Tuple[bool, str, Dict[str, Any]]
            ],
        ] = {
            "temporal": self._validate_temporal_rule,
            "quality": self._validate_quality_rule,
            "resource": self._validate_resource_rule,
            "dependency": self._validate_dependency_rule,
            "schema": self._validate_schema_rule,
        }

    def evaluate(
        self, rules: List[ValidationRule], contract_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Evaluate enabled rules against provided contract data."""

        results: List[ValidationResult] = []
        contract_id = contract_data.get("contract_id", "unknown")

        for rule in rules:
            handler = self.handlers.get(rule.rule_type, self._validate_generic_rule)
            try:
                passed, message, details = handler(rule, contract_data)
                severity = rule.severity
            except Exception as exc:  # pragma: no cover - defensive
                self.logger.error("Error evaluating rule %s: %s", rule.rule_id, exc)
                passed, message, details = (
                    False,
                    f"Validation exception: {exc}",
                    {"error": str(exc)},
                )
                severity = ValidationSeverity.ERROR

            results.append(
                ValidationResult(
                    contract_id=contract_id,
                    rule_id=rule.rule_id,
                    passed=passed,
                    severity=severity,
                    message=message,
                    details=details,
                    timestamp=time.time(),
                )
            )

        return results

    # --- Rule Handlers -------------------------------------------------

    def _validate_temporal_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate temporal rules such as deadline checks."""
        if rule.rule_id == "deadline_check":
            deadline = contract_data.get("deadline")
            delivery_date = contract_data.get("delivery_date")
            if not deadline or not delivery_date:
                return (
                    False,
                    "Missing deadline or delivery date",
                    {
                        "deadline": deadline,
                        "delivery_date": delivery_date,
                    },
                )
            passed = delivery_date <= deadline
            return (
                passed,
                ("Deadline met" if passed else "Deadline exceeded"),
                {
                    "deadline": deadline,
                    "delivery_date": delivery_date,
                    "on_time": passed,
                },
            )
        return True, "Temporal rule passed", {}

    def _validate_quality_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate quality related rules."""
        if rule.rule_id == "quality_standard":
            quality_score = contract_data.get("quality_score", 0)
            minimum_standard = contract_data.get("minimum_standard", 80)
            passed = quality_score >= minimum_standard
            return (
                passed,
                ("Quality standards met" if passed else "Quality below standard"),
                {
                    "quality_score": quality_score,
                    "minimum_standard": minimum_standard,
                    "passed": passed,
                },
            )
        return True, "Quality rule passed", {}

    def _validate_resource_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate resource related rules."""
        if rule.rule_id == "resource_limit":
            resource_usage = contract_data.get("resource_usage", 0)
            resource_limit = contract_data.get("resource_limit", 100)
            passed = resource_usage <= resource_limit
            return (
                passed,
                (
                    "Resource usage within limits"
                    if passed
                    else "Resource usage exceeded"
                ),
                {
                    "resource_usage": resource_usage,
                    "resource_limit": resource_limit,
                    "within_limits": passed,
                },
            )
        return True, "Resource rule passed", {}

    def _validate_dependency_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate dependency related rules."""
        if rule.rule_id == "dependency_check":
            dependencies = contract_data.get("dependencies", [])
            completed = contract_data.get("completed_dependencies", [])
            all_completed = all(dep in completed for dep in dependencies)
            return (
                all_completed,
                (
                    "All dependencies satisfied"
                    if all_completed
                    else "Dependencies not satisfied"
                ),
                {
                    "dependencies": dependencies,
                    "completed_dependencies": completed,
                    "all_satisfied": all_completed,
                },
            )
        return True, "Dependency rule passed", {}

    def _validate_schema_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate schema related rules."""
        required_fields = contract_data.get("required_fields", [])
        missing = [field for field in required_fields if field not in contract_data]
        passed = not missing
        message = (
            "Schema validation passed"
            if passed
            else f"Missing required fields: {missing}"
        )
        return (
            passed,
            message,
            {
                "required_fields": required_fields,
                "missing_fields": missing,
                "valid": passed,
            },
        )

    def _validate_generic_rule(
        self, rule: ValidationRule, contract_data: Dict[str, Any]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Fallback handler for unspecified rule types."""
        return True, "Generic rule passed", {"rule_type": rule.rule_type}
