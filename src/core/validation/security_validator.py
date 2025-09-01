#!/usr/bin/env python3
"""
Security Validator Module - Agent Cellphone V2
============================================

Security compliance validation functionality.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from typing import Dict, Any, List

from .validation_models import ValidationIssue, ValidationSeverity


class SecurityValidator:
    """Handles security compliance validation."""

    def validate_security_compliance(self, security_data: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate security compliance requirements."""
        issues = []

        # Check authentication mechanisms
        if 'authentication' in security_data:
            auth_data = security_data['authentication']
            if not isinstance(auth_data, dict):
                issues.append(ValidationIssue(
                    rule_id="security_structure",
                    rule_name="Security Structure",
                    severity=ValidationSeverity.ERROR,
                    message="Authentication configuration must be a dictionary",
                    details={"authentication": auth_data},
                    timestamp=datetime.now(),
                    component="security_compliance"
                ))
            else:
                # Check for required auth fields
                if 'enabled' not in auth_data:
                    issues.append(ValidationIssue(
                        rule_id="authentication_validation",
                        rule_name="Authentication Validation",
                        severity=ValidationSeverity.WARNING,
                        message="Authentication enabled status not specified",
                        details={"authentication": auth_data},
                        timestamp=datetime.now(),
                        component="security_compliance"
                    ))

        return issues
