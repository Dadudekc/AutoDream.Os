"""
Thea Cookie Manager
==================

Basic cookie manager for Thea Manager sessions.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class TheaCookieConfig:
    """Configuration for Thea cookie management."""

    cookie_file: str = "data/thea_cookies.json"
    auto_save: bool = True


class TheaCookieManager:
    """Basic cookie manager stub."""

    def __init__(self, config: TheaCookieConfig | None = None):
        self.config = config or TheaCookieConfig()

    def save_cookies(self, driver: Any, service_name: str) -> None:
        """Stub cookie saving."""
        pass

    def load_cookies(self, driver: Any, service_name: str) -> None:
        """Stub cookie loading."""
        pass

    def has_valid_session(self, service_name: str) -> bool:
        """Stub session validation."""
        return False

    def get_session_info(self, service_name: str) -> dict[str, Any]:
        """Stub session info."""
        return {"status": "unknown"}
