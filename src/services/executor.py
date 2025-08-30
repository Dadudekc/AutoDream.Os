from __future__ import annotations

import argparse
from .interfaces import MessagingMode, MessageType
from .config import DEFAULT_COORDINATE_MODE, AGENT_COUNT
from .output_formatter import OutputFormatter
from .unified_messaging_service import UnifiedMessagingService


class CommandExecutor:
    """Execution logic for messaging commands."""

    def __init__(
        self,
        service: UnifiedMessagingService | None = None,
        formatter: OutputFormatter | None = None,
    ) -> None:
        self.service = service or UnifiedMessagingService()
        self.formatter = formatter or OutputFormatter()

    # --- Basic operations -------------------------------------------------
    def handle_validation(self, args: argparse.Namespace) -> bool:
        results = self.service.validate_coordinates()
        self.formatter.validation_results(results)
        return True

    def handle_bulk_messaging(self, args: argparse.Namespace) -> bool:
        mode = MessagingMode(args.mode)
        message_type = MessageType(args.type)
        print(f"📡 Bulk messaging to all agents via {mode.value}...")
        messages = {f"Agent-{i}": args.message for i in range(1, AGENT_COUNT + 1)}
        new_chat = bool(args.onboarding or args.new_chat)
        if new_chat:
            print("🚀 ONBOARDING messages detected - using new chat sequence!")
            if args.onboarding:
                message_type = MessageType.ONBOARDING_START
        results = self.service.send_bulk_messages(
            messages, DEFAULT_COORDINATE_MODE, message_type, new_chat
        )
        self.formatter.generic_results(
            "📊 Bulk Message Results:", results, args.high_priority
        )
        return True

    def handle_campaign_messaging(self, args: argparse.Namespace) -> bool:
        print("🗳️ Campaign messaging...")
        results = self.service.send_campaign_message(args.message)
        self.formatter.generic_results("📊 Campaign Results:", results)
        return True

    def handle_yolo_messaging(self, args: argparse.Namespace) -> bool:
        print("🚀 YOLO MODE ACTIVATED...")
        results = self.service.activate_yolo_mode(args.message)
        self.formatter.generic_results("📊 YOLO Results:", results)
        return True

    def handle_single_agent_messaging(self, args: argparse.Namespace) -> bool:
        mode = MessagingMode(args.mode)
        message_type = MessageType(args.type)
        print(f"🤖 Agent messaging via {mode.value}...")
        print("🔍 Validating coordinates before sending...")
        coordinate_mode = getattr(args, "coordinate_mode", DEFAULT_COORDINATE_MODE)
        validation_result = self.service.validate_agent_coordinates(
            args.agent, coordinate_mode
        )
        if not validation_result.get("valid", False):
            print(f"❌ Coordinate validation failed for {args.agent}:")
            print(f"   Error: {validation_result.get('error', 'Unknown error')}")
            print("   Please check coordinates and try again.")
            return False
        print(f"✅ Coordinates validated for {args.agent}")
        if args.high_priority:
            print("🚨 HIGH PRIORITY message detected - using Ctrl+Enter 2x sequence!")
            message_type = MessageType.HIGH_PRIORITY
        new_chat = bool(args.onboarding or args.new_chat)
        if new_chat:
            print("🚀 ONBOARDING message detected - using new chat sequence!")
            if args.onboarding:
                message_type = MessageType.ONBOARDING_START
        success = self.service.send_message(
            args.agent, args.message, message_type, mode, new_chat
        )
        if args.high_priority:
            status = (
                "✅ HIGH PRIORITY message sent successfully"
                if success
                else "❌ HIGH PRIORITY message failed"
            )
        else:
            status = "✅ Success" if success else "❌ Failed"
        print(f"Agent message: {status}")
        return success
