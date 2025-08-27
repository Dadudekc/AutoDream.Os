#!/usr/bin/env python3
"""Unit tests for launcher core functionality."""

import unittest
from src.launchers.launcher_core import LauncherCore


class TestLauncherCore(unittest.TestCase):
    """Test launcher core functionality."""

    def setUp(self):
        self.core = LauncherCore()

    def test_initialization(self):
        """Launcher core initializes correctly."""
        self.assertIsNotNone(self.core)
        self.assertFalse(self.core.system_ready)

    def test_system_check_simulation(self):
        """System check returns a boolean."""
        result = self.core.check_system()
        self.assertIsInstance(result, bool)

    def test_agent_management(self):
        """Agent status retrieval and shutdown behave as expected."""
        status = self.core.get_agent_status()
        self.assertEqual(status, {})
        result = self.core.shutdown_agents()
        self.assertTrue(result)
