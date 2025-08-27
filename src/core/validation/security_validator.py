"""Security Validator - Unified Validation Framework"""

from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from .security_rules import (
    SECURITY_PATTERNS,
    SENSITIVE_FIELDS,
    apply_default_rules,
)
from .security_logic import (
    validate_security_structure,
    validate_security_level,
    validate_authentication,
    validate_authorization,
    validate_encryption,
    check_sensitive_data_exposure,
    add_security_pattern as _add_security_pattern,
    add_sensitive_field as _add_sensitive_field,
)
from .security_reporting import (
    validate_security_policy_legacy as _validate_security_policy_legacy,
    get_security_policy_summary as _get_security_policy_summary,
)


class SecurityValidator(BaseValidator):
    """Validates security-related data and configurations."""

    def __init__(self) -> None:
        super().__init__("SecurityValidator")
        self.security_patterns = SECURITY_PATTERNS.copy()
        self.sensitive_fields = SENSITIVE_FIELDS.copy()

    def _setup_default_rules(self) -> None:  # pragma: no cover - rule setup
        apply_default_rules(self)

    def validate(self, security_data: Dict[str, Any], **kwargs) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        try:
            results.extend(validate_security_structure(self, security_data))

            required_fields = ["security_level", "authentication_method", "timestamp"]
            results.extend(self._validate_required_fields(security_data, required_fields))

            if "security_level" in security_data:
                level_result = validate_security_level(self, security_data["security_level"])
                if level_result:
                    results.append(level_result)

            if "authentication" in security_data:
                results.extend(
                    validate_authentication(self, security_data["authentication"])
                )

            if "authorization" in security_data:
                results.extend(
                    validate_authorization(self, security_data["authorization"])
                )

            if "encryption" in security_data:
                results.extend(validate_encryption(self, security_data["encryption"]))

            results.extend(check_sensitive_data_exposure(self, security_data))

            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_security_validation",
                    rule_name="Overall Security Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Security validation passed successfully",
                    details={"total_checks": len(results)},
                )
                results.append(success_result)
        except Exception as e:
            error_result = self._create_result(
                rule_id="security_validation_error",
                rule_name="Security Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Security validation error: {str(e)}",
                details={"error_type": type(e).__name__},
            )
            results.append(error_result)
        return results

    # Wrapper methods for logic helpers -------------------------------------
    def add_security_pattern(self, pattern_name: str, pattern: str) -> bool:
        return _add_security_pattern(self, pattern_name, pattern)

    def add_sensitive_field(self, field_name: str) -> bool:
        return _add_sensitive_field(self, field_name)

    # Reporting wrappers ----------------------------------------------------
    def validate_security_policy_legacy(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        return _validate_security_policy_legacy(self, policy)

    def get_security_policy_summary(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        return _get_security_policy_summary(self, policy)
