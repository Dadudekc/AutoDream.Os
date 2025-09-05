#!/usr/bin/env python3
"""
Error Handling Package - V2 Compliant
=====================================

Unified error handling system with modular architecture.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant error handling package
"""

from .error_handling_orchestrator import (
    UnifiedErrorHandlingOrchestrator,
    get_error_handling_orchestrator
)
from .error_handling_models import (
    ErrorSeverity, ErrorCategory, ErrorContext,
    StandardErrorResponse, FileErrorResponse, NetworkErrorResponse,
    DatabaseErrorResponse, ValidationErrorResponse, ConfigurationErrorResponse,
    AgentErrorResponse, CoordinationErrorResponse, ErrorSummary,
    RetryConfiguration
)
from .retry_safety_engine import RetrySafetyEngine, retry_operation, safe_execute
from .specialized_handlers import SpecializedErrorHandlers, handle_operation_error
from .error_analysis_engine import ErrorAnalysisEngine

# Export main interfaces
__all__ = [
    'UnifiedErrorHandlingOrchestrator',
    'get_error_handling_orchestrator',
    'ErrorSeverity',
    'ErrorCategory', 
    'ErrorContext',
    'StandardErrorResponse',
    'FileErrorResponse',
    'NetworkErrorResponse', 
    'DatabaseErrorResponse',
    'ValidationErrorResponse',
    'ConfigurationErrorResponse',
    'AgentErrorResponse',
    'CoordinationErrorResponse',
    'ErrorSummary',
    'RetryConfiguration',
    'RetrySafetyEngine',
    'retry_operation',
    'safe_execute',
    'SpecializedErrorHandlers',
    'handle_operation_error',
    'ErrorAnalysisEngine'
]
