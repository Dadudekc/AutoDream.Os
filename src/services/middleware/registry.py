from __future__ import annotations

"""Registration utilities for middleware components and chains."""

import logging
from typing import Dict, List

from .base import BaseMiddlewareComponent
from .models import MiddlewareChain

logger = logging.getLogger(__name__)


def register_middleware(
    components: Dict[str, BaseMiddlewareComponent],
    middleware: BaseMiddlewareComponent,
) -> None:
    """Register a middleware component.

    Parameters
    ----------
    components:
        Dictionary mapping component names to middleware instances.
    middleware:
        The middleware component to register.
    """
    if middleware.name in components:
        logger.warning("Middleware %s already registered, overwriting", middleware.name)
    components[middleware.name] = middleware


def create_chain(chains: List[MiddlewareChain], chain: MiddlewareChain) -> None:
    """Add a middleware chain and maintain priority ordering."""
    chains.append(chain)
    chains.sort(key=lambda c: c.priority)
