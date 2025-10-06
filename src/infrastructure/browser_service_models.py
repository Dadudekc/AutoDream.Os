#!/usr/bin/env python3
"""
Browser Service Data Models
===========================

Data models and configuration classes for browser service.
V2 Compliant: ≤400 lines, focused data structures.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Tuple

# Import enhanced unified configuration system
from ..core.enhanced_unified_config import get_enhanced_config

# Get enhanced unified config instance
_unified_config = get_enhanced_config()


@dataclass
class BrowserConfig:
    """Configuration for browser operations with enhanced config integration."""
    headless: bool = False  # Use enhanced config for browser settings
    user_data_dir: Optional[str] = None
    window_size: Tuple[int, int] = (1920, 1080)
    timeout: float = _unified_config.get_timeout_config().get('SCRAPE_TIMEOUT', 30.0)
    implicit_wait: float = _unified_config.get_timeout_config().get('QUALITY_CHECK_INTERVAL', 10.0)
    page_load_timeout: float = _unified_config.get_timeout_config().get('RESPONSE_WAIT_TIMEOUT', 120.0)


@dataclass
class TheaConfig:
    """Configuration for Thea Manager interactions with enhanced config integration."""
    conversation_url: str = "https://chat.openai.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
    cookie_file: str = "data/thea_cookies.json"
    auto_save_cookies: bool = True
    rate_limit_requests_per_minute: int = 10
    rate_limit_burst_limit: int = 5


@dataclass
class SessionInfo:
    """Session information."""
    session_id: str
    service_name: str
    status: str
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    request_count: int = 0


@dataclass
class RateLimitStatus:
    """Rate limit status information."""
    requests_remaining: int
    reset_time: Optional[float] = None
    is_rate_limited: bool = False


@dataclass
class BrowserStatus:
    """Browser status information."""
    is_running: bool = False
    current_url: str = ""
    page_title: str = ""
    session_count: int = 0
    services_with_cookies: List[str] = field(default_factory=list)
    page_status: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationResult:
    """Result of browser operations."""
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[str] = None


# Factory functions for creating configurations
def create_browser_config(
    headless: bool = False,
    user_data_dir: Optional[str] = None,
    window_size: Tuple[int, int] = (1920, 1080)
) -> BrowserConfig:
    """Create browser configuration with default values."""
    return BrowserConfig(
        headless=headless,
        user_data_dir=user_data_dir,
        window_size=window_size
    )


def create_thea_config(
    conversation_url: str = "https://chat.openai.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager",
    cookie_file: str = "data/thea_cookies.json"
) -> TheaConfig:
    """Create Thea configuration with default values."""
    return TheaConfig(
        conversation_url=conversation_url,
        cookie_file=cookie_file
    )


def create_session_info(session_id: str, service_name: str, status: str = "active") -> SessionInfo:
    """Create session information."""
    return SessionInfo(
        session_id=session_id,
        service_name=service_name,
        status=status
    )


def create_rate_limit_status(requests_remaining: int) -> RateLimitStatus:
    """Create rate limit status."""
    return RateLimitStatus(requests_remaining=requests_remaining)


def create_browser_status() -> BrowserStatus:
    """Create browser status."""
    return BrowserStatus()


def create_operation_result(success: bool, message: str = "", data: Any = None, error: str = None) -> OperationResult:
    """Create operation result."""
    return OperationResult(
        success=success,
        message=message,
        data=data,
        error=error
    )

