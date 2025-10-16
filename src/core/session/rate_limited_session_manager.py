"""
Rate Limited Session Manager - V2 Compliant
===========================================

Session manager with rate limiting capabilities.
Specialized for browser services that require request throttling.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Integration & Core Systems Specialist
Mission: DUP-002 SessionManager Consolidation (consolidates SessionManager + TheaSessionManager)
License: MIT
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from .base_session_manager import BaseSessionManager, BaseSessionInfo


@dataclass
class RateLimitStatus:
    """Rate limit status tracking."""
    requests_remaining: int
    reset_time: Optional[float] = None
    is_rate_limited: bool = False


@dataclass
class RateLimitedSessionInfo(BaseSessionInfo):
    """Extended session info with rate limit tracking."""
    rate_limit_status: Optional[RateLimitStatus] = field(default_factory=lambda: RateLimitStatus(requests_remaining=0))


class RateLimitedSessionManager(BaseSessionManager):
    """
    Session manager with rate limiting.
    
    Manages browser sessions with request throttling and rate limit tracking.
    Consolidates logic from SessionManager and TheaSessionManager.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, logger_name: Optional[str] = None):
        """
        Initialize rate-limited session manager.
        
        Args:
            config: Configuration dictionary with rate limit settings
            logger_name: Custom logger name
        """
        super().__init__(config, logger_name)
        
        # Rate limiting settings
        self.requests_per_minute = self.config.get('rate_limit_requests_per_minute', 10)
        self.burst_limit = self.config.get('burst_limit', 5)
        
        # Rate limit tracking per service
        self.rate_limits: Dict[str, RateLimitStatus] = {}
        
        self.logger.info(f"Rate limiting: {self.requests_per_minute} req/min, burst: {self.burst_limit}")

    def create_session(self, service_name: str, **kwargs) -> Optional[str]:
        """
        Create a new rate-limited session.
        
        Args:
            service_name: Name of service session is for
            **kwargs: Additional session parameters
            
        Returns:
            Session ID if successful, None otherwise
        """
        try:
            # Check max sessions limit
            if len(self.sessions) >= self.max_sessions:
                self.logger.warning(f"Max sessions ({self.max_sessions}) reached, cleaning up expired")
                self.cleanup_expired_sessions()
                
                if len(self.sessions) >= self.max_sessions:
                    self.logger.error("Cannot create session - max sessions limit reached")
                    return None
            
            # Generate session ID
            session_id = self._generate_session_id(service_name)
            
            # Initialize rate limit for this service if not exists
            if service_name not in self.rate_limits:
                self.rate_limits[service_name] = RateLimitStatus(
                    requests_remaining=self.requests_per_minute
                )
            
            # Create session info
            session_info = RateLimitedSessionInfo(
                session_id=session_id,
                service_name=service_name,
                status="active",
                rate_limit_status=self.rate_limits[service_name]
            )
            
            self.sessions[session_id] = session_info
            self.logger.info(f"✅ Created rate-limited session {session_id} for {service_name}")
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to create session for {service_name}: {e}")
            return None

    def validate_session(self, session_id: str) -> bool:
        """
        Validate that a session exists and is active.
        
        Args:
            session_id: Session ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not self.session_exists(session_id):
            self.logger.warning(f"Session validation failed - {session_id} not found")
            return False
        
        session = self.sessions[session_id]
        
        # Check if session is active
        if session.status != "active":
            self.logger.warning(f"Session validation failed - {session_id} not active (status: {session.status})")
            return False
        
        # Check if session has expired
        if time.time() - session.last_activity > self.session_timeout:
            self.logger.warning(f"Session validation failed - {session_id} expired")
            return False
        
        return True

    def can_make_request(self, service_name: str, session_id: str) -> Tuple[bool, str]:
        """
        Check if a request can be made for this session.
        
        Args:
            service_name: Service name
            session_id: Session ID
            
        Returns:
            Tuple of (can_make_request, reason_if_not)
        """
        # Validate session exists
        if not self.session_exists(session_id):
            return False, "Session not found"
        
        # Validate session is active
        if not self.validate_session(session_id):
            return False, "Session not active or expired"
        
        # Check rate limit
        if service_name not in self.rate_limits:
            self.logger.warning(f"Rate limit not configured for {service_name}")
            return False, "Rate limit not configured"
        
        rate_limit = self.rate_limits[service_name]
        
        # Check if rate limited
        if rate_limit.is_rate_limited:
            wait_time = 0
            if rate_limit.reset_time:
                wait_time = rate_limit.reset_time - time.time()
            return False, f"Rate limited (reset in {wait_time:.1f}s)"
        
        # Check requests remaining
        if rate_limit.requests_remaining <= 0:
            return False, "No requests remaining"
        
        return True, ""

    def record_request(self, service_name: str, session_id: str, success: bool = True) -> None:
        """
        Record a request for rate limiting.
        
        Args:
            service_name: Service name
            session_id: Session ID
            success: Whether request was successful
        """
        # Update rate limit
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            rate_limit.requests_remaining -= 1
            
            # Trigger rate limit if exhausted
            if rate_limit.requests_remaining <= 0:
                rate_limit.is_rate_limited = True
                rate_limit.reset_time = time.time() + 60  # Reset in 1 minute
                self.logger.warning(f"⏳ Rate limit triggered for {service_name} (reset in 60s)")
        
        # Update session activity
        self.update_session_activity(session_id)

    def wait_for_rate_limit_reset(self, service_name: str, session_id: str) -> None:
        """
        Wait for rate limit to reset.
        
        Args:
            service_name: Service name
            session_id: Session ID
        """
        if service_name not in self.rate_limits:
            return
        
        rate_limit = self.rate_limits[service_name]
        
        if rate_limit.reset_time:
            wait_time = rate_limit.reset_time - time.time()
            
            if wait_time > 0:
                self.logger.info(f"⏳ Waiting {wait_time:.1f}s for rate limit reset ({service_name})")
                time.sleep(wait_time)
            
            # Reset rate limit
            rate_limit.is_rate_limited = False
            rate_limit.requests_remaining = self.requests_per_minute
            rate_limit.reset_time = None
            self.logger.info(f"✅ Rate limit reset for {service_name}")

    def handle_rate_limit_error(self, service_name: str, session_id: str) -> None:
        """
        Handle a rate limit error from the service.
        
        Immediately triggers rate limiting regardless of local counter.
        
        Args:
            service_name: Service name
            session_id: Session ID
        """
        if service_name in self.rate_limits:
            rate_limit = self.rate_limits[service_name]
            rate_limit.is_rate_limited = True
            rate_limit.requests_remaining = 0
            rate_limit.reset_time = time.time() + 60
            self.logger.warning(f"🚨 Rate limit error detected for {service_name} - throttling enabled")

    def get_rate_limit_status(self, service_name: str) -> Dict[str, Any]:
        """
        Get rate limit status for a service.
        
        Args:
            service_name: Service name
            
        Returns:
            Dictionary with rate limit status
        """
        if service_name not in self.rate_limits:
            return {
                "error": "Service not configured",
                "service_name": service_name
            }
        
        rate_limit = self.rate_limits[service_name]
        
        return {
            "service_name": service_name,
            "requests_remaining": rate_limit.requests_remaining,
            "reset_time": rate_limit.reset_time,
            "is_rate_limited": rate_limit.is_rate_limited,
            "requests_per_minute": self.requests_per_minute,
            "burst_limit": self.burst_limit
        }

    def reset_rate_limit(self, service_name: str) -> bool:
        """
        Manually reset rate limit for a service.
        
        Args:
            service_name: Service name
            
        Returns:
            True if successful, False if service not found
        """
        if service_name not in self.rate_limits:
            return False
        
        rate_limit = self.rate_limits[service_name]
        rate_limit.is_rate_limited = False
        rate_limit.requests_remaining = self.requests_per_minute
        rate_limit.reset_time = None
        
        self.logger.info(f"✅ Manually reset rate limit for {service_name}")
        return True

