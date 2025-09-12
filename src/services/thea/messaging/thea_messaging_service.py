#!/usr/bin/env python3
"""
Thea Messaging Service - V2 Compliant Message Handling
====================================================

Handles message sending, receiving, and communication flow for Thea services.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

import webbrowser
from datetime import datetime
from enum import Enum
from pathlib import Path

import pyperclip

from ...thea.config.thea_config import TheaConfig
from ..browser.thea_browser_service import BrowserMode, TheaBrowserService
from ..responses.thea_response_service import TheaResponseService


class MessageStatus(Enum):
    """Message sending status."""
    SENT = "sent"
    FAILED = "failed"
    PENDING = "pending"


class TheaMessagingService:
    """Handles message sending and receiving for Thea communication."""

    def __init__(self, config: TheaConfig, browser_service: TheaBrowserService, response_service: TheaResponseService):
        self.config = config
        self.browser = browser_service
        self.response_service = response_service

    def send_message(self, message: str) -> MessageStatus:
        """Send a message to Thea."""
        print("🌟 PHASE 1: SENDING MESSAGE TO THEA")
        print("=" * 50)

        # Save message for reference
        message_path = self._save_message(message)
        print(f"💾 Message saved: {message_path}")

        # Copy to clipboard
        pyperclip.copy(message)
        print("✅ Message copied to clipboard")

        # Send based on browser mode
        if self.browser.mode == BrowserMode.SELENIUM and self.browser.driver:
            return self._send_via_selenium(message)
        else:
            return self._send_via_manual(message)

    def _send_via_selenium(self, message: str) -> MessageStatus:
        """Send message using Selenium automation."""
        try:
            print("🤖 AUTOMATED MESSAGE SENDING")
            print("-" * 30)

            # Ensure we're on Thea page
            if "thea-manager" not in self.browser.get_current_url():
                print("🌐 Navigating to Thea...")
                if not self.browser.navigate_to_thea():
                    return MessageStatus.FAILED

            # Send the message
            if self.browser.send_message_to_input(message):
                return MessageStatus.SENT
            else:
                print("🔄 Falling back to manual mode...")
                return self._send_via_manual(message)

        except Exception as e:
            print(f"❌ Selenium message sending failed: {e}")
            return self._send_via_manual(message)

    def _send_via_manual(self, message: str) -> MessageStatus:
        """Send message using manual user interaction."""
        print("👤 MANUAL MESSAGE SENDING")
        print("-" * 30)

        # Open Thea in browser if not already open
        try:
            if not self.browser.driver or self.browser.mode == BrowserMode.MANUAL:
                webbrowser.open(self.config.thea_url, new=1)
                print("✅ Browser opened to Thea page")
        except:
            print("⚠️  Could not open browser automatically")

        print("\n📝 MANUAL STEPS REQUIRED:")
        print("1. Make sure you're on the Thea page")
        print("2. Click on the input field")
        print("3. Press Ctrl+V (or Cmd+V on Mac) to paste")
        print("4. Press Enter to send the message")

        input("\n🎯 Press Enter AFTER you have sent the message to Thea...")

        print("✅ Message should now be sent to Thea!")
        return MessageStatus.SENT

    def wait_for_response(self, timeout: int = None) -> bool:
        """Wait for Thea to respond."""
        if timeout is None:
            timeout = self.config.response_timeout

        print("\n⏳ WAITING FOR THEA'S RESPONSE")
        print("=" * 50)

        if self.browser.mode == BrowserMode.MANUAL:
            return self._wait_for_response_manual()

        return self.response_service.wait_for_response(timeout)

    def _wait_for_response_manual(self) -> bool:
        """Fallback to manual waiting for response."""
        print("👤 MANUAL RESPONSE DETECTION")
        print("-" * 35)
        print("Please wait for Thea to finish responding, then press Enter")
        input("🎯 Press Enter when Thea has finished responding...")
        return True

    def _save_message(self, message: str) -> Path:
        """Save message to file for reference."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        message_path = self.config.responses_dir / f"sent_message_{timestamp}.txt"

        with open(message_path, 'w', encoding='utf-8') as f:
            f.write(message)

        return message_path

    def get_default_message(self) -> str:
        """Get default test message."""
        return """THEA COMMUNICATION TEST - V2_SWARM

Hello Thea! This is Agent-4 (Captain) testing the automated communication system.

Current V2_SWARM Status:
- Captain's Handbook: Complete
- Discord Integration: Ready
- Swarm Coordination: Operational
- Tool Ecosystem: Active
- Automated Login: Integrated

Please acknowledge this test message and provide guidance for our next priorities.

Thank you!
WE ARE SWARM"""

    def load_message_template(self) -> str | None:
        """Load message from template file."""
        try:
            if self.config.message_template_path.exists():
                with open(self.config.message_template_path, encoding='utf-8') as f:
                    return f.read().strip()
        except Exception as e:
            print(f"⚠️  Could not load message template: {e}")

        return None
