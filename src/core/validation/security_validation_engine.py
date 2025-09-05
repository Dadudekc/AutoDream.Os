#!/usr/bin/env python3
"""
Security Validation Engine
==========================

Security validation engine for the unified validation system.
Handles security validation for authentication and authorization.
V2 COMPLIANT: Focused security validation under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR SECURITY VALIDATION
@license MIT
"""

import logging
from typing import List, Dict, Any, Optional

from .models.validation_models import (
    ValidationResult, ValidationSeverity, ValidationIssue
)


class SecurityValidationEngine:
    """Security validation engine for authentication and authorization"""
    
    def __init__(self):
        """Initialize security validation engine"""
        self.logger = logging.getLogger(__name__)
        self.pattern = ValidationPatterns.get_pattern("security")
    
    def validate_security(self, security_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate security data."""
        issues = []
        
        try:
            # Check required fields
            for field in self.pattern.required_fields:
                if field not in security_data:
                    issues.append(create_validation_issue(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field
                    ))
            
            # Validate attempts
            if "attempts" in security_data:
                attempt_issues = self._validate_attempts(security_data["attempts"])
                issues.extend(attempt_issues)
            
            # Validate timeout
            if "timeout" in security_data:
                timeout_issues = self._validate_timeout(security_data["timeout"])
                issues.extend(timeout_issues)
            
            # Validate permissions
            if "permissions" in security_data:
                perm_issues = self._validate_permissions(security_data["permissions"])
                issues.extend(perm_issues)
            
            # Log validation results
            if issues:
                self.logger.warning(f"Security validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Security validation passed")
                
        except Exception as e:
            issues.append(create_validation_issue(
                message=f"Security validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="security_data",
                value=security_data
            ))
        
        return issues
    
    def _validate_attempts(self, attempts: int) -> List[ValidationResult]:
        """Validate attempt count."""
        issues = []
        max_attempts = self.pattern.constraints["max_attempts"]
        
        if not isinstance(attempts, int):
            issues.append(create_validation_issue(
                message="Attempts must be an integer",
                severity=ValidationSeverity.ERROR,
                field="attempts",
                value=attempts
            ))
            return issues
        
        if attempts < 0:
            issues.append(create_validation_issue(
                message="Attempts cannot be negative",
                severity=ValidationSeverity.ERROR,
                field="attempts",
                value=attempts
            ))
        
        if attempts > max_attempts:
            issues.append(create_validation_issue(
                message=f"Attempts {attempts} exceeds maximum {max_attempts}",
                severity=ValidationSeverity.WARNING,
                field="attempts",
                value=attempts,
                suggestion="Consider implementing rate limiting"
            ))
        
        return issues
    
    def _validate_timeout(self, timeout: float) -> List[ValidationResult]:
        """Validate timeout value."""
        issues = []
        max_timeout = self.pattern.constraints["timeout_seconds"]
        
        if not isinstance(timeout, (int, float)):
            issues.append(create_validation_issue(
                message="Timeout must be a number",
                severity=ValidationSeverity.ERROR,
                field="timeout",
                value=timeout
            ))
            return issues
        
        if timeout < 0:
            issues.append(create_validation_issue(
                message="Timeout cannot be negative",
                severity=ValidationSeverity.ERROR,
                field="timeout",
                value=timeout
            ))
        
        if timeout > max_timeout:
            issues.append(create_validation_issue(
                message=f"Timeout {timeout}s exceeds maximum {max_timeout}s",
                severity=ValidationSeverity.WARNING,
                field="timeout",
                value=timeout,
                suggestion=f"Consider reducing to {max_timeout} seconds or less"
            ))
        
        return issues
    
    def _validate_permissions(self, permissions: List[str]) -> List[ValidationResult]:
        """Validate permissions list."""
        issues = []
        
        if not isinstance(permissions, list):
            issues.append(create_validation_issue(
                message="Permissions must be a list",
                severity=ValidationSeverity.ERROR,
                field="permissions",
                value=permissions
            ))
            return issues
        
        if not permissions:
            issues.append(create_validation_issue(
                message="Permissions list cannot be empty",
                severity=ValidationSeverity.WARNING,
                field="permissions",
                suggestion="Add at least one permission"
            ))
        
        valid_permissions = ["read", "write", "execute", "admin", "user"]
        for perm in permissions:
            if perm not in valid_permissions:
                issues.append(create_validation_issue(
                    message=f"Invalid permission: {perm}",
                    severity=ValidationSeverity.WARNING,
                    field="permissions",
                    value=perm,
                    suggestion=f"Use one of: {', '.join(valid_permissions)}"
                ))
        
        return issues
    
    def get_security_validation_result(self, security_data: Dict[str, Any]) -> ValidationResult:
        """Get comprehensive validation result for security data."""
        issues = self.validate_security(security_data)
        is_valid = len(issues) == 0 or not any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for issue in issues)
        
        return create_validation_result(
            is_valid=is_valid,
            issues=issues,
            validated_data=security_data,
            validation_type="security"
        )


# Factory function for dependency injection
def create_security_validation_engine() -> SecurityValidationEngine:
    """Factory function to create security validation engine"""
    return SecurityValidationEngine()


# Export for DI
__all__ = ['SecurityValidationEngine', 'create_security_validation_engine']
