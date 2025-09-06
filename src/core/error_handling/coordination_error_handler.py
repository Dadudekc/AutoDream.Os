#!/usr/bin/env python3
"""
Coordination & Communication Error Handler - Agent Cellphone V2
============================================================

Streamlined error handler leveraging modular components for V2 compliance.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""


# Type variable for generic return types
T = TypeVar("T")

logger = logging.getLogger(__name__)


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
        return (
            datetime.now() - self.last_failure_time
        ).total_seconds() >= self.recovery_timeout

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


def handle_errors(operation: Callable, error_handler: Optional[Callable] = None):
    """Decorator for error handling."""

    def wrapper(*args, **kwargs):
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            get_logger(__name__).error(
                f"Error in operation {operation.__name__}: {str(e)}"
            )
            if error_handler:
                return error_handler(e, *args, **kwargs)
            else:
                raise e

    return wrapper


class CoordinationErrorHandler:
    """Main error handler for coordination and communication systems.

    This class now serves as a lightweight facade over the modular error handling
    system, achieving V2 compliance through component orchestration.
    """

    def __init__(self):
        """Initialize the streamlined error handler."""
        self.orchestrator = ErrorHandlingOrchestrator()
        self.recovery_manager = self.orchestrator.recovery_manager
        self.error_reporter = self.orchestrator.error_reporter

        # Register coordination-specific recovery strategies
        self._register_coordination_strategies()

        get_logger(__name__).info(
            "CoordinationErrorHandler initialized with modular architecture"
        )

    def _register_coordination_strategies(self):
        """Register coordination-specific recovery strategies."""

        # Service restart strategy for coordination components
        def restart_coordination_service():
            """Restart coordination service components."""
            get_logger(__name__).info("Restarting coordination service components")
            # Implementation would restart specific coordination services
            return True

        restart_strategy = RecoveryStrategy(
            "coordination_restart", "Restart coordination services"
        )
        self.recovery_manager.add_strategy(restart_strategy)

        # Configuration reset strategy for coordination
        def reset_coordination_config():
            """Reset coordination configuration to defaults."""
            get_logger(__name__).info("Resetting coordination configuration")
            # Implementation would reset coordination-specific config
            return True

        config_strategy = RecoveryStrategy(
            "coordination_config_reset", "Reset coordination configuration"
        )
        self.recovery_manager.add_strategy(config_strategy)

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
        config = RetryConfig(
            max_attempts=max_attempts, base_delay=base_delay, max_delay=max_delay
        )
        self.orchestrator.register_retry_mechanism(component, config)

    def get_error_report(self) -> Dict[str, Any]:
        """Generate comprehensive error report."""
        return self.orchestrator.get_system_health_report()

    def add_recovery_strategy(self, strategy: RecoveryStrategy):
        """Add a custom recovery strategy."""
        self.recovery_manager.add_strategy(strategy)

    def get_component_status(self, component: str) -> Dict[str, Any]:
        """Get detailed status for a specific component."""
        return self.orchestrator.get_component_status(component)

    def cleanup_stale_data(self) -> Dict[str, int]:
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
