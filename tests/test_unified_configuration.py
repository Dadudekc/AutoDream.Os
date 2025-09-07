#!/usr/bin/env python3
"""
Test Suite for Unified Configuration System - Agent Cellphone V2
==============================================================

Comprehensive testing of the unified configuration constants system to ensure
all functionality works correctly and backward compatibility is maintained.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import unittest
import os
import logging
from unittest.mock import patch

from src.core.configuration import (
    # Core classes and enums
    ConfigCategory,
    ConfigPriority,
    ConfigConstant,
    UnifiedConstantsRegistry,
    
    # Global instance
    UNIFIED_CONSTANTS,
    
    # Convenience functions
    get_constant,
    get_constants_by_category,
    export_all_constants,
    
    # All constant values for backward compatibility
    LOG_LEVEL,
    TASK_ID_TIMESTAMP_FORMAT,
    APP_NAME,
    APP_VERSION,
    APP_ENVIRONMENT,
    DEFAULT_MAX_WORKERS,
    DEFAULT_THREAD_POOL_SIZE,
    DEFAULT_CACHE_SIZE,
    DEFAULT_OPERATION_TIMEOUT,
    DEFAULT_CHECK_INTERVAL,
    DEFAULT_COVERAGE_THRESHOLD,
    DEFAULT_HISTORY_WINDOW,
    DEFAULT_MESSAGING_MODE,
    DEFAULT_AGENT_COUNT,
    DEFAULT_CAPTAIN_ID,
    DEFAULT_AI_MODEL_TIMEOUT,
    DEFAULT_AI_BATCH_SIZE,
    DEFAULT_FSM_TIMEOUT,
    DEFAULT_FSM_MAX_STATES,
    DEFAULT_REFACTORING_MAX_WORKERS,
    DEFAULT_REFACTORING_TIMEOUT,
    DEFAULT_TEST_TIMEOUT,
    DEFAULT_COVERAGE_MIN_PERCENT,
    DEFAULT_NETWORK_HOST,
    DEFAULT_NETWORK_PORT,
    DEFAULT_MAX_CONNECTIONS,
    DEFAULT_SECURITY_TIMEOUT,
    DEFAULT_MAX_LOGIN_ATTEMPTS,
    DEFAULT_DB_HOST,
    DEFAULT_DB_PORT,
    DEFAULT_DB_POOL_SIZE,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_FILE_SIZE
)


# ============================================================================
# TEST UNIFIED CONSTANTS SYSTEM
# ============================================================================

class TestUnifiedConstantsSystem(unittest.TestCase):
    """Test the unified constants system functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = UnifiedConstantsRegistry()
    
    def test_config_category_enum(self):
        """Test ConfigCategory enum values."""
        self.assertEqual(ConfigCategory.GLOBAL.value, "global")
        self.assertEqual(ConfigCategory.PERFORMANCE.value, "performance")
        self.assertEqual(ConfigCategory.QUALITY.value, "quality")
        self.assertEqual(ConfigCategory.MESSAGING.value, "messaging")
        self.assertEqual(ConfigCategory.AI_ML.value, "ai_ml")
        self.assertEqual(ConfigCategory.FSM.value, "fsm")
        self.assertEqual(ConfigCategory.REFACTORING.value, "refactoring")
        self.assertEqual(ConfigCategory.TESTING.value, "testing")
        self.assertEqual(ConfigCategory.NETWORK.value, "network")
        self.assertEqual(ConfigCategory.SECURITY.value, "security")
        self.assertEqual(ConfigCategory.DATABASE.value, "database")
        self.assertEqual(ConfigCategory.CUSTOM.value, "custom")
    
    def test_config_priority_enum(self):
        """Test ConfigPriority enum values."""
        self.assertEqual(ConfigPriority.CRITICAL.value, 1)
        self.assertEqual(ConfigPriority.HIGH.value, 2)
        self.assertEqual(ConfigPriority.MEDIUM.value, 3)
        self.assertEqual(ConfigPriority.LOW.value, 4)
        self.assertEqual(ConfigPriority.OPTIONAL.value, 5)
    
    def test_config_constant_dataclass(self):
        """Test ConfigConstant dataclass creation."""
        constant = ConfigConstant(
            name="TEST_CONSTANT",
            value=42,
            category=ConfigCategory.TESTING,
            description="Test constant for testing",
            priority=ConfigPriority.HIGH
        )
        
        self.assertEqual(constant.name, "TEST_CONSTANT")
        self.assertEqual(constant.value, 42)
        self.assertEqual(constant.category, ConfigCategory.TESTING)
        self.assertEqual(constant.description, "Test constant for testing")
        self.assertEqual(constant.priority, ConfigPriority.HIGH)
        self.assertFalse(constant.is_environment_override)
        self.assertIsNone(constant.environment_key)
        self.assertIsNone(constant.validation_rules)
    
    def test_registry_initialization(self):
        """Test that the registry initializes with all constants."""
        self.assertGreater(len(self.registry.constants), 0)
        
        # Check that key constants are present
        self.assertIn("LOG_LEVEL", self.registry.constants)
        self.assertIn("DEFAULT_MAX_WORKERS", self.registry.constants)
        self.assertIn("DEFAULT_CHECK_INTERVAL", self.registry.constants)
        self.assertIn("DEFAULT_MESSAGING_MODE", self.registry.constants)
        self.assertIn("DEFAULT_AI_MODEL_TIMEOUT", self.registry.constants)
        self.assertIn("DEFAULT_FSM_TIMEOUT", self.registry.constants)
        self.assertIn("DEFAULT_REFACTORING_MAX_WORKERS", self.registry.constants)
        self.assertIn("DEFAULT_TEST_TIMEOUT", self.registry.constants)
        self.assertIn("DEFAULT_NETWORK_HOST", self.registry.constants)
        self.assertIn("DEFAULT_SECURITY_TIMEOUT", self.registry.constants)
        self.assertIn("DEFAULT_DB_HOST", self.registry.constants)
        self.assertIn("DEFAULT_LOG_FORMAT", self.registry.constants)
    
    def test_get_constant(self):
        """Test getting constants from the registry."""
        # Test existing constants
        self.assertEqual(self.registry.get_constant("LOG_LEVEL"), LOG_LEVEL)
        self.assertEqual(self.registry.get_constant("DEFAULT_MAX_WORKERS"), DEFAULT_MAX_WORKERS)
        self.assertEqual(self.registry.get_constant("DEFAULT_CHECK_INTERVAL"), DEFAULT_CHECK_INTERVAL)
        
        # Test non-existent constants with default
        self.assertEqual(self.registry.get_constant("NON_EXISTENT", "default"), "default")
        self.assertIsNone(self.registry.get_constant("NON_EXISTENT"))
    
    def test_get_constants_by_category(self):
        """Test getting constants by category."""
        # Test performance constants
        performance_constants = self.registry.get_constants_by_category(ConfigCategory.PERFORMANCE)
        self.assertIn("DEFAULT_MAX_WORKERS", performance_constants)
        self.assertIn("DEFAULT_THREAD_POOL_SIZE", performance_constants)
        self.assertIn("DEFAULT_CACHE_SIZE", performance_constants)
        self.assertIn("DEFAULT_OPERATION_TIMEOUT", performance_constants)
        
        # Test quality constants
        quality_constants = self.registry.get_constants_by_category(ConfigCategory.QUALITY)
        self.assertIn("DEFAULT_CHECK_INTERVAL", quality_constants)
        self.assertIn("DEFAULT_COVERAGE_THRESHOLD", quality_constants)
        self.assertIn("DEFAULT_HISTORY_WINDOW", quality_constants)
        
        # Test messaging constants
        messaging_constants = self.registry.get_constants_by_category(ConfigCategory.MESSAGING)
        self.assertIn("DEFAULT_MESSAGING_MODE", messaging_constants)
        self.assertIn("DEFAULT_AGENT_COUNT", messaging_constants)
        self.assertIn("DEFAULT_CAPTAIN_ID", messaging_constants)
        
        # Test AI/ML constants
        ai_ml_constants = self.registry.get_constants_by_category(ConfigCategory.AI_ML)
        self.assertIn("DEFAULT_AI_MODEL_TIMEOUT", ai_ml_constants)
        self.assertIn("DEFAULT_AI_BATCH_SIZE", ai_ml_constants)
        
        # Test FSM constants
        fsm_constants = self.registry.get_constants_by_category(ConfigCategory.FSM)
        self.assertIn("DEFAULT_FSM_TIMEOUT", fsm_constants)
        self.assertIn("DEFAULT_FSM_MAX_STATES", fsm_constants)
        
        # Test refactoring constants
        refactoring_constants = self.registry.get_constants_by_category(ConfigCategory.REFACTORING)
        self.assertIn("DEFAULT_REFACTORING_MAX_WORKERS", refactoring_constants)
        self.assertIn("DEFAULT_REFACTORING_TIMEOUT", refactoring_constants)
        
        # Test testing constants
        testing_constants = self.registry.get_constants_by_category(ConfigCategory.TESTING)
        self.assertIn("DEFAULT_TEST_TIMEOUT", testing_constants)
        self.assertIn("DEFAULT_COVERAGE_MIN_PERCENT", testing_constants)
        
        # Test network constants
        network_constants = self.registry.get_constants_by_category(ConfigCategory.NETWORK)
        self.assertIn("DEFAULT_NETWORK_HOST", network_constants)
        self.assertIn("DEFAULT_NETWORK_PORT", network_constants)
        self.assertIn("DEFAULT_MAX_CONNECTIONS", network_constants)
        
        # Test security constants
        security_constants = self.registry.get_constants_by_category(ConfigCategory.SECURITY)
        self.assertIn("DEFAULT_SECURITY_TIMEOUT", security_constants)
        self.assertIn("DEFAULT_MAX_LOGIN_ATTEMPTS", security_constants)
        
        # Test database constants
        database_constants = self.registry.get_constants_by_category(ConfigCategory.DATABASE)
        self.assertIn("DEFAULT_DB_HOST", database_constants)
        self.assertIn("DEFAULT_DB_PORT", database_constants)
        self.assertIn("DEFAULT_DB_POOL_SIZE", database_constants)
        
        # Test logging constants
        logging_constants = self.registry.get_constants_by_category(ConfigCategory.LOGGING)
        self.assertIn("DEFAULT_LOG_FORMAT", logging_constants)
        self.assertIn("DEFAULT_LOG_FILE_SIZE", logging_constants)
    
    def test_get_constants_by_priority(self):
        """Test getting constants by priority."""
        # Test critical constants
        critical_constants = self.registry.get_constants_by_priority(ConfigPriority.CRITICAL)
        self.assertIn("LOG_LEVEL", critical_constants)
        self.assertIn("APP_NAME", critical_constants)
        self.assertIn("APP_VERSION", critical_constants)
        self.assertIn("APP_ENVIRONMENT", critical_constants)
        
        # Test high priority constants
        high_constants = self.registry.get_constants_by_priority(ConfigPriority.HIGH)
        self.assertIn("TASK_ID_TIMESTAMP_FORMAT", high_constants)
        self.assertIn("DEFAULT_MAX_WORKERS", high_constants)
        self.assertIn("DEFAULT_THREAD_POOL_SIZE", high_constants)
        self.assertIn("DEFAULT_OPERATION_TIMEOUT", high_constants)
        self.assertIn("DEFAULT_AGENT_COUNT", high_constants)
        self.assertIn("DEFAULT_CAPTAIN_ID", high_constants)
        self.assertIn("DEFAULT_NETWORK_HOST", high_constants)
        self.assertIn("DEFAULT_NETWORK_PORT", high_constants)
        self.assertIn("DEFAULT_SECURITY_TIMEOUT", high_constants)
        self.assertIn("DEFAULT_MAX_LOGIN_ATTEMPTS", high_constants)
        self.assertIn("DEFAULT_DB_HOST", high_constants)
        self.assertIn("DEFAULT_DB_PORT", high_constants)
        
        # Test medium priority constants
        medium_constants = self.registry.get_constants_by_priority(ConfigPriority.MEDIUM)
        self.assertIn("DEFAULT_CACHE_SIZE", medium_constants)
        self.assertIn("DEFAULT_CHECK_INTERVAL", medium_constants)
        self.assertIn("DEFAULT_COVERAGE_THRESHOLD", medium_constants)
        self.assertIn("DEFAULT_MESSAGING_MODE", medium_constants)
        self.assertIn("DEFAULT_AI_MODEL_TIMEOUT", medium_constants)
        self.assertIn("DEFAULT_AI_BATCH_SIZE", medium_constants)
        self.assertIn("DEFAULT_FSM_TIMEOUT", medium_constants)
        self.assertIn("DEFAULT_REFACTORING_MAX_WORKERS", medium_constants)
        self.assertIn("DEFAULT_REFACTORING_TIMEOUT", medium_constants)
        self.assertIn("DEFAULT_TEST_TIMEOUT", medium_constants)
        self.assertIn("DEFAULT_COVERAGE_MIN_PERCENT", medium_constants)
        self.assertIn("DEFAULT_MAX_CONNECTIONS", medium_constants)
        self.assertIn("DEFAULT_DB_POOL_SIZE", medium_constants)
        self.assertIn("DEFAULT_LOG_FORMAT", medium_constants)
        
        # Test low priority constants
        low_constants = self.registry.get_constants_by_priority(ConfigPriority.LOW)
        self.assertIn("DEFAULT_HISTORY_WINDOW", low_constants)
        self.assertIn("DEFAULT_FSM_MAX_STATES", low_constants)
        self.assertIn("DEFAULT_LOG_FILE_SIZE", low_constants)
    
    def test_list_all_constants(self):
        """Test listing all constants with metadata."""
        all_constants = self.registry.list_all_constants()
        
        # Check that we have metadata for key constants
        self.assertIn("LOG_LEVEL", all_constants)
        self.assertIn("DEFAULT_MAX_WORKERS", all_constants)
        self.assertIn("DEFAULT_CHECK_INTERVAL", all_constants)
        
        # Check metadata structure
        log_level_meta = all_constants["LOG_LEVEL"]
        self.assertIn("value", log_level_meta)
        self.assertIn("category", log_level_meta)
        self.assertIn("description", log_level_meta)
        self.assertIn("priority", log_level_meta)
        
        # Check specific metadata values
        self.assertEqual(log_level_meta["category"], "global")
        self.assertEqual(log_level_meta["priority"], 1)  # CRITICAL
        
        max_workers_meta = all_constants["DEFAULT_MAX_WORKERS"]
        self.assertEqual(max_workers_meta["category"], "performance")
        self.assertEqual(max_workers_meta["priority"], 2)  # HIGH
    
    def test_export_constants(self):
        """Test exporting constants."""
        # Test export all constants
        all_constants = self.registry.export_constants()
        self.assertIn("LOG_LEVEL", all_constants)
        self.assertIn("DEFAULT_MAX_WORKERS", all_constants)
        self.assertIn("DEFAULT_CHECK_INTERVAL", all_constants)
        
        # Test export by category
        performance_constants = self.registry.export_constants(ConfigCategory.PERFORMANCE)
        self.assertIn("DEFAULT_MAX_WORKERS", performance_constants)
        self.assertIn("DEFAULT_THREAD_POOL_SIZE", performance_constants)
        self.assertIn("DEFAULT_CACHE_SIZE", performance_constants)
        self.assertIn("DEFAULT_OPERATION_TIMEOUT", performance_constants)
        
        # Verify no other categories are included
        self.assertNotIn("LOG_LEVEL", performance_constants)  # Global category
        self.assertNotIn("DEFAULT_CHECK_INTERVAL", performance_constants)  # Quality category


