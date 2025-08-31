#!/usr/bin/env python3
"""
Test Unified Type System - Comprehensive Validation
==================================================

Comprehensive testing of the unified type system implementation.
Validates all components and ensures proper functionality.

Agent: Agent-8 (Type Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Type Registry

Author: Agent-8 - Integration Enhancement Optimization Manager
License: MIT
"""

import unittest
import sys
import os
from pathlib import Path

# Add the src directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.types import (
    # Core enums
    WorkflowStatus,
    TaskStatus,
    TaskPriority,
    TaskType,
    WorkflowType,
    ExecutionStrategy,
    HealthLevel,
    AlertType,
    PerformanceLevel,
    BenchmarkType,
    ServiceStatus,
    HTTPMethod,
    AuthenticationLevel,
    RateLimitType,
    ValidationSeverity,
    ValidationStatus,
    ErrorSeverity,
    ComplianceLevel,
    MessagePriority,
    MessageStatus,
    CoordinationMode,
    NotificationType,
    SystemStatus,
    ResourceType,
    SecurityLevel,
    MonitoringType,
    
    # Registry and utilities
    TypeRegistry,
    type_registry,
    validate_type,
    convert_type,
    get_type_info,
    register_custom_type
)


class TestUnifiedEnums(unittest.TestCase):
    """Test unified enum functionality."""
    
    def test_workflow_status_enum(self):
        """Test WorkflowStatus enum values and transitions."""
        # Test basic enum values
        self.assertIn(WorkflowStatus.CREATED, WorkflowStatus)
        self.assertIn(WorkflowStatus.COMPLETED, WorkflowStatus)
        self.assertIn(WorkflowStatus.FAILED, WorkflowStatus)
        
        # Test transition map
        transitions = WorkflowStatus.get_transition_map()
        self.assertIsInstance(transitions, dict)
        self.assertIn(WorkflowStatus.CREATED.value, transitions)
        
        # Test specific transitions
        created_transitions = transitions[WorkflowStatus.CREATED.value]
        self.assertIn(WorkflowStatus.INITIALIZING.value, created_transitions)
        self.assertIn(WorkflowStatus.PLANNING.value, created_transitions)
    
    def test_task_status_enum(self):
        """Test TaskStatus enum functionality."""
        # Test terminal status check
        self.assertTrue(TaskStatus.is_terminal(TaskStatus.COMPLETED))
        self.assertTrue(TaskStatus.is_terminal(TaskStatus.FAILED))
        self.assertFalse(TaskStatus.is_terminal(TaskStatus.RUNNING))
        
        # Test active status check
        self.assertTrue(TaskStatus.is_active(TaskStatus.RUNNING))
        self.assertTrue(TaskStatus.is_active(TaskStatus.EXECUTING))
        self.assertFalse(TaskStatus.is_active(TaskStatus.COMPLETED))
    
    def test_task_priority_enum(self):
        """Test TaskPriority enum numeric values."""
        # Test priority comparison
        self.assertGreater(
            TaskPriority.get_numeric_value(TaskPriority.HIGH),
            TaskPriority.get_numeric_value(TaskPriority.LOW)
        )
        self.assertGreater(
            TaskPriority.get_numeric_value(TaskPriority.CRITICAL),
            TaskPriority.get_numeric_value(TaskPriority.HIGH)
        )
    
    def test_health_level_enum(self):
        """Test HealthLevel enum numeric values."""
        # Test health comparison
        self.assertGreater(
            HealthLevel.get_numeric_value(HealthLevel.EXCELLENT),
            HealthLevel.get_numeric_value(HealthLevel.GOOD)
        )
        self.assertGreater(
            HealthLevel.get_numeric_value(HealthLevel.GOOD),
            HealthLevel.get_numeric_value(HealthLevel.CRITICAL)
        )
    
    def test_enum_utility_functions(self):
        """Test enum utility functions."""
        from src.core.types.unified_enums import (
            get_all_enums,
            get_enum_by_name,
            get_enum_values,
            validate_enum_value
        )
        
        # Test get_all_enums
        all_enums = get_all_enums()
        self.assertIsInstance(all_enums, dict)
        self.assertIn('WorkflowStatus', all_enums)
        self.assertIn('TaskStatus', all_enums)
        
        # Test get_enum_by_name
        workflow_enum = get_enum_by_name('WorkflowStatus')
        self.assertEqual(workflow_enum, WorkflowStatus)
        
        # Test get_enum_values
        workflow_values = get_enum_values('WorkflowStatus')
        self.assertIsInstance(workflow_values, list)
        self.assertIn('created', workflow_values)
        
        # Test validate_enum_value
        self.assertTrue(validate_enum_value('WorkflowStatus', 'created'))
        self.assertFalse(validate_enum_value('WorkflowStatus', 'invalid_status'))


