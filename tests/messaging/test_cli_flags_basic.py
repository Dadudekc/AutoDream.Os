import pytest

from .cli_test_utils import TestCLIFlagsBase


class TestCLIFlagsBasics(TestCLIFlagsBase):
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
    def test_all_flags_exist_and_have_help(self, flag, expected_help):
        self._skip_if_imports_unavailable()
        help_text = self.parser.format_help()
        assert flag in help_text, f"Flag {flag} not found in help text"
        assert expected_help in help_text

    def test_message_content_flags(self):
        self._skip_if_imports_unavailable()
        args = self.parser.get_unified_utility().parse_args(["--message", "Test message"])
        assert args.message == "Test message"
        args = self.parser.get_unified_utility().parse_args(["--message", "Test"])
        assert args.sender == "Captain Agent-4"
        args = self.parser.get_unified_utility().parse_args(["--message", "Test", "--sender", "Agent-1"])
        assert args.sender == "Agent-1"

    def test_recipient_selection_flags(self):
        args = self.parser.get_unified_utility().parse_args(["--agent", "Agent-7", "--message", "Test"])
        assert args.agent == "Agent-7"
        assert args.bulk is False
        args = self.parser.get_unified_utility().parse_args(["--bulk", "--message", "Test"])
        assert args.bulk is True
        assert args.agent is None

    @pytest.mark.parametrize(
        "msg_type",
        ["text", "broadcast", "onboarding", "agent_to_agent", "system_to_agent", "human_to_agent"],
    )
    def test_message_type_flag(self, msg_type):
        args = self.parser.get_unified_utility().parse_args(["--message", "Test", "--type", msg_type])
        assert args.type == msg_type

    @pytest.mark.parametrize("priority", ["regular", "urgent"])
    def test_priority_flag(self, priority):
        args = self.parser.get_unified_utility().parse_args(["--message", "Test", "--priority", priority])
        assert args.priority == priority

    def test_high_priority_flag(self):
        args = self.parser.get_unified_utility().parse_args(["--message", "Test", "--high-priority"])
        assert args.high_priority is True
        assert args.priority == "regular"

    @pytest.mark.parametrize("mode", ["pyautogui", "inbox"])
    def test_mode_flag(self, mode):
        args = self.parser.get_unified_utility().parse_args(["--message", "Test", "--mode", mode])
        assert args.mode == mode

    def test_no_paste_flag(self):
        args = self.parser.get_unified_utility().parse_args(["--message", "Test", "--no-paste"])
        assert args.no_paste is True

    @pytest.mark.parametrize("tab_method", ["ctrl_t", "ctrl_n"])
    def test_new_tab_method_flag(self, tab_method):
        args = self.parser.get_unified_utility().parse_args([
            "--message",
            "Test",
            "--new-tab-method",
            tab_method,
        ])
        assert args.new_tab_method == tab_method
