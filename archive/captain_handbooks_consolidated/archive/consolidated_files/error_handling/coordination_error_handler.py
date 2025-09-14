#!/usr/bin/env python3
"""
Coordination & Communication Error Handler - Agent Cellphone V2
============================================================

Streamlined error handler leveraging modular components for V2 compliance.

Features:
- Circuit breaker patterns for fault tolerance
- Retry mechanisms with exponential backoff
- Recovery strategies for coordination components
- Comprehensive error reporting and monitoring

Author: Agent-3 (Configuration Management Specialist) - Enhanced Implementation
License: MIT
"""

import logging
import time
from collections.abc import Callable
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, TypeVar

# Type variable for generic return types
T = TypeVar("T")


# Get logger function for compatibility
def get_logger(name: str):
    """Get logger with consistent formatting."""
    return logging.getLogger(name)


logger = logging.getLogger(__name__)


class RecoveryStrategy:
    """Base class for recovery strategies."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def execute(self, error_context: dict[str, Any]) -> bool:
        """Execute the recovery strategy."""
        raise NotImplementedError("Subclasses must implement execute method")

    def can_recover(self, error_context: dict[str, Any]) -> bool:
        """Check if this strategy can recover from the error."""
        return True  # Default implementation - subclasses can override


class CircuitBreakerConfig:
    """Configuration for circuit breaker."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0, name: str = ""):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name


class RetryConfig:
    """Configuration for retry mechanism."""

    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay


