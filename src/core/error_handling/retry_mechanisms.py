#!/usr/bin/env python3
"""
Retry Mechanisms Module - Agent Cellphone V2
==========================================

Retry logic and exponential backoff implementation.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
import random
import time
from typing import Callable, Any, Optional, Union, Type
from functools import wraps
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RetryConfig:
    """Configuration for retry mechanism."""
    max_attempts: int = 3
    base_delay: float = 1.0
    backoff_factor: float = 2.0
    max_delay: float = 60.0
    jitter: bool = True


class RetryMechanism:
    """Retry mechanism with exponential backoff and jitter."""

    def __init__(self, config: RetryConfig):
        """Initialize retry mechanism."""
        self.config = config

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for the given attempt."""
        delay = self.config.base_delay * (self.config.backoff_factor**attempt)

        # Apply maximum delay limit
        delay = min(delay, self.config.max_delay)

        # Apply jitter if enabled
        if self.config.jitter:
            jitter_range = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_range, jitter_range)
            delay = max(0.1, delay)  # Minimum 100ms delay

        return delay

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry mechanism."""
        last_exception = None

        for attempt in range(self.config.max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                if attempt == self.config.max_attempts - 1:
                    # Last attempt failed
                    logger.error(
                        f"Function failed after {self.config.max_attempts} attempts",
                        exc_info=True,
                    )
                    raise e

                delay = self._calculate_delay(attempt)
                logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}"
                )

                time.sleep(delay)

        # This should never be reached, but just in case
        raise last_exception


def retry_on_exception(
    config: RetryConfig, exceptions: Union[Type[Exception], tuple] = Exception
):
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


def retry_on_failure(config: RetryConfig, failure_condition: Optional[Callable] = None):
    """Decorator for retrying based on custom failure condition."""
    mechanism = RetryMechanism(config)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            def execute():
                result = func(*args, **kwargs)
                if failure_condition and failure_condition(result):
                    raise RetryException(
                        f"Failure condition met: {failure_condition.__name__}"
                    )
                return result

            return mechanism.execute_with_retry(execute)

        return wrapper

    return decorator


class RetryException(Exception):
    """Exception raised to trigger retry."""

    pass


class ExponentialBackoff:
    """Exponential backoff calculator."""

    def __init__(
        self,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: bool = True,
    ):
        """Initialize exponential backoff calculator."""
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """Get delay for the given attempt."""
        delay = self.base_delay * (self.backoff_factor**attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            jitter_range = delay * 0.1
            delay += random.uniform(-jitter_range, jitter_range)
            delay = max(0.1, delay)

        return delay


def with_exponential_backoff(
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    max_attempts: int = 3,
    jitter: bool = True,
):
    """Decorator for functions with exponential backoff retry."""
    backoff = ExponentialBackoff(base_delay, max_delay, backoff_factor, jitter)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if attempt == max_attempts - 1:
                        raise e

                    delay = backoff.get_delay(attempt)
                    logger.warning(
                        f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}"
                    )
                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator
