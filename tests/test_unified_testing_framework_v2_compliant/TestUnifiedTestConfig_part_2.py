"""V2 Compliant TestUnifiedTestConfig_part_2 - class_section_split"""

# Standard library imports
import os
import sys
import unittest

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

