from datetime import datetime

import unittest

from .decision_algorithms import DecisionAlgorithmExecutor, AlgorithmPerformance
from .decision_core import DecisionCore, DecisionCoreConfig
from .decision_manager import DecisionManager, DecisionManagerConfig
from .decision_metrics import DecisionMetrics
from .decision_rules import DecisionRuleEngine, RuleEvaluationResult, RulePerformance
from .decision_types import (
from .decision_workflows import DecisionWorkflowExecutor, WorkflowStep, WorkflowExecution
from unittest.mock import Mock, patch
import time
import uuid

#!/usr/bin/env python3
"""
Modular Decision System Tests - Comprehensive Testing Suite
==========================================================

Tests all modular decision system components including core,
algorithms, workflows, and rules. Ensures V2 standards compliance.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""


# Import modular decision system components

# Import decision models
    DecisionRequest, DecisionResult, DecisionContext, DecisionType,
    DecisionPriority, DecisionStatus, DecisionConfidence, DecisionAlgorithm,
    DecisionRule, DecisionWorkflow
)


class TestDecisionCore(unittest.TestCase):
    """Test DecisionCore functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.core = DecisionCore("test_core", "Test Decision Core", "Test core for unit testing")
    
    def tearDown(self):
        """Clean up test environment."""
        if self.core.is_running:
            self.core.stop()
    
    def test_initialization(self):
        """Test core initialization."""
        self.assertIsNotNone(self.core)
        self.assertEqual(self.core.manager_id, "test_core")
        self.assertEqual(self.core.name, "Test Decision Core")
        self.assertIsInstance(self.core.config, DecisionCoreConfig)
    
    def test_start_stop(self):
        """Test core start and stop functionality."""
        # Test start
        self.assertTrue(self.core.start())
        self.assertTrue(self.core.is_running)
        
        # Test stop
        self.core.stop()
        self.assertFalse(self.core.is_running)
    
    def test_make_decision(self):
        """Test decision making functionality."""
        self.core.start()
        
        # Create test decision
        result = self.core.make_decision(
            decision_type=DecisionType.TASK_ASSIGNMENT,
            requester="test_agent",
            parameters={"task": "test_task"},
            priority=DecisionPriority.MEDIUM
        )
        
        self.assertIsInstance(result, DecisionResult)
        self.assertEqual(result.decision_type, DecisionType.TASK_ASSIGNMENT)
        self.assertIsNotNone(result.decision_id)
    
    def test_decision_tracking(self):
        """Test decision tracking functionality."""
        self.core.start()
        
        # Make a decision
        result = self.core.make_decision(
            decision_type=DecisionType.PRIORITY_DETERMINATION,
            requester="test_agent",
            parameters={"priority": "high"},
            priority=DecisionPriority.HIGH
        )
        
        # Check tracking
        self.assertEqual(len(self.core.active_decisions), 0)  # Should be cleaned up
        self.assertEqual(len(self.core.decision_history), 1)
        self.assertEqual(self.core.total_decisions_made, 1)
        self.assertEqual(self.core.successful_decisions, 1)


class TestDecisionAlgorithmExecutor(unittest.TestCase):
    """Test DecisionAlgorithmExecutor functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.executor = DecisionAlgorithmExecutor()
        self.executor.initialize()
    
    def test_initialization(self):
        """Test executor initialization."""
        self.assertIsNotNone(self.executor)
        self.assertGreater(len(self.executor.algorithms), 0)
        self.assertIn("rule_based", self.executor.algorithms)
        self.assertIn("learning_based", self.executor.algorithms)
    
    def test_algorithm_selection(self):
        """Test algorithm selection functionality."""
        # Test selection for task assignment
        algorithm = self.executor.select_algorithm_for_decision_type(DecisionType.TASK_ASSIGNMENT)
        self.assertIsInstance(algorithm, DecisionAlgorithm)
        self.assertIn(DecisionType.TASK_ASSIGNMENT, algorithm.decision_types)
    
    def test_algorithm_execution(self):
        """Test algorithm execution functionality."""
        # Get a test algorithm
        algorithm = self.executor.get_algorithm("rule_based")
        self.assertIsNotNone(algorithm)
        
        # Create test request and context
        request = DecisionRequest(
            decision_type=DecisionType.TASK_ASSIGNMENT,
            requester="test_agent",
            parameters={"task": "test_task"},
            priority=DecisionPriority.MEDIUM
        )
        
        context = DecisionContext(
            decision_id=request.decision_id,
            decision_type=request.decision_type,
            timestamp=datetime.now().isoformat(),
            agent_id=request.requester,
            context_data=request.parameters,
            constraints=[],
            objectives=[],
            risk_factors=[]
        )
        
        # Execute algorithm
        result = self.executor.execute_algorithm(algorithm, request, context)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "algorithm_execution_failed")
    
    def test_advanced_algorithm_creation(self):
        """Test advanced algorithm creation."""
        # Create neural network algorithm
        algorithm_id = self.executor.create_advanced_algorithm("neural_network", {
            "layers": [128, 64, 32],
            "activation": "tanh",
            "learning_rate": 0.01
        })
        
        self.assertIsNotNone(algorithm_id)
        self.assertIn(algorithm_id, self.executor.algorithms)
        
        algorithm = self.executor.get_algorithm(algorithm_id)
        self.assertEqual(algorithm.algorithm_id, algorithm_id)
        self.assertIn("neural_network", algorithm.name.lower())


class TestDecisionWorkflowExecutor(unittest.TestCase):
    """Test DecisionWorkflowExecutor functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.executor = DecisionWorkflowExecutor()
        self.executor.initialize()
    
    def test_initialization(self):
        """Test executor initialization."""
        self.assertIsNotNone(self.executor)
        self.assertGreater(len(self.executor.workflows), 0)
        self.assertIn("standard_decision", self.executor.workflows)
        self.assertIn("collaborative_decision", self.executor.workflows)
    
    def test_workflow_selection(self):
        """Test workflow selection functionality."""
        # Test selection for different decision types
        workflow = self.executor.select_workflow_for_decision_type("conflict_resolution")
        self.assertIsInstance(workflow, DecisionWorkflow)
        self.assertIn("collaborative", workflow.name.lower())
    
    def test_workflow_from_template(self):
        """Test workflow creation from template."""
        # Create workflow from simple validation template
        workflow_id = self.executor.create_workflow_from_template(
            "simple_validation",
            "Test Workflow",
            "Test workflow created from template"
        )
        
        self.assertIsNotNone(workflow_id)
        self.assertIn(workflow_id, self.executor.workflows)
        
        workflow = self.executor.get_workflow(workflow_id)
        self.assertEqual(workflow.name, "Test Workflow")
        self.assertGreater(len(workflow.steps), 0)
    
    def test_workflow_execution(self):
        """Test workflow execution functionality."""
        # Get a test workflow
        workflow = self.executor.get_workflow("standard_decision")
        self.assertIsNotNone(workflow)
        
        # Create test request and algorithm
        request = DecisionRequest(
            decision_type=DecisionType.TASK_ASSIGNMENT,
            requester="test_agent",
            parameters={"task": "test_task"},
            priority=DecisionPriority.MEDIUM
        )
        
        algorithm = DecisionAlgorithm(
            algorithm_id="test_algorithm",
            name="Test Algorithm",
            description="Test algorithm for workflow execution",
            decision_types=[DecisionType.TASK_ASSIGNMENT],
            parameters={"confidence_threshold": 0.8}
        )
        
        # Execute workflow
        result = self.executor.execute_workflow(workflow, request, algorithm, None)
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "workflow_execution_failed")


