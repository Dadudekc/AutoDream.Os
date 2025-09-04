#!/usr/bin/env python3
"""
Comprehensive CLI Integration Tests - Agent Cellphone V2
========================================================

Integration tests for CLI functionality, end-to-end scenarios, and edge cases.
Tests the complete CLI workflow from argument parsing to command execution.

Run with: python -m pytest tests/messaging/test_messaging_cli_integration.py -v
"""

import pytest

# Add src to path for imports
sys.path.insert(0, str(get_unified_utility().Path(__file__).parent.parent.parent / "src"))

try:
        handle_utility_commands,
        handle_contract_commands,
        handle_onboarding_commands,
        handle_message_commands
    )
    IMPORTS_AVAILABLE = True
except ImportError:
    # Define mock classes for testing when imports fail
    class MockCLIValidator:
        def validate_args(self, args):
            return True, None

    class MockParser:
        def get_unified_utility().parse_args(self, args=None):
            return MagicMock()

        def format_help(self):
            return "Mock help text"

    CLIValidator = MockCLIValidator
    def create_enhanced_parser():
        return MockParser()

    def handle_utility_commands(args, service):
        return True

    def handle_contract_commands(args):
        return True

    def handle_onboarding_commands(args, service):
        return True

    def handle_message_commands(args, service):
        return True

    UnifiedMessagingCore = MagicMock
    IMPORTS_AVAILABLE = False


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required modules not available")
class TestCLIIntegrationEndToEnd:
    """End-to-end integration tests for CLI functionality."""

    def setup_method(self):
        """Setup for each test."""
        self.parser = create_enhanced_parser()
        self.validator = CLIValidator()

    @patch('services.messaging_core.UnifiedMessagingCore')
    def test_send_to_specific_agent_workflow(self, mock_core):
        """Test complete workflow for sending message to specific agent."""
        mock_instance = MagicMock()
        mock_core.return_value = mock_instance

        # Parse arguments
        args = self.parser.get_unified_utility().parse_args([
            "--agent", "Agent-7",
            "--message", "Test message",
            "--type", "broadcast",
            "--priority", "urgent"
        ])

        # Validate arguments
        is_valid, error = self.validator.validate_args(args)
        assert is_valid
        assert error is None

        # Execute message command
        with patch('services.messaging_cli_handlers.ContractService'):
            result = handle_message_commands(args, mock_instance)
            assert result is True

        # Verify core was called correctly
        mock_instance.send_message.assert_called_once()

    @patch('services.messaging_core.UnifiedMessagingCore')
    def test_bulk_message_workflow(self, mock_core):
        """Test complete workflow for bulk message sending."""
        mock_instance = MagicMock()
        mock_core.return_value = mock_instance

        # Parse arguments
        args = self.parser.get_unified_utility().parse_args([
            "--bulk",
            "--message", "System maintenance notification",
            "--sender", "Captain Agent-4",
            "--type", "broadcast"
        ])

        # Validate arguments
        is_valid, error = self.validator.validate_args(args)
        assert is_valid
        assert error is None

        # Execute message command
        with patch('services.messaging_cli_handlers.ContractService'):
            result = handle_message_commands(args, mock_instance)
            assert result is True

        # Verify core was called correctly
        mock_instance.send_bulk_message.assert_called_once()

    @patch('services.messaging_core.UnifiedMessagingCore')
    def test_utility_command_workflow(self, mock_core):
        """Test utility command execution workflow."""
        mock_instance = MagicMock()
        mock_core.return_value = mock_instance

        # Test list agents
        args = self.parser.get_unified_utility().parse_args(["--list-agents"])
        result = handle_utility_commands(args, mock_instance)
        assert result is True
        mock_instance.list_agents.assert_called_once()

        # Test coordinates
        mock_instance.reset_mock()
        args = self.parser.get_unified_utility().parse_args(["--coordinates"])
        result = handle_utility_commands(args, mock_instance)
        assert result is True
        mock_instance.show_coordinates.assert_called_once()

        # Test history
        mock_instance.reset_mock()
        args = self.parser.get_unified_utility().parse_args(["--history"])
        result = handle_utility_commands(args, mock_instance)
        assert result is True
        mock_instance.show_message_history.assert_called_once()

    @patch('services.messaging_core.UnifiedMessagingCore')
    def test_queue_management_workflow(self, mock_core):
        """Test queue management command workflow."""
        mock_instance = MagicMock()
        mock_core.return_value = mock_instance

        # Test queue stats
        args = self.parser.get_unified_utility().parse_args(["--queue-stats"])
        with patch('services.messaging_cli_handlers.handle_queue_stats') as mock_handler:
            mock_handler.return_value = True
            result = handle_utility_commands(args, mock_instance)
            assert result is True
            mock_handler.assert_called_once_with(mock_instance)

    @patch('services.messaging_core.UnifiedMessagingCore')
    def test_contract_command_workflow(self, mock_core):
        """Test contract command execution workflow."""
        mock_instance = MagicMock()
        mock_core.return_value = mock_instance

        # Test get next task
        args = self.parser.get_unified_utility().parse_args(["--get-next-task", "--agent", "Agent-7"])
        with patch('services.messaging_cli_handlers.ContractService') as mock_contract:
            mock_contract_instance = MagicMock()
            mock_contract.return_value = mock_contract_instance
            mock_contract_instance.get_next_task.return_value = "Task data"

            result = handle_contract_commands(args)
            assert result is True
            mock_contract.assert_called_once()
            mock_contract_instance.get_next_task.assert_called_once_with("Agent-7")

    @patch('services.messaging_core.UnifiedMessagingCore')
    def test_onboarding_workflow(self, mock_core):
        """Test onboarding command execution workflow."""
        mock_instance = MagicMock()
        mock_core.return_value = mock_instance

        # Test bulk onboarding
        args = self.parser.get_unified_utility().parse_args(["--onboarding", "--onboarding-style", "professional"])
        with patch('services.messaging_cli_handlers.ContractService'):
            result = handle_onboarding_commands(args, mock_instance)
            assert result is True
            mock_instance.send_bulk_onboarding.assert_called_once_with("professional")

        # Test single agent onboarding
        mock_instance.reset_mock()
        args = self.parser.get_unified_utility().parse_args(["--onboard", "--agent", "Agent-7", "--onboarding-style", "friendly"])
        with patch('services.messaging_cli_handlers.ContractService'):
            result = handle_onboarding_commands(args, mock_instance)
            assert result is True
            mock_instance.send_single_onboarding.assert_called_once_with("Agent-7", "friendly")


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases."""

    def setup_method(self):
        """Setup for each test."""
        try:
            self.parser = create_enhanced_parser()
            self.validator = CLIValidator()
            self.imports_available = True
        except (ImportError, AttributeError):
            self.imports_available = False

    def _skip_if_imports_unavailable(self):
        """Skip test if imports are not available."""
        if not self.imports_available:
            pytest.skip("Required modules not available for testing")

    def test_invalid_flag_combination_error_handling(self):
        """Test error handling for invalid flag combinations."""
        self._skip_if_imports_unavailable()

        # Test mutually exclusive flags
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--agent", "Agent-7", "--bulk", "--message", "Test"])

    def test_missing_required_dependency_error_handling(self):
        """Test error handling for missing required dependencies."""
        self._skip_if_imports_unavailable()

        # Test get-next-task without agent
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--get-next-task"])

        # Test onboard without agent
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--onboard"])

    def test_mode_gating_error_handling(self):
        """Test error handling for mode gating violations."""
        self._skip_if_imports_unavailable()

        # Test no-paste with inbox mode
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--mode", "inbox", "--no-paste", "--message", "Test"])

        # Test new-tab-method with inbox mode
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--mode", "inbox", "--new-tab-method", "ctrl_t", "--message", "Test"])

    def test_invalid_enum_values_error_handling(self):
        """Test error handling for invalid enum values."""
        self._skip_if_imports_unavailable()

        # Test invalid message type
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--type", "invalid_type", "--message", "Test"])

        # Test invalid priority
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--priority", "invalid_priority", "--message", "Test"])

        # Test invalid mode
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--mode", "invalid_mode", "--message", "Test"])

    def test_message_requirement_error_handling(self):
        """Test error handling for missing message requirement."""
        self._skip_if_imports_unavailable()

        # Test agent message without content
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--agent", "Agent-7"])

        # Test bulk message without content
        with pytest.raises(SystemExit):
            self.parser.get_unified_utility().parse_args(["--bulk"])


class TestCLIValidationScenarios:
    """Test various CLI validation scenarios."""

    def setup_method(self):
        """Setup for each test."""
        try:
            self.parser = create_enhanced_parser()
            self.validator = CLIValidator()
            self.imports_available = True
        except (ImportError, AttributeError):
            self.imports_available = False

    def _skip_if_imports_unavailable(self):
        """Skip test if imports are not available."""
        if not self.imports_available:
            pytest.skip("Required modules not available for testing")

    def test_complex_valid_flag_combinations(self):
        """Test complex but valid flag combinations."""
        self._skip_if_imports_unavailable()

        valid_combinations = [
            # Full featured agent message
            ["--agent", "Agent-7", "--message", "Complex message",
             "--sender", "Agent-1", "--type", "broadcast", "--priority", "urgent",
             "--mode", "pyautogui", "--no-paste", "--new-tab-method", "ctrl_n"],

            # Full featured bulk message
            ["--bulk", "--message", "Bulk notification", "--type", "system_to_agent",
             "--sender", "System", "--priority", "regular", "--mode", "inbox"],

            # Onboarding with compliance mode
            ["--onboarding", "--onboarding-style", "professional", "--compliance-mode"],

            # Contract task with specific agent
            ["--get-next-task", "--agent", "Agent-7"],
        ]

        for combination in valid_combinations:
            args = self.parser.get_unified_utility().parse_args(combination)
            assert args is not None, f"Failed to parse valid combination: {combination}"

            # Validate the parsed arguments
            is_valid, error = self.validator.validate_args(args)
            assert is_valid, f"Valid combination failed validation: {combination}, error: {error}"

    def test_edge_case_flag_values(self):
        """Test edge cases for flag values."""
        self._skip_if_imports_unavailable()

        # Test with special characters in message
        args = self.parser.get_unified_utility().parse_args([
            "--message", "Message with special chars: !@#$%^&*()",
            "--agent", "Agent-7"
        ])
        assert args.message == "Message with special chars: !@#$%^&*()"
        assert args.agent == "Agent-7"

        # Test with long message
        long_message = "A" * 1000
        args = self.parser.get_unified_utility().parse_args(["--message", long_message, "--bulk"])
        assert args.message == long_message
        assert args.bulk is True

        # Test with unicode characters
        unicode_message = "🚀 Agent Cellphone V2 - Test Message 📨"
        args = self.parser.get_unified_utility().parse_args(["--message", unicode_message, "--agent", "Agent-1"])
        assert args.message == unicode_message

    def test_default_value_behavior(self):
        """Test that default values are applied correctly."""
        self._skip_if_imports_unavailable()

        # Test defaults for basic message
        args = self.parser.get_unified_utility().parse_args(["--agent", "Agent-7", "--message", "Test"])
        assert args.sender == "Captain Agent-4"
        assert args.type == "text"
        assert args.priority == "regular"
        assert args.mode == "pyautogui"
        assert args.new_tab_method == "ctrl_t"
        assert args.onboarding_style == "friendly"

        # Test defaults for bulk message
        args = self.parser.get_unified_utility().parse_args(["--bulk", "--message", "Test"])
        assert args.sender == "Captain Agent-4"
        assert args.type == "text"
        assert args.priority == "regular"

    def test_boolean_flag_behavior(self):
        """Test boolean flag behavior."""
        self._skip_if_imports_unavailable()

        # Test single boolean flag
        args = self.parser.get_unified_utility().parse_args(["--list-agents"])
        assert args.list_agents is True
        assert args.coordinates is False
        assert args.history is False

        # Test multiple boolean flags (should work since they're not mutually exclusive)
        args = self.parser.get_unified_utility().parse_args(["--coordinates", "--history"])
        assert args.coordinates is True
        assert args.history is True
        assert args.list_agents is False


class TestCLIPerformanceScenarios:
    """Test CLI performance and stress scenarios."""

    def setup_method(self):
        """Setup for each test."""
        try:
            self.parser = create_enhanced_parser()
            self.validator = CLIValidator()
            self.imports_available = True
        except (ImportError, AttributeError):
            self.imports_available = False

    def _skip_if_imports_unavailable(self):
        """Skip test if imports are not available."""
        if not self.imports_available:
            pytest.skip("Required modules not available for testing")

    def test_multiple_flag_parsing_performance(self):
        """Test parsing performance with many flags."""
        self._skip_if_imports_unavailable()

        # Test with maximum number of flags
        args = self.parser.get_unified_utility().parse_args([
            "--agent", "Agent-7",
            "--message", "Performance test message",
            "--sender", "Test-Sender",
            "--type", "broadcast",
            "--priority", "urgent",
            "--mode", "pyautogui",
            "--no-paste",
            "--new-tab-method", "ctrl_t"
        ])

        assert args.agent == "Agent-7"
        assert args.message == "Performance test message"
        assert args.sender == "Test-Sender"
        assert args.type == "broadcast"
        assert args.priority == "urgent"
        assert args.no_paste is True

    def test_validation_performance_with_complex_args(self):
        """Test validation performance with complex argument sets."""
        self._skip_if_imports_unavailable()

        # Create complex argument set
        args = self.parser.get_unified_utility().parse_args([
            "--agent", "Agent-7",
            "--message", "Complex validation test",
            "--type", "agent_to_agent",
            "--priority", "urgent",
            "--mode", "pyautogui",
            "--no-paste"
        ])

        # Validate multiple times to test performance
        for _ in range(10):
            is_valid, error = self.validator.validate_args(args)
            assert is_valid
            assert error is None


class TestCLIHelpAndDocumentation:
    """Test CLI help text and documentation."""

    def setup_method(self):
        """Setup for each test."""
        try:
            self.parser = create_enhanced_parser()
            self.imports_available = True
        except (ImportError, AttributeError):
            self.imports_available = False

    def _skip_if_imports_unavailable(self):
        """Skip test if imports are not available."""
        if not self.imports_available:
            pytest.skip("Required modules not available for testing")

    def test_help_text_completeness(self):
        """Test that help text contains all expected sections and information."""
        self._skip_if_imports_unavailable()

        help_text = self.parser.format_help()

        # Check for main sections
        assert "🚀 Agent Cellphone V2 - Unified Messaging System" in help_text
        assert "📝 Message Content" in help_text
        assert "👥 Recipient Selection" in help_text
        assert "⚙️ Message Properties" in help_text
        assert "📨 Delivery Mode" in help_text
        assert "🔍 Utility & Information" in help_text
        assert "📊 Queue Management" in help_text
        assert "🎓 Onboarding & Training" in help_text
        assert "📋 Contract & Task Management" in help_text

        # Check for examples
        assert "EXAMPLES:" in help_text
        assert "EXIT CODES:" in help_text

        # Check for key flags
        assert "--message" in help_text
        assert "--agent" in help_text
        assert "--bulk" in help_text
        assert "--list-agents" in help_text
        assert "--onboarding" in help_text

    def test_help_text_examples(self):
        """Test that help text contains useful examples."""
        self._skip_if_imports_unavailable()

        help_text = self.parser.format_help()

        # Check for specific examples
        assert "python -m src.services.messaging_cli --agent Agent-7 --message" in help_text
        assert "--bulk --message" in help_text
        assert "--onboarding" in help_text
        assert "--get-next-task" in help_text

    def test_flag_descriptions_accuracy(self):
        """Test that flag descriptions are accurate and helpful."""
        self._skip_if_imports_unavailable()

        help_text = self.parser.format_help()

        # Check specific flag descriptions
        assert "Message content to send" in help_text
        assert "Send to specific agent" in help_text
        assert "Send to all agents simultaneously" in help_text
        assert "Delivery method" in help_text
        assert "Display all available agents" in help_text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
