#!/usr/bin/env python3
"""
Comprehensive Messaging CLI Flags Test Suite - Agent-1 Integration & Core Systems
================================================================================

Comprehensive test coverage for all messaging CLI flags and their functionality.
Tests all command-line interface options, flag combinations, and edge cases.

V2 Compliance: Comprehensive CLI flag testing with modular design and single responsibility.

Author: Agent-1 - Integration & Core Systems Specialist
License: MIT
"""

import pytest

# Import messaging CLI components
    handle_utility_commands,
    handle_contract_commands,
    handle_onboarding_commands,
    handle_message_commands
)


class TestMessagingCLIFlags:
    """Comprehensive test suite for messaging CLI flags."""

    @pytest.fixture
    def temp_inbox_dirs(self):
        """Create temporary inbox directories for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            inbox_dirs = {}
            for i in range(1, 9):  # Create 8 test agents
                agent_dir = get_unified_utility().Path(temp_dir) / f"Agent-{i}" / "inbox"
                agent_dir.mkdir(parents=True)
                inbox_dirs[f"Agent-{i}"] = str(agent_dir)
            yield inbox_dirs

    @pytest.fixture
    def mock_messaging_service(self):
        """Mock messaging service for testing."""
        service = Mock()
        service.send_message_to_inbox = Mock(return_value=True)
        service.send_message_pyautogui = Mock(return_value=True)
        service.bulk_send_messages = Mock(return_value={"Agent-1": True, "Agent-2": True})
        service.get_agent_list = Mock(return_value=["Agent-1", "Agent-2", "Agent-3", "Agent-4"])
        service.get_agent_coordinates = Mock(return_value={"Agent-1": {"x": 100, "y": 200}})
        service.get_delivery_history = Mock(return_value=[])
        service.get_system_health = Mock(return_value={"status": "healthy"})
        service.list_agents = Mock()
        service.send_bulk_onboarding = Mock(return_value=True)
        return service

    @pytest.fixture
    def parser(self):
        """Create argument parser for testing."""
        return create_enhanced_parser()

    # ==================== BASIC MESSAGE FLAGS ====================

    def test_basic_message_flags(self, parser):
        """Test basic message content flags."""
        # Test --message flag
        args = parser.get_unified_utility().parse_args(["--message", "Test message", "--agent", "Agent-1"])
        assert args.message == "Test message"
        assert args.agent == "Agent-1"

        # Test --sender flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--sender", "Agent-2"])
        assert args.sender == "Agent-2"

        # Test default sender
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1"])
        assert args.sender == "Captain Agent-4"

    def test_recipient_selection_flags(self, parser):
        """Test recipient selection flags."""
        # Test --agent flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-7"])
        assert args.agent == "Agent-7"
        assert args.bulk is False

        # Test --bulk flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--bulk"])
        assert args.bulk is True
        assert args.agent is None

        # Test mutual exclusivity validation
        validator = CLIValidator()
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--bulk"])
        is_valid, error = validator.validate_args(args)
        assert is_valid is False
        assert error is not None

    def test_message_properties_flags(self, parser):
        """Test message properties flags."""
        # Test --type flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--type", "broadcast"])
        assert args.type == "broadcast"

        # Test --priority flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--priority", "urgent"])
        assert args.priority == "urgent"

        # Test --high-priority flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--high-priority"])
        assert args.high_priority is True

        # Test --sender-type flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--sender-type", "system"])
        assert args.sender_type == "system"

        # Test --recipient-type flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--recipient-type", "agent"])
        assert args.recipient_type == "agent"

    def test_delivery_mode_flags(self, parser):
        """Test delivery mode flags."""
        # Test --mode flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--mode", "inbox"])
        assert args.mode == "inbox"

        # Test --no-paste flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--no-paste"])
        assert args.no_paste is True

        # Test --new-tab-method flag
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--new-tab-method", "ctrl_n"])
        assert args.new_tab_method == "ctrl_n"

    # ==================== UTILITY FLAGS ====================

    def test_utility_flags(self, parser):
        """Test utility and information flags."""
        # Test --list-agents flag
        args = parser.get_unified_utility().parse_args(["--list-agents"])
        assert args.list_agents is True

        # Test --coordinates flag
        args = parser.get_unified_utility().parse_args(["--coordinates"])
        assert args.coordinates is True

        # Test --history flag
        args = parser.get_unified_utility().parse_args(["--history"])
        assert args.history is True

        # Test --check-status flag
        args = parser.get_unified_utility().parse_args(["--check-status"])
        assert args.get_unified_validator().check_status is True

    def test_queue_management_flags(self, parser):
        """Test queue management flags."""
        # Test --queue-stats flag
        args = parser.get_unified_utility().parse_args(["--queue-stats"])
        assert args.queue_stats is True

        # Test --process-queue flag
        args = parser.get_unified_utility().parse_args(["--process-queue"])
        assert args.process_queue is True

        # Test --start-queue-processor flag
        args = parser.get_unified_utility().parse_args(["--start-queue-processor"])
        assert args.start_queue_processor is True

        # Test --stop-queue-processor flag
        args = parser.get_unified_utility().parse_args(["--stop-queue-processor"])
        assert args.stop_queue_processor is True

    def test_onboarding_flags(self, parser):
        """Test onboarding and training flags."""
        # Test --onboarding flag
        args = parser.get_unified_utility().parse_args(["--onboarding"])
        assert args.onboarding is True

        # Test --onboard flag
        args = parser.get_unified_utility().parse_args(["--onboard", "--agent", "Agent-1"])
        assert args.onboard is True
        assert args.agent == "Agent-1"

        # Test --onboarding-style flag
        args = parser.get_unified_utility().parse_args(["--onboarding", "--onboarding-style", "professional"])
        assert args.onboarding_style == "professional"

        # Test --compliance-mode flag
        args = parser.get_unified_utility().parse_args(["--onboarding", "--compliance-mode"])
        assert args.compliance_mode is True

    def test_contract_flags(self, parser):
        """Test contract and task management flags."""
        # Test --get-next-task flag
        args = parser.get_unified_utility().parse_args(["--get-next-task", "--agent", "Agent-1"])
        assert args.get_next_task is True
        assert args.agent == "Agent-1"

        # Test --wrapup flag
        args = parser.get_unified_utility().parse_args(["--wrapup"])
        assert args.wrapup is True

    # ==================== FLAG COMBINATIONS ====================

    def test_flag_combinations(self, parser):
        """Test various flag combinations."""
        # Test message with all properties
        args = parser.get_unified_utility().parse_args([
            "--message", "Test message",
            "--agent", "Agent-1",
            "--sender", "Agent-2",
            "--type", "agent_to_agent",
            "--priority", "urgent",
            "--mode", "inbox"
        ])
        assert args.message == "Test message"
        assert args.agent == "Agent-1"
        assert args.sender == "Agent-2"
        assert args.type == "agent_to_agent"
        assert args.priority == "urgent"
        assert args.mode == "inbox"

        # Test bulk message with properties
        args = parser.get_unified_utility().parse_args([
            "--message", "Bulk test",
            "--bulk",
            "--type", "broadcast",
            "--priority", "regular"
        ])
        assert args.message == "Bulk test"
        assert args.bulk is True
        assert args.type == "broadcast"
        assert args.priority == "regular"

    def test_invalid_flag_combinations(self, parser):
        """Test invalid flag combinations."""
        validator = CLIValidator()
        
        # Test mutual exclusivity: agent and bulk
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--bulk"])
        is_valid, error = validator.validate_args(args)
        assert is_valid is False
        assert error is not None

        # Test missing required message for send
        args = parser.get_unified_utility().parse_args(["--agent", "Agent-1"])
        is_valid, error = validator.validate_args(args)
        assert is_valid is False
        assert error is not None

    # ==================== CLI HANDLER TESTS ====================

    def test_utility_command_handlers(self, mock_messaging_service):
        """Test utility command handlers."""
        # Test --list-agents handler
        args = argparse.Namespace(list_agents=True, message=None)
        with patch('builtins.print') as mock_print:
            result = handle_utility_commands(args, mock_messaging_service)
            assert result is True
            mock_print.assert_called()

        # Test --coordinates handler
        args = argparse.Namespace(coordinates=True, message=None)
        with patch('builtins.print') as mock_print:
            result = handle_utility_commands(args, mock_messaging_service)
            assert result is True
            mock_print.assert_called()

        # Test --history handler
        args = argparse.Namespace(history=True, message=None)
        with patch('builtins.print') as mock_print:
            result = handle_utility_commands(args, mock_messaging_service)
            assert result is True
            mock_print.assert_called()

        # Test --check-status handler
        args = argparse.Namespace(get_unified_validator().check_status=True, message=None)
        with patch('builtins.print') as mock_print:
            result = handle_utility_commands(args, mock_messaging_service)
            assert result is True
            mock_print.assert_called()

    def test_contract_command_handlers(self):
        """Test contract command handlers."""
        # Test --get-next-task handler
        args = argparse.Namespace(get_next_task=True, agent="Agent-1", message=None)
        with patch('builtins.print') as mock_print:
            result = handle_contract_commands(args)
            assert result is True
            mock_print.assert_called()

        # Test --check-status handler
        args = argparse.Namespace(get_unified_validator().check_status=True, message=None)
        with patch('builtins.print') as mock_print:
            result = handle_contract_commands(args)
            assert result is True
            mock_print.assert_called()

    def test_onboarding_command_handlers(self, mock_messaging_service):
        """Test onboarding command handlers."""
        # Test --onboarding handler
        args = argparse.Namespace(
            onboarding=True,
            bulk=False,
            agent=None,
            message=None,
            onboarding_style="friendly",
            compliance_mode=False,
            mode="inbox",
            new_tab_method="ctrl_t"
        )
        with patch('builtins.print') as mock_print:
            result = handle_onboarding_commands(args, mock_messaging_service)
            assert result is True
            mock_print.assert_called()

        # Test --onboard handler
        args = argparse.Namespace(
            onboard=True,
            agent="Agent-1",
            message=None,
            onboarding_style="professional",
            mode="inbox",
            new_tab_method="ctrl_t"
        )
        with patch('builtins.print') as mock_print:
            result = handle_onboarding_commands(args, mock_messaging_service)
            assert result is True
            mock_print.assert_called()

        # Test --wrapup handler
        args = argparse.Namespace(
            wrapup=True,
            message=None,
            mode="inbox",
            new_tab_method="ctrl_t"
        )
        with patch('builtins.print') as mock_print:
            result = handle_onboarding_commands(args, mock_messaging_service)
            assert result is True
            mock_print.assert_called()

    def test_message_command_handlers(self, mock_messaging_service):
        """Test message command handlers."""
        # Test single agent message
        args = argparse.Namespace(
            message="Test message",
            agent="Agent-1",
            bulk=False,
            sender="Agent-2",
            type="text",
            priority="regular",
            high_priority=False,
            sender_type=None,
            recipient_type=None,
            mode="inbox",
            no_paste=False,
            new_tab_method="ctrl_t"
        )
        with patch('builtins.print') as mock_print:
            result = handle_message_commands(args, mock_messaging_service)
            assert result is True
            mock_messaging_service.send_message_to_inbox.assert_called()

        # Test bulk message
        args = argparse.Namespace(
            message="Bulk test",
            agent=None,
            bulk=True,
            sender="Agent-1",
            type="broadcast",
            priority="urgent",
            high_priority=False,
            sender_type=None,
            recipient_type=None,
            mode="pyautogui"
        )
        with patch('builtins.print') as mock_print:
            result = handle_message_commands(args, mock_messaging_service)
            assert result is True
            mock_messaging_service.bulk_send_messages.assert_called()

    # ==================== INTEGRATION TESTS ====================

    def test_cli_integration_basic_message(self, temp_inbox_dirs):
        """Test CLI integration with basic message sending."""
        # Test single agent message via CLI
        cmd = [
            sys.executable, "-m", "src.services.messaging_cli",
            "--message", "Integration test message",
            "--agent", "Agent-1",
            "--mode", "inbox"
        ]
        
        with patch('src.services.messaging_cli.load_config_with_precedence') as mock_config:
            mock_config.return_value = {"inbox_paths": temp_inbox_dirs}
            result = subprocess.run(cmd, capture_output=True, text=True)
            # Should succeed (exit code 0)
            assert result.returncode == 0

    def test_cli_integration_bulk_message(self, temp_inbox_dirs):
        """Test CLI integration with bulk message sending."""
        # Test bulk message via CLI
        cmd = [
            sys.executable, "-m", "src.services.messaging_cli",
            "--message", "Bulk integration test",
            "--bulk",
            "--mode", "inbox"
        ]
        
        with patch('src.services.messaging_cli.load_config_with_precedence') as mock_config:
            mock_config.return_value = {"inbox_paths": temp_inbox_dirs}
            result = subprocess.run(cmd, capture_output=True, text=True)
            # Should succeed (exit code 0)
            assert result.returncode == 0

    def test_cli_integration_utility_commands(self):
        """Test CLI integration with utility commands."""
        # Test --list-agents command
        cmd = [sys.executable, "-m", "src.services.messaging_cli", "--list-agents"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Should succeed (exit code 0)
        assert result.returncode == 0

        # Test --coordinates command
        cmd = [sys.executable, "-m", "src.services.messaging_cli", "--coordinates"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Should succeed (exit code 0)
        assert result.returncode == 0

    def test_cli_integration_onboarding_commands(self, temp_inbox_dirs):
        """Test CLI integration with onboarding commands."""
        # Test --onboarding command
        cmd = [
            sys.executable, "-m", "src.services.messaging_cli",
            "--onboarding",
            "--mode", "inbox"
        ]
        
        with patch('src.services.messaging_cli.load_config_with_precedence') as mock_config:
            mock_config.return_value = {"inbox_paths": temp_inbox_dirs}
            result = subprocess.run(cmd, capture_output=True, text=True)
            # Should succeed (exit code 0)
            assert result.returncode == 0

    # ==================== ERROR HANDLING TESTS ====================

    def test_error_handling_invalid_agent(self, parser):
        """Test error handling for invalid agent."""
        validator = CLIValidator()
        # Test with invalid agent format
        args = parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "InvalidAgent"])
        is_valid, error = validator.validate_args(args)
        assert is_valid is False
        assert error is not None

    def test_error_handling_missing_message(self, parser):
        """Test error handling for missing message."""
        validator = CLIValidator()
        # Test without message for send operation
        args = parser.get_unified_utility().parse_args(["--agent", "Agent-1"])
        is_valid, error = validator.validate_args(args)
        assert is_valid is False
        assert error is not None

    def test_error_handling_invalid_priority(self, parser):
        """Test error handling for invalid priority."""
        # Test with invalid priority (this should be caught by argparse)
        with pytest.raises(SystemExit):
            parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--priority", "invalid"])

    def test_error_handling_invalid_mode(self, parser):
        """Test error handling for invalid mode."""
        # Test with invalid mode (this should be caught by argparse)
        with pytest.raises(SystemExit):
            parser.get_unified_utility().parse_args(["--message", "Test", "--agent", "Agent-1", "--mode", "invalid"])

    # ==================== V2 COMPLIANCE TESTS ====================

    def test_v2_compliance_modular_design(self):
        """Test V2 compliance: modular design principles."""
        # Test that CLI components are properly modularized
        assert get_unified_validator().validate_hasattr(handle_utility_commands, '__call__')
        assert get_unified_validator().validate_hasattr(handle_contract_commands, '__call__')
        assert get_unified_validator().validate_hasattr(handle_onboarding_commands, '__call__')
        assert get_unified_validator().validate_hasattr(handle_message_commands, '__call__')

    def test_v2_compliance_single_responsibility(self):
        """Test V2 compliance: single responsibility principle."""
        # Test that each handler has a single responsibility
        parser = create_enhanced_parser()
        
        # Utility commands should only handle utility operations
        args = argparse.Namespace(list_agents=True, message=None)
        result = handle_utility_commands(args, Mock())
        assert result is True

        # Contract commands should only handle contract operations
        args = argparse.Namespace(get_next_task=True, agent="Agent-1", message=None)
        result = handle_contract_commands(args)
        assert result is True

    def test_v2_compliance_comprehensive_coverage(self):
        """Test V2 compliance: comprehensive test coverage."""
        # Test that all major flag categories are covered
        parser = create_enhanced_parser()
        
        # Test all flag groups
        flag_groups = [
            # Message content flags
            ["--message", "test", "--agent", "Agent-1"],
            # Recipient selection flags
            ["--message", "test", "--bulk"],
            # Message properties flags
            ["--message", "test", "--agent", "Agent-1", "--type", "broadcast", "--priority", "urgent"],
            # Delivery mode flags
            ["--message", "test", "--agent", "Agent-1", "--mode", "inbox", "--no-paste"],
            # Utility flags
            ["--list-agents"],
            ["--coordinates"],
            ["--history"],
            ["--check-status"],
            # Queue management flags
            ["--queue-stats"],
            ["--process-queue"],
            ["--start-queue-processor"],
            ["--stop-queue-processor"],
            # Onboarding flags
            ["--onboarding"],
            ["--onboard", "--agent", "Agent-1"],
            ["--wrapup"],
            # Contract flags
            ["--get-next-task", "--agent", "Agent-1"]
        ]
        
        for flags in flag_groups:
            args = parser.get_unified_utility().parse_args(flags)
            assert args is not None

    def test_v2_compliance_error_handling(self):
        """Test V2 compliance: comprehensive error handling."""
        parser = create_enhanced_parser()
        validator = CLIValidator()
        
        # Test various error scenarios
        error_scenarios = [
            # Missing required message
            ["--agent", "Agent-1"],
            # Invalid flag combination
            ["--message", "test", "--agent", "Agent-1", "--bulk"],
        ]
        
        for flags in error_scenarios:
            args = parser.get_unified_utility().parse_args(flags)
            is_valid, error = validator.validate_args(args)
            assert is_valid is False
            assert error is not None
        
        # Test argparse-level errors (invalid enum values)
        argget_unified_utility().parse_error_scenarios = [
            ["--message", "test", "--agent", "Agent-1", "--priority", "invalid"],
            ["--message", "test", "--agent", "Agent-1", "--mode", "invalid"],
            ["--message", "test", "--agent", "Agent-1", "--type", "invalid"]
        ]
        
        for flags in argget_unified_utility().parse_error_scenarios:
            with pytest.raises(SystemExit):
                parser.get_unified_utility().parse_args(flags)


def run_cli_flags_tests():
    """Run all messaging CLI flags tests."""
    get_logger(__name__).info("🧪 MESSAGING CLI FLAGS COMPREHENSIVE TEST SUITE - AGENT-1")
    get_logger(__name__).info("=" * 70)
    
    # Run pytest with verbose output
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])


if __name__ == "__main__":
    run_cli_flags_tests()
