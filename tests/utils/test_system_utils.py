#!/usr/bin/env python3
"""Unit tests for system utilities."""

import unittest
from src.utils.system_utils import SystemUtils


class TestSystemUtils(unittest.TestCase):
    """Test system utilities functionality."""

    def setUp(self):
        self.system_utils = SystemUtils()

    def test_system_info(self):
        """System information includes expected fields."""
        info = self.system_utils.get_system_info()
        self.assertIn("platform", info)
        self.assertIn("python_version", info)
        self.assertIn("current_working_directory", info)

    def test_dependencies_check(self):
        """Dependency check reports built-in modules as available."""
        deps = self.system_utils.check_dependencies()
        self.assertTrue(deps["pathlib"])
        self.assertTrue(deps["logging"])
        self.assertTrue(deps["json"])
        self.assertTrue(deps["re"])

    def test_logging_setup(self):
        """Logging setup succeeds with a valid level."""
        result = self.system_utils.setup_logging("INFO")
        self.assertTrue(result)
