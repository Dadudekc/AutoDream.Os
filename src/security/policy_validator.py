#!/usr/bin/env python3
"""Security policy validation and compliance checking."""

from dataclasses import dataclass
from typing import Dict, List
import logging
import os
import yaml


@dataclass
class SecurityPolicy:
    """Security policy configuration."""

    password_min_length: int
    require_special_chars: bool
    require_numbers: bool
    require_uppercase: bool
    max_login_attempts: int
    session_timeout: int
    password_expiry_days: int
    mfa_required: bool
    encryption_required: bool
    audit_logging_enabled: bool


@dataclass
class ValidationResult:
    """Policy validation result."""

    is_valid: bool
    warnings: List[str]
    errors: List[str]
    compliance_score: float
    recommendations: List[str]


class SecurityPolicyValidator:
    """Validate security policy configurations."""

    def __init__(self, config_file: str = "security_policy.yaml") -> None:
        self.logger = logging.getLogger(__name__)
        self.config_file = config_file
        self.default_policy = SecurityPolicy(
            password_min_length=12,
            require_special_chars=True,
            require_numbers=True,
            require_uppercase=True,
            max_login_attempts=3,
            session_timeout=3600,
            password_expiry_days=90,
            mfa_required=True,
            encryption_required=True,
            audit_logging_enabled=True,
        )
        self.policy = self._load_policy()

    def validate_policy(self, policy: Dict) -> ValidationResult:
        """Validate security policy configuration."""
        try:
            warnings: List[str] = []
            errors: List[str] = []
            compliance_score = 100.0

            password_score, pw_warnings, pw_errors = self._validate_password_policy(
                policy
            )
            warnings.extend(pw_warnings)
            errors.extend(pw_errors)
            compliance_score -= (100 - password_score) * 0.3

            (
                auth_score,
                auth_warnings,
                auth_errors,
            ) = self._validate_authentication_policy(policy)
            warnings.extend(auth_warnings)
            errors.extend(auth_errors)
            compliance_score -= (100 - auth_score) * 0.25

            sess_score, sess_warnings, sess_errors = self._validate_session_policy(
                policy
            )
            warnings.extend(sess_warnings)
            errors.extend(sess_errors)
            compliance_score -= (100 - sess_score) * 0.2

            ctrl_score, ctrl_warnings, ctrl_errors = self._validate_security_controls(
                policy
            )
            warnings.extend(ctrl_warnings)
            errors.extend(ctrl_errors)
            compliance_score -= (100 - ctrl_score) * 0.25

            recommendations = self._generate_recommendations(
                warnings, errors, compliance_score
            )
            is_valid = len(errors) == 0 and compliance_score >= 80.0

            return ValidationResult(
                is_valid=is_valid,
                warnings=warnings,
                errors=errors,
                compliance_score=max(0.0, compliance_score),
                recommendations=recommendations,
            )
        except Exception as exc:  # pragma: no cover - defensive programming
            self.logger.error("Policy validation failed: %s", exc)
            return ValidationResult(
                is_valid=False,
                warnings=[],
                errors=[f"Validation error: {exc}"],
                compliance_score=0.0,
                recommendations=["Fix validation system errors"],
            )

    def _validate_password_policy(self, policy: Dict) -> tuple:
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

    def _validate_authentication_policy(self, policy: Dict) -> tuple:
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

    def _validate_session_policy(self, policy: Dict) -> tuple:
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

    def _validate_security_controls(self, policy: Dict) -> tuple:
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

    def _generate_recommendations(
        self, warnings: List[str], errors: List[str], compliance_score: float
    ) -> List[str]:
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

    def _load_policy(self) -> SecurityPolicy:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as fh:
                    config = yaml.safe_load(fh) or {}
                policy = SecurityPolicy(
                    password_min_length=config.get(
                        "password_min_length", self.default_policy.password_min_length
                    ),
                    require_special_chars=config.get(
                        "require_special_chars",
                        self.default_policy.require_special_chars,
                    ),
                    require_numbers=config.get(
                        "require_numbers", self.default_policy.require_numbers
                    ),
                    require_uppercase=config.get(
                        "require_uppercase", self.default_policy.require_uppercase
                    ),
                    max_login_attempts=config.get(
                        "max_login_attempts", self.default_policy.max_login_attempts
                    ),
                    session_timeout=config.get(
                        "session_timeout", self.default_policy.session_timeout
                    ),
                    password_expiry_days=config.get(
                        "password_expiry_days", self.default_policy.password_expiry_days
                    ),
                    mfa_required=config.get(
                        "mfa_required", self.default_policy.mfa_required
                    ),
                    encryption_required=config.get(
                        "encryption_required", self.default_policy.encryption_required
                    ),
                    audit_logging_enabled=config.get(
                        "audit_logging_enabled",
                        self.default_policy.audit_logging_enabled,
                    ),
                )
                self.logger.info("Security policy loaded from %s", self.config_file)
                return policy
            self.logger.warning(
                "Policy file %s not found, using defaults", self.config_file
            )
            return self.default_policy
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to load security policy: %s", exc)
            return self.default_policy

    def save_policy(self, policy: SecurityPolicy, filename: str | None = None) -> None:
        try:
            filename = filename or self.config_file
            config = {
                "password_min_length": policy.password_min_length,
                "require_special_chars": policy.require_special_chars,
                "require_numbers": policy.require_numbers,
                "require_uppercase": policy.require_uppercase,
                "max_login_attempts": policy.max_login_attempts,
                "session_timeout": policy.session_timeout,
                "password_expiry_days": policy.password_expiry_days,
                "mfa_required": policy.mfa_required,
                "encryption_required": policy.encryption_required,
                "audit_logging_enabled": policy.audit_logging_enabled,
            }
            with open(filename, "w") as fh:
                yaml.dump(config, fh, default_flow_style=False)
            self.logger.info("Security policy saved to %s", filename)
        except Exception as exc:  # pragma: no cover - defensive
            self.logger.error("Failed to save security policy: %s", exc)
