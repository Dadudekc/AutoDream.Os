"""Profiling utilities for performance measurement.

This module provides lightweight helpers for measuring execution time of code
blocks. It enables consistent profiling across the codebase without duplicating
timing logic in individual services.
"""

import time
from contextlib import contextmanager
from typing import Callable, Iterator

__all__ = ["time_block"]


@contextmanager
def time_block() -> Iterator[Callable[[], float]]:
    """Measure the elapsed time of a code block in milliseconds.

    Usage::

        with time_block() as elapsed:
            ...  # code to measure
        duration_ms = elapsed()
    """

    start = time.time()

    def _elapsed() -> float:
        return (time.time() - start) * 1000

    yield _elapsed
