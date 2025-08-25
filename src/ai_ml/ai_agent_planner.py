"""Orchestrator for AI agent planning workflow."""
from .ai_agent_planner_core import PlannerCore, Plan
from .ai_agent_strategy import StrategyBuilder, Strategy
from .ai_agent_execution import ExecutionCoordinator, ExecutionResult


class AIAgentPlanner:
    """Coordinates planning, strategy, and execution for an AI agent."""

    def __init__(self) -> None:
        self.core = PlannerCore()
        self.strategy_builder = StrategyBuilder()
        self.executor = ExecutionCoordinator()

    def run(self, goal: str) -> ExecutionResult:
        """Run the full planning workflow for the provided goal."""
        plan: Plan = self.core.create_plan(goal)
        strategy: Strategy = self.strategy_builder.build(plan)
        return self.executor.execute(strategy)


__all__ = ["AIAgentPlanner"]
