#!/usr/bin/env python3
"""
Test Suite for AI Agent Framework System
Agent-6: Gaming & Entertainment Development Specialist
TDD Integration Project - Agent_Cellphone_V2_Repository

Comprehensive testing of:
- Behavior tree nodes and structures
- Decision engines and learning systems
- AI agent behaviors and states
- Multi-agent coordination
- Learning experiences and adaptation
- Behavior tree execution
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to the path to import gaming modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.ai_agent_framework import (
    AgentState,
    DecisionType,
    BehaviorNodeType,
    GameState,
    AgentDecision,
    LearningExperience,
    BehaviorNode,
    ActionNode,
    ConditionNode,
    SequenceNode,
    SelectorNode,
    DecoratorNode,
    BehaviorTree,
    DecisionEngine,
    AIGamingAgent,
    MultiAgentCoordinator
)

class TestAgentState(unittest.TestCase):
    """Test AgentState enumeration"""
    
    def test_agent_states(self):
        """Test all agent states exist"""
        states = [
            AgentState.IDLE,
            AgentState.ACTIVE,
            AgentState.LEARNING,
            AgentState.COORDINATING,
            AgentState.ERROR
        ]
        
        for state in states:
            self.assertIsInstance(state.value, str)
            self.assertTrue(len(state.value) > 0)

class TestDecisionType(unittest.TestCase):
    """Test DecisionType enumeration"""
    
    def test_decision_types(self):
        """Test all decision types exist"""
        decision_types = [
            DecisionType.MOVE,
            DecisionType.ATTACK,
            DecisionType.DEFEND,
            DecisionType.COLLECT,
            DecisionType.COMMUNICATE,
            DecisionType.WAIT
        ]
        
        for decision_type in decision_types:
            self.assertIsInstance(decision_type.value, str)
            self.assertTrue(len(decision_type.value) > 0)

class TestBehaviorNodeType(unittest.TestCase):
    """Test BehaviorNodeType enumeration"""
    
    def test_node_types(self):
        """Test all behavior node types exist"""
        node_types = [
            BehaviorNodeType.ACTION,
            BehaviorNodeType.CONDITION,
            BehaviorNodeType.SEQUENCE,
            BehaviorNodeType.SELECTOR,
            BehaviorNodeType.DECORATOR
        ]
        
        for node_type in node_types:
            self.assertIsInstance(node_type.value, str)
            self.assertTrue(len(node_type.value) > 0)

class TestGameState(unittest.TestCase):
    """Test GameState data class"""
    
    def test_default_game_state(self):
        """Test default game state values"""
        state = GameState(
            level=1,
            score=0,
            time_elapsed=0.0,
            player_health=100,
            enemies_remaining=5
        )
        
        self.assertEqual(state.level, 1)
        self.assertEqual(state.score, 0)
        self.assertEqual(state.time_elapsed, 0.0)
        self.assertEqual(state.player_health, 100)
        self.assertEqual(state.enemies_remaining, 5)
    
    def test_custom_game_state(self):
        """Test custom game state values"""
        state = GameState(
            level=10,
            score=5000,
            time_elapsed=120.5,
            player_health=75,
            enemies_remaining=2
        )
        
        self.assertEqual(state.level, 10)
        self.assertEqual(state.score, 5000)
        self.assertEqual(state.time_elapsed, 120.5)
        self.assertEqual(state.player_health, 75)
        self.assertEqual(state.enemies_remaining, 2)

class TestAgentDecision(unittest.TestCase):
    """Test AgentDecision data class"""
    
    def test_agent_decision(self):
        """Test agent decision creation"""
        decision = AgentDecision(
            decision_type=DecisionType.MOVE,
            target_position=(100, 200),
            priority=0.8,
            confidence=0.9,
            reasoning="Move to strategic position"
        )
        
        self.assertEqual(decision.decision_type, DecisionType.MOVE)
        self.assertEqual(decision.target_position, (100, 200))
        self.assertEqual(decision.priority, 0.8)
        self.assertEqual(decision.confidence, 0.9)
        self.assertEqual(decision.reasoning, "Move to strategic position")

class TestLearningExperience(unittest.TestCase):
    """Test LearningExperience data class"""
    
    def test_learning_experience(self):
        """Test learning experience creation"""
        experience = LearningExperience(
            action_taken=DecisionType.ATTACK,
            outcome="success",
            reward=10.0,
            context={"enemy_type": "goblin", "distance": 50},
            timestamp=datetime.now()
        )
        
        self.assertEqual(experience.action_taken, DecisionType.ATTACK)
        self.assertEqual(experience.outcome, "success")
        self.assertEqual(experience.reward, 10.0)
        self.assertEqual(experience.context["enemy_type"], "goblin")
        self.assertEqual(experience.context["distance"], 50)
        self.assertIsInstance(experience.timestamp, datetime)

class TestBehaviorNode(unittest.TestCase):
    """Test BehaviorNode abstract class"""
    
    def test_abstract_methods(self):
        """Test that abstract methods exist"""
        # This test verifies the interface structure
        node_methods = [
            'execute',
            'add_child',
            'remove_child',
            'get_children'
        ]
        
        for method_name in node_methods:
            self.assertTrue(hasattr(BehaviorNode, method_name))

class TestActionNode(unittest.TestCase):
    """Test ActionNode implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.action_node = ActionNode("test_action")
        self.mock_action = Mock(return_value=True)
        self.action_node.action = self.mock_action
    
    def test_action_node_creation(self):
        """Test action node creation"""
        self.assertEqual(self.action_node.name, "test_action")
        self.assertEqual(self.action_node.node_type, BehaviorNodeType.ACTION)
        self.assertIsNone(self.action_node.action)
    
    def test_set_action(self):
        """Test setting action function"""
        self.action_node.action = self.mock_action
        self.assertEqual(self.action_node.action, self.mock_action)
    
    def test_execute_success(self):
        """Test successful action execution"""
        result = self.action_node.execute()
        
        self.assertTrue(result)
        self.mock_action.assert_called_once()
    
    def test_execute_no_action(self):
        """Test execution without action set"""
        self.action_node.action = None
        result = self.action_node.execute()
        
        self.assertFalse(result)
    
    def test_execute_action_failure(self):
        """Test action execution failure"""
        self.mock_action.return_value = False
        result = self.action_node.execute()
        
        self.assertFalse(result)
    
    def test_add_child(self):
        """Test adding child nodes (should not be allowed for action nodes)"""
        child_node = ActionNode("child")
        self.action_node.add_child(child_node)
        
        # Action nodes should not have children
        self.assertEqual(len(self.action_node.get_children()), 0)

