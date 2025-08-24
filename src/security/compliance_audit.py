#!/usr/bin/env python3
"""Compatibility layer for compliance and audit components.

This module preserves the original import paths while delegating to the
newly partitioned modules that provide audit logging, security policy
validation, and compliance reporting.
"""

from .policy_validator import SecurityPolicy, ValidationResult, SecurityPolicyValidator
from .audit_logger import AuditEvent, AuditLogger
from .compliance_reporter import ComplianceReport, ComplianceReporter

__all__ = [
    "SecurityPolicyValidator",
    "AuditLogger",
    "ComplianceReporter",
    "SecurityPolicy",
    "ValidationResult",
    "AuditEvent",
    "ComplianceReport",
]
