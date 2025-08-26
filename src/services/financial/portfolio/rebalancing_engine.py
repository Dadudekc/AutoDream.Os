"""Rebalancing engine for managing asset weights and history.

Single Responsibility: Track portfolio weights and coordinate with rebalancing modules.
Follows V2 coding standards: Clean OOP design, SRP compliance, focused functionality.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from .rebalancing import PortfolioRebalancing
from .rebalancing_core import RebalancingPlan


@dataclass
class WeightSnapshot:
    """Snapshot of asset weights at a specific time."""

    timestamp: datetime
    weights: Dict[str, float]


class RebalancingEngine:
    """High level engine coordinating weight tracking and rebalancing operations."""

    def __init__(self, threshold: float = 0.05, max_history: int = 100) -> None:
        self.logger = self._setup_logging()
        self.threshold = threshold
        self.max_history = max_history
        self.current_weights: Dict[str, float] = {}
        self.weight_history: List[WeightSnapshot] = []
        self.rebalancer = PortfolioRebalancing()
        self.logger.info(
            "RebalancingEngine initialized with threshold %.2f", self.threshold
        )

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the engine."""
        logger = logging.getLogger("RebalancingEngine")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    # ------------------------------------------------------------------
    def update_weights(self, weights: Dict[str, float], timestamp: Optional[datetime] = None) -> None:
        """Update current asset weights and record a snapshot."""
        self.current_weights = weights.copy()
        snapshot = WeightSnapshot(
            timestamp=timestamp or datetime.now(), weights=self.current_weights.copy()
        )
        self.weight_history.append(snapshot)
        if len(self.weight_history) > self.max_history:
            self.weight_history = self.weight_history[-self.max_history :]
        self.logger.debug("Updated weights: %s", self.current_weights)

    def generate_plan(
        self,
        target_weights: Dict[str, float],
        prices: Optional[Dict[str, float]] = None,
    ) -> Optional[RebalancingPlan]:
        """Generate a rebalancing plan via the orchestrator."""
        if not self.current_weights:
            self.logger.warning("Current weights are empty; cannot generate plan")
            return None
        return self.rebalancer.create_rebalancing_plan(
            self.current_weights, target_weights, current_prices=prices
        )

    def execute_plan(self, plan: RebalancingPlan) -> bool:
        """Execute a previously generated plan."""
        return self.rebalancer.execute_rebalancing_plan(plan)

    def get_weight_history(self, limit: int = 10) -> List[WeightSnapshot]:
        """Return recent weight snapshots."""
        return self.weight_history[-limit:] if limit > 0 else self.weight_history
