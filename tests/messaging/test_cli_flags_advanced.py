import pytest

from src.core.validation.unified_validation_orchestrator import get_unified_validator

from .cli_test_utils import TestCLIFlagsBase, create_enhanced_parser


class TestCLIFlagsAdvanced(TestCLIFlagsBase):
    def test_utility_flags(self):
        flags = [
            "--list-agents",
            "--coordinates",
            "--history",
            "--queue-stats",
            "--process-queue",
            "--start-queue-processor",
            "--stop-queue-processor",
            "--check-status",
        ]
        for flag in flags:
            args = self.parser.get_unified_utility().parse_args([flag])
            flag_attr = flag.replace("--", "").replace("-", "_")
            assert get_unified_validator().safe_getattr(args, flag_attr) is True

    def test_onboarding_flags(self):
        args = self.parser.get_unified_utility().parse_args(["--onboarding"])
        assert args.onboarding is True
        args = self.parser.get_unified_utility().parse_args(["--onboard", "--agent", "Agent-7"])
        assert args.onboard is True
        assert args.agent == "Agent-7"
        args = self.parser.get_unified_utility().parse_args(["--onboarding-style", "professional", "--onboarding"])
        assert args.onboarding_style == "professional"
        args = self.parser.get_unified_utility().parse_args(["--compliance-mode"])
        assert args.compliance_mode is True

    def test_contract_flags(self):
        args = self.parser.get_unified_utility().parse_args(["--get-next-task", "--agent", "Agent-7"])
        assert args.get_next_task is True
        assert args.agent == "Agent-7"
        args = self.parser.get_unified_utility().parse_args(["--wrapup"])
        assert args.wrapup is True

    def test_valid_flag_combinations(self):
        valid_combinations = [
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
                "--sender-type",
                "system",
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
        ]
        for combination in valid_combinations:
            args = self.parser.get_unified_utility().parse_args(combination)
            assert args is not None, f"Failed to parse combination: {combination}"

    def test_parser_creation_and_help(self):
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

    def test_comprehensive_flag_coverage(self):
        parser = create_enhanced_parser()
        help_text = parser.format_help()
        flag_count = help_text.count("--")
        assert flag_count >= 20, f"Expected at least 20 flags, found {flag_count}"
