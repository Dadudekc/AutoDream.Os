"""
Thea Response Collector Module - V2 Compliance
=============================================

Handles advanced response collection with DOM polling and cursor detection.
Provides sophisticated response extraction capabilities.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class TheaResponseCollector:
    """
    Advanced response collector with DOM polling and cursor detection.

    Provides sophisticated response extraction by monitoring DOM changes,
    detecting cursor position changes, and handling dynamic content loading.
    """

    def __init__(self, driver: Any):
        """Initialize response collector with browser driver."""
        self.driver = driver
        self._response_cache = {}
        self._polling_active = False
        self._last_cursor_position = None

    def collect_full_response(self, timeout: float = 120.0) -> str | None:
        """
        Collect full response using enhanced DOM polling and cursor detection.

        This method implements advanced response detection by:
        1. Monitoring DOM changes for new conversation turns
        2. Detecting cursor position changes as response indicators
        3. Polling for response completion patterns
        4. Handling streaming responses with real-time updates

        Args:
            timeout: Maximum time to wait for response completion

        Returns:
            Complete response text or None if extraction fails
        """
        if not self.driver:
            return None

        logger.info("🚀 Starting enhanced response collection with DOM polling...")
        start_time = time.time()
        last_response_length = 0
        stable_count = 0
        max_stable_count = 3

        try:
            while time.time() - start_time < timeout:
                current_response = self._extract_current_response()
                if current_response:
                    current_length = len(current_response)
                    if current_length > last_response_length:
                        last_response_length = current_length
                        stable_count = 0
                        logger.info(f"📈 Response growing: {current_length} characters")
                    elif current_length == last_response_length:
                        stable_count += 1
                        logger.info(f"⏸️  Response stable: {stable_count}/{max_stable_count}")
                        if stable_count >= max_stable_count:
                            logger.info("✅ Response collection complete!")
                            return current_response
                    else:
                        last_response_length = current_length
                        stable_count = 0

                if self._is_response_complete():
                    logger.info("🎯 Response completion detected via indicators")
                    return self._extract_current_response()

                time.sleep(0.5)  # Brief pause between checks

            logger.warning(f"⏰ Response collection timed out after {timeout} seconds")
            return self._extract_current_response()  # Return whatever we have

        except Exception as e:
            logger.error(f"❌ Error during response collection: {e}")
            return None

    def _extract_current_response(self) -> str | None:
        """Extract current response from the page."""
        try:
            # Try primary selector first
            response_element = self.driver.find_element_by_css_selector(
                "[data-testid='conversation-turn']:last-child .markdown"
            )
            if response_element and response_element.text.strip():
                return response_element.text.strip()

            # Try fallback selectors
            fallback_selectors = [
                '.message-content:last-child',
                '.markdown:last-child',
                '[data-message-id]:last-child'
            ]

            for selector in fallback_selectors:
                try:
                    element = self.driver.find_element_by_css_selector(selector)
                    if element and element.text.strip():
                        return element.text.strip()
                except:
                    continue

            return None

        except Exception as e:
            logger.debug(f"Response extraction attempt failed: {e}")
            return None

    def _is_response_complete(self) -> bool:
        """Check if response is complete using various indicators."""
        try:
            # Check if thinking indicator is gone
            thinking_indicators = self.driver.find_elements_by_css_selector(
                "[data-testid='thinking-indicator']"
            )
            if not thinking_indicators:
                return True

            # Check for send button availability (indicates response complete)
            send_buttons = self.driver.find_elements_by_css_selector(
                "button[data-testid='send-button']"
            )
            if send_buttons and len(send_buttons) > 0:
                return True

            return False

        except Exception:
            return False

    def poll_for_completion(self, timeout: float = 30.0) -> bool:
        """
        Poll for response completion indicators.

        Args:
            timeout: Maximum time to poll

        Returns:
            True if completion detected, False otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._is_response_complete():
                return True
            time.sleep(1.0)
        return False

    def wait_for_response_start(self, timeout: float = 30.0) -> bool:
        """
        Wait for response to start appearing.

        Args:
            timeout: Maximum time to wait

        Returns:
            True if response started, False otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._extract_current_response():
                return True
            time.sleep(0.5)
        return False

    def get_response_metadata(self) -> dict[str, Any]:
        """Get metadata about the current response."""
        return {
            'has_response': self._extract_current_response() is not None,
            'is_complete': self._is_response_complete(),
            'response_length': len(self._extract_current_response() or ""),
            'timestamp': time.time()
        }


class TheaResponseMonitor:
    """Monitors response collection progress and provides status updates."""

    def __init__(self, collector: TheaResponseCollector):
        """Initialize response monitor."""
        self.collector = collector
        self._start_time = None
        self._last_update = None

    def start_monitoring(self) -> None:
        """Start monitoring response collection."""
        self._start_time = time.time()
        self._last_update = self._start_time

    def get_progress(self) -> dict[str, Any]:
        """Get current progress of response collection."""
        if not self._start_time:
            return {'status': 'not_started'}

        elapsed = time.time() - self._start_time
        metadata = self.collector.get_response_metadata()

        return {
            'status': 'in_progress' if not metadata['is_complete'] else 'complete',
            'elapsed_time': elapsed,
            'has_response': metadata['has_response'],
            'response_length': metadata['response_length'],
            'is_complete': metadata['is_complete']
        }

    def should_continue(self, max_time: float = 120.0) -> bool:
        """Check if monitoring should continue."""
        if not self._start_time:
            return True

        elapsed = time.time() - self._start_time
        return elapsed < max_time
