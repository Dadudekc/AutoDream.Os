"""Validation rule execution module.

Handles applying validation rules to contract data and producing
individual validation results.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Tuple

from .validation_rules import (
    ValidationRule,
    ValidationRuleManager,
    ValidationResult,
    ValidationSeverity,
)
from .constants import DEFAULT_CONTRACT_ID


class ValidationExecutor:
    """Execute validation rules against contract data."""

    def __init__(self, rule_manager: ValidationRuleManager | None = None) -> None:
        self.rule_manager = rule_manager or ValidationRuleManager()

    def execute(self, contract_data: Dict[str, Any]) -> List[ValidationResult]:
        """Run all enabled rules and return their results."""
        results: List[ValidationResult] = []
        enabled_rules = [
            rule for rule in self.rule_manager.get_all_rules().values() if rule.enabled
        ]
        for rule in enabled_rules:
            passed, message, details = self._apply_rule(rule, contract_data)
            results.append(
                ValidationResult(
                    contract_id=contract_data.get("contract_id", DEFAULT_CONTRACT_ID),
                    rule_id=rule.rule_id,
                    passed=passed,
                    severity=rule.severity,
                    message=message,
                    details=details,
                    timestamp=time.time(),
                )
            )
        return results

    def _apply_rule(self, rule: ValidationRule, contract_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Apply a single rule and return pass state, message and details."""
        handler_name = f"_rule_{rule.rule_id}"
        handler = getattr(self, handler_name, self._rule_generic)
        return handler(contract_data)

    # Rule handlers -----------------------------------------------------
    def _rule_deadline_check(self, data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        deadline = data.get("deadline")
        delivery_date = data.get("delivery_date")
        passed = bool(deadline and delivery_date and delivery_date <= deadline)
        message = "Deadline met" if passed else "Deadline exceeded"
        return passed, message, {"deadline": deadline, "delivery_date": delivery_date}

    def _rule_quality_standard(self, data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        quality_score = data.get("quality_score", 0)
        minimum_standard = data.get("minimum_standard", 0)
        passed = quality_score >= minimum_standard
        message = "Quality standards met" if passed else "Quality below standard"
        return passed, message, {
            "quality_score": quality_score,
            "minimum_standard": minimum_standard,
        }

    def _rule_resource_limit(self, data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        usage = data.get("resource_usage", 0)
        limit = data.get("resource_limit", 0)
        passed = usage <= limit
        message = "Resource usage within limits" if passed else "Resource usage exceeded"
        return passed, message, {"resource_usage": usage, "resource_limit": limit}

    def _rule_dependency_check(self, data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        deps = data.get("dependencies", [])
        completed = data.get("completed_dependencies", [])
        all_done = all(dep in completed for dep in deps)
        message = "All dependencies satisfied" if all_done else "Dependencies not satisfied"
        return all_done, message, {
            "dependencies": deps,
            "completed_dependencies": completed,
        }

    def _rule_generic(self, data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        return True, "Rule passed", {}
