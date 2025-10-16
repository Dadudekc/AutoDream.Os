"""
Base Session Manager - V2 Compliant
====================================

Abstract base class for all session managers.
Provides common session tracking, configuration, and logging infrastructure.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Integration & Core Systems Specialist
Mission: DUP-002 SessionManager Consolidation
License: MIT
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class BaseSessionInfo:
    """
    Base session information structure.
    
    Can be extended by specialized session managers for additional fields.
    """
    session_id: str
    service_name: str
    status: str = "active"
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    request_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseSessionManager(ABC):
    """
    Abstract base class for session managers.
    
    Provides common infrastructure:
    - Session tracking and lifecycle management
    - Configuration management
    - Logging infrastructure
    - Session info retrieval
    - Basic validation
    
    Subclasses must implement:
    - create_session: Create a new session
    - validate_session: Validate session is still active
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, logger_name: Optional[str] = None):
        """
        Initialize base session manager.
        
        Args:
            config: Configuration dictionary (implementation-specific)
            logger_name: Custom logger name (defaults to class module name)
        """
        self.config = config or {}
        self.logger = logging.getLogger(logger_name or __name__)
        
        # Session tracking
        self.sessions: Dict[str, BaseSessionInfo] = {}
        self.session_count = 0
        
        # Settings from config
        self.persistent = self.config.get('persistent', False)
        self.session_timeout = self.config.get('session_timeout', 3600)  # 1 hour default
        self.max_sessions = self.config.get('max_sessions', 100)
        
        self.logger.info(f"Initialized {self.__class__.__name__}")

    @abstractmethod
    def create_session(self, service_name: str, **kwargs) -> Optional[str]:
        """
        Create a new session.
        
        Args:
            service_name: Name of service session is for
            **kwargs: Implementation-specific parameters
            
        Returns:
            Session ID if successful, None otherwise
        """
        pass

    @abstractmethod
    def validate_session(self, session_id: str) -> bool:
        """
        Validate that a session is still active and valid.
        
        Args:
            session_id: Session ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """
        Get information about a session.
        
        Args:
            session_id: Session ID to retrieve info for
            
        Returns:
            Dictionary with session information
        """
        if session_id not in self.sessions:
            return {
                "error": "Session not found",
                "session_id": session_id
            }
        
        session = self.sessions[session_id]
        return {
            "session_id": session.session_id,
            "service_name": session.service_name,
            "status": session.status,
            "created_at": session.created_at,
            "last_activity": session.last_activity,
            "request_count": session.request_count,
            "age_seconds": time.time() - session.created_at,
            "idle_seconds": time.time() - session.last_activity,
            "metadata": session.metadata
        }

    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.
        
        Args:
            session_id: Session ID to check
            
        Returns:
            True if exists, False otherwise
        """
        return session_id in self.sessions

    def update_session_activity(self, session_id: str) -> bool:
        """
        Update last activity timestamp for a session.
        
        Args:
            session_id: Session ID to update
            
        Returns:
            True if successful, False if session not found
        """
        if session_id not in self.sessions:
            self.logger.warning(f"Cannot update activity - session {session_id} not found")
            return False
        
        self.sessions[session_id].last_activity = time.time()
        self.sessions[session_id].request_count += 1
        return True

    def close_session(self, session_id: str) -> bool:
        """
        Close a session and clean up resources.
        
        Args:
            session_id: Session ID to close
            
        Returns:
            True if successful, False if session not found
        """
        if session_id not in self.sessions:
            self.logger.warning(f"Cannot close - session {session_id} not found")
            return False
        
        self.sessions[session_id].status = "closed"
        self.logger.info(f"Closed session {session_id}")
        return True

    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions based on timeout.
        
        Returns:
            Number of sessions cleaned up
        """
        current_time = time.time()
        expired = []
        
        for session_id, session in self.sessions.items():
            if session.status == "closed":
                expired.append(session_id)
            elif current_time - session.last_activity > self.session_timeout:
                expired.append(session_id)
                self.logger.info(f"Session {session_id} expired (timeout: {self.session_timeout}s)")
        
        # Remove expired sessions
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            self.logger.info(f"Cleaned up {len(expired)} expired sessions")
        
        return len(expired)

    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all sessions.
        
        Returns:
            Dictionary mapping session_id to session info
        """
        return {
            session_id: self.get_session_info(session_id)
            for session_id in self.sessions.keys()
        }

    def get_active_session_count(self) -> int:
        """
        Get count of active sessions.
        
        Returns:
            Number of active sessions
        """
        return sum(1 for s in self.sessions.values() if s.status == "active")

    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get statistics about session manager.
        
        Returns:
            Dictionary with session statistics
        """
        active_count = self.get_active_session_count()
        
        return {
            "manager_class": self.__class__.__name__,
            "total_sessions": len(self.sessions),
            "active_sessions": active_count,
            "closed_sessions": len(self.sessions) - active_count,
            "session_timeout": self.session_timeout,
            "max_sessions": self.max_sessions,
            "persistent": self.persistent,
            "session_count_lifetime": self.session_count
        }

    def _generate_session_id(self, service_name: str) -> str:
        """
        Generate a unique session ID.
        
        Args:
            service_name: Service name to include in ID
            
        Returns:
            Unique session ID
        """
        self.session_count += 1
        timestamp = int(time.time() * 1000)
        hash_part = hash(f"{service_name}_{timestamp}_{self.session_count}") % 10000
        return f"{service_name}_{timestamp}_{hash_part}"

    def __repr__(self) -> str:
        """String representation of session manager."""
        return (
            f"<{self.__class__.__name__} "
            f"sessions={len(self.sessions)} "
            f"active={self.get_active_session_count()}>"
        )

