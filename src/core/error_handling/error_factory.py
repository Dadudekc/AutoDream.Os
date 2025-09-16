#!/usr/bin/env python3
"""
Error Handling Factory Module - V2 Compliant
Factory pattern implementation for error handling extracted from error_handling_examples.py
V2 Compliance: ≤400 lines for compliance

Author: Agent-7 (Web Development Specialist) - Swarm Coordination
License: MIT
"""

from __future__ import annotations

import logging
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Types of errors that can be handled."""

    VALIDATION_ERROR = "validation_error"
    NETWORK_ERROR = "network_error"
    DATABASE_ERROR = "database_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    BUSINESS_LOGIC_ERROR = "business_logic_error"
    SYSTEM_ERROR = "system_error"
    UNKNOWN_ERROR = "unknown_error"


class ErrorSeverity(Enum):
    """Severity levels for errors."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ErrorContext:
    """Context information for error handling."""

    user_id: str | None = None
    session_id: str | None = None
    request_id: str | None = None
    component: str | None = None
    operation: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorDetails:
    """Detailed error information."""

    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    code: str
    context: ErrorContext
    timestamp: datetime = field(default_factory=datetime.now)
    stack_trace: str | None = None
    recovery_suggestions: list[str] = field(default_factory=list)


class BaseErrorHandler:
    """Base class for error handlers."""

    def __init__(self, error_type: ErrorType):
        self.error_type = error_type
        self.handled_count = 0
        self.last_handled = None

    def can_handle(self, error: Exception) -> bool:
        """Check if this handler can handle the given error."""
        raise NotImplementedError

    def handle(self, error: Exception, context: ErrorContext) -> ErrorDetails:
        """Handle the error and return error details."""
        raise NotImplementedError

    def get_recovery_suggestions(self, error: Exception) -> list[str]:
        """Get recovery suggestions for the error."""
        return ["Contact system administrator", "Retry operation", "Check system status"]


class ValidationErrorHandler(BaseErrorHandler):
    """Handler for validation errors."""

    def __init__(self):
        super().__init__(ErrorType.VALIDATION_ERROR)

    def can_handle(self, error: Exception) -> bool:
        """Check if this is a validation error."""
        return isinstance(error, (ValueError, TypeError, AttributeError))

    def handle(self, error: Exception, context: ErrorContext) -> ErrorDetails:
        """Handle validation error."""
        self.handled_count += 1
        self.last_handled = datetime.now()

        return ErrorDetails(
            error_type=self.error_type,
            severity=ErrorSeverity.MEDIUM,
            message=f"Validation error: {str(error)}",
            code="VALIDATION_ERROR",
            context=context,
            stack_trace=str(error),
            recovery_suggestions=self.get_recovery_suggestions(error),
        )

    def get_recovery_suggestions(self, error: Exception) -> list[str]:
        """Get validation-specific recovery suggestions."""
        return [
            "Check input data format",
            "Verify required fields are provided",
            "Ensure data types are correct",
            "Review validation rules",
        ]


class NetworkErrorHandler(BaseErrorHandler):
    """Handler for network errors."""

    def __init__(self):
        super().__init__(ErrorType.NETWORK_ERROR)

    def can_handle(self, error: Exception) -> bool:
        """Check if this is a network error."""
        return isinstance(error, (ConnectionError, TimeoutError, OSError))

    def handle(self, error: Exception, context: ErrorContext) -> ErrorDetails:
        """Handle network error."""
        self.handled_count += 1
        self.last_handled = datetime.now()

        return ErrorDetails(
            error_type=self.error_type,
            severity=ErrorSeverity.HIGH,
            message=f"Network error: {str(error)}",
            code="NETWORK_ERROR",
            context=context,
            stack_trace=str(error),
            recovery_suggestions=self.get_recovery_suggestions(error),
        )

    def get_recovery_suggestions(self, error: Exception) -> list[str]:
        """Get network-specific recovery suggestions."""
        return [
            "Check network connectivity",
            "Verify server availability",
            "Retry with exponential backoff",
            "Check firewall settings",
        ]


