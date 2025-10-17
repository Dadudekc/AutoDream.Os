#!/usr/bin/env python3
"""
Thea Response Detector - Response Capture & Persistence
========================================================

Handles response detection, capture, and saving.

Author: Agent-2 (Architecture) - V2 Consolidation
License: MIT
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path

try:
    from response_detector import ResponseDetector, ResponseWaitResult

    DETECTOR_AVAILABLE = True
except ImportError:
    DETECTOR_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("⚠️  ResponseDetector not available - response capture disabled")

from .thea_config import TheaConfig

logger = logging.getLogger(__name__)


class TheaDetector:
    """
    Response detection and capture manager.

    Responsibilities:
    - Wait for Thea's response
    - Capture response text
    - Save conversations (text + screenshots)
    - Maintain response history
    """

    def __init__(self, config: TheaConfig):
        """Initialize detector."""
        self.config = config
        self.detector = None
        self._detector_initialized = False

        # Note: ResponseDetector needs a driver, so we initialize it lazily
        if not DETECTOR_AVAILABLE:
            logger.warning("⚠️  ResponseDetector module not available")

    def _ensure_detector(self, driver) -> bool:
        """
        Ensure response detector is initialized with driver.
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            bool: True if detector ready
        """
        if not DETECTOR_AVAILABLE:
            return False
            
        if self.detector is None or not self._detector_initialized:
            try:
                self.detector = ResponseDetector(driver)
                self._detector_initialized = True
                logger.info("✅ Response detector initialized")
                return True
            except Exception as e:
                logger.warning(f"⚠️  Failed to initialize detector: {e}")
                return False
        
        return True

    def wait_for_response(
        self, driver=None, timeout: int | None = None
    ) -> tuple[bool, str]:
        """
        Wait for Thea's response.

        Args:
            driver: Selenium WebDriver instance (required for initialization)
            timeout: Maximum wait time in seconds (default: config value)

        Returns:
            tuple[bool, str]: (success, response_text)
        """
        if not DETECTOR_AVAILABLE:
            logger.warning("⚠️  Response detector module not available")
            return False, ""

        if driver and not self._ensure_detector(driver):
            logger.warning("⚠️  Could not initialize response detector")
            return False, ""

        if not self.detector:
            logger.warning("⚠️  Response detector not available")
            return False, ""

        timeout = timeout or self.config.response_timeout

        try:
            logger.info(f"⏳ Waiting for response (timeout: {timeout}s)...")

            result: ResponseWaitResult = self.detector.wait_for_complete_response(
                timeout=timeout
            )

            if result.success:
                logger.info(f"✅ Response received ({result.response_length} chars)")
                return True, result.response_text
            else:
                logger.warning(f"⚠️  Response wait failed: {result.message}")
                return False, ""

        except Exception as e:
            logger.error(f"❌ Response detection error: {e}")
            return False, ""

    def capture_response(self, driver) -> str:
        """
        Capture response text from page.

        Args:
            driver: Selenium WebDriver instance

        Returns:
            str: Response text (empty if failed)
        """
        try:
            # Use detector if available
            if self.detector:
                success, response = self.wait_for_response()
                if success:
                    return response

            # Fallback: simple wait
            logger.info("⏳ Waiting for response (fallback)...")
            time.sleep(10)  # Simple wait

            # Try to extract from page
            try:
                from selenium.webdriver.common.by import By

                # Look for message elements
                messages = driver.find_elements(By.TAG_NAME, "article")
                if messages:
                    # Get last message (should be Thea's response)
                    last_message = messages[-1].text
                    logger.info(f"✅ Captured response ({len(last_message)} chars)")
                    return last_message

            except Exception as e:
                logger.debug(f"Element extraction error: {e}")

            logger.warning("⚠️  Could not capture response")
            return ""

        except Exception as e:
            logger.error(f"❌ Response capture error: {e}")
            return ""

    def save_conversation(
        self, message: str, response: str, driver=None
    ) -> dict[str, Path | None]:
        """
        Save conversation to files.

        Args:
            message: Sent message
            response: Received response
            driver: Optional driver for screenshot

        Returns:
            dict: Paths to saved files
        """
        if not self.config.save_responses:
            return {"text": None, "screenshot": None, "metadata": None}

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        saved_files = {}

        try:
            # Save text conversation
            if self.config.save_responses:
                text_file = self.config.responses_path / f"conversation_log_{timestamp}.md"
                with open(text_file, "w", encoding="utf-8") as f:
                    f.write(f"# Thea Conversation - {timestamp}\n\n")
                    f.write("## Sent Message\n\n")
                    f.write(f"{message}\n\n")
                    f.write("---\n\n")
                    f.write("## Response\n\n")
                    f.write(f"{response}\n")

                saved_files["text"] = text_file
                logger.info(f"✅ Saved conversation to {text_file}")

            # Save screenshot
            if self.config.save_screenshots and driver:
                screenshot_file = (
                    self.config.responses_path / f"thea_response_{timestamp}.png"
                )
                driver.save_screenshot(str(screenshot_file))
                saved_files["screenshot"] = screenshot_file
                logger.info(f"✅ Saved screenshot to {screenshot_file}")

            # Save metadata
            if self.config.save_metadata:
                metadata_file = (
                    self.config.responses_path / f"response_metadata_{timestamp}.json"
                )
                metadata = {
                    "timestamp": timestamp,
                    "message_length": len(message),
                    "response_length": len(response),
                    "files": {
                        "conversation": str(saved_files.get("text", "")),
                        "screenshot": str(saved_files.get("screenshot", "")),
                    },
                }

                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2)

                saved_files["metadata"] = metadata_file
                logger.info(f"✅ Saved metadata to {metadata_file}")

            return saved_files

        except Exception as e:
            logger.error(f"❌ Failed to save conversation: {e}")
            return saved_files

    def save_sent_message(self, message: str) -> Path | None:
        """
        Save sent message to file (before receiving response).

        Args:
            message: Message text

        Returns:
            Path: Path to saved file (or None if failed)
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            message_file = self.config.responses_path / f"sent_message_{timestamp}.txt"

            with open(message_file, "w", encoding="utf-8") as f:
                f.write(message)

            logger.info(f"✅ Saved sent message to {message_file}")
            return message_file

        except Exception as e:
            logger.error(f"❌ Failed to save sent message: {e}")
            return None

