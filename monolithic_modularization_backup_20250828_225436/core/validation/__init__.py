#!/usr/bin/env python3
"""
Validation System - Unified Validation Framework
===============================================

Unified validation framework following V2 standards.
Provides validation capabilities for all system components.

Author: Agent-8 (Integration Enhancement Manager)
License: MIT
"""

# Core validation components
from .base_validator import BaseValidator
from .validation_result import ValidationResult, ValidationSeverity, ValidationStatus

# Export main classes
__all__ = [
    "BaseValidator",
    "ValidationResult",
    "ValidationSeverity", 
    "ValidationStatus"
]
