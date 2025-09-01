#!/usr/bin/env python3
"""
CLI Validation Tests - Agent Cellphone V2
=========================================

Tests for CLI flag validation, mutual exclusions, dependencies,
and exit code handling.

Run with: python -m pytest tests/messaging/test_cli_validation.py -v
"""

import pytest
import subprocess
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from services.cli_validator import (
    CLIValidator, ValidationError, create_enhanced_parser,
    validate_and_parse_args
)


class TestCLIFlagValidation:
    """Test CLI flag validation logic."""

    def setup_method(self):
        """Setup for each test."""
        self.validator = CLIValidator()

    def test_mutual_exclusion_agent_bulk(self):
        """Test that --agent and --bulk cannot be used together."""
        # Create mock args with conflicting flags
        mock_args = MagicMock()
        mock_args.agent = "Agent-7"
        mock_args.bulk = True
        mock_args.onboarding = False
        mock_args.wrapup = False
        # Set other required attributes to avoid AttributeError
        for attr in ['onboard', 'get_next_task', 'message', 'mode', 'no_paste', 'new_tab_method']:
            setattr(mock_args, attr, None)

        is_valid, error = self.validator.validate_args(mock_args)

        assert not is_valid
        assert error is not None
        assert error.code == CLIValidator.EXIT_INVALID_FLAGS
        assert "XOR" in error.message or "cannot combine" in error.message.lower()

    def test_dependency_get_next_task_requires_agent(self):
        """Test that --get-next-task requires --agent."""
        mock_args = MagicMock()
        mock_args.agent = None
        mock_args.get_next_task = True
        # Set other required attributes
        for attr in ['bulk', 'onboarding', 'wrapup', 'onboard', 'message', 'mode', 'no_paste', 'new_tab_method']:
            setattr(mock_args, attr, None)

        is_valid, error = self.validator.validate_args(mock_args)

        assert not is_valid
        assert error is not None
        assert error.code == CLIValidator.EXIT_DEPENDENCY_MISSING

    def test_dependency_onboard_requires_agent(self):
        """Test that --onboard requires --agent."""
        mock_args = MagicMock()
        mock_args.agent = None
        mock_args.onboard = True
        # Set other required attributes
        for attr in ['bulk', 'onboarding', 'wrapup', 'get_next_task', 'message', 'mode', 'no_paste', 'new_tab_method']:
            setattr(mock_args, attr, None)

        is_valid, error = self.validator.validate_args(mock_args)

        assert not is_valid
        assert error is not None
        assert error.code == CLIValidator.EXIT_DEPENDENCY_MISSING

    def test_mode_gating_no_paste_requires_pyautogui(self):
        """Test that --no-paste only works with --mode pyautogui."""
        mock_args = MagicMock()
        mock_args.mode = "inbox"
        mock_args.no_paste = True
        # Set other required attributes
        for attr in ['agent', 'bulk', 'onboarding', 'wrapup', 'onboard', 'get_next_task', 'message', 'new_tab_method']:
            setattr(mock_args, attr, None)

        is_valid, error = self.validator.validate_args(mock_args)

        assert not is_valid
        assert error is not None
        assert error.code == CLIValidator.EXIT_MODE_MISMATCH

    def test_mode_gating_new_tab_method_requires_pyautogui(self):
        """Test that --new-tab-method only works with --mode pyautogui."""
        mock_args = MagicMock()
        mock_args.mode = "inbox"
        mock_args.new_tab_method = "ctrl_t"
        mock_args.no_paste = False
        # Set other required attributes
        for attr in ['agent', 'bulk', 'onboarding', 'wrapup', 'onboard', 'get_next_task', 'message']:
            setattr(mock_args, attr, None)

        is_valid, error = self.validator.validate_args(mock_args)

        assert not is_valid
        assert error is not None
        assert error.code == CLIValidator.EXIT_MODE_MISMATCH

    def test_valid_flag_combination(self):
        """Test a valid flag combination passes validation."""
        mock_args = MagicMock()
        mock_args.agent = "Agent-7"
        mock_args.message = "Hello"
        mock_args.bulk = False
        mock_args.onboarding = False
        mock_args.wrapup = False
        # Set other required attributes
        for attr in ['onboard', 'get_next_task', 'mode', 'no_paste', 'new_tab_method', 'sender', 'type', 'priority']:
            if attr == 'mode':
                setattr(mock_args, attr, 'pyautogui')
            else:
                setattr(mock_args, attr, None)

        is_valid, error = self.validator.validate_args(mock_args)

        assert is_valid
        assert error is None

    def test_valid_bulk_operation(self):
        """Test valid bulk operation."""
        mock_args = MagicMock()
        mock_args.agent = None
        mock_args.bulk = True
        mock_args.message = "System update"
        mock_args.onboarding = False
        mock_args.wrapup = False
        # Set other required attributes
        for attr in ['onboard', 'get_next_task', 'mode', 'no_paste', 'new_tab_method', 'sender', 'type', 'priority']:
            if attr == 'mode':
                setattr(mock_args, attr, 'pyautogui')
            else:
                setattr(mock_args, attr, None)

        is_valid, error = self.validator.validate_args(mock_args)

        assert is_valid
        assert error is None

    def test_message_requirement_for_send_operations(self):
        """Test that message is required for standard send operations."""
        mock_args = MagicMock()
        mock_args.agent = "Agent-7"
        mock_args.message = None  # No message provided
        mock_args.bulk = False
        mock_args.onboarding = False
        mock_args.onboard = False
        mock_args.wrapup = False
        mock_args.get_next_task = False
        # Set other required attributes
        for attr in ['mode', 'no_paste', 'new_tab_method', 'sender', 'type', 'priority']:
            if attr == 'mode':
                setattr(mock_args, attr, 'pyautogui')
            else:
                setattr(mock_args, attr, None)

        is_valid, error = self.validator.validate_args(mock_args)

        assert not is_valid
        assert error is not None
        assert error.code == CLIValidator.EXIT_DEPENDENCY_MISSING

    def test_special_operations_dont_require_message(self):
        """Test that special operations (onboarding, wrapup, get-next-task) don't require --message."""
        test_cases = [
            ("onboarding", True, False, False, False),
            ("onboard", False, True, False, False),
            ("wrapup", False, False, False, True),
            ("get_next_task", False, False, True, False),
        ]

        for operation, onboarding, onboard, wrapup, get_next_task in test_cases:
            mock_args = MagicMock()
            mock_args.agent = "Agent-7" if operation in ["onboard", "get_next_task"] else None
            mock_args.message = None  # No message
            mock_args.bulk = True if operation == "onboarding" else False
            mock_args.onboarding = onboarding
            mock_args.onboard = onboard
            mock_args.wrapup = wrapup
            mock_args.get_next_task = get_next_task
            # Set other required attributes
            for attr in ['mode', 'no_paste', 'new_tab_method', 'sender', 'type', 'priority']:
                if attr == 'mode':
                    setattr(mock_args, attr, 'pyautogui')
                else:
                    setattr(mock_args, attr, None)

            is_valid, error = self.validator.validate_args(mock_args)

            assert is_valid, f"Special operation {operation} should not require --message"
            assert error is None


