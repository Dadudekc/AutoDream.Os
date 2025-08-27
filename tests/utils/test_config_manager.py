#!/usr/bin/env python3
"""Unit tests for configuration manager."""

import unittest
from src.utils.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test configuration manager functionality."""

    def setUp(self):
        self.config_manager = ConfigManager("test_config.yaml")

    def test_config_validation(self):
        """Validation reports missing sections."""
        errors = self.config_manager.validate_config()
        self.assertIn("system", errors)
        self.assertIn("agents", errors)

    def test_config_operations(self):
        """Configuration values can be set and retrieved."""
        success = self.config_manager.set_config("test.key", "test_value")
        self.assertTrue(success)
        value = self.config_manager.get_config("test.key")
        self.assertEqual(value, "test_value")
