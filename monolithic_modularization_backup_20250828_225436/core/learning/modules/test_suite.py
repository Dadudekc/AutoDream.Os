from datetime import datetime
from typing import Dict, Any
import logging

import unittest

        from ..models import LearningStrategy, LearningMode
from .data_processing import DataProcessingModule, DataProcessingResult
from .interfaces import UnifiedLearningInterface
from .learning_algorithms import LearningAlgorithmsModule
from .model_management import ModelManagementModule, ModelType, ModelStatus

#!/usr/bin/env python3
"""
Learning Modules Test Suite - Agent Cellphone V2
===============================================

Comprehensive testing for all modularized learning components.
Follows V2 standards: thorough testing, validation, quality assurance.

**Author:** Captain Agent-3 (MODULAR-007 Contract)
**Created:** Current Sprint
**Status:** ACTIVE - TESTING IN PROGRESS
"""




class TestLearningAlgorithmsModule(unittest.TestCase):
    """Test suite for LearningAlgorithmsModule"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.algorithms_module = LearningAlgorithmsModule()
        
        # Create test learning strategy
        self.test_strategy = LearningStrategy(
            strategy_id="test_strategy",
            name="Test Strategy",
            description="Test learning strategy for unit testing",
            learning_modes=[LearningMode.ADAPTIVE],
            parameters={"adaptation_rate": 0.15, "performance_threshold": 0.85}
        )
    
    def test_module_initialization(self):
        """Test module initialization"""
        self.assertIsNotNone(self.algorithms_module)
        self.assertEqual(len(self.algorithms_module.algorithms), 0)
        self.assertEqual(len(self.algorithms_module.performance_history), 0)
    
    def test_strategy_registration(self):
        """Test learning strategy registration"""
        result = self.algorithms_module.register_learning_strategy(self.test_strategy)
        self.assertTrue(result)
        self.assertIn("test_strategy", self.algorithms_module.algorithms)
        self.assertIn("test_strategy", self.algorithms_module.performance_history)
    
    def test_strategy_execution(self):
        """Test learning strategy execution"""
        # Register strategy first
        self.algorithms_module.register_learning_strategy(self.test_strategy)
        
        # Execute strategy
        result = self.algorithms_module.execute_learning_strategy(
            "test_strategy",
            {"test_input": "value"},
            "test_context"
        )
        
        self.assertIsNotNone(result)
        self.assertIn("performance_score", result)
        self.assertIn("execution_mode", result)
        self.assertEqual(result["execution_mode"], "adaptive")
    
    def test_performance_tracking(self):
        """Test performance tracking functionality"""
        # Register and execute strategy multiple times
        self.algorithms_module.register_learning_strategy(self.test_strategy)
        
        for i in range(5):
            self.algorithms_module.execute_learning_strategy(
                "test_strategy",
                {"test_input": f"value_{i}"},
                "test_context"
            )
        
        # Check performance history
        performance = self.algorithms_module.get_algorithm_performance("test_strategy")
        self.assertIsNotNone(performance)
        self.assertEqual(performance["total_executions"], 5)
        self.assertGreater(len(performance["recent_performance"]), 0)
    
    def test_parameter_optimization(self):
        """Test algorithm parameter optimization"""
        # Register strategy
        self.algorithms_module.register_learning_strategy(self.test_strategy)
        
        # Execute multiple times to build performance history
        for i in range(10):
            self.algorithms_module.execute_learning_strategy(
                "test_strategy",
                {"test_input": f"value_{i}"},
                "test_context"
            )
        
        # Test optimization
        result = self.algorithms_module.optimize_algorithm_parameters("test_strategy")
        self.assertTrue(result)
    
    def test_module_test_function(self):
        """Test the module's built-in test function"""
        result = self.algorithms_module.run_module_test()
        self.assertTrue(result)


