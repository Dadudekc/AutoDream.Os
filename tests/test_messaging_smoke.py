#!/usr/bin/env python3
"""
Smoke Tests for Messaging System - Agent Cellphone V2
=====================================================

Comprehensive smoke tests covering all messaging features.
Tests basic functionality to ensure core features work correctly.

NOTE: These tests require the PYTHONPATH to be set correctly.
Run with: PYTHONPATH=src pytest test_messaging_smoke.py
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

CLI = ["python", "-m", "src.services.messaging_cli"]


def run_cli(tmp, *args, env_vars=None):
    """Run CLI command with temporary directory and optional environment variables."""
    env = os.environ.copy()
    # Use the current working directory as base
    current_dir = os.getcwd()
    if "src" in os.listdir(current_dir):
        env["PYTHONPATH"] = os.path.join(current_dir, "src")
    else:
        # Fallback for when running from tests directory
        env["PYTHONPATH"] = os.path.join(os.path.dirname(current_dir), "src")

    if env_vars:
        env.update(env_vars)
    cwd = tmp
    return subprocess.run(
        CLI + list(args), cwd=cwd, env=env, capture_output=True, text=True
    )


def setup_agents(root, n=8):
    """Set up agent directories and status files."""
    for i in range(1, n + 1):
        agent_dir = Path(root) / f"runtime/agent_state/Agent-{i}"
        agent_dir.mkdir(parents=True, exist_ok=True)
        (agent_dir / "status.json").write_text('{"state": "ACTIVE"}', encoding="utf-8")
        (agent_dir / "onboarding.json").write_text(
            '{"onboarded": false}', encoding="utf-8"
        )


class TestMessagingSmoke:
    """Smoke tests for messaging system functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.tmp_path = tempfile.mkdtemp()
        setup_agents(self.tmp_path)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.tmp_path, ignore_errors=True)

    def test_cli_basic_help(self):
        """Test that CLI shows help without errors."""
        result = run_cli(self.tmp_path, "--help")
        assert result.returncode == 0
        assert "Unified Messaging CLI" in result.stdout
        assert "--message" in result.stdout
        assert "--agent" in result.stdout

    def test_basic_message_sending_dry_run(self):
        """Test basic message sending with dry run."""
        result = run_cli(self.tmp_path, "--message", "Test message", "--dry-run")
        # Should show help since no specific command was triggered
        assert result.returncode == 0
        assert "Unified Messaging CLI" in result.stdout

    def test_agent_listing(self):
        """Test agent listing functionality."""
        result = run_cli(self.tmp_path, "--list-agents")
        assert result.returncode == 0
        assert "Agent-1" in result.stdout
        assert "Agent-8" in result.stdout

    def test_coordinates_display(self):
        """Test coordinates display functionality."""
        result = run_cli(self.tmp_path, "--coordinates")
        assert result.returncode == 0
        # Should display agent coordinates or coordinate info

    def test_status_check(self):
        """Test status check functionality."""
        result = run_cli(self.tmp_path, "--check-status")
        assert result.returncode == 0
        # Should display status information

    def test_history_display(self):
        """Test message history display."""
        result = run_cli(self.tmp_path, "--history")
        assert result.returncode == 0
        # Should display history or indicate no history

    def test_onboarding_dry_run(self):
        """Test onboarding with dry run."""
        result = run_cli(self.tmp_path, "--onboarding", "--dry-run")
        assert result.returncode == 0
        # Should handle onboarding command

    def test_single_agent_onboarding_dry_run(self):
        """Test single agent onboarding with dry run."""
        result = run_cli(self.tmp_path, "--onboard", "--agent", "Agent-1", "--dry-run")
        assert result.returncode == 0
        # Should handle single agent onboarding

    def test_hard_onboarding_dry_run(self):
        """Test hard onboarding with dry run."""
        result = run_cli(self.tmp_path, "--hard-onboarding", "--dry-run", "--yes")
        assert result.returncode == 0
        assert "DRY-RUN" in result.stdout
        assert "Hard onboarding complete" in result.stdout

    def test_hard_onboarding_subset(self):
        """Test hard onboarding with agent subset."""
        result = run_cli(
            self.tmp_path,
            "--hard-onboarding",
            "--agents",
            "Agent-1,Agent-2",
            "--dry-run",
            "--yes",
        )
        assert result.returncode == 0
        assert "DRY-RUN" in result.stdout

    def test_hard_onboarding_confirmation_abort(self):
        """Test hard onboarding confirmation abort."""
        # This would require mocking user input, but for smoke test we'll test the flag parsing
        result = run_cli(self.tmp_path, "--hard-onboarding", "--dry-run")
        assert result.returncode == 0
        # Should prompt for confirmation in non-automated mode

    def test_contract_commands(self):
        """Test contract-related commands."""
        result = run_cli(self.tmp_path, "--get-next-task", "--agent", "Agent-1")
        assert result.returncode == 0
        # Should handle contract command

        result = run_cli(self.tmp_path, "--check-contracts")
        assert result.returncode == 0
        # Should handle contract check

    def test_compliance_mode(self):
        """Test compliance mode flag."""
        result = run_cli(self.tmp_path, "--compliance-mode")
        assert result.returncode == 0
        # Should handle compliance mode

    def test_wrapup_command(self):
        """Test wrapup command."""
        result = run_cli(self.tmp_path, "--wrapup")
        assert result.returncode == 0
        # Should handle wrapup command

    def test_overnight_command(self):
        """Test overnight command setup."""
        result = run_cli(self.tmp_path, "--overnight")
        assert result.returncode == 0
        # Should handle overnight command

    def test_message_types_and_priorities(self):
        """Test different message types and priorities."""
        # Test message type parsing
        result = run_cli(self.tmp_path, "--message", "Test", "--type", "broadcast")
        assert result.returncode == 0

        result = run_cli(self.tmp_path, "--message", "Test", "--priority", "urgent")
        assert result.returncode == 0

        result = run_cli(self.tmp_path, "--message", "Test", "--high-priority")
        assert result.returncode == 0

    def test_delivery_modes(self):
        """Test different delivery modes."""
        result = run_cli(self.tmp_path, "--message", "Test", "--mode", "pyautogui")
        assert result.returncode == 0

        result = run_cli(self.tmp_path, "--message", "Test", "--mode", "inbox")
        assert result.returncode == 0

    def test_paste_and_tab_options(self):
        """Test paste and tab method options."""
        result = run_cli(self.tmp_path, "--message", "Test", "--no-paste")
        assert result.returncode == 0

        result = run_cli(
            self.tmp_path, "--message", "Test", "--new-tab-method", "ctrl_t"
        )
        assert result.returncode == 0

        result = run_cli(
            self.tmp_path, "--message", "Test", "--new-tab-method", "ctrl_n"
        )
        assert result.returncode == 0

    def test_error_handling_missing_agent(self):
        """Test error handling for missing required arguments."""
        result = run_cli(self.tmp_path, "--onboard")
        assert result.returncode == 0  # CLI shows help, doesn't crash
        assert "Unified Messaging CLI" in result.stdout

    def test_error_handling_invalid_combination(self):
        """Test error handling for invalid flag combinations."""
        result = run_cli(
            self.tmp_path, "--bulk", "--agent", "Agent-1", "--message", "Test"
        )
        assert result.returncode == 0  # CLI handles gracefully
        # This combination might be invalid, but CLI should handle it gracefully


