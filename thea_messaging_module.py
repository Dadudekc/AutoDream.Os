#!/usr/bin/env python3
"""
Thea Messaging Module - V2_SWARM Compliant Messaging Operations
===============================================================

Handles all messaging operations for Thea communication with V2 compliance.

V2 COMPLIANCE:
- ✅ File size: <400 lines
- ✅ Type hints: Full coverage
- ✅ Modular design: Clean separation of concerns
- ✅ Repository pattern: Data access layer

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

import time
import webbrowser
from pathlib import Path
from typing import Any

import pyperclip


class TheaMessagingModule:
    """Handles messaging operations for Thea - V2_SWARM Compliant."""

    def __init__(self, responses_dir: Path, thea_url: str) -> None:
        """Initialize messaging module.

        Args:
            responses_dir: Directory to store response files
            thea_url: URL of the Thea service
        """
        self.responses_dir: Path = responses_dir
        self.thea_url: str = thea_url

    def send_message_to_thea(self, comm_instance: Any, message: str) -> bool:
        """Send a message to Thea via browser - maintains exact original behavior.

        Args:
            comm_instance: Thea communication instance
            message: The message to send to Thea

        Returns:
            bool: True if message sent successfully, False otherwise
        """
        print("🌟 PHASE 1: SENDING MESSAGE TO THEA")
        print("=" * 50)

        # Step 1: Ensure authentication
        if not comm_instance.ensure_authenticated():
            print("❌ AUTHENTICATION FAILED")
            return False

        # Step 2: Prepare message
        pyperclip.copy(message)
        print("✅ Message copied to clipboard")

        # Step 3: Send message based on mode
        if comm_instance.use_selenium and comm_instance.driver:
            return self._send_message_selenium(comm_instance, message)
        else:
            return self._send_message_manual(message)

    def _send_message_selenium(self, comm_instance: Any, message: str) -> bool:
        """Send message using Selenium automation - maintains exact original behavior.

        Args:
            comm_instance: Thea communication instance
            message: The message to send

        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            print("🤖 AUTOMATED MESSAGE SENDING")
            print("-" * 30)

            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            # Navigate to Thea if not already there
            if "thea-manager" not in comm_instance.driver.current_url:
                print("🌐 Navigating to Thea...")
                comm_instance.driver.get(self.thea_url)
                time.sleep(3)

            # Wait for input field to be available
            wait = WebDriverWait(comm_instance.driver, 10)

            # Try multiple selectors for the input field
            input_selectors = [
                "textarea[data-testid*='prompt']",
                "textarea[placeholder*='Message']",
                "#prompt-textarea",
                "textarea",
                "[contenteditable='true']"
            ]

            input_field = None
            for selector in input_selectors:
                try:
                    if selector.startswith("#") or selector.startswith("."):
                        input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    else:
                        input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue

            if not input_field:
                print("❌ Could not find input field")
                return False

            # Clear and send message with proper line breaks
            input_field.clear()

            # Send message line by line to respect Shift+Enter for line breaks
            lines = message.split('\n')
            for i, line in enumerate(lines):
                if i > 0:  # Not the first line
                    input_field.send_keys(Keys.SHIFT + Keys.RETURN)
                input_field.send_keys(line)

            # Wait a moment then send the message
            time.sleep(1)
            input_field.send_keys(Keys.RETURN)

            print("✅ Message sent via Selenium!")
            return True

        except Exception as e:
            print(f"❌ Selenium message sending failed: {e}")
            print("🔄 Falling back to manual mode...")
            return self._send_message_manual(message)

    def _send_message_manual(self, message: str) -> bool:
        """Send message using manual user interaction - maintains exact original behavior.

        Args:
            message: The message to send

        Returns:
            bool: Always returns True (manual sending always succeeds)
        """
        print("👤 MANUAL MESSAGE SENDING")
        print("-" * 30)

        # Open Thea in browser if not already open
        try:
            webbrowser.open(self.thea_url, new=1)
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
        return True

    def wait_for_thea_response(self, comm_instance: Any, timeout: int = 120) -> bool:
        """Wait for Thea to finish responding using robust DOM polling - maintains exact original behavior.

        Args:
            comm_instance: Thea communication instance
            timeout: Maximum time to wait for response in seconds

        Returns:
            bool: True if response detected, False otherwise
        """
        print("\n⏳ WAITING FOR THEA'S RESPONSE (AUTOMATED)")
        print("=" * 50)
        print("🔍 Using robust DOM polling to detect when Thea is done...")

        if not comm_instance.use_selenium or not comm_instance.driver:
            print("⚠️  Selenium not available - switching to manual mode")
            return self._wait_for_response_manual()

        # Use robust, quorum-based detector
        if not comm_instance.detector:
            from response_detector import ResponseDetector
            comm_instance.detector = ResponseDetector(comm_instance.driver)

        result = comm_instance.detector.wait_until_complete(
            timeout=timeout,
            stable_secs=3.0,
            poll=0.5,
            auto_continue=True,
            max_continue_clicks=1,
        )

        if result.name == "COMPLETE":
            print("✅ Thea's response detected (stable & finished).")
            return True
        elif result.name == "CONTINUE_REQUIRED":
            print("⚠️ Continue required but not auto-clicked; falling back to manual confirmation.")
            return self._wait_for_response_manual()
        elif result.name == "TIMEOUT":
            print(f"⏰ Timeout after {timeout} seconds.")
            return self._wait_for_response_manual()
        else:  # NO_TURN
            print("⚠️ No assistant turn detected; switching to manual confirmation.")
            return self._wait_for_response_manual()

    def _wait_for_response_manual(self) -> bool:
        """Fallback to manual waiting for response - maintains exact original behavior.

        Returns:
            bool: Always returns True (manual waiting always succeeds)
        """
        print("👤 MANUAL RESPONSE DETECTION")
        print("-" * 35)
        print("Please wait for Thea to finish responding, then press Enter")
        input("🎯 Press Enter when Thea has finished responding...")
        return True
