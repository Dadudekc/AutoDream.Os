"""
Thea Login Handler
==================

Basic login handler for Thea Manager authentication.
"""

from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class TheaLoginConfig:
    """Configuration for Thea login."""
    max_retries: int = 3
    login_timeout_s: float = 30.0


class TheaLoginHandler:
    """Basic login handler stub."""

    def __init__(self, config: Optional[TheaLoginConfig] = None):
        self.config = config or TheaLoginConfig()

    def ensure_authenticated(self, driver: Any, url: str, allow_manual: bool = True) -> bool:
        """Stub authentication method."""
        return True

    def _is_authenticated(self, driver: Any, url: str) -> bool:
        """Stub authentication check."""
        return True