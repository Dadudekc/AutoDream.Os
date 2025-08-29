from typing import Protocol, Any

from ..contract_models import Contract
from __future__ import annotations


"""Scoring algorithms for contract assignment.

This module exposes a simple interface for computing a score
between a contract and an agent. Alternative strategies can
implement the :class:`ScoringStrategy` protocol to plug in
custom optimisation logic.
"""




class ScoringStrategy(Protocol):
    """Protocol for scoring strategies."""

    def score(self, contract: Contract, agent_info: dict[str, Any]) -> float:
        """Return a confidence score for ``agent_info`` handling ``contract``.

        Implementations should normalise scores to the range ``0.0``-``1.0``.
        """


class CapabilityScoringStrategy:
    """Default scoring based on capability overlap."""

    def score(self, contract: Contract, agent_info: dict[str, Any]) -> float:  # type: ignore[override]
        required = set(contract.required_capabilities)
        available = set(agent_info.get("capabilities", []))
        if not required:
            return 1.0
        return len(required & available) / len(required)


__all__ = ["ScoringStrategy", "CapabilityScoringStrategy"]
