"""
Session Manager - Unified Browser Service
==========================================

Manages browser sessions and rate limiting.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

import logging
import time
from typing import Any

from .browser_models import RateLimitStatus, SessionInfo, TheaConfig

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages browser sessions and rate limiting."""

    def __init__(self, config: TheaConfig):
        """Initialize session manager."""
        self.config = config
        self.sessions: dict[str, SessionInfo] = {}
        self.rate_limits: dict[str, RateLimitStatus] = {}

    def create_session(self, service_name: str) -> str | None:
        """Create a new session for a service."""
        session_id = f"{service_name}_{int(time.time())}_{hash(service_name) % 1000}"

        session_info = SessionInfo(
            session_id=session_id, service_name=service_name, status="active"
        )

        self.sessions[session_id] = session_info
        self.rate_limits[service_name] = RateLimitStatus(
            requests_remaining=self.config.rate_limit_requests_per_minute
        )

        logger.info(f"✅ Created session {session_id} for {service_name}")
        return session_id

    def can_make_request(self, service_name: str, session_id: str) -> tuple[bool, str]:
        """Check if a request can be made."""
        if session_id not in self.sessions:
            return False, "Session not found"

        if service_name not in self.rate_limits:
            return False, "Rate limit not configured"

        rate_limit = self.rate_limits[service_name]
        if rate_limit.is_rate_limited:
            return False, "Rate limited"

        if rate_limit.requests_remaining <= 0:
            return False, "No requests remaining"

        return True, ""

    def record_request(self, service_name: str, session_id: str, success: bool) -> None:
        """Record a request for rate limiting."""
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            rate_limit.requests_remaining -= 1

            if rate_limit.requests_remaining <= 0:
                rate_limit.is_rate_limited = True
                rate_limit.reset_time = time.time() + 60  # Reset in 1 minute

        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.last_activity = time.time()
            session.request_count += 1

    def wait_for_rate_limit_reset(self, service_name: str, session_id: str) -> None:
        """Wait for rate limit to reset."""
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            if rate_limit.reset_time:
                wait_time = rate_limit.reset_time - time.time()
                if wait_time > 0:
                    logger.info(f"⏳ Waiting {wait_time:.1f}s for rate limit reset")
                    time.sleep(wait_time)
                    rate_limit.is_rate_limited = False
                    rate_limit.requests_remaining = self.config.rate_limit_requests_per_minute
                    rate_limit.reset_time = None

    def get_session_info(self, session_id: str) -> dict[str, Any]:
        """Get session information."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            return {
                "session_id": session.session_id,
                "service_name": session.service_name,
                "status": session.status,
                "created_at": session.created_at,
                "last_activity": session.last_activity,
                "request_count": session.request_count,
            }
        return {"error": "Session not found"}

    def get_rate_limit_status(self, service_name: str) -> dict[str, Any]:
        """Get rate limit status for a service."""
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            return {
                "requests_remaining": rate_limit.requests_remaining,
                "reset_time": rate_limit.reset_time,
                "is_rate_limited": rate_limit.is_rate_limited,
            }
        return {"error": "Service not configured"}
