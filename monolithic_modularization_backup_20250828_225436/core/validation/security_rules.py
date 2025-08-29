"""Security rule definitions and constants."""

from .base_validator import ValidationRule, ValidationSeverity

# Common security-related patterns used across validators
SECURITY_PATTERNS = {
    "api_key": r"^[a-zA-Z0-9]{32,64}$",
    "jwt_token": r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$",
    "uuid": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "ip_address": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
}

# Fields that commonly contain sensitive data
SENSITIVE_FIELDS = [
    "password",
    "secret",
    "key",
    "token",
    "credential",
    "auth",
    "private",
    "sensitive",
    "confidential",
    "secure",
]

# Default validation rules applied by the SecurityValidator
DEFAULT_SECURITY_RULES = [
    ValidationRule(
        rule_id="security_structure",
        rule_name="Security Structure",
        rule_type="security",
        description="Validate security data structure and format",
        severity=ValidationSeverity.ERROR,
    ),
    ValidationRule(
        rule_id="authentication_validation",
        rule_name="Authentication Validation",
        rule_type="security",
        description="Validate authentication mechanisms and credentials",
        severity=ValidationSeverity.ERROR,
    ),
    ValidationRule(
        rule_id="authorization_check",
        rule_name="Authorization Check",
        rule_type="security",
        description="Validate authorization rules and permissions",
        severity=ValidationSeverity.ERROR,
    ),
    ValidationRule(
        rule_id="data_encryption_validation",
        rule_name="Data Encryption Validation",
        rule_type="security",
        description="Validate encryption methods and key management",
        severity=ValidationSeverity.WARNING,
    ),
]


def apply_default_rules(validator) -> None:
    """Register default security validation rules on the given validator."""
    for rule in DEFAULT_SECURITY_RULES:
        validator.add_validation_rule(rule)
