#!/usr/bin/env python3
"""
AI Agent Framework System
Agent-6: Gaming & Entertainment Development Specialist
TDD Integration Project - Agent_Cellphone_V2_Repository

Provides intelligent gaming agents with:
- Decision-making systems
- Learning and adaptation
- Multi-agent coordination
- Behavior trees and state machines
"""

import json
import time
import random
import logging
import threading

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Agent state enumeration"""

    IDLE = "idle"
    ACTIVE = "active"
    THINKING = "thinking"
    ACTING = "acting"
    LEARNING = "learning"
    ERROR = "error"
    COORDINATING = "coordinating"


class DecisionType(Enum):
    """Decision type enumeration"""

    MOVE = "move"
    ATTACK = "attack"
    DEFEND = "defend"
    COLLECT = "collect"
    EXPLORE = "explore"
    COORDINATE = "coordinate"
    WAIT = "wait"
    COMMUNICATE = "communicate"


class BehaviorNodeType(Enum):
    """Behavior tree node types"""

    SEQUENCE = "sequence"
    SELECTOR = "selector"
    ACTION = "action"
    CONDITION = "condition"
    DECORATOR = "decorator"


@dataclass
class GameState:
    """Game state information for AI agents"""

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
    """AI agent decision data"""

    decision_type: DecisionType
    target_position: Optional[tuple[float, float]] = None
    target_id: Optional[str] = None
    priority: float = 1.0
    confidence: float = 1.0
    reasoning: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class LearningExperience:
    """Learning experience for AI agents"""

    state: GameState
    action: AgentDecision
    reward: float
    next_state: GameState
    success: bool
    timestamp: float = field(default_factory=time.time)
    action_taken: str = ""


class BehaviorNode(ABC):
    """Abstract base class for behavior tree nodes"""

    def __init__(self, name: str):
        self.name = name
        self.children: List["BehaviorNode"] = []
        self.parent: Optional["BehaviorNode"] = None
        self.node_type: BehaviorNodeType = None

    @abstractmethod
    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute the behavior node"""
        pass

    def add_child(self, child: "BehaviorNode"):
        """Add a child node"""
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: "BehaviorNode"):
        """Remove a child node"""
        if child in self.children:
            child.parent = None
            self.children.remove(child)


class ActionNode(BehaviorNode):
    """Action node for behavior trees"""

    def __init__(self, name: str, action_func: Optional[Callable] = None):
        super().__init__(name)
        self.node_type = BehaviorNodeType.ACTION
        self.action_func = action_func

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute the action"""
        if self.action_func:
            try:
                return self.action_func(agent, game_state)
            except Exception as e:
                logger.error(f"Action execution error: {e}")
                return False
        return True

    def set_action(self, action_func: Callable):
        """Set the action function"""
        self.action_func = action_func


class ConditionNode(BehaviorNode):
    """Condition node for behavior trees"""

    def __init__(self, name: str, condition_func: Callable):
        super().__init__(name)
        self.node_type = BehaviorNodeType.CONDITION
        self.condition_func = condition_func

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute the condition check"""
        try:
            return self.condition_func(agent, game_state)
        except Exception as e:
            logger.error(f"Condition check error: {e}")
            return False

    def set_condition(self, condition_func: Callable):
        """Set the condition function"""
        self.condition_func = condition_func


class SequenceNode(BehaviorNode):
    """Sequence node for behavior trees"""

    def __init__(self, name: str):
        super().__init__(name)
        self.node_type = BehaviorNodeType.SEQUENCE

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute all children in sequence"""
        for child in self.children:
            if not child.execute(agent, game_state):
                return False
        return True


class SelectorNode(BehaviorNode):
    """Selector node for behavior trees"""

    def __init__(self, name: str):
        super().__init__(name)
        self.node_type = BehaviorNodeType.SELECTOR

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute children until one succeeds"""
        for child in self.children:
            if child.execute(agent, game_state):
                return True
        return False


class DecoratorNode(BehaviorNode):
    """Decorator node for behavior trees"""

    def __init__(self, name: str, decorator_func: Callable):
        super().__init__(name)
        self.node_type = BehaviorNodeType.DECORATOR
        self.decorator_func = decorator_func

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute with decorator function"""
        if not self.children:
            return True

        try:
            return self.decorator_func(self.children[0].execute(agent, game_state))
        except Exception as e:
            logger.error(f"Decorator execution error: {e}")
            return False


class BehaviorTree:
    """Behavior tree for AI agents"""

    def __init__(self, name: str):
        self.name = name
        self.root: Optional[BehaviorNode] = None

    def set_root(self, node: BehaviorNode):
        """Set the root node"""
        self.root = node

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute the behavior tree"""
        if not self.root:
            return False

        try:
            return self.root.execute(agent, game_state)
        except Exception as e:
            logger.error(f"Behavior tree execution error: {e}")
            return False

    def get_all_nodes(self) -> List[BehaviorNode]:
        """Get all nodes in the tree"""
        nodes = []
        if self.root:
            self._collect_nodes(self.root, nodes)
        return nodes

    def _collect_nodes(self, node: BehaviorNode, nodes: List[BehaviorNode]):
        """Recursively collect all nodes"""
        nodes.append(node)
        for child in node.children:
            self._collect_nodes(child, nodes)

    def find_node_by_name(self, name: str) -> Optional[BehaviorNode]:
        """Find a node by name"""
        if not self.root:
            return None

        return self._find_node_recursive(self.root, name)

    def _find_node_recursive(
        self, node: BehaviorNode, name: str
    ) -> Optional[BehaviorNode]:
        """Recursively find a node by name"""
        if node.name == name:
            return node

        for child in node.children:
            result = self._find_node_recursive(child, name)
            if result:
                return result

        return None


