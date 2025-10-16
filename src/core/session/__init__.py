"""
Session Management - V2 Compliant
=================================

Unified session management infrastructure.
Provides base classes and specialized implementations for different session types.

DUP-002 SessionManager Consolidation Complete:
- BaseSessionManager: Abstract base class (session tracking, config, logging)
- RateLimitedSessionManager: Rate-limited sessions (consolidates SessionManager + TheaSessionManager)
- BrowserSessionManager: Browser automation (ChatGPT cookies/auth) - refactored to use base

Legacy classes (src.infrastructure.browser_backup) now use these implementations.

Exports:
    - BaseSessionManager: Abstract base for all session managers
    - BaseSessionInfo: Base session information structure
    - RateLimitedSessionManager: Rate-limited session manager
    - RateLimitStatus: Rate limit status tracking
    - RateLimitedSessionInfo: Extended session info with rate limits

Author: Agent-1 - Integration & Core Systems Specialist
Mission: DUP-002 SessionManager Consolidation
License: MIT
"""

from .base_session_manager import BaseSessionManager, BaseSessionInfo
from .rate_limited_session_manager import (
    RateLimitedSessionManager,
    RateLimitStatus,
    RateLimitedSessionInfo,
)

__all__ = [
    "BaseSessionManager",
    "BaseSessionInfo",
    "RateLimitedSessionManager",
    "RateLimitStatus",
    "RateLimitedSessionInfo",
]

__version__ = "2.0.0"

