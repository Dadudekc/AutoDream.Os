#!/usr/bin/env python3
"""
Vector Database Security Validator - V2 Compliance
==================================================

Comprehensive security validation for vector database integration.
Refactored into modular components for V2 compliance.

Author: Agent-2 (Security Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive security validation
"""

from .security_validator_checks import SecurityChecks

# Import all components from refactored modules
from .security_validator_core import VectorDatabaseSecurityCore
from .security_validator_main import (
    VectorDatabaseSecurityValidator,
    generate_security_report,
    validate_vector_database_security,
)

# Re-export main classes for backward compatibility
__all__ = [
    # Core classes
    "VectorDatabaseSecurityCore",
    "SecurityChecks",
    # Main validator
    "VectorDatabaseSecurityValidator",
    # Convenience functions
    "validate_vector_database_security",
    "generate_security_report",
]


# For backward compatibility, create a default instance
_default_validator = None


def get_default_validator() -> VectorDatabaseSecurityValidator:
    """Get default security validator instance."""
    global _default_validator
    if _default_validator is None:
        _default_validator = VectorDatabaseSecurityValidator()
    return _default_validator


# Convenience functions for backward compatibility
def validate_security() -> dict:
    """Validate security using default validator."""
    return get_default_validator().validate_security()


def get_security_score() -> float:
    """Get security score using default validator."""
    return get_default_validator().get_security_score()


def get_vulnerabilities() -> list:
    """Get vulnerabilities using default validator."""
    return get_default_validator().get_vulnerabilities()
