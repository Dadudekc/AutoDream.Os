#!/usr/bin/env python3
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
                "domain": "chatgpt.com"
            }

            with open(self.cookie_file, 'w') as f:
                json.dump(cookie_data, f, indent=2)

            print(f"✅ Cookies saved: {self.cookie_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to save cookies: {e}")
            return False

    def load_cookies(self) -> tuple[list[dict[str, Any]], bool]:
        """Load cookies from file and check validity."""
        if not self.cookie_file.exists():
            return [], False

        try:
            with open(self.cookie_file) as f:
                data = json.load(f)

            # Handle both old and new cookie formats
            if isinstance(data, list):
                # Old format: direct list of cookies
                cookies = data
                print(f"✅ Cookies loaded (legacy format): {len(cookies)} cookies")
                return cookies, True
            elif isinstance(data, dict):
                # New format: dict with metadata
                cookies = data.get('cookies', [])
                timestamp_str = data.get('timestamp', '')

                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        # Check if cookies are less than 24 hours old
                        if datetime.now() - timestamp > timedelta(hours=24):
                            print("⚠️  Cookies are stale (>24 hours old)")
                            return cookies, False
                    except ValueError:
                        print("⚠️  Invalid timestamp format in cookie file")

                print(f"✅ Cookies loaded: {len(cookies)} cookies")
                return cookies, True
            else:
                print("⚠️  Invalid cookie file format")
                return [], False

        except Exception as e:
            print(f"⚠️  Failed to load cookies: {e}")
            return [], False

    def has_valid_cookies(self) -> bool:
        """Check if valid cookies exist."""
        _, valid = self.load_cookies()
        return valid

    def clear_cookies(self) -> None:
        """Clear saved cookies."""
        if self.cookie_file.exists():
            self.cookie_file.unlink()
            print("✅ Cookies cleared")


class TheaLoginDetector:
    """Detects login status on ChatGPT pages."""

    def __init__(self, browser_service: "TheaBrowserService"):
        self.browser = browser_service

    def is_logged_in(self) -> AuthStatus:
        """Check if user is logged in."""
        if not self.browser.driver:
            return AuthStatus.UNKNOWN

        try:
            # Check for login page indicators
            login_indicators = [
                ".flex.items-center.justify-center > div:contains('Sign up for free')",
                "a[href*='login']",
                "button:contains('Log in')"
            ]

            for indicator in login_indicators:
                try:
                    element = self.browser.driver.find_element(By.CSS_SELECTOR, indicator)
                    if element.is_displayed():
                        print("🔍 Detected login page - authentication required")
                        return AuthStatus.REQUIRES_LOGIN
                except Exception:
                    continue

            # Check for authenticated user indicators
            auth_indicators = [
                "[data-testid='profile-button']",
                "[data-testid='send-button']",
                "#prompt-textarea",
                "textarea[data-testid*='prompt']"
            ]

            for indicator in auth_indicators:
                try:
                    element = self.browser.driver.find_element(By.CSS_SELECTOR, indicator)
                    if element.is_displayed():
                        print("🔍 Detected authenticated interface")
                        return AuthStatus.AUTHENTICATED
                except Exception:
                    continue

            print("🔍 Login status unclear - may need manual verification")
            return AuthStatus.UNKNOWN

        except Exception as e:
            print(f"⚠️  Login detection error: {e}")
            return AuthStatus.UNKNOWN


class TheaAuthenticationService:
    """Handles authentication for Thea services."""

    def __init__(self, config: TheaConfig):
        self.config = config
        self.cookie_manager = TheaCookieManager(config.cookie_file)
        self.login_detector = None  # Will be set when browser is available

    def ensure_authenticated(self, browser_service: "TheaBrowserService") -> bool:
        """Ensure user is authenticated, using cookies or manual login."""
        print("🔐 AUTHENTICATION CHECK")
        print("-" * 25)

        self.login_detector = TheaLoginDetector(browser_service)

        # Try cookie-based authentication first
        if self.config.use_cookies and self.cookie_manager.has_valid_cookies():
            if self._try_cookie_authentication(browser_service):
                return True

        # Fall back to manual authentication
        return self._manual_authentication()

    def _try_cookie_authentication(self, browser_service: "TheaBrowserService") -> bool:
        """Try to authenticate using saved cookies."""
        print("🍪 ATTEMPTING COOKIE AUTHENTICATION")

        try:
            # Load cookies
            cookies, valid = self.cookie_manager.load_cookies()
            if not valid or not cookies:
                print("⚠️  No valid cookies available")
                return False

            # Navigate to ChatGPT first
            if not browser_service.navigate_to_chatgpt():
                return False

            time.sleep(2)  # Allow page to load

            # Add cookies
            browser_service.add_cookies(cookies)
            print("✅ Cookies applied to browser")

            # Refresh to apply cookies
            browser_service.refresh_page()
            time.sleep(3)

            # Check login status
            auth_status = self.login_detector.is_logged_in()
            if auth_status == AuthStatus.AUTHENTICATED:
                print("✅ COOKIE AUTHENTICATION SUCCESSFUL")

                # Save updated cookies
                updated_cookies = browser_service.get_cookies()
                self.cookie_manager.save_cookies(updated_cookies)

                # Navigate to Thea
                browser_service.navigate_to_thea()
                return True
            else:
                print("❌ COOKIE AUTHENTICATION FAILED")
                return False

        except Exception as e:
            print(f"❌ Cookie authentication error: {e}")
            return False

    def _manual_authentication(self) -> bool:
        """Handle manual authentication."""
        print("👤 MANUAL AUTHENTICATION REQUIRED")
        print("-" * 35)
        print("Please complete these steps:")
        print("1. Open your browser")
        print("2. Navigate to:", self.config.thea_url)
        print("3. Log in if needed")
        print("4. Return to this terminal")

        input("\n🎯 Press Enter when you're logged in and on the Thea page...")

        # Try to open browser for user
        try:
            webbrowser.open(self.config.thea_url, new=1)
            print("✅ Browser opened to Thea page")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")

        print("⏳ Waiting 5 seconds for page to load...")
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
        print("✅ Authentication data cleared")
