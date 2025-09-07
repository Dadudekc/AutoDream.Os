"""Minimal security validator orchestrating rules, scanners and reporting."""

from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from .security_rules import SENSITIVE_FIELDS, apply_default_rules
from .scanners import scan_sensitive_fields
from . import security_reporting


class SecurityValidator(BaseValidator):
    """Orchestrates security validation using rules, scanners and reporting."""

    def __init__(self) -> None:
        super().__init__("SecurityValidator")
        apply_default_rules(self)

    # --- Orchestration -------------------------------------------------
    def validate(self, security_data: Dict[str, Any], **kwargs: Any) -> List[ValidationResult]:
        """Validate security data and return results."""
        results: List[ValidationResult] = []

        exposures = scan_sensitive_fields(security_data, SENSITIVE_FIELDS)
        for field in exposures:
            results.append(
                self._create_result(
                    rule_id="sensitive_data_exposure",
                    rule_name="Sensitive Data Exposure",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Sensitive field '{field}' may be exposed",
                    field_path=field,
                )
            )

        if not results:
            results.append(
                self._create_result(
                    rule_id="overall_security_validation",
                    rule_name="Overall Security Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Security validation passed successfully",
                )
            )

        return results

    # --- Reporting wrappers -------------------------------------------
    def validate_security_policy_legacy(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to legacy policy validation helper."""
        return security_reporting.validate_security_policy_legacy(self, policy)

    def get_security_policy_summary(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Generate combined summary of security policy validation."""
        return security_reporting.get_security_policy_summary(self, policy)
