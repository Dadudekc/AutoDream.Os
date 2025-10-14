"""
CLI Toolbelt Tests - Comprehensive Test Suite
==============================================

Tests for CLI Toolbelt unified tool launcher.

Author: Agent-1 - Code Integration & Testing Specialist
Date: 2025-10-11
License: MIT
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools import toolbelt
from tools.toolbelt_help import HelpGenerator
from tools.toolbelt_registry import TOOLS_REGISTRY, ToolRegistry
from tools.toolbelt_runner import ToolRunner


class TestToolRegistry:
    """Tests for ToolRegistry class."""

    def test_registry_initialization(self):
        """Test registry initializes correctly."""
        registry = ToolRegistry()
        assert registry.tools == TOOLS_REGISTRY
        assert len(registry.tools) == 9

    def test_get_tool_by_primary_flag(self):
        """Test getting tool by primary flag."""
        registry = ToolRegistry()
        tool = registry.get_tool_for_flag("--scan")
        assert tool is not None
        assert tool["name"] == "Project Scanner"

    def test_get_tool_by_alias(self):
        """Test getting tool by alias flag."""
        registry = ToolRegistry()
        tool = registry.get_tool_for_flag("-s")
        assert tool is not None
        assert tool["name"] == "Project Scanner"

    def test_get_tool_for_unknown_flag(self):
        """Test getting tool with unknown flag returns None."""
        registry = ToolRegistry()
        tool = registry.get_tool_for_flag("--unknown")
        assert tool is None

    def test_get_tool_by_name(self):
        """Test getting tool by tool ID."""
        registry = ToolRegistry()
        tool = registry.get_tool_by_name("scan")
        assert tool is not None
        assert tool["name"] == "Project Scanner"

    def test_list_tools(self):
        """Test listing all tools."""
        registry = ToolRegistry()
        tools = registry.list_tools()
        assert len(tools) == 9
        assert all("id" in tool for tool in tools)

    def test_get_all_flags(self):
        """Test getting all registered flags."""
        registry = ToolRegistry()
        flags = registry.get_all_flags()
        assert "--scan" in flags
        assert "-s" in flags
        assert len(flags) > 9  # Should have primary + aliases


class TestToolRunner:
    """Tests for ToolRunner class."""

    def test_runner_initialization(self):
        """Test runner initializes correctly."""
        runner = ToolRunner()
        assert runner is not None

    @patch("importlib.import_module")
    def test_execute_tool_success(self, mock_import):
        """Test successful tool execution."""
        # Mock tool module
        mock_module = MagicMock()
        mock_module.main = MagicMock(return_value=0)
        mock_import.return_value = mock_module

        runner = ToolRunner()
        tool_config = {
            "name": "Test Tool",
            "module": "test.module",
            "main_function": "main",
            "args_passthrough": False,
        }

        exit_code = runner.execute_tool(tool_config, [])
        assert exit_code == 0
        mock_module.main.assert_called_once()

    @patch("importlib.import_module")
    def test_execute_tool_with_args_passthrough(self, mock_import):
        """Test tool execution with argument passthrough."""
        # Mock tool module
        mock_module = MagicMock()
        mock_module.main = MagicMock(return_value=0)
        mock_import.return_value = mock_module

        runner = ToolRunner()
        tool_config = {
            "name": "Test Tool",
            "module": "test.module",
            "main_function": "main",
            "args_passthrough": True,
        }

        test_args = ["--option", "value"]
        exit_code = runner.execute_tool(tool_config, test_args)
        assert exit_code == 0

    @patch("importlib.import_module")
    def test_execute_tool_import_error(self, mock_import):
        """Test tool execution with import error."""
        mock_import.side_effect = ImportError("Module not found")

        runner = ToolRunner()
        tool_config = {
            "name": "Test Tool",
            "module": "nonexistent.module",
            "main_function": "main",
            "args_passthrough": False,
        }

        exit_code = runner.execute_tool(tool_config, [])
        assert exit_code == 1


class TestHelpGenerator:
    """Tests for HelpGenerator class."""

    def test_help_generator_initialization(self):
        """Test help generator initializes correctly."""
        registry = ToolRegistry()
        help_gen = HelpGenerator(registry)
        assert help_gen.registry == registry

    def test_generate_help_contains_header(self):
        """Test help contains header."""
        registry = ToolRegistry()
        help_gen = HelpGenerator(registry)
        help_text = help_gen.generate_help()
        assert "CLI Toolbelt" in help_text
        assert "Usage:" in help_text

    def test_generate_help_contains_all_tools(self):
        """Test help contains all tools."""
        registry = ToolRegistry()
        help_gen = HelpGenerator(registry)
        help_text = help_gen.generate_help()

        assert "Project Scanner" in help_text
        assert "--scan" in help_text
        assert "V2 Compliance Checker" in help_text
        assert "--v2-check" in help_text

    def test_generate_help_contains_examples(self):
        """Test help contains usage examples."""
        registry = ToolRegistry()
        help_gen = HelpGenerator(registry)
        help_text = help_gen.generate_help()

        assert "Examples:" in help_text
        assert "python -m tools.toolbelt" in help_text

    def test_show_tool_help(self):
        """Test tool-specific help generation."""
        registry = ToolRegistry()
        help_gen = HelpGenerator(registry)
        tool_config = registry.get_tool_by_name("scan")

        help_text = help_gen.show_tool_help(tool_config)
        assert "Project Scanner" in help_text
        assert "--scan" in help_text


class TestToolbeltMain:
    """Tests for main toolbelt entry point."""

    def test_main_help_flag(self):
        """Test --help flag shows help."""
        with patch.object(sys, "argv", ["toolbelt", "--help"]):
            exit_code = toolbelt.main()
            assert exit_code == 0

    def test_main_version_flag(self):
        """Test --version flag shows version."""
        with patch.object(sys, "argv", ["toolbelt", "--version"]):
            exit_code = toolbelt.main()
            assert exit_code == 0

    def test_main_list_flag(self):
        """Test --list flag lists tools."""
        with patch.object(sys, "argv", ["toolbelt", "--list"]):
            exit_code = toolbelt.main()
            assert exit_code == 0

    def test_main_no_args_shows_help(self):
        """Test no arguments shows help."""
        with patch.object(sys, "argv", ["toolbelt"]):
            exit_code = toolbelt.main()
            assert exit_code == 0


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
