#!/usr/bin/env python3
"""
Thea Communication Core - V2 Compliant Core Module
==================================================

Core communication functionality for Thea agent system.
Extracted from simple_thea_communication.py to maintain V2 compliance.

Features:
- Message sending and receiving
- Response detection and extraction
- Screenshot capture and metadata handling
- Conversation logging

Usage:
    from src.services.thea.thea_communication_core import TheaCommunicationCore

    core = TheaCommunicationCore()
    success = core.send_message("Hello Thea!")
"""

import json
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip
from response_detector import ResponseDetector, ResponseWaitResult


class TheaCommunicationCore:
    """Core Thea communication functionality."""

    def __init__(self, responses_dir: str = "thea_responses"):
        """Initialize the communication core."""
        self.responses_dir = Path(responses_dir)
        self.responses_dir.mkdir(exist_ok=True)
        self.detector: ResponseDetector | None = None

    def prepare_message(self, message: str) -> Path:
        """Prepare and save message for sending."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        message_path = self.responses_dir / f"sent_message_{timestamp}.txt"

        with open(message_path, "w", encoding="utf-8") as f:
            f.write(message)

        pyperclip.copy(message)
        print(f"💾 Message saved: {message_path}")
        print(f"📤 Message prepared: {len(message)} characters")

        return message_path

    def send_message_selenium(self, driver, message: str) -> bool:
        """Send message using Selenium automation."""
        try:
            print("AUTOMATED MESSAGE SENDING")
            print("-" * 30)

            from selenium.webdriver.common.by import By

            # SECURITY: Key placeholder - replace with environment variable
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"

            # Navigate to Thea if not already there
            if "thea-manager" not in driver.current_url:
                print("Navigating to Thea...")
                driver.get(thea_url)
                time.sleep(3)

            # Wait for input field to be available
            wait = WebDriverWait(driver, 10)

            # Try multiple selectors for the input field (updated for current ChatGPT)
            input_selectors = [
                "#prompt-textarea > p",  # Primary selector - contenteditable paragraph
                "p[data-placeholder='Ask anything']",  # Alternative selector
                "p[class*='placeholder']",  # Another alternative
                "textarea[data-testid*='prompt']",
                "textarea[placeholder*='Message']",
                "#prompt-textarea",
                "textarea[placeholder*='Send a message']",
                "textarea[data-testid='prompt-textarea']",
                "div[contenteditable='true'][role='textbox']",
                "textarea",
                "[contenteditable='true']",
                "div[data-testid='conversation-composer-input'] textarea",
                "div[data-testid='conversation-composer-input'] div[contenteditable='true']",
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
                    print(f"Skipping selector {selector}: {e}")
                    continue

            if not input_field:
                print("Could not find input field")
                return False

            # Clear and send message with proper line breaks
            input_field.clear()

            # Check if this is a contenteditable element (like the paragraph)
            is_contenteditable = (
                input_field.get_attribute("contenteditable") == "true"
                or input_field.tag_name == "p"
            )

            if is_contenteditable:
                # For contenteditable elements, use Selenium's send_keys with proper line breaks
                print("Using Selenium send_keys for contenteditable element")
                from selenium.webdriver.common.keys import Keys

                # Send message line by line to respect Shift+Enter for line breaks
                lines = message.split("\n")
                for i, line in enumerate(lines):
                    if i > 0:  # Not the first line
                        # Send Shift+Enter for line break
                        input_field.send_keys(Keys.SHIFT + Keys.ENTER)
                        time.sleep(0.1)

                    # Type the line
                    input_field.send_keys(line)
                    time.sleep(0.1)
            else:
                # For regular textareas, use PyAutoGUI
                print("Using PyAutoGUI for textarea element")
                # Send message line by line to respect Shift+Enter for line breaks
                lines = message.split("\n")
                for i, line in enumerate(lines):
                    if i > 0:  # Not the first line
                        # Send Shift+Enter for line break
                        pyautogui.hotkey("shift", "enter")
                        time.sleep(0.5)

                    # Type the line
                    pyautogui.typewrite(line)
                    time.sleep(0.1)

            # Wait a moment then send the message
            time.sleep(1)

            if is_contenteditable:
                # For contenteditable elements, use Selenium ActionChains
                from selenium.webdriver.common.action_chains import ActionChains
                from selenium.webdriver.common.keys import Keys

                print("Using Selenium ActionChains to send message")
                ActionChains(driver).send_keys(Keys.ENTER).perform()
            else:
                # For regular textareas, use PyAutoGUI
                print("Using PyAutoGUI to send message")
                pyautogui.press("enter")

            print("✅ Message sent via Selenium!")
            return True

        except Exception as e:
            print(f"❌ Selenium message sending failed: {e}")
            return False

    def wait_for_response(self, driver, timeout: int = 120) -> bool:
        """Wait for Thea to finish responding using robust DOM polling."""
        print("🔍 Detecting Thea's response...")

        # Use robust, quorum-based detector
        if not self.detector:
            self.detector = ResponseDetector(driver)

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

    def extract_response_text(self, driver) -> str:
        """Extract the actual response text from Thea using ResponseDetector."""
        if not self.detector:
            self.detector = ResponseDetector(driver)

        print("🔍 EXTRACTING THEA'S RESPONSE TEXT...")
        text = self.detector.extract_response_text()
        if text:
            print(f"✅ Selected response content ({len(text)} chars)")
        else:
            print("⚠️  Could not extract response text from DOM")
        return text

    def capture_screenshot(self) -> Path | None:
        """Capture screenshot of current state."""
        print("\n📸 TAKING SCREENSHOT")
        print("-" * 35)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        try:
            screenshot = pyautogui.screenshot()
            screenshot_path = self.responses_dir / f"thea_response_{timestamp}.png"
            screenshot.save(screenshot_path)
            print(f"✅ Screenshot captured: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None

    def save_metadata(
        self, screenshot_path: Path, sent_message_path: Path, extracted_response: str
    ) -> Path:
        """Save comprehensive metadata about the conversation."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Load the sent message for reference
        sent_message = ""
        try:
            with open(sent_message_path, encoding="utf-8") as f:
                sent_message = f.read()
        except Exception as e:
            print(f"⚠️  Could not load sent message: {e}")

        # Save comprehensive metadata
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "screenshot_path": str(screenshot_path),
            "sent_message_path": str(sent_message_path),
            "sent_message_preview": (
                sent_message[:200] + "..." if len(sent_message) > 200 else sent_message
            ),
            "extracted_response": extracted_response,
            "thea_url": "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager",
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

        return json_path

    def create_conversation_log(
        self,
        sent_message: str,
        sent_message_path: Path,
        screenshot_path: Path,
        extracted_response: str,
    ) -> Path:
        """Create a comprehensive conversation log."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
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
**User Observation:** automated_extraction_used
**Detection Method:** Automated DOM polling

## Analysis Notes
- [Add your analysis here]
- [What did Thea actually say?]
# SECURITY: Key placeholder - replace with environment variable
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
            return log_path

        except Exception as e:
            print(f"⚠️  Could not create conversation log: {e}")
            return None

    def create_analysis_template(self, screenshot_path: Path) -> Path:
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