class TestDataProcessingModule(unittest.TestCase):
    """Test suite for DataProcessingModule"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data_processing_module = DataProcessingModule()
        
        # Test data
        self.valid_test_data = {
            "input_data": {"test_input": "value"},
            "output_data": {"test_output": "result"},
            "performance_score": 0.85,
            "context": "test"
        }
        
        self.invalid_test_data = {
            "input_data": "not_a_dict",
            "output_data": {"test_output": "result"}
        }
    
    def test_module_initialization(self):
        """Test module initialization"""
        self.assertIsNotNone(self.data_processing_module)
        self.assertEqual(self.data_processing_module.processing_stats["total_processed"], 0)
        self.assertEqual(len(self.data_processing_module.data_cache), 0)
    
    def test_valid_data_processing(self):
        """Test processing of valid data"""
        result = self.data_processing_module.process_learning_data(
            self.valid_test_data,
            "test",
            "standard"
        )
        
        self.assertTrue(result.success)
        self.assertGreater(result.data_quality_score, 0.5)
        self.assertIsNotNone(result.processed_data)
        self.assertGreater(result.processing_time_ms, 0)
    
    def test_invalid_data_processing(self):
        """Test processing of invalid data"""
        result = self.data_processing_module.process_learning_data(
            self.invalid_test_data,
            "test",
            "strict"
        )
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)
        self.assertEqual(result.data_quality_score, 0.0)
    
    def test_data_validation_levels(self):
        """Test different validation levels"""
        # Standard validation
        result_standard = self.data_processing_module.process_learning_data(
            self.valid_test_data,
            "test",
            "standard"
        )
        self.assertTrue(result_standard.success)
        
        # Strict validation
        result_strict = self.data_processing_module.process_learning_data(
            self.valid_test_data,
            "test",
            "strict"
        )
        self.assertTrue(result_strict.success)
    
    def test_context_specific_processing(self):
        """Test context-specific data processing"""
        # Test collaborative context
        collaborative_data = self.valid_test_data.copy()
        collaborative_data["collaborators"] = ["agent1", "agent2", "agent3"]
        
        result = self.data_processing_module.process_learning_data(
            collaborative_data,
            "collaborative",
            "standard"
        )
        
        self.assertTrue(result.success)
        self.assertIn("_collaboration_metrics", result.processed_data)
    
    def test_cache_operations(self):
        """Test data cache operations"""
        # Process data to populate cache
        result = self.data_processing_module.process_learning_data(
            self.valid_test_data,
            "test",
            "standard"
        )
        
        # Check cache size
        self.assertGreater(len(self.data_processing_module.data_cache), 0)
        
        # Get cache key
        cache_key = list(self.data_processing_module.data_cache.keys())[0]
        
        # Retrieve cached data
        cached_data = self.data_processing_module.get_cached_data(cache_key)
        self.assertIsNotNone(cached_data)
        
        # Test cache clearing
        cleared_count = self.data_processing_module.clear_cache(older_than_hours=0)
        self.assertGreater(cleared_count, 0)
    
    def test_processing_statistics(self):
        """Test processing statistics"""
        # Process some data first
        self.data_processing_module.process_learning_data(
            self.valid_test_data,
            "test",
            "standard"
        )
        
        # Get statistics
        stats = self.data_processing_module.get_processing_statistics()
        
        self.assertIn("total_processed", stats)
        self.assertIn("successful_processing", stats)
        self.assertIn("success_rate_percent", stats)
        self.assertGreater(stats["total_processed"], 0)
    
    def test_module_test_function(self):
        """Test the module's built-in test function"""
        result = self.data_processing_module.run_module_test()
        self.assertTrue(result)


