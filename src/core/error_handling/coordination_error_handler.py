#!/usr/bin/env python3
"""
Coordination & Communication Error Handler - Agent Cellphone V2
============================================================

Streamlined error handler leveraging modular components for V2 compliance.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from typing import Any, Callable, Dict, List, Optional, TypeVar

from .orchestrator import ErrorHandlingOrchestrator, handle_operation, get_health_report
from .error_models import ErrorContext, ErrorSeverity, CircuitBreakerConfig, RetryConfig
from .error_recovery import ErrorRecoveryManager, RecoveryStrategy
from .error_reporting import ErrorReporter

# Type variable for generic return types
T = TypeVar('T')

logger = logging.getLogger(__name__)


class CoordinationErrorHandler:
    """
    Main error handler for coordination and communication systems.

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

        logger.info("CoordinationErrorHandler initialized with modular architecture")

    def _register_coordination_strategies(self):
        """Register coordination-specific recovery strategies."""
        # Service restart strategy for coordination components
        def restart_coordination_service():
            """Restart coordination service components."""
            logger.info("Restarting coordination service components")
            # Implementation would restart specific coordination services
            return True

        restart_strategy = RecoveryStrategy("coordination_restart", "Restart coordination services")
        self.recovery_manager.add_strategy(restart_strategy)

        # Configuration reset strategy for coordination
        def reset_coordination_config():
            """Reset coordination configuration to defaults."""
            logger.info("Resetting coordination configuration")
            # Implementation would reset coordination-specific config
            return True

        config_strategy = RecoveryStrategy("coordination_config_reset", "Reset coordination configuration")
        self.recovery_manager.add_strategy(config_strategy)

    def execute_with_error_handling(self, operation: Callable[[], T],
                                   operation_name: str = "operation",
                                   component: str = "coordination",
                                   use_retry: bool = True,
                                   use_circuit_breaker: bool = True,
                                   use_recovery: bool = True) -> T:
        """
        Execute operation with comprehensive error handling.

        Delegates to the orchestrator for complete error management.
        """
        return self.orchestrator.execute_with_comprehensive_error_handling(
            operation, operation_name, component,
            use_retry=use_retry,
            use_circuit_breaker=use_circuit_breaker,
            use_recovery=use_recovery
        )

    def register_circuit_breaker(self, component: str,
                                failure_threshold: int = 5,
                                recovery_timeout: float = 60.0) -> None:
        """Register a circuit breaker for a component."""
        config = CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            name=component
        )
        self.orchestrator.register_circuit_breaker(component, config)

    def register_retry_mechanism(self, component: str,
                                max_attempts: int = 3,
                                base_delay: float = 1.0,
                                max_delay: float = 60.0) -> None:
        """Register a retry mechanism for a component."""
        config = RetryConfig(
            max_attempts=max_attempts,
            base_delay=base_delay,
            max_delay=max_delay
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


def handle_coordination_errors(component: str = "coordination",
                              use_retry: bool = True,
                              use_circuit_breaker: bool = True,
                              use_recovery: bool = True):
    """
    Decorator for coordination-specific error handling.

    Provides comprehensive error management for coordination operations.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            operation_name = f"{func.__module__}.{func.__name__}"

            def operation():
                return func(*args, **kwargs)

            return coordination_handler.execute_with_error_handling(
                operation, operation_name, component,
                use_retry, use_circuit_breaker, use_recovery
            )
        return wrapper
    return decorator


# Legacy alias for backward compatibility
def handle_errors(component: str = "coordination", use_retry: bool = True,
                  use_circuit_breaker: bool = True):
    """Legacy decorator for backward compatibility."""
    return handle_coordination_errors(component, use_retry, use_circuit_breaker, True)
