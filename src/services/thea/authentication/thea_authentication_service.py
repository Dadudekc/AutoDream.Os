import logging

logger = logging.getLogger(__name__)
"""
Thea Authentication Service - V2 Compliant Authentication Management
==================================================================

Handles login, cookie persistence, and authentication state management.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""
import json
import time
import webbrowser
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any

from ...thea.config.thea_config import TheaConfig


class AuthStatus(Enum):
    """Authentication status."""

    AUTHENTICATED = "authenticated"
    REQUIRES_LOGIN = "requires_login"
    EXPIRED = "expired"
    UNKNOWN = "unknown"


class TheaCookieManager:
    """Manages cookie persistence for Thea authentication."""

    def __init__(self, cookie_file: str = "thea_cookies.json"):
        self.cookie_file = Path(cookie_file)

    def save_cookies(self, cookies: list[dict[str, Any]]) -> bool:
        """Save cookies to file with metadata."""
        try:
            cookie_data = {
                "timestamp": datetime.now().isoformat(),
                "cookies": cookies,
                "domain": "chatgpt.com",
            }
            with open(self.cookie_file, "w") as f:
                json.dump(cookie_data, f, indent=2)
            logger.info(f"✅ Cookies saved: {self.cookie_file}")
            return True
        except Exception as e:
            logger.info(f"❌ Failed to save cookies: {e}")
            return False

    def load_cookies(self) -> tuple[list[dict[str, Any]], bool]:
        """Load cookies from file and check validity."""
        if not self.cookie_file.exists():
            return [], False
        try:
            with open(self.cookie_file) as f:
                data = json.load(f)
            if isinstance(data, list):
                cookies = data
                logger.info(f"✅ Cookies loaded (legacy format): {len(cookies)} cookies")
                return cookies, True
            elif isinstance(data, dict):
                cookies = data.get("cookies", [])
                timestamp_str = data.get("timestamp", "")
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        if datetime.now() - timestamp > timedelta(hours=24):
                            logger.info("⚠️  Cookies are stale (>24 hours old)")
                            return cookies, False
                    except ValueError:
                        logger.info("⚠️  Invalid timestamp format in cookie file")
                logger.info(f"✅ Cookies loaded: {len(cookies)} cookies")
                return cookies, True
            else:
                logger.info("⚠️  Invalid cookie file format")
                return [], False
        except Exception as e:
            logger.info(f"⚠️  Failed to load cookies: {e}")
            return [], False

    def has_valid_cookies(self) -> bool:
        """Check if valid cookies exist."""
        _, valid = self.load_cookies()
        return valid

    def clear_cookies(self) -> None:
        """Clear saved cookies."""
        if self.cookie_file.exists():
            self.cookie_file.unlink()
            logger.info("✅ Cookies cleared")


class TheaLoginDetector:
    """Detects login status on ChatGPT pages."""

    def __init__(self, browser_service: "TheaBrowserService"):
        self.browser = browser_service

    def is_logged_in(self) -> AuthStatus:
        """Check if user is logged in."""
        if not self.browser.driver:
            return AuthStatus.UNKNOWN
        try:
            login_indicators = [
                ".flex.items-center.justify-center > div:contains('Sign up for free')",
                "a[href*='login']",
                "button:contains('Log in')",
            ]
            for indicator in login_indicators:
                try:
                    element = self.browser.driver.find_element(By.CSS_SELECTOR, indicator)
                    if element.is_displayed():
                        logger.info("🔍 Detected login page - authentication required")
                        return AuthStatus.REQUIRES_LOGIN
                except Exception:
                    continue
            auth_indicators = [
                "[data-testid='profile-button']",
                "[data-testid='send-button']",
                "#prompt-textarea",
                "textarea[data-testid*='prompt']",
            ]
            for indicator in auth_indicators:
                try:
                    element = self.browser.driver.find_element(By.CSS_SELECTOR, indicator)
                    if element.is_displayed():
                        logger.info("🔍 Detected authenticated interface")
                        return AuthStatus.AUTHENTICATED
                except Exception:
                    continue
            logger.info("🔍 Login status unclear - may need manual verification")
            return AuthStatus.UNKNOWN
        except Exception as e:
            logger.info(f"⚠️  Login detection error: {e}")
            return AuthStatus.UNKNOWN


class TheaAuthenticationService:
    """Handles authentication for Thea services."""

    def __init__(self, config: TheaConfig):
        self.config = config
        self.cookie_manager = TheaCookieManager(config.cookie_file)
        self.login_detector = None

    def ensure_authenticated(self, browser_service: "TheaBrowserService") -> bool:
        """Ensure user is authenticated, using cookies or manual login."""
        logger.info("🔐 AUTHENTICATION CHECK")
        logger.info("-" * 25)
        self.login_detector = TheaLoginDetector(browser_service)
        if self.config.use_cookies and self.cookie_manager.has_valid_cookies():
            if self._try_cookie_authentication(browser_service):
                return True
        return self._manual_authentication()

    def _try_cookie_authentication(self, browser_service: "TheaBrowserService") -> bool:
        """Try to authenticate using saved cookies."""
        logger.info("🍪 ATTEMPTING COOKIE AUTHENTICATION")
        try:
            cookies, valid = self.cookie_manager.load_cookies()
            if not valid or not cookies:
                logger.info("⚠️  No valid cookies available")
                return False
            if not browser_service.navigate_to_chatgpt():
                return False
            time.sleep(2)
            browser_service.add_cookies(cookies)
            logger.info("✅ Cookies applied to browser")
            browser_service.refresh_page()
            time.sleep(3)
            auth_status = self.login_detector.is_logged_in()
            if auth_status == AuthStatus.AUTHENTICATED:
                logger.info("✅ COOKIE AUTHENTICATION SUCCESSFUL")
                updated_cookies = browser_service.get_cookies()
                self.cookie_manager.save_cookies(updated_cookies)
                browser_service.navigate_to_thea()
                return True
            else:
                logger.info("❌ COOKIE AUTHENTICATION FAILED")
                return False
        except Exception as e:
            logger.info(f"❌ Cookie authentication error: {e}")
            return False

    def _manual_authentication(self) -> bool:
        """Handle manual authentication."""
        logger.info("👤 MANUAL AUTHENTICATION REQUIRED")
        logger.info("-" * 35)
        logger.info("Please complete these steps:")
        logger.info("1. Open your browser")
        logger.info("2. Navigate to: {}")
        logger.info("3. Log in if needed")
        logger.info("4. Return to this terminal")
        input("\n🎯 Press Enter when you're logged in and on the Thea page...")
        try:
            webbrowser.open(self.config.thea_url, new=1)
            logger.info("✅ Browser opened to Thea page")
        except Exception as e:
            logger.info(f"⚠️  Could not open browser: {e}")
        logger.info("⏳ Waiting 5 seconds for page to load...")
        time.sleep(5)
        return True

    def save_session_cookies(self, browser_service: "TheaBrowserService") -> None:
        """Save current session cookies."""
        if browser_service.driver:
            cookies = browser_service.get_cookies()
            self.cookie_manager.save_cookies(cookies)

    def check_login_status(self, browser_service: "TheaBrowserService") -> AuthStatus:
        """Check current login status."""
        if not self.login_detector:
            self.login_detector = TheaLoginDetector(browser_service)
        return self.login_detector.is_logged_in()

    def clear_authentication(self) -> None:
        """Clear all authentication data."""
        self.cookie_manager.clear_cookies()
        logger.info("✅ Authentication data cleared")
