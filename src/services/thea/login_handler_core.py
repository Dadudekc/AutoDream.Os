#!/usr/bin/env python3
"""
Thea Login Handler - Core Logic
===============================

Main login handler for Thea/ChatGPT authentication.
Extracted and adapted from DreamVault's authentication system.

Features:
- Automated login status detection
- Cookie-based session persistence
- Manual login fallback
- Selenium WebDriver integration
- ChatGPT/Thea specific selectors

Usage:
    from src.services.thea.login_handler import TheaLoginHandler

    handler = TheaLoginHandler(username="user@example.com", password="password")
    if handler.ensure_login(driver):
        print("Logged in successfully!")
"""

import logging
import time

# Import our modular components
from .login_handler_detection import TheaLoginDetector
from .login_handler_utils import TheaCookieManager

logger = logging.getLogger(__name__)

# Selenium availability check
try:
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class TheaLoginHandler:
    """
    Handles Thea/ChatGPT login with automated detection and cookie persistence.

    Adapted from DreamVault's authentication system for Thea communication.
    """

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        cookie_file: str = "thea_cookies.json",
        timeout: int = 30,
    ):
        """
        Initialize the Thea login handler.

        Args:
            username: ChatGPT username/email
            password: ChatGPT password
            cookie_file: Path to cookie file for persistence
            timeout: Timeout for login operations
        """
        self.username = username
        self.password = password
        self.timeout = timeout
        self.cookie_manager = TheaCookieManager(cookie_file)
        self.detector = TheaLoginDetector()

        # Thea/ChatGPT specific URLs
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager?model=gpt-5"
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
            if self.detector.is_logged_in(driver) and self._is_on_thea_page(driver):
                logger.info("✅ Already logged in to Thea")
                return True

            # Try cookie-based authentication
            if self.cookie_manager.has_valid_cookies():
                logger.info("🍪 Trying cookie-based login...")
                self.cookie_manager.load_cookies(driver)
                driver.refresh()
                time.sleep(3)

                if self.detector.is_logged_in(driver):
                    # First navigate to main ChatGPT page to ensure proper authentication
                    logger.info("🔄 Navigating to main ChatGPT page to ensure authentication...")
                    driver.get("https://chatgpt.com/")
                    time.sleep(3)

                    # Check if still logged in after navigation
                    if self.detector.is_logged_in(driver):
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
            if self.username and self.password:
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

    def _automated_login(self, driver) -> bool:
        """
        Perform automated login with credentials.

        Args:
            driver: Selenium webdriver instance

        Returns:
            True if automated login successful, False otherwise
        """
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available - cannot perform automated login")
            return False

        try:
            logger.info("🔄 Attempting automated login...")

            # Wait for login form
            wait = WebDriverWait(driver, self.timeout)

            # Find and fill username
            try:
                username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
                username_field.clear()
                username_field.send_keys(self.username)

                # Click continue
                continue_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                continue_button.click()
                time.sleep(2)

            except TimeoutException:
                logger.warning("Username field not found - may already be on password page")

            # Find and fill password
            try:
                password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
                password_field.clear()
                password_field.send_keys(self.password)

                # Click login
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()
                time.sleep(3)

            except TimeoutException:
                logger.warning("Password field not found - login flow may have changed")

            # Check if login successful
            if self.detector.is_logged_in(driver):
                logger.info("✅ Automated login successful")
                return True
            else:
                logger.warning("⚠️ Automated login failed - may need manual intervention")
                return False

        except Exception as e:
            logger.error(f"Automated login error: {e}")
            return False

    def _manual_login(self, driver, timeout: int) -> bool:
        """
        Allow manual login with timeout.

        Args:
            driver: Selenium webdriver instance
            timeout: Timeout in seconds

        Returns:
            True if manual login successful, False otherwise
        """
        try:
            logger.info(f"⏰ Manual login timeout: {timeout} seconds")
            logger.info("👤 Please log in manually in the browser...")
            logger.info("🔍 System will automatically detect when login is complete")

            start_time = time.time()
            check_interval = 2  # Check every 2 seconds

            while time.time() - start_time < timeout:
                if self.detector.is_logged_in(driver):
                    logger.info("✅ Manual login successful")
                    # Save cookies after manual login
                    self.cookie_manager.save_cookies(driver)
                    return True

                time.sleep(check_interval)
                remaining = int(timeout - (time.time() - start_time))
                if remaining % 10 == 0:  # Log every 10 seconds
                    logger.info(f"⏰ Waiting for login... {remaining} seconds remaining")

            logger.error("❌ Manual login timeout")
            return False

        except Exception as e:
            logger.error(f"Manual login error: {e}")
            return False

    def _is_on_thea_page(self, driver) -> bool:
        """Check if we're currently on the Thea page."""
        try:
            current_url = driver.current_url
            page_title = driver.title

            # Check URL contains Thea identifier
            if "g-67f437d96d7c81918b2dbc12f0423867" in current_url:
                return True

            # Check title contains Thea
            if "thea" in page_title.lower():
                return True

            return False
        except Exception:
            return False

    def _navigate_to_thea(self, driver) -> bool:
        """Navigate to the Thea page if logged in but on wrong page."""
        try:
            logger.info("🌐 Navigating to Thea page...")

            # If we're not on Thea, navigate there
            if not self._is_on_thea_page(driver):
                driver.get(self.thea_url)
                time.sleep(3)

            # Check if navigation was successful
            if self._is_on_thea_page(driver):
                logger.info("✅ Successfully navigated to Thea")
                return True
            else:
                logger.info("⚠️ Navigation to Thea may have failed")
                return False

        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return False

    def force_logout(self, driver) -> bool:
        """
        Force logout from ChatGPT.

        Args:
            driver: Selenium webdriver instance

        Returns:
            True if logout successful, False otherwise
        """
        try:
            logger.info("🚪 Forcing logout...")

            # Clear cookies
            self.cookie_manager.clear_cookies()

            # Navigate to logout if possible
            driver.get("https://chat.openai.com/auth/logout")
            time.sleep(2)

            logger.info("✅ Logout completed")
            return True

        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False

