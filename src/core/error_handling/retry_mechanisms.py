"""
Retry Mechanisms Module
========================

Retry mechanism with exponential backoff extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from .error_handling_core import RetryConfig

logger = logging.getLogger(__name__)


class RetryMechanism:
    """Retry mechanism with exponential backoff and jitter."""

    def __init__(self, config: RetryConfig):
        """Initialize retry mechanism."""
        self.config = config

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry mechanism."""
        last_exception = None

        for attempt in range(self.config.max_attempts):
            try:
                return func(*args, **kwargs)
            except self.config.exceptions as e:
                last_exception = e

                if attempt == self.config.max_attempts - 1:
                    logger.error(
                        f"Function failed after {self.config.max_attempts} attempts",
                        exc_info=True,
                    )
                    raise e

                delay = self.config.calculate_delay(attempt)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}")

                time.sleep(delay)

        raise last_exception


def retry_on_exception(config: RetryConfig, exceptions: type[Exception] | tuple = Exception):
    """Decorator for retrying on specific exceptions."""
    mechanism = RetryMechanism(config)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            def execute():
                return func(*args, **kwargs)

            return mechanism.execute_with_retry(execute)

        return wrapper

    return decorator


def with_exponential_backoff(
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    max_attempts: int = 3,
    jitter: bool = True,
):
    """Decorator for exponential backoff retry."""
    config = RetryConfig(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        backoff_factor=backoff_factor,
        jitter=jitter,
        exceptions=Exception,
    )
    return retry_on_exception(config)
