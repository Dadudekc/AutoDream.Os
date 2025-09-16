import logging
logger = logging.getLogger(__name__)
"""
Thea Response Service - V2 Compliant Response Handling
====================================================

Handles response detection, capture, and processing for Thea services.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""
import json
from datetime import datetime
from enum import Enum
from pathlib import Path
import pyautogui
from ...thea.config.thea_config import TheaConfig
from ..browser.thea_browser_service import TheaBrowserService


class ResponseStatus(Enum):
    """Response detection status."""
    DETECTED = 'detected'
    TIMEOUT = 'timeout'
    CONTINUE_NEEDED = 'continue_needed'
    NO_RESPONSE = 'no_response'


class TheaResponseService:
    """Service for handling Thea responses."""

    def __init__(self, config: TheaConfig, browser_service: TheaBrowserService
        ):
        self.config = config
        self.browser = browser_service

    def wait_for_response(self, timeout: int=None) ->bool:
        """Wait for Thea to finish responding."""
        if timeout is None:
            timeout = self.config.response_timeout
        if not self.browser.driver:
            logger.info(
                '⚠️  No browser driver available for response detection')
            return False
        logger.info(
            '🔍 Using automated DOM polling to detect when Thea is done...')
        result = self.response_detector.wait_until_complete(timeout=timeout,
            stable_secs=self.config.stable_secs, poll=self.config.
            poll_interval, auto_continue=self.config.auto_continue,
            max_continue_clicks=self.config.max_continue_clicks)
        if result == ResponseWaitResult.COMPLETE:
            logger.info("✅ Thea's response detected (stable & finished).")
            return True
        elif result == ResponseWaitResult.CONTINUE_REQUIRED:
            logger.info(
                '⚠️ Continue required but not auto-clicked; switching to manual confirmation.'
                )
            return self._wait_for_response_manual()
        elif result == ResponseWaitResult.TIMEOUT:
            logger.info(f'⏰ Timeout after {timeout} seconds.')
            return self._wait_for_response_manual()
        else:
            logger.info(
                '⚠️ No assistant turn detected; switching to manual confirmation.'
                )
            return self._wait_for_response_manual()

    def _wait_for_response_manual(self) ->bool:
        """Manual waiting for response."""
        logger.info('👤 MANUAL RESPONSE DETECTION')
        logger.info('-' * 35)
        logger.info(
            'Please wait for Thea to finish responding, then press Enter')
        input('🎯 Press Enter when Thea has finished responding...')
        return True

    def capture_response(self) ->(Path | None):
        """Capture Thea's response via screenshot and extract text."""
        logger.info("\n📸 CAPTURING THEA'S RESPONSE")
        logger.info('=' * 50)
        extracted_response = self._extract_response_text()
        screenshot_path = self._take_screenshot()
        if screenshot_path:
            self._create_response_metadata(screenshot_path, extracted_response)
            return screenshot_path
        return None

    def _extract_response_text(self) ->str:
        """Extract response text from Thea using DOM."""
        if not self.browser.driver:
            return ''
        logger.info("🔍 EXTRACTING THEA'S RESPONSE TEXT...")
        text = self.response_detector.extract_response_text()
        if text:
            logger.info(f'✅ Selected response content ({len(text)} chars)')
        else:
            logger.info('⚠️  Could not extract response text from DOM')
        return text

    def _take_screenshot(self) ->(Path | None):
        """Take screenshot of the current page."""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_path = (self.config.responses_dir /
                f'thea_response_{timestamp}.png')
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            logger.info(f'✅ Screenshot captured: {screenshot_path}')
            return screenshot_path
        except Exception as e:
            logger.info(f'❌ Screenshot failed: {e}')
            return None

    def _create_response_metadata(self, screenshot_path: Path,
        extracted_response: str) ->None:
        """Create comprehensive response metadata."""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        sent_message_path = self._find_latest_sent_message()
        metadata = {'timestamp': datetime.now().isoformat(),
            'screenshot_path': str(screenshot_path), 'sent_message_path': 
            str(sent_message_path) if sent_message_path else None,
            'extracted_response': extracted_response, 'thea_url': self.
            config.thea_url, 'detection_method': 'automated_dom_polling',
            'character_count': len(extracted_response) if
            extracted_response else 0, 'response_extracted': bool(
            extracted_response)}
        json_path = (self.config.responses_dir /
            f'response_metadata_{timestamp}.json')
        with open(json_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f'✅ Metadata saved: {json_path}')
        self._create_conversation_log(sent_message_path, screenshot_path,
            timestamp, extracted_response)

    def _find_latest_sent_message(self) ->(Path | None):
        """Find the most recent sent message file."""
        try:
            message_files = list(self.config.responses_dir.glob(
                'sent_message_*.txt'))
            if message_files:
                return max(message_files, key=lambda x: x.stat().st_mtime)
        except Exception:
            pass
        return None

    def _create_conversation_log(self, sent_message_path: (Path | None),
        screenshot_path: Path, timestamp: str, extracted_response: str) ->None:
        """Create a comprehensive conversation log."""
        try:
            log_path = (self.config.responses_dir /
                f'conversation_log_{timestamp}.md')
            sent_message = ''
            if sent_message_path and sent_message_path.exists():
                with open(sent_message_path, encoding='utf-8') as f:
                    sent_message = f.read()
            response_section = ''
            if extracted_response:
                response_section = f"""

## Thea's Response
**Characters:** {len(extracted_response)}

```
{extracted_response}
```"""
            else:
                response_section = """

## Thea's Response
**Status:** Response text extraction failed
**Note:** Check screenshot for response content"""
            log_content = f"""# Thea Conversation Log
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Sent Message
**File:** {sent_message_path}
**Characters:** {len(sent_message) if sent_message else 0}

```
{sent_message}
```{response_section}

## Response Data
**Screenshot:** {screenshot_path}
**Detection Method:** Automated DOM polling

## Technical Details
- Response detection: Automated
- Screenshot captured: Yes
- Response text extracted: {'Yes' if extracted_response else 'No'}
- Metadata saved: Yes

---
**Conversation logged by:** V2_SWARM Automated System
"""
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(log_content)
            logger.info(f'📋 Conversation log created: {log_path}')
        except Exception as e:
            logger.info(f'⚠️  Could not create conversation log: {e}')