class TestConditionNode(unittest.TestCase):
    """Test ConditionNode implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.condition_node = ConditionNode("test_condition")
        self.mock_condition = Mock(return_value=True)
        self.condition_node.condition = self.mock_condition
    
    def test_condition_node_creation(self):
        """Test condition node creation"""
        self.assertEqual(self.condition_node.name, "test_condition")
        self.assertEqual(self.condition_node.node_type, BehaviorNodeType.CONDITION)
        self.assertIsNone(self.condition_node.condition)
    
    def test_set_condition(self):
        """Test setting condition function"""
        self.condition_node.condition = self.mock_condition
        self.assertEqual(self.condition_node.condition, self.mock_condition)
    
    def test_execute_condition_true(self):
        """Test condition execution when true"""
        result = self.condition_node.execute()
        
        self.assertTrue(result)
        self.mock_condition.assert_called_once()
    
    def test_execute_condition_false(self):
        """Test condition execution when false"""
        self.mock_condition.return_value = False
        result = self.condition_node.execute()
        
        self.assertFalse(result)
    
    def test_execute_no_condition(self):
        """Test execution without condition set"""
        self.condition_node.condition = None
        result = self.condition_node.execute()
        
        self.assertFalse(result)

class TestSequenceNode(unittest.TestCase):
    """Test SequenceNode implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sequence_node = SequenceNode("test_sequence")
        
        # Create mock child nodes
        self.success_node = Mock()
        self.success_node.execute.return_value = True
        
        self.failure_node = Mock()
        self.failure_node.execute.return_value = False
    
    def test_sequence_node_creation(self):
        """Test sequence node creation"""
        self.assertEqual(self.sequence_node.name, "test_sequence")
        self.assertEqual(self.sequence_node.node_type, BehaviorNodeType.SEQUENCE)
        self.assertEqual(len(self.sequence_node.get_children()), 0)
    
    def test_add_child(self):
        """Test adding child nodes"""
        self.sequence_node.add_child(self.success_node)
        self.sequence_node.add_child(self.failure_node)
        
        children = self.sequence_node.get_children()
        self.assertEqual(len(children), 2)
        self.assertIn(self.success_node, children)
        self.assertIn(self.failure_node, children)
    
    def test_execute_all_success(self):
        """Test sequence execution when all children succeed"""
        self.sequence_node.add_child(self.success_node)
        self.sequence_node.add_child(self.success_node)
        
        result = self.sequence_node.execute()
        
        self.assertTrue(result)
        self.assertEqual(self.success_node.execute.call_count, 2)
    
    def test_execute_with_failure(self):
        """Test sequence execution when a child fails"""
        self.sequence_node.add_child(self.success_node)
        self.sequence_node.add_child(self.failure_node)
        self.sequence_node.add_child(self.success_node)
        
        result = self.sequence_node.execute()
        
        self.assertFalse(result)
        self.assertEqual(self.success_node.execute.call_count, 1)
        self.assertEqual(self.failure_node.execute.call_count, 1)
        # Third child should not be executed due to failure
    
    def test_execute_no_children(self):
        """Test sequence execution with no children"""
        result = self.sequence_node.execute()
        
        self.assertTrue(result)  # Empty sequence succeeds by default

