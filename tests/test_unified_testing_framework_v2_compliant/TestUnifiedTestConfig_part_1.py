"""V2 Compliant TestUnifiedTestConfig_part_1 - class_section_split"""

# Standard library imports
import os
import sys
import unittest

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
