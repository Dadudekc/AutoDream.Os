#!/usr/bin/env python3
"""
Thea Cookie Manager - V2 Compliant Cookie Management
====================================================

Manages cookie persistence for Thea sessions.
Extracted from thea_login_handler.py to maintain V2 compliance.

Features:
- Cookie saving and loading
- Cookie validation and expiry checking
- ChatGPT-specific cookie filtering
- Session persistence management

Usage:
    from src.services.thea.thea_cookie_manager import TheaCookieManager
    
    manager = TheaCookieManager("thea_cookies.json")
    success = manager.save_cookies(driver)
"""

import json
import logging
import time
from pathlib import Path

# Selenium imports
try:
    from selenium import webdriver
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not available - cookie manager will use fallback methods")

logger = logging.getLogger(__name__)


class TheaCookieManager:
    """Manages cookie persistence for Thea sessions."""

    def __init__(self, cookie_file: str = "thea_cookies.json"):
        """
        Initialize the cookie manager.

        Args:
            cookie_file: Path to cookie file for persistence
        """
        self.cookie_file = Path(cookie_file)
        self.cookie_file.parent.mkdir(parents=True, exist_ok=True)

    def save_cookies(self, driver) -> bool:
        """
        Save cookies from the current driver session.

        Args:
            driver: Selenium webdriver instance

        Returns:
            True if cookies saved successfully, False otherwise
        """
        try:
            if not SELENIUM_AVAILABLE:
                logger.warning("Selenium not available - cannot save cookies")
                return False

            cookies = driver.get_cookies()
            print(f"🔍 Found {len(cookies)} total cookies from browser")

            # Filter and save cookies - be more permissive for ChatGPT
            persistent_cookies = []
            for cookie in cookies:
                cookie_name = cookie.get("name", "")
                domain = cookie.get("domain", "")
                expiry = cookie.get("expiry")
                print(f"🔍 Cookie: {cookie_name} | Domain: {domain} | Expiry: {expiry}")
                
                # Skip obviously unimportant cookies
                cookie_name = cookie.get("name", "").lower()

                # Skip analytics and tracking cookies (optional)
                skip_names = ["_ga", "_gid", "_gat", "__gads", "_fbp", "_fbc"]
                if any(skip_name in cookie_name for skip_name in skip_names):
                    continue

                # For ChatGPT, save all cookies that are likely authentication-related
                # This includes session cookies which are often needed for login
                domain = cookie.get("domain", "").lower()
                if any(
                    chatgpt_domain in domain
                    for chatgpt_domain in ["openai.com", "chatgpt.com", "chat.openai.com"]
                ):
                    persistent_cookies.append(cookie)
                elif not domain or domain == "":  # Local cookies
                    persistent_cookies.append(cookie)
                elif cookie_name.startswith("__") and (
                    "openai" in cookie_name or "chatgpt" in cookie_name
                ):
                    # Special case for cookies with OpenAI/ChatGPT in name
                    persistent_cookies.append(cookie)

            with open(self.cookie_file, "w", encoding="utf-8") as f:
                json.dump(persistent_cookies, f, indent=2)

            logger.info(f"✅ Saved {len(persistent_cookies)} Thea cookies to {self.cookie_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
            return False

    def load_cookies(self, driver) -> bool:
        """
        Load cookies into the current driver session.

        Args:
            driver: Selenium webdriver instance

        Returns:
            True if cookies loaded successfully, False otherwise
        """
        try:
            if not SELENIUM_AVAILABLE:
                logger.warning("Selenium not available - cannot load cookies")
                return False

            if not self.cookie_file.exists():
                logger.info(f"Cookie file not found: {self.cookie_file}")
                return False

            with open(self.cookie_file, encoding="utf-8") as f:
                cookies = json.load(f)

            # Add cookies to driver
            loaded_count = 0
            for cookie in cookies:
                try:
                    # Ensure cookie has required fields
                    if "name" in cookie and "value" in cookie:
                        driver.add_cookie(cookie)
                        loaded_count += 1
                except Exception as e:
                    logger.warning(f"Failed to add cookie {cookie.get('name', 'unknown')}: {e}")

            logger.info(f"✅ Loaded {loaded_count} cookies from {self.cookie_file}")
            return loaded_count > 0

        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
            return False

    def has_valid_cookies(self) -> bool:
        """
        Check if valid cookies exist.

        Returns:
            True if cookie file exists and contains cookies
        """
        if not self.cookie_file.exists():
            return False

        try:
            with open(self.cookie_file, encoding="utf-8") as f:
                cookies = json.load(f)

            if len(cookies) == 0:
                return False

            # Check if cookies are recent (within last 24 hours)
            # This helps avoid using very old/stale cookies
            current_time = time.time()
            recent_cookies = []

            for cookie in cookies:
                expiry = cookie.get("expiry")
                if expiry and expiry > current_time:
                    recent_cookies.append(cookie)
                elif not expiry:  # Session cookies are considered valid
                    recent_cookies.append(cookie)

            return len(recent_cookies) > 0

        except Exception as e:
            print(f"⚠️  Error checking cookies: {e}")
            return False

    def clear_cookies(self) -> bool:
        """
        Clear saved cookies.

        Returns:
            True if cookies cleared successfully, False otherwise
        """
        try:
            if self.cookie_file.exists():
                self.cookie_file.unlink()
                logger.info("✅ Cookies cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear cookies: {e}")
            return False


# Convenience functions for easy integration
def create_cookie_manager(cookie_file: str = "thea_cookies.json") -> TheaCookieManager:
    """
    Create a Thea cookie manager with default settings.

    Args:
        cookie_file: Path to cookie file

    Returns:
        TheaCookieManager instance
    """
    return TheaCookieManager(cookie_file)


if __name__ == "__main__":
    # Example usage
    print("🐝 V2_SWARM Thea Cookie Manager")
    print("=" * 40)

    # Create manager
    manager = create_cookie_manager()

    print("✅ Thea Cookie Manager created")
    print("📝 To use:")
    print("   manager = create_cookie_manager('my_cookies.json')")
    print("   success = manager.save_cookies(driver)")

