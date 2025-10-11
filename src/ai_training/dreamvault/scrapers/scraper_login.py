"""ChatGPT Scraper Login Logic - V2 Compliance | Agent-5"""

import logging
import time

logger = logging.getLogger(__name__)


class ScraperLoginHelper:
    """Handles login and authentication logic."""

    @staticmethod
    def ensure_login_with_cookies(
        driver, cookie_manager, login_handler, allow_manual=True, manual_timeout=60
    ) -> bool:
        """Ensure user is logged into ChatGPT with cookie handling."""
        try:
            # Ensure on ChatGPT domain before loading cookies
            if not driver.current_url.startswith("https://chat.openai.com"):
                logger.info("🌐 Navigating to ChatGPT before loading cookies...")
                driver.get("https://chat.openai.com")
                time.sleep(3)
            # Try to load cookies first
            if cookie_manager.has_valid_cookies():
                logger.info("🍪 Found saved cookies, attempting auto-login...")
                cookie_manager.load_cookies(driver)
                time.sleep(3)
                logger.info("🔄 Refreshing page to apply cookies...")
                driver.refresh()
                time.sleep(3)
                logger.info("🔍 Testing if cookies still work...")
                if login_handler._is_logged_in(driver):
                    logger.info("✅ ✨ SUCCESS! Cookies work! Auto-login successful!")
                    if ScraperLoginHelper._handle_workspace_selection(driver):
                        logger.info("✅ Workspace selection handled")
                    logger.info("⚡ Skipping manual login - proceeding directly to scraping...")
                    return True
                else:
                    logger.warning("⚠️ Cookies expired or invalid")
                    logger.info("🔄 Falling back to manual login...")
            else:
                logger.info("📝 No saved cookies found")
                logger.info("👤 Will need manual login this time...")
            # Perform manual login
            logger.info("🔐 Starting manual login process...")
            if login_handler.ensure_login(driver, allow_manual, manual_timeout):
                cookie_manager.save_cookies(driver)
                logger.info("✅ Login successful! Cookies saved for next time.")
                logger.info("💡 Next run will auto-login with these cookies!")
                return True
            else:
                logger.error("❌ Login failed")
                return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    @staticmethod
    def _handle_workspace_selection(driver) -> bool:
        """Handle workspace selection modal."""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            wait = WebDriverWait(driver, 5)
            modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))
            logger.info("📋 Workspace selection modal detected")
            buttons = modal.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if "stay" in button.text.lower() or "personal" in button.text.lower():
                    button.click()
                    logger.info("✅ Selected personal workspace")
                    time.sleep(2)
                    return True
            logger.warning("⚠️ Could not find workspace selection button")
            return False
        except:
            return True
