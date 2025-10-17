#!/usr/bin/env python3
"""
Thea Browser Manager - Browser Lifecycle & Navigation
======================================================

Handles browser initialization, navigation, and lifecycle management.

Author: Agent-2 (Architecture) - V2 Consolidation
License: MIT
"""

import logging
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Try undetected-chromedriver for Cloudflare bypass
try:
    import undetected_chromedriver as uc

    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

from .thea_config import TheaConfig

logger = logging.getLogger(__name__)


class TheaBrowser:
    """
    Browser lifecycle manager.

    Responsibilities:
    - Initialize Chrome WebDriver
    - Navigate to ChatGPT/Thea
    - Detect login status
    - Cleanup resources
    """

    def __init__(self, config: TheaConfig):
        """Initialize browser manager."""
        self.config = config
        self.driver = None

    def start(self) -> bool:
        """
        Start browser with anti-detection settings.

        Uses undetected-chromedriver if available (bypasses Cloudflare).

        Returns:
            bool: True if browser started successfully
        """
        if not SELENIUM_AVAILABLE:
            logger.error("❌ Selenium not available")
            return False

        try:
            logger.info("🚀 Starting browser...")

            # Try undetected-chromedriver first (best for Cloudflare)
            if UNDETECTED_AVAILABLE:
                logger.info("🔐 Using undetected-chromedriver (Cloudflare bypass)")
                
                options = uc.ChromeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument(
                    f"--window-size={self.config.window_width},{self.config.window_height}"
                )

                if self.config.headless:
                    logger.warning("⚠️  Headless mode may be detected by Cloudflare")
                    options.add_argument("--headless=new")

                self.driver = uc.Chrome(
                    options=options,
                    use_subprocess=True,
                    driver_executable_path=None,  # Auto-download
                )

                logger.info("✅ Undetected browser started (Cloudflare bypass enabled)")
                return True

            # Fallback to standard Chrome
            logger.info("⚠️  Using standard Chrome (may be blocked by Cloudflare)")
            logger.info("💡 Install undetected-chromedriver for better results:")
            logger.info("   pip install undetected-chromedriver")

            options = Options()

            # Headless mode
            if self.config.headless:
                options.add_argument("--headless=new")

            # Standard options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument(
                f"--window-size={self.config.window_width},{self.config.window_height}"
            )

            # Anti-detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            # Create driver
            self.driver = webdriver.Chrome(options=options)

            logger.info("✅ Standard browser started")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start browser: {e}")
            return False

    def navigate_to_domain(self) -> bool:
        """
        Navigate to ChatGPT base domain.

        CRITICAL: Must be called BEFORE loading cookies!

        Returns:
            bool: True if navigation successful
        """
        if not self.driver:
            logger.error("❌ Browser not started")
            return False

        try:
            logger.info("🌐 Navigating to ChatGPT domain...")
            self.driver.get(self.config.chatgpt_base_url)
            time.sleep(self.config.navigation_delay)
            logger.info("✅ Domain navigation complete")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to navigate to domain: {e}")
            return False

    def navigate_to_thea(self) -> bool:
        """
        Navigate to Thea Manager.

        Should be called AFTER cookies are loaded.

        Returns:
            bool: True if navigation successful
        """
        if not self.driver:
            logger.error("❌ Browser not started")
            return False

        try:
            logger.info("🌐 Navigating to Thea Manager...")
            self.driver.get(self.config.thea_url)
            time.sleep(self.config.navigation_delay)
            logger.info("✅ Thea navigation complete")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to navigate to Thea: {e}")
            return False

    def refresh(self) -> bool:
        """
        Refresh current page.

        Returns:
            bool: True if refresh successful
        """
        if not self.driver:
            return False

        try:
            self.driver.refresh()
            time.sleep(self.config.navigation_delay)
            return True

        except Exception as e:
            logger.error(f"❌ Failed to refresh: {e}")
            return False

    def is_logged_in(self) -> bool:
        """
        Check if user is logged in to ChatGPT/Thea.

        Returns:
            bool: True if logged in
        """
        if not self.driver:
            return False

        try:
            # Look for VISIBLE textarea (indicates logged in)
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            visible_textareas = [ta for ta in textareas if ta.is_displayed()]
            
            if visible_textareas:
                logger.debug(f"✅ Found {len(visible_textareas)} visible textarea(s) - logged in")
                return True

            # Look for send button (alternative login indicator)
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                try:
                    if btn.is_displayed() and "send" in str(btn.text or "").lower():
                        logger.debug("✅ Found send button - logged in")
                        return True
                except:
                    continue

            # Look for login buttons (indicates NOT logged in)
            for button in buttons:
                try:
                    text = button.text.lower()
                    if any(word in text for word in ["log in", "sign in", "sign up"]):
                        logger.debug(f"❌ Found login button: '{text}' - not logged in")
                        return False
                except:
                    continue

            # If no clear indicators, assume not logged in
            logger.debug("⚠️  No clear login indicators found")
            return False

        except Exception as e:
            logger.debug(f"Login check error: {e}")
            return False

    def is_ready(self) -> bool:
        """
        Check if browser is ready for operations.

        Returns:
            bool: True if ready
        """
        return self.driver is not None

    def cleanup(self):
        """Clean up browser resources."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Browser closed")
            except Exception as e:
                logger.error(f"⚠️  Error closing browser: {e}")
            finally:
                self.driver = None

