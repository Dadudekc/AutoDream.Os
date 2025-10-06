#!/usr/bin/env python3
"""
Cookie Manager for Browser Service
==================================

Manages browser cookies for session persistence.
V2 Compliant: ≤400 lines, focused cookie operations.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from .browser_adapter import BrowserAdapter

logger = logging.getLogger(__name__)


class CookieManager:
    """Manages browser cookies for sessions."""

    def __init__(self, cookie_file: str = "data/thea_cookies.json", auto_save: bool = True):
        """Initialize cookie manager."""
        self.cookie_file = cookie_file
        self.auto_save = auto_save
        self.cookies: Dict[str, List[Dict]] = {}
        self._load_cookies_from_file()

    def save_cookies(self, browser_adapter: BrowserAdapter, service_name: str) -> bool:
        """Save cookies for a service."""
        if not browser_adapter.is_running():
            return False

        try:
            # Get cookies from browser
            cookies = browser_adapter.get_cookies()
            if cookies:
                self.cookies[service_name] = cookies

            if self.auto_save:
                return self._persist_cookies()

            return True

        except Exception as e:
            logger.error(f"❌ Failed to save cookies for {service_name}: {e}")
            return False

    def load_cookies(self, browser_adapter: BrowserAdapter, service_name: str) -> bool:
        """Load cookies for a service."""
        if not browser_adapter.is_running():
            return False

        try:
            if service_name in self.cookies:
                # Load cookies into browser
                browser_adapter.add_cookies(self.cookies[service_name])
                return True
            return False

        except Exception as e:
            logger.error(f"❌ Failed to load cookies for {service_name}: {e}")
            return False

    def has_valid_session(self, service_name: str) -> bool:
        """Check if there's a valid session for the service."""
        return service_name in self.cookies and len(self.cookies[service_name]) > 0

    def _persist_cookies(self) -> bool:
        """Persist cookies to file."""
        try:
            # Ensure directory exists
            cookie_path = Path(self.cookie_file)
            cookie_path.parent.mkdir(parents=True, exist_ok=True)

            # Save cookies to file
            with open(self.cookie_file, 'w') as f:
                json.dump(self.cookies, f, indent=2)

            logger.info(f"✅ Cookies saved to {self.cookie_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to persist cookies: {e}")
            return False

    def _load_cookies_from_file(self) -> bool:
        """Load cookies from file."""
        try:
            cookie_path = Path(self.cookie_file)
            if not cookie_path.exists():
                return True

            with open(self.cookie_file, 'r') as f:
                self.cookies = json.load(f)

            logger.info(f"✅ Cookies loaded from {self.cookie_file}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to load cookies from file: {e}")
            return False

    def clear_cookies(self, service_name: Optional[str] = None) -> bool:
        """Clear cookies for a service or all services."""
        try:
            if service_name:
                if service_name in self.cookies:
                    del self.cookies[service_name]
                    logger.info(f"✅ Cleared cookies for {service_name}")
                else:
                    logger.warning(f"⚠️ No cookies found for {service_name}")
            else:
                self.cookies.clear()
                logger.info("✅ Cleared all cookies")

            if self.auto_save:
                return self._persist_cookies()

            return True

        except Exception as e:
            logger.error(f"❌ Failed to clear cookies: {e}")
            return False

    def get_cookie_count(self, service_name: str) -> int:
        """Get number of cookies for a service."""
        if service_name in self.cookies:
            return len(self.cookies[service_name])
        return 0

    def get_all_services(self) -> List[str]:
        """Get list of all services with cookies."""
        return list(self.cookies.keys())

    def get_cookie_summary(self) -> Dict[str, int]:
        """Get summary of cookies by service."""
        return {service: len(cookies) for service, cookies in self.cookies.items()}


def create_cookie_manager(cookie_file: str = "data/thea_cookies.json", auto_save: bool = True) -> CookieManager:
    """Create cookie manager with specified settings."""
    return CookieManager(cookie_file=cookie_file, auto_save=auto_save)

