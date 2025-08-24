"""Gaming-oriented components for the AI Agent Framework."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .ai_agent_framework_config import logger
from .ai_agent_framework_core import (
    AgentDecision,
    AgentState,
    BehaviorTree,
    DecisionEngine,
    GameState,
    LearningExperience,
)


class AIGamingAgent:
    """AI Gaming Agent."""

    def __init__(self, name: str, agent_type: str = "general"):
        self.name = name
        self.agent_type = agent_type
        self.state = AgentState.IDLE
        self.behavior_tree: Optional[BehaviorTree] = None
        self.decision_engine: Optional[DecisionEngine] = None
        self.learning_experiences: List[LearningExperience] = []
        self.performance_metrics: Dict[str, int | float] = {
            "actions_completed": 0,
            "decisions_made": 0,
            "successful_actions": 0,
            "learning_experiences": 0,
        }

    def set_decision_engine(self, engine: DecisionEngine) -> None:
        self.decision_engine = engine

    def set_behavior_tree(self, tree: BehaviorTree) -> None:
        self.behavior_tree = tree

    def update_state(self, new_state: AgentState) -> None:
        self.state = new_state
        logger.info(f"Agent {self.name} state changed to {new_state.value}")

    def make_decision(self, game_state: GameState) -> Optional[AgentDecision]:
        if not self.decision_engine:
            return None
        decision = self.decision_engine.make_decision(self, game_state)
        if decision:
            self.performance_metrics["decisions_made"] += 1
        return decision

    def execute_behavior_tree(self, game_state: GameState) -> bool:
        if not self.behavior_tree:
            return False
        result = self.behavior_tree.execute(self, game_state)
        if result:
            self.performance_metrics["actions_completed"] += 1
            self.performance_metrics["successful_actions"] += 1
        else:
            self.performance_metrics["actions_completed"] += 1
        return result

    def add_learning_experience(self, experience: LearningExperience) -> None:
        self.learning_experiences.append(experience)
        self.performance_metrics["learning_experiences"] += 1
        if len(self.learning_experiences) > 1000:
            self.learning_experiences = self.learning_experiences[-1000:]

    def get_performance_metrics(self) -> Dict[str, Any]:
        success_rate = (
            self.performance_metrics["successful_actions"]
            / self.performance_metrics["actions_completed"]
            if self.performance_metrics["actions_completed"] > 0
            else 0
        )
        return {
            **self.performance_metrics,
            "success_rate": success_rate,
            "learning_efficiency": len(self.learning_experiences)
            / max(1, self.performance_metrics["actions_completed"]),
        }

    def learn(
        self,
        game_state: GameState,
        action: AgentDecision,
        reward: float,
        next_state: GameState,
        success: bool,
    ) -> None:
        experience = LearningExperience(
            state=game_state,
            action=action,
            reward=reward,
            next_state=next_state,
            success=success,
            action_taken=action.decision_type.value,
        )
        self.add_learning_experience(experience)

    def render(self) -> str:
        return f"Agent({self.name}, {self.agent_type}, {self.state.value})"

    def update(self, game_state: GameState) -> None:
        decision = self.make_decision(game_state)
        if decision:
            self.execute_behavior_tree(game_state)
        self.performance_metrics["actions_completed"] += 1


def create_ai_gaming_agent(name: str, agent_type: str = "general") -> AIGamingAgent:
    """Factory function to create AI gaming agent."""
    return AIGamingAgent(name, agent_type)


__all__ = [
    "AIGamingAgent",
    "create_ai_gaming_agent",
]
