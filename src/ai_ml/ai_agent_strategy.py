"""Strategy construction tools for AI agent planning."""
from dataclasses import dataclass
from typing import List

from .ai_agent_planner_core import Plan


@dataclass
class Strategy:
    """Concrete strategy derived from a planning phase."""
    steps: List[str]


class StrategyBuilder:
    """Builds executable strategies from plans."""

    def build(self, plan: Plan) -> Strategy:
        """Convert a plan into an executable strategy."""
        strategy_steps = [f"Implement step: {step}" for step in plan.steps]
        return Strategy(steps=strategy_steps)
