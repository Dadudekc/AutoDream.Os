#!/usr/bin/env python3
"""
Smoke Tests for Messaging CLI - Agent Cellphone V2
=================================================

Comprehensive smoke tests for messaging CLI commands and functionality.
Tests command parsing, argument validation, and core CLI operations.

Author: Agent-2 (Architecture & Design)
License: MIT
"""

import pytest
import argparse
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys
import json
from pathlib import Path
import tempfile

# Import CLI components
from src.services.messaging_cli import create_enhanced_parser, main
import src.services.messaging_cli_handlers as handlers


class TestMessagingCLISmoke:
    """Smoke tests for messaging CLI functionality."""

    @pytest.fixture
    def temp_workspace_dir(self):
        """Create temporary workspace directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create agent workspaces
            for agent_id in ["Agent-1", "Agent-2", "Agent-4"]:
                agent_dir = Path(temp_dir) / "agent_workspaces" / agent_id
                agent_dir.mkdir(parents=True, exist_ok=True)

                # Create inbox directory
                inbox_dir = agent_dir / "inbox"
                inbox_dir.mkdir(exist_ok=True)

                # Create status.json
                status_file = agent_dir / "status.json"
                status_data = {
                    "agent_id": agent_id,
                    "agent_name": f"Test {agent_id}",
                    "status": "ACTIVE_AGENT_MODE",
                    "current_phase": "TASK_EXECUTION",
                    "last_updated": "2025-01-27 12:00:00",
                    "current_mission": "Testing messaging CLI",
                    "mission_priority": "HIGH"
                }
                with open(status_file, 'w') as f:
                    json.dump(status_data, f)

            yield temp_dir

    def test_parser_creation(self):
        """Test that the enhanced parser is created correctly."""
        parser = create_enhanced_parser()

        # Verify parser is created
        assert isinstance(parser, argparse.ArgumentParser)

        # Test basic message arguments
        args = parser.parse_args(["--message", "test message", "--agent", "Agent-1"])
        assert args.message == "test message"
        assert args.agent == "Agent-1"
        assert args.sender == "Captain Agent-4"  # default value

    def test_parser_message_flags(self):
        """Test message-related command line flags."""
        parser = create_enhanced_parser()

        # Test message with all flags
        args = parser.parse_args([
            "--message", "Hello world",
            "--agent", "Agent-2",
            "--sender", "Agent-4",
            "--type", "text",
            "--priority", "urgent",
            "--high-priority"
        ])

        assert args.message == "Hello world"
        assert args.agent == "Agent-2"
        assert args.sender == "Agent-4"
        assert args.type == "text"
        assert args.priority == "urgent"
        assert args.high_priority is True

    def test_parser_bulk_flags(self):
        """Test bulk messaging flags."""
        parser = create_enhanced_parser()

        # Test bulk messaging
        args = parser.parse_args([
            "--bulk",
            "--message", "System announcement",
            "--type", "broadcast"
        ])

        assert args.bulk is True
        assert args.message == "System announcement"
        assert args.type == "broadcast"
        assert args.agent is None  # bulk and agent are mutually exclusive

    def test_parser_utility_commands(self):
        """Test utility command flags."""
        parser = create_enhanced_parser()

        # Test various utility commands
        commands = [
            ["--list-agents"],
            ["--coordinates"],
            ["--check-status"],
            ["--history"]
        ]

        for cmd in commands:
            args = parser.parse_args(cmd)
            flag_name = cmd[0].replace("--", "").replace("-", "_")
            assert getattr(args, flag_name) is True

    def test_parser_onboarding_commands(self):
        """Test onboarding-related command flags."""
        parser = create_enhanced_parser()

        # Test onboarding commands
        args = parser.parse_args([
            "--onboarding",
            "--onboarding-style", "professional"
        ])

        assert args.onboarding is True
        assert args.onboarding_style == "professional"

        # Test single agent onboarding
        args = parser.parse_args([
            "--onboard",
            "--agent", "Agent-1"
        ])

        assert args.onboard is True
        assert args.agent == "Agent-1"

    def test_parser_contract_commands(self):
        """Test contract-related command flags."""
        parser = create_enhanced_parser()

        # Test contract commands
        args = parser.parse_args([
            "--get-next-task",
            "--agent", "Agent-2"
        ])

        assert args.get_next_task is True
        assert args.agent == "Agent-2"

    def test_parser_delivery_options(self):
        """Test delivery mode and options."""
        parser = create_enhanced_parser()

        # Test PyAutoGUI mode
        args = parser.parse_args([
            "--mode", "pyautogui",
            "--new-tab-method", "ctrl_t",
            "--no-paste"
        ])

        assert args.mode == "pyautogui"
        assert args.new_tab_method == "ctrl_t"
        assert args.no_paste is True

        # Test inbox mode
        args = parser.parse_args([
            "--mode", "inbox",
            "--message", "Test inbox message",
            "--agent", "Agent-1"
        ])

        assert args.mode == "inbox"
        assert args.message == "Test inbox message"
        assert args.agent == "Agent-1"

    @patch('src.services.messaging_cli_handlers.handle_utility_commands')
    def test_main_utility_commands(self, mock_utility_handler):
        """Test main function with utility commands."""
        mock_utility_handler.return_value = True  # Command handled

        with patch('sys.argv', ['messaging_cli', '--list-agents']):
            # This should call utility handler and return
            with patch('src.services.messaging_cli.create_enhanced_parser') as mock_parser:
                mock_args = Mock()
                mock_args.list_agents = True
                mock_args.check_status = False
                mock_args.coordinates = False
                mock_args.history = False
                mock_parser.return_value.parse_args.return_value = mock_args

                main()

                # Verify utility handler was called
                mock_utility_handler.assert_called_once()

    @patch('src.services.messaging_cli_handlers.handle_contract_commands')
    def test_main_contract_commands(self, mock_contract_handler):
        """Test main function with contract commands."""
        mock_contract_handler.return_value = True

        with patch('sys.argv', ['messaging_cli', '--get-next-task', '--agent', 'Agent-1']):
            with patch('src.services.messaging_cli.create_enhanced_parser') as mock_parser:
                mock_args = Mock()
                mock_args.get_next_task = True
                mock_args.agent = "Agent-1"
                mock_parser.return_value.parse_args.return_value = mock_args

                # Mock other handlers to return False
                with patch('src.services.messaging_cli_handlers.handle_utility_commands', return_value=False):
                    with patch('src.services.messaging_cli_handlers.handle_onboarding_commands', return_value=False):
                        with patch('src.services.messaging_cli_handlers.handle_message_commands', return_value=False):
                            with patch('src.services.messaging_cli_handlers.handle_overnight_commands', return_value=False):
                                main()

                                mock_contract_handler.assert_called_once()

    @patch('src.services.messaging_cli_handlers.handle_onboarding_commands')
    def test_main_onboarding_commands(self, mock_onboarding_handler):
        """Test main function with onboarding commands."""
        mock_onboarding_handler.return_value = True

        with patch('sys.argv', ['messaging_cli', '--onboarding']):
            with patch('src.services.messaging_cli.create_enhanced_parser') as mock_parser:
                mock_args = Mock()
                mock_args.onboarding = True
                mock_parser.return_value.parse_args.return_value = mock_args

                # Mock other handlers
                with patch('src.services.messaging_cli_handlers.handle_utility_commands', return_value=False):
                    with patch('src.services.messaging_cli_handlers.handle_contract_commands', return_value=False):
                        with patch('src.services.messaging_cli_handlers.handle_message_commands', return_value=False):
                            with patch('src.services.messaging_cli_handlers.handle_overnight_commands', return_value=False):
                                main()

                                mock_onboarding_handler.assert_called_once()

    def test_parser_validation_mutual_exclusion(self):
        """Test parser validation for mutually exclusive options."""
        parser = create_enhanced_parser()

        # Test that bulk and agent work together (they should be allowed)
        args = parser.parse_args([
            "--bulk",
            "--agent", "Agent-1",
            "--message", "Test message"
        ])

        # The parser allows both, but logic should handle appropriately
        assert args.bulk is True
        assert args.agent == "Agent-1"

    def test_parser_default_values(self):
        """Test default values in parser."""
        parser = create_enhanced_parser()

        args = parser.parse_args([])  # No arguments

        # Check default values
        assert args.sender == "Captain Agent-4"
        assert args.mode == "pyautogui"
        assert args.type == "text"
        assert args.priority == "regular"
        assert args.onboarding_style == "friendly"
        assert args.new_tab_method == "ctrl_t"
        assert args.high_priority is False
        assert args.bulk is False

    def test_parser_required_arguments(self):
        """Test parser behavior with required arguments."""
        parser = create_enhanced_parser()

        # Test that message is not required for utility commands
        args = parser.parse_args(["--list-agents"])
        assert args.list_agents is True
        assert args.message is None

        # Test message with agent
        args = parser.parse_args([
            "--message", "Hello",
            "--agent", "Agent-1"
        ])
        assert args.message == "Hello"
        assert args.agent == "Agent-1"

    @patch('sys.stdout', new_callable=StringIO)
    def test_parser_help_output(self, mock_stdout):
        """Test parser help output."""
        parser = create_enhanced_parser()

        # Test help output
        with pytest.raises(SystemExit):  # --help causes SystemExit
            parser.parse_args(["--help"])

    def test_parser_error_handling(self):
        """Test parser error handling."""
        parser = create_enhanced_parser()

        # Test invalid mode
        with pytest.raises(SystemExit):  # Argument parsing error
            parser.parse_args(["--mode", "invalid_mode"])

    def test_parser_advanced_flags(self):
        """Test advanced command line flags."""
        parser = create_enhanced_parser()

        # Test coordinate management flags
        args = parser.parse_args([
            "--set-onboarding-coords",
            "Agent-1,100,200"
        ])
        assert args.set_onboarding_coords == "Agent-1,100,200"

        # Test capture flags
        args = parser.parse_args([
            "--capture-coords",
            "--capture-agent", "Agent-2"
        ])
        assert args.capture_coords is True
        assert args.capture_agent == "Agent-2"

    def test_parser_dry_run_mode(self):
        """Test dry run mode flag."""
        parser = create_enhanced_parser()

        args = parser.parse_args([
            "--dry-run",
            "--message", "Test message",
            "--agent", "Agent-1"
        ])

        assert args.dry_run is True
        assert args.message == "Test message"
        assert args.agent == "Agent-1"

    def test_parser_overnight_mode(self):
        """Test overnight autonomous mode."""
        parser = create_enhanced_parser()

        args = parser.parse_args([
            "--overnight"
        ])

        assert args.overnight is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
