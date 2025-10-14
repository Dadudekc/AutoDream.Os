#!/usr/bin/env python3
"""
Error Decision Models
=====================

Error classification, retry configuration, and decision engine models.
Extracted from error_handling_models.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring (500 pts, ROI 33.33)
License: MIT
"""

from dataclasses import dataclass, field
from typing import Any

from .error_models_enums import ErrorCategory, ErrorRecoverability, ErrorSeverity


@dataclass
class ErrorClassifier:
    """
    Intelligent error classifier for autonomous systems.

    Classifies errors by severity, category, and recoverability.
    """

    # Severity thresholds
    critical_threshold: int = 90
    high_threshold: int = 70
    medium_threshold: int = 40

    # Error type mappings
    critical_errors: tuple[type[Exception], ...] = field(
        default_factory=lambda: (
            SystemError,
            MemoryError,
            KeyboardInterrupt,
        )
    )
    high_errors: tuple[type[Exception], ...] = field(
        default_factory=lambda: (
            ConnectionError,
            TimeoutError,
            OSError,
        )
    )

    def classify(
        self, error: Exception
    ) -> tuple[ErrorSeverity, ErrorCategory, ErrorRecoverability]:
        """Classify error by severity, category, and recoverability.

        Args:
            error: Exception to classify

        Returns:
            Tuple of (severity, category, recoverability)
        """
        severity = self._determine_severity(error)
        category = self._determine_category(error)
        recoverability = self._determine_recoverability(error, severity)

        return severity, category, recoverability

    def _determine_severity(self, error: Exception) -> ErrorSeverity:
        """Determine error severity."""
        if isinstance(error, self.critical_errors):
            return ErrorSeverity.CRITICAL
        elif isinstance(error, self.high_errors):
            return ErrorSeverity.HIGH
        elif isinstance(error, (ValueError, TypeError)):
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW

    def _determine_category(self, error: Exception) -> ErrorCategory:
        """Determine error category."""
        if isinstance(error, (ConnectionError, TimeoutError)):
            return ErrorCategory.NETWORK
        elif isinstance(error, (IOError, FileNotFoundError)):
            return ErrorCategory.FILE
        elif isinstance(error, (ValueError, KeyError)):
            return ErrorCategory.VALIDATION
        else:
            return ErrorCategory.SYSTEM

    def _determine_recoverability(
        self, error: Exception, severity: ErrorSeverity
    ) -> ErrorRecoverability:
        """Determine if error is recoverable."""
        if severity == ErrorSeverity.CRITICAL:
            return ErrorRecoverability.NOT_RECOVERABLE
        elif isinstance(error, (ConnectionError, TimeoutError, IOError)):
            return ErrorRecoverability.RECOVERABLE
        elif severity == ErrorSeverity.HIGH:
            return ErrorRecoverability.PARTIALLY_RECOVERABLE
        else:
            return ErrorRecoverability.RECOVERABLE


@dataclass
class RetryConfiguration:
    """
    Retry configuration for error recovery.

    Defines retry behavior for different error types.
    """

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_backoff: bool = True
    backoff_factor: float = 2.0
    retry_exceptions: tuple[type[Exception], ...] = field(
        default_factory=lambda: (
            ConnectionError,
            TimeoutError,
            IOError,
        )
    )

    def should_retry(self, error: Exception, attempt: int) -> bool:
        """Determine if operation should be retried.

        Args:
            error: Exception that occurred
            attempt: Current attempt number

        Returns:
            True if should retry
        """
        if attempt >= self.max_retries:
            return False

        return isinstance(error, self.retry_exceptions)

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt.

        Args:
            attempt: Current attempt number

        Returns:
            Delay in seconds
        """
        if self.exponential_backoff:
            delay = self.base_delay * (self.backoff_factor**attempt)
        else:
            delay = self.base_delay

        return min(delay, self.max_delay)


@dataclass
class ErrorDecisionEngine:
    """
    Error decision engine for autonomous error handling.

    Makes decisions about error handling strategies based on classification.
    """

    classifier: ErrorClassifier = field(default_factory=ErrorClassifier)
    retry_config: RetryConfiguration = field(default_factory=RetryConfiguration)

    def decide_action(self, error: Exception, attempt: int = 0) -> dict[str, Any]:
        """Decide action for error handling.

        Args:
            error: Exception that occurred
            attempt: Current attempt number

        Returns:
            Decision dictionary with action and parameters
        """
        severity, category, recoverability = self.classifier.classify(error)

        decision = {
            "severity": severity.value,
            "category": category.value,
            "recoverability": recoverability.value,
            "should_retry": False,
            "should_recover": False,
            "suggested_action": "log_and_raise",
        }

        # Determine if should retry
        if recoverability in (
            ErrorRecoverability.RECOVERABLE,
            ErrorRecoverability.PARTIALLY_RECOVERABLE,
        ):
            decision["should_retry"] = self.retry_config.should_retry(error, attempt)
            if decision["should_retry"]:
                decision["retry_delay"] = self.retry_config.get_delay(attempt)
                decision["suggested_action"] = "retry_with_backoff"

        # Determine if should attempt recovery
        if recoverability != ErrorRecoverability.NOT_RECOVERABLE and not decision["should_retry"]:
            decision["should_recover"] = True
            decision["suggested_action"] = "attempt_recovery"

        return decision