class TestSelectorNode(unittest.TestCase):
    """Test SelectorNode implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.selector_node = SelectorNode("test_selector")
        
        # Create mock child nodes
        self.failure_node = Mock()
        self.failure_node.execute.return_value = False
        
        self.success_node = Mock()
        self.success_node.execute.return_value = True
    
    def test_selector_node_creation(self):
        """Test selector node creation"""
        self.assertEqual(self.selector_node.name, "test_selector")
        self.assertEqual(self.selector_node.node_type, BehaviorNodeType.SELECTOR)
        self.assertEqual(len(self.selector_node.get_children()), 0)
    
    def test_execute_first_success(self):
        """Test selector execution when first child succeeds"""
        self.selector_node.add_child(self.success_node)
        self.selector_node.add_child(self.failure_node)
        
        result = self.selector_node.execute()
        
        self.assertTrue(result)
        self.assertEqual(self.success_node.execute.call_count, 1)
        self.assertEqual(self.failure_node.execute.call_count, 0)  # Should not execute
    
    def test_execute_second_success(self):
        """Test selector execution when second child succeeds"""
        self.selector_node.add_child(self.failure_node)
        self.selector_node.add_child(self.success_node)
        
        result = self.selector_node.execute()
        
        self.assertTrue(result)
        self.assertEqual(self.failure_node.execute.call_count, 1)
        self.assertEqual(self.success_node.execute.call_count, 1)
    
    def test_execute_all_failure(self):
        """Test selector execution when all children fail"""
        self.selector_node.add_child(self.failure_node)
        self.selector_node.add_child(self.failure_node)
        
        result = self.selector_node.execute()
        
        self.assertFalse(result)
        self.assertEqual(self.failure_node.execute.call_count, 2)
    
    def test_execute_no_children(self):
        """Test selector execution with no children"""
        result = self.selector_node.execute()
        
        self.assertFalse(result)  # Empty selector fails by default

class TestDecoratorNode(unittest.TestCase):
    """Test DecoratorNode implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.decorator_node = DecoratorNode("test_decorator")
        
        # Create mock child node
        self.child_node = Mock()
        self.child_node.execute.return_value = True
        
        # Create mock decorator function
        self.mock_decorator = Mock(side_effect=lambda x: not x)  # Inverts result
        self.decorator_node.decorator = self.mock_decorator
    
    def test_decorator_node_creation(self):
        """Test decorator node creation"""
        self.assertEqual(self.decorator_node.name, "test_decorator")
        self.assertEqual(self.decorator_node.node_type, BehaviorNodeType.DECORATOR)
        self.assertIsNone(self.decorator_node.decorator)
        self.assertEqual(len(self.decorator_node.get_children()), 0)
    
    def test_add_child(self):
        """Test adding child node"""
        self.decorator_node.add_child(self.child_node)
        
        children = self.decorator_node.get_children()
        self.assertEqual(len(children), 1)
        self.assertIn(self.child_node, children)
    
    def test_execute_with_decorator(self):
        """Test decorator execution with decorator function"""
        self.decorator_node.add_child(self.child_node)
        
        result = self.decorator_node.execute()
        
        self.assertFalse(result)  # Decorator inverts True to False
        self.child_node.execute.assert_called_once()
        self.mock_decorator.assert_called_once_with(True)
    
    def test_execute_no_decorator(self):
        """Test decorator execution without decorator function"""
        self.decorator_node.add_child(self.child_node)
        self.decorator_node.decorator = None
        
        result = self.decorator_node.execute()
        
        self.assertTrue(result)  # Should return child result directly
        self.child_node.execute.assert_called_once()
    
    def test_execute_no_child(self):
        """Test decorator execution with no child"""
        result = self.decorator_node.execute()
        
        self.assertFalse(result)  # No child means failure