# ============================================================================
# TEST GLOBAL INSTANCE
# ============================================================================

class TestGlobalInstance(unittest.TestCase):
    """Test the global unified constants instance."""
    
    def test_global_instance_exists(self):
        """Test that the global instance exists and is properly initialized."""
        self.assertIsInstance(UNIFIED_CONSTANTS, UnifiedConstantsRegistry)
        self.assertGreater(len(UNIFIED_CONSTANTS.constants), 0)
    
    def test_global_instance_has_all_constants(self):
        """Test that the global instance has all expected constants."""
        # Check key constants are present
        self.assertIn("LOG_LEVEL", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_MAX_WORKERS", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_CHECK_INTERVAL", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_MESSAGING_MODE", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_AI_MODEL_TIMEOUT", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_FSM_TIMEOUT", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_REFACTORING_MAX_WORKERS", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_TEST_TIMEOUT", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_NETWORK_HOST", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_SECURITY_TIMEOUT", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_DB_HOST", UNIFIED_CONSTANTS.constants)
        self.assertIn("DEFAULT_LOG_FORMAT", UNIFIED_CONSTANTS.constants)


# ============================================================================
# TEST CONVENIENCE FUNCTIONS
# ============================================================================

class TestConvenienceFunctions(unittest.TestCase):
    """Test the convenience functions for accessing constants."""
    
    def test_get_constant_function(self):
        """Test the get_constant convenience function."""
        # Test existing constants
        self.assertEqual(get_constant("LOG_LEVEL"), LOG_LEVEL)
        self.assertEqual(get_constant("DEFAULT_MAX_WORKERS"), DEFAULT_MAX_WORKERS)
        self.assertEqual(get_constant("DEFAULT_CHECK_INTERVAL"), DEFAULT_CHECK_INTERVAL)
        
        # Test non-existent constants with default
        self.assertEqual(get_constant("NON_EXISTENT", "default"), "default")
        self.assertIsNone(get_constant("NON_EXISTENT"))
    
    def test_get_constants_by_category_function(self):
        """Test the get_constants_by_category convenience function."""
        # Test performance constants
        performance_constants = get_constants_by_category(ConfigCategory.PERFORMANCE)
        self.assertIn("DEFAULT_MAX_WORKERS", performance_constants)
        self.assertIn("DEFAULT_THREAD_POOL_SIZE", performance_constants)
        self.assertIn("DEFAULT_CACHE_SIZE", performance_constants)
        self.assertIn("DEFAULT_OPERATION_TIMEOUT", performance_constants)
        
        # Test quality constants
        quality_constants = get_constants_by_category(ConfigCategory.QUALITY)
        self.assertIn("DEFAULT_CHECK_INTERVAL", quality_constants)
        self.assertIn("DEFAULT_COVERAGE_THRESHOLD", quality_constants)
        self.assertIn("DEFAULT_HISTORY_WINDOW", quality_constants)
        
        # Test messaging constants
        messaging_constants = get_constants_by_category(ConfigCategory.MESSAGING)
        self.assertIn("DEFAULT_MESSAGING_MODE", messaging_constants)
        self.assertIn("DEFAULT_AGENT_COUNT", messaging_constants)
        self.assertIn("DEFAULT_CAPTAIN_ID", messaging_constants)
    
    def test_export_all_constants_function(self):
        """Test the export_all_constants convenience function."""
        all_constants = export_all_constants()
        
        # Check that key constants are exported
        self.assertIn("LOG_LEVEL", all_constants)
        self.assertIn("DEFAULT_MAX_WORKERS", all_constants)
        self.assertIn("DEFAULT_CHECK_INTERVAL", all_constants)
        self.assertIn("DEFAULT_MESSAGING_MODE", all_constants)
        self.assertIn("DEFAULT_AI_MODEL_TIMEOUT", all_constants)
        self.assertIn("DEFAULT_FSM_TIMEOUT", all_constants)
        self.assertIn("DEFAULT_REFACTORING_MAX_WORKERS", all_constants)
        self.assertIn("DEFAULT_TEST_TIMEOUT", all_constants)
        self.assertIn("DEFAULT_NETWORK_HOST", all_constants)
        self.assertIn("DEFAULT_SECURITY_TIMEOUT", all_constants)
        self.assertIn("DEFAULT_DB_HOST", all_constants)
        self.assertIn("DEFAULT_LOG_FORMAT", all_constants)


