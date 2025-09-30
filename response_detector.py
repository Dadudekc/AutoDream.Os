#!/usr/bin/env python3
"""
Response Detector - THEA Response Detection Module
=================================================

Provides response detection and extraction capabilities for THEA communication.
This module handles DOM polling, response stability detection, and text extraction.

Features:
- Response completion detection
- Response text extraction
- DOM stability monitoring
- Timeout handling
- Continue button detection

Usage:
    from response_detector import ResponseDetector, ResponseWaitResult
    
    detector = ResponseDetector(driver)
    result = detector.wait_until_complete(timeout=120)
    text = detector.extract_response_text()
"""

import time
from enum import Enum

# Selenium imports
try:
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException, TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not available - ResponseDetector will use fallback methods")


class ResponseWaitResult(Enum):
    """Result of waiting for response completion."""

    COMPLETE = "complete"
    TIMEOUT = "timeout"
    CONTINUE_REQUIRED = "continue_required"
    NO_TURN = "no_turn"


class ResponseDetector:
    """Detects and extracts responses from THEA/ChatGPT interface."""

    def __init__(self, driver: webdriver.Chrome | None = None):
        """Initialize response detector."""
        self.driver = driver
        self.last_response_length = 0
        self.stable_count = 0

        # Common selectors for ChatGPT/THEA interface
        self.response_selectors = [
            # ChatGPT response containers
            '[data-message-author-role="assistant"]',
            ".markdown.prose",
            '[data-testid="conversation-turn-3"]',
            ".group\\/conversation-turn",
            # Generic response containers
            ".response-container",
            ".assistant-response",
            ".thea-response",
            # Fallback selectors
            "main",
            ".conversation",
            '[role="main"]',
        ]

        # Continue button selectors
        self.continue_selectors = [
            'button[aria-label*="Continue"]',
            'button[aria-label*="continue"]',
            'button:contains("Continue")',
            ".continue-button",
            '[data-testid="continue-button"]',
        ]

    def wait_until_complete(
        self,
        timeout: int = 120,
        stable_secs: float = 3.0,
        poll: float = 0.5,
        auto_continue: bool = True,
        max_continue_clicks: int = 1,
    ) -> ResponseWaitResult:
        """Wait until THEA response is complete and stable."""
        if not SELENIUM_AVAILABLE or not self.driver:
            print("⚠️  Selenium not available - using fallback detection")
            return self._fallback_wait(timeout)

        print(f"🔍 Waiting for response completion (timeout: {timeout}s)...")
        start_time = time.time()
        continue_clicks = 0

        while time.time() - start_time < timeout:
            try:
                # Check if response is present
                response_element = self._find_response_element()
                if not response_element:
                    print("⚠️  No response element found")
                    time.sleep(poll)
                    continue

                # Check for continue button
                if self._has_continue_button():
                    if auto_continue and continue_clicks < max_continue_clicks:
                        print("🔄 Continue button detected - clicking...")
                        if self._click_continue_button():
                            continue_clicks += 1
                            time.sleep(2)  # Wait for response to continue
                            continue
                    else:
                        print("⚠️  Continue required but not auto-clicking")
                        return ResponseWaitResult.CONTINUE_REQUIRED

                # Check response stability
                current_length = len(response_element.text)
                if current_length == self.last_response_length:
                    self.stable_count += 1
                    if self.stable_count >= int(stable_secs / poll):
                        print("✅ Response stable and complete")
                        return ResponseWaitResult.COMPLETE
                else:
                    self.stable_count = 0
                    self.last_response_length = current_length

                time.sleep(poll)

            except Exception as e:
                print(f"⚠️  Error during response detection: {e}")
                time.sleep(poll)

        print(f"⏰ Timeout after {timeout} seconds")
        return ResponseWaitResult.TIMEOUT

    def extract_response_text(self) -> str:
        """Extract the actual response text from THEA."""
        if not SELENIUM_AVAILABLE or not self.driver:
            print("⚠️  Selenium not available - using fallback extraction")
            return self._fallback_extract()

        try:
            response_element = self._find_response_element()
            if response_element:
                text = response_element.text.strip()
                if text:
                    print(f"✅ Extracted response text ({len(text)} characters)")
                    return text
                else:
                    print("⚠️  Response element found but no text content")
                    return ""
            else:
                print("⚠️  No response element found for extraction")
                return ""

        except Exception as e:
            print(f"❌ Error extracting response text: {e}")
            return ""

    def _find_response_element(self):
        """Find the response element using multiple selectors."""
        if not self.driver:
            return None

        for selector in self.response_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Return the last (most recent) element
                    return elements[-1]
            except Exception:
                continue

        return None

    def _has_continue_button(self) -> bool:
        """Check if continue button is present."""
        if not self.driver:
            return False

        for selector in self.continue_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return True
            except Exception:
                continue

        return False

    def _click_continue_button(self) -> bool:
        """Click the continue button if present."""
        if not self.driver:
            return False

        for selector in self.continue_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    element = elements[0]
                    if element.is_enabled() and element.is_displayed():
                        element.click()
                        print("✅ Continue button clicked")
                        return True
            except Exception as e:
                print(f"⚠️  Error clicking continue button: {e}")
                continue

        return False

    def _fallback_wait(self, timeout: int) -> ResponseWaitResult:
        """Fallback waiting method when Selenium is not available."""
        print("🔄 Using fallback response detection...")
        print("Please wait for THEA to finish responding, then press Enter")

        try:
            input("🎯 Press Enter when THEA has finished responding...")
            return ResponseWaitResult.COMPLETE
        except KeyboardInterrupt:
            return ResponseWaitResult.TIMEOUT

    def _fallback_extract(self) -> str:
        """Fallback text extraction when Selenium is not available."""
        print("🔄 Using fallback text extraction...")
        print("Please copy THEA's response and press Enter")

        try:
            input("📋 Copy THEA's response and press Enter...")
            # In a real implementation, this would use pyperclip or similar
            return "Fallback response text - manual extraction required"
        except KeyboardInterrupt:
            return ""


# Convenience functions for backward compatibility
def create_response_detector(driver: webdriver.Chrome | None = None) -> ResponseDetector:
    """Create a ResponseDetector instance."""
    return ResponseDetector(driver)


def wait_for_response(driver: webdriver.Chrome | None = None, timeout: int = 120) -> bool:
    """Convenience function to wait for response."""
    detector = ResponseDetector(driver)
    result = detector.wait_until_complete(timeout=timeout)
    return result == ResponseWaitResult.COMPLETE


def extract_response(driver: webdriver.Chrome | None = None) -> str:
    """Convenience function to extract response text."""
    detector = ResponseDetector(driver)
    return detector.extract_response_text()
