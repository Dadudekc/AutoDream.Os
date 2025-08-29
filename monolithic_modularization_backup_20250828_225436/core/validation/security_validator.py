from typing import Dict, List, Any, Optional
import re

        from datetime import datetime
from .base_validator import (

"""
Security Validator - Unified Validation Framework

This module provides security validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class SecurityValidator(BaseValidator):
    """Validates security-related data and configurations using unified validation framework"""

    def __init__(self):
        """Initialize security validator"""
        super().__init__("SecurityValidator")
        self.security_patterns = self._config.get("patterns", {})
        self.sensitive_fields = [
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

    def validate(
        self, security_data: Dict[str, Any], **kwargs
    ) -> List[ValidationResult]:
        """Validate security data and return validation results.

        Returns:
            List[ValidationResult]: Validation results produced during security
            validation.
        """
        results = []

        try:
            # Validate security data structure
            structure_results = self._validate_security_structure(security_data)
            results.extend(structure_results)

            # Validate required fields
            required_fields = ["security_level", "authentication_method", "timestamp"]
            field_results = self._validate_required_fields(
                security_data, required_fields
            )
            results.extend(field_results)

            # Validate security level if present
            if "security_level" in security_data:
                level_result = self._validate_security_level(
                    security_data["security_level"]
                )
                if level_result:
                    results.append(level_result)

            # Validate authentication if present
            if "authentication" in security_data:
                auth_results = self._validate_authentication(
                    security_data["authentication"]
                )
                results.extend(auth_results)

            # Validate authorization if present
            if "authorization" in security_data:
                authz_results = self._validate_authorization(
                    security_data["authorization"]
                )
                results.extend(authz_results)

            # Validate encryption if present
            if "encryption" in security_data:
                encryption_results = self._validate_encryption(
                    security_data["encryption"]
                )
                results.extend(encryption_results)

            # Check for sensitive data exposure
            exposure_results = self._check_sensitive_data_exposure(security_data)
            results.extend(exposure_results)

            # Add overall success result if no critical errors
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

    def _validate_security_structure(
        self, security_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate security data structure and format"""
        results = []

        if not isinstance(security_data, dict):
            result = self._create_result(
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
            result = self._create_result(
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

    def _validate_security_level(
        self, security_level: Any
    ) -> Optional[ValidationResult]:
        """Validate security level value"""
        valid_levels = ["low", "medium", "high", "critical"]

        if not isinstance(security_level, str):
            return self._create_result(
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
            return self._create_result(
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

    def _validate_authentication(self, authentication: Any) -> List[ValidationResult]:
        """Validate authentication data"""
        results = []

        if not isinstance(authentication, dict):
            result = self._create_result(
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

        # Validate authentication method
        if "method" in authentication:
            method = authentication["method"]
            valid_methods = [
                "password",
                "token",
                "oauth",
                "saml",
                "ldap",
                "mfa",
                "biometric",
            ]

            if not isinstance(method, str):
                result = self._create_result(
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
                result = self._create_result(
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

        # Validate credentials if present
        if "credentials" in authentication:
            creds = authentication["credentials"]
            cred_results = self._validate_credentials(creds)
            for cred_result in cred_results:
                cred_result.field_path = (
                    f"authentication.credentials.{cred_result.field_path}"
                )
            results.extend(cred_results)

        return results

    def _validate_credentials(self, credentials: Any) -> List[ValidationResult]:
        """Validate credential data"""
        results = []

        if not isinstance(credentials, dict):
            result = self._create_result(
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

        # Check for password strength if present
        if "password" in credentials:
            password = credentials["password"]
            if isinstance(password, str):
                strength_result = self._validate_password_strength(password)
                if strength_result:
                    strength_result.field_path = "password"
                    results.append(strength_result)

        # Check for API key format if present
        if "api_key" in credentials:
            api_key = credentials["api_key"]
            if isinstance(api_key, str):
                if not re.match(self.security_patterns["api_key"], api_key):
                    result = self._create_result(
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

    def _validate_password_strength(self, password: str) -> Optional[ValidationResult]:
        """Validate password strength"""
        if len(password) < 8:
            return self._create_result(
                rule_id="password_length",
                rule_name="Password Length Check",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Password must be at least 8 characters long",
                field_path="password",
                actual_value=len(password),
                expected_value=">= 8",
            )

        # Check for complexity requirements
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        if not (has_upper and has_lower and has_digit and has_special):
            return self._create_result(
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

    def _validate_authorization(self, authorization: Any) -> List[ValidationResult]:
        """Validate authorization data"""
        results = []

        if not isinstance(authorization, dict):
            result = self._create_result(
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

        # Validate roles if present
        if "roles" in authorization:
            roles = authorization["roles"]
            if isinstance(roles, list):
                if len(roles) == 0:
                    result = self._create_result(
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
                    # Validate each role
                    for i, role in enumerate(roles):
                        if not isinstance(role, str):
                            result = self._create_result(
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

        # Validate permissions if present
        if "permissions" in authorization:
            permissions = authorization["permissions"]
            if isinstance(permissions, list):
                if len(permissions) == 0:
                    result = self._create_result(
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

    def _validate_encryption(self, encryption: Any) -> List[ValidationResult]:
        """Validate encryption data"""
        results = []

        if not isinstance(encryption, dict):
            result = self._create_result(
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

        # Validate encryption algorithm if present
        if "algorithm" in encryption:
            algorithm = encryption["algorithm"]
            valid_algorithms = [
                "AES",
                "RSA",
                "ChaCha20",
                "Ed25519",
                "SHA-256",
                "SHA-512",
            ]

            if not isinstance(algorithm, str):
                result = self._create_result(
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
                result = self._create_result(
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

        # Validate key size if present
        if "key_size" in encryption:
            key_size = encryption["key_size"]
            if isinstance(key_size, int):
                if key_size < 128:
                    result = self._create_result(
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

    def _check_sensitive_data_exposure(self, data: Any) -> List[ValidationResult]:
        """Check for potential sensitive data exposure"""
        results = []

        if isinstance(data, dict):
            for key, value in data.items():
                # Check if field name suggests sensitive data
                key_lower = key.lower()
                if any(sensitive in key_lower for sensitive in self.sensitive_fields):
                    if isinstance(value, str) and len(value) > 0:
                        # Check if value looks like sensitive data
                        if self._looks_like_sensitive_data(value):
                            result = self._create_result(
                                rule_id="sensitive_data_exposure",
                                rule_name="Sensitive Data Exposure Check",
                                status=ValidationStatus.WARNING,
                                severity=ValidationSeverity.WARNING,
                                message=f"Potential sensitive data exposure in field '{key}'",
                                field_path=key,
                                actual_value="sensitive data detected",
                                expected_value="masked or encrypted value",
                            )
                            results.append(result)

                # Recursively check nested structures
                if isinstance(value, (dict, list)):
                    nested_results = self._check_sensitive_data_exposure(value)
                    for nested_result in nested_results:
                        nested_result.field_path = f"{key}.{nested_result.field_path}"
                    results.extend(nested_results)

        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    nested_results = self._check_sensitive_data_exposure(item)
                    for nested_result in nested_results:
                        nested_result.field_path = f"[{i}].{nested_result.field_path}"
                    results.extend(nested_results)

        return results

    def _looks_like_sensitive_data(self, value: str) -> bool:
        """Check if a string value looks like sensitive data"""
        # Check for common patterns
        if re.match(self.security_patterns["api_key"], value):
            return True
        if re.match(self.security_patterns["jwt_token"], value):
            return True
        if re.match(self.security_patterns["uuid"], value):
            return True
        if re.match(self.security_patterns["email"], value):
            return True

        # Check for long random-looking strings
        if len(value) > 20 and value.isalnum():
            return True

        return False

    def add_security_pattern(self, pattern_name: str, pattern: str) -> bool:
        """Add a custom security pattern"""
        try:
            self.security_patterns[pattern_name] = pattern
            self.logger.info(f"Security pattern added: {pattern_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add security pattern: {e}")
            return False

    def add_sensitive_field(self, field_name: str) -> bool:
        """Add a field name to the sensitive fields list"""
        try:
            if field_name not in self.sensitive_fields:
                self.sensitive_fields.append(field_name)
                self.logger.info(f"Sensitive field added: {field_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add sensitive field: {e}")
            return False

    # Security Policy Validation functionality integration (from duplicate policy_validator.py)
    def validate_security_policy_legacy(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy security policy validation method (from duplicate policy_validator.py)"""
        try:
            warnings: List[str] = []
            errors: List[str] = []
            compliance_score = 100.0

            # Validate password policy
            (
                password_score,
                pw_warnings,
                pw_errors,
            ) = self._validate_password_policy_legacy(policy)
            warnings.extend(pw_warnings)
            errors.extend(pw_errors)
            compliance_score -= (100 - password_score) * 0.3

            # Validate authentication policy
            (
                auth_score,
                auth_warnings,
                auth_errors,
            ) = self._validate_authentication_policy_legacy(policy)
            warnings.extend(auth_warnings)
            errors.extend(auth_errors)
            compliance_score -= (100 - auth_score) * 0.25

            # Validate session policy
            (
                sess_score,
                sess_warnings,
                sess_errors,
            ) = self._validate_session_policy_legacy(policy)
            warnings.extend(sess_warnings)
            errors.extend(sess_errors)
            compliance_score -= (100 - sess_score) * 0.2

            # Validate security controls
            (
                ctrl_score,
                ctrl_warnings,
                ctrl_errors,
            ) = self._validate_security_controls_legacy(policy)
            warnings.extend(ctrl_warnings)
            errors.extend(ctrl_errors)
            compliance_score -= (100 - ctrl_score) * 0.25

            recommendations = self._generate_recommendations_legacy(
                warnings, errors, compliance_score
            )
            is_valid = len(errors) == 0 and compliance_score >= 80.0

            return {
                "is_valid": is_valid,
                "warnings": warnings,
                "errors": errors,
                "compliance_score": max(0.0, compliance_score),
                "recommendations": recommendations,
            }

        except Exception as e:
            self.logger.error(f"Security policy validation failed: {e}")
            return {
                "is_valid": False,
                "warnings": [],
                "errors": [f"Validation error: {str(e)}"],
                "compliance_score": 0.0,
                "recommendations": ["Fix validation system errors"],
            }

    def _validate_password_policy_legacy(self, policy: Dict[str, Any]) -> tuple:
        """Validate password policy (from duplicate policy_validator.py)"""
        score = 100.0
        warnings: List[str] = []
        errors: List[str] = []

        min_length = policy.get("password_min_length", 0)
        if min_length < 8:
            errors.append("Password minimum length must be at least 8 characters")
            score -= 30
        elif min_length < 12:
            warnings.append(
                "Consider increasing password minimum length to 12+ characters"
            )
            score -= 10

        if not policy.get("require_special_chars", False):
            warnings.append("Consider requiring special characters in passwords")
            score -= 15
        if not policy.get("require_numbers", False):
            warnings.append("Consider requiring numbers in passwords")
            score -= 10
        if not policy.get("require_uppercase", False):
            warnings.append("Consider requiring uppercase letters in passwords")
            score -= 10

        expiry_days = policy.get("password_expiry_days", 0)
        if expiry_days == 0:
            warnings.append("Consider implementing password expiry policy")
            score -= 20
        elif expiry_days > 365:
            warnings.append("Password expiry period is very long")
            score -= 10

        return max(0.0, score), warnings, errors

    def _validate_authentication_policy_legacy(self, policy: Dict[str, Any]) -> tuple:
        """Validate authentication policy (from duplicate policy_validator.py)"""
        score = 100.0
        warnings: List[str] = []
        errors: List[str] = []

        max_attempts = policy.get("max_login_attempts", 0)
        if max_attempts <= 0:
            errors.append("Maximum login attempts must be greater than 0")
            score -= 40
        elif max_attempts > 5:
            warnings.append("Consider reducing maximum login attempts to 5 or fewer")
            score -= 20

        if not policy.get("mfa_required", False):
            warnings.append("Consider requiring multi-factor authentication")
            score -= 30

        return max(0.0, score), warnings, errors

    def _validate_session_policy_legacy(self, policy: Dict[str, Any]) -> tuple:
        """Validate session policy (from duplicate policy_validator.py)"""
        score = 100.0
        warnings: List[str] = []
        errors: List[str] = []

        session_timeout = policy.get("session_timeout", 0)
        if session_timeout <= 0:
            errors.append("Session timeout must be greater than 0")
            score -= 40
        elif session_timeout > 86400:
            warnings.append("Session timeout is very long, consider reducing")
            score -= 20

        return max(0.0, score), warnings, errors

    def _validate_security_controls_legacy(self, policy: Dict[str, Any]) -> tuple:
        """Validate security controls (from duplicate policy_validator.py)"""
        score = 100.0
        warnings: List[str] = []
        errors: List[str] = []

        if not policy.get("encryption_required", False):
            warnings.append("Consider requiring encryption for all communications")
            score -= 25
        if not policy.get("audit_logging_enabled", False):
            warnings.append("Audit logging should be enabled for compliance")
            score -= 30

        return max(0.0, score), warnings, errors

    def _generate_recommendations_legacy(
        self, warnings: List[str], errors: List[str], compliance_score: float
    ) -> List[str]:
        """Generate recommendations (from duplicate policy_validator.py)"""
        recommendations: List[str] = []
        for error in errors:
            recommendations.append(f"CRITICAL: {error}")
        for warning in warnings:
            recommendations.append(f"IMPROVE: {warning}")
        if compliance_score < 70:
            recommendations.extend(
                [
                    "Conduct comprehensive security review",
                    "Implement security awareness training",
                ]
            )
        elif compliance_score < 85:
            recommendations.extend(
                [
                    "Review and update security policies",
                    "Conduct security assessment",
                ]
            )
        else:
            recommendations.extend(
                [
                    "Maintain current security posture",
                    "Schedule regular security reviews",
                ]
            )
        return recommendations

    def get_security_policy_summary(self, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Get security policy validation summary"""
        try:
            # Use both validation methods
            unified_results = self.validate(policy)
            legacy_results = self.validate_security_policy_legacy(policy)

            return {
                "unified_validation": {
                    "total": len(unified_results),
                    "passed": len(
                        [r for r in unified_results if r.status.value == "passed"]
                    ),
                    "failed": len(
                        [r for r in unified_results if r.status.value == "failed"]
                    ),
                    "warnings": len(
                        [r for r in unified_results if r.severity.value == "warning"]
                    ),
                },
                "legacy_validation": legacy_results,
                "timestamp": self._get_current_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get security policy summary: {e}")
            return {"error": str(e)}

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""

        return datetime.now().isoformat()
