#!/usr/bin/env python3
"""
Error Handling Orchestrator - Agent Cellphone V2
==========================================

Coordinates all error handling components for comprehensive error management.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""



logger = logging.getLogger(__name__)


class ErrorHandlingOrchestrator:
    """Orchestrates comprehensive error handling across the system."""

    def __init__(self):
        """Initialize the error handling orchestrator."""
        self.retry_mechanisms: Dict[str, RetryMechanism] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.error_history: List[ErrorContext] = []
        self.recovery_manager = ErrorRecoveryManager()
        self.error_reporter = ErrorReporter()

        # Initialize default configurations
        self._setup_default_configurations()

        get_logger(__name__).info("ErrorHandlingOrchestrator initialized successfully")

    def _setup_default_configurations(self):
        """Set up default configurations for common components."""
        # Default retry configurations
        default_retry_config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=60.0,
            backoff_factor=2.0,
            jitter=True,
        )

        # Default circuit breaker configurations
        default_circuit_config = CircuitBreakerConfig(
            failure_threshold=5, recovery_timeout=60, name="default"
        )

        # Register default configurations
        self.register_retry_mechanism("default", default_retry_config)
        self.register_circuit_breaker("default", default_circuit_config)

        # Register common component configurations
        self.register_retry_mechanism("messaging", default_retry_config)
        self.register_retry_mechanism("coordination", default_retry_config)
        self.register_retry_mechanism("validation", default_retry_config)

        self.register_circuit_breaker("messaging", default_circuit_config)
        self.register_circuit_breaker("coordination", default_circuit_config)
        self.register_circuit_breaker("validation", default_circuit_config)

    def register_retry_mechanism(self, component: str, config: RetryConfig):
        """Register a retry mechanism for a component."""
        self.retry_mechanisms[component] = RetryMechanism(config)
        get_logger(__name__).info(f"Registered retry mechanism for component: {component}")

    def register_circuit_breaker(self, component: str, config: CircuitBreakerConfig):
        """Register a circuit breaker for a component."""
        self.circuit_breakers[component] = CircuitBreaker(config)
        get_logger(__name__).info(f"Registered circuit breaker for component: {component}")

    def execute_with_comprehensive_error_handling(
        self,
        operation: Callable,
        operation_name: str = "operation",
        component: str = "unknown",
        use_retry: bool = True,
        use_circuit_breaker: bool = True,
        use_recovery: bool = True,
    ) -> Any:
        """
        Execute operation with comprehensive error handling.

        This method orchestrates retry mechanisms, circuit breakers,
        error recovery, and reporting for complete error management.
        """
        start_time = datetime.now()

        try:
            # Execute with circuit breaker and retry if enabled
            if use_circuit_breaker and component in self.circuit_breakers:
                result = self.circuit_breakers[component].call(
                    lambda: self._execute_with_retry(
                        operation, operation_name, component, use_retry
                    ),
                    operation_name,
                )
            else:
                result = self._execute_with_retry(
                    operation, operation_name, component, use_retry
                )

            # Log successful execution
            execution_time = (datetime.now() - start_time).total_seconds()
            get_logger(__name__).info(
                f"✅ Operation '{operation_name}' completed successfully in {execution_time:.2f}s"
            )

            return result

        except Exception as e:
            # Create comprehensive error context
            error_context = ErrorContext(
                operation=operation_name,
                component=component,
                timestamp=datetime.now(),
                severity=self._determine_severity(e, component),
                details={
                    "exception": str(e),
                    "exception_type": type(e).__name__,
                    "execution_time": (datetime.now() - start_time).total_seconds(),
                },
            )

            # Store error in history
            self.error_history.append(error_context)

            # Report error
            self.error_reporter.report_error(error_context)

            # Attempt recovery if enabled
            if use_recovery:
                recovery_success = self.recovery_manager.attempt_recovery(error_context)
                if recovery_success:
                    get_logger(__name__).info(
                        f"🔄 Recovery successful for {operation_name}, retrying..."
                    )
                    try:
                        # Retry operation once after successful recovery
                        return operation()
                    except Exception as recovery_retry_error:
                        get_logger(__name__).error(
                            f"❌ Operation failed even after recovery: {recovery_retry_error}"
                        )
                        error_context.details["recovery_retry_failed"] = str(
                            recovery_retry_error
                        )
                        raise recovery_retry_error

            # Log comprehensive error information
            get_logger(__name__).error(
                f"❌ Operation '{operation_name}' failed in component '{component}': {e} "
                f"(Severity: {error_context.severity.value})"
            )

            raise e

    def _execute_with_retry(
        self, operation: Callable, operation_name: str, component: str, use_retry: bool
    ) -> Any:
        """Execute operation with retry if enabled."""
        if use_retry and component in self.retry_mechanisms:
            return self.retry_mechanisms[component].execute_with_retry(
                operation, operation_name
            )
        else:
            return operation()

    def _determine_severity(
        self, exception: Exception, component: str
    ) -> ErrorSeverity:
        """Determine error severity based on exception and component."""
        exception_type = type(exception).__name__

        # Critical errors
        if any(
            critical in exception_type.lower()
            for critical in ["connectionerror", "timeouterror", "configurationerror"]
        ):
            return ErrorSeverity.CRITICAL

        # High severity errors
        if any(
            high in exception_type.lower()
            for high in ["valueerror", "keyerror", "attributeerror", "ioerror"]
        ):
            return ErrorSeverity.HIGH

        # Medium severity for component-specific errors
        if "validation" in component.lower() and "validation" in str(exception).lower():
            return ErrorSeverity.MEDIUM

        # Default to medium severity
        return ErrorSeverity.MEDIUM

    def get_system_health_report(self) -> Dict[str, Any]:
        """Get comprehensive system health report."""
        return {
            "timestamp": datetime.now().isoformat(),
            "error_handling_status": "ACTIVE",
            "components_monitored": {
                "retry_mechanisms": list(self.retry_mechanisms.keys()),
                "circuit_breakers": list(self.circuit_breakers.keys()),
                "total_components": len(
                    set(self.retry_mechanisms.keys())
                    | set(self.circuit_breakers.keys())
                ),
            },
            "error_statistics": {
                "total_errors": len(self.error_history),
                "errors_last_24h": len(
                    [
                        e
                        for e in self.error_history
                        if (datetime.now() - e.timestamp).total_seconds() < 86400
                    ]
                ),
                "severity_breakdown": self._get_severity_breakdown(),
            },
            "circuit_breaker_status": {
                component: cb.get_status()
                for component, cb in self.circuit_breakers.items()
            },
            "recovery_statistics": self.recovery_manager.get_recovery_statistics(),
            "error_report": self.error_reporter.generate_report(),
        }

    def _get_severity_breakdown(self) -> Dict[str, int]:
        """Get error severity breakdown."""
        breakdown = {}
        for error in self.error_history:
            severity = error.severity.value
            breakdown[severity] = breakdown.get(severity, 0) + 1
        return breakdown

    def cleanup_stale_data(self) -> Dict[str, int]:
        """Clean up stale error data and logs."""
        cleaned = {}

        # Clean up old error history (keep last 1000 errors)
        if len(self.error_history) > 1000:
            removed = len(self.error_history) - 1000
            self.error_history = self.error_history[-1000:]
            cleaned["error_history"] = removed

        # Clean up error reporter logs
        cleaned["error_logs"] = self.error_reporter.cleanup_old_logs()

        get_logger(__name__).info(f"Cleaned up stale data: {cleaned}")
        return cleaned

    def reset_component(self, component: str) -> bool:
        """Reset error handling state for a specific component."""
        success = True

        # Reset circuit breaker if it exists
        if component in self.circuit_breakers:
            try:
                # Create new circuit breaker instance
                config = self.circuit_breakers[component].config
                self.circuit_breakers[component] = CircuitBreaker(config)
                get_logger(__name__).info(f"Reset circuit breaker for component: {component}")
            except Exception as e:
                get_logger(__name__).error(f"Failed to reset circuit breaker for {component}: {e}")
                success = False

        # Reset retry mechanism if it exists
        if component in self.retry_mechanisms:
            try:
                # Retry mechanisms don't need explicit reset as they're stateless
                get_logger(__name__).info(f"Retry mechanism ready for component: {component}")
            except Exception as e:
                get_logger(__name__).error(f"Error with retry mechanism for {component}: {e}")
                success = False

        return success

    def get_component_status(self, component: str) -> Dict[str, Any]:
        """Get detailed status for a specific component."""
        status = {
            "component": component,
            "timestamp": datetime.now().isoformat(),
            "retry_mechanism": component in self.retry_mechanisms,
            "circuit_breaker": component in self.circuit_breakers,
        }

        if component in self.circuit_breakers:
            status["circuit_breaker_status"] = self.circuit_breakers[
                component
            ].get_status()

        # Get recent errors for this component
        recent_errors = [
            {
                "operation": error.operation,
                "severity": error.severity.value,
                "timestamp": error.timestamp.isoformat(),
                "details": error.details,
            }
            for error in self.error_history[-50:]  # Last 50 errors
            if error.component == component
        ]

        status["recent_errors"] = recent_errors[-10:]  # Last 10 errors
        status["error_count_24h"] = len(
            [
                e
                for e in recent_errors
                if (
                    datetime.now() - datetime.fromisoformat(e["timestamp"])
                ).total_seconds()
                < 86400
            ]
        )

        return status


# Global orchestrator instance
error_orchestrator = ErrorHandlingOrchestrator()


def handle_operation(
    operation: Callable,
    operation_name: str = "operation",
    component: str = "unknown",
    **kwargs,
) -> Any:
    """Convenience function for comprehensive error handling."""
    return error_orchestrator.execute_with_comprehensive_error_handling(
        operation, operation_name, component, **kwargs
    )


def get_health_report() -> Dict[str, Any]:
    """Convenience function to get system health report."""
    return error_orchestrator.get_system_health_report()
