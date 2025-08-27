#!/usr/bin/env python3
"""Unit tests for launcher CLI functionality."""

import unittest
from src.launchers.launcher_cli import LauncherCLI


class TestLauncherCLI(unittest.TestCase):
    """Test launcher CLI functionality."""

    def setUp(self):
        self.cli = LauncherCLI()

    def test_cli_initialization(self):
        """CLI initializes with a parser."""
        self.assertIsNotNone(self.cli)
        self.assertIsNotNone(self.cli.parser)

    def test_help_output(self):
        """Help text includes expected options."""
        help_text = self.cli.parser.format_help()
        self.assertIn("Unified Launcher for Agent Cellphone System", help_text)
        self.assertIn("--check", help_text)
        self.assertIn("--init", help_text)
