#!/usr/bin/env python3
"""
Session Manager
===============

Manages browser sessions and rate limiting.
"""

import logging
import time
from collections import defaultdict
from typing import Any

from ..config.browser_config import RateLimitStatus, SessionInfo, TheaConfig

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages browser sessions and rate limiting."""

    def __init__(self, config: TheaConfig):
        """Initialize session manager."""
        self.config = config
        self.sessions: dict[str, SessionInfo] = {}
        self.rate_limits: dict[str, RateLimitStatus] = defaultdict(
            lambda: RateLimitStatus(service_name="")
        )

    def create_session(self, service_name: str) -> str | None:
        """Create a new session for a service."""
        try:
            session_id = f"{service_name}_{int(time.time())}"
            session_info = SessionInfo(session_id=session_id, service_name=service_name)

            self.sessions[session_id] = session_info

            # Initialize rate limit status
            if service_name not in self.rate_limits:
                self.rate_limits[service_name] = RateLimitStatus(service_name=service_name)

            logger.info(f"Created session {session_id} for {service_name}")
            return session_id

        except Exception as e:
            logger.error(f"Failed to create session for {service_name}: {e}")
            return None

    def can_make_request(self, service_name: str, session_id: str) -> tuple[bool, str]:
        """Check if a request can be made within rate limits."""
        try:
            if session_id not in self.sessions:
                return False, "Session not found"

            rate_limit = self.rate_limits[service_name]
            current_time = time.time()

            # Check minute rate limit
            if rate_limit.requests_this_minute >= self.config.rate_limit_requests_per_minute:
                time_since_last = current_time - rate_limit.last_request_time
                if time_since_last < 60:
                    return (
                        False,
                        f"Rate limit exceeded: {rate_limit.requests_this_minute} requests per minute",
                    )

            # Check hour rate limit
            if rate_limit.requests_this_hour >= self.config.rate_limit_requests_per_hour:
                time_since_last = current_time - rate_limit.last_request_time
                if time_since_last < 3600:
                    return (
                        False,
                        f"Rate limit exceeded: {rate_limit.requests_this_hour} requests per hour",
                    )

            return True, "OK"

        except Exception as e:
            logger.error(f"Error checking rate limit for {service_name}: {e}")
            return False, f"Error: {e}"

    def record_request(self, service_name: str, session_id: str, success: bool) -> None:
        """Record a request for rate limiting."""
        try:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                session.last_activity = time.time()
                session.request_count += 1

                if success:
                    session.success_count += 1
                else:
                    session.failure_count += 1

            # Update rate limit status
            rate_limit = self.rate_limits[service_name]
            current_time = time.time()

            # Reset counters if needed
            if current_time - rate_limit.last_request_time >= 60:
                rate_limit.requests_this_minute = 0
            if current_time - rate_limit.last_request_time >= 3600:
                rate_limit.requests_this_hour = 0

            rate_limit.requests_this_minute += 1
            rate_limit.requests_this_hour += 1
            rate_limit.last_request_time = current_time

        except Exception as e:
            logger.error(f"Error recording request for {service_name}: {e}")

    def wait_for_rate_limit_reset(self, service_name: str, session_id: str) -> None:
        """Wait for rate limit to reset."""
        try:
            rate_limit = self.rate_limits[service_name]
            current_time = time.time()

            # Calculate wait time
            wait_time = 60 - (current_time - rate_limit.last_request_time)
            if wait_time > 0:
                logger.info(f"Waiting {wait_time:.1f} seconds for rate limit reset")
                time.sleep(wait_time)

        except Exception as e:
            logger.error(f"Error waiting for rate limit reset: {e}")

    def get_session_info(self, session_id: str) -> dict[str, Any]:
        """Get session information."""
        if session_id not in self.sessions:
            return {}

        session = self.sessions[session_id]
        return {
            "session_id": session.session_id,
            "service_name": session.service_name,
            "created_at": session.created_at,
            "last_activity": session.last_activity,
            "request_count": session.request_count,
            "success_count": session.success_count,
            "failure_count": session.failure_count,
        }

    def get_rate_limit_status(self, service_name: str) -> dict[str, Any]:
        """Get rate limit status for a service."""
        rate_limit = self.rate_limits[service_name]
        return {
            "service_name": service_name,
            "requests_this_minute": rate_limit.requests_this_minute,
            "requests_this_hour": rate_limit.requests_this_hour,
            "last_request_time": rate_limit.last_request_time,
            "is_limited": rate_limit.is_limited,
            "reset_time": rate_limit.reset_time,
        }
