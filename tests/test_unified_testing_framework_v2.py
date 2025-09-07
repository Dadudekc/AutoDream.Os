#!/usr/bin/env python3
"""
Test Suite for Unified Testing Framework V2 - Agent Cellphone V2
===============================================================

Comprehensive test suite for V2-compliant unified testing framework.
Tests all modular components and their integration.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import json
import time

# Import V2-compliant components
from .core import (
    TestMode, TestStatus, TestPriority, TestEnvironment,
    TestCategory, TestResult, TestExecutionConfig, TestSuite, TestReport,
    TestUtilityType, MockObjectType, TestDataType, ValidationType,
    MockObjectConfig, TestDataConfig, ValidationRule, TestEnvConfig, TestReportConfig
)

from .unified_test_runner_v2 import UnifiedTestRunnerV2
from .unified_test_config_v2 import UnifiedTestConfigV2
from .unified_test_utilities_v2 import UnifiedTestUtilitiesV2


class TestUnifiedTestRunnerV2(unittest.TestCase):
    """Test cases for V2-compliant unified test runner."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        self.runner = UnifiedTestRunnerV2(self.repo_root)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test runner initialization."""
        self.assertIsNotNone(self.runner)
        self.assertEqual(self.runner.repo_root, self.repo_root)
        self.assertIsInstance(self.runner.test_categories, dict)
        self.assertIsInstance(self.runner.execution_config, TestExecutionConfig)
    
    def test_test_categories_initialization(self):
        """Test test categories initialization."""
        categories = self.runner.test_categories
        expected_categories = ["smoke", "unit", "integration", "performance", "security", "api"]
        
        for category in expected_categories:
            self.assertIn(category, categories)
            self.assertIsInstance(categories[category], TestCategory)
    
    def test_discover_tests_empty_directory(self):
        """Test test discovery in empty directory."""
        test_files = self.runner.discover_tests()
        self.assertEqual(len(test_files), 0)
    
    def test_discover_tests_with_files(self):
        """Test test discovery with test files."""
        # Create test files
        test_dir = self.repo_root / "tests"
        test_dir.mkdir(parents=True)
        
        (test_dir / "test_example.py").write_text("def test_something(): pass")
        (test_dir / "test_another.py").write_text("def test_another(): pass")
        (test_dir / "not_a_test.py").write_text("def not_a_test(): pass")
        
        test_files = self.runner.discover_tests()
        self.assertEqual(len(test_files), 2)
        self.assertTrue(any("test_example.py" in f for f in test_files))
        self.assertTrue(any("test_another.py" in f for f in test_files))
    
    def test_run_test_success(self):
        """Test running a successful test."""
        # Create a simple test file
        test_dir = self.repo_root / "tests"
        test_dir.mkdir(parents=True)
        test_file = test_dir / "test_success.py"
        test_file.write_text("""
def test_success():
    assert True
""")
        
        result = self.runner.run_test(str(test_file), "unit")
        self.assertEqual(result.status, TestStatus.PASSED)
        self.assertIsInstance(result.duration, float)
        self.assertIsInstance(result.timestamp, str)
    
    def test_run_test_failure(self):
        """Test running a failing test."""
        # Create a failing test file
        test_dir = self.repo_root / "tests"
        test_dir.mkdir(parents=True)
        test_file = test_dir / "test_failure.py"
        test_file.write_text("""
def test_failure():
    assert False
""")
        
        result = self.runner.run_test(str(test_file), "unit")
        self.assertEqual(result.status, TestStatus.FAILED)
        self.assertIsInstance(result.duration, float)
        self.assertIsInstance(result.timestamp, str)