class TestDecisionRuleEngine(unittest.TestCase):
    """Test DecisionRuleEngine functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.engine = DecisionRuleEngine()
        self.engine.initialize()
    
    def test_initialization(self):
        """Test engine initialization."""
        self.assertIsNotNone(self.engine)
        self.assertGreater(len(self.engine.rules), 0)
        self.assertIn("high_priority_first", self.engine.rules)
        self.assertIn("collaborative_conflict", self.engine.rules)
    
    def test_rule_evaluation(self):
        """Test rule evaluation functionality."""
        # Create test context
        context = DecisionContext(
            decision_id=str(uuid.uuid4()),
            decision_type=DecisionType.PRIORITY_DETERMINATION,
            timestamp=datetime.now().isoformat(),
            agent_id="test_agent",
            context_data={"priority": 5},  # High priority
            constraints=[],
            objectives=[],
            risk_factors=[]
        )
        
        # Evaluate rules
        results = self.engine.evaluate_rules(context, DecisionType.PRIORITY_DETERMINATION)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # Check if high priority rule matched
        high_priority_matched = any(
            result.matched and "high_priority" in result.rule_id
            for result in results
        )
        self.assertTrue(high_priority_matched)
    
    def test_rule_management(self):
        """Test rule management functionality."""
        # Create test rule
        test_rule = DecisionRule(
            rule_id="test_rule",
            name="Test Rule",
            description="Test rule for unit testing",
            condition="priority >= 3",
            action="test_action",
            priority=2,
            decision_types=[DecisionType.TASK_ASSIGNMENT]
        )
        
        # Add rule
        self.assertTrue(self.engine.add_rule(test_rule))
        self.assertIn("test_rule", self.engine.rules)
        
        # Remove rule
        self.assertTrue(self.engine.remove_rule("test_rule"))
        self.assertNotIn("test_rule", self.engine.rules)
    
    def test_rule_categories(self):
        """Test rule categorization functionality."""
        categories = self.engine.get_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
        
        # Test getting rules by category
        priority_rules = self.engine.get_rules_by_category("priority")
        self.assertIsInstance(priority_rules, list)
        self.assertGreater(len(priority_rules), 0)


class TestDecisionManager(unittest.TestCase):
    """Test DecisionManager integration functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.manager = DecisionManager("test_manager", "Test Decision Manager", "Test manager for unit testing")
    
    def tearDown(self):
        """Clean up test environment."""
        if self.manager.is_running:
            self.manager.stop()
    
    def test_initialization(self):
        """Test manager initialization."""
        self.assertIsNotNone(self.manager)
        self.assertEqual(self.manager.manager_id, "test_manager")
        self.assertEqual(self.manager.name, "Test Decision Manager")
        self.assertIsInstance(self.manager.decision_config, DecisionManagerConfig)
    
    def test_component_integration(self):
        """Test component integration."""
        # Check that all components are available
        self.assertIsNotNone(self.manager.decision_core)
        self.assertIsNotNone(self.manager.algorithm_executor)
        self.assertIsNotNone(self.manager.workflow_executor)
        self.assertIsNotNone(self.manager.rule_engine)
    
    def test_start_stop(self):
        """Test manager start and stop functionality."""
        # Test start
        self.assertTrue(self.manager.start())
        self.assertTrue(self.manager.is_running)
        
        # Test stop
        self.manager.stop()
        self.assertFalse(self.manager.is_running)
    
    def test_decision_making_integration(self):
        """Test integrated decision making."""
        self.manager.start()
        
        # Make a decision through the manager
        result = self.manager.make_decision(
            decision_type=DecisionType.TASK_ASSIGNMENT,
            requester="test_agent",
            parameters={"task": "test_task"},
            priority=DecisionPriority.MEDIUM
        )
        
        self.assertIsInstance(result, DecisionResult)
        self.assertEqual(result.decision_type, DecisionType.TASK_ASSIGNMENT)
    
    def test_intelligent_rule_engine(self):
        """Test intelligent rule engine functionality."""
        self.manager.start()
        
        # Create test request
        request = DecisionRequest(
            decision_type=DecisionType.CONFLICT_RESOLUTION,
            requester="test_agent",
            parameters={"conflict_type": "resource_dispute"},
            priority=DecisionPriority.HIGH
        )
        
        # Execute intelligent rule engine
        result = self.manager.execute_intelligent_rule_engine(request)
        self.assertIsInstance(result, DecisionResult)
        self.assertEqual(result.decision_type, DecisionType.CONFLICT_RESOLUTION)
    
    def test_collaborative_decision(self):
        """Test collaborative decision functionality."""
        self.manager.start()
        
        # Create test request
        request = DecisionRequest(
            decision_type=DecisionType.AGENT_COORDINATION,
            requester="test_agent",
            parameters={"coordination_type": "task_distribution"},
            priority=DecisionPriority.MEDIUM
        )
        
        # Coordinate collaborative decision
        participant_agents = ["agent-1", "agent-2", "agent-3"]
        result = self.manager.coordinate_collaborative_decision(request, participant_agents)
        
        self.assertIsInstance(result, DecisionResult)
        self.assertEqual(result.decision_type, DecisionType.AGENT_COORDINATION)
    
    def test_risk_assessment(self):
        """Test risk assessment functionality."""
        self.manager.start()
        
        # Create test context
        context = DecisionContext(
            decision_id=str(uuid.uuid4()),
            decision_type=DecisionType.RISK_ASSESSMENT,
            timestamp=datetime.now().isoformat(),
            agent_id="test_agent",
            context_data={"stakes": "high", "deadline": "tight"},
            constraints=["time_limit", "budget_limit"],
            objectives=["quality", "speed"],
            risk_factors=["unknown_environment", "complex_requirements"]
        )
        
        # Assess risk
        risk_assessment = self.manager.assess_decision_risk(context)
        self.assertIsInstance(risk_assessment, dict)
        self.assertIn("risk_level", risk_assessment)
        self.assertIn("risk_score", risk_assessment)
        self.assertIn("mitigation_strategies", risk_assessment)
    
    def test_workflow_creation(self):
        """Test workflow creation from template."""
        self.manager.start()
        
        # Create workflow from template
        workflow_id = self.manager.create_workflow_from_template(
            "collaborative_resolution",
            "Test Collaborative Workflow",
            "Test workflow for collaborative decisions"
        )
        
        self.assertIsNotNone(workflow_id)
        
        # Verify workflow was created
        workflow = self.manager.workflow_executor.get_workflow(workflow_id)
        self.assertIsNotNone(workflow)
        self.assertEqual(workflow.name, "Test Collaborative Workflow")
    
    def test_rule_management(self):
        """Test rule management through manager."""
        self.manager.start()
        
        # Create test rule
        test_rule = DecisionRule(
            rule_id="test_manager_rule",
            name="Test Manager Rule",
            description="Test rule managed through decision manager",
            condition="priority >= 4",
            action="urgent_processing",
            priority=1,
            decision_types=[DecisionType.TASK_ASSIGNMENT]
        )
        
        # Add rule through manager
        self.assertTrue(self.manager.add_decision_rule(test_rule))
        
        # Verify rule was added
        self.assertIn("test_manager_rule", self.manager.rule_engine.rules)
        
        # Remove rule
        self.assertTrue(self.manager.rule_engine.remove_rule("test_manager_rule"))
    
    def test_rule_evaluation(self):
        """Test rule evaluation through manager."""
        self.manager.start()
        
        # Create test context
        context = DecisionContext(
            decision_id=str(uuid.uuid4()),
            decision_type=DecisionType.TASK_ASSIGNMENT,
            timestamp=datetime.now().isoformat(),
            agent_id="test_agent",
            context_data={"priority": 5},
            constraints=[],
            objectives=[],
            risk_factors=[]
        )
        
        # Evaluate rules through manager
        results = self.manager.evaluate_decision_rules(context, DecisionType.TASK_ASSIGNMENT)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
    
    def test_integration_health(self):
        """Test integration health monitoring."""
        self.manager.start()
        
        # Get integration health
        health = self.manager.get_integration_health()
        self.assertIsInstance(health, dict)
        self.assertIn("overall_health", health)
        self.assertIn("core_system", health)
        self.assertIn("algorithm_system", health)
        self.assertIn("workflow_system", health)
        self.assertIn("rule_system", health)
        
        # Check that all systems are healthy
        self.assertEqual(health["overall_health"], "healthy")
    
    def test_comprehensive_status(self):
        """Test comprehensive status reporting."""
        self.manager.start()
        
        # Get comprehensive status
        status = self.manager.get_decision_status()
        self.assertIsInstance(status, dict)
        
        # Check core status
        self.assertIn("decision_operations", status)
        self.assertIn("integration_status", status)
        
        # Check component statuses
        self.assertIn("algorithm_system", status)
        self.assertIn("workflow_system", status)
        self.assertIn("rule_system", status)
        
        # Check modular architecture info
        self.assertIn("modular_architecture", status)
        modular_arch = status["modular_architecture"]
        self.assertEqual(modular_arch["core_system"], "DecisionCore")
        self.assertEqual(modular_arch["algorithm_system"], "DecisionAlgorithmExecutor")
        self.assertEqual(modular_arch["workflow_system"], "DecisionWorkflowExecutor")
        self.assertEqual(modular_arch["rule_system"], "DecisionRuleEngine")


