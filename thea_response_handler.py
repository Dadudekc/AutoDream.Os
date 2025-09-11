#!/usr/bin/env python3
"""
Thea Response Handler - V2_SWARM Compliant Response Management
===============================================================

Handles Thea response capture, logging, and analysis with V2 compliance.

V2 COMPLIANCE:
- ✅ File size: <400 lines
- ✅ Type hints: Full coverage
- ✅ Modular design: Clean separation of concerns
- ✅ Repository pattern: Data access layer
- ✅ Single source of truth: SSOT for response handling

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
import pyautogui


class TheaResponseHandler:
    """Handles Thea response capture, logging, and analysis - V2_SWARM Compliant."""

    def __init__(self, responses_dir: Path, thea_url: str) -> None:
        """Initialize response handler.

        Args:
            responses_dir: Directory to store response files
            thea_url: URL of the Thea service
        """
        self.responses_dir: Path = responses_dir
        self.thea_url: str = thea_url

    def capture_response(
        self,
        extracted_response: str,
        detector: Optional[Any] = None
    ) -> Optional[Path]:
        """Capture Thea's response via screenshot and extract response text.

        Args:
            extracted_response: Pre-extracted response text
            detector: Response detector instance (if available)

        Returns:
            Optional[Path]: Path to captured screenshot, or None if failed
        """
        print("\n📸 PHASE 3: CAPTURING THEA'S RESPONSE")
        print("=" * 50)

        print("🔍 STEP 1: CHECKING BROWSER STATE")
        print("-" * 40)
        print("👁️  LOOK AT THE BROWSER NOW!")
        print("🤖 I need to know:")
        print("   - Did Thea respond? (yes/no)")
        print("   - What does Thea's response say?")
        print("   - Are there any error messages?")
        print("   - Is the conversation visible?")

        user_observation: str = input("\n🎯 DESCRIBE WHAT YOU SEE IN THE BROWSER: ").strip()

        if "error" in user_observation.lower() or "no response" in user_observation.lower():
            print("⚠️  ISSUE DETECTED!")
            print("📝 Please describe the issue so I can help fix it:")
            issue_details: str = input("🎯 ISSUE DESCRIPTION: ").strip()
            print(f"🔧 NOTED: {issue_details}")
            print("💡 We'll capture the screenshot anyway for debugging")

        print("\n📸 STEP 2: TAKING SCREENSHOT")
        print("-" * 35)

        timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        try:
            screenshot = pyautogui.screenshot()
            screenshot_path: Path = self.responses_dir / f"thea_response_{timestamp}.png"
            screenshot.save(screenshot_path)
            print(f"✅ Screenshot captured: {screenshot_path}")
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None

        # Load the sent message for reference
        sent_message, sent_message_path = self._load_sent_message()

        # Save comprehensive metadata
        metadata: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "screenshot_path": str(screenshot_path),
            "sent_message_path": str(sent_message_path) if sent_message_path else None,
            "sent_message_preview": sent_message[:200] + "..." if len(sent_message) > 200 else sent_message,
            "extracted_response": extracted_response,
            "thea_url": self.thea_url,
            "user_observation": user_observation,
            "status": "response_captured",
            "detection_method": "automated_dom_polling",
            "character_count": len(sent_message) if sent_message else 0,
            "response_extracted": bool(extracted_response)
        }

        json_path: Path = self.responses_dir / f"response_metadata_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Metadata saved: {json_path}")

        # Create comprehensive conversation log
        self._create_conversation_log(
            sent_message, sent_message_path, screenshot_path,
            user_observation, timestamp, extracted_response
        )

        print("\n🔍 STEP 3: RESPONSE ANALYSIS")
        print("-" * 30)
        print("📝 Based on your observation, here's what I captured:")
        print(f"   Screenshot: {screenshot_path}")
        print(f"   Sent Message: {sent_message_path}")
        if extracted_response:
            print(f"   📝 Extracted Response: {len(extracted_response)} characters")
            print(f"      Preview: {extracted_response[:100]}...")
        else:
            print("   ⚠️  Response text extraction failed")
        print(f"   Your notes: {user_observation}")
        print(f"   Timestamp: {timestamp}")

        return screenshot_path

    def _load_sent_message(self) -> Tuple[str, Optional[Path]]:
        """Load the most recent sent message for reference.

        Returns:
            Tuple[str, Optional[Path]]: Message content and file path
        """
        sent_message: str = ""
        sent_message_path: Optional[Path] = None

        try:
            # Find the most recent sent message file
            message_files = list(self.responses_dir.glob("sent_message_*.txt"))
            if message_files:
                sent_message_path = max(message_files, key=lambda x: x.stat().st_mtime)
                with open(sent_message_path, 'r', encoding='utf-8') as f:
                    sent_message = f.read()
        except Exception as e:
            print(f"⚠️  Could not load sent message: {e}")

        return sent_message, sent_message_path

    def _create_conversation_log(
        self,
        sent_message: str,
        sent_message_path: Optional[Path],
        screenshot_path: Path,
        user_observation: str,
        timestamp: str,
        extracted_response: str = ""
    ) -> None:
        """Create a comprehensive conversation log.

        Args:
            sent_message: The message that was sent
            sent_message_path: Path to the saved message file
            screenshot_path: Path to the captured screenshot
            user_observation: User's observation of the browser state
            timestamp: Timestamp string for the log
            extracted_response: Extracted response text (if available)
        """
        try:
            log_path: Path = self.responses_dir / f"conversation_log_{timestamp}.md"

            response_section: str = ""
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

            log_content: str = f"""# Thea Conversation Log
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

            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(log_content)

            print(f"📋 Conversation log created: {log_path}")

        except Exception as e:
            print(f"⚠️  Could not create conversation log: {e}")

    def create_response_analysis(self, screenshot_path: Path) -> Path:
        """Create analysis template for the captured response.

        Args:
            screenshot_path: Path to the captured screenshot

        Returns:
            Path: Path to the created analysis template
        """
        print("\n📝 CREATING RESPONSE ANALYSIS TEMPLATE")
        print("-" * 40)

        template_path: Path = self.responses_dir / "response_analysis_template.md"

        template: str = f"""# Thea Response Analysis

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

        with open(template_path, 'w') as f:
            f.write(template)
        print(f"✅ Analysis template created: {template_path}")

        return template_path
