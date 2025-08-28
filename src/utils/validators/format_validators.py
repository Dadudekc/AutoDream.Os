"""Validation helpers for checking value formats such as emails and URLs."""

import logging
import re
from typing import List

logger = logging.getLogger(__name__)


class FormatValidators:
    """Collection of format validation helpers."""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email address format."""
        try:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            return bool(re.match(pattern, email))
        except Exception as e:  # pragma: no cover - defensive logging
            logger.error("Email validation error: %s", e)
            return False

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format."""
        try:
            pattern = r"^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$"
            return bool(re.match(pattern, url))
        except Exception as e:  # pragma: no cover - defensive logging
            logger.error("URL validation error: %s", e)
            return False

    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
        """Validate file extension against allowed values."""
        try:
            if not filename:
                return False
            extension = filename.lower().split(".")[-1]
            return extension in [ext.lower() for ext in allowed_extensions]
        except Exception:  # pragma: no cover - simple failure path
            return False

    @staticmethod
    def validate_pattern(text: str, pattern: str) -> bool:
        """Validate text against a regular expression pattern."""
        try:
            return bool(re.match(pattern, text))
        except Exception as e:  # pragma: no cover - defensive logging
            logger.error("Pattern validation error: %s", e)
            return False
