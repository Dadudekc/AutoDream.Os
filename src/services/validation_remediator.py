"""Remediation logic for contract validation failures."""
from __future__ import annotations

import time
from typing import Optional

from .validation_rules import (
    ValidationResult,
    Violation,
    ViolationType,
    ValidationRule,
    ValidationRuleManager,
)


class RemediationManager:
    """Create violation records and map rules to remediation actions."""

    def __init__(self, rule_manager: ValidationRuleManager) -> None:
        self.rule_manager = rule_manager

    def create_violation(self, validation_result: ValidationResult) -> Violation:
        """Convert a failed validation result into a :class:`Violation`."""
        if validation_result.passed:
            raise ValueError("Cannot create violation from passed validation")

        rule: Optional[ValidationRule] = self.rule_manager.get_rule(
            validation_result.rule_id
        )
        violation_type = (
            self._map_rule_to_violation_type(rule)
            if rule
            else ViolationType.SCHEMA_VIOLATION
        )

        return Violation(
            violation_id=f"violation_{int(time.time())}_{validation_result.rule_id}",
            contract_id=validation_result.contract_id,
            violation_type=violation_type,
            severity=validation_result.severity,
            description=validation_result.message,
            detected_at=time.time(),
            enforcement_applied=rule.enforcement_action if rule else None,
            metadata=validation_result.details,
        )

    def _map_rule_to_violation_type(self, rule: ValidationRule) -> ViolationType:
        """Map a rule definition to a specific :class:`ViolationType`."""
        rule_id = rule.rule_id.lower()
        if "deadline" in rule_id:
            return ViolationType.DEADLINE_MISSED
        if "quality" in rule_id:
            return ViolationType.QUALITY_BELOW_STANDARD
        if "resource" in rule_id:
            return ViolationType.RESOURCE_EXCEEDED
        if "dependency" in rule_id:
            return ViolationType.DEPENDENCY_UNMET
        return ViolationType.SCHEMA_VIOLATION
