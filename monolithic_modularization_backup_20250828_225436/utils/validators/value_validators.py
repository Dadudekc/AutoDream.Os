"""Validation helpers for validating values and ranges."""

import logging
from typing import Any, List, Optional, Union

logger = logging.getLogger(__name__)


class ValueValidators:
    """Collection of value validation helpers."""

    @staticmethod
    def validate_string_length(text: str, min_length: int = 0, max_length: Optional[int] = None) -> bool:
        """Validate string length constraints."""
        try:
            if not isinstance(text, str):
                return False
            if len(text) < min_length:
                return False
            if max_length is not None and len(text) > max_length:
                return False
            return True
        except Exception:  # pragma: no cover - simple failure path
            return False

    @staticmethod
    def validate_numeric_range(
        value: Union[int, float],
        min_val: Optional[Union[int, float]] = None,
        max_val: Optional[Union[int, float]] = None,
    ) -> bool:
        """Validate numeric value is within range."""
        try:
            if not isinstance(value, (int, float)):
                return False
            if min_val is not None and value < min_val:
                return False
            if max_val is not None and value > max_val:
                return False
            return True
        except Exception:  # pragma: no cover - simple failure path
            return False

    @staticmethod
    def validate_choice(value: Any, choices: List[Any]) -> bool:
        """Validate value is one of the allowed choices."""
        try:
            return value in choices
        except Exception:  # pragma: no cover - simple failure path
            return False
