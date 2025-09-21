#!/usr/bin/env python3
"""
Thea Browser Manager - V2 Compliant Browser Management
======================================================

Handles browser initialization and management for Thea communication.
Extracted from thea_communication_main.py to maintain V2 compliance.

Features:
- Selenium WebDriver initialization
- Chrome options configuration
- Headless and visible mode support
- Undetected Chrome integration

Usage:
    from src.services.thea.thea_browser_manager import TheaBrowserManager
    
    manager = TheaBrowserManager(headless=True)
    driver = manager.initialize_driver()
"""

import logging

# Selenium imports
try:
    import undetected_chromedriver as uc
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not available - browser manager will use fallback methods")

logger = logging.getLogger(__name__)


class TheaBrowserManager:
    """Manages browser initialization and configuration for Thea communication."""

    def __init__(self, headless: bool = False, use_undetected: bool = True):
        """
        Initialize the browser manager.

        Args:
            headless: Whether to run browser in headless mode
            use_undetected: Whether to use undetected Chrome driver
        """
        self.headless = headless
        self.use_undetected = use_undetected
        self.selenium_available = SELENIUM_AVAILABLE

    def initialize_driver(self):
        """Initialize Selenium WebDriver."""
        if not self.selenium_available:
            print("❌ Selenium not available")
            return None

        try:
            print("🚀 INITIALIZING SELENIUM DRIVER")
            print("-" * 35)

            # Configure Chrome options
            options = self._configure_chrome_options()

            # Try undetected Chrome first (better for ChatGPT)
            try:
                print("🔍 Trying undetected Chrome driver...")
                if self.headless:
                    driver = uc.Chrome(options=options, headless=True)
                else:
                    driver = uc.Chrome(options=options)
                print("✅ Undetected Chrome driver initialized")
                return driver
            except Exception as e:
                print(f"⚠️  Undetected Chrome failed: {e}")
                print("🔄 Falling back to standard Chrome driver...")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                print("✅ Standard Chrome driver initialized")
                return driver

        except Exception as e:
            print(f"❌ Failed to initialize driver: {e}")
            return None

    def _configure_chrome_options(self):
        """Configure Chrome options based on headless mode."""
        options = Options()
        
        if self.headless:
            print("🫥 HEADLESS MODE: Configuring browser to run invisibly...")
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument(
                "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        else:
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        return options

    def cleanup_driver(self, driver):
        """Clean up browser driver resources."""
        if driver:
            try:
                driver.quit()
                print("✅ Browser driver closed")
            except Exception as e:
                print(f"⚠️  Error closing driver: {e}")

    def is_selenium_available(self) -> bool:
        """Check if Selenium is available."""
        return self.selenium_available


# Convenience functions for easy integration
def create_browser_manager(headless: bool = False, use_undetected: bool = True) -> TheaBrowserManager:
    """
    Create a Thea browser manager with default settings.

    Args:
        headless: Whether to run browser in headless mode
        use_undetected: Whether to use undetected Chrome driver

    Returns:
        TheaBrowserManager instance
    """
    return TheaBrowserManager(headless=headless, use_undetected=use_undetected)


if __name__ == "__main__":
    # Example usage
    print("🐝 V2_SWARM Thea Browser Manager")
    print("=" * 40)

    # Create manager
    manager = create_browser_manager()

    print("✅ Thea Browser Manager created")
    print("📝 To use:")
    print("   manager = create_browser_manager(headless=True)")
    print("   driver = manager.initialize_driver()")

