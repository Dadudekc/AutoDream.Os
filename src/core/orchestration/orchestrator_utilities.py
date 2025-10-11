"""
Orchestrator Utility Functions
===============================

Utility functions for orchestrator operations extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class OrchestratorUtilities:
    """Utility functions for orchestrator operations."""

    @staticmethod
    def safe_execute(
        operation: callable,
        operation_name: str,
        default_return: Any,
        logger_instance,
        emit_func,
        **kwargs,
    ) -> Any:
        """Safely execute an operation with error handling."""
        try:
            logger_instance.debug(f"Executing {operation_name}")
            result = operation(**kwargs)
            emit_func(f"{operation_name}_success", result)
            return result
        except Exception as e:
            logger_instance.error(f"Error executing {operation_name}: {e}")
            emit_func(f"{operation_name}_error", {"error": str(e)})
            return default_return

    @staticmethod
    def sanitize_config(config: dict[str, Any], logger_instance) -> dict[str, Any]:
        """Sanitize configuration values to prevent injection or invalid data."""
        sanitized = {}

        for key, value in config.items():
            # Convert to string and check for suspicious patterns
            str_value = str(value)

            # Block common injection patterns
            suspicious_patterns = ["DROP TABLE", "DELETE FROM", "rm -rf", "eval(", "exec("]

            if any(pattern.lower() in str_value.lower() for pattern in suspicious_patterns):
                logger_instance.warning(f"Suspicious config value for {key}, using safe default")
                sanitized[key] = None
            else:
                sanitized[key] = value

        return sanitized
