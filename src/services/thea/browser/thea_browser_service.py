import logging
logger = logging.getLogger(__name__)
"""
Thea Browser Service - V2 Compliant Browser Management
=======================================================

Handles browser initialization, navigation, and automation for Thea services.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""
from contextlib import contextmanager
from enum import Enum
from typing import Any
from ...thea.config.thea_config import TheaConfig


class BrowserMode(Enum):
    """Browser automation modes."""
    SELENIUM = 'selenium'
    MANUAL = 'manual'


class TheaBrowserService:
    """Browser service for Thea automation."""

    def __init__(self, config: TheaConfig):
        self.config = config
        self.driver = None
        self.mode = (BrowserMode.SELENIUM if config.use_selenium else
            BrowserMode.MANUAL)
        self._selenium_available = self._check_selenium_availability()

    def _check_selenium_availability(self) ->bool:
        """Check if Selenium dependencies are available."""
        try:
            import selenium
            import undetected_chromedriver as uc
            from selenium import webdriver
            from webdriver_manager.chrome import ChromeDriverManager
            return True
        except ImportError:
            return False

    def initialize_driver(self) ->bool:
        """Initialize the browser driver."""
        if self.mode == BrowserMode.MANUAL or not self._selenium_available:
            logger.info('🔄 USING MANUAL MODE - Browser initialization skipped')
            return True
        if not self.config.use_selenium:
            logger.info('🔄 SELENIUM DISABLED - Using manual mode')
            self.mode = BrowserMode.MANUAL
            return True
        try:
            logger.info('🚀 INITIALIZING SELENIUM DRIVER')
            logger.info('-' * 35)
            options = self._create_chrome_options()
            try:
                logger.info('🔍 Trying undetected Chrome driver...')
                import undetected_chromedriver as uc
                self.driver = uc.Chrome(options=options)
                logger.info('✅ Undetected Chrome driver initialized')
            except Exception as e:
                logger.info(f'⚠️  Undetected Chrome failed: {e}')
                logger.info('🔄 Falling back to standard Chrome driver...')
                from selenium import webdriver
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(ChromeDriverManager().
                    install(), options=options)
                logger.info('✅ Standard Chrome driver initialized')
            self.driver.implicitly_wait(self.config.browser_timeout)
            self.driver.set_page_load_timeout(self.config.page_load_timeout)
            return True
        except Exception as e:
            logger.info(f'❌ Failed to initialize driver: {e}')
            self.mode = BrowserMode.MANUAL
            return False

    def _create_chrome_options(self):
        """Create Chrome options from configuration."""
        from selenium.webdriver.chrome.options import Options
        options = Options()
        if self.config.headless:
            options.add_argument('--headless')
        for key, value in self.config.selenium_options.items():
            if isinstance(value, bool) and value:
                options.add_argument(f'--{key}')
            elif isinstance(value, str):
                options.add_argument(f'--{key}={value}')
        return options

    def navigate_to_thea(self) ->bool:
        """Navigate to Thea page."""
        if not self.driver:
            return False
        try:
            logger.info('🌐 Navigating to Thea...')
            self.driver.get(self.config.thea_url)
            return True
        except Exception as e:
            logger.info(f'❌ Failed to navigate to Thea: {e}')
            return False

    def navigate_to_chatgpt(self) ->bool:
        """Navigate to ChatGPT base page for login verification."""
        if not self.driver:
            return False
        try:
            logger.info('🌐 Navigating to ChatGPT for verification...')
            self.driver.get(self.config.chatgpt_base_url)
            return True
        except Exception as e:
            logger.info(f'❌ Failed to navigate to ChatGPT: {e}')
            return False

    def get_current_url(self) ->str:
        """Get current page URL."""
        if not self.driver:
            return ''
        return self.driver.current_url

    def wait_for_element(self, selector: str, timeout: int=10):
        """Wait for element to be available."""
        if not self.driver:
            return None
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((By.
                CSS_SELECTOR, selector)))
        except Exception:
            return None

    def find_input_field(self) ->(Any | None):
        """Find the message input field using configured selectors."""
        if not self.driver:
            return None
        for selector in self.config.input_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    return element
            except Exception:
                continue
        return None

    def send_message_to_input(self, message: str) ->bool:
        """Send message to input field with proper line breaks."""
        if not self.driver:
            return False
        try:
            from selenium.webdriver.common.keys import Keys
            input_field = self.find_input_field()
            if not input_field:
                logger.info('❌ Could not find input field')
                return False
            input_field.clear()
            lines = message.split('\n')
            for i, line in enumerate(lines):
                if i > 0:
                    input_field.send_keys(Keys.SHIFT + Keys.RETURN)
                input_field.send_keys(line)
            input_field.send_keys(Keys.RETURN)
            logger.info('✅ Message sent via Selenium!')
            return True
        except Exception as e:
            logger.info(f'❌ Selenium message sending failed: {e}')
            return False

    def get_cookies(self) ->list[dict[str, Any]]:
        """Get browser cookies."""
        if not self.driver:
            return []
        return self.driver.get_cookies()

    def add_cookies(self, cookies: list[dict[str, Any]]) ->None:
        """Add cookies to browser."""
        if not self.driver:
            return
        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                logger.info(
                    f"⚠️  Failed to add cookie {cookie.get('name', 'unknown')}: {e}"
                    )

    def refresh_page(self) ->None:
        """Refresh the current page."""
        if self.driver:
            self.driver.refresh()

    def execute_script(self, script: str, *args) ->Any:
        """Execute JavaScript in the browser."""
        if not self.driver:
            return None
        return self.driver.execute_script(script, *args)

    @contextmanager
    def driver_context(self):
        """Context manager for driver lifecycle."""
        try:
            yield self.driver
        finally:
            self.cleanup()

    def cleanup(self) ->None:
        """Clean up browser resources."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info('✅ Browser driver closed')
            except Exception as e:
                logger.info(f'⚠️  Error closing driver: {e}')
            finally:
                self.driver = None

    def __enter__(self):
        """Context manager entry."""
        self.initialize_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
