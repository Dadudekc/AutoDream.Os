#!/usr/bin/env python3
"""
Thea Login Handler - V2 Compliant Refactored Version
====================================================

Refactored login handler using modular components to maintain V2 compliance.
Uses thea_cookie_manager.py and thea_login_detector.py for functionality.

Features:
- Automated login detection and cookie management
- Manual login fallback
- Selenium WebDriver integration
- ChatGPT/Thea specific selectors

Usage:
    from src.services.thea.thea_login_handler_refactored import TheaLoginHandler
    
# SECURITY: Password placeholder - replace with environment variable
    if handler.ensure_login(driver):
        print("Logged in successfully!")
"""

import logging
import time

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

# Import our modular components
from src.services.thea.thea_cookie_manager import TheaCookieManager
from src.services.thea.thea_login_detector import TheaLoginDetector

logger = logging.getLogger(__name__)


class TheaLoginHandler:
    """
    Handles Thea/ChatGPT login with automated detection and cookie persistence.
    
    Refactored to use modular components for V2 compliance.
    """

    def __init__(
        self,
        username: str | None = None,
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
        
        # Initialize modular components
        self.cookie_manager = TheaCookieManager(cookie_file)
        self.login_detector = TheaLoginDetector()

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
            if self.login_detector.is_logged_in(driver) and self.login_detector.is_on_thea_page(driver):
                logger.info("✅ Already logged in to Thea")
                return True

            # Try cookie-based authentication
            if self.cookie_manager.has_valid_cookies():
                logger.info("🍪 Trying cookie-based login...")
                self.cookie_manager.load_cookies(driver)
                driver.refresh()
                time.sleep(3)

                if self.login_detector.is_logged_in(driver):
                    # First navigate to main ChatGPT page to ensure proper authentication
                    logger.info("🔄 Navigating to main ChatGPT page to ensure authentication...")
                    driver.get("https://chatgpt.com/")
                    time.sleep(3)

                    # Check if still logged in after navigation
                    if self.login_detector.is_logged_in(driver):
                        logger.info("✅ Authentication confirmed on main page")
                    else:
                        logger.warning("⚠️ Lost authentication when navigating to main page")
                        return False

                    # Check if we're on Thea page, if not navigate there
                    if self.login_detector.is_on_thea_page(driver):
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
# SECURITY: Key placeholder - replace with environment variable

                # Click continue
                continue_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                continue_button.click()
                time.sleep(2)

            except TimeoutException:
                logger.warning("Continue button not found, proceeding with login")

            # Find and fill password
            try:
                password_field = driver.find_element(By.NAME, "password")
                password_field.clear()
                password_field.send_keys(os.getenv("THEA_PASSWORD", ""))
                time.sleep(1)

                # Click login
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()
                time.sleep(3)

            except TimeoutException:
                logger.warning("Password field not found")

            # Check if login successful
            if self.login_detector.is_logged_in(driver):
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
                if self.login_detector.is_logged_in(driver):
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

    def _navigate_to_thea(self, driver) -> bool:
        """Navigate to the Thea page if logged in but on wrong page."""
        try:
            logger.info("🌐 Navigating to Thea page...")

            # If we're not on Thea, navigate there
            if not self.login_detector.is_on_thea_page(driver):
                driver.get(self.thea_url)
                time.sleep(3)

            # Check if navigation was successful
            if self.login_detector.is_on_thea_page(driver):
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


# Convenience functions for easy integration
# SECURITY: Password placeholder - replace with environment variable
    """
    Create a Thea login handler with default settings.

    Args:
        username: ChatGPT username/email
# SECURITY: Password placeholder - replace with environment variable
        cookie_file: Path to cookie file

    Returns:
        TheaLoginHandler instance
    """
# SECURITY: Password placeholder - replace with environment variable


def check_thea_login_status(driver) -> bool:
    """
    Quick check of Thea login status.

    Args:
        driver: Selenium webdriver instance

    Returns:
        True if logged in, False otherwise
    """
    detector = TheaLoginDetector()
    return detector.is_logged_in(driver)


if __name__ == "__main__":
    # Example usage
    print("🐝 V2_SWARM Thea Login Handler - Refactored")
    print("=" * 50)

    # Create handler (add credentials as needed)
    handler = create_thea_login_handler()

    print("✅ Thea Login Handler created")
    print("📝 To use with credentials:")
    print(
# SECURITY: Password placeholder - replace with environment variable
    )
    print("   success = handler.ensure_login(driver)")


def create_thea_login_handler(username=None, password=None):
    """Factory function to create a TheaLoginHandler instance."""
    return TheaLoginHandler(username=username)