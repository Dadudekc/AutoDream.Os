"""Security validation reporting helpers."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def validate_security_policy_legacy(validator, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Perform a very small set of legacy security policy checks."""
    warnings: List[str] = []
    errors: List[str] = []
    score = 100.0

    min_length = policy.get("password_min_length", 0)
    if min_length < 8:
        errors.append("Password minimum length must be at least 8 characters")
        score -= 30
    if not policy.get("mfa_required", False):
        warnings.append("Consider requiring multi-factor authentication")
        score -= 20

    return {
        "is_valid": not errors,
        "warnings": warnings,
        "errors": errors,
        "compliance_score": max(0.0, score),
        "recommendations": warnings + errors,
    }


def get_security_policy_summary(validator, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Combine validator results with legacy policy validation."""
    results = validator.validate(policy)
    legacy = validate_security_policy_legacy(validator, policy)
    return {
        "unified_validation": {
            "total": len(results),
            "passed": len([r for r in results if r.status.value == "passed"]),
            "failed": len([r for r in results if r.status.value == "failed"]),
            "warnings": len([r for r in results if r.severity.value == "warning"]),
        },
        "legacy_validation": legacy,
        "timestamp": datetime.now().isoformat(),
    }