class DecisionRule:
    """Decision rule for AI agents"""

    def __init__(
        self, name: str, condition: Callable, action: Callable, priority: float = 1.0
    ):
        self.name = name
        self.condition = condition
        self.action = action
        self.priority = priority
        self.usage_count = 0
        self.success_count = 0

    def evaluate(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Evaluate if the rule should be applied"""
        try:
            return self.condition(agent, game_state)
        except Exception as e:
            logger.error(f"Rule evaluation error: {e}")
            return False

    def execute(self, agent: "AIGamingAgent", game_state: GameState) -> bool:
        """Execute the rule action"""
        try:
            self.usage_count += 1
            result = self.action(agent, game_state)
            if result:
                self.success_count += 1
            return result
        except Exception as e:
            logger.error(f"Rule execution error: {e}")
            return False

    def get_success_rate(self) -> float:
        """Get the success rate of this rule"""
        if self.usage_count == 0:
            return 0.0
        return self.success_count / self.usage_count


class DecisionEngine:
    """Decision engine for AI agents"""

    def __init__(self):
        self.rules: List[DecisionRule] = []
        self.learning_experiences: List[LearningExperience] = []
        self.decision_history: List[AgentDecision] = []

    def add_rule(self, rule: DecisionRule):
        """Add a decision rule"""
        self.rules.append(rule)

    def make_decision(
        self, agent: "AIGamingAgent", game_state: GameState
    ) -> Optional[AgentDecision]:
        """Make a decision based on current rules and state"""
        applicable_rules = []

        # Find applicable rules
        for rule in self.rules:
            if rule.evaluate(agent, game_state):
                applicable_rules.append(rule)

        if not applicable_rules:
            return None

        # Sort by priority and success rate
        applicable_rules.sort(
            key=lambda r: (r.priority, r.get_success_rate()), reverse=True
        )

        # Execute the best rule
        best_rule = applicable_rules[0]
        if best_rule.execute(agent, game_state):
            decision = AgentDecision(
                decision_type=DecisionType.MOVE,  # Default type
                reasoning=f"Applied rule: {best_rule.name}",
            )
            self.decision_history.append(decision)
            return decision

        return None

    def add_learning_experience(self, experience: LearningExperience):
        """Add a learning experience"""
        self.learning_experiences.append(experience)

        # Keep only recent experiences
        if len(self.learning_experiences) > 1000:
            self.learning_experiences = self.learning_experiences[-1000:]

    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from learning experiences"""
        if not self.learning_experiences:
            return {}

        total_experiences = len(self.learning_experiences)
        successful_experiences = sum(
            1 for exp in self.learning_experiences if exp.success
        )
        success_rate = (
            successful_experiences / total_experiences if total_experiences > 0 else 0
        )

        return {
            "total_experiences": total_experiences,
            "success_rate": success_rate,
            "recent_success_rate": self._calculate_recent_success_rate(),
            "best_actions": self._find_best_actions(),
        }

    def _calculate_recent_success_rate(self) -> float:
        """Calculate success rate of recent experiences"""
        recent_experiences = (
            self.learning_experiences[-100:]
            if len(self.learning_experiences) >= 100
            else self.learning_experiences
        )
        if not recent_experiences:
            return 0.0

        successful = sum(1 for exp in recent_experiences if exp.success)
        return successful / len(recent_experiences)

    def _find_best_actions(self) -> List[str]:
        """Find the most successful actions"""
        action_success = {}

        for exp in self.learning_experiences:
            action = exp.action.decision_type.value
            if action not in action_success:
                action_success[action] = {"success": 0, "total": 0}

            action_success[action]["total"] += 1
            if exp.success:
                action_success[action]["success"] += 1

        # Calculate success rates and sort
        action_rates = []
        for action, stats in action_success.items():
            rate = stats["success"] / stats["total"] if stats["total"] > 0 else 0
            action_rates.append((action, rate))

        action_rates.sort(key=lambda x: x[1], reverse=True)
        return [action for action, rate in action_rates[:5]]


class AIGamingAgent:
    """AI Gaming Agent"""

    def __init__(self, name: str, agent_type: str = "general"):
        self.name = name
        self.agent_type = agent_type
        self.state = AgentState.IDLE
        self.behavior_tree: Optional[BehaviorTree] = None
        self.decision_engine: Optional[DecisionEngine] = None
        self.learning_experiences: List[LearningExperience] = []
        self.performance_metrics = {
            "actions_completed": 0,
            "decisions_made": 0,
            "successful_actions": 0,
            "learning_experiences": 0,
        }

    def set_decision_engine(self, engine: DecisionEngine):
        """Set the decision engine"""
        self.decision_engine = engine

    def set_behavior_tree(self, tree: BehaviorTree):
        """Set the behavior tree"""
        self.behavior_tree = tree

    def update_state(self, new_state: AgentState):
        """Update agent state"""
        self.state = new_state
        logger.info(f"Agent {self.name} state changed to {new_state.value}")

    def make_decision(self, game_state: GameState) -> Optional[AgentDecision]:
        """Make a decision using the decision engine"""
        if not self.decision_engine:
            return None

        decision = self.decision_engine.make_decision(self, game_state)
        if decision:
            self.performance_metrics["decisions_made"] += 1

        return decision

    def execute_behavior_tree(self, game_state: GameState) -> bool:
        """Execute the behavior tree"""
        if not self.behavior_tree:
            return False

        result = self.behavior_tree.execute(self, game_state)
        if result:
            self.performance_metrics["actions_completed"] += 1
            self.performance_metrics["successful_actions"] += 1
        else:
            self.performance_metrics["actions_completed"] += 1

        return result

    def add_learning_experience(self, experience: LearningExperience):
        """Add a learning experience"""
        self.learning_experiences.append(experience)
        self.performance_metrics["learning_experiences"] += 1

        # Keep only recent experiences
        if len(self.learning_experiences) > 1000:
            self.learning_experiences = self.learning_experiences[-1000:]

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
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
    ):
        """Learn from an action"""
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
        """Render agent information"""
        return f"Agent({self.name}, {self.agent_type}, {self.state.value})"

    def update(self, game_state: GameState):
        """Update agent state and make decisions"""
        # Make decision
        decision = self.make_decision(game_state)

        # Execute behavior tree
        if decision:
            self.execute_behavior_tree(game_state)

        # Update performance metrics
        self.performance_metrics["actions_completed"] += 1