class ErrorHandlingOrchestrator:
    """Comprehensive error handling orchestrator with circuit breaker and retry patterns."""

    def __init__(self):
        self.retry_mechanisms: dict[str, RetryConfig] = {}
        self.circuit_breakers: dict[str, CircuitBreaker] = {}
        self.components: dict[str, dict[str, Any]] = {}
        self.recovery_manager = RecoveryManager()
        self.error_reporter = ErrorReporter()
        self._component_stats: dict[str, dict[str, Any]] = {}

    def register_retry_mechanism(self, component: str, config: RetryConfig):
        """Register a retry mechanism for a component."""
        self.retry_mechanisms[component] = config
        get_logger(__name__).info(f"Registered retry mechanism for {component}")

    def register_circuit_breaker(self, component: str, config: CircuitBreakerConfig):
        """Register a circuit breaker for a component."""
        self.circuit_breakers[component] = CircuitBreaker(
            failure_threshold=config.failure_threshold, recovery_timeout=config.recovery_timeout
        )
        get_logger(__name__).info(f"Registered circuit breaker for {component}")

    def execute_with_comprehensive_error_handling(
        self,
        operation: Callable[[], T],
        operation_name: str = "operation",
        component: str = "coordination",
        use_retry: bool = True,
        use_circuit_breaker: bool = True,
        use_recovery: bool = True,
    ) -> T:
        """Execute operation with comprehensive error handling."""
        start_time = time.time()

        try:
            # Initialize component stats if needed
            if component not in self._component_stats:
                self._component_stats[component] = {
                    "total_calls": 0,
                    "successful_calls": 0,
                    "failed_calls": 0,
                    "last_call_time": None,
                    "circuit_breaker_trips": 0,
                    "retry_attempts": 0,
                }

            self._component_stats[component]["total_calls"] += 1
            self._component_stats[component]["last_call_time"] = datetime.now()

            # Execute with circuit breaker if enabled
            if use_circuit_breaker and component in self.circuit_breakers:
                result = self.circuit_breakers[component].call(operation)
            else:
                result = operation()

            # Record success
            self._component_stats[component]["successful_calls"] += 1
            execution_time = time.time() - start_time

            get_logger(__name__).info(
                f"Operation {operation_name} completed successfully in {execution_time:.2f}s"
            )

            return result

        except Exception as e:
            # Record failure
            self._component_stats[component]["failed_calls"] += 1
            execution_time = time.time() - start_time

            error_context = {
                "operation": operation_name,
                "component": component,
                "error": str(e),
                "error_type": type(e).__name__,
                "timestamp": datetime.now(),
                "execution_time": execution_time,
            }

            get_logger(__name__).error(f"Operation {operation_name} failed: {e}")

            # Attempt recovery if enabled
            if use_recovery:
                if self.recovery_manager.attempt_recovery(error_context):
                    get_logger(__name__).info(f"Recovery successful for {operation_name}")
                    # Retry once after successful recovery
                    try:
                        if use_circuit_breaker and component in self.circuit_breakers:
                            result = self.circuit_breakers[component].call(operation)
                        else:
                            result = operation()
                        self._component_stats[component]["successful_calls"] += 1
                        return result
                    except Exception as retry_error:
                        get_logger(__name__).error(f"Retry failed after recovery: {retry_error}")
                        raise retry_error
                else:
                    get_logger(__name__).warning(
                        f"No recovery strategy succeeded for {operation_name}"
                    )

            # Report error
            self.error_reporter.report_error(error_context)

            raise e

    def get_system_health_report(self) -> dict[str, Any]:
        """Get comprehensive system health report."""
        total_components = len(self._component_stats)
        healthy_components = sum(
            1
            for stats in self._component_stats.values()
            if stats["failed_calls"] == 0
            or (stats["total_calls"] > 0 and stats["successful_calls"] / stats["total_calls"] > 0.8)
        )

        circuit_breaker_status = {}
        for component, breaker in self.circuit_breakers.items():
            circuit_breaker_status[component] = {
                "state": breaker.state.value,
                "failure_count": breaker.failure_count,
                "last_failure_time": (
                    breaker.last_failure_time.isoformat() if breaker.last_failure_time else None
                ),
            }

        return {
            "status": "healthy" if healthy_components == total_components else "degraded",
            "total_components": total_components,
            "healthy_components": healthy_components,
            "unhealthy_components": total_components - healthy_components,
            "circuit_breakers": circuit_breaker_status,
            "recovery_stats": self.recovery_manager.get_recovery_statistics(),
            "timestamp": datetime.now().isoformat(),
        }

    def get_component_status(self, component: str) -> dict[str, Any]:
        """Get detailed status for a specific component."""
        if component not in self._component_stats:
            return {
                "component": component,
                "status": "unknown",
                "error": "Component not registered",
            }

        stats = self._component_stats[component]

        # Determine component health
        if stats["total_calls"] == 0:
            health_status = "idle"
        elif stats["failed_calls"] == 0:
            health_status = "healthy"
        elif stats["successful_calls"] / stats["total_calls"] > 0.8:
            health_status = "mostly_healthy"
        elif stats["successful_calls"] / stats["total_calls"] > 0.5:
            health_status = "degraded"
        else:
            health_status = "unhealthy"

        circuit_breaker_info = {}
        if component in self.circuit_breakers:
            breaker = self.circuit_breakers[component]
            circuit_breaker_info = {
                "state": breaker.state.value,
                "failure_count": breaker.failure_count,
                "failure_threshold": breaker.failure_threshold,
                "recovery_timeout": breaker.recovery_timeout,
            }

        return {
            "component": component,
            "status": health_status,
            "stats": stats,
            "circuit_breaker": circuit_breaker_info,
            "last_updated": datetime.now().isoformat(),
        }

    def cleanup_stale_data(self) -> dict[str, int]:
        """Clean up stale error data and reset component stats."""
        cleaned_records = 0
        cutoff_time = datetime.now() - timedelta(days=7)  # Clean data older than 7 days

        # Clean recovery history
        original_count = len(self.recovery_manager.recovery_history)
        self.recovery_manager.recovery_history = [
            record
            for record in self.recovery_manager.recovery_history
            if record["timestamp"] > cutoff_time
        ]
        cleaned_records += original_count - len(self.recovery_manager.recovery_history)

        # Clean error reporter history
        cleaned_records += self.error_reporter.cleanup_stale_data()

        get_logger(__name__).info(f"Cleaned up {cleaned_records} stale records")

        return {"cleaned_records": cleaned_records}

    def reset_component(self, component: str) -> bool:
        """Reset error handling state for a specific component."""
        try:
            if component in self._component_stats:
                self._component_stats[component] = {
                    "total_calls": 0,
                    "successful_calls": 0,
                    "failed_calls": 0,
                    "last_call_time": None,
                    "circuit_breaker_trips": 0,
                    "retry_attempts": 0,
                }

            if component in self.circuit_breakers:
                self.circuit_breakers[component] = CircuitBreaker()

            get_logger(__name__).info(f"Reset error handling state for component: {component}")
            return True

        except Exception as e:
            get_logger(__name__).error(f"Failed to reset component {component}: {e}")
            return False


