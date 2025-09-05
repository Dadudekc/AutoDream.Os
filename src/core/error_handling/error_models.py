#!/usr/bin/env python3
"""
Error Models - V2 Compliance Error Handling Data Models (V2 Refactored)
=======================================================================

V2 Refactored data models and enums for error handling system with V2 compliance standards.

V2 COMPLIANCE: Type-safe error models with validation and configuration
DESIGN PATTERN: Builder pattern for error context creation
DEPENDENCY INJECTION: Configuration-driven error handling parameters

Author: Agent-2 (Architecture & Design Specialist)
Mission: V2 Compliance Architecture & Design Optimization
Status: V2 COMPLIANT - Error Models Refactored Optimized
"""

# V2 Refactored - Backward Compatibility Wrapper
from .error_models_refactored import *

# Maintain backward compatibility
__all__ = [
    # Enums
    'ErrorSeverity', 'CircuitState', 'ErrorType', 'RetryStrategy',
    # Core Models
    'ErrorContext', 'CircuitBreakerConfig', 'RetryConfig',
    # Metrics Models
    'ErrorMetrics', 'ErrorReport', 'ErrorAlert',
    # Functions
    'create_error_context', 'validate_error_configurations'
]