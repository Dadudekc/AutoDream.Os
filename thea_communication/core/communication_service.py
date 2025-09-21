#!/usr/bin/env python3
"""
Thea Communication Service
=========================

Core communication service for Thea interaction.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..automation.selenium_handler import SeleniumHandler
from ..automation.simple_manual import SimpleManualHandler
from ..response.response_handler import ResponseHandler
from thea_login_handler import create_thea_login_handler


class TheaCommunicationService:
    """Core service for Thea communication."""

    def __init__(self, username=None, use_selenium=True, headless=False):
        """Initialize the communication service."""
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
        self.responses_dir = Path("thea_responses")
        self.responses_dir.mkdir(exist_ok=True)

        # Configuration
        self.username = username
        self.use_selenium = use_selenium
        self.headless = headless

        # Initialize components
        self.login_handler = create_thea_login_handler(
# SECURITY: Password placeholder - replace with environment variable
        )
        
        self.selenium_handler = SeleniumHandler(headless=headless)
        self.manual_handler = SimpleManualHandler()
        self.response_handler = ResponseHandler()

    def initialize_driver(self):
        """Initialize the Selenium driver."""
        return self.selenium_handler.initialize_driver()

    def ensure_authenticated(self) -> bool:
        """Ensure user is authenticated with Thea."""
        if self.use_selenium:
            return self.selenium_handler.ensure_authenticated(self.login_handler)
        else:
            return self.manual_handler.ensure_authenticated()

    def send_message_to_thea(self, message: str) -> bool:
        """Send message to Thea."""
        if self.use_selenium:
            return self.selenium_handler.send_message(message)
        else:
            return self.manual_handler.send_message(message)

    def wait_for_thea_response(self, timeout: int = 120) -> bool:
        """Wait for Thea's response."""
        if self.use_selenium:
            return self.selenium_handler.wait_for_response(timeout)
        else:
            return self.manual_handler.wait_for_response()

    def capture_thea_response(self) -> Optional[str]:
        """Capture Thea's response."""
        driver = self.selenium_handler.driver if self.use_selenium else None
        return self.response_handler.capture_response(self.use_selenium, driver)

    def cleanup(self):
        """Cleanup resources."""
        if self.selenium_handler.driver:
            self.selenium_handler.cleanup()

    def run_communication_cycle(self, message: str = None) -> bool:
        """Run the complete send/receive communication cycle."""
        print("🚀 QUERYING THEA...")

        # Default message if none provided
        if not message:
            message = """🌟 THEA COMMUNICATION TEST - V2_SWARM

Hello Thea! This is Agent-4 (Captain) testing the communication system.

Please acknowledge this test message and confirm you can see it.

Thank you!
🐝 WE ARE SWARM"""

        # Save the message for reference
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        message_path = self.responses_dir / f"sent_message_{timestamp}.txt"
        with open(message_path, "w", encoding="utf-8") as f:
            f.write(message)
        print(f"💾 Message saved: {message_path}")

        print(f"📤 Message prepared: {len(message)} characters")
        print("Message preview:")
        print("-" * 30)
        print(message[:200] + "..." if len(message) > 200 else message)
        print("-" * 30)

        # Phase 1: Send message
        print("📤 Sending message to Thea...")
        success = self.send_message_to_thea(message)
        if not success:
            print("❌ Failed to send message")
            return False

        # Phase 2: Wait for response
        print("⏳ Waiting for Thea's response...")
        response_ready = self.wait_for_thea_response()

        if response_ready:
            print("✅ Response detected")
        else:
            print("⚠️  Manual confirmation used")

        # Phase 3: Capture response
        print("📸 Capturing response...")
        screenshot_path = self.capture_thea_response()
        if not screenshot_path:
            print("❌ Failed to capture response")
            return False

        print(f"📸 Response captured: {screenshot_path}")

        # Phase 4: Analysis is created automatically by response handler
        print("📊 Response analysis created automatically")

        print("✅ Communication cycle completed successfully!")
        return True