# ============================================================================
# TEST BACKWARD COMPATIBILITY
# ============================================================================

class TestBackwardCompatibility(unittest.TestCase):
    """Test that all constants are accessible for backward compatibility."""
    
    def test_global_constants_accessible(self):
        """Test that global constants are directly accessible."""
        self.assertEqual(LOG_LEVEL, getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO))
        self.assertEqual(TASK_ID_TIMESTAMP_FORMAT, "%Y%m%d_%H%M%S_%f")
        self.assertEqual(APP_NAME, "Agent Cellphone V2")
        self.assertEqual(APP_VERSION, "2.0.0")
        self.assertEqual(APP_ENVIRONMENT, os.getenv("APP_ENVIRONMENT", "development"))
    
    def test_performance_constants_accessible(self):
        """Test that performance constants are directly accessible."""
        self.assertEqual(DEFAULT_MAX_WORKERS, int(os.getenv("DEFAULT_MAX_WORKERS", "4")))
        self.assertEqual(DEFAULT_THREAD_POOL_SIZE, int(os.getenv("DEFAULT_THREAD_POOL_SIZE", "10")))
        self.assertEqual(DEFAULT_CACHE_SIZE, int(os.getenv("DEFAULT_CACHE_SIZE", "1000")))
        self.assertEqual(DEFAULT_OPERATION_TIMEOUT, float(os.getenv("DEFAULT_OPERATION_TIMEOUT", "30.0")))
    
    def test_quality_constants_accessible(self):
        """Test that quality constants are directly accessible."""
        self.assertEqual(DEFAULT_CHECK_INTERVAL, float(os.getenv("DEFAULT_CHECK_INTERVAL", "30.0")))
        self.assertEqual(DEFAULT_COVERAGE_THRESHOLD, float(os.getenv("DEFAULT_COVERAGE_THRESHOLD", "80.0")))
        self.assertEqual(DEFAULT_HISTORY_WINDOW, int(os.getenv("DEFAULT_HISTORY_WINDOW", "100")))
    
    def test_messaging_constants_accessible(self):
        """Test that messaging constants are directly accessible."""
        self.assertEqual(DEFAULT_MESSAGING_MODE, os.getenv("DEFAULT_MESSAGING_MODE", "pyautogui"))
        self.assertEqual(DEFAULT_AGENT_COUNT, int(os.getenv("DEFAULT_AGENT_COUNT", "8")))
        self.assertEqual(DEFAULT_CAPTAIN_ID, os.getenv("DEFAULT_CAPTAIN_ID", "Agent-4"))
    
    def test_ai_ml_constants_accessible(self):
        """Test that AI/ML constants are directly accessible."""
        self.assertEqual(DEFAULT_AI_MODEL_TIMEOUT, float(os.getenv("DEFAULT_AI_MODEL_TIMEOUT", "60.0")))
        self.assertEqual(DEFAULT_AI_BATCH_SIZE, int(os.getenv("DEFAULT_AI_BATCH_SIZE", "32")))
    
    def test_fsm_constants_accessible(self):
        """Test that FSM constants are directly accessible."""
        self.assertEqual(DEFAULT_FSM_TIMEOUT, float(os.getenv("DEFAULT_FSM_TIMEOUT", "30.0")))
        self.assertEqual(DEFAULT_FSM_MAX_STATES, int(os.getenv("DEFAULT_FSM_MAX_STATES", "100")))
    
    def test_refactoring_constants_accessible(self):
        """Test that refactoring constants are directly accessible."""
        self.assertEqual(DEFAULT_REFACTORING_MAX_WORKERS, int(os.getenv("DEFAULT_REFACTORING_MAX_WORKERS", "4")))
        self.assertEqual(DEFAULT_REFACTORING_TIMEOUT, float(os.getenv("DEFAULT_REFACTORING_TIMEOUT", "300.0")))
    
    def test_testing_constants_accessible(self):
        """Test that testing constants are directly accessible."""
        self.assertEqual(DEFAULT_TEST_TIMEOUT, float(os.getenv("DEFAULT_TEST_TIMEOUT", "30.0")))
        self.assertEqual(DEFAULT_COVERAGE_MIN_PERCENT, float(os.getenv("DEFAULT_COVERAGE_MIN_PERCENT", "80.0")))
    
    def test_network_constants_accessible(self):
        """Test that network constants are directly accessible."""
        self.assertEqual(DEFAULT_NETWORK_HOST, os.getenv("DEFAULT_NETWORK_HOST", "0.0.0.0"))
        self.assertEqual(DEFAULT_NETWORK_PORT, int(os.getenv("DEFAULT_NETWORK_PORT", "8000")))
        self.assertEqual(DEFAULT_MAX_CONNECTIONS, int(os.getenv("DEFAULT_MAX_CONNECTIONS", "100")))
    
    def test_security_constants_accessible(self):
        """Test that security constants are directly accessible."""
        self.assertEqual(DEFAULT_SECURITY_TIMEOUT, float(os.getenv("DEFAULT_SECURITY_TIMEOUT", "30.0")))
        self.assertEqual(DEFAULT_MAX_LOGIN_ATTEMPTS, int(os.getenv("DEFAULT_MAX_LOGIN_ATTEMPTS", "5")))
    
    def test_database_constants_accessible(self):
        """Test that database constants are directly accessible."""
        self.assertEqual(DEFAULT_DB_HOST, os.getenv("DEFAULT_DB_HOST", "localhost"))
        self.assertEqual(DEFAULT_DB_PORT, int(os.getenv("DEFAULT_DB_PORT", "5432")))
        self.assertEqual(DEFAULT_DB_POOL_SIZE, int(os.getenv("DEFAULT_DB_POOL_SIZE", "10")))
    
    def test_logging_constants_accessible(self):
        """Test that logging constants are directly accessible."""
        self.assertEqual(DEFAULT_LOG_FORMAT, os.getenv("DEFAULT_LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.assertEqual(DEFAULT_LOG_FILE_SIZE, int(os.getenv("DEFAULT_LOG_FILE_SIZE", "10485760")))


# ============================================================================
# TEST ENVIRONMENT OVERRIDES
# ============================================================================

class TestEnvironmentOverrides(unittest.TestCase):
    """Test environment variable overrides for configuration constants."""
    
    def test_log_level_environment_override(self):
        """Test that LOG_LEVEL can be overridden by environment variable."""
        with patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}):
            # Re-import to get updated value
            import importlib
            import src.core.configuration
            importlib.reload(src.core.configuration)
            
            # Check that the value is updated
            self.assertEqual(src.core.configuration.LOG_LEVEL, logging.DEBUG)
    
    def test_max_workers_environment_override(self):
        """Test that DEFAULT_MAX_WORKERS can be overridden by environment variable."""
        with patch.dict(os.environ, {"DEFAULT_MAX_WORKERS": "8"}):
            # Re-import to get updated value
            import importlib
            import src.core.configuration
            importlib.reload(src.core.configuration)
            
            # Check that the value is updated
            self.assertEqual(src.core.configuration.DEFAULT_MAX_WORKERS, 8)
    
    def test_cache_size_environment_override(self):
        """Test that DEFAULT_CACHE_SIZE can be overridden by environment variable."""
        with patch.dict(os.environ, {"DEFAULT_CACHE_SIZE": "2000"}):
            # Re-import to get updated value
            import importlib
            import src.core.configuration
            importlib.reload(src.core.configuration)
            
            # Check that the value is updated
            self.assertEqual(src.core.configuration.DEFAULT_CACHE_SIZE, 2000)


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestUnifiedConstantsSystem))
    test_suite.addTest(unittest.makeSuite(TestGlobalInstance))
    test_suite.addTest(unittest.makeSuite(TestConvenienceFunctions))
    test_suite.addTest(unittest.makeSuite(TestBackwardCompatibility))
    test_suite.addTest(unittest.makeSuite(TestEnvironmentOverrides))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"UNIFIED CONFIGURATION SYSTEM TEST RESULTS")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    print(f"\n{'='*60}")
    
    # Exit with appropriate code
    exit(len(result.failures) + len(result.errors))
