#!/usr/bin/env python3
"""
Error Handling System - V2 Compliant
====================================

Unified error handling system with retry, recovery, and circuit breaker.

Consolidates:
- retry_mechanisms.py (RetryMechanism, decorators, exponential backoff)
- error_recovery.py (RecoveryStrategy, ErrorRecoveryManager)
- coordination_error_handler.py (CircuitBreaker, CoordinationErrorHandler)
- error_handling_orchestrator.py (UnifiedErrorHandlingOrchestrator)

Author: Agent-3 - Infrastructure & DevOps Specialist
Created: 2025-10-10 (C-055-3 Consolidation)
Purpose: V2 compliant unified error handling system
"""

import logging
import time
from collections.abc import Callable
from datetime import datetime, timedelta
from functools import wraps
from typing import Any

from .error_handling_core import (
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitState,
    ErrorContext,
    ErrorSeverity,
    RetryConfig,
    RetryException,
)

logger = logging.getLogger(__name__)


# ============================================================================
# RETRY MECHANISM
# ============================================================================


class RetryMechanism:
    """Retry mechanism with exponential backoff and jitter."""

    def __init__(self, config: RetryConfig):
        """Initialize retry mechanism."""
        self.config = config

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry mechanism."""
        last_exception = None

        for attempt in range(self.config.max_attempts):
            try:
                return func(*args, **kwargs)
            except self.config.exceptions as e:
                last_exception = e

                if attempt == self.config.max_attempts - 1:
                    # Last attempt failed
                    logger.error(
                        f"Function failed after {self.config.max_attempts} attempts",
                        exc_info=True,
                    )
                    raise e

                delay = self.config.calculate_delay(attempt)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}")

                time.sleep(delay)

        # This should never be reached, but just in case
        raise last_exception


def retry_on_exception(config: RetryConfig, exceptions: type[Exception] | tuple = Exception):
    """Decorator for retrying on specific exceptions."""
    mechanism = RetryMechanism(config)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            def execute():
                return func(*args, **kwargs)

            return mechanism.execute_with_retry(execute)

        return wrapper

    return decorator


def with_exponential_backoff(
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    max_attempts: int = 3,
    jitter: bool = True,
):
    """Decorator for functions with exponential backoff retry."""
    config = RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        backoff_factor=backoff_factor,
        jitter=jitter,
    )
    mechanism = RetryMechanism(config)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return mechanism.execute_with_retry(func, *args, **kwargs)

        return wrapper

    return decorator


# ============================================================================
# CIRCUIT BREAKER
# ============================================================================


class CircuitBreaker:
    """Circuit breaker for fault tolerance."""

    def __init__(self, config: CircuitBreakerConfig):
        """Initialize circuit breaker."""
        self.config = config
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, operation: Callable, *args, **kwargs):
        """Execute operation through circuit breaker."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerError(f"Circuit breaker is OPEN for {self.config.name}")

        try:
            result = operation(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt to reset."""
        if self.last_failure_time is None:
            return True
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.config.recovery_timeout

    def _on_success(self):
        """Handle successful operation."""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            logger.info(f"Circuit breaker reset to CLOSED state for {self.config.name}")

    def _on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(
                f"Circuit breaker opened after {self.failure_count} failures for {self.config.name}"
            )


# ============================================================================
# RECOVERY STRATEGIES
# ============================================================================


class RecoveryStrategy:
    """Base class for error recovery strategies."""

    def __init__(self, name: str, description: str = ""):
        """Initialize recovery strategy."""
        self.name = name
        self.description = description or name

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if this strategy can recover from the error."""
        raise NotImplementedError("Subclasses must implement can_recover")

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute the recovery strategy."""
        raise NotImplementedError("Subclasses must implement execute_recovery")


class ServiceRestartStrategy(RecoveryStrategy):
    """Strategy for restarting failed services."""

    def __init__(self, service_manager: Callable):
        """Initialize service restart strategy."""
        super().__init__("service_restart", "Restart failed service components")
        self.service_manager = service_manager
        self.last_restart = None
        self.restart_cooldown = timedelta(minutes=5)

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if service restart is appropriate."""
        if self.last_restart and datetime.now() - self.last_restart < self.restart_cooldown:
            return False
        return error_context.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute service restart."""
        try:
            logger.info(f"Executing service restart for {error_context.operation}")
            success = self.service_manager()
            if success:
                self.last_restart = datetime.now()
                logger.info(f"Service restart successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Service restart failed: {e}")
            return False


class ConfigurationResetStrategy(RecoveryStrategy):
    """Strategy for resetting configuration to defaults."""

    def __init__(self, config_reset_func: Callable):
        """Initialize configuration reset strategy."""
        super().__init__("config_reset", "Reset configuration to safe defaults")
        self.config_reset_func = config_reset_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if configuration reset is appropriate."""
        return (
            "config" in error_context.operation.lower()
            or error_context.severity == ErrorSeverity.CRITICAL
        )

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute configuration reset."""
        try:
            logger.info(f"Executing configuration reset for {error_context.operation}")
            success = self.config_reset_func()
            if success:
                logger.info(f"Configuration reset successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Configuration reset failed: {e}")
            return False


class ResourceCleanupStrategy(RecoveryStrategy):
    """Strategy for cleaning up stuck resources."""

    def __init__(self, cleanup_func: Callable):
        """Initialize resource cleanup strategy."""
        super().__init__("resource_cleanup", "Clean up stuck resources and locks")
        self.cleanup_func = cleanup_func

    def can_recover(self, error_context: ErrorContext) -> bool:
        """Check if resource cleanup is appropriate."""
        error_data = str(error_context.additional_data).lower()
        return "resource" in error_data or "lock" in error_data

    def execute_recovery(self, error_context: ErrorContext) -> bool:
        """Execute resource cleanup."""
        try:
            logger.info(f"Executing resource cleanup for {error_context.operation}")
            success = self.cleanup_func()
            if success:
                logger.info(f"Resource cleanup successful for {error_context.operation}")
            return success
        except Exception as e:
            logger.error(f"Resource cleanup failed: {e}")
            return False


# ============================================================================
# RECOVERY MANAGER
# ============================================================================


class ErrorRecoveryManager:
    """Manages error recovery strategies."""

    def __init__(self):
        """Initialize error recovery manager."""
        self.strategies: list[RecoveryStrategy] = []
        self.recovery_history: list[dict[str, Any]] = []

    def add_strategy(self, strategy: RecoveryStrategy):
        """Add a recovery strategy."""
        self.strategies.append(strategy)
        logger.info(f"Added recovery strategy: {strategy.name}")

    def attempt_recovery(self, error_context: ErrorContext) -> bool:
        """Attempt to recover from an error using available strategies."""
        recovery_attempt = {
            "timestamp": datetime.now(),
            "error_context": error_context,
            "strategies_attempted": [],
            "successful_strategy": None,
            "recovery_success": False,
        }

        for strategy in self.strategies:
            if strategy.can_recover(error_context):
                recovery_attempt["strategies_attempted"].append(strategy.name)

                logger.info(f"Attempting recovery with strategy: {strategy.name}")
                success = strategy.execute_recovery(error_context)

                if success:
                    recovery_attempt["successful_strategy"] = strategy.name
                    recovery_attempt["recovery_success"] = True
                    logger.info(f"Recovery successful using strategy: {strategy.name}")
                    break
                else:
                    logger.warning(f"Recovery failed with strategy: {strategy.name}")

        self.recovery_history.append(recovery_attempt)
        return recovery_attempt["recovery_success"]

    def get_recovery_statistics(self) -> dict[str, Any]:
        """Get recovery statistics."""
        if not self.recovery_history:
            return {"total_attempts": 0, "successful_recoveries": 0, "success_rate": 0}

        total_attempts = len(self.recovery_history)
        successful_recoveries = len([r for r in self.recovery_history if r["recovery_success"]])

        return {
            "total_attempts": total_attempts,
            "successful_recoveries": successful_recoveries,
            "success_rate": (
                (successful_recoveries / total_attempts) * 100 if total_attempts > 0 else 0
            ),
        }


# ============================================================================
# UNIFIED ERROR HANDLING ORCHESTRATOR
# ============================================================================


class UnifiedErrorHandlingOrchestrator:
    """
    Unified Error Handling Orchestrator - V2 Compliant

    Orchestrates all error handling functionality:
    - Retry operations with exponential backoff
    - Circuit breaker fault tolerance
    - Recovery strategies and automatic remediation
    - Comprehensive error tracking and reporting
    """

    def __init__(self, logger_instance: logging.Logger | None = None):
        """Initialize error handling orchestrator."""
        self.logger = logger_instance or logger
        self.retry_mechanisms: dict[str, RetryMechanism] = {}
        self.circuit_breakers: dict[str, CircuitBreaker] = {}
        self.recovery_manager = ErrorRecoveryManager()

    def register_retry_mechanism(self, component: str, config: RetryConfig):
        """Register a retry mechanism for a component."""
        self.retry_mechanisms[component] = RetryMechanism(config)
        logger.info(f"Registered retry mechanism for {component}")

    def register_circuit_breaker(self, component: str, config: CircuitBreakerConfig):
        """Register a circuit breaker for a component."""
        self.circuit_breakers[component] = CircuitBreaker(config)
        logger.info(f"Registered circuit breaker for {component}")

    def execute_with_comprehensive_error_handling(
        self,
        operation: Callable,
        operation_name: str,
        component: str,
        use_retry: bool = True,
        use_circuit_breaker: bool = True,
        use_recovery: bool = True,
    ) -> Any:
        """Execute operation with comprehensive error handling."""

        def wrapped_operation():
            return operation()

        # Apply circuit breaker if enabled
        if use_circuit_breaker and component in self.circuit_breakers:
            circuit_breaker = self.circuit_breakers[component]

            def circuit_protected_operation():
                return circuit_breaker.call(wrapped_operation)

            wrapped_operation = circuit_protected_operation

        # Apply retry if enabled
        if use_retry:
            retry_mechanism = self.retry_mechanisms.get(
                component, RetryMechanism(RetryConfig())
            )

            try:
                return retry_mechanism.execute_with_retry(wrapped_operation)
            except Exception as e:
                # Attempt recovery if enabled
                if use_recovery:
                    error_context = ErrorContext(
                        operation=operation_name,
                        timestamp=datetime.now().isoformat(),
                        error_type=type(e).__name__,
                        category=None,  # Will be determined by recovery strategy
                        severity=ErrorSeverity.HIGH,
                        additional_data={"exception": str(e)},
                    )

                    if self.recovery_manager.attempt_recovery(error_context):
                        # Retry once after recovery
                        try:
                            return retry_mechanism.execute_with_retry(wrapped_operation)
                        except Exception as retry_error:
                            logger.error(f"Operation failed even after recovery: {retry_error}")
                            raise retry_error

                raise e
        else:
            return wrapped_operation()

    def get_system_health_report(self) -> dict[str, Any]:
        """Get comprehensive system health report."""
        circuit_statuses = {
            name: breaker.state.value for name, breaker in self.circuit_breakers.items()
        }

        recovery_stats = self.recovery_manager.get_recovery_statistics()

        return {
            "status": "operational",
            "circuit_breakers": circuit_statuses,
            "recovery_statistics": recovery_stats,
            "timestamp": datetime.now().isoformat(),
        }

    def get_component_status(self, component: str) -> dict[str, Any]:
        """Get detailed status for a specific component."""
        status = {"component": component, "timestamp": datetime.now().isoformat()}

        if component in self.circuit_breakers:
            breaker = self.circuit_breakers[component]
            status["circuit_breaker"] = {
                "state": breaker.state.value,
                "failure_count": breaker.failure_count,
                "last_failure": breaker.last_failure_time.isoformat()
                if breaker.last_failure_time
                else None,
            }

        if component in self.retry_mechanisms:
            status["retry_mechanism"] = {"configured": True}

        return status

    def cleanup_stale_data(self) -> dict[str, int]:
        """Clean up stale error data and logs."""
        # Clean old recovery history (keep last 1000)
        initial_count = len(self.recovery_manager.recovery_history)
        if initial_count > 1000:
            self.recovery_manager.recovery_history = self.recovery_manager.recovery_history[-1000:]

        cleaned = initial_count - len(self.recovery_manager.recovery_history)

        return {"cleaned_records": cleaned}

    def reset_component(self, component: str) -> bool:
        """Reset error handling state for a specific component."""
        if component in self.circuit_breakers:
            breaker = self.circuit_breakers[component]
            breaker.state = CircuitState.CLOSED
            breaker.failure_count = 0
            breaker.last_failure_time = None
            logger.info(f"Reset circuit breaker for {component}")
            return True

        return False


# ============================================================================
# DECORATOR FUNCTIONS
# ============================================================================


def with_error_recovery(recovery_manager: ErrorRecoveryManager):
    """Decorator for automatic error recovery."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Create error context
                error_context = ErrorContext(
                    operation=f"{func.__module__}.{func.__name__}",
                    timestamp=datetime.now().isoformat(),
                    error_type=type(e).__name__,
                    category=None,
                    severity=ErrorSeverity.HIGH,
                    additional_data={"exception": str(e), "exception_type": type(e).__name__},
                )

                # Attempt recovery
                if recovery_manager.attempt_recovery(error_context):
                    # Retry the operation once after successful recovery
                    try:
                        return func(*args, **kwargs)
                    except Exception as retry_error:
                        logger.error(f"Operation failed even after recovery: {retry_error}")
                        raise retry_error
                else:
                    logger.error(f"No recovery strategy succeeded for: {e}")
                    raise e

        return wrapper

    return decorator


# ============================================================================
# GLOBAL ORCHESTRATOR INSTANCE
# ============================================================================

_global_orchestrator = None


def get_error_handling_orchestrator(
    logger_instance: logging.Logger | None = None,
) -> UnifiedErrorHandlingOrchestrator:
    """Get global error handling orchestrator instance."""
    global _global_orchestrator
    if _global_orchestrator is None:
        _global_orchestrator = UnifiedErrorHandlingOrchestrator(logger_instance)
    return _global_orchestrator