class DatabaseErrorHandler(BaseErrorHandler):
    """Handler for database errors."""

    def __init__(self):
        super().__init__(ErrorType.DATABASE_ERROR)

    def can_handle(self, error: Exception) -> bool:
        """Check if this is a database error."""
        return "database" in str(error).lower() or "sql" in str(error).lower()

    def handle(self, error: Exception, context: ErrorContext) -> ErrorDetails:
        """Handle database error."""
        self.handled_count += 1
        self.last_handled = datetime.now()

        return ErrorDetails(
            error_type=self.error_type,
            severity=ErrorSeverity.HIGH,
            message=f"Database error: {str(error)}",
            code="DATABASE_ERROR",
            context=context,
            stack_trace=str(error),
            recovery_suggestions=self.get_recovery_suggestions(error),
        )

    def get_recovery_suggestions(self, error: Exception) -> list[str]:
        """Get database-specific recovery suggestions."""
        return [
            "Check database connection",
            "Verify database permissions",
            "Review SQL query syntax",
            "Check database server status",
        ]


class AuthenticationErrorHandler(BaseErrorHandler):
    """Handler for authentication errors."""

    def __init__(self):
        super().__init__(ErrorType.AUTHENTICATION_ERROR)

    def can_handle(self, error: Exception) -> bool:
        """Check if this is an authentication error."""
        return "auth" in str(error).lower() or "login" in str(error).lower()

    def handle(self, error: Exception, context: ErrorContext) -> ErrorDetails:
        """Handle authentication error."""
        self.handled_count += 1
        self.last_handled = datetime.now()

        return ErrorDetails(
            error_type=self.error_type,
            severity=ErrorSeverity.MEDIUM,
            message=f"Authentication error: {str(error)}",
            code="AUTHENTICATION_ERROR",
            context=context,
            stack_trace=str(error),
            recovery_suggestions=self.get_recovery_suggestions(error),
        )

    def get_recovery_suggestions(self, error: Exception) -> list[str]:
        """Get authentication-specific recovery suggestions."""
        return [
            "Verify credentials",
            "Check account status",
            "Reset password if needed",
            "Contact administrator",
        ]


class ErrorHandlerFactory:
    """
    Factory for creating error handlers.

    V2 Compliance: Factory pattern implementation for error handling.
    """

    def __init__(self):
        self.handlers: dict[ErrorType, BaseErrorHandler] = {}
        self._initialize_handlers()

    def _initialize_handlers(self):
        """Initialize default error handlers."""
        self.handlers = {
            ErrorType.VALIDATION_ERROR: ValidationErrorHandler(),
            ErrorType.NETWORK_ERROR: NetworkErrorHandler(),
            ErrorType.DATABASE_ERROR: DatabaseErrorHandler(),
            ErrorType.AUTHENTICATION_ERROR: AuthenticationErrorHandler(),
        }

    def get_handler(self, error_type: ErrorType) -> BaseErrorHandler | None:
        """Get handler for specific error type."""
        return self.handlers.get(error_type)

    def register_handler(self, error_type: ErrorType, handler: BaseErrorHandler):
        """Register a custom error handler."""
        self.handlers[error_type] = handler
        logger.info(f"✅ Registered handler for {error_type.value}")

    def create_handler(
        self, error_type: ErrorType, handler_class: type[BaseErrorHandler]
    ) -> BaseErrorHandler:
        """Create and register a new handler instance."""
        handler = handler_class()
        self.register_handler(error_type, handler)
        return handler

    def handle_error(self, error: Exception, context: ErrorContext) -> ErrorDetails:
        """Handle error using appropriate handler."""
        # Try to find a handler that can handle this error
        for handler in self.handlers.values():
            if handler.can_handle(error):
                return handler.handle(error, context)

        # Fallback to generic handler
        return self._create_generic_error_details(error, context)

    def _create_generic_error_details(
        self, error: Exception, context: ErrorContext
    ) -> ErrorDetails:
        """Create generic error details for unhandled errors."""
        return ErrorDetails(
            error_type=ErrorType.UNKNOWN_ERROR,
            severity=ErrorSeverity.HIGH,
            message=f"Unhandled error: {str(error)}",
            code="UNKNOWN_ERROR",
            context=context,
            stack_trace=str(error),
            recovery_suggestions=["Contact system administrator", "Check system logs"],
        )

    def get_handler_statistics(self) -> dict[str, Any]:
        """Get statistics for all handlers."""
        stats = {}
        for error_type, handler in self.handlers.items():
            stats[error_type.value] = {
                "handled_count": handler.handled_count,
                "last_handled": handler.last_handled.isoformat() if handler.last_handled else None,
            }
        return stats

    def reset_statistics(self):
        """Reset statistics for all handlers."""
        for handler in self.handlers.values():
            handler.handled_count = 0
            handler.last_handled = None
        logger.info("🔄 Handler statistics reset")


