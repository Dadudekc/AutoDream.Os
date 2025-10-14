"""
Navigator Messaging Helper
===========================

Message sending operations extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import asyncio
import logging

try:
    from playwright.async_api import Page

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = None

logger = logging.getLogger(__name__)


class NavigatorMessaging:
    """Handles message sending and response waiting for ChatGPT navigator."""

    @staticmethod
    async def send_message_to_page(
        page: Page, message: str, wait_for_response: bool, wait_for_selector: str, logger_instance
    ) -> str | None:
        """
        Send message to ChatGPT and optionally wait for response.

        Args:
            page: Playwright page object
            message: Message to send
            wait_for_response: Whether to wait for response
            wait_for_selector: Selector for input element
            logger_instance: Logger instance

        Returns:
            Response text if wait_for_response=True, None otherwise
        """
        if not PLAYWRIGHT_AVAILABLE or not page:
            logger_instance.error(
                "Cannot send message - Playwright not available or page not ready"
            )
            return None

        try:
            # Find input textarea
            textarea = await page.wait_for_selector(wait_for_selector, timeout=5000)

            if not textarea:
                logger_instance.error(f"Input element not found: {wait_for_selector}")
                return None

            # Type message
            await textarea.fill(message)
            logger_instance.info(f"Message typed: {message[:50]}...")

            # Send message (usually Enter key or button click)
            await page.keyboard.press("Enter")
            logger_instance.info("Message sent")

            # Wait for response if requested
            if wait_for_response:
                return await NavigatorMessaging.wait_for_response(page, logger_instance)

            return None

        except Exception as e:
            logger_instance.error(f"Failed to send message: {e}")
            return None

    @staticmethod
    async def wait_for_response(page: Page, logger_instance, timeout: int = 30000) -> str | None:
        """
        Wait for ChatGPT response.

        Args:
            page: Playwright page object
            logger_instance: Logger instance
            timeout: Max wait time in milliseconds

        Returns:
            Response text or None if failed
        """
        try:
            # Wait for response to appear
            # This is a simplified implementation - actual logic would detect response completion
            await asyncio.sleep(2)

            # Get last message (response)
            messages = await page.query_selector_all("[data-message-author-role]")

            if messages:
                last_message = messages[-1]
                text_element = await last_message.query_selector("[data-message-text]")

                if text_element:
                    response_text = await text_element.inner_text()
                    logger_instance.info(f"Received response: {response_text[:100]}...")
                    return response_text

            logger_instance.warning("No response detected")
            return None

        except Exception as e:
            logger_instance.error(f"Failed to wait for response: {e}")
            return None
