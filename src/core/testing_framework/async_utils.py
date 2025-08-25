#!/usr/bin/env python3
"""Asynchronous utility helpers for the testing framework."""

from __future__ import annotations

import logging
from typing import Awaitable, Callable


async def run_phase(
    phase: Callable[[], Awaitable[bool]],
    name: str,
    logger: logging.Logger,
    logs: list[str],
    *,
    suppress_exceptions: bool = False,
) -> bool:
    """Execute a test phase coroutine with consistent logging.

    Args:
        phase: Coroutine function representing the phase.
        name: Human readable phase name.
        logger: Logger for emitting messages.
        logs: List to append textual logs to.
        suppress_exceptions: If True, swallow exceptions and report failure.

    Returns:
        Whether the phase succeeded.
    """
    try:
        result = await phase()
        if not result and not suppress_exceptions:
            raise RuntimeError(f"{name} phase failed")
        return result
    except Exception as exc:  # pragma: no cover - defensive branch
        message = f"{name.capitalize()} failed: {exc}"
        logs.append(message)
        logger.error(message)
        if not suppress_exceptions:
            raise
        return False
