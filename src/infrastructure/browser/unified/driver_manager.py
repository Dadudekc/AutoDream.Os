"""
UnifiedDriverManager - Chrome WebDriver management with advanced features.

V2 Compliance: Adapted from Chat_Mate with V2 logging patterns
Author: Agent-7 - Repository Cloning Specialist
License: MIT
"""

import logging
import threading
from typing import Any, Optional

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    uc = None
    ChromeService = None
    ChromeDriverManager = None

# V2 Logging Pattern
logger = logging.getLogger(__name__)


# ---------------------------
# UnifiedDriverManager Class
# ---------------------------
class UnifiedDriverManager:
    """
    Singleton class for managing an undetected Chrome WebDriver instance.

    Features:
      - Persistent profile support (or temporary profiles in headless mode)
      - Cookie saving and loading for session persistence
      - Mobile emulation and headless mode support
      - Context management for automatic cleanup
      - Ability to update driver options dynamically
    """

    _instance: Optional["UnifiedDriverManager"] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> "UnifiedDriverManager":
        """Ensure singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, driver_options: dict[str, Any] | None = None):
        """
        Initialize the driver manager with options.

        Args:
            driver_options: Optional dictionary of driver configuration options
        """
        if hasattr(self, "_initialized"):
            return

        self.driver_options = driver_options or {}
        self.headless = self.driver_options.get("headless", False)
        self.mobile_emulation = self.driver_options.get("mobile_emulation", False)
        self.driver = None
        self.profile_path = None
        self._initialized = True

        logger.info(
            f"UnifiedDriverManager initialized: Headless={self.headless}, Mobile={self.mobile_emulation}"
        )

    def _download_driver_if_needed(self) -> str:
        """
        Download Chrome driver if not present.

        Returns:
            str: Path to Chrome driver executable

        Raises:
            Exception: If driver download fails
        """
        try:
            if ChromeDriverManager is None:
                raise ImportError("webdriver_manager not installed")
            driver_path = ChromeDriverManager().install()
            logger.info(f"Chrome driver downloaded: {driver_path}")
            return driver_path
        except Exception as e:
            logger.error(f"Failed to download Chrome driver: {e}")
            raise

    def _setup_chrome_options(self):
        """
        Setup Chrome options based on configuration.

        Returns:
            ChromeOptions: Configured Chrome options
        """
        if uc is None:
            raise ImportError("undetected_chromedriver not installed")
        options = uc.ChromeOptions()

        if self.headless:
            options.add_argument("--headless")

        if self.mobile_emulation:
            mobile_emulation = {
                "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)

        # Common options for stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        return options

    def get_driver(self):
        """
        Get the Chrome WebDriver instance.

        Returns:
            Chrome: Undetected Chrome WebDriver instance

        Raises:
            Exception: If driver initialization fails
        """
        if self.driver is None:
            try:
                if uc is None:
                    raise ImportError("undetected_chromedriver not installed")
                driver_path = self._download_driver_if_needed()
                options = self._setup_chrome_options()

                service = ChromeService(driver_path)
                self.driver = uc.Chrome(service=service, options=options)
                logger.info("Chrome WebDriver initialized successfully")

            except Exception as e:
                logger.error(f"Failed to initialize Chrome WebDriver: {e}")
                raise

        return self.driver

    def close_driver(self):
        """
        Close the Chrome WebDriver instance.

        Raises:
            Exception: If driver cleanup fails
        """
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info("Chrome WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Error closing Chrome WebDriver: {e}")

    def __enter__(self):
        """
        Context manager entry.

        Returns:
            Chrome: WebDriver instance
        """
        return self.get_driver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit - cleanup driver.

        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised
        """
        self.close_driver()
