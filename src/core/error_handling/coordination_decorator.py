#!/usr/bin/env python3
"""
Coordination Error Handling Decorator
======================================

Decorator for applying comprehensive error handling to coordination operations.
Extracted from coordination_error_handler.py for V2 compliance.

Author: Agent-4 (Captain) - V2 Refactoring & Autonomy Enhancement
License: MIT
"""

from collections.abc import Callable
from typing import Any


def handle_coordination_errors(
    component: str = "coordination",
    use_retry: bool = True,
    use_circuit_breaker: bool = True,
    use_recovery: bool = True,
    use_intelligence: bool = True,
) -> Callable:
    """Decorator for coordination-specific error handling.

    Provides comprehensive error management for coordination operations.

    Args:
        component: Component identifier
        use_retry: Enable retry mechanism
        use_circuit_breaker: Enable circuit breaker
        use_recovery: Enable recovery strategies
        use_intelligence: Enable intelligent error analysis

    Returns:
        Decorated function with error handling
    """

    def decorator(func: Callable) -> Callable:
        """Decorator implementation.

        Args:
            func: Function to decorate

        Returns:
            Wrapped function with error handling
        """

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper function that applies error handling.

            Args:
                *args: Positional arguments
                **kwargs: Keyword arguments

            Returns:
                Function result
            """
            # Late import to avoid circular dependency
            from .coordination_error_handler import coordination_handler_core

            operation_name = f"{func.__module__}.{func.__name__}"

            def operation() -> Any:
                """Execute the wrapped operation.

                Returns:
                    Operation result
                """
                return func(*args, **kwargs)

            return coordination_handler_core.execute_with_error_handling(
                operation,
                operation_name,
                component,
                use_retry,
                use_circuit_breaker,
                use_recovery,
                use_intelligence,
            )

        return wrapper

    return decorator
