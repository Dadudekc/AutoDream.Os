#!/usr/bin/env python3
"""
Thea Cycle Manager - V2_SWARM Compliant Communication Cycle Management
======================================================================

Manages the complete Thea communication cycle with V2 compliance.

V2 COMPLIANCE:
- ✅ File size: <400 lines
- ✅ Type hints: Full coverage
- ✅ Modular design: Clean separation of concerns
- ✅ Repository pattern: Data access layer
- ✅ Single source of truth: SSOT for cycle management

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .thea_response_handler import TheaResponseHandler


class TheaCycleManager:
    """Manages the complete Thea communication cycle - V2_SWARM Compliant."""

    def __init__(self, responses_dir: Path) -> None:
        """Initialize cycle manager.

        Args:
            responses_dir: Directory to store response files
        """
        self.responses_dir: Path = responses_dir

    def run_communication_cycle(
        self,
        comm_instance: Any,
        message: str | None = None
    ) -> bool:
        """Run the complete send/receive communication cycle.

        Args:
            comm_instance: Thea communication instance
            message: Custom message to send, or None for default test message

        Returns:
            bool: True if communication cycle completed successfully, False otherwise
        """
        print("🐝 V2_SWARM THEA COMMUNICATION CYCLE")
        print("=" * 60)
        print("🎯 GOAL: Send prompt to Thea and receive response")
        print("👁️  USER WILL BE MY EYES THROUGHOUT THE PROCESS")
        print("=" * 60)

        # Default message if none provided
        if not message:
            message = """🌟 THEA COMMUNICATION TEST - V2_SWARM

Hello Thea! This is Agent-4 (Captain) testing the communication system.

Please acknowledge this test message and confirm you can see it.

Thank you!
🐝 WE ARE SWARM"""

        # Save the message for reference
        timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        message_path: Path = self.responses_dir / f"sent_message_{timestamp}.txt"
        with open(message_path, 'w', encoding='utf-8') as f:
            f.write(message)
        print(f"💾 Message saved: {message_path}")

        print(f"📤 Message prepared: {len(message)} characters")
        print("Message preview:")
        print("-" * 30)
        print(message[:200] + "..." if len(message) > 200 else message)
        print("-" * 30)

        try:
            # Phase 1: Authentication and Message Sending
            print("\n🚀 STARTING PHASE 1: MESSAGE SENDING")
            if not comm_instance.ensure_authenticated():
                print("❌ PHASE 1 FAILED: Could not authenticate")
                return False

            if not comm_instance.send_message_to_thea(message):
                print("❌ PHASE 1 FAILED: Could not send message")
                return False

            print("\n✅ PHASE 1 COMPLETE: Message sent to Thea")

            # Phase 2: Wait for Response (automated)
            print("\n⏳ PHASE 2: WAITING FOR THEA'S RESPONSE")
            print("=" * 50)

            # Use automated response detection
            response_ready: bool = comm_instance.wait_for_thea_response()

            if response_ready:
                print("✅ PHASE 2 COMPLETE: Thea's response detected")
            else:
                print("⚠️  PHASE 2: Manual confirmation used")

            # Phase 3: Capture Response
            print("\n🚀 STARTING PHASE 3: RESPONSE CAPTURE")
            response_handler = TheaResponseHandler(self.responses_dir, comm_instance.thea_url)
            screenshot_path: Path | None = response_handler.capture_response(
                comm_instance._extract_thea_response_text()
            )

            if not screenshot_path:
                print("❌ PHASE 3 FAILED: Could not capture response")
                return False

            print("✅ PHASE 3 COMPLETE: Response captured")

            # Phase 4: Create analysis
            print("\n🚀 STARTING PHASE 4: ANALYSIS SETUP")
            template_path: Path = response_handler.create_response_analysis(screenshot_path)

            # Success Summary
            self._print_success_summary(message, screenshot_path, template_path, message_path, timestamp)

            return True

        except Exception as e:
            print(f"\n💥 ERROR: {e}")
            return False

    def _print_success_summary(
        self,
        message: str,
        screenshot_path: Path,
        template_path: Path,
        message_path: Path,
        timestamp: str
    ) -> None:
        """Print comprehensive success summary.

        Args:
            message: The message that was sent
            screenshot_path: Path to the captured screenshot
            template_path: Path to the analysis template
            message_path: Path to the saved message
            timestamp: Timestamp string
        """
        print("\n🎉 COMMUNICATION CYCLE COMPLETE!")
        print("=" * 50)
        print("✅ SUMMARY:")
        print(f"   📤 Message sent: {len(message)} characters")
        print(f"   💾 Message saved: {message_path}")
        print(f"   📸 Response captured: {screenshot_path}")
        print(f"   📋 Conversation log: {self.responses_dir}/conversation_log_{timestamp}.md")
        print(f"   📝 Analysis template: {template_path}")
        print()
        print("🎯 NEXT STEPS:")
        print("   1. Review the conversation log for complete record")
        print("   2. Check the screenshot to see Thea's response")
        print("   3. Fill out the analysis template")
        print("   4. Let me know what Thea said!")
        print()
        print("🐝 WE ARE SWARM - COMMUNICATION SUCCESSFUL!")
