#!/usr/bin/env python3
"""Minimal security policy validator used in tests."""

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class SecurityPolicy:
    password_min_length: int = 8


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]


class SecurityPolicyValidator:
    """Validate basic security policy settings."""

    def __init__(self, config_file: str | None = None) -> None:
        self.config_file = config_file
        self.default_policy = SecurityPolicy()

    def validate_policy(self, policy: Dict) -> ValidationResult:
        errors: List[str] = []
        if (
            policy.get("password_min_length", self.default_policy.password_min_length)
            < 8
        ):
            errors.append("Password minimum length must be at least 8 characters")
        return ValidationResult(is_valid=not errors, errors=errors)


__all__ = ["SecurityPolicy", "ValidationResult", "SecurityPolicyValidator"]