class RecoveryManager:
    """Manages error recovery strategies with circuit breaker integration."""

    def __init__(self):
        self.strategies: list[RecoveryStrategy] = []
        self.recovery_history: list[dict[str, Any]] = []

    def add_strategy(self, strategy: RecoveryStrategy):
        """Add a recovery strategy."""
        self.strategies.append(strategy)
        get_logger(__name__).info(f"Added recovery strategy: {strategy.name}")

    def attempt_recovery(self, error_context: dict[str, Any]) -> bool:
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

                get_logger(__name__).info(f"Attempting recovery with strategy: {strategy.name}")
                success = strategy.execute(error_context)

                if success:
                    recovery_attempt["successful_strategy"] = strategy.name
                    recovery_attempt["recovery_success"] = True
                    get_logger(__name__).info(
                        f"Recovery successful using strategy: {strategy.name}"
                    )
                    break
                else:
                    get_logger(__name__).warning(f"Recovery failed with strategy: {strategy.name}")

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


class ErrorReporter:
    """Reports errors and manages error history."""

    def __init__(self):
        self.error_history: list[dict[str, Any]] = []

    def report_error(self, error_context: dict[str, Any]):
        """Report an error to the error tracking system."""
        error_record = {
            "timestamp": datetime.now(),
            "error_context": error_context,
            "reported": True,
        }
        self.error_history.append(error_record)

        get_logger(__name__).error(
            f"Error reported: {error_context.get('operation', 'unknown')} "
            f"failed with {error_context.get('error_type', 'UnknownError')}"
        )

    def cleanup_stale_data(self) -> int:
        """Clean up stale error data."""
        cutoff_time = datetime.now() - timedelta(days=7)
        original_count = len(self.error_history)
        self.error_history = [
            record for record in self.error_history if record["timestamp"] > cutoff_time
        ]
        return original_count - len(self.error_history)


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class RetryHandler:
    """Retry handler for failed operations."""

    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def execute_with_retry(self, operation: Callable, *args, **kwargs):
        """Execute operation with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return operation(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = self.backoff_factor * (2**attempt)
                    get_logger(__name__).warning(
                        f"Operation failed, retrying in {wait_time}s (attempt {attempt + 1}/{self.max_retries + 1})"
                    )
                    time.sleep(wait_time)
                else:
                    get_logger(__name__).error(
                        f"Operation failed after {self.max_retries + 1} attempts"
                    )

        raise last_exception


class CircuitBreaker:
    """Circuit breaker for fault tolerance."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, operation: Callable, *args, **kwargs):
        """Execute operation through circuit breaker."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

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
        return (datetime.now() - self.last_failure_time).total_seconds() >= self.recovery_timeout

    def _on_success(self):
        """Handle successful operation."""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            get_logger(__name__).info("Circuit breaker reset to CLOSED state")

    def _on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            get_logger(__name__).warning(
                f"Circuit breaker opened after {self.failure_count} failures"
            )


def handle_errors(operation: Callable, error_handler: Callable | None = None):
    """Decorator for error handling."""

    def wrapper(*args, **kwargs):
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            get_logger(__name__).error(f"Error in operation {operation.__name__}: {str(e)}")
            if error_handler:
                return error_handler(e, *args, **kwargs)
            else:
                raise e

    return wrapper


class CoordinationServiceRestartStrategy(RecoveryStrategy):
    """Strategy for restarting coordination services."""

    def __init__(self, service_manager: Callable | None = None):
        super().__init__("coordination_restart", "Restart coordination services")
        self.service_manager = service_manager or self._default_restart
        self.last_restart = None
        self.restart_cooldown = timedelta(minutes=5)

    def execute(self, error_context: dict[str, Any]) -> bool:
        """Execute service restart."""
        if self.last_restart and datetime.now() - self.last_restart < self.restart_cooldown:
            get_logger(__name__).warning("Service restart on cooldown")
            return False

        try:
            get_logger(__name__).info("Restarting coordination service components")
            success = self.service_manager()
            if success:
                self.last_restart = datetime.now()
            return success
        except Exception as e:
            get_logger(__name__).error(f"Service restart failed: {e}")
            return False

    def can_recover(self, error_context: dict[str, Any]) -> bool:
        """Check if service restart is appropriate."""
        return (
            "coordination" in error_context.get("component", "").lower()
            or "communication" in error_context.get("component", "").lower()
            or error_context.get("error_type")
            in ["ConnectionError", "TimeoutError", "ServiceUnavailableError"]
        )

    def _default_restart(self) -> bool:
        """Default restart implementation."""
        get_logger(__name__).info("Default coordination service restart")
        return True


class CoordinationConfigResetStrategy(RecoveryStrategy):
    """Strategy for resetting coordination configuration."""

    def __init__(self, config_reset_func: Callable | None = None):
        super().__init__("coordination_config_reset", "Reset coordination configuration")
        self.config_reset_func = config_reset_func or self._default_reset

    def execute(self, error_context: dict[str, Any]) -> bool:
        """Execute configuration reset."""
        try:
            get_logger(__name__).info("Resetting coordination configuration")
            return self.config_reset_func()
        except Exception as e:
            get_logger(__name__).error(f"Configuration reset failed: {e}")
            return False

    def can_recover(self, error_context: dict[str, Any]) -> bool:
        """Check if configuration reset is appropriate."""
        return "config" in error_context.get("operation", "").lower() or error_context.get(
            "error_type"
        ) in ["ConfigurationError", "ValidationError"]

    def _default_reset(self) -> bool:
        """Default configuration reset implementation."""
        get_logger(__name__).info("Default coordination configuration reset")
        return True


class CoordinationErrorHandler:
    """Main error handler for coordination and communication systems.

    This class provides a comprehensive facade over the modular error handling
    system, achieving V2 compliance through component orchestration and
    circuit breaker patterns.
    """

    def __init__(self):
        """Initialize the coordination error handler."""
        self.orchestrator = ErrorHandlingOrchestrator()
        self.recovery_manager = self.orchestrator.recovery_manager
        self.error_reporter = self.orchestrator.error_reporter

        # Register coordination-specific recovery strategies
        self._register_coordination_strategies()

        get_logger(__name__).info("CoordinationErrorHandler initialized with modular architecture")

    def _register_coordination_strategies(self):
        """Register coordination-specific recovery strategies."""
        # Add built-in strategies
        self.recovery_manager.add_strategy(CoordinationServiceRestartStrategy())
        self.recovery_manager.add_strategy(CoordinationConfigResetStrategy())

    def execute_with_error_handling(
        self,
        operation: Callable[[], T],
        operation_name: str = "operation",
        component: str = "coordination",
        use_retry: bool = True,
        use_circuit_breaker: bool = True,
        use_recovery: bool = True,
    ) -> T:
        """Execute operation with comprehensive error handling.

        Delegates to the orchestrator for complete error management.
        """
        return self.orchestrator.execute_with_comprehensive_error_handling(
            operation,
            operation_name,
            component,
            use_retry=use_retry,
            use_circuit_breaker=use_circuit_breaker,
            use_recovery=use_recovery,
        )

    def register_circuit_breaker(
        self, component: str, failure_threshold: int = 5, recovery_timeout: float = 60.0
    ) -> None:
        """Register a circuit breaker for a component."""
        config = CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            name=component,
        )
        self.orchestrator.register_circuit_breaker(component, config)

    def register_retry_mechanism(
        self,
        component: str,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
    ) -> None:
        """Register a retry mechanism for a component."""
        config = RetryConfig(max_attempts=max_attempts, base_delay=base_delay, max_delay=max_delay)
        self.orchestrator.register_retry_mechanism(component, config)

    def get_error_report(self) -> dict[str, Any]:
        """Generate comprehensive error report."""
        return self.orchestrator.get_system_health_report()

    def get_system_health_report(self) -> dict[str, Any]:
        """Get comprehensive system health report."""
        return self.orchestrator.get_system_health_report()

    def add_recovery_strategy(self, strategy: RecoveryStrategy):
        """Add a custom recovery strategy."""
        self.recovery_manager.add_strategy(strategy)

    def get_component_status(self, component: str) -> dict[str, Any]:
        """Get detailed status for a specific component."""
        return self.orchestrator.get_component_status(component)

    def cleanup_stale_data(self) -> dict[str, int]:
        """Clean up stale error data and logs."""
        return self.orchestrator.cleanup_stale_data()

    def reset_component(self, component: str) -> bool:
        """Reset error handling state for a specific component."""
        return self.orchestrator.reset_component(component)


# Global coordination error handler instance
coordination_handler = CoordinationErrorHandler()


def handle_coordination_errors(
    component: str = "coordination",
    use_retry: bool = True,
    use_circuit_breaker: bool = True,
    use_recovery: bool = True,
):
    """Decorator for coordination-specific error handling.

    Provides comprehensive error management for coordination operations.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            operation_name = f"{func.__module__}.{func.__name__}"

            def operation():
                return func(*args, **kwargs)

            return coordination_handler.execute_with_error_handling(
                operation,
                operation_name,
                component,
                use_retry,
                use_circuit_breaker,
                use_recovery,
            )

        return wrapper

    return decorator


# Legacy alias for backward compatibility
def handle_errors(
    component: str = "coordination",
    use_retry: bool = True,
    use_circuit_breaker: bool = True,
):
    """Legacy decorator for backward compatibility."""
    return handle_coordination_errors(component, use_retry, use_circuit_breaker, True)
