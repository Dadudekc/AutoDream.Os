#!/usr/bin/env python3
"""
Simple Thea Communication - Send & Receive
===========================================

Focus: Send prompt to Thea and capture response.
Fully automated login detection and cookie persistence.

Usage:
    python simple_thea_communication.py [--username EMAIL] [--password PASS]
"""

import argparse
import json
import time
import webbrowser
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip

from response_detector import ResponseDetector, ResponseWaitResult

# Import our modular login handler
from thea_login_handler import create_thea_login_handler


class SimpleTheaCommunication:
    """Simple send/receive communication with Thea."""

    def __init__(self, username=None, password=None, use_selenium=True, headless=False):
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
        self.responses_dir = Path("thea_responses")
        self.responses_dir.mkdir(exist_ok=True)

        # Login configuration
        self.username = username
        self.password = password
        self.use_selenium = use_selenium
        self.headless = headless

        # Initialize components
        self.login_handler = create_thea_login_handler(
            username=username, password=password, cookie_file="thea_cookies.json"
        )

        # Selenium driver (initialized when needed)
        self.driver = None
        self.detector: ResponseDetector | None = None

        # Check if Selenium is available
        try:
            import undetected_chromedriver as uc
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager

            self.selenium_available = True
        except ImportError:
            self.selenium_available = False
            if use_selenium:
                print("⚠️  Selenium not available - falling back to manual mode")
                self.use_selenium = False

    def initialize_driver(self):
        """Initialize Selenium WebDriver."""
        if not self.selenium_available or not self.use_selenium:
            return False

        try:
            import undetected_chromedriver as uc
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager

            print("🚀 INITIALIZING SELENIUM DRIVER")
            print("-" * 35)

            # Configure Chrome options
            options = Options()
            if self.headless:
                print("🫥 HEADLESS MODE: Configuring browser to run invisibly...")
                options.add_argument("--headless=new")  # Use new headless mode
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                # Additional headless-specific options
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-plugins")
                options.add_argument("--disable-images")
                options.add_argument("--disable-web-security")
                options.add_argument("--disable-features=VizDisplayCompositor")
                # Critical for headless mode
                options.add_argument("--remote-debugging-port=9222")
                options.add_argument(
                    "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
            else:
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")

            # Try undetected Chrome first (better for ChatGPT)
            try:
                print("🔍 Trying undetected Chrome driver...")
                if self.headless:
                    self.driver = uc.Chrome(options=options, headless=True)
                else:
                    self.driver = uc.Chrome(options=options)
                print("✅ Undetected Chrome driver initialized")
            except Exception as e:
                print(f"⚠️  Undetected Chrome failed: {e}")
                print("🔄 Falling back to standard Chrome driver...")
                from selenium import webdriver

                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()), options=options
                )
                print("✅ Standard Chrome driver initialized")

            return True

        except Exception as e:
            print(f"❌ Failed to initialize driver: {e}")
            self.use_selenium = False
            return False

    def ensure_authenticated(self) -> bool:
        """Ensure user is authenticated with Thea."""
        if not self.use_selenium:
            print("🔄 USING MANUAL MODE")
            return self._manual_authentication()

        if not self.driver:
            if not self.initialize_driver():
                return self._manual_authentication()

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
                if self.login_handler._is_logged_in(self.driver):
                    print("✅ LOGIN STATUS CONFIRMED after navigation")
                else:
                    print("⚠️  LOGIN STATUS UNCLEAR after navigation - continuing anyway")

            except Exception as e:
                print(f"⚠️  Navigation/stabilization warning: {e}")

            # Attach detector once driver is live
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

        # Step 3: Send message based on mode
        if self.use_selenium and self.driver:
            return self._send_message_selenium(message)
        else:
            return self._send_message_manual(message)

    def _send_message_selenium(self, message: str) -> bool:
        """Send message using Selenium automation."""
        try:
            print("🤖 AUTOMATED MESSAGE SENDING")
            print("-" * 30)

            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            # Navigate to Thea if not already there
            if "thea-manager" not in self.driver.current_url:
                print("🌐 Navigating to Thea...")
                self.driver.get(self.thea_url)
                time.sleep(3)

            # Wait for input field to be available
            wait = WebDriverWait(self.driver, 10)

            # Try multiple selectors for the input field
            input_selectors = [
                "textarea[data-testid*='prompt']",
                "textarea[placeholder*='Message']",
                "#prompt-textarea",
                "textarea",
                "[contenteditable='true']",
            ]

            input_field = None
            for selector in input_selectors:
                try:
                    if selector.startswith("#") or selector.startswith("."):
                        input_field = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    else:
                        input_field = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except Exception as e:
                    print(f"⚠️  Skipping selector {selector}: {e}")
                    continue

            if not input_field:
                print("❌ Could not find input field")
                return False

            # Clear and send message with proper line breaks
            input_field.clear()

            # Send message line by line to respect Shift+Enter for line breaks
            lines = message.split("\n")
            for i, line in enumerate(lines):
                if i > 0:  # Not the first line
                    # Send Shift+Enter for line break
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
        print("🔍 Detecting Thea's response...")

        if not self.use_selenium or not self.driver:
            print("⚠️  Selenium not available - switching to manual mode")
            return self._wait_for_response_manual()

        # Use robust, quorum-based detector
        if not self.detector:
            self.detector = ResponseDetector(self.driver)

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
            return self._wait_for_response_manual()
        elif result == ResponseWaitResult.TIMEOUT:
            print(f"⏰ Timeout after {timeout} seconds.")
            return self._wait_for_response_manual()
        else:  # NO_TURN
            print("⚠️ No assistant turn detected; switching to manual confirmation.")
            return self._wait_for_response_manual()

    def _wait_for_response_manual(self) -> bool:
        """Fallback to manual waiting for response."""
        print("👤 MANUAL RESPONSE DETECTION")
        print("-" * 35)
        print("Please wait for Thea to finish responding, then press Enter")
        input("🎯 Press Enter when Thea has finished responding...")
        return True

    def capture_thea_response(self):
        """Capture Thea's response via screenshot and extract response text."""
        print("\n📸 PHASE 3: CAPTURING THEA'S RESPONSE")
        print("=" * 50)

        # First, try to extract the actual response text from Thea
        extracted_response = self._extract_thea_response_text()

        print("🔍 Processing response...")

        # No manual observation needed - we have automated text extraction

        print("\n📸 STEP 2: TAKING SCREENSHOT")
        print("-" * 35)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        try:
            screenshot = pyautogui.screenshot()
            screenshot_path = self.responses_dir / f"thea_response_{timestamp}.png"
            screenshot.save(screenshot_path)
            print(f"✅ Screenshot captured: {screenshot_path}")
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None

        # Load the sent message for reference
        sent_message = ""
        sent_message_path = None
        try:
            # Find the most recent sent message file
            message_files = list(self.responses_dir.glob("sent_message_*.txt"))
            if message_files:
                sent_message_path = max(message_files, key=lambda x: x.stat().st_mtime)
                with open(sent_message_path, encoding="utf-8") as f:
                    sent_message = f.read()
        except Exception as e:
            print(f"⚠️  Could not load sent message: {e}")

        # Save comprehensive metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "screenshot_path": str(screenshot_path),
            "sent_message_path": str(sent_message_path) if sent_message_path else None,
            "sent_message_preview": (
                sent_message[:200] + "..." if len(sent_message) > 200 else sent_message
            ),
            "extracted_response": extracted_response,
            "thea_url": self.thea_url,
            "user_observation": "automated_extraction_used",
            "status": "response_captured",
            "detection_method": "automated_dom_polling",
            "character_count": len(sent_message) if sent_message else 0,
            "response_extracted": bool(extracted_response),
        }

        json_path = self.responses_dir / f"response_metadata_{timestamp}.json"
        with open(json_path, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Metadata saved: {json_path}")

        # Create comprehensive conversation log
        self._create_conversation_log(
            sent_message,
            sent_message_path,
            screenshot_path,
            "automated_extraction_used",
            timestamp,
            extracted_response,
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

    def _extract_thea_response_text(self) -> str:
        """Extract the actual response text from Thea using ResponseDetector."""
        if not (self.use_selenium and self.driver):
            return ""
        if not self.detector:
            self.detector = ResponseDetector(self.driver)

        print("🔍 EXTRACTING THEA'S RESPONSE TEXT...")
        text = self.detector.extract_response_text()
        if text:
            print(f"✅ Selected response content ({len(text)} chars)")
        else:
            print("⚠️  Could not extract response text from DOM")
        return text

    def _create_conversation_log(
        self,
        sent_message,
        sent_message_path,
        screenshot_path,
        user_observation,
        timestamp,
        extracted_response="",
    ):
        """Create a comprehensive conversation log."""
        try:
            log_path = self.responses_dir / f"conversation_log_{timestamp}.md"

            response_section = ""
            if extracted_response:
                response_section = f"""

## Thea's Response
**Characters:** {len(extracted_response)}

```
{extracted_response}
```
"""
            else:
                response_section = """

## Thea's Response
**Status:** Response text extraction failed
**Note:** Check screenshot for response content
"""

            log_content = f"""# Thea Conversation Log
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Sent Message
**File:** {sent_message_path}
**Characters:** {len(sent_message) if sent_message else 0}

```
{sent_message}
```
{response_section}
## Response Data
**Screenshot:** {screenshot_path}
**User Observation:** {user_observation}
**Detection Method:** Automated DOM polling

## Analysis Notes
- [Add your analysis here]
- [What did Thea actually say?]
- [Key insights from the response]
- [Next steps or follow-up questions]

## Technical Details
- Response detection: Automated
- Screenshot captured: Yes
- Response text extracted: {'Yes' if extracted_response else 'No'}
- Metadata saved: Yes
- Analysis template: Generated

---
**Conversation logged by:** V2_SWARM Automated System
"""

            with open(log_path, "w", encoding="utf-8") as f:
                f.write(log_content)

            print(f"📋 Conversation log created: {log_path}")

        except Exception as e:
            print(f"⚠️  Could not create conversation log: {e}")

    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser driver closed")
            except Exception as e:
                print(f"⚠️  Error closing driver: {e}")

    def create_response_analysis(self, screenshot_path):
        """Create analysis template for the captured response."""
        print("\n📝 CREATING RESPONSE ANALYSIS TEMPLATE")
        print("-" * 40)

        template_path = self.responses_dir / "response_analysis_template.md"

        template = f"""# Thea Response Analysis

**Captured:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Screenshot:** {screenshot_path}

## Captured Response
[View the screenshot at: {screenshot_path}]

## Thea's Response Content
[Copy Thea's response text here from the screenshot]

## Key Insights
- [Insight 1]
- [Insight 2]
- [Insight 3]

## Action Items
- [Action 1]
- [Action 2]
- [Action 3]

## Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

---
**Analysis completed by:** Agent-4 (Captain)
"""

        with open(template_path, "w") as f:
            f.write(template)
        print(f"✅ Analysis template created: {template_path}")

        return template_path

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
        self.create_response_analysis(screenshot_path)

        # Get extracted response from the capture method
        extracted_response = ""
        try:
            # Find the most recent metadata file to get extraction status
            metadata_files = list(self.responses_dir.glob("response_metadata_*.json"))
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
        print(f"   📋 Log: conversation_log_{timestamp}.md")
        if extracted_response:
            print(f"   📝 Thea responded: {len(extracted_response)} characters")
        else:
            print("   📸 Screenshot captured (check manually)")

        return True


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

Please provide guidance and recommendations.

URGENT - AGENT ESCALATION"""
        )

        print("🤖 AGENT THEA QUERY TOOL")
        print("=" * 30)

        success = comm.run_communication_cycle(test_message)

        if success:
            print("✅ Thea query completed successfully!")
        else:
            print("❌ Query failed - try --no-selenium for manual mode")

    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
    finally:
        # Always cleanup
        if "comm" in locals():
            comm.cleanup()


if __name__ == "__main__":
    main()
