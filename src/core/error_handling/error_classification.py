#!/usr/bin/env python3
"""
Error Classification Module
===========================

Intelligent error classification for autonomous systems.
Extracts from coordination_error_handler.py for better modularity.

Features:
- Error severity determination
- Error type categorization
- Pattern-based classification
- Autonomous error identification

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring
License: MIT
"""

import logging
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels for classification."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ErrorCategory(Enum):
    """Error categories for intelligent handling."""

    SYSTEM = "system"  # System-level errors
    NETWORK = "network"  # Network/connection errors
    RESOURCE = "resource"  # Resource availability errors
    CONFIGURATION = "configuration"  # Configuration errors
    COORDINATION = "coordination"  # Coordination-specific errors
    UNKNOWN = "unknown"  # Unclassified errors


class ErrorClassifier:
    """Intelligent error classifier for autonomous systems."""

    # Error type mappings for classification
    CRITICAL_ERRORS = (SystemError, MemoryError, KeyboardInterrupt)
    HIGH_ERRORS = (ConnectionError, TimeoutError, OSError, IOError)
    NETWORK_ERRORS = (ConnectionError, TimeoutError, ConnectionRefusedError, ConnectionResetError)
    RESOURCE_ERRORS = (MemoryError, OSError, PermissionError)
    CONFIGURATION_ERRORS = (ValueError, KeyError, AttributeError)

    def __init__(self):
        """Initialize error classifier."""
        self.classification_cache: dict[str, tuple[ErrorSeverity, ErrorCategory]] = {}
        logger.info("ErrorClassifier initialized")

    def classify_error(self, error: Exception) -> tuple[ErrorSeverity, ErrorCategory]:
        """Classify error by severity and category.

        Args:
            error: Exception to classify

        Returns:
            Tuple of (severity, category)
        """
        error_type = type(error).__name__

        # Check cache first
        if error_type in self.classification_cache:
            return self.classification_cache[error_type]

        severity = self.determine_severity(error)
        category = self.determine_category(error)

        # Cache result
        self.classification_cache[error_type] = (severity, category)

        logger.debug(f"Classified {error_type}: {severity.value}/{category.value}")
        return severity, category

    def determine_severity(self, error: Exception) -> ErrorSeverity:
        """Determine error severity based on error type.

        Args:
            error: Exception to analyze

        Returns:
            ErrorSeverity level
        """
        if isinstance(error, self.CRITICAL_ERRORS):
            return ErrorSeverity.CRITICAL
        elif isinstance(error, self.HIGH_ERRORS):
            return ErrorSeverity.HIGH
        elif isinstance(error, (ValueError, TypeError)):
            return ErrorSeverity.MEDIUM
        elif isinstance(error, (Warning, UserWarning)):
            return ErrorSeverity.LOW
        else:
            return ErrorSeverity.MEDIUM

    def determine_category(self, error: Exception) -> ErrorCategory:
        """Determine error category for targeted handling.

        Args:
            error: Exception to analyze

        Returns:
            ErrorCategory
        """
        if isinstance(error, self.NETWORK_ERRORS):
            return ErrorCategory.NETWORK
        elif isinstance(error, self.RESOURCE_ERRORS):
            return ErrorCategory.RESOURCE
        elif isinstance(error, self.CONFIGURATION_ERRORS):
            return ErrorCategory.CONFIGURATION
        elif isinstance(error, (SystemError, RuntimeError)):
            return ErrorCategory.SYSTEM
        else:
            return ErrorCategory.UNKNOWN

    def is_recoverable(self, error: Exception) -> bool:
        """Determine if error is potentially recoverable.

        Args:
            error: Exception to analyze

        Returns:
            True if error might be recoverable
        """
        severity, category = self.classify_error(error)

        # Critical system errors usually not recoverable
        if severity == ErrorSeverity.CRITICAL:
            return False

        # Network and resource errors often recoverable
        if category in (ErrorCategory.NETWORK, ErrorCategory.RESOURCE):
            return True

        # Configuration errors might be recoverable
        if category == ErrorCategory.CONFIGURATION:
            return True

        # High severity errors might be recoverable depending on type
        return severity in (ErrorSeverity.HIGH, ErrorSeverity.MEDIUM, ErrorSeverity.LOW)

    def suggest_recovery_approach(self, error: Exception) -> str:
        """Suggest recovery approach based on error classification.

        Args:
            error: Exception to analyze

        Returns:
            Suggested recovery approach
        """
        severity, category = self.classify_error(error)

        if category == ErrorCategory.NETWORK:
            return "retry_with_backoff"
        elif category == ErrorCategory.RESOURCE:
            return "resource_cleanup"
        elif category == ErrorCategory.CONFIGURATION:
            return "configuration_reset"
        elif category == ErrorCategory.SYSTEM:
            return "service_restart"
        else:
            return "generic_retry"

    def get_classification_stats(self) -> dict:
        """Get classification statistics.

        Returns:
            Statistics about classified errors
        """
        severity_counts = {}
        category_counts = {}

        for _, (severity, category) in self.classification_cache.items():
            severity_counts[severity.value] = severity_counts.get(severity.value, 0) + 1
            category_counts[category.value] = category_counts.get(category.value, 0) + 1

        return {
            "total_classifications": len(self.classification_cache),
            "by_severity": severity_counts,
            "by_category": category_counts,
        }

    def clear_cache(self):
        """Clear classification cache."""
        self.classification_cache.clear()
        logger.info("Classification cache cleared")


# Global classifier instance
error_classifier = ErrorClassifier()


# Helper functions for quick classification
def classify_error(error: Exception) -> tuple[ErrorSeverity, ErrorCategory]:
    """Classify error using global classifier."""
    return error_classifier.classify_error(error)


def determine_severity(error: Exception) -> ErrorSeverity:
    """Determine error severity using global classifier."""
    return error_classifier.determine_severity(error)


def is_recoverable(error: Exception) -> bool:
    """Check if error is recoverable using global classifier."""
    return error_classifier.is_recoverable(error)


def suggest_recovery_approach(error: Exception) -> str:
    """Suggest recovery approach using global classifier."""
    return error_classifier.suggest_recovery_approach(error)
