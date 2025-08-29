from typing import Dict, Any
import json
import logging

import unittest

        import time
from ml_robot_bridge import MLRobotBridge, create_ml_robot_bridge, validate_ml_robot_integration
from ml_robot_config import MLTask, MLModelBlueprint, MLExperiment
from unittest.mock import Mock, patch, MagicMock

#!/usr/bin/env python3
"""
ML Robot Integration Test Module - Agent Cellphone V2
====================================================

Compatibility testing for ML robot system integration with core infrastructure.
Ensures V2 standards compliance and proper integration.

Follows V2 standards: ≤400 LOC, SRP, OOP principles, existing architecture testing.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""


# Import the integration module to test

# Import existing ML robot systems for testing

logger = logging.getLogger(__name__)


class MLRobotIntegrationTest(unittest.TestCase):
    """Test suite for ML robot system integration."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock coordinate manager
        self.mock_coordinate_manager = Mock()
        self.mock_coordinate_manager.get_agent_count.return_value = 8
        self.mock_coordinate_manager.get_agent_coordinates.return_value = {
            "input_x": 500,
            "input_y": 300,
            "status": "active"
        }
        
        # Mock messaging system
        self.mock_messaging = Mock()
        self.mock_messaging.send_message.return_value = Mock(success=True)
        
        # Mock agent coordinator
        self.mock_agent_coordinator = Mock()
        self.mock_agent_coordinator.register_task = Mock(return_value=True)
        
        # Create bridge with mocked dependencies
        with patch('src.ai_ml.ml_robot_bridge.UnifiedPyAutoGUIMessaging', return_value=self.mock_messaging), \
             patch('src.ai_ml.ml_robot_bridge.AgentCoordinatorOrchestrator', return_value=self.mock_agent_coordinator):
            self.bridge = MLRobotBridge(self.mock_coordinate_manager)

    def test_bridge_initialization(self):
        """Test ML robot bridge initialization."""
        self.assertIsNotNone(self.bridge)
        self.assertEqual(self.bridge.integration_status["coordinate_manager"], "CONNECTED")
        self.assertEqual(self.bridge.integration_status["messaging_system"], "CONNECTED")
        self.assertEqual(self.bridge.integration_status["agent_coordinator"], "CONNECTED")

    def test_ml_task_creation_with_integration(self):
        """Test ML task creation with core system integration."""
        # Test data
        task_type = "classification"
        description = "Test classification task"
        dataset_info = {"size": 100, "features": 10}
        model_requirements = {"accuracy": 0.9, "framework": "scikit_learn"}
        
        # Mock ML robot creator
        mock_task = Mock(spec=MLTask)
        mock_task.task_id = "test_task_001"
        mock_blueprint = Mock(spec=MLModelBlueprint)
        
        with patch.object(self.bridge.ml_creator, 'create_task', return_value=mock_task), \
             patch.object(self.bridge.ml_creator, 'generate_model_blueprint', return_value=mock_blueprint):
            
            task, integration_result = self.bridge.create_ml_task_with_integration(
                task_type=task_type,
                description=description,
                dataset_info=dataset_info,
                model_requirements=model_requirements
            )
            
            # Verify task creation
            self.assertEqual(task.task_id, "test_task_001")
            
            # Verify integration
            self.assertTrue(integration_result["coordination_updated"])

    def test_ml_experiment_execution_with_monitoring(self):
        """Test ML experiment execution with monitoring integration."""
        # Test data
        mock_task = Mock(spec=MLTask)
        mock_blueprint = Mock(spec=MLModelBlueprint)
        mock_experiment = Mock(spec=MLExperiment)
        mock_experiment.experiment_id = "test_exp_001"
        mock_experiment.evaluation_results = {"accuracy": 0.85}
        
        # Mock ML robot processor
        with patch.object(self.bridge.ml_processor, 'execute_experiment', return_value=mock_experiment):
            
            experiment, monitoring_result = self.bridge.execute_ml_experiment_with_monitoring(
                task=mock_task,
                blueprint=mock_blueprint
            )
            
            # Verify experiment execution
            self.assertEqual(experiment.experiment_id, "test_exp_001")
            
            # Verify monitoring
            self.assertTrue(monitoring_result["experiment_tracked"])
            self.assertTrue(monitoring_result["performance_monitored"])
            self.assertEqual(monitoring_result["integration_health"], "GOOD")

    def test_integration_status_reporting(self):
        """Test integration status reporting."""
        status = self.bridge.get_integration_status()
        
        # Verify status structure
        self.assertIn("coordinate_manager", status)
        self.assertIn("messaging_system", status)
        self.assertIn("agent_coordinator", status)
        self.assertIn("ml_robot_systems", status)
        self.assertIn("core_infrastructure", status)
        
        # Verify ML robot systems status
        ml_systems = status["ml_robot_systems"]
        self.assertEqual(ml_systems["creator"], "OPERATIONAL")
        self.assertEqual(ml_systems["processor"], "OPERATIONAL")
        self.assertEqual(ml_systems["framework_manager"], "OPERATIONAL")
        self.assertEqual(ml_systems["model_manager"], "OPERATIONAL")

    def test_ml_status_update_sending(self):
        """Test ML status update sending via messaging system."""
        recipient = "Agent-2"
        status_type = "experiment_started"
        content = {"task_id": "test_001", "status": "running"}
        
        result = self.bridge.send_ml_status_update(
            recipient=recipient,
            status_type=status_type,
            content=content
        )
        
        # Verify message was sent
        self.assertTrue(result)
        self.mock_messaging.send_message.assert_called_once()

    def test_integration_compliance_validation(self):
        """Test integration compliance validation against V2 standards."""
        compliance = self.bridge.validate_integration_compliance()
        
        # Verify V2 standards compliance
        v2_standards = compliance["v2_standards"]
        self.assertEqual(v2_standards["single_responsibility"], "PASS")
        self.assertEqual(v2_standards["oop_design"], "PASS")
        self.assertEqual(v2_standards["existing_architecture"], "PASS")
        self.assertEqual(v2_standards["no_duplication"], "PASS")
        
        # Verify architecture compliance
        arch_compliance = compliance["architecture_compliance"]
        self.assertEqual(arch_compliance["coordinate_manager_integration"], "PASS")
        self.assertEqual(arch_compliance["messaging_system_integration"], "PASS")
        self.assertEqual(arch_compliance["agent_coordinator_integration"], "PASS")
        self.assertEqual(arch_compliance["ml_robot_system_preservation"], "PASS")
        
        # Verify overall score
        self.assertEqual(compliance["overall_score"], 100.0)

    def test_factory_function_creation(self):
        """Test factory function for creating ML robot bridge."""
        bridge = create_ml_robot_bridge(self.mock_coordinate_manager)
        
        self.assertIsInstance(bridge, MLRobotBridge)
        self.assertEqual(bridge.coordinate_manager, self.mock_coordinate_manager)

    def test_validation_function(self):
        """Test validation function for ML robot integration."""
        compliance = validate_ml_robot_integration(self.bridge)
        
        self.assertIn("overall_score", compliance)
        self.assertEqual(compliance["overall_score"], 100.0)

    def test_error_handling_in_task_creation(self):
        """Test error handling in ML task creation."""
        # Mock failure in ML robot creator
        with patch.object(self.bridge.ml_creator, 'create_task', side_effect=Exception("Test error")):
            with self.assertRaises(Exception):
                self.bridge.create_ml_task_with_integration(
                    task_type="test",
                    description="test",
                    dataset_info={},
                    model_requirements={}
                )

    def test_error_handling_in_experiment_execution(self):
        """Test error handling in ML experiment execution."""
        # Mock failure in ML robot processor
        mock_task = Mock(spec=MLTask)
        mock_blueprint = Mock(spec=MLModelBlueprint)
        
        with patch.object(self.bridge.ml_processor, 'execute_experiment', side_effect=Exception("Test error")):
            with self.assertRaises(Exception):
                self.bridge.execute_ml_experiment_with_monitoring(
                    task=mock_task,
                    blueprint=mock_blueprint
                )

    def test_performance_monitoring_alert(self):
        """Test performance monitoring alert system."""
        # Test data with low performance
        mock_task = Mock(spec=MLTask)
        mock_blueprint = Mock(spec=MLModelBlueprint)
        mock_experiment = Mock(spec=MLExperiment)
        mock_experiment.experiment_id = "test_exp_002"
        mock_experiment.evaluation_results = {"accuracy": 0.3}  # Low performance
        
        # Mock ML robot processor
        with patch.object(self.bridge.ml_processor, 'execute_experiment', return_value=mock_experiment):
            
            experiment, monitoring_result = self.bridge.execute_ml_experiment_with_monitoring(
                task=mock_task,
                blueprint=mock_blueprint
            )
            
            # Verify performance alert
            self.assertEqual(monitoring_result["integration_health"], "WARNING")
            self.assertIn("performance_alert", monitoring_result)
            self.assertIn("Low performance: 0.3", monitoring_result["performance_alert"])