class TestModelManagementModule(unittest.TestCase):
    """Test suite for ModelManagementModule"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.model_management_module = ModelManagementModule()
        
        # Test model
        self.test_model = {"test": "data"}
    
    def test_module_initialization(self):
        """Test module initialization"""
        self.assertIsNotNone(self.model_management_module)
        self.assertEqual(len(self.model_management_module.models), 0)
        self.assertEqual(len(self.model_management_module.model_metadata), 0)
    
    def test_model_registration(self):
        """Test model registration"""
        model_id = self.model_management_module.register_model(
            self.test_model,
            ModelType.LEARNING_STRATEGY,
            "Test Model",
            "Test model for unit testing"
        )
        
        self.assertIsNotNone(model_id)
        self.assertIn(model_id, self.model_management_module.models)
        self.assertIn(model_id, self.model_management_module.model_metadata)
    
    def test_model_activation(self):
        """Test model activation"""
        # Register model first
        model_id = self.model_management_module.register_model(
            self.test_model,
            ModelType.LEARNING_STRATEGY,
            "Test Model",
            "Test model for unit testing"
        )
        
        # Activate model
        result = self.model_management_module.activate_model(model_id)
        self.assertTrue(result)
        
        # Check status
        model_info = self.model_management_module.get_model_info(model_id)
        self.assertEqual(model_info["status"], "active")
    
    def test_model_deactivation(self):
        """Test model deactivation"""
        # Register and activate model
        model_id = self.model_management_module.register_model(
            self.test_model,
            ModelType.LEARNING_STRATEGY,
            "Test Model",
            "Test model for unit testing"
        )
        self.model_management_module.activate_model(model_id)
        
        # Deactivate model
        result = self.model_management_module.deactivate_model(model_id)
        self.assertTrue(result)
        
        # Check status
        model_info = self.model_management_module.get_model_info(model_id)
        self.assertEqual(model_info["status"], "inactive")
    
    def test_performance_tracking(self):
        """Test model performance tracking"""
        # Register model
        model_id = self.model_management_module.register_model(
            self.test_model,
            ModelType.LEARNING_STRATEGY,
            "Test Model",
            "Test model for unit testing"
        )
        
        # Update performance multiple times
        for i in range(5):
            self.model_management_module.update_model_performance(model_id, 0.8 + (i * 0.02))
        
        # Check performance history
        model_info = self.model_management_module.get_model_info(model_id)
        self.assertEqual(len(model_info["performance_history"]), 5)
        self.assertGreater(model_info["current_performance"], 0.8)
    
    def test_usage_tracking(self):
        """Test model usage tracking"""
        # Register model
        model_id = self.model_management_module.register_model(
            self.test_model,
            ModelType.LEARNING_STRATEGY,
            "Test Model",
            "Test model for unit testing"
        )
        
        # Record usage multiple times
        for i in range(3):
            self.model_management_module.record_model_usage(model_id)
        
        # Check usage count
        model_info = self.model_management_module.get_model_info(model_id)
        self.assertEqual(model_info["usage_count"], 3)
    
    def test_error_tracking(self):
        """Test model error tracking"""
        # Register model
        model_id = self.model_management_module.register_model(
            self.test_model,
            ModelType.LEARNING_STRATEGY,
            "Test Model",
            "Test model for unit testing"
        )
        
        # Record errors
        self.model_management_module.record_model_error(model_id, "Test error 1")
        self.model_management_module.record_model_error(model_id, "Test error 2")
        
        # Check error count
        model_info = self.model_management_module.get_model_info(model_id)
        self.assertEqual(model_info["error_count"], 2)
        self.assertEqual(len(model_info["recent_errors"]), 2)
    
    def test_model_cleanup(self):
        """Test deprecated model cleanup"""
        # Register model
        model_id = self.model_management_module.register_model(
            self.test_model,
            ModelType.LEARNING_STRATEGY,
            "Test Model",
            "Test model for unit testing"
        )
        
        # Deprecate model
        self.model_management_module._deprecate_model(model_id, "Test deprecation")
        
        # Clean up deprecated models
        cleaned_count = self.model_management_module.cleanup_deprecated_models(older_than_days=0)
        self.assertGreater(cleared_count, 0)
        
        # Verify model is removed
        model_info = self.model_management_module.get_model_info(model_id)
        self.assertIsNone(model_info)
    
    def test_module_test_function(self):
        """Test the module's built-in test function"""
        result = self.model_management_module.run_module_test()
        self.assertTrue(result)


