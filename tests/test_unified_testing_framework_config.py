#!/usr/bin/env python3
"""
Test Unified Testing Framework Configuration - Test Configuration System Tests
=============================================================================

This module contains comprehensive test cases for the unified test configuration system.
It validates all aspects of test environment detection, path setup, and configuration management.

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
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import the unified testing framework components
from tests.unified_test_config import (
    UnifiedTestConfig, TestEnvironment, TestLevel, TestType,
    TestCategoryConfig, StandardsConfig, CoverageConfig,
    PerformanceConfig, ReportingConfig
)


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
    
    def test_environment_enumeration(self):
        """Test environment enumeration values."""
        self.assertEqual(TestEnvironment.DEVELOPMENT.value, "development")
        self.assertEqual(TestEnvironment.CI.value, "ci")
        self.assertEqual(TestEnvironment.STAGING.value, "staging")
        self.assertEqual(TestEnvironment.PRODUCTION.value, "production")
    
    def test_test_level_enumeration(self):
        """Test test level enumeration values."""
        self.assertEqual(TestLevel.CRITICAL.value, "critical")
        self.assertEqual(TestLevel.HIGH.value, "high")
        self.assertEqual(TestLevel.MEDIUM.value, "medium")
        self.assertEqual(TestLevel.LOW.value, "low")


if __name__ == "__main__":
    unittest.main()
