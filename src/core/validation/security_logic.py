"""Security validation logic functions."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from .models import ValidationResult, ValidationSeverity, ValidationStatus


def validate_security_structure(validator, security_data: Dict[str, Any]) -> List[ValidationResult]:
    """Validate security data structure and format."""
    results: List[ValidationResult] = []

    if not isinstance(security_data, dict):
        result = validator._create_result(
            rule_id="security_type",
            rule_name="Security Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Security data must be a dictionary",
            actual_value=type(security_data).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if len(security_data) == 0:
        result = validator._create_result(
            rule_id="security_empty",
            rule_name="Security Empty Check",
            status=ValidationStatus.WARNING,
            severity=ValidationSeverity.WARNING,
            message="Security data is empty",
            actual_value=security_data,
            expected_value="non-empty security data",
        )
        results.append(result)

    return results


def validate_security_level(validator, security_level: Any) -> Optional[ValidationResult]:
    """Validate security level value."""
    valid_levels = ["low", "medium", "high", "critical"]

    if not isinstance(security_level, str):
        return validator._create_result(
            rule_id="security_level_type",
            rule_name="Security Level Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Security level must be a string",
            field_path="security_level",
            actual_value=type(security_level).__name__,
            expected_value="str",
        )

    if security_level.lower() not in valid_levels:
        return validator._create_result(
            rule_id="security_level_value",
            rule_name="Security Level Value Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message=f"Invalid security level: {security_level}",
            field_path="security_level",
            actual_value=security_level,
            expected_value=f"one of {valid_levels}",
        )

    return None


def validate_authentication(validator, authentication: Any) -> List[ValidationResult]:
    """Validate authentication data."""
    results: List[ValidationResult] = []

    if not isinstance(authentication, dict):
        result = validator._create_result(
            rule_id="authentication_type",
            rule_name="Authentication Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Authentication data must be a dictionary",
            field_path="authentication",
            actual_value=type(authentication).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "method" in authentication:
        method = authentication["method"]
        valid_methods = ["password", "token", "oauth", "saml", "ldap", "mfa", "biometric"]

        if not isinstance(method, str):
            result = validator._create_result(
                rule_id="auth_method_type",
                rule_name="Authentication Method Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Authentication method must be a string",
                field_path="authentication.method",
                actual_value=type(method).__name__,
                expected_value="str",
            )
            results.append(result)
        elif method.lower() not in valid_methods:
            result = validator._create_result(
                rule_id="auth_method_value",
                rule_name="Authentication Method Value Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid authentication method: {method}",
                field_path="authentication.method",
                actual_value=method,
                expected_value=f"one of {valid_methods}",
            )
            results.append(result)

    if "credentials" in authentication:
        creds = authentication["credentials"]
        cred_results = validate_credentials(validator, creds)
        for cred_result in cred_results:
            cred_result.field_path = f"authentication.credentials.{cred_result.field_path}"
        results.extend(cred_results)

    return results


def validate_credentials(validator, credentials: Any) -> List[ValidationResult]:
    """Validate credential data."""
    results: List[ValidationResult] = []

    if not isinstance(credentials, dict):
        result = validator._create_result(
            rule_id="credentials_type",
            rule_name="Credentials Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Credentials must be a dictionary",
            field_path="credentials",
            actual_value=type(credentials).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "password" in credentials:
        password = credentials["password"]
        if isinstance(password, str):
            strength_result = validate_password_strength(validator, password)
            if strength_result:
                strength_result.field_path = "password"
                results.append(strength_result)

    if "api_key" in credentials:
        api_key = credentials["api_key"]
        if isinstance(api_key, str):
            pattern = validator.security_patterns.get("api_key")
            if pattern and not re.match(pattern, api_key):
                result = validator._create_result(
                    rule_id="api_key_format",
                    rule_name="API Key Format Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Invalid API key format",
                    field_path="api_key",
                    actual_value=api_key,
                    expected_value="32-64 character alphanumeric string",
                )
                results.append(result)

    return results


def validate_password_strength(validator, password: str) -> Optional[ValidationResult]:
    """Validate password strength."""
    if len(password) < 8:
        return validator._create_result(
            rule_id="password_length",
            rule_name="Password Length Check",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Password must be at least 8 characters long",
            field_path="password",
            actual_value=len(password),
            expected_value=">= 8",
        )

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    if not (has_upper and has_lower and has_digit and has_special):
        return validator._create_result(
            rule_id="password_complexity",
            rule_name="Password Complexity Check",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Password must contain uppercase, lowercase, digit, and special character",
            field_path="password",
            actual_value="insufficient complexity",
            expected_value="mixed case, digits, and special characters",
        )

    return None


def validate_authorization(validator, authorization: Any) -> List[ValidationResult]:
    """Validate authorization data."""
    results: List[ValidationResult] = []

    if not isinstance(authorization, dict):
        result = validator._create_result(
            rule_id="authorization_type",
            rule_name="Authorization Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Authorization data must be a dictionary",
            field_path="authorization",
            actual_value=type(authorization).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "roles" in authorization:
        roles = authorization["roles"]
        if isinstance(roles, list):
            if len(roles) == 0:
                result = validator._create_result(
                    rule_id="roles_empty",
                    rule_name="Roles Empty Check",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message="No roles defined for authorization",
                    field_path="authorization.roles",
                    actual_value=roles,
                    expected_value="non-empty list of roles",
                )
                results.append(result)
            else:
                for i, role in enumerate(roles):
                    if not isinstance(role, str):
                        result = validator._create_result(
                            rule_id=f"role_{i}_type",
                            rule_name=f"Role {i} Type Validation",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Role {i} must be a string",
                            field_path=f"authorization.roles[{i}]",
                            actual_value=type(role).__name__,
                            expected_value="str",
                        )
                        results.append(result)

    if "permissions" in authorization:
        permissions = authorization["permissions"]
        if isinstance(permissions, list) and len(permissions) == 0:
            result = validator._create_result(
                rule_id="permissions_empty",
                rule_name="Permissions Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="No permissions defined for authorization",
                field_path="authorization.permissions",
                actual_value=permissions,
                expected_value="non-empty list of permissions",
            )
            results.append(result)

    return results


def validate_encryption(validator, encryption: Any) -> List[ValidationResult]:
    """Validate encryption data."""
    results: List[ValidationResult] = []

    if not isinstance(encryption, dict):
        result = validator._create_result(
            rule_id="encryption_type",
            rule_name="Encryption Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Encryption data must be a dictionary",
            field_path="encryption",
            actual_value=type(encryption).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "algorithm" in encryption:
        algorithm = encryption["algorithm"]
        valid_algorithms = ["AES", "RSA", "ChaCha20", "Ed25519", "SHA-256", "SHA-512"]

        if not isinstance(algorithm, str):
            result = validator._create_result(
                rule_id="encryption_algorithm_type",
                rule_name="Encryption Algorithm Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Encryption algorithm must be a string",
                field_path="encryption.algorithm",
                actual_value=type(algorithm).__name__,
                expected_value="str",
            )
            results.append(result)
        elif algorithm not in valid_algorithms:
            result = validator._create_result(
                rule_id="encryption_algorithm_value",
                rule_name="Encryption Algorithm Value Validation",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message=f"Unrecognized encryption algorithm: {algorithm}",
                field_path="encryption.algorithm",
                actual_value=algorithm,
                expected_value=f"one of {valid_algorithms}",
            )
            results.append(result)

    if "key_size" in encryption:
        key_size = encryption["key_size"]
        if isinstance(key_size, int) and key_size < 128:
            result = validator._create_result(
                rule_id="encryption_key_size",
                rule_name="Encryption Key Size Check",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Encryption key size too small: {key_size} bits",
                field_path="encryption.key_size",
                actual_value=f"{key_size} bits",
                expected_value=">= 128 bits",
            )
            results.append(result)

    return results


def check_sensitive_data_exposure(validator, data: Any) -> List[ValidationResult]:
    """Check for potential sensitive data exposure."""
    results: List[ValidationResult] = []

    if isinstance(data, dict):
        for key, value in data.items():
            if any(field in key.lower() for field in validator.sensitive_fields):
                if isinstance(value, str) and looks_like_sensitive_data(validator, value):
                    result = validator._create_result(
                        rule_id="sensitive_data_exposure",
                        rule_name="Sensitive Data Exposure",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Potential sensitive data exposure in field '{key}'",
                        field_path=key,
                        actual_value="<hidden>",
                        expected_value="redacted or secure storage",
                    )
                    results.append(result)
            if isinstance(value, (dict, list)):
                nested_results = check_sensitive_data_exposure(validator, value)
                for nr in nested_results:
                    nr.field_path = f"{key}.{nr.field_path}" if nr.field_path else key
                results.extend(nested_results)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            nested_results = check_sensitive_data_exposure(validator, item)
            for nr in nested_results:
                nr.field_path = f"[{i}].{nr.field_path}" if nr.field_path else f"[{i}]"
            results.extend(nested_results)

    return results


def looks_like_sensitive_data(validator, value: str) -> bool:
    """Check if a string value looks like sensitive data."""
    patterns = validator.security_patterns
    if re.match(patterns["api_key"], value):
        return True
    if re.match(patterns["jwt_token"], value):
        return True
    if re.match(patterns["uuid"], value):
        return True
    if re.match(patterns["email"], value):
        return True
    if len(value) > 20 and value.isalnum():
        return True
    return False


def add_security_pattern(validator, pattern_name: str, pattern: str) -> bool:
    """Add a custom security pattern."""
    try:
        validator.security_patterns[pattern_name] = pattern
        validator.logger.info(f"Security pattern added: {pattern_name}")
        return True
    except Exception as e:
        validator.logger.error(f"Failed to add security pattern: {e}")
        return False


def add_sensitive_field(validator, field_name: str) -> bool:
    """Add a field name to the sensitive fields list."""
    try:
        if field_name not in validator.sensitive_fields:
            validator.sensitive_fields.append(field_name)
            validator.logger.info(f"Sensitive field added: {field_name}")
        return True
    except Exception as e:
        validator.logger.error(f"Failed to add sensitive field: {e}")
        return False
