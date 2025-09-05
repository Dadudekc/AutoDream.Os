#!/usr/bin/env python3
"""Comprehensive CLI flag tests for Agent Cellphone V2."""

from __future__ import annotations

import pytest

from tests.messaging.helpers.cli import create_enhanced_parser, parse_flags


class TestComprehensiveCLIFlags:
    """Comprehensive tests for messaging CLI flags."""

    def setup_method(self) -> None:
        """Create a parser for each test."""
        self.parser = create_enhanced_parser()

    @pytest.mark.parametrize(
        "flag,expected_help",
        [
            ("--message", "Message content to send"),
            ("--sender", "Message sender identity"),
            ("--agent", "Send to specific agent"),
            ("--bulk", "Send to all agents simultaneously"),
            ("--type", "Message category"),
            ("--priority", "Delivery priority"),
            ("--high-priority", "FORCE URGENT PRIORITY"),
            ("--mode", "Delivery method"),
            ("--no-paste", "Use keystroke typing instead of clipboard paste"),
            ("--list-agents", "Display all available agents"),
            ("--coordinates", "Show PyAutoGUI coordinate positions"),
            ("--history", "Show message delivery history"),
            ("--queue-stats", "Display message queue statistics"),
            ("--process-queue", "Process one batch of queued messages"),
            ("--start-queue-processor", "Start continuous background queue processor"),
            ("--stop-queue-processor", "Stop continuous background queue processor"),
            ("--check-status", "Check status of all agents"),
            ("--onboarding", "Send onboarding message to ALL agents"),
            ("--onboard", "Send onboarding message to specific agent"),
            ("--onboarding-style", "Onboarding message tone"),
            ("--compliance-mode", "AUTONOMOUS DEVELOPMENT MODE"),
            ("--get-next-task", "Claim next contract task"),
            ("--wrapup", "Send system wrapup message to ALL agents"),
        ],
    )
    def test_all_flags_exist_and_have_help(self, flag: str, expected_help: str) -> None:
        """Flags should be documented in parser help text."""
        help_text = self.parser.format_help()
        assert flag in help_text
        assert expected_help in help_text

    def test_message_content_flags(self) -> None:
        """Message and sender flags behave as expected."""
        args = parse_flags(["--message", "Test message"])
        assert args.message == "Test message"

        args = parse_flags(["--message", "Test"])
        assert args.sender == "Captain Agent-4"

        args = parse_flags(["--message", "Test", "--sender", "Agent-1"])
        assert args.sender == "Agent-1"

    def test_recipient_selection_flags(self) -> None:
        """Agent and bulk flags select recipients."""
        args = parse_flags(["--agent", "Agent-7", "--message", "Test"])
        assert args.agent == "Agent-7"
        assert not args.bulk

        args = parse_flags(["--bulk", "--message", "Test"])
        assert args.bulk
        assert args.agent is None

    @pytest.mark.parametrize(
        "msg_type",
        [
            "text",
            "broadcast",
            "onboarding",
            "agent_to_agent",
            "system_to_agent",
            "human_to_agent",
        ],
    )
    def test_message_type_flag(self, msg_type: str) -> None:
        """Type flag accepts all valid options."""
        args = parse_flags(["--type", msg_type, "--message", "Test"])
        assert args.type == msg_type

    @pytest.mark.parametrize("priority", ["regular", "urgent"])
    def test_priority_flag(self, priority: str) -> None:
        """Priority flag accepts all valid options."""
        args = parse_flags(["--priority", priority, "--message", "Test"])
        assert args.priority == priority

    def test_high_priority_flag(self) -> None:
        """High priority flag sets urgent priority."""
        args = parse_flags(["--high-priority", "--message", "Test"])
        assert args.high_priority

    @pytest.mark.parametrize("mode", ["pyautogui", "inbox"])
    def test_mode_flag(self, mode: str) -> None:
        """Mode flag accepts all valid options."""
        args = parse_flags(["--mode", mode, "--message", "Test"])
        assert args.mode == mode

    def test_no_paste_flag(self) -> None:
        """No-paste flag toggles typing mode."""
        args = parse_flags(["--no-paste", "--message", "Test"])
        assert args.no_paste

    @pytest.mark.parametrize("tab_method", ["ctrl_t", "ctrl_n"])
    def test_new_tab_method_flag(self, tab_method: str) -> None:
        """New-tab-method flag accepts both options."""
        args = parse_flags(["--new-tab-method", tab_method, "--message", "Test"])
        assert args.new_tab_method == tab_method

    @pytest.mark.parametrize(
        "flag",
        [
            "--list-agents",
            "--coordinates",
            "--history",
            "--queue-stats",
            "--process-queue",
            "--start-queue-processor",
            "--stop-queue-processor",
            "--check-status",
        ],
    )
    def test_utility_flags(self, flag: str) -> None:
        """Utility flags should set corresponding attributes."""
        args = parse_flags([flag])
        attr = flag.lstrip("-").replace("-", "_")
        assert getattr(args, attr)

    def test_onboarding_flags(self) -> None:
        """Onboarding-related flags work together."""
        args = parse_flags(["--onboarding"])
        assert args.onboarding

        args = parse_flags(["--onboard", "--agent", "Agent-7"])
        assert args.onboard
        assert args.agent == "Agent-7"

        args = parse_flags(["--onboarding-style", "professional", "--onboarding"])
        assert args.onboarding_style == "professional"

        args = parse_flags(["--compliance-mode"])
        assert args.compliance_mode

    def test_contract_flags(self) -> None:
        """Contract flags require agents when necessary."""
        args = parse_flags(["--get-next-task", "--agent", "Agent-7"])
        assert args.get_next_task
        assert args.agent == "Agent-7"

        args = parse_flags(["--wrapup"])
        assert args.wrapup

    @pytest.mark.parametrize(
        "combo",
        [
            ["--agent", "Agent-7", "--message", "Hello"],
            ["--bulk", "--message", "System update"],
            [
                "--agent",
                "Agent-7",
                "--message",
                "Test",
                "--type",
                "broadcast",
                "--priority",
                "urgent",
            ],
            [
                "--agent",
                "Agent-7",
                "--message",
                "Test",
                "--mode",
                "pyautogui",
                "--no-paste",
                "--new-tab-method",
                "ctrl_n",
            ],
            ["--agent", "Agent-7", "--message", "Test", "--mode", "inbox"],
        ],
    )
    def test_valid_flag_combinations(self, combo: list[str]) -> None:
        """Various valid flag combinations should parse."""
        args = parse_flags(combo)
        assert args is not None


class TestCLIIntegration:
    """Integration tests for parser output."""

    def test_parser_creation_and_help(self) -> None:
        """Parser can be created and help text contains expected sections."""
        parser = create_enhanced_parser()
        help_text = parser.format_help()
        assert "🚀 Agent Cellphone V2 - Unified Messaging System" in help_text
        assert "📝 Message Content" in help_text
        assert "👥 Recipient Selection" in help_text
        assert "⚙️ Message Properties" in help_text
        assert "📨 Delivery Mode" in help_text
        assert "🔍 Utility & Information" in help_text
        assert "📊 Queue Management" in help_text
        assert "🎓 Onboarding & Training" in help_text
        assert "📋 Contract & Task Management" in help_text

    def test_comprehensive_flag_coverage(self) -> None:
        """Help text should mention many flags."""
        parser = create_enhanced_parser()
        help_text = parser.format_help()
        assert help_text.count("--") >= 20


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
