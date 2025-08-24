import unittest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.ai_agent_framework import (
    BehaviorNodeType,
    ActionNode,
    ConditionNode,
    SequenceNode,
    SelectorNode,
    DecoratorNode,
    BehaviorTree,
    DecisionEngine,
    DecisionRule,
    GameState,
    DecisionType,
    AgentDecision,
    LearningExperience,
)


class TestActionNode(unittest.TestCase):
    def setUp(self):
        self.action_node = ActionNode("action")
        self.mock_action = Mock(return_value=True)

    def test_action_node_creation(self):
        self.assertEqual(self.action_node.name, "action")
        self.assertEqual(self.action_node.node_type, BehaviorNodeType.ACTION)
        self.assertIsNone(self.action_node.action_func)

    def test_set_and_execute_action(self):
        self.action_node.set_action(self.mock_action)
        result = self.action_node.execute(Mock(), GameState())
        self.assertTrue(result)
        self.mock_action.assert_called_once()

    def test_execute_no_action(self):
        self.assertTrue(self.action_node.execute(Mock(), GameState()))

    def test_execute_action_failure(self):
        self.action_node.set_action(Mock(return_value=False))
        self.assertFalse(self.action_node.execute(Mock(), GameState()))

    def test_add_child(self):
        child = ActionNode("child")
        self.action_node.add_child(child)
        self.assertIn(child, self.action_node.children)


class TestConditionNode(unittest.TestCase):
    def setUp(self):
        self.mock_condition = Mock(return_value=True)
        self.condition_node = ConditionNode("cond", self.mock_condition)

    def test_condition_node_creation(self):
        self.assertEqual(self.condition_node.name, "cond")
        self.assertEqual(self.condition_node.node_type, BehaviorNodeType.CONDITION)

    def test_execute_condition_true(self):
        self.assertTrue(self.condition_node.execute(Mock(), GameState()))
        self.mock_condition.assert_called_once()

    def test_execute_condition_false(self):
        self.mock_condition.return_value = False
        self.assertFalse(self.condition_node.execute(Mock(), GameState()))


class TestSequenceAndSelector(unittest.TestCase):
    def test_sequence_execution(self):
        seq = SequenceNode("seq")
        child1 = ActionNode("a1", action_func=lambda a, s: True)
        child2 = ActionNode("a2", action_func=lambda a, s: False)
        seq.add_child(child1)
        seq.add_child(child2)
        self.assertFalse(seq.execute(Mock(), GameState()))

    def test_selector_execution(self):
        sel = SelectorNode("sel")
        child1 = ActionNode("a1", action_func=lambda a, s: False)
        child2 = ActionNode("a2", action_func=lambda a, s: True)
        sel.add_child(child1)
        sel.add_child(child2)
        self.assertTrue(sel.execute(Mock(), GameState()))


class TestDecoratorNode(unittest.TestCase):
    def test_decorator_execution(self):
        child = ActionNode("a", action_func=lambda a, s: True)
        decorator = DecoratorNode("d", lambda x: not x)
        decorator.add_child(child)
        self.assertFalse(decorator.execute(Mock(), GameState()))

    def test_decorator_no_child(self):
        decorator = DecoratorNode("d", lambda x: not x)
        self.assertTrue(decorator.execute(Mock(), GameState()))


class TestBehaviorTree(unittest.TestCase):
    def setUp(self):
        self.tree = BehaviorTree("tree")
        self.action = ActionNode("a", action_func=lambda a, s: True)

    def test_set_root(self):
        self.tree.set_root(self.action)
        self.assertEqual(self.tree.root, self.action)

    def test_execute_with_root(self):
        self.tree.set_root(self.action)
        self.assertTrue(self.tree.execute(Mock(), GameState()))

    def test_execute_without_root(self):
        self.assertFalse(self.tree.execute(Mock(), GameState()))

    def test_get_all_nodes(self):
        seq = SequenceNode("seq")
        seq.add_child(self.action)
        seq.add_child(ConditionNode("c", lambda a, s: True))
        self.tree.set_root(seq)
        nodes = self.tree.get_all_nodes()
        self.assertEqual(len(nodes), 3)

    def test_find_node_by_name(self):
        self.tree.set_root(self.action)
        self.assertEqual(self.tree.find_node_by_name("a"), self.action)
        self.assertIsNone(self.tree.find_node_by_name("x"))


class TestDecisionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine()

    def test_add_rule_and_make_decision(self):
        rule = DecisionRule(
            name="r1",
            condition=lambda a, s: True,
            action=lambda a, s: True,
            priority=1.0,
        )
        self.engine.add_rule(rule)
        agent = Mock()
        decision = self.engine.make_decision(agent, GameState())
        self.assertIsInstance(decision, AgentDecision)

    def test_make_decision_no_rules(self):
        agent = Mock()
        self.assertIsNone(self.engine.make_decision(agent, GameState()))

    def test_learning_experiences(self):
        state = GameState()
        action = AgentDecision(decision_type=DecisionType.MOVE)
        exp = LearningExperience(
            state=state,
            action=action,
            reward=1.0,
            next_state=state,
            success=True,
            action_taken="move",
        )
        self.engine.add_learning_experience(exp)
        insights = self.engine.get_learning_insights()
        self.assertIn("total_experiences", insights)
        self.assertEqual(insights["total_experiences"], 1)
