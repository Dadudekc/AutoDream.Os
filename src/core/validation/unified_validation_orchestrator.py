#!/usr/bin/env python3
"""
Unified Validation Orchestrator - V2 Compliant Module
====================================================

Validation orchestrator for the Agent Cellphone V2 system.

V2 Compliance: < 300 lines, single responsibility.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class UnifiedValidationOrchestrator:
    """Unified validation orchestrator."""

    def __init__(self):
        """Initialize validation orchestrator."""
        self.logger = logger

    def validate_hasattr(self, obj: Any, attr: str) -> bool:
        """Validate that object has attribute.

        Args:
            obj: Object to validate
            attr: Attribute name to check

        Returns:
            True if object has attribute, False otherwise
        """
        return hasattr(obj, attr)

    def validate_type(self, obj: Any, expected_type: type) -> bool:
        """Validate that object is of expected type.

        Args:
            obj: Object to validate
            expected_type: Expected type

        Returns:
            True if object is of expected type, False otherwise
        """
        return isinstance(obj, expected_type)

    def validate_not_none(self, obj: Any) -> bool:
        """Validate that object is not None.

        Args:
            obj: Object to validate

        Returns:
            True if object is not None, False otherwise
        """
        return obj is not None

    def validate_not_empty(self, obj: Any) -> bool:
        """Validate that object is not empty.

        Args:
            obj: Object to validate

        Returns:
            True if object is not empty, False otherwise
        """
        if obj is None:
            return False
        if isinstance(obj, (str, list, dict)):
            return len(obj) > 0
        return True

    def validate_range(self, value: float, min_val: float, max_val: float) -> bool:
        """Validate that value is within range.

        Args:
            value: Value to validate
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            True if value is within range, False otherwise
        """
        return min_val <= value <= max_val

    def validate_regex(self, value: str, pattern: str) -> bool:
        """Validate that value matches regex pattern.

        Args:
            value: Value to validate
            pattern: Regex pattern

        Returns:
            True if value matches pattern, False otherwise
        """
        import re

        return bool(re.match(pattern, value))

    def validate_custom(self, obj: Any, validator_func: callable) -> bool:
        """Validate using custom validator function.

        Args:
            obj: Object to validate
            validator_func: Custom validator function

        Returns:
            True if validation passes, False otherwise
        """
        try:
            return validator_func(obj)
        except Exception as e:
            self.logger.error(f"Custom validation error: {e}")
            return False


# Global instance
_unified_validator = None


def get_unified_validator() -> UnifiedValidationOrchestrator:
    """Get the global unified validator instance."""
    global _unified_validator
    if _unified_validator is None:
        _unified_validator = UnifiedValidationOrchestrator()
    return _unified_validator
