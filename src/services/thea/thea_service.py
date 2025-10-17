#!/usr/bin/env python3
"""
Thea Service - Unified V2 Compliant Implementation
===================================================

Single unified implementation consolidating 25 files into one service.
Uses modular architecture with clear separation of concerns.

Features:
- Cookie-based authentication (proven pattern)
- Browser lifecycle management
- PyAutoGUI message sending
- Response detection and capture
- Session persistence

Author: Agent-2 (Architecture) - V2 Consolidation
License: MIT
"""

import logging
import time
from pathlib import Path

from .thea_browser import TheaBrowser
from .thea_config import TheaConfig
from .thea_cookies import TheaCookieManager
from .thea_detector import TheaDetector
from .thea_messaging import TheaMessenger

logger = logging.getLogger(__name__)


class TheaService:
    """
    Unified Thea communication service.

    Orchestrates all Thea operations through modular components:
    - Browser: Lifecycle and navigation
    - Cookies: Authentication and session
    - Messenger: PyAutoGUI message sending
    - Detector: Response capture and saving

    This is the SINGLE authoritative Thea implementation.
    """

    def __init__(
        self, cookie_file: str = "thea_cookies.json", headless: bool = False, config: TheaConfig | None = None
    ):
        """
        Initialize Thea service.

        Args:
            cookie_file: Path to cookie storage file
            headless: Run browser in headless mode
            config: Optional custom configuration
        """
        # Configuration
        self.config = config or TheaConfig()
        self.config.cookie_file = cookie_file
        self.config.headless = headless

        # Initialize components
        self.browser = TheaBrowser(self.config)
        self.cookies = TheaCookieManager(self.config.cookie_file)
        self.messenger = TheaMessenger(self.config)
        self.detector = TheaDetector(self.config)

        logger.info("✅ Thea service initialized (unified implementation)")

    def start_browser(self) -> bool:
        """Initialize browser with cookies."""
        try:
            logger.info("🚀 Starting browser...")

            options = Options()
            if self.headless:
                options.add_argument("--headless=new")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # Anti-detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            self.driver = webdriver.Chrome(options=options)
            logger.info("✅ Browser started")
            return True

        except Exception as e:
            logger.error(f"❌ Browser start failed: {e}")
            return False

    def ensure_login(self) -> bool:
        """Ensure logged in to Thea Manager."""
        try:
            if not self.driver:
                if not self.start_browser():
                    return False

            # CRITICAL: Navigate to domain FIRST before loading cookies
            logger.info("🌐 Navigating to ChatGPT domain...")
            self.driver.get("https://chatgpt.com/")
            time.sleep(2)

            # Load cookies if available (must be on domain first!)
            if self.cookie_file.exists():
                logger.info("🍪 Loading saved cookies...")
                with open(self.cookie_file) as f:
                    cookies = json.load(f)

                loaded_count = 0
                for cookie in cookies:
                    try:
                        self.driver.add_cookie(cookie)
                        loaded_count += 1
                    except Exception as e:
                        logger.debug(f"Skipped cookie: {e}")

                logger.info(f"✅ Loaded {loaded_count} cookies")

                # Now navigate to Thea with cookies
                logger.info("🌐 Navigating to Thea Manager...")
                self.driver.get(self.thea_url)
                time.sleep(3)
            else:
                # No cookies, just navigate to Thea
                logger.info(f"🌐 Navigating to {self.thea_url}")
                self.driver.get(self.thea_url)
                time.sleep(3)

            # Check if logged in
            if self._is_logged_in():
                logger.info("✅ Already logged in")
                return True

            # Manual login required
            logger.info("⚠️  Manual login required")
            logger.info("Please log in to ChatGPT in the browser window...")
            time.sleep(60)

            if self._is_logged_in():
                # Save cookies for next time
                cookies = self.driver.get_cookies()
                self.cookie_file.parent.mkdir(parents=True, exist_ok=True)
                with open(self.cookie_file, "w") as f:
                    json.dump(cookies, f, indent=2)
                logger.info("✅ Login successful, cookies saved")
                return True

            logger.error("❌ Login failed")
            return False

        except Exception as e:
            logger.error(f"❌ Login error: {e}")
            return False

    def _is_logged_in(self) -> bool:
        """Check if logged in."""
        try:
            current_url = self.driver.current_url
            if "auth" in current_url or "login" in current_url:
                return False

            # Check for textarea (indicates logged in)
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, "textarea")
                return elem.is_displayed()
            except:
                pass

            return "chatgpt.com" in current_url

        except:
            return False

    def send_message(self, message: str, wait_for_response: bool = True) -> str | None:
        """
        Send message to Thea and optionally wait for response.

        Args:
            message: Message to send
            wait_for_response: Whether to wait for response

        Returns:
            Response text if wait_for_response=True, else None
        """
        try:
            # Ensure browser and login
            if not self.driver:
                if not self.start_browser():
                    return None

            if not self.ensure_login():
                return None

            # Send message via PyAutoGUI (proven working method)
            if PYAUTOGUI_AVAILABLE:
                logger.info(f"📤 Sending message: {message[:50]}...")
                pyperclip.copy(message)
                time.sleep(0.5)

                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.5)
                pyautogui.press("enter")
                logger.info("✅ Message sent")
            else:
                logger.error("❌ PyAutoGUI not available")
                return None

            # Wait for response if requested
            if wait_for_response:
                return self.wait_for_response()

            return None

        except Exception as e:
            logger.error(f"❌ Send message failed: {e}")
            return None

    def wait_for_response(self, timeout: int = 120) -> str | None:
        """Wait for and capture Thea's response."""
        try:
            logger.info("⏳ Waiting for response...")

            if not DETECTOR_AVAILABLE:
                logger.warning("ResponseDetector not available - basic wait")
                time.sleep(15)
                return self._extract_basic_response()

            if not self.detector:
                self.detector = ResponseDetector(self.driver)

            # Wait for response
            result = self.detector.wait_until_complete(
                timeout=timeout, stable_secs=3.0, auto_continue=True
            )

            if result == ResponseWaitResult.COMPLETE:
                logger.info("✅ Response complete")
                response = self.detector.extract_response_text()
                return response
            else:
                logger.warning(f"⚠️ Response status: {result}")
                response = self.detector.extract_response_text()
                return response or f"⚠️ Incomplete: {result}"

        except Exception as e:
            logger.error(f"❌ Response capture failed: {e}")
            return None

    def _extract_basic_response(self) -> str | None:
        """Basic response extraction fallback."""
        try:
            articles = self.driver.find_elements(By.TAG_NAME, "article")
            if articles and len(articles) > 1:
                return articles[-1].text.strip()
            return None
        except:
            return None

    def communicate(self, message: str, save: bool = True) -> dict:
        """
        Complete communication cycle: send message and get response.

        Args:
            message: Message to send
            save: Whether to save conversation

        Returns:
            dict with 'success', 'message', 'response', 'file' keys
        """
        result = {"success": False, "message": message, "response": "", "file": ""}

        try:
            response = self.send_message(message, wait_for_response=True)

            if response:
                result["response"] = response
                result["success"] = True

                if save:
                    result["file"] = self._save_conversation(message, response)

            return result

        except Exception as e:
            result["response"] = f"Error: {e}"
            return result

    def _save_conversation(self, message: str, response: str) -> str:
        """Save conversation to file."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = self.responses_dir / f"conversation_{timestamp}.json"

            data = {
                "timestamp": timestamp,
                "message": message,
                "response": response,
                "thea_url": self.thea_url,
            }

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"💾 Saved to: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"❌ Save failed: {e}")
            return ""

    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Browser closed")
            except:
                pass
            finally:
                self.driver = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()


# Factory
def create_thea_service(
    cookie_file: str = "thea_cookies.json", headless: bool = False
) -> TheaService:
    """Create Thea service instance."""
    return TheaService(cookie_file, headless)


__all__ = ["TheaService", "create_thea_service"]
