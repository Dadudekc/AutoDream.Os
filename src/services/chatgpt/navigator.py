"""
ChatGPT Navigator - V2 Compliant
===============================

Browser navigation for ChatGPT conversations using Playwright.
Extends V2's existing browser infrastructure for ChatGPT automation.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Browser Automation Specialist
License: MIT
"""

import time
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Optional dependencies for browser automation
try:
    from playwright.async_api import BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logging.warning("Playwright not available - ChatGPT navigation disabled")

# V2 Integration imports
try:
    from ...infrastructure.browser import UnifiedBrowserService
    from ...core.unified_config import get_unified_config
    from ...core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)
    
    class UnifiedBrowserService:
        pass


class ChatGPTNavigator:
    """
    ChatGPT browser navigation helper.
    
    Provides navigation capabilities for ChatGPT conversations
    with integration to V2's browser infrastructure.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize ChatGPT navigator.
        
        Args:
            config: Configuration dictionary (uses config/chatgpt.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Navigation settings
        nav_config = self.config.get('navigation', {})
        self.default_url = nav_config.get('default_url', 'https://chat.openai.com/')
        self.timeout = nav_config.get('timeout', 60000)
        self.wait_for_selector = nav_config.get('wait_for_selector', 'textarea')
        self.retry_attempts = nav_config.get('retry_attempts', 3)
        self.retry_delay = nav_config.get('retry_delay', 2.0)
        
        # Browser settings
        browser_config = self.config.get('browser', {})
        self.headless = browser_config.get('headless', False)
        self.user_data_dir = browser_config.get('user_data_dir', 'runtime/browser_profiles/chatgpt')
        
        # State
        self._page: Optional[Page] = None
        self._context: Optional[BrowserContext] = None
        self.browser_service = None
        
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.warning("ChatGPT navigation disabled - Playwright not available")

    async def navigate_to_chat(
        self,
        context: Optional[BrowserContext] = None,
        conversation_url: Optional[str] = None,
    ) -> Optional[Page]:
        """
        Navigate to ChatGPT conversation and wait until ready.
        
        Args:
            context: Browser context (creates new if None)
            conversation_url: Specific conversation URL (uses default if None)
            
        Returns:
            Playwright page object, or None if failed
        """
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.error("ChatGPT navigation failed: Playwright not available")
            return None
        
        try:
            url = conversation_url or self.default_url
            self.logger.info(f"Navigating to ChatGPT: {url}")
            
            # Create or use provided context
            if context:
                self._context = context
            else:
                self._context = await self._create_browser_context()
            
            if not self._context:
                self.logger.error("Failed to create browser context")
                return None
            
            # Create new page
            self._page = await self._context.new_page()
            
            # Navigate to URL with retries
            for attempt in range(self.retry_attempts):
                try:
                    await self._page.goto(url, timeout=self.timeout)
                    self.logger.info(f"Successfully navigated to {url}")
                    break
                except Exception as e:
                    self.logger.warning(f"Navigation attempt {attempt + 1} failed: {e}")
                    if attempt < self.retry_attempts - 1:
                        await asyncio.sleep(self.retry_delay)
                    else:
                        raise
            
            # Wait for ChatGPT interface to be ready
            await self._wait_for_ready()
            
            self.logger.info("ChatGPT interface ready")
            return self._page
            
        except Exception as e:
            self.logger.error(f"ChatGPT navigation failed: {e}")
            return None

    async def _create_browser_context(self) -> Optional[BrowserContext]:
        """Create browser context with ChatGPT-specific settings."""
        try:
            # Use V2's browser service if available
            if hasattr(self, 'browser_service') and self.browser_service:
                return await self.browser_service.create_context(
                    user_data_dir=self.user_data_dir,
                    headless=self.headless
                )
            
            # Fallback to direct Playwright usage
            from playwright.async_api import async_playwright
            
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(
                headless=self.headless,
                user_data_dir=self.user_data_dir
            )
            
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent=self.config.get('browser', {}).get('user_agent')
            )
            
            return context
            
        except Exception as e:
            self.logger.error(f"Failed to create browser context: {e}")
            return None

    async def _wait_for_ready(self) -> None:
        """Wait for ChatGPT interface to be ready."""
        try:
            # Wait for message input textarea
            await self._page.wait_for_selector(
                self.wait_for_selector,
                timeout=self.timeout
            )
            
            # Additional wait for interface to stabilize
            await asyncio.sleep(1)
            
            self.logger.info("ChatGPT interface is ready")
            
        except Exception as e:
            self.logger.error(f"Failed to wait for ChatGPT interface: {e}")
            raise

    def get_active_page(self) -> Optional[Page]:
        """
        Get the active page created by navigate_to_chat.
        
        Returns:
            Active page object, or None if not available
        """
        if self._page is None:
            self.logger.warning("No active page - call navigate_to_chat first")
        return self._page

    async def send_message(self, message: str, wait_for_response: bool = True) -> Optional[str]:
        """
        Send a message to ChatGPT.
        
        Args:
            message: Message text to send
            wait_for_response: Whether to wait for response
            
        Returns:
            Response text if wait_for_response is True, None otherwise
        """
        if not self._page:
            self.logger.error("No active page - call navigate_to_chat first")
            return None
        
        try:
            # Find and focus the textarea
            textarea = await self._page.query_selector(self.wait_for_selector)
            if not textarea:
                self.logger.error("Could not find message input textarea")
                return None
            
            # Clear and type message
            await textarea.click()
            await textarea.fill(message)
            
            # Send message (usually Enter key)
            await textarea.press('Enter')
            
            self.logger.info(f"Message sent: {message[:50]}...")
            
            if wait_for_response:
                return await self._wait_for_response()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return None

    async def _wait_for_response(self, timeout: int = 30000) -> Optional[str]:
        """Wait for ChatGPT response."""
        try:
            # Wait for response to appear (simplified detection)
            # In a real implementation, this would be more sophisticated
            await asyncio.sleep(3)  # Give ChatGPT time to respond
            
            # Look for response elements
            response_elements = await self._page.query_selector_all('[data-message-author-role="assistant"]')
            
            if response_elements:
                # Get the latest response
                latest_response = response_elements[-1]
                response_text = await latest_response.inner_text()
                return response_text.strip()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to wait for response: {e}")
            return None

    async def close(self) -> None:
        """Close the browser context and page."""
        try:
            if self._page:
                await self._page.close()
                self._page = None
            
            if self._context:
                await self._context.close()
                self._context = None
            
            self.logger.info("ChatGPT navigator closed")
            
        except Exception as e:
            self.logger.error(f"Failed to close navigator: {e}")

    def get_navigation_info(self) -> Dict[str, Any]:
        """Get information about navigation capabilities."""
        return {
            "playwright_available": PLAYWRIGHT_AVAILABLE,
            "default_url": self.default_url,
            "timeout": self.timeout,
            "wait_for_selector": self.wait_for_selector,
            "retry_attempts": self.retry_attempts,
            "retry_delay": self.retry_delay,
            "headless": self.headless,
            "user_data_dir": self.user_data_dir,
            "has_active_page": self._page is not None,
            "has_active_context": self._context is not None,
        }
