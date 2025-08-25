"""Core optimization strategies for AI agents.

This module contains the low level logic that applies registered
optimization strategies to an agent's state.  It is intentionally
lightweight and free of side effects so that higher level components
can orchestrate optimizations in a predictable manner.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict

logger = logging.getLogger(__name__)


class AIAgentOptimizerCore:
    """Apply optimization strategies to an agent state."""

    def __init__(self) -> None:
        self._strategies: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_strategy(
        self, name: str, strategy: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> None:
        """Register an optimization strategy.

        Parameters
        ----------
        name:
            Identifier for the strategy.
        strategy:
            Callable that accepts and returns a state mapping.
        """

        self._strategies[name] = strategy
        logger.debug("Registered optimization strategy: %s", name)

    def optimize(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run all registered strategies on the provided state.

        Each strategy receives the output of the previous one.  Errors are
        logged but do not interrupt the optimization chain.
        """

        for name, strategy in self._strategies.items():
            try:
                state = strategy(state)
                logger.debug("Applied strategy: %s", name)
            except Exception as exc:  # pragma: no cover - defensive programming
                logger.exception("Strategy %s failed: %s", name, exc)
        return state