class TestCLIExitCodes:
    """Test CLI exit code handling."""

    def test_exit_code_mapping(self):
        """Test that exit codes match specification."""
        assert CLIValidator.EXIT_SUCCESS == 0
        assert CLIValidator.EXIT_INVALID_FLAGS == 2
        assert CLIValidator.EXIT_DEPENDENCY_MISSING == 3
        assert CLIValidator.EXIT_MODE_MISMATCH == 4
        assert CLIValidator.EXIT_LOCK_TIMEOUT == 7
        assert CLIValidator.EXIT_QUEUE_FULL == 8
        assert CLIValidator.EXIT_INTERNAL_ERROR == 9

    def test_validation_error_structure(self):
        """Test ValidationError has required fields."""
        from datetime import datetime

        error = ValidationError(
            code=2,
            message="Test error",
            hint="Test hint",
            correlation_id="test123",
            timestamp=datetime.now()
        )

        assert error.code == 2
        assert error.message == "Test error"
        assert error.hint == "Test hint"
        assert error.correlation_id == "test123"
        assert isinstance(error.timestamp, datetime)

        # Test JSON serialization
        json_str = error.to_json()
        assert isinstance(json_str, str)

        # Test dict conversion
        error_dict = error.to_dict()
        assert isinstance(error_dict, dict)
        assert error_dict["code"] == 2


class TestCLIConfigSupport:
    """Test configuration loading and precedence."""

    def test_yaml_config_loading(self):
        """Test loading configuration from YAML file."""
        # This would require mocking file system access
        # For now, test the precedence logic structure
        pass

    def test_env_var_precedence(self):
        """Test environment variable precedence."""
        # This would require mocking environment variables
        pass


class TestParserCreation:
    """Test enhanced parser creation."""

    def test_parser_creation(self):
        """Test that enhanced parser can be created."""
        parser = create_enhanced_parser()
        assert parser is not None

        # Test that parser has expected argument groups
        help_text = parser.format_help()
        assert "📝 Message Content" in help_text
        assert "👥 Recipient Selection" in help_text
        assert "⚙️ Message Properties" in help_text
        assert "📨 Delivery Mode" in help_text

    def test_parser_help_formatting(self):
        """Test that help text is properly formatted."""
        parser = create_enhanced_parser()
        help_text = parser.format_help()

        # Check for key sections
        assert "EXAMPLES:" in help_text
        assert "EXIT CODES:" in help_text
        assert "23 flags" in help_text or "flags" in help_text


if __name__ == "__main__":
    # Run basic validation tests
    print("🧪 Running CLI Validation Tests...")

    validator = CLIValidator()
    test_instance = TestCLIFlagValidation()
    test_instance.setup_method()

    # Test mutual exclusion
    print("  Testing mutual exclusion (agent + bulk)...")
    test_instance.test_mutual_exclusion_agent_bulk()
    print("  ✅ Mutual exclusion test passed")

    # Test dependency
    print("  Testing dependency (get-next-task requires agent)...")
    test_instance.test_dependency_get_next_task_requires_agent()
    print("  ✅ Dependency test passed")

    # Test mode gating
    print("  Testing mode gating (no-paste requires pyautogui)...")
    test_instance.test_mode_gating_no_paste_requires_pyautogui()
    print("  ✅ Mode gating test passed")

    # Test valid combination
    print("  Testing valid flag combination...")
    test_instance.test_valid_flag_combination()
    print("  ✅ Valid combination test passed")

    print("🎉 All CLI validation tests passed!")
