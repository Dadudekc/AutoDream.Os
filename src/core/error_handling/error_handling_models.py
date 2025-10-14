#!/usr/bin/env python3
"""
Error Handling Models - Refactored Facade
==========================================

Unified error handling models with modular architecture.
Refactored for V2 compliance (class count limit: ≤5 classes per file).

Architecture:
- error_response_models: Error response classes (10 classes)
- error_context_models: Context and summary models (2 classes)
- error_decision_models: Classifier, retry, decision engine (3 classes)
- This file: Facade for backward compatibility

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring (500 pts, ROI 33.33)
Original: V2 SWARM Error Handling Team
License: MIT
"""

# Import all models for backward compatibility
from .error_context_models import ErrorContext, ErrorSummary
from .error_decision_models import ErrorClassifier, ErrorDecisionEngine, RetryConfiguration
from .error_models_enums import ErrorCategory, ErrorRecoverability, ErrorSeverity
from .error_response_models import (
    AgentErrorResponse,
    BaseErrorResponse,
    ConfigurationErrorResponse,
    CoordinationErrorResponse,
    CriticalErrorResponse,
    DatabaseErrorResponse,
    FileErrorResponse,
    NetworkErrorResponse,
    RecoverableErrorResponse,
    ValidationErrorResponse,
)

# Backward compatibility exports
__all__ = [
    # Enums (from error_models_enums)
    "ErrorSeverity",
    "ErrorCategory",
    "ErrorRecoverability",
    # Context models (from error_context_models)
    "ErrorContext",
    "ErrorSummary",
    # Response models (from error_response_models)
    "BaseErrorResponse",
    "RecoverableErrorResponse",
    "FileErrorResponse",
    "NetworkErrorResponse",
    "DatabaseErrorResponse",
    "CriticalErrorResponse",
    "ValidationErrorResponse",
    "ConfigurationErrorResponse",
    "AgentErrorResponse",
    "CoordinationErrorResponse",
    # Decision models (from error_decision_models)
    "ErrorClassifier",
    "RetryConfiguration",
    "ErrorDecisionEngine",
]
