#!/usr/bin/env python3
"""
Error Handling Orchestrator - V2 Compliant
==========================================

Main orchestrator for unified error handling system.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant error handling orchestration
"""

import logging
from collections.abc import Callable
from typing import Any

from .error_analysis_engine import ErrorAnalysisEngine
from .error_handling_models import RetryConfiguration
from .retry_safety_engine import RetrySafetyEngine
from .specialized_handlers import SpecializedErrorHandlers


class UnifiedErrorHandlingOrchestrator:
    """
    Unified Error Handling Orchestrator - V2 Compliant

    Orchestrates all error handling functionality:
    - Retry operations and safety mechanisms
    - Specialized error handlers for different contexts
    - Error analysis and severity assessment
    - Recovery recommendations and system health monitoring
    """

    def __init__(self, logger: logging.Logger | None = None):
        """Initialize error handling orchestrator."""
        self.logger = logger
        self.retry_engine = RetrySafetyEngine(logger)
        self.handlers = SpecializedErrorHandlers(logger)
        self.analysis_engine = ErrorAnalysisEngine()

    # Retry and Safety Operations
    def retry_operation(
        self,
        operation_func: Callable,
        max_retries: int = 3,
        delay: float = 1.0,
        backoff_factor: float = 2.0,
        exceptions: tuple = (Exception,),
        logger: logging.Logger | None = None,
    ) -> Any:
        """Retry operation with exponential backoff."""
        config = RetryConfiguration(max_retries, delay, backoff_factor, exceptions)
        return self.retry_engine.retry_operation(operation_func, config, logger)

    def safe_execute(
        self,
        operation_func: Callable,
        default_return: Any = None,
        logger: logging.Logger | None = None,
        operation_name: str = "operation",
    ) -> Any:
        """Safely execute operation with fallback return value."""
        return self.retry_engine.safe_execute(
            operation_func, default_return, logger, operation_name
        )

    def validate_and_execute(
        self,
        operation_func: Callable,
        validation_func: Callable,
        error_message: str = "Validation failed",
        logger: logging.Logger | None = None,
    ) -> Any:
        """Validate input and execute operation."""
        return self.retry_engine.validate_and_execute(
            operation_func, validation_func, error_message, logger
        )

    # Specialized Error Handlers
    def handle_operation_error(
        self,
        logger: logging.Logger,
        operation: str,
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle operation error with standardized response."""
        return self.handlers.handle_operation_error(logger, operation, error, context)

    def handle_file_operation_error(
        self,
        logger: logging.Logger,
        operation: str,
        file_path: str,
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle file operation error with standardized response."""
        return self.handlers.handle_file_operation_error(
            logger, operation, file_path, error, context
        )

    def handle_network_operation_error(
        self,
        logger: logging.Logger,
        operation: str,
        url: str,
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle network operation error with standardized response."""
        return self.handlers.handle_network_operation_error(logger, operation, url, error, context)

    def handle_database_operation_error(
        self,
        logger: logging.Logger,
        operation: str,
        table: str,
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle database operation error with standardized response."""
        return self.handlers.handle_database_operation_error(
            logger, operation, table, error, context
        )

    def handle_validation_error(
        self,
        logger: logging.Logger,
        validation_type: str,
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle validation error with standardized response."""
        return self.handlers.handle_validation_error(logger, validation_type, error, context)

    def handle_configuration_error(
        self,
        logger: logging.Logger,
        config_key: str,
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle configuration error with standardized response."""
        return self.handlers.handle_configuration_error(logger, config_key, error, context)

    def handle_agent_operation_error(
        self,
        logger: logging.Logger,
        agent_id: str,
        operation: str,
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle agent operation error with standardized response."""
        return self.handlers.handle_agent_operation_error(
            logger, agent_id, operation, error, context
        )

    def handle_coordination_error(
        self,
        logger: logging.Logger,
        coordination_type: str,
        participants: list[str],
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle coordination error with standardized response."""
        return self.handlers.handle_coordination_error(
            logger, coordination_type, participants, error, context
        )

    # Error Analysis and Assessment
    def create_error_summary(self, errors: list[dict[str, Any]]) -> dict[str, Any]:
        """Create error summary from list of errors."""
        return self.analysis_engine.create_error_summary(errors)

    def is_recoverable_error(self, error: Exception) -> bool:
        """Check if error is recoverable."""
        return self.analysis_engine.is_recoverable_error(error)

    def get_error_severity(self, error: Exception) -> str:
        """Get error severity level."""
        return self.analysis_engine.get_error_severity(error)

    def analyze_error_patterns(self, errors: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze error patterns from error list."""
        return self.analysis_engine.analyze_error_patterns(errors)

    def get_recovery_recommendations(
        self, error: Exception, context: dict[str, Any] = None
    ) -> list[str]:
        """Get recovery recommendations for specific error."""
        return self.analysis_engine.get_recovery_recommendations(error, context)

    def assess_system_health(self, errors: list[dict[str, Any]]) -> dict[str, Any]:
        """Assess overall system health based on error patterns."""
        return self.analysis_engine.assess_system_health(errors)


# Global orchestrator instance
_orchestrator = None


def get_error_handling_orchestrator(
    logger: logging.Logger | None = None,
) -> UnifiedErrorHandlingOrchestrator:
    """Get global error handling orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = UnifiedErrorHandlingOrchestrator(logger)
    return _orchestrator
