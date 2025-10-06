#!/usr/bin/env python3
"""
Session Manager for Browser Service
==================================

Manages browser sessions and rate limiting.
V2 Compliant: ≤400 lines, focused session operations.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import time
import logging
from typing import Dict, List, Optional, Tuple

from .browser_service_models import SessionInfo, RateLimitStatus, TheaConfig

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages browser sessions and rate limiting."""

    def __init__(self, thea_config: TheaConfig):
        """Initialize session manager."""
        self.thea_config = thea_config
        self.sessions: Dict[str, SessionInfo] = {}
        self.rate_limits: Dict[str, RateLimitStatus] = {}

    def create_session(self, service_name: str) -> Optional[str]:
        """Create a new session."""
        try:
            session_id = f"{service_name}_{int(time.time())}"
            session_info = SessionInfo(
                session_id=session_id,
                service_name=service_name,
                status="active"
            )
            
            self.sessions[session_id] = session_info
            
            # Initialize rate limit for service
            if service_name not in self.rate_limits:
                self.rate_limits[service_name] = RateLimitStatus(
                    requests_remaining=self.thea_config.rate_limit_requests_per_minute
                )
            
            logger.info(f"✅ Created session {session_id} for {service_name}")
            return session_id

        except Exception as e:
            logger.error(f"❌ Failed to create session for {service_name}: {e}")
            return None

    def can_make_request(self, service_name: str, session_id: str) -> Tuple[bool, str]:
        """Check if a request can be made."""
        try:
            # Check if session exists
            if session_id not in self.sessions:
                return False, "Session not found"

            session = self.sessions[session_id]
            if session.status != "active":
                return False, f"Session status: {session.status}"

            # Check rate limit
            if service_name in self.rate_limits:
                rate_limit = self.rate_limits[service_name]
                if rate_limit.is_rate_limited:
                    return False, "Rate limited"
                
                if rate_limit.requests_remaining <= 0:
                    return False, "No requests remaining"

            return True, "OK"

        except Exception as e:
            logger.error(f"❌ Error checking request permission: {e}")
            return False, f"Error: {e}"

    def record_request(self, service_name: str, session_id: str, success: bool = True) -> None:
        """Record a request."""
        try:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                session.request_count += 1
                session.last_activity = time.time()

            # Update rate limit
            if service_name in self.rate_limits:
                rate_limit = self.rate_limits[service_name]
                if rate_limit.requests_remaining > 0:
                    rate_limit.requests_remaining -= 1

        except Exception as e:
            logger.error(f"❌ Failed to record request: {e}")

    def get_session_info(self, session_id: str) -> Dict[str, any]:
        """Get session information."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            return {
                "session_id": session.session_id,
                "service_name": session.service_name,
                "status": session.status,
                "created_at": session.created_at,
                "last_activity": session.last_activity,
                "request_count": session.request_count
            }
        return {}

    def get_rate_limit_status(self, service_name: str) -> Dict[str, any]:
        """Get rate limit status."""
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            return {
                "requests_remaining": rate_limit.requests_remaining,
                "reset_time": rate_limit.reset_time,
                "is_rate_limited": rate_limit.is_rate_limited
            }
        return {
            "requests_remaining": self.thea_config.rate_limit_requests_per_minute,
            "reset_time": None,
            "is_rate_limited": False
        }

    def update_session_status(self, session_id: str, status: str) -> bool:
        """Update session status."""
        try:
            if session_id in self.sessions:
                self.sessions[session_id].status = status
                logger.info(f"✅ Updated session {session_id} status to {status}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to update session status: {e}")
            return False

    def cleanup_expired_sessions(self, max_age: float = 3600) -> int:
        """Clean up expired sessions."""
        try:
            current_time = time.time()
            expired_sessions = []
            
            for session_id, session in self.sessions.items():
                if current_time - session.last_activity > max_age:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del self.sessions[session_id]
            
            if expired_sessions:
                logger.info(f"✅ Cleaned up {len(expired_sessions)} expired sessions")
            
            return len(expired_sessions)
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup expired sessions: {e}")
            return 0

    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs."""
        return [session_id for session_id, session in self.sessions.items() 
                if session.status == "active"]

    def get_session_count(self) -> int:
        """Get total number of sessions."""
        return len(self.sessions)

    def get_service_sessions(self, service_name: str) -> List[str]:
        """Get sessions for a specific service."""
        return [session_id for session_id, session in self.sessions.items() 
                if session.service_name == service_name]


def create_session_manager(thea_config: TheaConfig) -> SessionManager:
    """Create session manager with Thea configuration."""
    return SessionManager(thea_config)

