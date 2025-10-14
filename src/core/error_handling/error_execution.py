#!/usr/bin/env python3
"""
Error Execution Orchestration Module
====================================

Execution logic for operations with comprehensive error handling.
Extracted from coordination_error_handler.py for autonomous systems.

Features:
- Retry execution with backoff
- Circuit breaker integration
- Recovery attempt orchestration
- Intelligent error analysis integration

Author: Agent-3 (Infrastructure & DevOps) - ROI Refactoring
License: MIT
"""

import logging
from collections.abc import Callable
from typing import TypeVar

from .circuit_breaker import CircuitBreaker
from .error_classification import ErrorClassifier, error_classifier
from .error_intelligence import intelligence_engine
from .recovery_strategies import RecoveryStrategy
from .retry_mechanisms import RetryMechanism

# Type variable for generic return types
T = TypeVar("T")

logger = logging.getLogger(__name__)


class ErrorExecutionOrchestrator:
    """Orchestrates operation execution with comprehensive error handling."""

    def __init__(
        self,
        circuit_breakers: dict[str, CircuitBreaker] | None = None,
        retry_mechanisms: dict[str, RetryMechanism] | None = None,
        recovery_strategies: list[RecoveryStrategy] | None = None,
        classifier: ErrorClassifier | None = None,
    ):
        """Initialize execution orchestrator.

        Args:
            circuit_breakers: Dict of circuit breakers by component
            retry_mechanisms: Dict of retry mechanisms by component
            recovery_strategies: List of recovery strategies
            classifier: Error classifier instance
        """
        self.circuit_breakers = circuit_breakers or {}
        self.retry_mechanisms = retry_mechanisms or {}
        self.recovery_strategies = recovery_strategies or []
        self.classifier = classifier or error_classifier
        logger.info("ErrorExecutionOrchestrator initialized")

    def execute_with_error_handling(
        self,
        operation: Callable[[], T],
        operation_name: str = "operation",
        component: str = "default",
        use_retry: bool = True,
        use_circuit_breaker: bool = True,
        use_recovery: bool = True,
        use_intelligence: bool = True,
    ) -> T:
        """Execute operation with comprehensive error handling.

        Args:
            operation: Operation to execute
            operation_name: Name for logging
            component: Component identifier
            use_retry: Enable retry mechanism
            use_circuit_breaker: Enable circuit breaker
            use_recovery: Enable recovery strategies
            use_intelligence: Enable intelligent error analysis

        Returns:
            Operation result

        Raises:
            Exception: If operation fails after all recovery attempts
        """
        # Check predictive failure risk if intelligence enabled
        if use_intelligence:
            self._check_failure_risk(component)

        # Get components
        circuit_breaker = self.circuit_breakers.get(component) if use_circuit_breaker else None
        retry_mechanism = self.retry_mechanisms.get(component) if use_retry else None

        try:
            # Execute with retry (circuit breaker integration pending)
            result = self._execute_with_retry(operation, retry_mechanism, operation_name)

            # Record successful execution
            if use_intelligence:
                intelligence_engine.record_recovery(component, success=True, recovery_time=0.0)

            return result

        except Exception as e:
            # Record error for intelligence analysis
            if use_intelligence:
                self._record_error_intelligence(e, component, operation_name)

            # Attempt recovery if enabled
            if use_recovery:
                logger.warning(f"Operation {operation_name} failed, attempting recovery: {e}")
                recovery_success = self._attempt_recovery(
                    component, type(e).__name__, use_intelligence
                )

                if recovery_success:
                    # Retry operation after successful recovery
                    return self._execute_with_retry(operation, retry_mechanism, operation_name)

            # If recovery failed or not enabled, raise the error
            logger.error(f"Operation {operation_name} failed after all attempts")
            raise e

    def _execute_with_retry(
        self,
        operation: Callable[[], T],
        retry_mechanism: RetryMechanism | None,
        operation_name: str,
    ) -> T:
        """Execute operation with retry mechanism if available.

        Args:
            operation: Operation to execute
            retry_mechanism: Retry mechanism to use (if any)
            operation_name: Operation name for logging

        Returns:
            Operation result
        """
        if retry_mechanism:
            logger.debug(f"Executing {operation_name} with retry mechanism")
            return retry_mechanism.execute_with_retry(operation)
        else:
            logger.debug(f"Executing {operation_name} without retry")
            return operation()

    def _attempt_recovery(self, component: str, error_type: str, use_intelligence: bool) -> bool:
        """Attempt error recovery using registered strategies.

        Args:
            component: Component to recover
            error_type: Type of error encountered
            use_intelligence: Whether to use intelligent suggestions

        Returns:
            True if recovery succeeded, False otherwise
        """
        # Get intelligent recovery suggestion
        suggested_strategy = None
        if use_intelligence:
            suggested_strategy = intelligence_engine.suggest_recovery_strategy(
                error_type, component
            )
            logger.info(
                f"Intelligence suggests recovery strategy: {suggested_strategy} for {component}"
            )

        # Try suggested strategy first
        if suggested_strategy:
            for strategy in self.recovery_strategies:
                if suggested_strategy.lower() in strategy.name.lower():
                    if self._execute_recovery_strategy(strategy, component, error_type):
                        if use_intelligence:
                            intelligence_engine.record_recovery(
                                component, success=True, recovery_time=1.0
                            )
                        return True

        # Fallback: try all strategies
        for strategy in self.recovery_strategies:
            if self._execute_recovery_strategy(strategy, component, error_type):
                if use_intelligence:
                    intelligence_engine.record_recovery(component, success=True, recovery_time=1.0)
                return True

        # Recovery failed
        if use_intelligence:
            intelligence_engine.record_recovery(component, success=False, recovery_time=1.0)

        logger.warning(f"All recovery strategies failed for {component}")
        return False

    def _execute_recovery_strategy(
        self, strategy: RecoveryStrategy, component: str, error_type: str
    ) -> bool:
        """Execute a single recovery strategy.

        Args:
            strategy: Strategy to execute
            component: Component to recover
            error_type: Type of error

        Returns:
            True if strategy succeeded
        """
        try:
            if strategy.execute({"component": component, "error_type": error_type}):
                logger.info(f"Recovery successful with strategy: {strategy.name}")
                return True
        except Exception as e:
            logger.error(f"Recovery strategy {strategy.name} failed: {e}")
        return False

    def _check_failure_risk(self, component: str):
        """Check predictive failure risk for component.

        Args:
            component: Component to check
        """
        try:
            risk_score, risk_level = intelligence_engine.predict_failure_risk(component)
            if risk_level in ("high", "critical"):
                logger.warning(
                    f"High failure risk detected for {component}: {risk_score:.2f} ({risk_level})"
                )
        except Exception as e:
            logger.debug(f"Could not check failure risk: {e}")

    def _record_error_intelligence(self, error: Exception, component: str, operation_name: str):
        """Record error for intelligence analysis.

        Args:
            error: Exception that occurred
            component: Component where error occurred
            operation_name: Name of operation that failed
        """
        try:
            error_type = type(error).__name__
            severity, category = self.classifier.classify_error(error)
            intelligence_engine.record_error(
                error_type=error_type,
                component=component,
                severity=severity.value,
                context={"operation": operation_name, "category": category.value},
            )
        except Exception as e:
            logger.error(f"Failed to record error intelligence: {e}")


# Global execution orchestrator (to be initialized with handlers)
_global_orchestrator: ErrorExecutionOrchestrator | None = None


def get_orchestrator() -> ErrorExecutionOrchestrator:
    """Get or create global execution orchestrator."""
    global _global_orchestrator
    if _global_orchestrator is None:
        _global_orchestrator = ErrorExecutionOrchestrator()
    return _global_orchestrator


def execute_with_error_handling(
    operation: Callable[[], T],
    operation_name: str = "operation",
    component: str = "default",
    **kwargs,
) -> T:
    """Execute operation with error handling using global orchestrator."""
    orchestrator = get_orchestrator()
    return orchestrator.execute_with_error_handling(operation, operation_name, component, **kwargs)
