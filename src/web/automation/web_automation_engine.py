"""
Web Automation Engine for Agent_Cellphone_V2_Repository
Provides comprehensive web automation capabilities using Selenium and Playwright
"""

import logging
import time

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from contextlib import contextmanager

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logging.warning(
        "Selenium not available. Install with: pip install selenium webdriver-manager"
    )

try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logging.warning("Playwright not available. Install with: pip install playwright")


@dataclass
class AutomationConfig:
    """Configuration for web automation"""

    headless: bool = False
    window_size: str = "1920x1080"
    timeout: int = 30
    implicit_wait: int = 10
    screenshot_dir: str = "automation_screenshots"
    log_level: str = "INFO"
    browser_type: str = "chrome"  # chrome, firefox, edge, playwright
    user_agent: Optional[str] = None


class WebAutomationEngine:
    """Main web automation engine supporting multiple automation frameworks"""

    def __init__(self, config: Optional[AutomationConfig] = None):
        self.config = config or AutomationConfig()
        self.logger = self._setup_logging()
        self.drivers = {}
        self.playwright_browser = None
        self.playwright_context = None

        # Ensure screenshot directory exists
        self.screenshot_dir = Path(self.config.screenshot_dir)
        self.screenshot_dir.mkdir(exist_ok=True)

        self.logger.info(
            f"Web Automation Engine initialized with config: {self.config}"
        )

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("WebAutomationEngine")
        logger.setLevel(getattr(logging, self.config.log_level.upper()))

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def get_selenium_driver(self, browser_type: str = None) -> webdriver.Remote:
        """Get or create a Selenium WebDriver instance"""
        if not SELENIUM_AVAILABLE:
            raise RuntimeError(
                "Selenium is not available. Please install selenium and webdriver-manager"
            )

        browser_type = browser_type or self.config.browser_type
        driver_key = f"selenium_{browser_type}"

        if driver_key not in self.drivers:
            self.logger.info(f"Creating new Selenium {browser_type} driver")
            self.drivers[driver_key] = self._create_selenium_driver(browser_type)

        return self.drivers[driver_key]

    def _create_selenium_driver(self, browser_type: str) -> webdriver.Remote:
        """Create a new Selenium WebDriver instance"""
        try:
            if browser_type.lower() == "chrome":
                options = ChromeOptions()
                if self.config.headless:
                    options.add_argument("--headless")
                options.add_argument(f"--window-size={self.config.window_size}")
                if self.config.user_agent:
                    options.add_argument(f"--user-agent={self.config.user_agent}")

                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)

            elif browser_type.lower() == "firefox":
                options = FirefoxOptions()
                if self.config.headless:
                    options.add_argument("--headless")
                options.add_argument(f"--width={self.config.window_size.split('x')[0]}")
                options.add_argument(
                    f"--height={self.config.window_size.split('x')[1]}"
                )
                if self.config.user_agent:
                    options.add_argument(f"--user-agent={self.config.user_agent}")

                service = Service(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)

            else:
                raise ValueError(f"Unsupported browser type: {browser_type}")

            driver.implicitly_wait(self.config.implicit_wait)
            driver.set_page_load_timeout(self.config.timeout)
            driver.set_script_timeout(self.config.timeout)

            self.logger.info(f"Successfully created {browser_type} driver")
            return driver

        except Exception as e:
            self.logger.error(f"Failed to create {browser_type} driver: {e}")
            raise

    def get_playwright_browser(self) -> Browser:
        """Get or create a Playwright browser instance"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright is not available. Please install playwright")

        if not self.playwright_browser:
            self.logger.info("Creating new Playwright browser")
            self.playwright_browser = self._create_playwright_browser()

        return self.playwright_browser

    def _create_playwright_browser(self) -> Browser:
        """Create a new Playwright browser instance"""
        try:
            playwright = sync_playwright().start()

            if self.config.browser_type.lower() == "chrome":
                browser = playwright.chromium.launch(
                    headless=self.config.headless,
                    args=[
                        f"--window-size={self.config.window_size}",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                    ],
                )
            elif self.config.browser_type.lower() == "firefox":
                browser = playwright.firefox.launch(headless=self.config.headless)
            else:
                browser = playwright.webkit.launch(headless=self.config.headless)

            self.logger.info("Successfully created Playwright browser")
            return browser

        except Exception as e:
            self.logger.error(f"Failed to create Playwright browser: {e}")
            raise

    def get_playwright_context(self) -> BrowserContext:
        """Get or create a Playwright browser context"""
        if not self.playwright_context:
            browser = self.get_playwright_browser()
            self.playwright_context = browser.new_context(
                viewport={
                    "width": int(self.config.window_size.split("x")[0]),
                    "height": int(self.config.window_size.split("x")[1]),
                },
                user_agent=self.config.user_agent,
            )

        return self.playwright_context

    def navigate_to(self, url: str, browser_type: str = None) -> bool:
        """Navigate to a URL using the specified browser"""
        try:
            if browser_type == "playwright" or self.config.browser_type == "playwright":
                page = self.get_playwright_context().new_page()
                page.goto(url, timeout=self.config.timeout * 1000)
                self.logger.info(f"Successfully navigated to {url} using Playwright")
                return True
            else:
                driver = self.get_selenium_driver(browser_type)
                driver.get(url)
                self.logger.info(f"Successfully navigated to {url} using Selenium")
                return True

        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {e}")
            return False

    def take_screenshot(self, filename: str, browser_type: str = None) -> Optional[str]:
        """Take a screenshot and save it to the screenshot directory"""
        try:
            timestamp = int(time.time())
            screenshot_path = self.screenshot_dir / f"{filename}_{timestamp}.png"

            if browser_type == "playwright" or self.config.browser_type == "playwright":
                page = self.get_playwright_context().new_page()
                page.screenshot(path=str(screenshot_path))
            else:
                driver = self.get_selenium_driver(browser_type)
                driver.save_screenshot(str(screenshot_path))

            self.logger.info(f"Screenshot saved to {screenshot_path}")
            return str(screenshot_path)

        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            return None

    def find_element(
        self,
        selector: str,
        by: str = "css",
        browser_type: str = None,
        timeout: int = None,
    ):
        """Find an element using the specified selector and method"""
        timeout = timeout or self.config.timeout

        try:
            if browser_type == "playwright" or self.config.browser_type == "playwright":
                page = self.get_playwright_context().new_page()
                if by.lower() == "css":
                    element = page.locator(selector).first
                elif by.lower() == "xpath":
                    element = page.locator(f"xpath={selector}")
                else:
                    element = page.locator(selector)

                element.wait_for(timeout=timeout * 1000)
                return element
            else:
                driver = self.get_selenium_driver(browser_type)
                wait = WebDriverWait(driver, timeout)

                if by.lower() == "css":
                    element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                elif by.lower() == "xpath":
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                else:
                    element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )

                return element

        except Exception as e:
            self.logger.error(f"Failed to find element {selector}: {e}")
            return None

    def click_element(
        self, selector: str, by: str = "css", browser_type: str = None
    ) -> bool:
        """Click an element using the specified selector"""
        try:
            element = self.find_element(selector, by, browser_type)
            if element:
                if (
                    browser_type == "playwright"
                    or self.config.browser_type == "playwright"
                ):
                    element.click()
                else:
                    element.click()

                self.logger.info(f"Successfully clicked element {selector}")
                return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to click element {selector}: {e}")
            return False

    def input_text(
        self, selector: str, text: str, by: str = "css", browser_type: str = None
    ) -> bool:
        """Input text into an element using the specified selector"""
        try:
            element = self.find_element(selector, by, browser_type)
            if element:
                if (
                    browser_type == "playwright"
                    or self.config.browser_type == "playwright"
                ):
                    element.fill(text)
                else:
                    element.clear()
                    element.send_keys(text)

                self.logger.info(f"Successfully input text into element {selector}")
                return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to input text into element {selector}: {e}")
            return False

    def wait_for_element(
        self,
        selector: str,
        by: str = "css",
        timeout: int = None,
        browser_type: str = None,
    ) -> bool:
        """Wait for an element to be present and visible"""
        timeout = timeout or self.config.timeout

        try:
            if browser_type == "playwright" or self.config.browser_type == "playwright":
                page = self.get_playwright_context().new_page()
                if by.lower() == "css":
                    page.locator(selector).wait_for(timeout=timeout * 1000)
                else:
                    page.locator(f"xpath={selector}").wait_for(timeout=timeout * 1000)
            else:
                driver = self.get_selenium_driver(browser_type)
                wait = WebDriverWait(driver, timeout)
                if by.lower() == "css":
                    wait.until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                else:
                    wait.until(EC.visibility_of_element_located((By.XPATH, selector)))

            self.logger.info(f"Element {selector} is now visible")
            return True

        except TimeoutException:
            self.logger.warning(f"Timeout waiting for element {selector}")
            return False
        except Exception as e:
            self.logger.error(f"Error waiting for element {selector}: {e}")
            return False

    def execute_script(self, script: str, browser_type: str = None, *args):
        """Execute JavaScript code in the browser"""
        try:
            if browser_type == "playwright" or self.config.browser_type == "playwright":
                page = self.get_playwright_context().new_page()
                result = page.evaluate(script, *args)
            else:
                driver = self.get_selenium_driver(browser_type)
                result = driver.execute_script(script, *args)

            self.logger.info(f"Successfully executed script: {script[:50]}...")
            return result

        except Exception as e:
            self.logger.error(f"Failed to execute script: {e}")
            return None

    def get_page_title(self, browser_type: str = None) -> Optional[str]:
        """Get the current page title"""
        try:
            if browser_type == "playwright" or self.config.browser_type == "playwright":
                page = self.get_playwright_context().new_page()
                return page.title()
            else:
                driver = self.get_selenium_driver(browser_type)
                return driver.title

        except Exception as e:
            self.logger.error(f"Failed to get page title: {e}")
            return None

    def get_page_source(self, browser_type: str = None) -> Optional[str]:
        """Get the current page source HTML"""
        try:
            if browser_type == "playwright" or self.config.browser_type == "playwright":
                page = self.get_playwright_context().new_page()
                return page.content()
            else:
                driver = self.get_selenium_driver(browser_type)
                return driver.page_source

        except Exception as e:
            self.logger.error(f"Failed to get page source: {e}")
            return None

    def close_all_browsers(self):
        """Close all browser instances and clean up resources"""
        try:
            # Close Selenium drivers
            for driver_key, driver in self.drivers.items():
                try:
                    driver.quit()
                    self.logger.info(f"Closed {driver_key}")
                except Exception as e:
                    self.logger.warning(f"Error closing {driver_key}: {e}")

            self.drivers.clear()

            # Close Playwright browser
            if self.playwright_browser:
                try:
                    self.playwright_browser.close()
                    self.logger.info("Closed Playwright browser")
                except Exception as e:
                    self.logger.warning(f"Error closing Playwright browser: {e}")

                self.playwright_browser = None
                self.playwright_context = None

            self.logger.info("All browsers closed successfully")

        except Exception as e:
            self.logger.error(f"Error during browser cleanup: {e}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup"""
        self.close_all_browsers()


# Convenience functions for common automation tasks
def create_automation_engine(
    config: Optional[AutomationConfig] = None,
) -> WebAutomationEngine:
    """Create a new web automation engine instance"""
    return WebAutomationEngine(config)


def run_automation_task(
    task_func, config: Optional[AutomationConfig] = None, *args, **kwargs
):
    """Run an automation task with automatic cleanup"""
    with WebAutomationEngine(config) as engine:
        return task_func(engine, *args, **kwargs)
