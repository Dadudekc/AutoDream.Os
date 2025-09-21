#!/usr/bin/env python3
"""
Thea Login Handler
==================

Handles Thea/ChatGPT login with automated detection and cookie persistence.
"""

import logging
import time
from typing import Optional

from .cookie_manager import TheaCookieManager

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
    print("⚠️  Selenium not available - login handler will use fallback methods")

logger = logging.getLogger(__name__)


class TheaLoginHandler:
    """
    Handles Thea/ChatGPT login with automated detection and cookie persistence.
    """

    def __init__(
        self,
        username: Optional[str] = None,
# SECURITY: Password placeholder - replace with environment variable
        cookie_file: str = "thea_cookies.json",
        timeout: int = 30,
    ):
        """
        Initialize the Thea login handler.

        Args:
            username: ChatGPT username/email
# SECURITY: Password placeholder - replace with environment variable
            cookie_file: Path to cookie file for persistence
            timeout: Timeout for login operations
        """
        self.username = username
# SECURITY: Password placeholder - replace with environment variable
        self.timeout = timeout
        self.cookie_manager = TheaCookieManager(cookie_file)

        # Thea/ChatGPT specific URLs
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
        self.chatgpt_base_url = "https://chat.openai.com"

    def ensure_login(self, driver, allow_manual: bool = True, manual_timeout: int = 60) -> bool:
        """
        Ensure user is logged into Thea/ChatGPT.

        Args:
            driver: Selenium webdriver instance
            allow_manual: Allow manual login if automated fails
            manual_timeout: Timeout for manual login

        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info("🔐 Ensuring Thea login...")

            # Navigate to Thea page
            driver.get(self.thea_url)
            time.sleep(3)

            # Check if already logged in and on Thea page
            if self._is_logged_in(driver) and self._is_on_thea_page(driver):
                logger.info("✅ Already logged in to Thea")
                return True

            # Try cookie-based authentication
            if self.cookie_manager.has_valid_cookies():
                logger.info("🍪 Trying cookie-based login...")
                self.cookie_manager.load_cookies(driver)
                driver.refresh()
                time.sleep(3)

                if self._is_logged_in(driver):
                    # First navigate to main ChatGPT page to ensure proper authentication
                    logger.info("🔄 Navigating to main ChatGPT page to ensure authentication...")
                    driver.get("https://chatgpt.com/")
                    time.sleep(3)

                    # Check if still logged in after navigation
                    if self._is_logged_in(driver):
                        logger.info("✅ Authentication confirmed on main page")
                    else:
                        logger.warning("⚠️ Lost authentication when navigating to main page")
                        return False

                    # Check if we're on Thea page, if not navigate there
                    if self._is_on_thea_page(driver):
                        logger.info("✅ Already on Thea page")
                        return True
                    else:
                        logger.info("🔄 Logged in but not on Thea page, navigating to Thea...")
                        if self._navigate_to_thea(driver):
                            return True

            # Try automated login if credentials provided
# SECURITY: Password placeholder - replace with environment variable
                if self._automated_login(driver):
                    # Save cookies after successful login
                    self.cookie_manager.save_cookies(driver)
                    return True

            # Try manual login if allowed
            if allow_manual:
                logger.info("🔄 Attempting manual login...")
                return self._manual_login(driver, manual_timeout)

            logger.error("❌ Login failed - no credentials and manual login not allowed")
            return False

        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    def _is_logged_in(self, driver) -> bool:
        """
        Check if user is logged in to Thea/ChatGPT.

        Uses multiple indicators to detect login status.
        """
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available - cannot check login status")
            return False

        try:
            # Look for logged-in indicators (Thea/ChatGPT specific)
            logged_in_indicators = [
                "//button[contains(@data-testid, 'send-button')]",
                "//button[contains(@aria-label, 'Send')]",
                "//textarea[contains(@data-testid, 'prompt-textarea')]",
                "//textarea[contains(@placeholder, 'Message')]",
                "//div[contains(@data-testid, 'conversation-turn')]",
                "textarea[data-testid*='prompt']",
                "textarea[placeholder*='Message']",
                "//div[contains(@class, 'conversation-turn')]",
                "//div[contains(@class, 'message user-message')]",
                "//div[contains(@class, 'message assistant-message')]",
                "//button[contains(@class, 'new-chat-button')]",
                "//div[contains(@class, 'sidebar')]",
            ]

            found_indicators = []
            login_page_found = False

            for indicator in logged_in_indicators:
                try:
                    if indicator.startswith("//"):
                        elements = driver.find_elements(By.XPATH, indicator)
                    else:
                        elements = driver.find_elements(By.CSS_SELECTOR, indicator)

                    visible_elements = [elem for elem in elements if elem.is_displayed()]
                    if visible_elements:
                        found_indicators.append(f"{indicator} ({len(visible_elements)} found)")
                        logger.debug(
                            f"✅ Found login indicator: {indicator} ({len(visible_elements)} visible)"
                        )
                except Exception as e:
                    logger.debug(f"Error checking {indicator}: {e}")
                    continue

            # Check for login page indicators
            login_indicators = [
                "//button[contains(text(), 'Log in')]",
                "//button[contains(text(), 'Sign up')]",
                "//a[contains(text(), 'Log in')]",
                "//a[contains(text(), 'Sign up')]",
                "//input[@name='username']",
# SECURITY: Password placeholder - replace with environment variable
                "//input[@type='email']",
                "//div[contains(text(), 'Welcome to ChatGPT')]",
                "//div[contains(text(), 'Log in to ChatGPT')]",
                "//h1[contains(text(), 'Welcome')]",
                "//div[contains(@class, 'login')]",
                "//form",
            ]

            for indicator in login_indicators:
                try:
                    element = driver.find_element(By.XPATH, indicator)
                    if element.is_displayed():
                        logger.debug(f"🔒 Found login page indicator: {indicator}")
                        login_page_found = True
                        break
                except NoSuchElementException:
                    continue

            # Decision logic
            if login_page_found and len(found_indicators) == 0:
                logger.info(
                    "🔒 Login page detected with no logged-in indicators - user is NOT logged in"
                )
                return False

            # If we found logged-in indicators, we're likely logged in
            if len(found_indicators) > 0:
                logger.info(f"✅ Found {len(found_indicators)} logged-in indicators - user IS logged in")
                return True

            # If no clear indicators, assume not logged in
            logger.info("❓ No clear login indicators found - assuming NOT logged in")
            return False

        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False

    def _automated_login(self, driver) -> bool:
        """Perform automated login using credentials."""
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available - cannot perform automated login")
            return False

        try:
            logger.info("🤖 Attempting automated login...")
            
            # Navigate to login page
            driver.get("https://chat.openai.com/auth/login")
            time.sleep(3)

            # Find and fill username field
            username_field = WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
# SECURITY: Key placeholder - replace with environment variable
            time.sleep(1)

            # Click continue button
            continue_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            continue_button.click()
            time.sleep(3)

            # Find and fill password field
# SECURITY: Password placeholder - replace with environment variable
# SECURITY: Key placeholder - replace with environment variable
            time.sleep(1)

            # Click login button
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            time.sleep(5)

            # Check if login was successful
            if self._is_logged_in(driver):
                logger.info("✅ Automated login successful")
                return True
            else:
                logger.error("❌ Automated login failed")
                return False

        except Exception as e:
            logger.error(f"Automated login error: {e}")
            return False

    def _manual_login(self, driver, timeout: int) -> bool:
        """Allow manual login with timeout."""
        logger.info(f"👤 Manual login required - waiting {timeout} seconds...")
        logger.info("Please log in manually in the browser window")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._is_logged_in(driver):
                logger.info("✅ Manual login successful")
                return True
            time.sleep(2)
        
        logger.error("❌ Manual login timeout")
        return False

    def _is_on_thea_page(self, driver) -> bool:
        """Check if currently on Thea page."""
        try:
            current_url = driver.current_url
            return "thea-manager" in current_url or "g-67f437d96d7c81918b2dbc12f0423867" in current_url
        except Exception:
            return False

    def _navigate_to_thea(self, driver) -> bool:
        """Navigate to Thea page."""
        try:
            logger.info("🔄 Navigating to Thea page...")
            driver.get(self.thea_url)
            time.sleep(3)
            return self._is_on_thea_page(driver)
        except Exception as e:
            logger.error(f"Error navigating to Thea: {e}")
            return False

    def force_logout(self, driver) -> bool:
        """Force logout and clear cookies."""
        try:
            logger.info("🚪 Forcing logout...")
            
            # Clear cookies
            self.cookie_manager.clear_cookies()
            
            # Clear browser cookies
            if SELENIUM_AVAILABLE:
                driver.delete_all_cookies()
            
            # Navigate to logout URL
            driver.get("https://chat.openai.com/auth/logout")
            time.sleep(3)
            
            logger.info("✅ Logout completed")
            return True
            
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return False


# Factory functions (consolidated from factory.py)
def create_thea_login_handler(username=None, cookie_file="thea_cookies.json"):
    """Create a Thea login handler instance."""
    return TheaLoginHandler(username=username, cookie_file=cookie_file)


def check_thea_login_status(driver):
    """Quick check of Thea login status."""
    handler = TheaLoginHandler()
    return handler._is_logged_in(driver)


