"""Security validation reporting helpers."""

from __future__ import annotations

from typing import Any, Dict, List


def _validate_password_policy(policy: Dict[str, Any]) -> tuple:
    score = 100.0
    warnings: List[str] = []
    errors: List[str] = []

    min_length = policy.get("password_min_length", 0)
    if min_length < 8:
        errors.append("Password minimum length must be at least 8 characters")
        score -= 30
    elif min_length < 12:
        warnings.append("Consider increasing password minimum length to 12+ characters")
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


def _validate_authentication_policy(policy: Dict[str, Any]) -> tuple:
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


def _validate_session_policy(policy: Dict[str, Any]) -> tuple:
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


def _validate_security_controls(policy: Dict[str, Any]) -> tuple:
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


def _generate_recommendations(warnings: List[str], errors: List[str], compliance_score: float) -> List[str]:
    recommendations: List[str] = []
    for error in errors:
        recommendations.append(f"CRITICAL: {error}")
    for warning in warnings:
        recommendations.append(f"IMPROVE: {warning}")
    if compliance_score < 70:
        recommendations.extend([
            "Conduct comprehensive security review",
            "Implement security awareness training",
        ])
    elif compliance_score < 85:
        recommendations.extend([
            "Review and update security policies",
            "Conduct security assessment",
        ])
    else:
        recommendations.extend([
            "Maintain current security posture",
            "Schedule regular security reviews",
        ])
    return recommendations


def validate_security_policy_legacy(validator, policy: Dict[str, Any]) -> Dict[str, Any]:
    try:
        warnings: List[str] = []
        errors: List[str] = []
        compliance_score = 100.0

        password_score, pw_warnings, pw_errors = _validate_password_policy(policy)
        warnings.extend(pw_warnings)
        errors.extend(pw_errors)
        compliance_score -= (100 - password_score) * 0.3

        auth_score, auth_warnings, auth_errors = _validate_authentication_policy(policy)
        warnings.extend(auth_warnings)
        errors.extend(auth_errors)
        compliance_score -= (100 - auth_score) * 0.25

        sess_score, sess_warnings, sess_errors = _validate_session_policy(policy)
        warnings.extend(sess_warnings)
        errors.extend(sess_errors)
        compliance_score -= (100 - sess_score) * 0.2

        ctrl_score, ctrl_warnings, ctrl_errors = _validate_security_controls(policy)
        warnings.extend(ctrl_warnings)
        errors.extend(ctrl_errors)
        compliance_score -= (100 - ctrl_score) * 0.25

        recommendations = _generate_recommendations(warnings, errors, compliance_score)
        is_valid = len(errors) == 0 and compliance_score >= 80.0

        return {
            "is_valid": is_valid,
            "warnings": warnings,
            "errors": errors,
            "compliance_score": max(0.0, compliance_score),
            "recommendations": recommendations,
        }
    except Exception as e:
        validator.logger.error(f"Security policy validation failed: {e}")
        return {
            "is_valid": False,
            "warnings": [],
            "errors": [f"Validation error: {str(e)}"],
            "compliance_score": 0.0,
            "recommendations": ["Fix validation system errors"],
        }


def get_security_policy_summary(validator, policy: Dict[str, Any]) -> Dict[str, Any]:
    try:
        unified_results = validator.validate(policy)
        legacy_results = validate_security_policy_legacy(validator, policy)
        return {
            "unified_validation": {
                "total": len(unified_results),
                "passed": len([r for r in unified_results if r.status.value == "passed"]),
                "failed": len([r for r in unified_results if r.status.value == "failed"]),
                "warnings": len([r for r in unified_results if r.severity.value == "warning"]),
            },
            "legacy_validation": legacy_results,
            "timestamp": get_current_timestamp(),
        }
    except Exception as e:
        validator.logger.error(f"Failed to get security policy summary: {e}")
        return {"error": str(e)}


def get_current_timestamp() -> str:
    from datetime import datetime

    return datetime.now().isoformat()
