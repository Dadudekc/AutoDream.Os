"""
Thea Manager Profile Module - V2 Compliance
==========================================

Main profile class for Thea Manager browser interactions.
Orchestrates configuration, browser operations, response collection, and content scraping.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import time
from typing import Any

from .browser_ops import TheaBrowserOperations, TheaElementFinder
from .config import TheaConfigManager
from .content_scraper import TheaContentProcessor, TheaContentScraper
from .response_collector import TheaResponseCollector, TheaResponseMonitor

logger = logging.getLogger(__name__)


class TheaManagerProfile:
    """
    Main profile class for Thea Manager browser interactions.

    This class orchestrates all Thea Manager functionality including:
    - Configuration management
    - Browser operations
    - Response collection with advanced DOM polling
    - Content scraping and processing
    - Session management and error handling
    """

    def __init__(self, driver: Any = None):
        """Initialize Thea Manager profile with all modules."""
        # Initialize configuration
        self.config_manager = TheaConfigManager()

        # Initialize browser components (will be set up when driver is available)
        self.driver = driver
        self.browser_ops = None
        self.element_finder = None
        self.response_collector = None
        self.response_monitor = None

        # Initialize content processing
        self.content_scraper = TheaContentScraper(self.config_manager)
        self.content_processor = TheaContentProcessor(self.content_scraper)

        # Profile state
        self._initialized = False
        self._last_activity = None

        # Set up browser components if driver provided
        if driver:
            self._setup_browser_components()

    def initialize(self, driver: Any = None) -> bool:

EXAMPLE USAGE:
==============

# Basic usage example
from src.infrastructure.browser.thea_modules.profile import Profile

# Initialize and use
instance = Profile()
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Profile(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

        """
        Initialize the Thea Manager profile.

        Args:
            driver: Browser driver instance

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            if driver:
                self.driver = driver

            if not self.driver:
                logger.error("No browser driver provided for initialization")
                return False

            self._setup_browser_components()

            # Navigate to conversation
            if self.browser_ops.navigate_to_conversation():
                self._initialized = True
                self._last_activity = time.time()
                logger.info("✅ Thea Manager profile initialized successfully")
                return True
            else:
                logger.error("❌ Failed to navigate to Thea Manager conversation")
                return False

        except Exception as e:
            logger.error(f"❌ Thea Manager profile initialization failed: {e}")
            return False

    def send_message_and_wait(self, message: str, timeout: float = 120.0) -> str | None:
        """
        Send a message and wait for response.

        Args:
            message: Message to send
            timeout: Maximum time to wait for response

        Returns:
            Response text or None if failed
        """
        try:
            if not self._initialized:
                logger.error("Profile not initialized")
                return None

            # Send message
            if not self.browser_ops.send_message(message):
                logger.error("Failed to send message")
                return None

            # Wait for response to start
            if not self.response_collector.wait_for_response_start(30.0):
                logger.error("Response did not start within timeout")
                return None

            # Collect full response
            self.response_monitor.start_monitoring()
            response = self.response_collector.collect_full_response(timeout)

            if response:
                # Process and scrape content
                scraped_content = self.content_scraper.scrape_content(response)
                self._last_activity = time.time()

                logger.info(f"✅ Response received and processed ({len(response)} chars)")
                return scraped_content.content
            else:
                logger.error("❌ Failed to collect response")
                return None

        except Exception as e:
            logger.error(f"❌ Error in send_message_and_wait: {e}")
            return None

    def get_status(self) -> dict[str, Any]:
        """Get current profile status."""
        try:
            status = {
                "initialized": self._initialized,
                "last_activity": self._last_activity,
                "driver_available": self.driver is not None,
            }

            if self.driver and self.browser_ops:
                page_status = self.browser_ops.get_page_status()
                status.update(
                    {
                        "page_status": page_status,
                        "url": page_status.get("url", "unknown"),
                        "ready_for_input": page_status.get("ready_for_input", False),
                    }
                )

            if self.response_monitor:
                progress = self.response_monitor.get_progress()
                status["response_progress"] = progress

            return status

        except Exception as e:
            return {
                "initialized": self._initialized,
                "error": str(e),
                "driver_available": self.driver is not None,
            }

    def scrape_current_content(self) -> Any | None:
        """Scrape current content from the page."""
        try:
            if not self.response_collector:
                return None

            current_response = self.response_collector._extract_current_response()
            if current_response:
                return self.content_scraper.scrape_content(current_response)
            return None

        except Exception as e:
            logger.error(f"Content scraping failed: {e}")
            return None

    def validate_setup(self) -> dict[str, Any]:
        """Validate that the Thea Manager setup is correct."""
        issues = []

        # Check configuration
        config_issues = self.config_manager.validate_config()
        issues.extend(config_issues)

        # Check browser components
        if not self.driver:
            issues.append("Browser driver not initialized")

        if not self.browser_ops:
            issues.append("Browser operations not initialized")

        if not self.response_collector:
            issues.append("Response collector not initialized")

        # Check page status
        if self.browser_ops:
            page_status = self.browser_ops.get_page_status()
            if not page_status.get("ready_for_input", False):
                issues.append("Page not ready for input")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "config_valid": len(config_issues) == 0,
            "browser_ready": self.driver is not None,
            "components_initialized": all(
                [
                    self.browser_ops is not None,
                    self.response_collector is not None,
                    self.content_scraper is not None,
                ]
            ),
        }

    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            self._initialized = False
            self._last_activity = None

            # Close browser if needed
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None

            logger.info("✅ Thea Manager profile cleaned up")

        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")

    def _setup_browser_components(self) -> None:
        """Set up browser-related components."""
        if not self.driver:
            return

        # Initialize browser operations
        self.browser_ops = TheaBrowserOperations(self.driver, self.config_manager)

        # Initialize element finder
        self.element_finder = TheaElementFinder(self.driver)

        # Initialize response collector
        self.response_collector = TheaResponseCollector(self.driver)

        # Initialize response monitor
        self.response_monitor = TheaResponseMonitor(self.response_collector)

    def __repr__(self) -> str:
        """String representation of the profile."""
        status = "initialized" if self._initialized else "not initialized"
        return (
            f"TheaManagerProfile(status={status}, driver={'available' if self.driver else 'none'})"
        )