class TestUnifiedLearningInterface(unittest.TestCase):
    """Test suite for UnifiedLearningInterface"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.interface = UnifiedLearningInterface()
        
        # Test data
        self.test_data = {
            "input_data": {"test_input": "value"},
            "output_data": {"test_output": "result"},
            "performance_score": 0.9
        }
    
    def test_interface_initialization(self):
        """Test interface initialization"""
        self.assertIsNotNone(self.interface)
        self.assertIsNotNone(self.interface.algorithms_module)
        self.assertIsNotNone(self.interface.data_processing_module)
        self.assertIsNotNone(self.interface.model_management_module)
    
    def test_data_processing_interface(self):
        """Test data processing through interface"""
        result = self.interface.process_learning_data(
            self.test_data,
            "test",
            "standard"
        )
        
        self.assertTrue(result.success)
        self.assertGreater(result.data_quality_score, 0.5)
    
    def test_learning_workflow_execution(self):
        """Test complete learning workflow execution"""
        # First register a learning strategy
        test_strategy = LearningStrategy(
            strategy_id="test_workflow_strategy",
            name="Test Workflow Strategy",
            description="Test strategy for workflow testing",
            learning_modes=[LearningMode.ADAPTIVE],
            parameters={"adaptation_rate": 0.15, "performance_threshold": 0.85}
        )
        
        strategy_id = self.interface.register_learning_strategy(test_strategy)
        self.assertIsNotNone(strategy_id)
        
        # Execute workflow
        workflow_result = self.interface.execute_learning_workflow(
            strategy_id,
            self.test_data,
            "test"
        )
        
        self.assertTrue(workflow_result["success"])
        self.assertIn("steps", workflow_result)
        self.assertIn("final_result", workflow_result)
    
    def test_comprehensive_status(self):
        """Test comprehensive status retrieval"""
        status = self.interface.get_comprehensive_status()
        
        self.assertIn("interface_status", status)
        self.assertIn("module_status", status)
        self.assertIn("algorithms_module", status)
        self.assertIn("data_processing_module", status)
        self.assertIn("model_management_module", status)
    
    def test_health_check(self):
        """Test interface health check"""
        result = self.interface.run_health_check()
        self.assertTrue(result)
    
    def test_module_test_function(self):
        """Test the interface's built-in test function"""
        result = self.interface.run_module_test()
        self.assertTrue(result)


def run_comprehensive_test_suite():
    """Run the comprehensive test suite"""
    print("🚀 RUNNING COMPREHENSIVE LEARNING MODULES TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestLearningAlgorithmsModule))
    test_suite.addTest(unittest.makeSuite(TestDataProcessingModule))
    test_suite.addTest(unittest.makeSuite(TestModelManagementModule))
    test_suite.addTest(unittest.makeSuite(TestUnifiedLearningInterface))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUITE RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED! MODULARIZATION SUCCESSFUL!")
    else:
        print("\n❌ SOME TESTS FAILED. MODULARIZATION NEEDS REVIEW.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run the comprehensive test suite
    success = run_comprehensive_test_suite()
    
    if success:
        print("\n🎉 MODULAR-007 CONTRACT: MODULARIZATION VALIDATION SUCCESSFUL!")
        print("🚀 CAPTAIN AGENT-3: LEADING WITH EXCELLENCE!")
    else:
        print("\n🔧 MODULAR-007 CONTRACT: MODULARIZATION VALIDATION NEEDS ATTENTION")
        print("📋 REVIEW REQUIRED BEFORE CONTRACT COMPLETION")