class TestBehaviorTree(unittest.TestCase):
    """Test BehaviorTree implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.behavior_tree = BehaviorTree("test_tree")
        
        # Create mock nodes
        self.action_node = Mock()
        self.action_node.execute.return_value = True
        self.action_node.name = "test_action"
        
        self.condition_node = Mock()
        self.condition_node.execute.return_value = True
        self.condition_node.name = "test_condition"
    
    def test_behavior_tree_creation(self):
        """Test behavior tree creation"""
        self.assertEqual(self.behavior_tree.name, "test_tree")
        self.assertIsNone(self.behavior_tree.root)
        self.assertEqual(len(self.behavior_tree.get_all_nodes()), 0)
    
    def test_set_root(self):
        """Test setting root node"""
        self.behavior_tree.set_root(self.action_node)
        
        self.assertEqual(self.behavior_tree.root, self.action_node)
        self.assertEqual(len(self.behavior_tree.get_all_nodes()), 1)
    
    def test_execute_with_root(self):
        """Test tree execution with root node"""
        self.behavior_tree.set_root(self.action_node)
        
        result = self.behavior_tree.execute()
        
        self.assertTrue(result)
        self.action_node.execute.assert_called_once()
    
    def test_execute_without_root(self):
        """Test tree execution without root node"""
        result = self.behavior_tree.execute()
        
        self.assertFalse(result)
    
    def test_get_all_nodes(self):
        """Test getting all nodes in tree"""
        # Create a simple tree structure
        sequence_node = SequenceNode("sequence")
        sequence_node.add_child(self.action_node)
        sequence_node.add_child(self.condition_node)
        
        self.behavior_tree.set_root(sequence_node)
        
        all_nodes = self.behavior_tree.get_all_nodes()
        self.assertEqual(len(all_nodes), 3)  # sequence + action + condition
        self.assertIn(self.action_node, all_nodes)
        self.assertIn(self.condition_node, all_nodes)
    
    def test_find_node_by_name(self):
        """Test finding node by name"""
        self.behavior_tree.set_root(self.action_node)
        
        found_node = self.behavior_tree.find_node_by_name("test_action")
        self.assertEqual(found_node, self.action_node)
        
        not_found = self.behavior_tree.find_node_by_name("nonexistent")
        self.assertIsNone(not_found)

class TestDecisionEngine(unittest.TestCase):
    """Test DecisionEngine implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.decision_engine = DecisionEngine()
        
        # Create mock rules
        self.mock_rule = Mock()
        self.mock_rule.evaluate.return_value = AgentDecision(
            decision_type=DecisionType.MOVE,
            target_position=(100, 200),
            priority=0.8,
            confidence=0.9,
            reasoning="Test rule"
        )
    
    def test_decision_engine_creation(self):
        """Test decision engine creation"""
        self.assertEqual(len(self.decision_engine.rules), 0)
        self.assertEqual(len(self.decision_engine.learning_experiences), 0)
    
    def test_add_rule(self):
        """Test adding decision rules"""
        self.decision_engine.add_rule(self.mock_rule)
        
        self.assertIn(self.mock_rule, self.decision_engine.rules)
    
    def test_add_learning_experience(self):
        """Test adding learning experiences"""
        experience = LearningExperience(
            action_taken=DecisionType.ATTACK,
            outcome="success",
            reward=10.0,
            context={"enemy_type": "goblin"},
            timestamp=datetime.now()
        )
        
        self.decision_engine.add_learning_experience(experience)
        
        self.assertIn(experience, self.decision_engine.learning_experiences)
    
    def test_make_decision_with_rules(self):
        """Test decision making with rules"""
        self.decision_engine.add_rule(self.mock_rule)
        
        game_state = GameState(level=1, score=0, time_elapsed=0.0, player_health=100, enemies_remaining=5)
        
        decision = self.decision_engine.make_decision(game_state)
        
        self.assertIsInstance(decision, AgentDecision)
        self.assertEqual(decision.decision_type, DecisionType.MOVE)
        self.mock_rule.evaluate.assert_called_once_with(game_state)
    
    def test_make_decision_no_rules(self):
        """Test decision making without rules"""
        game_state = GameState(level=1, score=0, time_elapsed=0.0, player_health=100, enemies_remaining=5)
        
        decision = self.decision_engine.make_decision(game_state)
        
        self.assertIsNone(decision)
    
    def test_get_learning_insights(self):
        """Test getting learning insights"""
        # Add some learning experiences
        experiences = [
            LearningExperience(DecisionType.ATTACK, "success", 10.0, {}, datetime.now()),
            LearningExperience(DecisionType.ATTACK, "failure", -5.0, {}, datetime.now()),
            LearningExperience(DecisionType.MOVE, "success", 5.0, {}, datetime.now())
        ]
        
        for exp in experiences:
            self.decision_engine.add_learning_experience(exp)
        
        insights = self.decision_engine.get_learning_insights()
        
        self.assertIsInstance(insights, dict)
        self.assertIn('attack_success_rate', insights)
        self.assertIn('move_success_rate', insights)
        self.assertIn('average_reward', insights)

