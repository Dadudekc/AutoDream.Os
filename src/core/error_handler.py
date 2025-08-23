#!/usr/bin/env python3
"""
Error Handler - Agent Cellphone V2
==================================

Automatic fault tolerance system with circuit breaker pattern and recovery strategies.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import threading
import logging
from typing import Dict, List, Optional, Any, Callable, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum
from functools import wraps

# Type variable for return values
T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states"""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


class ErrorSeverity(Enum):
    """Error severity levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ErrorInfo:
    """Error information and metadata"""

    error_id: str
    component_id: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    timestamp: float
    retry_count: int = 0
    is_recovered: bool = False
    recovery_strategy: Optional[str] = None


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for fault tolerance
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: type = Exception,
    ):
        self.logger = logging.getLogger(f"{__name__}.CircuitBreaker")
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.success_count = 0

        self.lock = threading.RLock()

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._set_half_open()
            else:
                raise Exception(f"Circuit breaker is OPEN for {func.__name__}")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _set_half_open(self):
        """Set circuit to half-open state for testing"""
        with self.lock:
            self.state = CircuitState.HALF_OPEN
            self.logger.info("Circuit breaker set to HALF_OPEN")

    def _on_success(self):
        """Handle successful operation"""
        with self.lock:
            self.failure_count = 0
            self.success_count += 1

            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.logger.info("Circuit breaker reset to CLOSED")

    def _on_failure(self):
        """Handle operation failure"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                self.logger.warning(
                    f"Circuit breaker opened after {self.failure_count} failures"
                )

    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state"""
        with self.lock:
            return {
                "state": self.state.value,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "last_failure_time": self.last_failure_time,
                "failure_threshold": self.failure_threshold,
                "recovery_timeout": self.recovery_timeout,
            }


class RetryStrategy:
    """
    Configurable retry strategy with exponential backoff
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
    ):
        self.logger = logging.getLogger(f"{__name__}.RetryStrategy")
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base

    def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with retry logic"""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}"
                    )
                    time.sleep(delay)
                else:
                    self.logger.error(f"All {self.max_retries + 1} attempts failed")

        raise last_exception

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt"""
        delay = self.base_delay * (self.exponential_base**attempt)
        return min(delay, self.max_delay)


