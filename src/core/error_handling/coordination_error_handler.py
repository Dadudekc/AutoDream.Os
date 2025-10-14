#!/usr/bin/env python3
"""
Coordination & Communication Error Handler - Refactored V2
===========================================================

Intelligent error handler for coordination and communication systems.
Refactored into modular components for autonomous systems.

Architecture:
- error_classification: Error severity and categorization
- error_execution: Execution orchestration with error handling
- component_management: Component registration and status
- coordination_strategies: Coordination-specific recovery strategies
- coordination_decorator: Error handling decorator
- This file: High-level coordination facade

Author: Agent-4 (Captain) - V2 Compliance Refactoring (650 pts, ROI 15.57)
Original: Agent-3 (Infrastructure), Agent-4 (Strategic), Agent-5 (Intelligence)
License: MIT
"""

import logging
from typing import Any, TypeVar

from .component_management import component_manager
from .coordination_strategies import register_default_coordination_strategies
from .error_classification import error_classifier
from .error_execution import ErrorExecutionOrchestrator
from .recovery_strategies import RecoveryStrategy

# Type variable for generic return types
T = TypeVar("T")

logger = logging.getLogger(__name__)


class CoordinationErrorHandlerCore:
    """Intelligent error handler for coordination and communication systems.

    Provides comprehensive error management with:
    - Retry mechanisms with exponential backoff
    - Circuit breakers for fault tolerance
    - Intelligent recovery strategies
    - Error pattern analysis and prediction
    - Learning from error history

    Refactored for autonomous systems with modular V2-compliant architecture.
    """

    def __init__(self):
        """Initialize the coordination error handler."""
        # Use global component manager
        self.component_manager = component_manager

        # Create execution orchestrator with manager's components
        self.orchestrator = ErrorExecutionOrchestrator(
            circuit_breakers=self.component_manager.circuit_breakers,
            retry_mechanisms=self.component_manager.retry_mechanisms,
            recovery_strategies=self.component_manager.recovery_strategies,
            classifier=error_classifier,
        )

        # Register default coordination strategies
        register_default_coordination_strategies(self.component_manager)

        logger.info("CoordinationErrorHandlerCore initialized with V2 modular architecture")

    def execute_with_error_handling(
        self,
        operation,
        operation_name: str = "operation",
        component: str = "coordination",
        use_retry: bool = True,
        use_circuit_breaker: bool = True,
        use_recovery: bool = True,
        use_intelligence: bool = True,
    ) -> Any:
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
        return self.orchestrator.execute_with_error_handling(
            operation=operation,
            operation_name=operation_name,
            component=component,
            use_retry=use_retry,
            use_circuit_breaker=use_circuit_breaker,
            use_recovery=use_recovery,
            use_intelligence=use_intelligence,
        )

    def register_circuit_breaker(
        self, component: str, failure_threshold: int = 5, recovery_timeout: float = 60.0
    ) -> None:
        """Register a circuit breaker for a component.

        Args:
            component: Component identifier
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Timeout before attempting recovery (seconds)
        """
        self.component_manager.register_circuit_breaker(
            component, failure_threshold, recovery_timeout
        )

    def register_retry_mechanism(
        self,
        component: str,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
    ) -> None:
        """Register a retry mechanism for a component.

        Args:
            component: Component identifier
            max_attempts: Maximum retry attempts
            base_delay: Initial delay between retries
            max_delay: Maximum delay between retries
        """
        self.component_manager.register_retry_mechanism(
            component, max_attempts, base_delay, max_delay
        )

    def add_recovery_strategy(self, strategy: RecoveryStrategy) -> None:
        """Add a custom recovery strategy.

        Args:
            strategy: Recovery strategy to add
        """
        self.component_manager.add_recovery_strategy(strategy)

    def get_error_report(self) -> dict[str, Any]:
        """Generate comprehensive error report with intelligence insights.

        Returns:
            Comprehensive error and intelligence report
        """
        return self.component_manager.get_error_report()

    def get_component_status(self, component: str) -> dict[str, Any]:
        """Get detailed status for a specific component.

        Args:
            component: Component to analyze

        Returns:
            Component status including health and intelligence insights
        """
        return self.component_manager.get_component_status(component)

    def reset_component(self, component: str) -> bool:
        """Reset error handling state for a specific component.

        Args:
            component: Component to reset

        Returns:
            True if reset successful
        """
        return self.component_manager.reset_component(component)


# Global coordination error handler instance (backward compatibility)
coordination_handler_core = CoordinationErrorHandlerCore()
coordination_handler = coordination_handler_core  # Alias for backward compatibility

# Import decorator from separate module for V2 compliance
from .coordination_decorator import handle_coordination_errors  # noqa: E402, F401

__all__ = [
    "CoordinationErrorHandlerCore",
    "coordination_handler_core",
    "coordination_handler",
    "handle_coordination_errors",
]
