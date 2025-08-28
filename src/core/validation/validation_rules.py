"""Default rule definitions for onboarding validation."""

from typing import List

from .models import ValidationRule, ValidationSeverity


def get_default_onboarding_rules() -> List[ValidationRule]:
    """Return default onboarding validation rules."""
    return [
        ValidationRule(
            rule_id="onboarding_structure",
            rule_name="Onboarding Structure",
            rule_type="onboarding",
            description="Validate onboarding data structure and format",
            severity=ValidationSeverity.ERROR,
        ),
        ValidationRule(
            rule_id="onboarding_flow_validation",
            rule_name="Onboarding Flow Validation",
            rule_type="onboarding",
            description="Validate onboarding flow and progression",
            severity=ValidationSeverity.ERROR,
        ),
        ValidationRule(
            rule_id="verification_validation",
            rule_name="Verification Validation",
            rule_type="onboarding",
            description="Validate verification methods and status",
            severity=ValidationSeverity.ERROR,
        ),
        ValidationRule(
            rule_id="compliance_check",
            rule_name="Compliance Check",
            rule_type="onboarding",
            description="Check onboarding compliance requirements",
            severity=ValidationSeverity.WARNING,
        ),
    ]


__all__ = ["get_default_onboarding_rules"]
