"""Extracted TestUnifiedTestConfig class from test_unified_testing_framework"""

# Standard library imports
import os
import sys

#!/usr/bin/env python3
"""
Test Suite for Unified Testing Framework - Agent Cellphone V2
============================================================

Comprehensive test suite for the unified testing framework that validates
all three consolidated systems: test runner, configuration, and utilities.

Author: Agent-3 (Testing Framework Enhancement Manager)
License: MIT
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
from tests.unified_test_config import (
    UnifiedTestConfig, TestEnvironment, TestLevel, TestType,
    TestCategoryConfig, StandardsConfig, CoverageConfig,
    PerformanceConfig, ReportingConfig
)
from tests.unified_test_utilities import (
    UnifiedTestUtilities, MockObjectType, MockObjectConfig,
    TestDataConfig
)


# ============================================================================
# TEST UNIFIED TEST RUNNER SYSTEM
# ============================================================================

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


# ============================================================================
# TEST UNIFIED TEST CONFIGURATION SYSTEM
# ============================================================================

class TestUnifiedTestConfig(unittest.TestCase):
    """Test cases for the unified test configuration system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        
        # Create test directory structure
        (self.repo_root / "tests").mkdir()
        (self.repo_root / "tests" / "unit").mkdir()
        (self.repo_root / "tests" / "smoke").mkdir()
        (self.repo_root / "tests" / "integration").mkdir()
        (self.repo_root / "config").mkdir()
        (self.repo_root / "test_results").mkdir()
        (self.repo_root / "htmlcov").mkdir()
        (self.repo_root / "logs").mkdir()
        
        self.config = UnifiedTestConfig(self.repo_root)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_config_initialization(self):
        """Test configuration system initialization."""
        self.assertIsNotNone(self.config)
        self.assertEqual(self.config.repo_root, self.repo_root)
        self.assertIsInstance(self.config.environment, TestEnvironment)
        self.assertIsInstance(self.config.test_categories, dict)
        self.assertIsInstance(self.config.standards, StandardsConfig)
        self.assertIsInstance(self.config.coverage, CoverageConfig)
        self.assertIsInstance(self.config.performance, PerformanceConfig)
        self.assertIsInstance(self.config.reporting, ReportingConfig)
    
    def test_environment_detection(self):
        """Test environment detection."""
        # Test default environment (development)
        self.assertEqual(self.config.environment, TestEnvironment.DEVELOPMENT)
        
        # Test CI environment detection
        with patch.dict(os.environ, {"CI": "true"}):
            config = UnifiedTestConfig(self.repo_root)
            self.assertEqual(config.environment, TestEnvironment.CI)
        
        # Test custom environment
        with patch.dict(os.environ, {"TEST_ENVIRONMENT": "staging"}):
            config = UnifiedTestConfig(self.repo_root)
            self.assertEqual(config.environment, TestEnvironment.STAGING)
    
    def test_path_setup(self):
        """Test path setup functionality."""
        paths = self.config.paths
        
        self.assertEqual(paths["repo_root"], self.repo_root)
        self.assertEqual(paths["tests_dir"], self.repo_root / "tests")
        self.assertEqual(paths["src_dir"], self.repo_root / "src")
        self.assertEqual(paths["results_dir"], self.repo_root / "test_results")
        self.assertEqual(paths["coverage_dir"], self.repo_root / "htmlcov")
        self.assertEqual(paths["config_dir"], self.repo_root / "config")
        self.assertEqual(paths["logs_dir"], self.repo_root / "logs")
    
    def test_test_categories_initialization(self):
        """Test test categories initialization."""
        categories = self.config.test_categories
        
        # Check that all expected categories exist
        expected_categories = [
            "smoke", "unit", "integration", "performance", "security",
            "api", "behavior", "decision", "coordination", "learning"
        ]
        
        for category in expected_categories:
            self.assertIn(category, categories)
            self.assertIsInstance(categories[category], TestCategoryConfig)
    
    def test_test_category_configuration(self):
        """Test test category configuration."""
        unit_category = self.config.test_categories["unit"]
        
        self.assertEqual(unit_category.name, "unit")
        self.assertEqual(unit_category.description, "Unit tests for individual components")
        self.assertEqual(unit_category.marker, "unit")
        self.assertEqual(unit_category.timeout, 120)
        self.assertEqual(unit_category.level, TestLevel.CRITICAL)
        self.assertEqual(unit_category.directory, "unit")
        self.assertTrue(unit_category.enabled)
        self.assertTrue(unit_category.parallel)
        self.assertTrue(unit_category.coverage_required)
        self.assertEqual(unit_category.min_coverage, 80.0)
    
    def test_standards_configuration(self):
        """Test standards configuration."""
        standards = self.config.standards
        
        self.assertEqual(standards.max_loc_standard, 400)
        self.assertEqual(standards.max_loc_gui, 600)
        self.assertEqual(standards.max_loc_core, 400)
        self.assertEqual(standards.max_loc_services, 400)
        self.assertEqual(standards.max_loc_utils, 300)
        self.assertEqual(standards.max_loc_launchers, 400)
        
        # Check component descriptions
        self.assertIn("core", standards.components)
        self.assertIn("services", standards.components)
        self.assertIn("utils", standards.components)
    
    def test_coverage_configuration(self):
        """Test coverage configuration."""
        coverage = self.config.coverage
        
        self.assertTrue(coverage.enabled)
        self.assertEqual(coverage.min_coverage, 80.0)
        self.assertEqual(coverage.fail_under, 70.0)
        self.assertIn("html", coverage.report_formats)
        self.assertIn("term", coverage.report_formats)
        self.assertIn("xml", coverage.report_formats)
        
        # Check exclude patterns
        self.assertIn("*/tests/*", coverage.exclude_patterns)
        self.assertIn("*/__pycache__/*", coverage.exclude_patterns)
    
    def test_performance_configuration(self):
        """Test performance configuration."""
        performance = self.config.performance
        
        self.assertEqual(performance.timeout_multiplier, 1.0)
        self.assertEqual(performance.max_workers, 4)
        self.assertEqual(performance.parallel_threshold, 10)
        self.assertEqual(performance.memory_limit_mb, 1024)
        self.assertEqual(performance.cpu_limit_percent, 80)
        self.assertFalse(performance.enable_profiling)
        self.assertEqual(performance.profiling_interval, 5.0)
    
    def test_reporting_configuration(self):
        """Test reporting configuration."""
        reporting = self.config.reporting
        
        self.assertTrue(reporting.enabled)
        self.assertIn("text", reporting.output_formats)
        self.assertIn("json", reporting.output_formats)
        self.assertIn("html", reporting.output_formats)
        self.assertEqual(reporting.output_directory, "test_results")
        self.assertTrue(reporting.detailed_output)
        self.assertTrue(reporting.include_coverage)
        self.assertTrue(reporting.include_performance)
        self.assertTrue(reporting.include_standards)
        self.assertFalse(reporting.email_notifications)
        self.assertFalse(reporting.slack_notifications)
    
    def test_get_test_category(self):
        """Test getting test category by name."""
        unit_category = self.config.get_test_category("unit")
        self.assertIsNotNone(unit_category)
        self.assertEqual(unit_category.name, "unit")
        
        # Test non-existent category
        non_existent = self.config.get_test_category("non_existent")
        self.assertIsNone(non_existent)
    
    def test_get_enabled_categories(self):
        """Test getting enabled test categories."""
        enabled_categories = self.config.get_enabled_categories()
        
        self.assertIsInstance(enabled_categories, list)
        self.assertGreater(len(enabled_categories), 0)
        
        # All returned categories should be enabled
        for category_name in enabled_categories:
            category = self.config.get_test_category(category_name)
            self.assertTrue(category.enabled)
    
    def test_get_critical_categories(self):
        """Test getting critical test categories."""
        critical_categories = self.config.get_critical_categories()
        
        self.assertIsInstance(critical_categories, list)
        
        # All returned categories should be critical
        for category_name in critical_categories:
            category = self.config.get_test_category(category_name)
            self.assertEqual(category.level, TestLevel.CRITICAL)
    
    def test_get_standards_limit(self):
        """Test getting standards limits for component types."""
        # Test web component
        web_limit = self.config.get_standards_limit("web")
        self.assertEqual(web_limit, 600)
        
        # Test core component
        core_limit = self.config.get_standards_limit("core")
        self.assertEqual(core_limit, 400)
        
        # Test utils component
        utils_limit = self.config.get_standards_limit("utils")
        self.assertEqual(utils_limit, 300)
        
        # Test unknown component
        unknown_limit = self.config.get_standards_limit("unknown")
        self.assertEqual(unknown_limit, 400)  # Default standard limit
    
    def test_get_coverage_requirements(self):
        """Test getting coverage requirements for test categories."""
        # Test unit tests
        coverage_required, min_coverage = self.config.get_coverage_requirements("unit")
        self.assertTrue(coverage_required)
        self.assertEqual(min_coverage, 80.0)
        
        # Test performance tests
        coverage_required, min_coverage = self.config.get_coverage_requirements("performance")
        self.assertFalse(coverage_required)
        self.assertEqual(min_coverage, 50.0)
    
    def test_configuration_validation(self):
        """Test configuration validation."""
        issues = self.config.validate_configuration()
        
        # Should have no validation issues with proper setup
        self.assertEqual(len(issues), 0)
    
    def test_configuration_export(self):
        """Test configuration export functionality."""
        # Test JSON export
        json_config = self.config.export_configuration("json")
        self.assertIsInstance(json_config, str)
        
        # Parse JSON to verify structure
        parsed_config = json.loads(json_config)
        self.assertIn("environment", parsed_config)
        self.assertIn("test_categories", parsed_config)
        self.assertIn("standards", parsed_config)
        self.assertIn("coverage", parsed_config)
        self.assertIn("performance", parsed_config)
        self.assertIn("reporting", parsed_config)
        self.assertIn("paths", parsed_config)
        
        # Test YAML export
        try:
            yaml_config = self.config.export_configuration("yaml")
            self.assertIsInstance(yaml_config, str)
        except ValueError:
            # YAML export might not be available
            pass
    
    def test_configuration_save(self):
        """Test configuration save functionality."""
        config_file = self.repo_root / "test_config.json"
        
        self.config.save_configuration(config_file, "json")
        
        # Verify file was created
        self.assertTrue(config_file.exists())
        
        # Verify content is valid JSON
        with open(config_file, 'r') as f:
            saved_config = json.load(f)
        
        self.assertIn("environment", saved_config)
        self.assertIn("test_categories", saved_config)