class TestAIGamingAgent(unittest.TestCase):
    """Test AIGamingAgent implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = AIGamingAgent("test_agent")
        
        # Create mock behavior tree
        self.mock_behavior_tree = Mock()
        self.mock_behavior_tree.execute.return_value = True
        
        # Create mock decision engine
        self.mock_decision_engine = Mock()
        self.mock_decision_engine.make_decision.return_value = AgentDecision(
            decision_type=DecisionType.MOVE,
            target_position=(100, 200),
            priority=0.8,
            confidence=0.9,
            reasoning="Test decision"
        )
    
    def test_agent_creation(self):
        """Test agent creation"""
        self.assertEqual(self.agent.name, "test_agent")
        self.assertEqual(self.agent.state, AgentState.IDLE)
        self.assertIsNone(self.agent.behavior_tree)
        self.assertIsNone(self.agent.decision_engine)
        self.assertEqual(len(self.agent.learning_experiences), 0)
    
    def test_set_behavior_tree(self):
        """Test setting behavior tree"""
        self.agent.set_behavior_tree(self.mock_behavior_tree)
        
        self.assertEqual(self.agent.behavior_tree, self.mock_behavior_tree)
    
    def test_set_decision_engine(self):
        """Test setting decision engine"""
        self.agent.set_decision_engine(self.mock_decision_engine)
        
        self.assertEqual(self.agent.decision_engine, self.mock_decision_engine)
    
    def test_update_state(self):
        """Test updating agent state"""
        self.agent.update_state(AgentState.ACTIVE)
        
        self.assertEqual(self.agent.state, AgentState.ACTIVE)
    
    def test_execute_behavior_tree(self):
        """Test executing behavior tree"""
        self.agent.set_behavior_tree(self.mock_behavior_tree)
        
        result = self.agent.execute_behavior_tree()
        
        self.assertTrue(result)
        self.mock_behavior_tree.execute.assert_called_once()
    
    def test_execute_behavior_tree_no_tree(self):
        """Test executing behavior tree without tree set"""
        result = self.agent.execute_behavior_tree()
        
        self.assertFalse(result)
    
    def test_make_decision(self):
        """Test making decisions"""
        self.agent.set_decision_engine(self.mock_decision_engine)
        
        game_state = GameState(level=1, score=0, time_elapsed=0.0, player_health=100, enemies_remaining=5)
        
        decision = self.agent.make_decision(game_state)
        
        self.assertIsInstance(decision, AgentDecision)
        self.mock_decision_engine.make_decision.assert_called_once_with(game_state)
    
    def test_make_decision_no_engine(self):
        """Test making decisions without decision engine"""
        game_state = GameState(level=1, score=0, time_elapsed=0.0, player_health=100, enemies_remaining=5)
        
        decision = self.agent.make_decision(game_state)
        
        self.assertIsNone(decision)
    
    def test_add_learning_experience(self):
        """Test adding learning experiences"""
        experience = LearningExperience(
            action_taken=DecisionType.ATTACK,
            outcome="success",
            reward=10.0,
            context={"enemy_type": "goblin"},
            timestamp=datetime.now()
        )
        
        self.agent.add_learning_experience(experience)
        
        self.assertIn(experience, self.agent.learning_experiences)
    
    def test_get_performance_metrics(self):
        """Test getting performance metrics"""
        # Add some learning experiences
        experiences = [
            LearningExperience(DecisionType.ATTACK, "success", 10.0, {}, datetime.now()),
            LearningExperience(DecisionType.ATTACK, "failure", -5.0, {}, datetime.now()),
            LearningExperience(DecisionType.MOVE, "success", 5.0, {}, datetime.now())
        ]
        
        for exp in experiences:
            self.agent.add_learning_experience(exp)
        
        metrics = self.agent.get_performance_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('total_experiences', metrics)
        self.assertIn('success_rate', metrics)
        self.assertIn('average_reward', metrics)

class TestMultiAgentCoordinator(unittest.TestCase):
    """Test MultiAgentCoordinator implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.coordinator = MultiAgentCoordinator()
        
        # Create mock agents
        self.agent1 = AIGamingAgent("agent1")
        self.agent2 = AIGamingAgent("agent2")
        self.agent3 = AIGamingAgent("agent3")
    
    def test_coordinator_creation(self):
        """Test coordinator creation"""
        self.assertEqual(len(self.coordinator.agents), 0)
        self.assertEqual(len(self.coordinator.communication_channels), 0)
    
    def test_register_agent(self):
        """Test registering agents"""
        self.coordinator.register_agent(self.agent1)
        self.coordinator.register_agent(self.agent2)
        
        self.assertIn(self.agent1, self.coordinator.agents)
        self.assertIn(self.agent2, self.coordinator.agents)
        self.assertEqual(len(self.coordinator.agents), 2)
    
    def test_unregister_agent(self):
        """Test unregistering agents"""
        self.coordinator.register_agent(self.agent1)
        self.coordinator.register_agent(self.agent2)
        
        self.coordinator.unregister_agent(self.agent1)
        
        self.assertNotIn(self.agent1, self.coordinator.agents)
        self.assertIn(self.agent2, self.coordinator.agents)
        self.assertEqual(len(self.coordinator.agents), 1)
    
    def test_create_communication_channel(self):
        """Test creating communication channels"""
        channel = self.coordinator.create_communication_channel("test_channel")
        
        self.assertIn("test_channel", self.coordinator.communication_channels)
        self.assertEqual(self.coordinator.communication_channels["test_channel"], channel)
    
    def test_send_message(self):
        """Test sending messages between agents"""
        self.coordinator.register_agent(self.agent1)
        self.coordinator.register_agent(self.agent2)
        
        channel = self.coordinator.create_communication_channel("test_channel")
        
        message = {"type": "coordinate", "data": "move_together"}
        success = self.coordinator.send_message("test_channel", self.agent1, self.agent2, message)
        
        self.assertTrue(success)
        self.assertIn(message, channel.messages)
    
    def test_get_agent_by_name(self):
        """Test getting agent by name"""
        self.coordinator.register_agent(self.agent1)
        self.coordinator.register_agent(self.agent2)
        
        found_agent = self.coordinator.get_agent_by_name("agent1")
        self.assertEqual(found_agent, self.agent1)
        
        not_found = self.coordinator.get_agent_by_name("nonexistent")
        self.assertIsNone(not_found)
    
    def test_coordinate_agents(self):
        """Test coordinating multiple agents"""
        self.coordinator.register_agent(self.agent1)
        self.coordinator.register_agent(self.agent2)
        self.coordinator.register_agent(self.agent3)
        
        # Mock behavior tree execution for all agents
        for agent in [self.agent1, self.agent2, self.agent3]:
            agent.set_behavior_tree(Mock())
            agent.behavior_tree.execute.return_value = True
        
        results = self.coordinator.coordinate_agents()
        
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(results.values()))
    
    def test_get_coordination_metrics(self):
        """Test getting coordination metrics"""
        self.coordinator.register_agent(self.agent1)
        self.coordinator.register_agent(self.agent2)
        
        # Create communication channel and send some messages
        channel = self.coordinator.create_communication_channel("test_channel")
        channel.messages = [
            {"sender": "agent1", "receiver": "agent2", "message": "test1"},
            {"sender": "agent2", "receiver": "agent1", "message": "test2"}
        ]
        
        metrics = self.coordinator.get_coordination_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('total_agents', metrics)
        self.assertIn('total_channels', metrics)
        self.assertIn('total_messages', metrics)
        self.assertEqual(metrics['total_agents'], 2)
        self.assertEqual(metrics['total_channels'], 1)
        self.assertEqual(metrics['total_messages'], 2)

def run_ai_agent_tests():
    """Run all AI agent framework tests"""
    print("🤖 Running AI Agent Framework Tests...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestAgentState,
        TestDecisionType,
        TestBehaviorNodeType,
        TestGameState,
        TestAgentDecision,
        TestLearningExperience,
        TestBehaviorNode,
        TestActionNode,
        TestConditionNode,
        TestSequenceNode,
        TestSelectorNode,
        TestDecoratorNode,
        TestBehaviorTree,
        TestDecisionEngine,
        TestAIGamingAgent,
        TestMultiAgentCoordinator
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 AI AGENT FRAMEWORK TEST RESULTS:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL AI AGENT FRAMEWORK TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME AI AGENT FRAMEWORK TESTS FAILED!")
        return False

if __name__ == "__main__":
    success = run_ai_agent_tests()
    sys.exit(0 if success else 1)
