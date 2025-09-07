#!/usr/bin/env python3
"""
Test Unified Testing Framework Runner - Test Runner System Tests
===============================================================

This module contains comprehensive test cases for the unified test runner system.
It validates all aspects of test discovery, execution, and result management.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-002 - Unified Testing Framework Modularization
**Status:** MODULARIZATION IN PROGRESS
**Target:** ≤250 lines per module, single responsibility principle
**V2 Compliance:** ✅ Under 250 lines, focused responsibility
"""

import unittest
import tempfile
import shutil
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import the unified testing framework components
from tests.unified_test_runner import (
    UnifiedTestRunner, TestMode, TestStatus, TestPriority,
    TestCategory, TestResult, TestExecutionConfig
)


class TestUnifiedTestRunner(unittest.TestCase):
    """Test cases for the unified test runner system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        self.runner = UnifiedTestRunner(self.repo_root)
        
        # Create test directory structure
        (self.repo_root / "tests").mkdir()
        (self.repo_root / "tests" / "unit").mkdir()
        (self.repo_root / "tests" / "smoke").mkdir()
        
        # Create test files
        (self.repo_root / "tests" / "unit" / "test_example.py").touch()
        (self.repo_root / "tests" / "smoke" / "test_smoke.py").touch()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_runner_initialization(self):
        """Test test runner initialization."""
        self.assertIsNotNone(self.runner)
        self.assertEqual(self.runner.repo_root, self.repo_root)
        self.assertIsInstance(self.runner.test_categories, dict)
        self.assertGreater(len(self.runner.test_categories), 0)
    
    def test_test_categories_initialization(self):
        """Test test categories initialization."""
        categories = self.runner.test_categories
        
        # Check that all expected categories exist
        expected_categories = ["smoke", "unit", "integration", "performance", "security", "api"]
        for category in expected_categories:
            self.assertIn(category, categories)
            self.assertIsInstance(categories[category], TestCategory)
    
    def test_test_category_configuration(self):
        """Test test category configuration."""
        smoke_category = self.runner.test_categories["smoke"]
        
        self.assertEqual(smoke_category.name, "smoke")
        self.assertEqual(smoke_category.marker, "smoke")
        self.assertEqual(smoke_category.timeout, 60)
        self.assertEqual(smoke_category.priority, TestPriority.CRITICAL)
        self.assertEqual(smoke_category.directory, "smoke")
        self.assertTrue(smoke_category.enabled)
        self.assertFalse(smoke_category.parallel)
    
    def test_execution_configuration(self):
        """Test execution configuration."""
        config = TestExecutionConfig(
            mode=TestMode.SMOKE,
            parallel=True,
            timeout=120,
            verbose=True
        )
        
        self.runner.configure_execution(config)
        self.assertEqual(self.runner.execution_config.mode, TestMode.SMOKE)
        self.assertTrue(self.runner.execution_config.parallel)
        self.assertEqual(self.runner.execution_config.timeout, 120)
        self.assertTrue(self.runner.execution_config.verbose)
    
    def test_test_discovery(self):
        """Test test discovery functionality."""
        test_files = self.runner.discover_tests()
        
        # Should discover test files in subdirectories
        self.assertGreater(len(test_files), 0)
        
        # Check that test files from different categories are discovered
        test_file_names = [Path(f).name for f in test_files]
        self.assertIn("test_example.py", test_file_names)
        self.assertIn("test_smoke.py", test_file_names)
    
    def test_category_specific_discovery(self):
        """Test category-specific test discovery."""
        unit_tests = self.runner.discover_tests("unit")
        smoke_tests = self.runner.discover_tests("smoke")
        
        self.assertGreater(len(unit_tests), 0)
        self.assertGreater(len(smoke_tests), 0)
        
        # Unit tests should only contain unit test files
        for test_file in unit_tests:
            self.assertIn("unit", test_file)
        
        # Smoke tests should only contain smoke test files
        for test_file in smoke_tests:
            self.assertIn("smoke", test_file)
    
    def test_test_execution_config(self):
        """Test test execution configuration dataclass."""
        config = TestExecutionConfig(
            mode=TestMode.UNIT,
            parallel=False,
            max_workers=2,
            timeout=180,
            verbose=False,
            coverage=True,
            fail_fast=True
        )
        
        self.assertEqual(config.mode, TestMode.UNIT)
        self.assertFalse(config.parallel)
        self.assertEqual(config.max_workers, 2)
        self.assertEqual(config.timeout, 180)
        self.assertFalse(config.verbose)
        self.assertTrue(config.coverage)
        self.assertTrue(config.fail_fast)
    
    def test_test_result_creation(self):
        """Test test result creation."""
        result = TestResult(
            test_name="test_example",
            category="unit",
            status=TestStatus.PASSED,
            duration=1.5,
            output="Test passed successfully",
            timestamp="2025-01-28 10:00:00"
        )
        
        self.assertEqual(result.test_name, "test_example")
        self.assertEqual(result.category, "unit")
        self.assertEqual(result.status, TestStatus.PASSED)
        self.assertEqual(result.duration, 1.5)
        self.assertEqual(result.output, "Test passed successfully")
        self.assertEqual(result.timestamp, "2025-01-28 10:00:00")
    
    def test_test_mode_enumeration(self):
        """Test test mode enumeration values."""
        self.assertEqual(TestMode.SMOKE.value, "smoke")
        self.assertEqual(TestMode.UNIT.value, "unit")
        self.assertEqual(TestMode.INTEGRATION.value, "integration")
        self.assertEqual(TestMode.PERFORMANCE.value, "performance")
        self.assertEqual(TestMode.SECURITY.value, "security")
        self.assertEqual(TestMode.API.value, "api")
    
    def test_test_status_enumeration(self):
        """Test test status enumeration values."""
        self.assertEqual(TestStatus.PASSED.value, "passed")
        self.assertEqual(TestStatus.FAILED.value, "failed")
        self.assertEqual(TestStatus.SKIPPED.value, "skipped")
        self.assertEqual(TestStatus.ERROR.value, "error")
        self.assertEqual(TestStatus.TIMEOUT.value, "timeout")
    
    def test_test_priority_enumeration(self):
        """Test test priority enumeration values."""
        self.assertEqual(TestPriority.CRITICAL.value, "critical")
        self.assertEqual(TestPriority.HIGH.value, "high")
        self.assertEqual(TestPriority.MEDIUM.value, "medium")
        self.assertEqual(TestPriority.LOW.value, "low")


if __name__ == "__main__":
    unittest.main()
