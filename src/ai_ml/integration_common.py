"""Shared utilities for AI/ML integrations."""

from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def get_env_var(name: str, default: Optional[str] = None) -> str:
    """Retrieve an environment variable or raise a :class:`ValueError`.

    Args:
        name: Environment variable name.
        default: Optional default if the variable is not set.

    Returns:
        The value of the environment variable.

    Raises:
        ValueError: If the variable is missing and no default is provided.
    """
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"{name} not provided")
    return value
