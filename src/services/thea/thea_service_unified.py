#!/usr/bin/env python3
"""
Thea Service - Unified V2 Compliant Implementation
===================================================

Single unified implementation consolidating 25 files into one cohesive service.
Uses modular architecture with clear separation of concerns.

This is the SINGLE authoritative Thea implementation.

Author: Agent-2 (Architecture) - V2 Consolidation
License: MIT
"""

import logging
import time
from pathlib import Path

from .thea_browser import TheaBrowser
from .thea_config import TheaConfig
from .thea_cookies import TheaCookieManager
from .thea_detector import TheaDetector
from .thea_messaging import TheaMessenger

logger = logging.getLogger(__name__)


class TheaService:
    """
    Unified Thea communication service.

    Orchestrates all Thea operations through modular components:
    - Browser: Lifecycle and navigation (TheaBrowser)
    - Cookies: Authentication and session (TheaCookieManager)
    - Messenger: PyAutoGUI message sending (TheaMessenger)
    - Detector: Response capture and saving (TheaDetector)

    This is the SINGLE authoritative Thea implementation replacing 25+ files.
    """

    def __init__(
        self,
        cookie_file: str = "thea_cookies.json",
        headless: bool = False,
        config: TheaConfig | None = None,
    ):
        """
        Initialize Thea service.

        Args:
            cookie_file: Path to cookie storage file
            headless: Run browser in headless mode
            config: Optional custom configuration
        """
        # Configuration
        self.config = config or TheaConfig()
        self.config.cookie_file = cookie_file
        self.config.headless = headless

        # Initialize components
        self.browser = TheaBrowser(self.config)
        self.cookies = TheaCookieManager(self.config.cookie_file)
        self.messenger = TheaMessenger(self.config)
        self.detector = TheaDetector(self.config)

        logger.info("✅ Thea service initialized (unified implementation)")

    def ensure_login(self) -> bool:
        """
        Ensure logged in to Thea Manager using proven cookie pattern.

        CRITICAL PATTERN:
        1. Navigate to domain FIRST (required for cookie loading!)
        2. Load cookies into browser
        3. Navigate to Thea with cookies applied

        Returns:
            bool: True if logged in successfully
        """
        try:
            # Start browser if not running
            if not self.browser.is_ready():
                if not self.browser.start():
                    logger.error("❌ Failed to start browser")
                    return False

            # STEP 1: Navigate to domain FIRST (required for cookie loading!)
            if not self.browser.navigate_to_domain():
                logger.error("❌ Failed to navigate to domain")
                return False

            # STEP 2: Load cookies if available
            if self.cookies.has_valid_cookies():
                logger.info("🍪 Loading saved cookies...")
                if self.cookies.load_cookies(self.browser.driver):
                    logger.info("✅ Cookies loaded successfully")
                    
                    # CRITICAL: Refresh to apply cookies!
                    logger.info("🔄 Refreshing to apply cookies...")
                    self.browser.refresh()
                else:
                    logger.warning("⚠️  Cookie loading failed, may need manual login")

            # STEP 3: Navigate to Thea (with cookies applied)
            if not self.browser.navigate_to_thea():
                logger.error("❌ Failed to navigate to Thea")
                return False

            # Check if logged in
            if self.browser.is_logged_in():
                logger.info("✅ Already logged in to Thea")
                return True

            # Manual login required
            logger.warning("⚠️  Manual login required")
            logger.info("Please log in to ChatGPT in the browser window...")
            logger.info(f"Waiting {self.config.login_timeout} seconds...")

            time.sleep(self.config.login_timeout)

            # Check again after wait
            if self.browser.is_logged_in():
                # Save cookies for future use
                self.cookies.save_cookies(self.browser.driver)
                logger.info("✅ Login successful, cookies saved")
                return True

            logger.error("❌ Login timeout - please try again")
            return False

        except Exception as e:
            logger.error(f"❌ Login error: {e}")
            return False

    def send_message(self, message: str, wait_for_response: bool = True) -> str | None:
        """
        Send message to Thea and optionally wait for response.

        Args:
            message: Message to send
            wait_for_response: Whether to wait for response

        Returns:
            Response text if wait_for_response=True, else None
        """
        try:
            # Ensure logged in
            if not self.ensure_login():
                logger.error("❌ Login failed, cannot send message")
                return None

            # Send message via PyAutoGUI
            logger.info(f"📤 Sending message ({len(message)} chars)...")

            if not self.messenger.send_and_submit(message):
                logger.error("❌ Failed to send message")
                return None

            logger.info("✅ Message sent successfully")

            # Save sent message
            self.detector.save_sent_message(message)

            # Wait for response if requested
            if wait_for_response:
                success, response = self.detector.wait_for_response(
                    driver=self.browser.driver
                )
                if success:
                    logger.info(f"✅ Response received ({len(response)} chars)")
                    return response
                else:
                    logger.warning("⚠️  No response received")
                    return None

            return None

        except Exception as e:
            logger.error(f"❌ Send message failed: {e}")
            return None

    def communicate(self, message: str, save: bool = True) -> dict:
        """
        Complete communication cycle: send message and get response.

        Args:
            message: Message to send
            save: Whether to save conversation

        Returns:
            dict with 'success', 'message', 'response', 'file' keys
        """
        result = {
            "success": False,
            "message": message,
            "response": "",
            "file": None,
            "files": {},
        }

        try:
            # Send message and wait for response
            response = self.send_message(message, wait_for_response=True)

            if response:
                result["response"] = response
                result["success"] = True

                # Save conversation if requested
                if save:
                    saved_files = self.detector.save_conversation(
                        message, response, self.browser.driver
                    )
                    result["files"] = saved_files

                    # Set primary file (text conversation)
                    if "text" in saved_files:
                        result["file"] = str(saved_files["text"])

                logger.info("✅ Communication successful")
            else:
                logger.warning("⚠️  Communication failed - no response")

            return result

        except Exception as e:
            logger.error(f"❌ Communication error: {e}")
            result["response"] = f"Error: {e}"
            return result

    def cleanup(self):
        """Clean up resources."""
        self.browser.cleanup()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


# Factory functions
def create_thea_service(
    cookie_file: str = "thea_cookies.json", headless: bool = False
) -> TheaService:
    """
    Create Thea service instance.

    Args:
        cookie_file: Path to cookie storage file
        headless: Run browser in headless mode

    Returns:
        TheaService instance
    """
    return TheaService(cookie_file=cookie_file, headless=headless)


__all__ = ["TheaService", "create_thea_service", "TheaConfig"]

