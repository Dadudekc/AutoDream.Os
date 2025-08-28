from __future__ import annotations

"""Assignment logic using pluggable scoring strategies."""

from typing import Any, Dict, Tuple

from ..contract_models import Contract
from .scoring import ScoringStrategy, CapabilityScoringStrategy


class AssignmentOptimizer:
    """Selects the best agent for a contract."""

    def __init__(self, scorer: ScoringStrategy | None = None) -> None:
        self.scorer = scorer or CapabilityScoringStrategy()

    def choose_agent(
        self, contract: Contract, agents: Dict[str, dict[str, Any]]
    ) -> Tuple[str | None, float]:
        """Return the agent ID and score for the best candidate."""
        best_id: str | None = None
        best_score = -1.0
        for agent_id, info in agents.items():
            score = self.scorer.score(contract, info)
            if score > best_score:
                best_id, best_score = agent_id, score
        return best_id, max(best_score, 0.0)

    def score(self, contract: Contract, agent_info: dict[str, Any]) -> float:
        """Convenience wrapper around the underlying scorer."""
        return self.scorer.score(contract, agent_info)


__all__ = ["AssignmentOptimizer"]
