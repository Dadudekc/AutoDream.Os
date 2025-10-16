"""
Thea Session Manager
===================

Basic session manager for Thea Manager rate limiting.

DEPRECATED: This stub is now replaced by RateLimitedSessionManager.
Please use src.core.session.RateLimitedSessionManager directly.

Author: Agent-1 (DUP-002) - Deprecated in favor of consolidated session manager
"""

import warnings
from dataclasses import dataclass
from typing import Any


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""

    requests_per_minute: int = 10
    burst_limit: int = 5


class TheaSessionManager:
    """
    Basic session manager stub.
    
    DEPRECATED: Use RateLimitedSessionManager from src.core.session instead.
    This stub is kept for backward compatibility only.
    """

    def __init__(self, config: RateLimitConfig | None = None):
        """
        Initialize Thea session manager.
        
        DEPRECATED: Migrating to RateLimitedSessionManager.
        """
        warnings.warn(
            "TheaSessionManager is deprecated. Use RateLimitedSessionManager from src.core.session instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self.config = config or RateLimitConfig()

    def start(self) -> None:
        """Stub start method."""
        pass

    def stop(self) -> None:
        """Stub stop method."""
        pass

    def create_session(self, service_name: str) -> str | None:
        """Stub session creation."""
        return "test_session_123"

    def can_make_request(self, service_name: str, session_id: str) -> tuple[bool, str]:
        """Stub rate limit check."""
        return True, ""

    def record_request(self, service_name: str, session_id: str, success: bool) -> None:
        """Stub request recording."""
        pass

    def wait_for_rate_limit_reset(self, service_name: str, session_id: str) -> None:
        """Stub rate limit waiting."""
        pass

    def handle_rate_limit_error(self, service_name: str, session_id: str) -> None:
        """Stub rate limit error handling."""
        pass

    def get_session_info(self, session_id: str) -> dict[str, Any]:
        """Stub session info."""
        return {"session_id": session_id, "status": "active"}

    def get_rate_limit_status(self, service_name: str) -> dict[str, Any]:
        """Stub rate limit status."""
        return {"requests_remaining": 10, "reset_time": None}