class TestUnifiedTestConfigV2(unittest.TestCase):
    """Test cases for V2-compliant unified test configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        self.config = UnifiedTestConfigV2(self.repo_root)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test configuration initialization."""
        self.assertIsNotNone(self.config)
        self.assertEqual(self.config.repo_root, self.repo_root)
        self.assertIsInstance(self.config.environment, TestEnvironment)
        self.assertIsInstance(self.config.test_categories, dict)
    
    def test_environment_detection(self):
        """Test environment detection."""
        # Test default environment
        self.assertEqual(self.config.environment, TestEnvironment.LOCAL)
        
        # Test CI environment
        with patch.dict('os.environ', {'CI': 'true'}):
            config = UnifiedTestConfigV2(self.repo_root)
            self.assertEqual(config.environment, TestEnvironment.CI)
    
    def test_test_categories_initialization(self):
        """Test test categories initialization."""
        categories = self.config.test_categories
        expected_categories = ["smoke", "unit", "integration", "performance", "security", "api"]
        
        for category in expected_categories:
            self.assertIn(category, categories)
            self.assertIsInstance(categories[category], TestCategoryConfig)
    
    def test_get_category_config(self):
        """Test getting category configuration."""
        config = self.config.get_category_config("unit")
        self.assertIsInstance(config, TestCategoryConfig)
        self.assertEqual(config.name, "unit")
        self.assertEqual(config.level, TestLevel.CRITICAL)
    
    def test_is_category_enabled(self):
        """Test category enabled status."""
        self.assertTrue(self.config.is_category_enabled("unit"))
        self.assertFalse(self.config.is_category_enabled("nonexistent"))
    
    def test_validate_standards(self):
        """Test standards validation."""
        # Create a test file
        test_file = self.repo_root / "test_file.py"
        test_file.write_text("print('hello')\n" * 100)  # 100 lines
        
        result = self.config.validate_standards(test_file)
        self.assertIn("file_path", result)
        self.assertIn("line_count", result)
        self.assertIn("compliant", result)
        self.assertEqual(result["line_count"], 100)
    
    def test_export_config(self):
        """Test configuration export."""
        json_config = self.config.export_config("json")
        self.assertIsInstance(json_config, str)
        
        # Parse JSON to verify structure
        config_data = json.loads(json_config)
        self.assertIn("environment", config_data)
        self.assertIn("test_categories", config_data)
        self.assertIn("coverage", config_data)
        self.assertIn("performance", config_data)
        self.assertIn("reporting", config_data)