class MLRobotIntegrationPerformanceTest(unittest.TestCase):
    """Performance testing for ML robot integration."""

    def setUp(self):
        """Set up performance test fixtures."""
        self.mock_coordinate_manager = Mock()
        self.mock_coordinate_manager.get_agent_count.return_value = 8
        
        with patch('src.ai_ml.ml_robot_bridge.UnifiedPyAutoGUIMessaging'), \
             patch('src.ai_ml.ml_robot_bridge.AgentCoordinatorOrchestrator'):
            self.bridge = MLRobotBridge(self.mock_coordinate_manager)

    def test_integration_health_update_performance(self):
        """Test performance of integration health updates."""
        
        start_time = time.time()
        
        # Perform multiple health updates
        for _ in range(100):
            self.bridge._update_integration_health()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete 100 updates in under 1 second
        self.assertLess(execution_time, 1.0, f"Health updates took {execution_time:.3f}s, expected <1.0s")

    def test_status_reporting_performance(self):
        """Test performance of status reporting."""
        
        start_time = time.time()
        
        # Generate multiple status reports
        for _ in range(50):
            status = self.bridge.get_integration_status()
            self.assertIsNotNone(status)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete 50 status reports in under 0.5 seconds
        self.assertLess(execution_time, 0.5, f"Status reporting took {execution_time:.3f}s, expected <0.5s")


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
