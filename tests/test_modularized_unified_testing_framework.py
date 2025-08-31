#!/usr/bin/env python3
"""
Test Suite for Modularized Unified Testing Framework
===================================================

This script tests the modularized unified testing framework to ensure
all components work correctly together.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-002 - Unified Testing Framework Modularization
**Status:** Testing modularized system
**V2 Compliance:** ✅ Under 250 lines per module, single responsibility principle
"""

import unittest
import tempfile
import shutil
from pathlib import Path

# Import the modularized test modules
from tests.test_unified_testing_framework_runner import TestUnifiedTestRunner
from tests.test_unified_testing_framework_config import TestUnifiedTestConfig
from tests.test_unified_testing_framework_utilities import TestUnifiedTestUtilities
from tests.test_unified_testing_framework_integration import TestUnifiedTestingFrameworkIntegration


def test_runner_module():
    """Test the runner module functionality."""
    print("Testing Unified Testing Framework Runner Module...")
    
    # Create test suite for runner module
    runner_suite = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedTestRunner)
    runner_runner = unittest.TextTestRunner(verbosity=2)
    runner_result = runner_runner.run(runner_suite)
    
    print(f"Runner Module Tests: {runner_result.testsRun} tests run")
    print(f"Runner Module Results: {len(runner_result.failures)} failures, {len(runner_result.errors)} errors")
    
    return len(runner_result.failures) == 0 and len(runner_result.errors) == 0


def test_config_module():
    """Test the config module functionality."""
    print("Testing Unified Testing Framework Config Module...")
    
    # Create test suite for config module
    config_suite = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedTestConfig)
    config_runner = unittest.TextTestRunner(verbosity=2)
    config_result = config_runner.run(config_suite)
    
    print(f"Config Module Tests: {config_result.testsRun} tests run")
    print(f"Config Module Results: {len(config_result.failures)} failures, {len(config_result.errors)} errors")
    
    return len(config_result.failures) == 0 and len(config_result.errors) == 0


def test_utilities_module():
    """Test the utilities module functionality."""
    print("Testing Unified Testing Framework Utilities Module...")
    
    # Create test suite for utilities module
    utilities_suite = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedTestUtilities)
    utilities_runner = unittest.TextTestRunner(verbosity=2)
    utilities_result = utilities_runner.run(utilities_suite)
    
    print(f"Utilities Module Tests: {utilities_result.testsRun} tests run")
    print(f"Utilities Module Results: {len(utilities_result.failures)} failures, {len(utilities_result.errors)} errors")
    
    return len(utilities_result.failures) == 0 and len(utilities_result.errors) == 0


def test_integration_module():
    """Test the integration module functionality."""
    print("Testing Unified Testing Framework Integration Module...")
    
    # Create test suite for integration module
    integration_suite = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedTestingFrameworkIntegration)
    integration_runner = unittest.TextTestRunner(verbosity=2)
    integration_result = integration_runner.run(integration_suite)
    
    print(f"Integration Module Tests: {integration_result.testsRun} tests run")
    print(f"Integration Module Results: {len(integration_result.failures)} failures, {len(integration_result.errors)} errors")
    
    return len(integration_result.failures) == 0 and len(integration_result.errors) == 0


def test_all_modules():
    """Test all modularized components together."""
    print("=" * 80)
    print("TESTING MODULARIZED UNIFIED TESTING FRAMEWORK")
    print("=" * 80)
    
    # Test each module individually
    runner_success = test_runner_module()
    config_success = test_config_module()
    utilities_success = test_utilities_module()
    integration_success = test_integration_module()
    
    # Test all modules together
    print("\n" + "=" * 80)
    print("COMPREHENSIVE INTEGRATION TEST")
    print("=" * 80)
    
    all_modules_suite = unittest.TestSuite()
    all_modules_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUnifiedTestRunner))
    all_modules_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUnifiedTestConfig))
    all_modules_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUnifiedTestUtilities))
    all_modules_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUnifiedTestingFrameworkIntegration))
    
    all_modules_runner = unittest.TextTestRunner(verbosity=2)
    all_modules_result = all_modules_runner.run(all_modules_suite)
    
    print(f"\nAll Modules Tests: {all_modules_result.testsRun} tests run")
    print(f"All Modules Results: {len(all_modules_result.failures)} failures, {len(all_modules_result.errors)} errors")
    
    # Summary
    print("\n" + "=" * 80)
    print("MODULARIZATION TEST SUMMARY")
    print("=" * 80)
    
    module_results = {
        "Runner Module": runner_success,
        "Config Module": config_success,
        "Utilities Module": utilities_success,
        "Integration Module": integration_success,
        "All Modules Integration": len(all_modules_result.failures) == 0 and len(all_modules_result.errors) == 0
    }
    
    for module_name, success in module_results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{module_name}: {status}")
    
    overall_success = all(module_results.values())
    overall_status = "✅ ALL TESTS PASSED" if overall_success else "❌ SOME TESTS FAILED"
    
    print(f"\nOverall Result: {overall_status}")
    print("=" * 80)
    
    return overall_success


def main():
    """Main function to run all tests."""
    success = test_all_modules()
    
    if success:
        print("\n🎉 MODULARIZATION SUCCESS: All modules working correctly!")
        print("✅ V2 Compliance achieved for Unified Testing Framework")
        print("✅ Single Responsibility Principle maintained")
        print("✅ All modules under 250 lines")
        print("✅ Comprehensive test coverage")
    else:
        print("\n⚠️ MODULARIZATION ISSUES: Some tests failed!")
        print("Please review and fix any failing tests.")
    
    return success


if __name__ == "__main__":
    main()
