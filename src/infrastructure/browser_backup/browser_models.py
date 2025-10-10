"""
Browser Models - Unified Browser Service
=========================================

Configuration and data models for browser operations.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Tuple

try:
    from ...core.enhanced_unified_config import get_enhanced_config

    _unified_config = get_enhanced_config()
except ImportError:
    _unified_config = None


@dataclass
class BrowserConfig:
    """Configuration for browser operations with enhanced config integration."""

    headless: bool = False
    user_data_dir: Optional[str] = None
    window_size: Tuple[int, int] = (1920, 1080)
    timeout: float = 30.0
    implicit_wait: float = 10.0
    page_load_timeout: float = 120.0

    def __post_init__(self):
        """Initialize from unified config if available."""
        if _unified_config:
            timeout_config = _unified_config.get_timeout_config()
            self.timeout = timeout_config.get("SCRAPE_TIMEOUT", self.timeout)
            self.implicit_wait = timeout_config.get(
                "QUALITY_CHECK_INTERVAL", self.implicit_wait
            )
            self.page_load_timeout = timeout_config.get(
                "RESPONSE_WAIT_TIMEOUT", self.page_load_timeout
            )


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

