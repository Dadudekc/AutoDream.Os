import unittest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.ai_agent_framework import (
    AgentState,
    DecisionType,
    GameState,
    AgentDecision,
    LearningExperience,
    AIGamingAgent,
    ActionNode,
    BehaviorTree,
    DecisionEngine,
    DecisionRule,
)


class TestAIGamingAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AIGamingAgent("agent")

    def test_agent_creation(self):
        self.assertEqual(self.agent.name, "agent")
        self.assertEqual(self.agent.state, AgentState.IDLE)
        self.assertIsNone(self.agent.behavior_tree)
        self.assertIsNone(self.agent.decision_engine)

    def test_setters(self):
        tree = BehaviorTree("tree")
        engine = DecisionEngine()
        self.agent.set_behavior_tree(tree)
        self.agent.set_decision_engine(engine)
        self.assertEqual(self.agent.behavior_tree, tree)
        self.assertEqual(self.agent.decision_engine, engine)

    def test_update_state(self):
        self.agent.update_state(AgentState.ACTIVE)
        self.assertEqual(self.agent.state, AgentState.ACTIVE)

    def test_execute_behavior_tree(self):
        tree = BehaviorTree("tree")
        tree.set_root(ActionNode("a", lambda a, s: True))
        self.agent.set_behavior_tree(tree)
        self.assertTrue(self.agent.execute_behavior_tree(GameState()))

    def test_execute_behavior_tree_no_tree(self):
        self.assertFalse(self.agent.execute_behavior_tree(GameState()))

    def test_make_decision(self):
        engine = DecisionEngine()
        rule = DecisionRule(
            name="r1",
            condition=lambda a, s: True,
            action=lambda a, s: True,
            priority=1.0,
        )
        engine.add_rule(rule)
        self.agent.set_decision_engine(engine)
        decision = self.agent.make_decision(GameState())
        self.assertIsInstance(decision, AgentDecision)

    def test_make_decision_no_engine(self):
        self.assertIsNone(self.agent.make_decision(GameState()))

    def test_add_learning_experience(self):
        exp = LearningExperience(
            state=GameState(),
            action=AgentDecision(decision_type=DecisionType.MOVE),
            reward=1.0,
            next_state=GameState(),
            success=True,
            action_taken="move",
        )
        self.agent.add_learning_experience(exp)
        self.assertIn(exp, self.agent.learning_experiences)

    def test_get_performance_metrics(self):
        metrics = self.agent.get_performance_metrics()
        self.assertIn("actions_completed", metrics)
        self.assertIn("success_rate", metrics)
