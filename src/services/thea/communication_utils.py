#!/usr/bin/env python3
"""
Thea Communication - Utilities
==============================

Response capture, logging, and analysis utilities for Thea communication.
Extracted from main communication module for V2 compliance.
"""

import json
import time
import webbrowser
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip


class TheaCommunicationUtils:
    """Utilities for Thea communication response handling."""

    def __init__(self, responses_dir: str = "thea_responses"):
        """
        Initialize communication utilities.

        Args:
            responses_dir: Directory to store response files
        """
        self.responses_dir = Path(responses_dir)
        self.responses_dir.mkdir(exist_ok=True)

    def send_message_manual(self, message: str, thea_url: str) -> bool:
        """Send message using manual user interaction."""
        print("👤 MANUAL MESSAGE SENDING")
        print("-" * 30)

        # Open Thea in browser if not already open
        try:
            webbrowser.open(thea_url, new=1)
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

    def wait_for_response_manual(self) -> bool:
        """Fallback to manual waiting for response."""
        print("👤 MANUAL RESPONSE DETECTION")
        print("-" * 35)
        print("Please wait for Thea to finish responding, then press Enter")
        input("🎯 Press Enter when Thea has finished responding...")
        return True

    def capture_response(self, detector=None, driver=None, use_selenium=True):
        """Capture Thea's response via screenshot and extract response text."""
        print("\n📸 PHASE 3: CAPTURING THEA'S RESPONSE")
        print("=" * 50)

        # First, try to extract the actual response text from Thea
        extracted_response = self._extract_response_text(detector, driver, use_selenium)

        print("🔍 Processing response...")

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
            "thea_url": "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5",
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

    def _extract_response_text(self, detector=None, driver=None, use_selenium=True) -> str:
        """Extract the actual response text from Thea using ResponseDetector."""
        if not (use_selenium and driver and detector):
            return ""

        print("🔍 EXTRACTING THEA'S RESPONSE TEXT...")
        text = detector.extract_response_text()
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

    def save_sent_message(self, message: str):
        """Save the sent message for reference."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        message_path = self.responses_dir / f"sent_message_{timestamp}.txt"
        
        with open(message_path, "w", encoding="utf-8") as f:
            f.write(message)
        
        print(f"✅ Sent message saved: {message_path}")
        return message_path

