import logging

logger = logging.getLogger(__name__)
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

    def __init__(
        self,
        config: TheaConfig,
        browser_service: TheaBrowserService,
        response_service: TheaResponseService,
    ):
        self.config = config
        self.browser = browser_service
        self.response_service = response_service

    def send_message(self, message: str) -> MessageStatus:
        """Send a message to Thea."""
        logger.info("🌟 PHASE 1: SENDING MESSAGE TO THEA")
        logger.info("=" * 50)
        message_path = self._save_message(message)
        logger.info(f"💾 Message saved: {message_path}")
        pyperclip.copy(message)
        logger.info("✅ Message copied to clipboard")
        if self.browser.mode == BrowserMode.SELENIUM and self.browser.driver:
            return self._send_via_selenium(message)
        else:
            return self._send_via_manual(message)

    def _send_via_selenium(self, message: str) -> MessageStatus:
        """Send message using Selenium automation."""
        try:
            logger.info("🤖 AUTOMATED MESSAGE SENDING")
            logger.info("-" * 30)
            if "thea-manager" not in self.browser.get_current_url():
                logger.info("🌐 Navigating to Thea...")
                if not self.browser.navigate_to_thea():
                    return MessageStatus.FAILED
            if self.browser.send_message_to_input(message):
                return MessageStatus.SENT
            else:
                logger.info("🔄 Falling back to manual mode...")
                return self._send_via_manual(message)
        except Exception as e:
            logger.info(f"❌ Selenium message sending failed: {e}")
            return self._send_via_manual(message)

    def _send_via_manual(self, message: str) -> MessageStatus:
        """Send message using manual user interaction."""
        logger.info("👤 MANUAL MESSAGE SENDING")
        logger.info("-" * 30)
        try:
            if not self.browser.driver or self.browser.mode == BrowserMode.MANUAL:
                webbrowser.open(self.config.thea_url, new=1)
                logger.info("✅ Browser opened to Thea page")
        except:
            logger.info("⚠️  Could not open browser automatically")
        logger.info("\n📝 MANUAL STEPS REQUIRED:")
        logger.info("1. Make sure you're on the Thea page")
        logger.info("2. Click on the input field")
        logger.info("3. Press Ctrl+V (or Cmd+V on Mac) to paste")
        logger.info("4. Press Enter to send the message")
        input("\n🎯 Press Enter AFTER you have sent the message to Thea...")
        logger.info("✅ Message should now be sent to Thea!")
        return MessageStatus.SENT

    def wait_for_response(self, timeout: int = None) -> bool:
        """Wait for Thea to respond."""
        if timeout is None:
            timeout = self.config.response_timeout
        logger.info("\n⏳ WAITING FOR THEA'S RESPONSE")
        logger.info("=" * 50)
        if self.browser.mode == BrowserMode.MANUAL:
            return self._wait_for_response_manual()
        return self.response_service.wait_for_response(timeout)

    def _wait_for_response_manual(self) -> bool:
        """Fallback to manual waiting for response."""
        logger.info("👤 MANUAL RESPONSE DETECTION")
        logger.info("-" * 35)
        logger.info("Please wait for Thea to finish responding, then press Enter")
        input("🎯 Press Enter when Thea has finished responding...")
        return True

    def _save_message(self, message: str) -> Path:
        """Save message to file for reference."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        message_path = self.config.responses_dir / f"sent_message_{timestamp}.txt"
        with open(message_path, "w", encoding="utf-8") as f:
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
                with open(self.config.message_template_path, encoding="utf-8") as f:
                    return f.read().strip()
        except Exception as e:
            logger.info(f"⚠️  Could not load message template: {e}")
        return None
