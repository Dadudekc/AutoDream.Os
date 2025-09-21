#!/usr/bin/env python3
"""
Selenium Handler
===============

Selenium-based automation for Thea communication.
"""

import time
from typing import Optional

# Try undetected Chrome first, fallback to standard Selenium
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from response_detector import ResponseDetector, ResponseWaitResult


class SeleniumHandler:
    """Selenium-based automation handler."""

    def __init__(self, headless=False):
        """Initialize the Selenium handler."""
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.detector: Optional[ResponseDetector] = None

    def initialize_driver(self):
        """Initialize the Selenium driver."""
        print("🔧 Initializing Selenium driver...")
        
        try:
            # Try undetected Chrome first (works better with ChatGPT)
            if UNDETECTED_AVAILABLE and not self.headless:
                print("🔍 Using undetected Chrome driver...")
                options = uc.ChromeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                
                self.driver = uc.Chrome(options=options)
                self.driver.maximize_window()
                
                print("✅ Undetected Chrome driver initialized successfully")
            else:
                # Fallback to standard Chrome driver
                print("🔍 Using standard Chrome driver...")
                chrome_options = Options()
                if self.headless:
                    chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.maximize_window()
                
                print("✅ Standard Chrome driver initialized successfully")
            
            # Initialize response detector
            self.detector = ResponseDetector(self.driver)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize Selenium driver: {e}")
            return False

    def ensure_authenticated(self, login_handler) -> bool:
        """Ensure user is authenticated."""
        print("🔐 Ensuring authentication...")
        
        try:
            # Navigate to Thea URL
            self.driver.get(login_handler.thea_url)
            time.sleep(3)
            
            # Check if already authenticated
            if self._is_authenticated():
                print("✅ Already authenticated")
                return True
            
            # Try to authenticate using login handler
            if login_handler.ensure_login(self.driver):
                print("✅ Authentication successful")
                return True
            else:
                print("❌ Authentication failed")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False

    def _is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        try:
            # Look for authentication indicators
            auth_indicators = [
                "Sign in",
                "Log in", 
                "Login",
                "Continue with Google",
                "Continue with Microsoft"
            ]
            
            page_text = self.driver.page_source.lower()
            for indicator in auth_indicators:
                if indicator.lower() in page_text:
                    return False
            
            return True
            
        except Exception:
            return False

    def send_message(self, message: str) -> bool:
        """Send message using Selenium."""
        print("📤 Sending message via Selenium...")
        
        try:
            # Navigate to Thea if not already there
            thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
            if "thea-manager" not in self.driver.current_url:
                print("🌐 Navigating to Thea...")
                self.driver.get(thea_url)
                time.sleep(3)
            
            # Wait for input field to be available
            wait = WebDriverWait(self.driver, 10)
            
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
                    input_field = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Found input field with selector: {selector}")
                    break
                except Exception as e:
                    print(f"⚠️  Skipping selector {selector}: {e}")
                    continue
            
            if not input_field:
                print("❌ Could not find input field with any selector")
                return False
            
            # Clear and type message
            input_field.clear()
            input_field.send_keys(message)
            
            # Try multiple selectors for the send button
            send_selectors = [
                "button[data-testid='send-button']",
                "button[aria-label*='Send']",
                "button[type='submit']",
                "button:has(svg)",
                "button[class*='send']",
            ]
            
            send_button = None
            for selector in send_selectors:
                try:
                    send_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if send_button.is_enabled():
                        print(f"✅ Found send button with selector: {selector}")
                        break
                except Exception:
                    continue
            
            if not send_button:
                print("❌ Could not find send button")
                return False
            
            send_button.click()
            print("✅ Message sent successfully")
            return True
            
        except TimeoutException:
            print("❌ Timeout waiting for message input field")
            return False
        except NoSuchElementException:
            print("❌ Could not find message input or send button")
            return False
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False

    def wait_for_response(self, timeout: int = 120) -> bool:
        """Wait for Thea's response."""
        print(f"⏳ Waiting for response (timeout: {timeout}s)...")
        
        if not self.detector:
            print("❌ Response detector not initialized")
            return False
        
        try:
            result = self.detector.wait_until_complete(
                timeout=timeout,
                stable_secs=3.0,
                poll=0.5,
                auto_continue=True,
                max_continue_clicks=1,
            )
            
            if result == ResponseWaitResult.COMPLETE:
                print("✅ Response detected automatically")
                return True
            elif result == ResponseWaitResult.TIMEOUT:
                print("⏰ Timeout waiting for response")
                return False
            else:
                print("⚠️  Response detection failed")
                return False
                
        except Exception as e:
            print(f"❌ Error waiting for response: {e}")
            return False

    def cleanup(self):
        """Cleanup Selenium resources."""
        if self.driver:
            try:
                self.driver.quit()
                print("🧹 Selenium driver cleaned up")
            except Exception as e:
                print(f"⚠️  Error cleaning up Selenium driver: {e}")
            finally:
                self.driver = None


