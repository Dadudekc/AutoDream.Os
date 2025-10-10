#!/usr/bin/env python3
"""
Thea Session Management - V2 Compliance
=======================================

Unified session, cookie, and rate limit management for Thea automation.
Consolidates: cookie_manager, session_manager, thea_cookie_manager, thea_session_manager

Author: Agent-3 (Infrastructure & DevOps) - Browser Consolidation
License: MIT
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from .browser_models import SessionInfo, RateLimitStatus

logger = logging.getLogger(__name__)


class TheaSessionManagement:
    """Unified session, cookie, and rate limit management."""

    def __init__(self, cookie_file: str = "data/thea_cookies.json", 
                 requests_per_minute: int = 10):
        """Initialize session management."""
        self.cookie_file = cookie_file
        self.requests_per_minute = requests_per_minute
        
        # Cookie storage
        self.cookies: Dict[str, List[Dict]] = {}
        
        # Session tracking
        self.sessions: Dict[str, SessionInfo] = {}
        
        # Rate limiting
        self.rate_limits: Dict[str, RateLimitStatus] = {}
        
        # Auto-load persisted cookies
        self._load_persisted_cookies()

    # ========== Cookie Management ==========
    
    def save_cookies(self, driver: Any, service_name: str) -> bool:
        """Save cookies for a service from browser driver."""
        try:
            if not driver:
                return False
            
            # Get cookies from driver (handle both Selenium driver and dict)
            if hasattr(driver, 'get_cookies'):
                cookies = driver.get_cookies()
            else:
                # Driver is already a cookies dict/list
                return False
            
            if cookies:
                self.cookies[service_name] = cookies
                self._persist_cookies()
                logger.info(f"✅ Saved {len(cookies)} cookies for {service_name}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to save cookies for {service_name}: {e}")
            return False

    def load_cookies(self, driver: Any, service_name: str) -> bool:
        """Load cookies for a service into browser driver."""
        try:
            if not driver or service_name not in self.cookies:
                return False
            
            # Add cookies to driver
            for cookie in self.cookies[service_name]:
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    logger.debug(f"Could not add cookie: {e}")
            
            logger.info(f"✅ Loaded cookies for {service_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load cookies for {service_name}: {e}")
            return False

    def has_valid_session(self, service_name: str) -> bool:
        """Check if there's a valid session for the service."""
        return service_name in self.cookies and len(self.cookies[service_name]) > 0

    def get_session_info_from_cookies(self, service_name: str) -> Dict[str, Any]:
        """Get session info from cookies."""
        if service_name in self.cookies:
            return {
                "status": "active",
                "cookie_count": len(self.cookies[service_name]),
                "service_name": service_name
            }
        return {"status": "unknown"}

    def _persist_cookies(self) -> bool:
        """Persist cookies to file."""
        try:
            Path(self.cookie_file).parent.mkdir(parents=True, exist_ok=True)
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
                with open(self.cookie_file, "r") as f:
                    self.cookies = json.load(f)
                logger.info(f"✅ Loaded persisted cookies from {self.cookie_file}")
                return True
            return False
        except Exception as e:
            logger.debug(f"Could not load persisted cookies: {e}")
            return False

    # ========== Session Management ==========
    
    def create_session(self, service_name: str) -> Optional[str]:
        """Create a new session for a service."""
        session_id = f"{service_name}_{int(time.time())}_{hash(service_name) % 1000}"
        
        session_info = SessionInfo(
            session_id=session_id,
            service_name=service_name,
            status="active"
        )
        
        self.sessions[session_id] = session_info
        
        # Initialize rate limiting
        self.rate_limits[service_name] = RateLimitStatus(
            requests_remaining=self.requests_per_minute
        )
        
        logger.info(f"✅ Created session {session_id} for {service_name}")
        return session_id

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
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
        return {"error": "Session not found"}

    def end_session(self, session_id: str) -> bool:
        """End a session."""
        if session_id in self.sessions:
            self.sessions[session_id].status = "ended"
            logger.info(f"✅ Ended session {session_id}")
            return True
        return False

    # ========== Rate Limiting ==========
    
    def can_make_request(self, service_name: str, session_id: str) -> Tuple[bool, str]:
        """Check if a request can be made."""
        if session_id not in self.sessions:
            return False, "Session not found"
        
        if service_name not in self.rate_limits:
            return False, "Rate limit not configured"
        
        rate_limit = self.rate_limits[service_name]
        
        # Check if rate limited
        if rate_limit.is_rate_limited:
            # Check if reset time has passed
            if rate_limit.reset_time and time.time() > rate_limit.reset_time:
                rate_limit.is_rate_limited = False
                rate_limit.requests_remaining = self.requests_per_minute
                rate_limit.reset_time = None
            else:
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
                    rate_limit.requests_remaining = self.requests_per_minute
                    rate_limit.reset_time = None

    def handle_rate_limit_error(self, service_name: str, session_id: str) -> None:
        """Handle rate limit error."""
        logger.warning(f"⚠️  Rate limit hit for {service_name}")
        self.wait_for_rate_limit_reset(service_name, session_id)

    def get_rate_limit_status(self, service_name: str) -> Dict[str, Any]:
        """Get rate limit status for a service."""
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            return {
                "requests_remaining": rate_limit.requests_remaining,
                "reset_time": rate_limit.reset_time,
                "is_rate_limited": rate_limit.is_rate_limited
            }
        return {"error": "Service not configured"}

    # ========== Cleanup ==========
    
    def cleanup_old_sessions(self, max_age_seconds: int = 3600) -> int:
        """Clean up old inactive sessions."""
        current_time = time.time()
        removed_count = 0
        
        to_remove = []
        for session_id, session in self.sessions.items():
            age = current_time - (session.last_activity or session.created_at)
            if age > max_age_seconds:
                to_remove.append(session_id)
        
        for session_id in to_remove:
            del self.sessions[session_id]
            removed_count += 1
        
        if removed_count > 0:
            logger.info(f"✅ Cleaned up {removed_count} old sessions")
        
        return removed_count


# Factory function
def create_thea_session_management(cookie_file: str = "data/thea_cookies.json",
                                   requests_per_minute: int = 10) -> TheaSessionManagement:
    """Create Thea session management instance."""
    return TheaSessionManagement(cookie_file, requests_per_minute)


__all__ = ['TheaSessionManagement', 'create_thea_session_management']


