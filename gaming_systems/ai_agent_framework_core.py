"""Core components for the AI Agent Framework."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .ai_agent_framework_config import logger


class AgentState(Enum):
    """Agent state enumeration."""

    IDLE = "idle"
    ACTIVE = "active"
    THINKING = "thinking"
    ACTING = "acting"
    LEARNING = "learning"
    ERROR = "error"
    COORDINATING = "coordinating"


class DecisionType(Enum):
    """Decision type enumeration."""

    MOVE = "move"
    ATTACK = "attack"
    DEFEND = "defend"
    COLLECT = "collect"
    EXPLORE = "explore"
    COORDINATE = "coordinate"
    WAIT = "wait"
    COMMUNICATE = "communicate"


class BehaviorNodeType(Enum):
    """Behavior tree node types."""

    SEQUENCE = "sequence"
    SELECTOR = "selector"
    ACTION = "action"
    CONDITION = "condition"
    DECORATOR = "decorator"


@dataclass
class GameState:
    """Game state information for AI agents."""

    player_position: tuple[float, float] = (0.0, 0.0)
    player_health: float = 100.0
    enemy_positions: List[tuple[float, float]] = field(default_factory=list)
    enemy_health: List[float] = field(default_factory=list)
    item_positions: List[tuple[float, float]] = field(default_factory=list)
    item_types: List[str] = field(default_factory=list)
    obstacles: List[tuple[float, float, float, float]] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    level: int = 1
    score: int = 0
    time_elapsed: float = 0.0
    enemies_remaining: int = 5


@dataclass
class AgentDecision:
    """AI agent decision data."""

    decision_type: DecisionType
    target_position: Optional[tuple[float, float]] = None
    target_id: Optional[str] = None
    priority: float = 1.0
    confidence: float = 1.0
    reasoning: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class LearningExperience:
    """Learning experience for AI agents."""

    state: GameState
    action: AgentDecision
    reward: float
    next_state: GameState
    success: bool
    timestamp: float = field(default_factory=time.time)
    action_taken: str = ""


class BehaviorNode(ABC):
    """Abstract base class for behavior tree nodes."""

    def __init__(self, name: str):
        self.name = name
        self.children: List["BehaviorNode"] = []
        self.parent: Optional["BehaviorNode"] = None
        self.node_type: BehaviorNodeType | None = None

    @abstractmethod
    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute the behavior node."""
        raise NotImplementedError

    def add_child(self, child: "BehaviorNode") -> None:
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: "BehaviorNode") -> None:
        if child in self.children:
            child.parent = None
            self.children.remove(child)


class ActionNode(BehaviorNode):
    """Action node for behavior trees."""

    def __init__(self, name: str, action_func: Optional[Callable] = None):
        super().__init__(name)
        self.node_type = BehaviorNodeType.ACTION
        self.action_func = action_func

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        if self.action_func:
            try:
                return self.action_func(agent, game_state)
            except Exception as e:  # pragma: no cover - defensive log
                logger.error(f"Action execution error: {e}")
                return False
        return True

    def set_action(self, action_func: Callable) -> None:
        self.action_func = action_func


class ConditionNode(BehaviorNode):
    """Condition node for behavior trees."""

    def __init__(self, name: str, condition_func: Callable):
        super().__init__(name)
        self.node_type = BehaviorNodeType.CONDITION
        self.condition_func = condition_func

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        try:
            return self.condition_func(agent, game_state)
        except Exception as e:  # pragma: no cover - defensive log
            logger.error(f"Condition check error: {e}")
            return False

    def set_condition(self, condition_func: Callable) -> None:
        self.condition_func = condition_func


class SequenceNode(BehaviorNode):
    """Sequence node for behavior trees."""

    def __init__(self, name: str):
        super().__init__(name)
        self.node_type = BehaviorNodeType.SEQUENCE

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        for child in self.children:
            if not child.execute(agent, game_state):
                return False
        return True


class SelectorNode(BehaviorNode):
    """Selector node for behavior trees."""

    def __init__(self, name: str):
        super().__init__(name)
        self.node_type = BehaviorNodeType.SELECTOR

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        for child in self.children:
            if child.execute(agent, game_state):
                return True
        return False


class DecoratorNode(BehaviorNode):
    """Decorator node for behavior trees."""

    def __init__(self, name: str, decorator_func: Callable):
        super().__init__(name)
        self.node_type = BehaviorNodeType.DECORATOR
        self.decorator_func = decorator_func

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        if not self.children:
            return True
        try:
            return self.decorator_func(self.children[0].execute(agent, game_state))
        except Exception as e:  # pragma: no cover - defensive log
            logger.error(f"Decorator execution error: {e}")
            return False


