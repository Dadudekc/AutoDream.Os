#!/usr/bin/env python3
"""
Unified Error Handling Module - V2 Compliant
===========================================

Unified error handling for all messaging system components.
V2 COMPLIANT: Under 200 lines, focused error handling responsibility.

Author: Agent-4 (Quality Assurance Specialist - CAPTAIN)
License: MIT
"""

import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MessagingError:
    """Messaging system error structure."""
    error_id: str
    component: str
    message: str
    severity: ErrorSeverity
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class UnifiedErrorHandler:
    """Unified error handler for messaging system."""
    
    def __init__(self):
        """Initialize the error handler."""
        self.error_count = 0
        self.errors: Dict[str, MessagingError] = {}
    
    def handle_error(self, error: Exception, component: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM) -> MessagingError:
        """Handle an error and return structured error information."""
        import uuid
        from datetime import datetime
        
        error_id = str(uuid.uuid4())
        error_obj = MessagingError(
            error_id=error_id,
            component=component,
            message=str(error),
            severity=severity,
            details={'type': type(error).__name__},
            timestamp=datetime.now().isoformat()
        )
        
        self.errors[error_id] = error_obj
        self.error_count += 1
        
        # Log the error
        log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }.get(severity, logging.WARNING)
        
        logger.log(log_level, f'Messaging Error [{component}]: {error}')
        
        return error_obj
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors."""
        return {
            'total_errors': self.error_count,
            'errors_by_severity': {
                severity.value: sum(1 for e in self.errors.values() if e.severity == severity)
                for severity in ErrorSeverity
            },
            'errors_by_component': {}
        }


# Global error handler instance
unified_error_handler = UnifiedErrorHandler()


def handle_messaging_error(error: Exception, component: str, severity: ErrorSeverity = ErrorSeverity.MEDIUM) -> MessagingError:
    """Convenience function for handling messaging errors."""
    return unified_error_handler.handle_error(error, component, severity)


def get_error_handler() -> UnifiedErrorHandler:
    """Get the global error handler instance."""
    return unified_error_handler
