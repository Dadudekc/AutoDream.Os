#!/usr/bin/env python3
"""
Thea Communication - Selenium Management
=======================================

Selenium WebDriver management and automation for Thea communication.
Extracted from main communication module for V2 compliance.
"""

import time
from pathlib import Path


class TheaSeleniumManager:
    """Manages Selenium WebDriver for Thea communication."""

    def __init__(self, headless=False):
        """
        Initialize the Selenium manager.

        Args:
            headless: Whether to run browser in headless mode
        """
        self.headless = headless
        self.driver = None
        self.selenium_available = False
        
        # Check if Selenium is available
        self._check_selenium_availability()

    def _check_selenium_availability(self):
        """Check if Selenium dependencies are available."""
        try:
            import undetected_chromedriver as uc
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            self.selenium_available = True
        except ImportError:
            self.selenium_available = False
            print("⚠️  Selenium not available - falling back to manual mode")

    def initialize_driver(self):
        """Initialize Selenium WebDriver."""
        if not self.selenium_available:
            return False

        try:
            import undetected_chromedriver as uc
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager

            print("🚀 INITIALIZING SELENIUM DRIVER")
            print("-" * 35)

            # Configure Chrome options
            options = Options()
            if self.headless:
                print("🫥 HEADLESS MODE: Configuring browser to run invisibly...")
                options.add_argument("--headless=new")  # Use new headless mode
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                # Additional headless-specific options
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-plugins")
                options.add_argument("--disable-images")
                options.add_argument("--disable-web-security")
                options.add_argument("--disable-features=VizDisplayCompositor")
                # Critical for headless mode
                options.add_argument("--remote-debugging-port=9222")
                options.add_argument(
                    "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
            else:
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")

            # Use webdriver_manager for automatic version matching (better compatibility)
            try:
                print("🔍 Initializing Chrome driver with automatic version matching...")
                from selenium import webdriver
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager

                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()), options=options
                )
                print("✅ Chrome driver initialized with automatic version matching")
            except Exception as e:
                print(f"⚠️  Standard Chrome failed: {e}")
                print("🔄 Trying undetected Chrome as fallback...")
                try:
                    if self.headless:
                        self.driver = uc.Chrome(options=options, headless=True)
                    else:
                        self.driver = uc.Chrome(options=options)
                    print("✅ Undetected Chrome driver initialized as fallback")
                except Exception as e2:
                    print(f"❌ All Chrome drivers failed: {e2}")
                    raise e2

            return True

        except Exception as e:
            print(f"❌ Failed to initialize driver: {e}")
            return False

    def send_message_selenium(self, driver, message: str, thea_url: str) -> bool:
        """Send message using Selenium automation."""
        try:
            print("🤖 AUTOMATED MESSAGE SENDING")
            print("-" * 30)

            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait

            # Navigate to Thea if not already there
            if "thea-manager" not in driver.current_url:
                print("🌐 Navigating to Thea...")
                driver.get(thea_url)
                time.sleep(3)

            # Wait for input field to be available
            wait = WebDriverWait(driver, 10)

            # Try multiple selectors for the input field
            input_selectors = [
                "textarea[data-testid*='prompt']",
                "textarea[placeholder*='Message']",
                "#prompt-textarea",
                "textarea",
                "[contenteditable='true']",
            ]

            input_field = None
            for selector in input_selectors:
                try:
                    if selector.startswith("#") or selector.startswith("."):
                        input_field = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    else:
                        input_field = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except Exception as e:
                    print(f"⚠️  Skipping selector {selector}: {e}")
                    continue

            if not input_field:
                print("❌ Could not find input field")
                return False

            # Clear and send message with proper line breaks
            input_field.clear()

            # Send message line by line to respect Shift+Enter for line breaks
            lines = message.split("\n")
            for i, line in enumerate(lines):
                if i > 0:  # Not the first line
                    # Send Shift+Enter for line break
                    input_field.send_keys(Keys.SHIFT + Keys.RETURN)
                input_field.send_keys(line)

            # Wait a moment then send the message
            time.sleep(1)
            input_field.send_keys(Keys.RETURN)

            print("✅ Message sent via Selenium!")
            return True

        except Exception as e:
            print(f"❌ Selenium message sending failed: {e}")
            return False

    def cleanup(self):
        """Clean up Selenium resources."""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser driver closed")
            except Exception as e:
                print(f"⚠️  Error closing driver: {e}")