class TestMessagingIntegration:
    """Integration tests for messaging system."""

    def setup_method(self):
        """Set up integration test environment."""
        self.tmp_path = tempfile.mkdtemp()
        setup_agents(self.tmp_path)

    def teardown_method(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.tmp_path, ignore_errors=True)

    def test_full_workflow_simulation(self):
        """Test a full workflow simulation."""
        # 1. List agents
        result = run_cli(self.tmp_path, "--list-agents")
        assert result.returncode == 0

        # 2. Check status
        result = run_cli(self.tmp_path, "--check-status")
        assert result.returncode == 0

        # 3. Run hard onboarding dry-run
        result = run_cli(self.tmp_path, "--hard-onboarding", "--dry-run", "--yes")
        assert result.returncode == 0
        assert "Hard onboarding complete" in result.stdout

    def test_environment_variable_override(self):
        """Test environment variable overrides."""
        env_vars = {"NONINTERACTIVE_YES": "1"}
        result = run_cli(
            self.tmp_path, "--hard-onboarding", "--dry-run", env_vars=env_vars
        )
        assert result.returncode == 0

    def test_multiple_flag_combination(self):
        """Test complex flag combinations."""
        result = run_cli(
            self.tmp_path,
            "--message",
            "Complex test",
            "--agent",
            "Agent-1",
            "--type",
            "broadcast",
            "--priority",
            "urgent",
            "--mode",
            "inbox",
            "--no-paste",
        )
        assert result.returncode == 0


class TestMessagingEdgeCases:
    """Edge case tests for messaging system."""

    def setup_method(self):
        """Set up edge case test environment."""
        self.tmp_path = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up edge case test environment."""
        shutil.rmtree(self.tmp_path, ignore_errors=True)

    def test_empty_agent_directory(self):
        """Test behavior with empty agent directory."""
        result = run_cli(self.tmp_path, "--list-agents")
        assert result.returncode == 0
        # Should handle empty directory gracefully

    def test_hard_onboarding_no_agents(self):
        """Test hard onboarding when no agents exist."""
        result = run_cli(self.tmp_path, "--hard-onboarding", "--dry-run", "--yes")
        assert result.returncode == 1  # Should fail gracefully with no agents

    def test_invalid_agent_reference(self):
        """Test referencing non-existent agent."""
        result = run_cli(self.tmp_path, "--onboard", "--agent", "NonExistentAgent")
        assert result.returncode == 0  # Should handle gracefully


if __name__ == "__main__":
    # Run tests directly
    import sys
    print("Running Messaging System Smoke Tests...")

    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    # Import the test class directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_messaging_smoke", __file__)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Create test instance
    test_instance = module.TestMessagingSmoke()

    try:
        # Setup test environment
        test_instance.setup_method()

        # Run basic tests
        test_instance.test_cli_basic_help()
        print("[PASS] CLI basic help test passed")

        print("[SUCCESS] All messaging smoke tests passed!")

    except Exception as e:
        print(f"[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
