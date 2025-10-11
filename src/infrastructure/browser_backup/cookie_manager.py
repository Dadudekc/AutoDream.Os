"""
Cookie Manager - Unified Browser Service
=========================================

Manages browser cookies for sessions.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

import json
import logging
import os

from .browser_adapter import BrowserAdapter

logger = logging.getLogger(__name__)


class CookieManager:
    """Manages browser cookies for sessions."""

    def __init__(self, cookie_file: str = "data/thea_cookies.json", auto_save: bool = True):
        """Initialize cookie manager."""
        self.cookie_file = cookie_file
        self.auto_save = auto_save
        self.cookies: dict[str, list[dict]] = {}

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
            os.makedirs(os.path.dirname(self.cookie_file), exist_ok=True)
            with open(self.cookie_file, "w") as f:
                json.dump(self.cookies, f, indent=2)
            return True

        except Exception as e:
            logger.error(f"❌ Failed to persist cookies: {e}")
            return False

    def _load_persisted_cookies(self) -> bool:
        """Load persisted cookies from file."""
        try:
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file) as f:
                    self.cookies = json.load(f)
                return True
            return False

        except Exception as e:
            logger.error(f"❌ Failed to load persisted cookies: {e}")
            return False
