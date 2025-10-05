#!/usr/bin/env python3
"""
Thea Communication Interface - V2 Compliant Simplified Interface
================================================================

Simplified interface for Thea agent communication system.
Refactored to maintain V2 compliance by using modular components.

Features:
- Simplified main interface
- Integration with all modular components
- Complete communication cycle orchestration
- V2 compliant design

Usage:
# SECURITY: Password placeholder - replace with environment variable
"""

import argparse
import time
import webbrowser
from datetime import datetime

from src.services.thea.thea_browser_manager import TheaBrowserManager

# Import our modular components
from src.services.thea.thea_communication_core import TheaCommunicationCore
from src.services.thea.thea_login_handler_refactored import create_thea_login_handler


class TheaCommunicationInterface:
    """Simplified interface for Thea communication system."""

    def __init__(
        self,
        username: str = None,
        password: str = None,
        use_selenium: bool = True,
        headless: bool = True,
    ):
        """Initialize the communication interface."""
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"

        # Configuration
        self.username = username
        self.password = password
        self.use_selenium = use_selenium
        self.headless = headless

        # Initialize components
        self.core = TheaCommunicationCore()
        self.browser_manager = TheaBrowserManager(headless=headless)
        self.login_handler = create_thea_login_handler(
            # SECURITY: Password placeholder - replace with environment variable
        )

        # Selenium driver (initialized when needed)
        self.driver = None

        # Check if Selenium is available
        if not self.browser_manager.is_selenium_available():
            if use_selenium:
                print("⚠️  Selenium not available - falling back to manual mode")
                self.use_selenium = False

    def ensure_authenticated(self) -> bool:
        """Ensure user is authenticated with Thea."""
        if not self.use_selenium:
            print("🔄 USING MANUAL MODE")
            return self._manual_authentication()

        if not self.driver:
            self.driver = self.browser_manager.initialize_driver()
            if not self.driver:
                return self._manual_authentication()

        print("🔐 AUTOMATED AUTHENTICATION")
        print("-" * 30)

        # Use our modular login handler
        success = self.login_handler.ensure_login(self.driver)

        if success:
            print("✅ AUTHENTICATION SUCCESSFUL")
            return True
        else:
            print("❌ AUTOMATED AUTHENTICATION FAILED")
            if self.headless:
                print("🫥 HEADLESS MODE: Manual authentication not possible")
                print("💡 Try running without --headless flag for manual auth")
                return False
            else:
                print("🔄 FALLING BACK TO MANUAL MODE")
                return self._manual_authentication()

    def _manual_authentication(self) -> bool:
        """Handle manual authentication."""
        print("👤 Manual authentication required - opening browser...")
        try:
            webbrowser.open(self.thea_url)
            print(f"✅ Browser opened to: {self.thea_url}")
            print("🔐 Please log in manually, then return to terminal")
            input("🎯 Press Enter when ready to continue...")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
            print(f"🔗 Please manually navigate to: {self.thea_url}")
            input("🎯 Press Enter when you're logged in...")

        print("⏳ Waiting 5 seconds for page to load...")
        time.sleep(5)
        return True

    def send_message_to_thea(self, message: str):
        """Send a message to Thea via browser."""
        print("🌟 PHASE 1: SENDING MESSAGE TO THEA")
        print("=" * 50)

        # Step 1: Ensure authentication
        if not self.ensure_authenticated():
            print("❌ AUTHENTICATION FAILED")
            return False

        # Step 2: Prepare message
        sent_message_path = self.core.prepare_message(message)

        # Step 3: Send message based on mode
        if self.use_selenium and self.driver:
            return self._send_message_selenium(message)
        else:
            return self._send_message_manual(message)

    def _send_message_selenium(self, message: str) -> bool:
        """Send message using Selenium automation."""
        return self.core.send_message_selenium(self.driver, message)

    def _send_message_manual(self, message: str) -> bool:
        """Send message using manual user interaction."""
        print("👤 MANUAL MESSAGE SENDING")
        print("-" * 30)

        # Open Thea in browser if not already open
        try:
            if not self.driver or not self.use_selenium:
                webbrowser.open(self.thea_url, new=1)
                print("✅ Browser opened to Thea page")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")

        print("\n📝 MANUAL STEPS REQUIRED:")
        print("1. Make sure you're on the Thea page")
        print("2. Click on the input field")
        print("3. Press Ctrl+V (or Cmd+V on Mac) to paste")
        print("4. Press Enter to send the message")

        input("\n🎯 Press Enter AFTER you have sent the message to Thea...")

        print("✅ Message should now be sent to Thea!")
        return True

    def wait_for_thea_response(self, timeout: int = 120) -> bool:
        """Wait for Thea to finish responding using robust DOM polling."""
        if not self.use_selenium or not self.driver:
            print("⚠️  Selenium not available - switching to manual mode")
            return self.core._wait_for_response_manual()

        return self.core.wait_for_response(self.driver, timeout)

    def capture_thea_response(self):
        """Capture Thea's response via screenshot and extract response text."""
        print("\n📸 PHASE 3: CAPTURING THEA'S RESPONSE")
        print("=" * 50)

        # First, try to extract the actual response text from Thea
        extracted_response = ""
        if self.use_selenium and self.driver:
            extracted_response = self.core.extract_response_text(self.driver)

        print("🔍 Processing response...")

        # Take screenshot
        screenshot_path = self.core.capture_screenshot()
        if not screenshot_path:
            print("❌ Failed to capture screenshot")
            return None

        # Find the most recent sent message file
        sent_message_path = None
        try:
            message_files = list(self.core.responses_dir.glob("sent_message_*.txt"))
            if message_files:
                sent_message_path = message_files[-1]  # Get most recent
        except Exception as e:
            print(f"⚠️  Could not find sent message file: {e}")

        # Save metadata
        if sent_message_path:
            self.core.save_metadata(screenshot_path, sent_message_path, extracted_response)

        # Create conversation log
        sent_message = ""
        if sent_message_path:
            try:
                with open(sent_message_path, encoding="utf-8") as f:
                    sent_message = f.read()
            except Exception as e:
                print(f"⚠️  Could not load sent message: {e}")

        self.core.create_conversation_log(
            sent_message, sent_message_path, screenshot_path, extracted_response
        )

        print("\n🔍 RESPONSE ANALYSIS")
        print("-" * 25)
        print("📝 Captured data:")
        print(f"   Screenshot: {screenshot_path}")
        print(f"   Sent Message: {sent_message_path}")
        if extracted_response:
            print(f"   📝 Extracted Response: {len(extracted_response)} characters")
            print(f"      Preview: {extracted_response[:100]}...")
        else:
            print("   ⚠️  Response text extraction failed")

        return screenshot_path

    def cleanup(self):
        """Clean up resources."""
        self.browser_manager.cleanup_driver(self.driver)

    def run_communication_cycle(self, message: str = None):
        """Run the complete send/receive communication cycle."""
        print("🚀 QUERYING THEA...")

        # Default message if none provided
        if not message:
            message = """🌟 THEA COMMUNICATION TEST - V2_SWARM

Hello Thea! This is Agent-4 (Captain) testing the communication system.

Please acknowledge this test message and confirm you can see it.

Thank you!
🐝 WE ARE SWARM"""

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

        # Phase 2: Wait for response (automated)
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

        # Phase 4: Create analysis
        print("📋 Generating analysis...")
        self.core.create_analysis_template(screenshot_path)

        print("\n🎉 QUERY COMPLETE!")
        print("=" * 30)
        print("📄 RESULTS:")
        print(f"   📋 Log: conversation_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md")
        print("   📸 Screenshot captured")

        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Thea Communication System - V2 Compliant")
    parser.add_argument("--username", help="ChatGPT username/email for automated login")
    # SECURITY: Password placeholder - replace with environment variable
    parser.add_argument("--no-selenium", action="store_true", help="Disable Selenium automation")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--message", help="Custom message to send to Thea")

    args = parser.parse_args()

    try:
        # Create communication instance
        comm = TheaCommunicationInterface(
            username=args.username,
            # SECURITY: Password placeholder - replace with environment variable
            use_selenium=not args.no_selenium,
            headless=args.headless,
        )

        # Use provided message or default agent query
        test_message = (
            args.message
            or """AGENT QUERY - BLOCKER ESCALATION

Hello Thea! Agent requesting assistance with blocker resolution.

Current Status: [Brief status update]

Blocker Details: [Describe the blocker/issue]

Please provide guidance and recommendations.

URGENT - AGENT ESCALATION"""
        )

        print("🤖 AGENT THEA QUERY TOOL - V2 COMPLIANT")
        print("=" * 40)

        success = comm.run_communication_cycle(test_message)

        if success:
            print("✅ Thea query completed successfully!")
        else:
            print("❌ Query failed - try --no-selenium for manual mode")

        # SECURITY: Key placeholder - replace with environment variable
        print("\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
    finally:
        # Always cleanup
        if "comm" in locals():
            comm.cleanup()


if __name__ == "__main__":
    main()