class TestModularSystemIntegration(unittest.TestCase):
    """Test complete modular system integration."""
    
    def setUp(self):
        """Set up test environment."""
        self.manager = DecisionManager("integration_test", "Integration Test Manager", "Test manager for integration testing")
        self.manager.start()
    
    def tearDown(self):
        """Clean up test environment."""
        if self.manager.is_running:
            self.manager.stop()
    
    def test_end_to_end_decision_workflow(self):
        """Test complete end-to-end decision workflow."""
        # Create advanced algorithm
        algorithm_id = self.manager.algorithm_executor.create_advanced_algorithm("neural_network", {
            "layers": [64, 32, 16],
            "activation": "relu",
            "learning_rate": 0.001
        })
        
        # Create custom workflow
        workflow_id = self.manager.create_workflow_from_template(
            "complex_analysis",
            "Custom Analysis Workflow",
            "Custom workflow for complex decision analysis"
        )
        
        # Create custom rule
        custom_rule = DecisionRule(
            rule_id="custom_analysis_rule",
            name="Custom Analysis Rule",
            description="Custom rule for analysis decisions",
            condition="decision_type == 'learning_strategy'",
            action="use_custom_workflow",
            priority=1,
            decision_types=[DecisionType.LEARNING_STRATEGY]
        )
        self.manager.add_decision_rule(custom_rule)
        
        # Make decision using all components
        result = self.manager.make_decision(
            decision_type=DecisionType.LEARNING_STRATEGY,
            requester="test_agent",
            parameters={"strategy_type": "adaptive", "complexity": "high"},
            priority=DecisionPriority.HIGH,
            algorithm_id=algorithm_id,
            workflow_id=workflow_id
        )
        
        # Verify result
        self.assertIsInstance(result, DecisionResult)
        self.assertEqual(result.decision_type, DecisionType.LEARNING_STRATEGY)
        self.assertIsNotNone(result.decision_id)
        
        # Check that all components were involved
        self.assertGreater(self.manager.decision_core.total_decisions_made, 0)
        self.assertIn(algorithm_id, self.manager.algorithm_executor.algorithms)
        self.assertIn(workflow_id, self.manager.workflow_executor.workflows)
        self.assertIn("custom_analysis_rule", self.manager.rule_engine.rules)
    
    def test_system_performance_under_load(self):
        """Test system performance under load."""
        # Make multiple decisions rapidly
        start_time = time.time()
        
        decision_results = []
        for i in range(10):
            result = self.manager.make_decision(
                decision_type=DecisionType.TASK_ASSIGNMENT,
                requester=f"test_agent_{i}",
                parameters={"task": f"test_task_{i}"},
                priority=DecisionPriority.MEDIUM
            )
            decision_results.append(result)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify all decisions completed
        self.assertEqual(len(decision_results), 10)
        self.assertTrue(all(isinstance(r, DecisionResult) for r in decision_results))
        
        # Verify performance (should complete in reasonable time)
        self.assertLess(execution_time, 5.0)  # Should complete in under 5 seconds
        
        # Check system metrics
        status = self.manager.get_decision_status()
        self.assertEqual(status["decision_operations"]["total"], 10)
        self.assertEqual(status["decision_operations"]["successful"], 10)
        self.assertEqual(status["decision_operations"]["failed"], 0)


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