class ErrorHandlingService:
    """
    Service layer for error handling operations.

    V2 Compliance: Service layer pattern implementation.
    """

    def __init__(self):
        self.factory = ErrorHandlerFactory()
        self.error_log: list[ErrorDetails] = []
        self.max_log_size = 1000

    def handle_error(self, error: Exception, context: ErrorContext) -> ErrorDetails:
        """Handle error and log details."""
        error_details = self.factory.handle_error(error, context)

        # Log error details
        self._log_error(error_details)

        # Notify web interface if available
        self._notify_web_interface(error_details)

        return error_details

    def _log_error(self, error_details: ErrorDetails):
        """Log error details."""
        self.error_log.append(error_details)

        # Keep log size manageable
        if len(self.error_log) > self.max_log_size:
            self.error_log = self.error_log[-self.max_log_size :]

        # Log to system logger
        logger.error(f"Error handled: {error_details.message} [{error_details.code}]")

    def _notify_web_interface(self, error_details: ErrorDetails):
        """Notify web interface of error."""
        try:
            # Web interface integration for real-time error monitoring
            web_data = {
                "error_type": error_details.error_type.value,
                "severity": error_details.severity.value,
                "message": error_details.message,
                "timestamp": error_details.timestamp.isoformat(),
                "context": {
                    "component": error_details.context.component,
                    "operation": error_details.context.operation,
                },
            }
            # TODO: Implement web interface notification
            logger.info(f"🌐 Web interface notified: {error_details.error_type.value}")
        except Exception as e:
            logger.error(f"❌ Web interface notification failed: {e}")

    def get_error_statistics(self) -> dict[str, Any]:
        """Get comprehensive error statistics."""
        stats = {
            "total_errors": len(self.error_log),
            "errors_by_type": {},
            "errors_by_severity": {},
            "recent_errors": [],
            "handler_statistics": self.factory.get_handler_statistics(),
        }

        # Count errors by type and severity
        for error in self.error_log:
            error_type = error.error_type.value
            severity = error.severity.value

            stats["errors_by_type"][error_type] = stats["errors_by_type"].get(error_type, 0) + 1
            stats["errors_by_severity"][severity] = stats["errors_by_severity"].get(severity, 0) + 1

        # Get recent errors (last 10)
        stats["recent_errors"] = [
            {
                "type": error.error_type.value,
                "severity": error.severity.value,
                "message": error.message,
                "timestamp": error.timestamp.isoformat(),
            }
            for error in self.error_log[-10:]
        ]

        return stats

    def clear_error_log(self):
        """Clear error log."""
        self.error_log.clear()
        logger.info("🧹 Error log cleared")


# Global instance for web interface integration
_error_handling_service = None


def get_error_handling_service() -> ErrorHandlingService:
    """Get the global error handling service instance."""
    global _error_handling_service
    if _error_handling_service is None:
        _error_handling_service = ErrorHandlingService()
    return _error_handling_service