class BehaviorTree:
    """Behavior tree for AI agents."""

    def __init__(self, name: str):
        self.name = name
        self.root: Optional[BehaviorNode] = None

    def set_root(self, node: BehaviorNode) -> None:
        self.root = node

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        if not self.root:
            return False
        try:
            return self.root.execute(agent, game_state)
        except Exception as e:  # pragma: no cover - defensive log
            logger.error(f"Behavior tree execution error: {e}")
            return False

    def get_all_nodes(self) -> List[BehaviorNode]:
        nodes: List[BehaviorNode] = []
        if self.root:
            self._collect_nodes(self.root, nodes)
        return nodes

    def _collect_nodes(self, node: BehaviorNode, nodes: List[BehaviorNode]) -> None:
        nodes.append(node)
        for child in node.children:
            self._collect_nodes(child, nodes)

    def find_node_by_name(self, name: str) -> Optional[BehaviorNode]:
        if not self.root:
            return None
        return self._find_node_recursive(self.root, name)

    def _find_node_recursive(self, node: BehaviorNode, name: str) -> Optional[BehaviorNode]:
        if node.name == name:
            return node
        for child in node.children:
            result = self._find_node_recursive(child, name)
            if result:
                return result
        return None


class DecisionRule:
    """Decision rule for AI agents."""

    def __init__(self, name: str, condition: Callable, action: Callable, priority: float = 1.0):
        self.name = name
        self.condition = condition
        self.action = action
        self.priority = priority
        self.usage_count = 0
        self.success_count = 0

    def evaluate(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        try:
            return self.condition(agent, game_state)
        except Exception as e:  # pragma: no cover - defensive log
            logger.error(f"Rule evaluation error: {e}")
            return False

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        try:
            self.usage_count += 1
            result = self.action(agent, game_state)
            if result:
                self.success_count += 1
            return result
        except Exception as e:  # pragma: no cover - defensive log
            logger.error(f"Rule execution error: {e}")
            return False

    def get_success_rate(self) -> float:
        if self.usage_count == 0:
            return 0.0
        return self.success_count / self.usage_count


class DecisionEngine:
    """Decision engine for AI agents."""

    def __init__(self) -> None:
        self.rules: List[DecisionRule] = []
        self.learning_experiences: List[LearningExperience] = []
        self.decision_history: List[AgentDecision] = []

    def add_rule(self, rule: DecisionRule) -> None:
        self.rules.append(rule)

    def make_decision(self, agent: "AIGamingAgent", game_state: GameState) -> Optional[AgentDecision]:
        applicable_rules = [rule for rule in self.rules if rule.evaluate(agent, game_state)]
        if not applicable_rules:
            return None
        applicable_rules.sort(key=lambda r: (r.priority, r.get_success_rate()), reverse=True)
        best_rule = applicable_rules[0]
        if best_rule.execute(agent, game_state):
            decision = AgentDecision(
                decision_type=DecisionType.MOVE,
                reasoning=f"Applied rule: {best_rule.name}",
            )
            self.decision_history.append(decision)
            return decision
        return None

    def add_learning_experience(self, experience: LearningExperience) -> None:
        self.learning_experiences.append(experience)
        if len(self.learning_experiences) > 1000:
            self.learning_experiences = self.learning_experiences[-1000:]

    def get_learning_insights(self) -> Dict[str, Any]:
        if not self.learning_experiences:
            return {}
        total_experiences = len(self.learning_experiences)
        successful_experiences = sum(1 for exp in self.learning_experiences if exp.success)
        success_rate = successful_experiences / total_experiences if total_experiences else 0
        return {
            "total_experiences": total_experiences,
            "success_rate": success_rate,
            "recent_success_rate": self._calculate_recent_success_rate(),
            "best_actions": self._find_best_actions(),
        }

    def _calculate_recent_success_rate(self) -> float:
        recent = self.learning_experiences[-100:] if len(self.learning_experiences) >= 100 else self.learning_experiences
        if not recent:
            return 0.0
        successful = sum(1 for exp in recent if exp.success)
        return successful / len(recent)

    def _find_best_actions(self) -> List[str]:
        action_success: Dict[str, Dict[str, int]] = {}
        for exp in self.learning_experiences:
            action = exp.action.decision_type.value
            if action not in action_success:
                action_success[action] = {"success": 0, "total": 0}
            action_success[action]["total"] += 1
            if exp.success:
                action_success[action]["success"] += 1
        action_rates: List[tuple[str, float]] = []
        for action, stats in action_success.items():
            rate = stats["success"] / stats["total"] if stats["total"] else 0
            action_rates.append((action, rate))
        action_rates.sort(key=lambda x: x[1], reverse=True)
        return [action for action, _ in action_rates[:5]]


def create_behavior_tree(name: str) -> BehaviorTree:
    """Factory function to create behavior tree."""
    return BehaviorTree(name)


def create_decision_engine() -> DecisionEngine:
    """Factory function to create decision engine."""
    return DecisionEngine()


__all__ = [
    "AgentState",
    "DecisionType",
    "BehaviorNodeType",
    "GameState",
    "AgentDecision",
    "LearningExperience",
    "BehaviorNode",
    "ActionNode",
    "ConditionNode",
    "SequenceNode",
    "SelectorNode",
    "DecoratorNode",
    "BehaviorTree",
    "DecisionRule",
    "DecisionEngine",
    "create_behavior_tree",
    "create_decision_engine",
]
