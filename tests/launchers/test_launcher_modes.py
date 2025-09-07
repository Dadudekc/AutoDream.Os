#!/usr/bin/env python3
"""Unit tests for launcher modes functionality."""

import unittest
from src.launchers.launcher_modes import LauncherModes


class TestLauncherModes(unittest.TestCase):
    """Test launcher modes functionality."""

    def setUp(self):
        self.modes = LauncherModes()

    def test_available_modes(self):
        """Expected modes are reported."""
        modes = self.modes.get_available_modes()
        expected_modes = ["onboarding", "coordination", "autonomous", "cleanup"]
        for mode in expected_modes:
            self.assertIn(mode, modes)

    def test_mode_execution_simulation(self):
        """Running each mode returns a boolean."""
        test_agents = {}
        for mode in self.modes.get_available_modes():
            result = self.modes.run_mode(mode, test_agents)
            self.assertIsInstance(result, bool)