class ErrorRecoveryStrategy:
    """
    Error recovery strategy implementation
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ErrorRecoveryStrategy")
        self.recovery_strategies: Dict[str, Callable] = {}
        self.default_strategy: Optional[Callable] = None

    def register_strategy(self, error_type: str, strategy: Callable):
        """Register a recovery strategy for an error type"""
        self.recovery_strategies[error_type] = strategy
        self.logger.info(f"Registered recovery strategy for {error_type}")

    def set_default_strategy(self, strategy: Callable):
        """Set default recovery strategy"""
        self.default_strategy = strategy

    def execute_recovery(self, error_info: ErrorInfo) -> bool:
        """Execute appropriate recovery strategy"""
        strategy = self.recovery_strategies.get(
            error_info.error_type, self.default_strategy
        )

        if strategy:
            try:
                success = strategy(error_info)
                if success:
                    error_info.is_recovered = True
                    error_info.recovery_strategy = strategy.__name__
                    self.logger.info(f"Recovery successful for {error_info.error_id}")
                return success
            except Exception as e:
                self.logger.error(f"Recovery strategy failed: {e}")

        return False


class ErrorHandler:
    """
    Main error handling system with automatic recovery
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ErrorHandler")
        self.errors: List[ErrorInfo] = []
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.retry_strategies: Dict[str, RetryStrategy] = {}
        self.recovery_strategy = ErrorRecoveryStrategy()

        # Error tracking
        self.error_counts: Dict[str, int] = {}
        self.recovery_counts: Dict[str, int] = {}

        # Configuration
        self.max_errors = 1000
        self.auto_recovery_enabled = True

    def create_circuit_breaker(
        self,
        component_id: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
    ) -> CircuitBreaker:
        """Create a circuit breaker for a component"""
        if component_id in self.circuit_breakers:
            raise ValueError(f"Circuit breaker already exists for {component_id}")

        circuit_breaker = CircuitBreaker(failure_threshold, recovery_timeout)
        self.circuit_breakers[component_id] = circuit_breaker

        self.logger.info(f"Created circuit breaker for {component_id}")
        return circuit_breaker

    def create_retry_strategy(
        self, component_id: str, max_retries: int = 3, base_delay: float = 1.0
    ) -> RetryStrategy:
        """Create a retry strategy for a component"""
        if component_id in self.retry_strategies:
            raise ValueError(f"Retry strategy already exists for {component_id}")

        retry_strategy = RetryStrategy(max_retries, base_delay)
        self.retry_strategies[component_id] = retry_strategy

        self.logger.info(f"Created retry strategy for {component_id}")
        return retry_strategy

    def handle_error(
        self,
        component_id: str,
        error: Exception,
        error_type: str = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    ) -> ErrorInfo:
        """Handle an error and attempt recovery"""
        error_type = error_type or type(error).__name__

        error_info = ErrorInfo(
            error_id=f"error_{int(time.time())}_{component_id}",
            component_id=component_id,
            error_type=error_type,
            error_message=str(error),
            severity=severity,
            timestamp=time.time(),
        )

        # Track error
        self.errors.append(error_info)
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

        # Limit error history
        if len(self.errors) > self.max_errors:
            self.errors = self.errors[-self.max_errors :]

        # Attempt automatic recovery
        if self.auto_recovery_enabled:
            self._attempt_recovery(error_info)

        self.logger.error(f"Error handled: {component_id} - {error_type}: {error}")
        return error_info

    def _attempt_recovery(self, error_info: ErrorInfo):
        """Attempt automatic error recovery"""
        try:
            success = self.recovery_strategy.execute_recovery(error_info)
            if success:
                self.recovery_counts[error_info.error_type] = (
                    self.recovery_counts.get(error_info.error_type, 0) + 1
                )
                self.logger.info(
                    f"Automatic recovery successful for {error_info.error_id}"
                )
            else:
                self.logger.warning(
                    f"Automatic recovery failed for {error_info.error_id}"
                )
        except Exception as e:
            self.logger.error(f"Recovery attempt failed: {e}")

    def get_error_stats(self) -> Dict[str, Any]:
        """Get error handling statistics"""
        return {
            "total_errors": len(self.errors),
            "error_counts": self.error_counts.copy(),
            "recovery_counts": self.recovery_counts.copy(),
            "recovery_rate": self._calculate_recovery_rate(),
            "circuit_breakers": {
                name: cb.get_state() for name, cb in self.circuit_breakers.items()
            },
            "recent_errors": self._get_recent_errors(10),
        }

    def _calculate_recovery_rate(self) -> float:
        """Calculate overall recovery rate"""
        total_errors = sum(self.error_counts.values())
        total_recoveries = sum(self.recovery_counts.values())

        if total_errors == 0:
            return 1.0
        return total_recoveries / total_errors

    def _get_recent_errors(self, limit: int) -> List[Dict[str, Any]]:
        """Get recent error information"""
        recent_errors = self.errors[-limit:] if self.errors else []
        return [
            {
                "error_id": error.error_id,
                "component_id": error.component_id,
                "error_type": error.error_type,
                "severity": error.severity.value,
                "timestamp": error.timestamp,
                "is_recovered": error.is_recovered,
            }
            for error in recent_errors
        ]

    def clear_errors(self, before_timestamp: Optional[float] = None):
        """Clear old errors from history"""
        if before_timestamp is None:
            before_timestamp = time.time() - 86400  # 24 hours ago

        self.errors = [
            error for error in self.errors if error.timestamp >= before_timestamp
        ]
        self.logger.info(f"Cleared errors older than {before_timestamp}")

    def get_component_errors(self, component_id: str) -> List[ErrorInfo]:
        """Get errors for a specific component"""
        return [error for error in self.errors if error.component_id == component_id]

    def is_component_healthy(self, component_id: str) -> bool:
        """Check if a component is healthy based on error history"""
        recent_errors = [
            error
            for error in self.errors
            if error.component_id == component_id
            and error.timestamp > time.time() - 300
        ]  # Last 5 minutes

        return len(recent_errors) < 3  # Consider healthy if less than 3 recent errors


# Decorator for automatic error handling
def with_error_handling(
    error_handler: ErrorHandler,
    component_id: str,
    retry: bool = True,
    circuit_breaker: bool = True,
):
    """Decorator for automatic error handling"""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                # Use circuit breaker if enabled
                if circuit_breaker and component_id in error_handler.circuit_breakers:
                    return error_handler.circuit_breakers[component_id].call(
                        func, *args, **kwargs
                    )

                # Use retry strategy if enabled
                if retry and component_id in error_handler.retry_strategies:
                    return error_handler.retry_strategies[component_id].execute(
                        func, *args, **kwargs
                    )

                # Direct execution
                return func(*args, **kwargs)

            except Exception as e:
                error_handler.handle_error(component_id, e)
                raise

        return wrapper

    return decorator