class TestUnifiedTestUtilitiesV2(unittest.TestCase):
    """Test cases for V2-compliant unified test utilities."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.utilities = UnifiedTestUtilitiesV2()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test utilities initialization."""
        self.assertIsNotNone(self.utilities)
        self.assertIsInstance(self.utilities.logger, type(self.utilities.logger))
    
    def test_create_mock_agent(self):
        """Test mock agent creation."""
        mock_agent = self.utilities.create_mock_agent()
        self.assertIsInstance(mock_agent, Mock)
        self.assertEqual(mock_agent.agent_id, "test_agent_001")
        self.assertEqual(mock_agent.name, "Test Agent")
        self.assertEqual(mock_agent.role, "testing")
        self.assertEqual(mock_agent.status, "active")
    
    def test_create_mock_agent_with_config(self):
        """Test mock agent creation with custom config."""
        config = MockObjectConfig(
            object_type=MockObjectType.AGENT,
            properties={
                "agent_id": "custom_agent",
                "name": "Custom Agent",
                "role": "custom_role"
            }
        )
        
        mock_agent = self.utilities.create_mock_agent(config)
        self.assertEqual(mock_agent.agent_id, "custom_agent")
        self.assertEqual(mock_agent.name, "Custom Agent")
        self.assertEqual(mock_agent.role, "custom_role")
    
    def test_create_mock_task(self):
        """Test mock task creation."""
        mock_task = self.utilities.create_mock_task()
        self.assertIsInstance(mock_task, Mock)
        self.assertEqual(mock_task.task_id, "test_task_001")
        self.assertEqual(mock_task.name, "Test Task")
        self.assertEqual(mock_task.status, "pending")
        self.assertEqual(mock_task.priority, "medium")
    
    def test_create_mock_config(self):
        """Test mock config creation."""
        mock_config = self.utilities.create_mock_config()
        self.assertIsInstance(mock_config, Mock)
        self.assertEqual(mock_config.config_id, "test_config_001")
        self.assertEqual(mock_config.name, "Test Config")
        self.assertEqual(mock_config.type, "test")
        self.assertTrue(mock_config.enabled)
    
    def test_generate_test_data_user(self):
        """Test user test data generation."""
        config = TestDataConfig(data_type=TestDataType.USER)
        data = self.utilities.generate_test_data(config)
        
        self.assertIsInstance(data, dict)
        self.assertIn("user_id", data)
        self.assertIn("username", data)
        self.assertIn("email", data)
        self.assertIn("role", data)
        self.assertIn("status", data)
        self.assertIn("created_at", data)
    
    def test_generate_test_data_task(self):
        """Test task test data generation."""
        config = TestDataConfig(data_type=TestDataType.TASK)
        data = self.utilities.generate_test_data(config)
        
        self.assertIsInstance(data, dict)
        self.assertIn("task_id", data)
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("status", data)
        self.assertIn("priority", data)
        self.assertIn("created_at", data)
    
    def test_generate_test_data_multiple(self):
        """Test multiple test data generation."""
        config = TestDataConfig(data_type=TestDataType.USER, size=3)
        data = self.utilities.generate_test_data(config)
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        for item in data:
            self.assertIsInstance(item, dict)
            self.assertIn("user_id", item)
    
    def test_create_temp_file(self):
        """Test temporary file creation."""
        content = "test content"
        temp_file = self.utilities.create_temp_file(content)
        
        self.assertIsInstance(temp_file, Path)
        self.assertTrue(temp_file.exists())
        self.assertEqual(temp_file.read_text(), content)
        
        # Cleanup
        self.utilities.cleanup_temp_files(temp_file)
    
    def test_create_temp_directory(self):
        """Test temporary directory creation."""
        temp_dir = self.utilities.create_temp_directory()
        
        self.assertIsInstance(temp_dir, Path)
        self.assertTrue(temp_dir.exists())
        self.assertTrue(temp_dir.is_dir())
        
        # Cleanup
        self.utilities.cleanup_temp_files(temp_dir)
    
    def test_create_test_file_structure(self):
        """Test test file structure creation."""
        base_path = Path(self.temp_dir)
        structure = {
            "file1.txt": "content1",
            "dir1": {
                "file2.txt": "content2",
                "dir2": {
                    "file3.txt": "content3"
                }
            }
        }
        
        self.utilities.create_test_file_structure(base_path, structure)
        
        # Verify structure
        self.assertTrue((base_path / "file1.txt").exists())
        self.assertTrue((base_path / "dir1" / "file2.txt").exists())
        self.assertTrue((base_path / "dir1" / "dir2" / "file3.txt").exists())
        
        self.assertEqual((base_path / "file1.txt").read_text(), "content1")
        self.assertEqual((base_path / "dir1" / "file2.txt").read_text(), "content2")
        self.assertEqual((base_path / "dir1" / "dir2" / "file3.txt").read_text(), "content3")
    
    def test_validate_object(self):
        """Test object validation."""
        class TestObject:
            def __init__(self):
                self.name = "test"
                self.age = 25
        
        obj = TestObject()
        rules = [
            ValidationRule("name", ValidationType.STRING, required=True, min_length=1),
            ValidationRule("age", ValidationType.INTEGER, required=True, min_value=0)
        ]
        
        result = self.utilities.validate_object(obj, rules)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)
    
    def test_validate_object_with_errors(self):
        """Test object validation with errors."""
        class TestObject:
            def __init__(self):
                self.name = ""  # Too short
                self.age = -1   # Too small
        
        obj = TestObject()
        rules = [
            ValidationRule("name", ValidationType.STRING, required=True, min_length=1),
            ValidationRule("age", ValidationType.INTEGER, required=True, min_value=0)
        ]
        
        result = self.utilities.validate_object(obj, rules)
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["errors"]), 0)
    
    def test_setup_test_environment(self):
        """Test test environment setup."""
        config = TestEnvConfig(
            name="test_env",
            description="Test environment",
            variables={"TEST_VAR": "test_value"},
            setup_commands=["echo 'setup'"]
        )
        
        result = self.utilities.setup_test_environment(config)
        self.assertTrue(result)
        self.assertEqual(os.environ.get("TEST_VAR"), "test_value")
    
    def test_generate_test_report(self):
        """Test test report generation."""
        config = TestReportConfig(
            title="Test Report",
            description="Test report description",
            results={"test1": "passed", "test2": "failed"},
            summary={"total": 2, "passed": 1, "failed": 1}
        )
        
        report = self.utilities.generate_test_report(config)
        self.assertIsInstance(report, str)
        
        # Parse JSON to verify structure
        report_data = json.loads(report)
        self.assertEqual(report_data["title"], "Test Report")
        self.assertEqual(report_data["description"], "Test report description")
        self.assertIn("results", report_data)
        self.assertIn("summary", report_data)


class TestUnifiedTestingFrameworkV2Integration(unittest.TestCase):
    """Integration tests for V2-compliant unified testing framework."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        self.runner = UnifiedTestRunnerV2(self.repo_root)
        self.config = UnifiedTestConfigV2(self.repo_root)
        self.utilities = UnifiedTestUtilitiesV2()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_framework_integration(self):
        """Test integration between all framework components."""
        # Create test files
        test_dir = self.repo_root / "tests"
        test_dir.mkdir(parents=True)
        
        (test_dir / "test_integration.py").write_text("""
def test_integration():
    assert True
""")
        
        # Test configuration
        self.assertTrue(self.config.is_category_enabled("unit"))
        category_config = self.config.get_category_config("unit")
        self.assertIsInstance(category_config, TestCategoryConfig)
        
        # Test utilities
        mock_agent = self.utilities.create_mock_agent()
        self.assertIsInstance(mock_agent, Mock)
        
        # Test runner
        test_files = self.runner.discover_tests()
        self.assertGreater(len(test_files), 0)
        
        # Test full integration
        if test_files:
            result = self.runner.run_test(test_files[0], "unit")
            self.assertIsInstance(result, TestResult)
            self.assertIsInstance(result.status, TestStatus)


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)
