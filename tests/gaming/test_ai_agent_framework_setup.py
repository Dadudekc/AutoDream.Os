from datetime import datetime
from pathlib import Path
import sys

import unittest

from gaming_systems.ai_agent_framework import (


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    AgentState,
    DecisionType,
    BehaviorNodeType,
    GameState,
    AgentDecision,
    LearningExperience,
    BehaviorNode,
)


class TestAgentState(unittest.TestCase):
    def test_agent_states(self):
        states = [
            AgentState.IDLE,
            AgentState.ACTIVE,
            AgentState.THINKING,
            AgentState.ACTING,
            AgentState.LEARNING,
            AgentState.ERROR,
            AgentState.COORDINATING,
        ]
        for state in states:
            self.assertIsInstance(state.value, str)
            self.assertTrue(state.value)


class TestDecisionType(unittest.TestCase):
    def test_decision_types(self):
        decision_types = [
            DecisionType.MOVE,
            DecisionType.ATTACK,
            DecisionType.DEFEND,
            DecisionType.COLLECT,
            DecisionType.EXPLORE,
            DecisionType.COORDINATE,
            DecisionType.WAIT,
            DecisionType.COMMUNICATE,
        ]
        for decision_type in decision_types:
            self.assertIsInstance(decision_type.value, str)
            self.assertTrue(decision_type.value)


class TestBehaviorNodeType(unittest.TestCase):
    def test_node_types(self):
        node_types = [
            BehaviorNodeType.SEQUENCE,
            BehaviorNodeType.SELECTOR,
            BehaviorNodeType.ACTION,
            BehaviorNodeType.CONDITION,
            BehaviorNodeType.DECORATOR,
        ]
        for node_type in node_types:
            self.assertIsInstance(node_type.value, str)
            self.assertTrue(node_type.value)


class TestGameState(unittest.TestCase):
    def test_default_game_state(self):
        state = GameState()
        self.assertEqual(state.level, 1)
        self.assertEqual(state.score, 0)
        self.assertEqual(state.time_elapsed, 0.0)
        self.assertEqual(state.enemies_remaining, 5)

    def test_custom_game_state(self):
        state = GameState(level=2, score=100, time_elapsed=10.5, enemies_remaining=3)
        self.assertEqual(state.level, 2)
        self.assertEqual(state.score, 100)
        self.assertEqual(state.time_elapsed, 10.5)
        self.assertEqual(state.enemies_remaining, 3)


class TestAgentDecision(unittest.TestCase):
    def test_agent_decision(self):
        decision = AgentDecision(
            decision_type=DecisionType.MOVE,
            target_position=(1.0, 2.0),
            priority=0.5,
            confidence=0.7,
            reasoning="test",
        )
        self.assertEqual(decision.decision_type, DecisionType.MOVE)
        self.assertEqual(decision.target_position, (1.0, 2.0))
        self.assertEqual(decision.priority, 0.5)
        self.assertEqual(decision.confidence, 0.7)
        self.assertEqual(decision.reasoning, "test")


class TestLearningExperience(unittest.TestCase):
    def test_learning_experience(self):
        state = GameState()
        action = AgentDecision(decision_type=DecisionType.ATTACK)
        next_state = GameState(score=10)
        experience = LearningExperience(
            state=state,
            action=action,
            reward=1.0,
            next_state=next_state,
            success=True,
            action_taken="attack",
        )
        self.assertEqual(experience.state, state)
        self.assertEqual(experience.action, action)
        self.assertEqual(experience.reward, 1.0)
        self.assertEqual(experience.next_state, next_state)
        self.assertTrue(experience.success)


class TestBehaviorNode(unittest.TestCase):
    def test_abstract_methods(self):
        for method in ("execute", "add_child", "remove_child"):
            self.assertTrue(hasattr(BehaviorNode, method))