class TestTypeRegistry(unittest.TestCase):
    """Test TypeRegistry functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.registry = TypeRegistry()
    
    def test_registry_initialization(self):
        """Test registry initialization."""
        self.assertIsInstance(self.registry.registered_types, dict)
        self.assertIsInstance(self.registry.type_metadata, dict)
        self.assertIsInstance(self.registry.import_paths, dict)
        
        # Check that core types are registered
        self.assertIn('WorkflowStatus', self.registry.registered_types)
        self.assertIn('TaskStatus', self.registry.registered_types)
    
    def test_type_registration(self):
        """Test type registration functionality."""
        # Test custom type registration
        class TestType:
            pass
        
        self.registry.register_type('TestType', TestType, 'test_module')
        
        # Verify registration
        self.assertIn('TestType', self.registry.registered_types)
        self.assertEqual(self.registry.get_type('TestType'), TestType)
        
        # Verify metadata
        metadata = self.registry.get_type_metadata('TestType')
        self.assertIsInstance(metadata, dict)
        self.assertEqual(metadata['source'], 'test_module')
    
    def test_type_discovery(self):
        """Test type discovery functionality."""
        # Test enum listing
        enums = self.registry.list_enums()
        self.assertIsInstance(enums, list)
        self.assertIn('WorkflowStatus', enums)
        self.assertIn('TaskStatus', enums)
        
        # Test type listing
        all_types = self.registry.list_types()
        self.assertIsInstance(all_types, list)
        self.assertGreater(len(all_types), 0)
    
    def test_type_validation(self):
        """Test type validation functionality."""
        # Test valid enum value
        self.assertTrue(self.registry.validate_type('WorkflowStatus', 'created'))
        
        # Test invalid enum value
        self.assertFalse(self.registry.validate_type('WorkflowStatus', 'invalid_status'))
        
        # Test non-existent type
        self.assertFalse(self.registry.validate_type('NonExistentType', 'value'))
    
    def test_type_conversion(self):
        """Test type conversion functionality."""
        # Test enum conversion
        converted = self.registry.convert_type('WorkflowStatus', 'created')
        self.assertEqual(converted, WorkflowStatus.CREATED)
        
        # Test invalid conversion
        converted = self.registry.convert_type('WorkflowStatus', 'invalid_status')
        self.assertIsNone(converted)
    
    def test_consolidation_tracking(self):
        """Test consolidation progress tracking."""
        # Test initial status
        progress = self.registry.get_consolidation_progress()
        self.assertIsInstance(progress, dict)
        self.assertIn('total_targets', progress)
        self.assertIn('completed_targets', progress)
        self.assertIn('progress_percentage', progress)
        
        # Test status update
        self.registry.update_consolidation_status('test_target', 'in_progress')
        status = self.registry.get_consolidation_status('test_target')
        self.assertEqual(status, 'in_progress')


class TestTypeUtilities(unittest.TestCase):
    """Test type utility functions."""
    
    def test_validate_type_function(self):
        """Test validate_type utility function."""
        # Test with enum types
        self.assertTrue(validate_type('created', WorkflowStatus))
        self.assertFalse(validate_type('invalid_status', WorkflowStatus))
        
        # Test with string types and registry
        from src.core.types import type_registry
        self.assertTrue(validate_type('created', 'WorkflowStatus', type_registry))
        self.assertFalse(validate_type('invalid_status', 'WorkflowStatus', type_registry))
    
    def test_convert_type_function(self):
        """Test convert_type utility function."""
        # Test with enum types
        converted = convert_type('created', WorkflowStatus)
        self.assertEqual(converted, WorkflowStatus.CREATED)
        
        # Test with string types and registry
        from src.core.types import type_registry
        converted = convert_type('created', 'WorkflowStatus', type_registry)
        self.assertEqual(converted, WorkflowStatus.CREATED)
    
    def test_get_type_info_function(self):
        """Test get_type_info utility function."""
        # Test with enum
        info = get_type_info(WorkflowStatus)
        self.assertIsInstance(info, dict)
        self.assertEqual(info['name'], 'WorkflowStatus')
        self.assertTrue(info['is_enum'])
        self.assertIn('enum_values', info)
        
        # Test with regular class
        class TestClass:
            def test_method(self):
                pass
        
        info = get_type_info(TestClass)
        self.assertEqual(info['name'], 'TestClass')
        self.assertFalse(info['is_enum'])
        self.assertIn('test_method', info['methods'])
    
    def test_type_compatibility_analysis(self):
        """Test type compatibility analysis."""
        from src.core.types.type_utils import analyze_type_compatibility
        
        # Test identical types
        compatibility = analyze_type_compatibility(WorkflowStatus, WorkflowStatus)
        self.assertTrue(compatibility['compatible'])
        self.assertEqual(compatibility['compatibility_score'], 1.0)
        
        # Test different enum types
        compatibility = analyze_type_compatibility(WorkflowStatus, TaskStatus)
        self.assertFalse(compatibility['compatible'])
        self.assertLess(compatibility['compatibility_score'], 0.5)
    
    def test_type_documentation_generation(self):
        """Test type documentation generation."""
        from src.core.types.type_utils import generate_type_documentation
        
        # Generate documentation for WorkflowStatus
        doc = generate_type_documentation(WorkflowStatus)
        self.assertIsInstance(doc, str)
        self.assertIn('# WorkflowStatus', doc)
        self.assertIn('## Enum Values', doc)
        self.assertIn('created', doc)
    
    def test_type_registry_validation(self):
        """Test type registry validation."""
        from src.core.types.type_utils import validate_type_registry
        
        # Validate the main type registry
        from src.core.types import type_registry
        validation = validate_type_registry(type_registry)
        
        self.assertIsInstance(validation, dict)
        self.assertIn('valid', validation)
        self.assertIn('total_types', validation)
        self.assertIn('enum_types', validation)
        
        # Should be valid
        self.assertTrue(validation['valid'])


class TestIntegration(unittest.TestCase):
    """Test integration between components."""
    
    def test_unified_type_system_imports(self):
        """Test that all unified types can be imported correctly."""
        # Test that all core enums are available
        self.assertIsNotNone(WorkflowStatus)
        self.assertIsNotNone(TaskStatus)
        self.assertIsNotNone(HealthLevel)
        self.assertIsNotNone(ServiceStatus)
        
        # Test that registry is available
        self.assertIsNotNone(type_registry)
        self.assertIsInstance(type_registry, TypeRegistry)
    
    def test_type_registry_integration(self):
        """Test integration between enums and registry."""
        # Verify that all enums are registered
        registered_types = type_registry.list_types()
        self.assertIn('WorkflowStatus', registered_types)
        self.assertIn('TaskStatus', registered_types)
        self.assertIn('HealthLevel', registered_types)
        
        # Verify enum functionality through registry
        self.assertTrue(type_registry.validate_type('WorkflowStatus', 'created'))
        converted = type_registry.convert_type('WorkflowStatus', 'created')
        self.assertEqual(converted, WorkflowStatus.CREATED)
    
    def test_utility_function_integration(self):
        """Test integration between utilities and registry."""
        # Test utility functions with registry
        self.assertTrue(validate_type('created', 'WorkflowStatus', type_registry))
        converted = convert_type('created', 'WorkflowStatus', type_registry)
        self.assertEqual(converted, WorkflowStatus.CREATED)
        
        # Test type info generation
        info = get_type_info(WorkflowStatus)
        self.assertIsInstance(info, dict)
        self.assertTrue(info['is_enum'])


class TestPerformance(unittest.TestCase):
    """Test performance characteristics."""
    
    def test_enum_value_access_performance(self):
        """Test performance of enum value access."""
        import time
        
        # Test direct enum access
        start_time = time.time()
        for _ in range(1000):
            _ = WorkflowStatus.CREATED.value
        direct_time = time.time() - start_time
        
        # Test registry-based access
        start_time = time.time()
        for _ in range(1000):
            _ = type_registry.get_type('WorkflowStatus')
        registry_time = time.time() - start_time
        
        # Registry access should be reasonable (within 10x of direct access)
        self.assertLess(registry_time, direct_time * 10)
    
    def test_type_validation_performance(self):
        """Test performance of type validation."""
        import time
        
        # Test validation performance
        start_time = time.time()
        for _ in range(1000):
            type_registry.validate_type('WorkflowStatus', 'created')
        validation_time = time.time() - start_time
        
        # Validation should be fast (< 1 second for 1000 operations)
        self.assertLess(validation_time, 1.0)


def run_comprehensive_tests():
    """Run comprehensive test suite."""
    print("🚀 Starting Comprehensive Unified Type System Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestUnifiedEnums,
        TestTypeRegistry,
        TestTypeUtilities,
        TestIntegration,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\n🚨 ERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED - Unified Type System is fully operational!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED - Review and fix issues")
        return False


if __name__ == "__main__":
    # Run comprehensive tests
    success = run_comprehensive_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