# ============================================================================
# TEST UNIFIED TEST UTILITIES SYSTEM
# ============================================================================

class TestUnifiedTestUtilities(unittest.TestCase):
    """Test cases for the unified test utilities system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.utilities = UnifiedTestUtilities()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_utilities_initialization(self):
        """Test utilities system initialization."""
        self.assertIsNotNone(self.utilities)
        self.assertIsNotNone(self.utilities.logger)
    
    def test_create_mock_agent(self):
        """Test mock agent creation."""
        agent = self.utilities.create_mock_agent(
            agent_id="test_123",
            name="Test Agent",
            role="testing",
            capabilities=["testing", "validation"],
            status="active"
        )
        
        self.assertIsInstance(agent, Mock)
        self.assertEqual(agent.id, "test_123")
        self.assertEqual(agent.name, "Test Agent")
        self.assertEqual(agent.role, "testing")
        self.assertEqual(agent.status, "active")
        self.assertEqual(agent.capabilities, ["testing", "validation"])
        
        # Test mock methods
        self.assertTrue(agent.start())
        self.assertTrue(agent.stop())
        self.assertEqual(agent.get_status(), "active")
        self.assertEqual(agent.get_capabilities(), ["testing", "validation"])
    
    def test_create_mock_task(self):
        """Test mock task creation."""
        task = self.utilities.create_mock_task(
            task_id="task_123",
            name="Test Task",
            task_type="testing",
            priority="high",
            status="running",
            content="Test content",
            metadata={"test": True}
        )
        
        self.assertIsInstance(task, Mock)
        self.assertEqual(task.task_id, "task_123")
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.type, "testing")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.status, "running")
        self.assertEqual(task.content, "Test content")
        self.assertEqual(task.metadata, {"test": True})
        
        # Test mock methods
        self.assertTrue(task.start())
        self.assertTrue(task.complete())
        self.assertTrue(task.fail())
        self.assertEqual(task.get_progress(), 0.0)
    
    def test_create_mock_config(self):
        """Test mock configuration creation."""
        config = self.utilities.create_mock_config(
            config_type="development",
            overrides={"custom_setting": "value"}
        )
        
        self.assertIsInstance(config, Mock)
        self.assertTrue(config.debug)
        self.assertEqual(config.log_level, "INFO")
        self.assertEqual(config.timeout, 60)
        self.assertEqual(config.max_retries, 5)
        self.assertFalse(config.test_mode)
        self.assertEqual(config.environment, "development")
        self.assertEqual(config.custom_setting, "value")
        
        # Test mock methods
        self.assertEqual(config.get("timeout"), 60)
        self.assertEqual(config.get("non_existent", "default"), "default")
        self.assertTrue(config.has("timeout"))
        self.assertFalse(config.has("non_existent"))
        
        config_dict = config.to_dict()
        self.assertIn("timeout", config_dict)
        self.assertIn("custom_setting", config_dict)
    
    def test_create_mock_service(self):
        """Test mock service creation."""
        service = self.utilities.create_mock_service(
            service_name="TestService",
            methods=["start", "stop", "execute"],
            return_values={"start": True, "stop": True, "execute": "success"}
        )
        
        self.assertIsInstance(service, Mock)
        self.assertEqual(service.name, "TestService")
        self.assertEqual(service.status, "stopped")
        
        # Test mock methods
        self.assertTrue(service.start())
        self.assertTrue(service.stop())
        self.assertEqual(service.execute(), "success")
    
    def test_create_mock_manager(self):
        """Test mock manager creation."""
        manager = self.utilities.create_mock_manager(
            manager_name="TestManager",
            managed_objects=["obj1", "obj2"],
            methods=["add", "remove", "get", "list"]
        )
        
        self.assertIsInstance(manager, Mock)
        self.assertEqual(manager.name, "TestManager")
        self.assertEqual(manager.managed_objects, ["obj1", "obj2"])
        self.assertEqual(manager.object_count, 2)
        
        # Test mock methods
        self.assertTrue(manager.add())
        self.assertTrue(manager.remove())
        self.assertEqual(manager.get(), "obj1")
        self.assertEqual(manager.list(), ["obj1", "obj2"])
        self.assertEqual(manager.count(), 2)
    
    def test_create_test_data(self):
        """Test test data creation."""
        # Single test data
        single_data = self.utilities.create_test_data(
            data_type="user",
            properties={"name": "Test User", "email": "test@example.com"},
            relationships=["profile", "settings"]
        )
        
        self.assertIsInstance(single_data, dict)
        self.assertIn("id", single_data)
        self.assertEqual(single_data["type"], "user")
        self.assertEqual(single_data["name"], "Test User")
        self.assertEqual(single_data["email"], "test@example.com")
        self.assertIn("profile_id", single_data)
        self.assertIn("settings_id", single_data)
        self.assertTrue(single_data["test"])
        
        # Multiple test data
        multiple_data = self.utilities.create_test_data(
            data_type="post",
            size=3,
            properties={"title": "Test Post"}
        )
        
        self.assertIsInstance(multiple_data, list)
        self.assertEqual(len(multiple_data), 3)
        
        for item in multiple_data:
            self.assertEqual(item["type"], "post")
            self.assertEqual(item["title"], "Test Post")
    
    def test_create_test_file(self):
        """Test test file creation."""
        test_file = self.utilities.create_test_file(
            content="Test file content",
            extension=".txt",
            directory=self.temp_dir
        )
        
        self.assertIsInstance(test_file, Path)
        self.assertTrue(test_file.exists())
        self.assertEqual(test_file.suffix, ".txt")
        
        # Verify content
        with open(test_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, "Test file content")
    
    def test_create_test_directory(self):
        """Test test directory creation."""
        test_dir = self.utilities.create_test_directory(
            name="test_dir",
            parent=self.temp_dir,
            files=["file1.txt", "file2.txt"]
        )
        
        self.assertIsInstance(test_dir, Path)
        self.assertTrue(test_dir.exists())
        self.assertTrue(test_dir.is_dir())
        
        # Verify files were created
        for file_name in ["file1.txt", "file2.txt"]:
            file_path = test_dir / file_name
            self.assertTrue(file_path.exists())
    
    def test_assert_test_results(self):
        """Test test results assertion."""
        # Valid test results
        valid_results = {
            "total": 10,
            "passed": 8,
            "failed": 1,
            "errors": 1,
            "status": "completed"
        }
        
        # Should not raise exception
        self.utilities.assert_test_results(
            valid_results,
            expected_keys=["total", "passed", "failed", "errors"],
            min_tests=5,
            required_status="completed"
        )
        
        # Invalid test results (missing key)
        invalid_results = {"total": 5, "passed": 4}
        
        with self.assertRaises(AssertionError):
            self.utilities.assert_test_results(
                invalid_results,
                expected_keys=["total", "passed", "failed"]
            )
    
    def test_assert_mock_called_with(self):
        """Test mock assertion functionality."""
        mock_obj = Mock()
        mock_obj.test_method = Mock(return_value=True)
        
        # Call the method
        mock_obj.test_method("arg1", "arg2", kwarg1="value1")
        
        # Should not raise exception
        self.utilities.assert_mock_called_with(
            mock_obj,
            "test_method",
            expected_args=("arg1", "arg2"),
            expected_kwargs={"kwarg1": "value1"}
        )
        
        # Test with wrong arguments
        with self.assertRaises(AssertionError):
            self.utilities.assert_mock_called_with(
                mock_obj,
                "test_method",
                expected_args=("wrong", "args")
            )
    
    def test_file_assertions(self):
        """Test file and directory assertions."""
        # Create test file
        test_file = self.temp_dir / "test_file.txt"
        test_file.touch()
        
        # Create test directory
        test_dir = self.temp_dir / "test_dir"
        test_dir.mkdir()
        
        # Should not raise exceptions
        self.utilities.assert_file_exists(test_file)
        self.utilities.assert_directory_exists(test_dir)
        
        # Test non-existent file/directory
        non_existent_file = self.temp_dir / "non_existent.txt"
        non_existent_dir = self.temp_dir / "non_existent"
        
        with self.assertRaises(AssertionError):
            self.utilities.assert_file_exists(non_existent_file)
        
        with self.assertRaises(AssertionError):
            self.utilities.assert_directory_exists(non_existent_dir)
    
    def test_cleanup_utilities(self):
        """Test cleanup utilities."""
        # Create test files and directories
        test_file = self.temp_dir / "cleanup_test.txt"
        test_file.touch()
        
        test_dir = self.temp_dir / "cleanup_test_dir"
        test_dir.mkdir()
        (test_dir / "nested_file.txt").touch()
        
        # Verify they exist
        self.assertTrue(test_file.exists())
        self.assertTrue(test_dir.exists())
        
        # Clean up
        self.utilities.cleanup_test_files([test_file])
        self.utilities.cleanup_test_directories([test_dir])
        
        # Verify they were removed
        self.assertFalse(test_file.exists())
        self.assertFalse(test_dir.exists())
    
    def test_mock_reset(self):
        """Test mock object reset functionality."""
        mock_obj = Mock()
        mock_obj.test_method = Mock(return_value=True)
        
        # Call the method
        mock_obj.test_method()
        
        # Verify it was called
        self.assertEqual(mock_obj.test_method.call_count, 1)
        
        # Reset
        self.utilities.reset_mock_objects([mock_obj])
        
        # Verify it was reset
        self.assertEqual(mock_obj.test_method.call_count, 0)
    
    def test_environment_utilities(self):
        """Test environment setup and restore utilities."""
        # Setup test environment
        env_state = self.utilities.setup_test_environment(
            env_vars={"TEST_VAR": "test_value"},
            working_dir=self.temp_dir
        )
        
        # Verify environment was set
        self.assertEqual(os.environ.get("TEST_VAR"), "test_value")
        self.assertEqual(os.getcwd(), self.temp_dir)
        
        # Restore environment
        self.utilities.restore_test_environment(env_state)
        
        # Verify environment was restored
        self.assertNotIn("TEST_VAR", os.environ)
    
    def test_command_execution(self):
        """Test command execution utilities."""
        # Test successful command
        return_code, stdout, stderr = self.utilities.run_command_with_timeout(
            ["echo", "test output"],
            timeout=5
        )
        
        self.assertEqual(return_code, 0)
        self.assertIn("test output", stdout)
        self.assertEqual(stderr, "")
        
        # Test command timeout
        return_code, stdout, stderr = self.utilities.run_command_with_timeout(
            ["sleep", "10"],
            timeout=1
        )
        
        self.assertEqual(return_code, -1)
        self.assertIn("timed out", stderr)
    
    def test_condition_waiting(self):
        """Test condition waiting utilities."""
        # Test successful condition
        start_time = time.time()
        result = self.utilities.wait_for_condition(
            lambda: time.time() - start_time > 0.1,
            timeout=1,
            interval=0.05
        )
        
        self.assertTrue(result)
        
        # Test timeout condition
        result = self.utilities.wait_for_condition(
            lambda: False,
            timeout=0.1,
            interval=0.01
        )
        
        self.assertFalse(result)
    
    def test_test_summary_generation(self):
        """Test test summary generation."""
        test_results = [
            {"status": "passed"},
            {"status": "passed"},
            {"status": "failed"},
            {"status": "error"}
        ]
        
        summary = self.utilities.generate_test_summary(test_results)
        
        self.assertEqual(summary["total"], 4)
        self.assertEqual(summary["passed"], 2)
        self.assertEqual(summary["failed"], 1)
        self.assertEqual(summary["errors"], 1)
        self.assertEqual(summary["success_rate"], 50.0)
        self.assertIn("details", summary)
        
        # Test without details
        summary_no_details = self.utilities.generate_test_summary(
            test_results, include_details=False
        )
        
        self.assertNotIn("details", summary_no_details)
    
    def test_test_report_saving(self):
        """Test test report saving functionality."""
        report_data = {
            "summary": {"total": 10, "passed": 8, "failed": 2},
            "details": ["detail1", "detail2"]
        }
        
        report_file = self.temp_dir / "test_report.json"
        
        self.utilities.save_test_report(report_data, report_file, "json")
        
        # Verify file was created
        self.assertTrue(report_file.exists())
        
        # Verify content
        with open(report_file, 'r') as f:
            saved_report = json.load(f)
        
        self.assertEqual(saved_report["summary"]["total"], 10)
        self.assertEqual(saved_report["summary"]["passed"], 8)
        self.assertEqual(saved_report["summary"]["failed"], 2)
        self.assertEqual(saved_report["details"], ["detail1", "detail2"])


# ============================================================================
# TEST INTEGRATION BETWEEN SYSTEMS
# ============================================================================

class TestUnifiedTestingFrameworkIntegration(unittest.TestCase):
    """Test cases for integration between unified testing framework systems."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_root = Path(self.temp_dir)
        
        # Create test directory structure
        (self.repo_root / "tests").mkdir()
        (self.repo_root / "tests" / "unit").mkdir()
        (self.repo_root / "tests" / "smoke").mkdir()
        
        # Initialize all systems
        self.config = UnifiedTestConfig(self.repo_root)
        self.runner = UnifiedTestRunner(self.repo_root)
        self.utilities = UnifiedTestUtilities()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_config_runner_integration(self):
        """Test integration between configuration and runner systems."""
        # Configure runner with config system
        runner_config = TestExecutionConfig(
            mode=TestMode.UNIT,
            parallel=True,
            timeout=120
        )
        self.runner.configure_execution(runner_config)
        
        # Verify configuration is applied
        self.assertEqual(self.runner.execution_config.mode, TestMode.UNIT)
        self.assertTrue(self.runner.execution_config.parallel)
        self.assertEqual(self.runner.execution_config.timeout, 120)
        
        # Verify runner uses config system categories
        unit_category = self.config.get_test_category("unit")
        runner_unit_category = self.runner.test_categories["unit"]
        
        self.assertEqual(unit_category.timeout, runner_unit_category.timeout)
        self.assertEqual(unit_category.priority.value, runner_unit_category.priority.value)
    
    def test_utilities_runner_integration(self):
        """Test integration between utilities and runner systems."""
        # Create mock objects using utilities
        mock_agent = self.utilities.create_mock_agent()
        mock_task = self.utilities.create_mock_task()
        
        # Use mock objects in runner context
        test_files = self.runner.discover_tests("unit")
        
        # Create test results using utilities
        test_results = [
            {"status": "passed", "test_name": "test1"},
            {"status": "passed", "test_name": "test2"},
            {"status": "failed", "test_name": "test3"}
        ]
        
        # Generate summary using utilities
        summary = self.utilities.generate_test_summary(test_results)
        
        # Verify integration works
        self.assertEqual(summary["total"], 3)
        self.assertEqual(summary["passed"], 2)
        self.assertEqual(summary["failed"], 1)
    
    def test_full_workflow_integration(self):
        """Test full workflow integration between all systems."""
        # 1. Setup test environment using utilities
        env_state = self.utilities.setup_test_environment(
            env_vars={"TEST_MODE": "integration"}
        )
        
        # 2. Configure test execution using config system
        runner_config = TestExecutionConfig(
            mode=TestMode.SMOKE,
            parallel=False,
            timeout=60,
            coverage=True
        )
        self.runner.configure_execution(runner_config)
        
        # 3. Discover tests using runner
        test_files = self.runner.discover_tests("smoke")
        
        # 4. Create mock test data using utilities
        test_data = self.utilities.create_test_data(
            data_type="test_result",
            size=len(test_files),
            properties={"framework": "unified"}
        )
        
        # 5. Generate test summary using utilities
        summary = self.utilities.generate_test_summary(test_data)
        
        # 6. Save report using utilities
        report_file = self.temp_dir / "integration_test_report.json"
        self.utilities.save_test_report(summary, report_file, "json")
        
        # 7. Verify integration results
        self.assertTrue(report_file.exists())
        
        with open(report_file, 'r') as f:
            saved_report = json.load(f)
        
        self.assertIn("total", saved_report)
        self.assertIn("success_rate", saved_report)
        
        # 8. Restore environment
        self.utilities.restore_test_environment(env_state)
        
        # Verify all systems worked together
        self.assertIsInstance(test_files, list)
        self.assertIsInstance(test_data, list)
        self.assertIsInstance(summary, dict)
        self.assertTrue(report_file.exists())


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestUnifiedTestRunner))
    test_suite.addTest(unittest.makeSuite(TestUnifiedTestConfig))
    test_suite.addTest(unittest.makeSuite(TestUnifiedTestUtilities))
    test_suite.addTest(unittest.makeSuite(TestUnifiedTestingFrameworkIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("UNIFIED TESTING FRAMEWORK TEST RESULTS")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    # Exit with appropriate code
    if result.failures or result.errors:
        exit(1)
    else:
        exit(0)
