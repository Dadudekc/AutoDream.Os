"""
ChatGPT Scraper for DreamVault - V2 Compliant
Integrated scraper - Agent-5 (V2 refactor) | DreamVault team (original)
"""

import logging
import time
from collections.abc import Callable
from pathlib import Path

# Selenium imports
from selenium.webdriver.common.by import By

from .adaptive_extractor import AdaptiveExtractor
from .browser_manager import BrowserManager
from .conversation_extractor import ConversationExtractor
from .cookie_manager import CookieManager
from .login_handler import LoginHandler
from .scraper_conversation_methods import ScraperConversationMethods
from .scraper_extraction import ScraperExtraction
from .scraper_login import ScraperLoginHelper
from .scraper_progress import ScraperProgressTracker

logger = logging.getLogger(__name__)


class ChatGPTScraper:
    """
    Integrated ChatGPT scraper with all essential features:
    Cookie persistence, manual login, rate limiting, model selection,
    conversation extraction, resume functionality.
    """

    def __init__(
        self,
        headless: bool = False,
        use_undetected: bool = True,
        username: str | None = None,
        password: str | None = None,
        totp_secret: str | None = None,
        cookie_file: str | None = None,
        rate_limit_delay: float = 2.0,
        progress_file: str = "data/scraper_progress.json",
    ):
        """Initialize the ChatGPT scraper."""
        # Initialize components
        self.browser_manager = BrowserManager(headless=headless, use_undetected=use_undetected)
        self.cookie_manager = CookieManager(cookie_file)
        self.login_handler = LoginHandler(username, password, totp_secret)
        self.conversation_extractor = ConversationExtractor()
        self.adaptive_extractor = AdaptiveExtractor()

        # Configuration
        self.rate_limit_delay = rate_limit_delay
        self.driver = None
        self.progress_file = progress_file

        # Rate limiting state
        self.last_request_time = 0
        self.request_count = 0

        # Progress tracking
        self.progress_tracker = ScraperProgressTracker(progress_file)

        logger.info("✅ ChatGPT Scraper initialized")

    def __enter__(self):
        """Context manager entry."""
        self.start_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_driver()

    def start_driver(self) -> bool:
        """Start the web driver."""
        try:
            self.driver = self.browser_manager.create_driver()
            if self.driver:
                logger.info("✅ Driver started successfully")
                # Navigate to ChatGPT to initialize the driver properly
                self.driver.get("https://chat.openai.com")
                time.sleep(2)  # Give driver time to fully initialize
                logger.info("✅ Driver initialized and navigated to ChatGPT")
                return True
            else:
                logger.error("❌ Failed to start driver")
                return False
        except Exception as e:
            logger.error(f"Failed to start driver: {e}")
            return False

    def close_driver(self):
        """Close the web driver."""
        if self.driver:
            self.browser_manager.close_driver()
            self.driver = None
            logger.info("✅ Driver closed")

    def ensure_login(self, allow_manual: bool = True, manual_timeout: int = 60) -> bool:
        """Ensure user is logged into ChatGPT."""
        return ScraperLoginHelper.ensure_login_with_cookies(
            self.driver, self.cookie_manager, self.login_handler, allow_manual, manual_timeout
        )

    def _rate_limit(self):
        """Apply rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_count += 1

    def select_model(self, model: str = "") -> bool:
        """Select a specific ChatGPT model."""
        if not model:
            logger.info("No specific model selected, using default")
            return True

        try:
            logger.info(f"🤖 Selecting model: {model}")

            # Navigate to ChatGPT
            self.driver.get("https://chat.openai.com")
            time.sleep(3)

            # Look for model selector
            model_selectors = [
                f"//button[contains(text(), '{model}')]",
                f"//div[contains(text(), '{model}')]",
                "//button[contains(@data-testid, 'model-selector')]",
            ]

            for selector in model_selectors:
                try:
                    element = self.driver.find_element_by_xpath(selector)
                    if element.is_displayed():
                        element.click()
                        time.sleep(2)
                        logger.info(f"✅ Model {model} selected")
                        return True
                except:
                    continue

            logger.warning(f"⚠️ Could not select model {model}, using default")
            return False

        except Exception as e:
            logger.error(f"Model selection error: {e}")
            return False

    def _handle_workspace_selection(self) -> bool:
        """Handle the workspace selection modal that appears after login."""
        try:
            logger.info("🔍 Checking for workspace selection modal...")

            # Wait a moment for modal to appear
            time.sleep(2)

            # Look for workspace selection modal
            workspace_selectors = [
                "//button[contains(text(), 'Personal account')]",
                "//button[contains(@class, '__menu-item') and contains(text(), 'Personal account')]",
                "//div[contains(text(), 'Select a workspace')]//following-sibling::*//button[contains(text(), 'Personal account')]",
                "//button[@data-state='off'][@role='radio'][contains(@class, '__menu-item')]",
            ]

            for selector in workspace_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        logger.info(
                            f"✅ Found workspace selection button with selector: {selector}"
                        )
                        button = elements[0]

                        # Click the Personal account button
                        logger.info("🖱️ Clicking 'Personal account' button...")
                        self.driver.execute_script("arguments[0].click();", button)
                        time.sleep(3)  # Wait for modal to close

                        logger.info("✅ Workspace selection completed")
                        return True

                except Exception as e:
                    logger.debug(f"Selector failed: {selector} - {e}")
                    continue

            logger.info("ℹ️ No workspace selection modal found (or already handled)")
            return True

        except Exception as e:
            logger.warning(f"Failed to handle workspace selection: {e}")
            return False

    def get_conversation_list(
        self, progress_callback: Callable | None = None
    ) -> list[dict[str, str]]:
        """Get list of available conversations with self-healing."""
        try:
            self._rate_limit()

            # Try adaptive extractor first (self-healing)
            logger.info("🔄 Using adaptive extractor for self-healing...")
            conversations = self.adaptive_extractor.get_conversation_list(
                self.driver, progress_callback
            )

            if conversations:
                logger.info(f"✅ Adaptive extractor found {len(conversations)} conversations")
                return conversations

            # Fallback to original extractor
            logger.warning("🔄 Adaptive extractor failed, trying original extractor...")
            return self.conversation_extractor.get_conversation_list(self.driver, progress_callback)

        except Exception as e:
            logger.error(f"Failed to get conversation list: {e}")
            return []

    def extract_conversation(
        self,
        conversation_url: str,
        output_dir: str = "data/raw",
        chronological_number: int | None = None,
    ) -> bool:
        """Extract a single conversation."""
        try:
            self._rate_limit()

            # Create output directory
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # Enter conversation
            if not self.conversation_extractor.enter_conversation(self.driver, conversation_url):
                return False

            # Extract content
            conversation_data = self.conversation_extractor.get_conversation_content(self.driver)

            # Generate filename with chronological number
            if chronological_number:
                filename = f"conversation_{chronological_number}.json"
                logger.info(f"📅 Saving as conversation #{chronological_number} chronologically")
            else:
                # Fallback to original method if no chronological number provided
                conversation_id = (
                    conversation_url.split("/c/")[-1]
                    if "/c/" in conversation_url
                    else f"conv_{int(time.time())}"
                )
                filename = f"{conversation_id}.json"

            output_file = Path(output_dir) / filename

            # Save conversation
            if self.conversation_extractor.save_conversation(conversation_data, str(output_file)):
                logger.info(f"✅ Extracted conversation: {filename}")
                return True
            else:
                logger.error(f"❌ Failed to save conversation: {filename}")
                return False

        except Exception as e:
            logger.error(f"Failed to extract conversation: {e}")
            return False

    def extract_all_conversations_smart(
        self,
        limit: int | None = None,
        output_dir: str = "data/raw",
        progress_callback: Callable | None = None,
        skip_processed: bool = True,
    ) -> dict[str, int]:
        """SMART extraction: Count first, extract as we go, reverse numbering at end."""
        return ScraperConversationMethods.extract_all_smart(
            self, limit, output_dir, progress_callback, skip_processed
        )

    def _count_total_conversations(self) -> int:
        """Quickly count total conversations with fast scrolling."""
        try:
            logger.info("🔍 Fast counting conversations...")

            # Use adaptive extractor for fast counting
            conversations = self.adaptive_extractor.get_conversation_list(self.driver)
            total_count = len(conversations)

            logger.info(f"📊 Fast count complete: {total_count} conversations")
            return total_count

        except Exception as e:
            logger.error(f"Failed to count conversations: {e}")
            return 0

    def _get_conversations_with_smart_extraction(
        self,
        total_count: int,
        output_dir: str,
        progress_callback: Callable | None,
        skip_processed: bool,
    ) -> list[dict]:
        """Extract conversations as we discover them (much faster)."""
        try:
            logger.info("⚡ Smart extraction: processing conversations as we find them...")

            # Get conversation list (this will scroll and find all)
            conversations = self.adaptive_extractor.get_conversation_list(self.driver)

            if not conversations:
                logger.warning("No conversations found")
                return []

            # Limit if specified
            if total_count and len(conversations) > total_count:
                conversations = conversations[:total_count]

            logger.info(f"📋 Processing {len(conversations)} conversations...")

            # Extract each conversation immediately
            extracted_count = 0
            for i, conversation in enumerate(conversations):
                try:
                    # Skip if already processed
                    if skip_processed and self._is_conversation_processed(conversation):
                        continue

                    # Extract immediately (no waiting)
                    logger.info(
                        f"📝 Extracting conversation {i+1}/{len(conversations)}: {conversation.get('title', 'Unknown')}"
                    )

                    if self.extract_conversation(conversation["url"], output_dir, i + 1):
                        extracted_count += 1
                        self._mark_conversation_processed(conversation, success=True)
                    else:
                        self._mark_conversation_processed(conversation, success=False)

                    if progress_callback:
                        progress_callback(i + 1, len(conversations))

                except Exception as e:
                    logger.error(f"Error extracting conversation {i+1}: {e}")
                    self._mark_conversation_processed(conversation, success=False)

            logger.info(f"✅ Smart extraction complete: {extracted_count} conversations extracted")
            return conversations

        except Exception as e:
            logger.error(f"Smart extraction failed: {e}")
            return []

    def _reverse_file_numbering(self, output_dir: str, total_count: int):
        """Reverse file numbering so conversation_1 = oldest, conversation_N = newest."""
        ScraperExtraction.reverse_file_numbering(output_dir, total_count)

    def extract_all_conversations(
        self,
        limit: int | None = None,
        output_dir: str = "data/raw",
        progress_callback: Callable | None = None,
        skip_processed: bool = True,
    ) -> dict[str, int]:
        """Extract all available conversations with resume functionality."""
        return ScraperConversationMethods.extract_all_standard(
            self, limit, output_dir, progress_callback, skip_processed
        )

    def get_rate_limit_info(self) -> dict[str, any]:
        """Get current rate limiting information."""
        return {
            "request_count": self.request_count,
            "rate_limit_delay": self.rate_limit_delay,
            "last_request_time": self.last_request_time,
        }

    def get_adaptive_health_status(self) -> dict[str, any]:
        """Get health status of the adaptive extractor."""
        return self.adaptive_extractor.get_health_status()

    def _is_conversation_processed(self, conversation: dict) -> bool:
        """Check if conversation has already been processed."""
        return self.progress_tracker._is_conversation_processed(conversation)

    def _mark_conversation_processed(self, conversation: dict, success: bool = True):
        """Mark conversation as processed."""
        self.progress_tracker._mark_conversation_processed(conversation, success)

    def reset_progress(self):
        """Reset progress tracking."""
        self.progress_tracker.reset_progress()

    def get_progress_stats(self) -> dict[str, any]:
        """Get progress statistics."""
        return self.progress_tracker.get_progress_stats()
