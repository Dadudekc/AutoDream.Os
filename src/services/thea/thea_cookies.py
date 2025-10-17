#!/usr/bin/env python3
"""
Thea Cookie Manager - Authentication & Session Persistence
===========================================================

Handles cookie-based authentication for Thea service using proven patterns.

CRITICAL PATTERN (PROVEN WORKING):
1. Navigate to domain FIRST (https://chatgpt.com/)
2. Load cookies into driver
3. Refresh page to apply cookies ⭐
4. Navigate to Thea with cookies applied

Note: The refresh step (3) is CRITICAL for cookies to work!

Author: Agent-2 (Architecture) - V2 Consolidation
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class TheaCookieManager:
    """
    Cookie-based authentication manager.

    Responsibilities:
    - Save/load cookies from file
    - Validate cookie freshness
    - Load cookies into browser (with proper domain handling)
    - Session validation
    """

    def __init__(self, cookie_file: str | Path):
        """Initialize cookie manager."""
        self.cookie_file = Path(cookie_file)

    def save_cookies(self, driver) -> bool:
        """
        Save cookies from current browser session.

        Args:
            driver: Selenium WebDriver instance

        Returns:
            bool: True if cookies saved successfully
        """
        try:
            cookies = driver.get_cookies()

            # Filter for ChatGPT/OpenAI cookies only
            auth_cookies = []
            for cookie in cookies:
                domain = cookie.get("domain", "").lower()
                name = cookie.get("name", "").lower()

                # Keep authentication-related cookies
                if any(d in domain for d in ["chatgpt.com", "openai.com"]):
                    # Skip analytics
                    if not any(skip in name for skip in ["_ga", "_gid", "_gat"]):
                        auth_cookies.append(cookie)

            # Save to file
            self.cookie_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cookie_file, "w", encoding="utf-8") as f:
                json.dump(auth_cookies, f, indent=2)

            logger.info(f"✅ Saved {len(auth_cookies)} cookies to {self.cookie_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save cookies: {e}")
            return False

    def load_cookies(self, driver) -> bool:
        """
        Load cookies into browser session.

        CRITICAL: Browser MUST be on chatgpt.com domain before calling this!

        Args:
            driver: Selenium WebDriver instance

        Returns:
            bool: True if cookies loaded successfully
        """
        try:
            if not self.cookie_file.exists():
                logger.warning("⚠️  No cookie file found")
                return False

            with open(self.cookie_file, encoding="utf-8") as f:
                cookies = json.load(f)

            if not cookies:
                logger.warning("⚠️  Cookie file is empty")
                return False

            # Load cookies into driver
            loaded_count = 0
            for cookie in cookies:
                try:
                    if "name" in cookie and "value" in cookie:
                        driver.add_cookie(cookie)
                        loaded_count += 1
                except Exception as e:
                    logger.debug(f"Skipped cookie {cookie.get('name')}: {e}")

            logger.info(f"✅ Loaded {loaded_count}/{len(cookies)} cookies")
            return loaded_count > 0

        except Exception as e:
            logger.error(f"❌ Failed to load cookies: {e}")
            return False

    def has_valid_cookies(self) -> bool:
        """
        Check if valid cookies exist.

        Returns:
            bool: True if valid cookies found
        """
        if not self.cookie_file.exists():
            return False

        try:
            with open(self.cookie_file, encoding="utf-8") as f:
                cookies = json.load(f)

            if not cookies or len(cookies) == 0:
                return False

            # Check for unexpired cookies
            now = datetime.now().timestamp()
            valid_cookies = 0

            for cookie in cookies:
                expiry = cookie.get("expiry", 0)
                if expiry == 0 or expiry > now:
                    valid_cookies += 1

            has_valid = valid_cookies > 0
            if has_valid:
                logger.debug(f"✅ Found {valid_cookies} valid cookies")
            else:
                logger.warning("⚠️  All cookies expired")

            return has_valid

        except Exception as e:
            logger.error(f"❌ Failed to validate cookies: {e}")
            return False

    def get_auth_cookies(self) -> list[dict]:
        """
        Get authentication cookies.

        Returns:
            list[dict]: List of authentication cookies
        """
        if not self.cookie_file.exists():
            return []

        try:
            with open(self.cookie_file, encoding="utf-8") as f:
                cookies = json.load(f)

            # Filter for session/auth cookies
            auth_cookies = [
                c
                for c in cookies
                if any(
                    name in c.get("name", "").lower()
                    for name in ["session", "auth", "token", "secure"]
                )
            ]

            return auth_cookies

        except Exception as e:
            logger.error(f"❌ Failed to get auth cookies: {e}")
            return []

    def clear_cookies(self) -> bool:
        """
        Delete cookie file.

        Returns:
            bool: True if cleared successfully
        """
        try:
            if self.cookie_file.exists():
                self.cookie_file.unlink()
                logger.info("✅ Cookies cleared")
                return True
            return False

        except Exception as e:
            logger.error(f"❌ Failed to clear cookies: {e}")
            return False