class MultiAgentCoordinator:
    """Coordinates multiple AI agents"""

    def __init__(self, name: str = "coordinator"):
        self.name = name
        self.agents: Dict[str, AIGamingAgent] = {}
        self.communication_channels: Dict[str, List[str]] = {}
        self.coordination_rules: List[Callable] = []

    def register_agent(self, agent: AIGamingAgent):
        """Register an agent with the coordinator"""
        self.agents[agent.name] = agent
        logger.info(f"Agent {agent.name} registered with coordinator")

    def unregister_agent(self, agent_name: str):
        """Unregister an agent"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            logger.info(f"Agent {agent_name} unregistered from coordinator")

    def get_agent_by_name(self, name: str) -> Optional[AIGamingAgent]:
        """Get an agent by name"""
        return self.agents.get(name)

    def create_communication_channel(self, channel_name: str) -> bool:
        """Create a communication channel"""
        if channel_name in self.communication_channels:
            return False

        self.communication_channels[channel_name] = []
        logger.info(f"Communication channel {channel_name} created")
        return True

    def send_message(self, channel_name: str, message: str, sender: str):
        """Send a message to a communication channel"""
        if channel_name not in self.communication_channels:
            return False

        self.communication_channels[channel_name].append(f"{sender}: {message}")
        logger.info(f"Message sent to {channel_name}: {message}")
        return True

    def coordinate_agents(self, game_state: GameState):
        """Coordinate all registered agents"""
        for agent in self.agents.values():
            agent.update(game_state)

        # Apply coordination rules
        for rule in self.coordination_rules:
            try:
                rule(self.agents, game_state)
            except Exception as e:
                logger.error(f"Coordination rule error: {e}")

    def get_coordination_metrics(self) -> Dict[str, Any]:
        """Get coordination metrics"""
        total_agents = len(self.agents)
        active_agents = sum(
            1 for agent in self.agents.values() if agent.state == AgentState.ACTIVE
        )

        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "communication_channels": len(self.communication_channels),
            "coordination_rules": len(self.coordination_rules),
        }


def create_ai_gaming_agent(name: str, agent_type: str = "general") -> AIGamingAgent:
    """Factory function to create AI gaming agent"""
    return AIGamingAgent(name, agent_type)


def create_behavior_tree(name: str) -> BehaviorTree:
    """Factory function to create behavior tree"""
    return BehaviorTree(name)


def create_decision_engine() -> DecisionEngine:
    """Factory function to create decision engine"""
    return DecisionEngine()


def create_multi_agent_coordinator(name: str = "coordinator") -> MultiAgentCoordinator:
    """Factory function to create multi-agent coordinator"""
    return MultiAgentCoordinator(name)


if __name__ == "__main__":
    # Example usage
    agent = create_ai_gaming_agent("test_agent")
    tree = create_behavior_tree("test_tree")
    engine = create_decision_engine()

    agent.set_behavior_tree(tree)
    agent.set_decision_engine(engine)

    game_state = GameState()
    agent.update(game_state)
