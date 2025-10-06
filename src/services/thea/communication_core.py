#!/usr/bin/env python3
"""
Thea Communication - Core Logic
==============================

Main communication logic for Thea/ChatGPT interaction.
V2 Compliant: ≤400 lines, imports from modular components.

Features:
- Automated login detection and cookie persistence
- Selenium WebDriver integration
- Manual fallback modes
- Response detection and capture
- Comprehensive logging and analysis

Usage:
    from src.services.thea.communication_core import SimpleTheaCommunication

    comm = SimpleTheaCommunication(username="user@example.com", password="password")
    comm.run_communication_cycle("Hello Thea!")
"""

import argparse
import time
from pathlib import Path

import pyperclip

# Import our modular components
from .communication_selenium import TheaSeleniumManager
from .communication_utils import TheaCommunicationUtils
from .login_handler import create_thea_login_handler

# Import response detector
try:
    from response_detector import ResponseDetector, ResponseWaitResult
    RESPONSE_DETECTOR_AVAILABLE = True
except ImportError:
    RESPONSE_DETECTOR_AVAILABLE = False
    print("⚠️  ResponseDetector not available - response detection will be manual")


class SimpleTheaCommunication:
    """Simple send/receive communication with Thea."""

    def __init__(self, username=None, password=None, use_selenium=True, headless=False):
        """
        Initialize Thea communication.

        Args:
            username: ChatGPT username/email
            password: ChatGPT password
            use_selenium: Whether to use Selenium automation
            headless: Whether to run browser in headless mode
        """
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5"
        
        # Configuration
        self.username = username
        self.password = password
        self.use_selenium = use_selenium
        self.headless = headless

        # Initialize components
        self.login_handler = create_thea_login_handler(
            username=username, password=password, cookie_file="thea_cookies.json"
        )
        self.selenium_manager = TheaSeleniumManager(headless=headless)
        self.utils = TheaCommunicationUtils()

        # Selenium driver (initialized when needed)
        self.driver = None
        self.detector = None

    def ensure_authenticated(self) -> bool:
        """Ensure user is authenticated with Thea."""
        if not self.use_selenium:
            print("🔄 USING MANUAL MODE")
            return self._manual_authentication()

        if not self.driver:
            if not self.selenium_manager.initialize_driver():
                return self._manual_authentication()
            self.driver = self.selenium_manager.driver

        print("🔐 AUTOMATED AUTHENTICATION")
        print("-" * 30)

        # Use our modular login handler
        success = self.login_handler.ensure_login(self.driver)

        if success:
            print("✅ AUTHENTICATION SUCCESSFUL")

            # Additional navigation to chatgpt.com to stabilize login detection
            print("🔄 STABILIZING LOGIN DETECTION...")
            try:
                self.driver.get("https://chatgpt.com")
                time.sleep(3)
                print("✅ Navigated to chatgpt.com for login verification")

                # Check login status after navigation
                if self.login_handler.detector.is_logged_in(self.driver):
                    print("✅ LOGIN STATUS CONFIRMED after navigation")
                else:
                    print("⚠️  LOGIN STATUS UNCLEAR after navigation - continuing anyway")

            except Exception as e:
                print(f"⚠️  Navigation/stabilization warning: {e}")

            # Attach detector once driver is live
            if RESPONSE_DETECTOR_AVAILABLE:
                try:
                    self.detector = ResponseDetector(self.driver)
                except Exception as e:
                    print(f"⚠️  ResponseDetector init warning: {e}")

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
            # Open browser to Thea URL
            import webbrowser
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
        pyperclip.copy(message)
        print("✅ Message copied to clipboard")

        # Step 3: Save sent message for reference
        self.utils.save_sent_message(message)

        # Step 4: Send message based on mode
        if self.use_selenium and self.driver:
            return self.selenium_manager.send_message_selenium(self.driver, message, self.thea_url)
        else:
            return self.utils.send_message_manual(message, self.thea_url)

    def wait_for_thea_response(self, timeout: int = 120) -> bool:
        """Wait for Thea to finish responding using robust DOM polling."""
        print("🔍 Detecting Thea's response...")

        if not self.use_selenium or not self.driver:
            print("⚠️  Selenium not available - switching to manual mode")
            return self.utils.wait_for_response_manual()

        # Use robust, quorum-based detector
        if not self.detector and RESPONSE_DETECTOR_AVAILABLE:
            self.detector = ResponseDetector(self.driver)

        if self.detector:
            result = self.detector.wait_until_complete(
                timeout=timeout,
                stable_secs=3.0,
                poll=0.5,
                auto_continue=True,
                max_continue_clicks=1,
            )

            if result == ResponseWaitResult.COMPLETE:
                print("✅ Thea's response detected (stable & finished).")
                return True
            elif result == ResponseWaitResult.CONTINUE_REQUIRED:
                print("⚠️ Continue required but not auto-clicked; falling back to manual confirmation.")
                return self.utils.wait_for_response_manual()
            elif result == ResponseWaitResult.TIMEOUT:
                print(f"⏰ Timeout after {timeout} seconds.")
                return self.utils.wait_for_response_manual()
            else:  # NO_TURN
                print("⚠️ No assistant turn detected; switching to manual confirmation.")
                return self.utils.wait_for_response_manual()
        else:
            print("⚠️ ResponseDetector not available - using manual mode")
            return self.utils.wait_for_response_manual()

    def capture_thea_response(self):
        """Capture Thea's response via screenshot and extract response text."""
        return self.utils.capture_response(
            detector=self.detector,
            driver=self.driver,
            use_selenium=self.use_selenium
        )

    def cleanup(self):
        """Clean up resources."""
        self.selenium_manager.cleanup()

    def run_communication_cycle(self, message: str = None):
        """Run the complete send/receive communication cycle."""
        print("🚀 QUERYING THEA...")

        # Default message if none provided
        if not message:
            message = """🌟 THEA COMMUNICATION TEST - V2_SWARM

Hello Thea! This is Agent-4 (Captain) testing the communication system.

Please acknowledge this test message and confirm you can see it.

Current Status: Testing automated communication pipeline
Blocker Details: Verifying end-to-end message flow
Request: Please respond with a brief acknowledgment

Thank you for your assistance!
- Agent-4 (Captain)"""

        print(f"📝 Message: {message[:100]}...")

        try:
            # Phase 1: Send message
            if not self.send_message_to_thea(message):
                print("❌ Failed to send message")
                return False

            # Phase 2: Wait for response
            print("\n⏳ PHASE 2: WAITING FOR THEA'S RESPONSE")
            print("=" * 50)
            if not self.wait_for_thea_response():
                print("⚠️  Response detection failed - continuing anyway")

            # Phase 3: Capture response
            screenshot_path = self.capture_thea_response()
            if not screenshot_path:
                print("❌ Failed to capture response")
                return False

            # Phase 4: Create analysis
            self.utils.create_response_analysis(screenshot_path)

            # Load extracted response if available
            extracted_response = ""
            try:
                metadata_files = list(self.utils.responses_dir.glob("response_metadata_*.json"))
                if metadata_files:
                    latest_metadata = max(metadata_files, key=lambda x: x.stat().st_mtime)
                    with open(latest_metadata) as f:
                        metadata = json.load(f)
                    extracted_response = metadata.get("extracted_response", "")
            except Exception as e:
                print(f"⚠️  Could not load response metadata: {e}")

            print("\n🎉 QUERY COMPLETE!")
            print("=" * 30)
            print("📄 RESULTS:")
            print(f"   📋 Log: conversation_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md")
            if extracted_response:
                print(f"   📝 Thea responded: {len(extracted_response)} characters")
            else:
                print("   📸 Screenshot captured (check manually)")

            return True

        except Exception as e:
            print(f"❌ Communication cycle failed: {e}")
            return False
        finally:
            self.cleanup()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Simple Thea Communication System")
    parser.add_argument("--username", help="ChatGPT username/email for automated login")
    parser.add_argument("--password", help="ChatGPT password for automated login")
    parser.add_argument("--no-selenium", action="store_true", help="Disable Selenium automation")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--message", help="Custom message to send to Thea")

    args = parser.parse_args()

    try:
        # Create communication instance
        comm = SimpleTheaCommunication(
            username=args.username,
            password=args.password,
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

Request: Please provide guidance on resolving this blocker.

Thank you for your assistance!
- Agent-4 (Captain)"""
        )

        # Run communication cycle
        success = comm.run_communication_cycle(test_message)

        if success:
            print("\n✅ Communication cycle completed successfully!")
        else:
            print("\n❌ Communication cycle failed!")
            return 1

    except KeyboardInterrupt:
        print("\n⏹️  Communication interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

