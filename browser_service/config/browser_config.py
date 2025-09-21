#!/usr/bin/env python3
"""
Browser Configuration
====================

Configuration classes for browser service operations.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Tuple
import time


@dataclass
class BrowserConfig:
    """Configuration for browser operations."""
    headless: bool = False
    user_data_dir: Optional[str] = None
    window_size: Tuple[int, int] = (1920, 1080)
    timeout: float = 30.0
    implicit_wait: float = 10.0
    page_load_timeout: float = 120.0


@dataclass
class TheaConfig:
    """Configuration for Thea Manager interactions."""
    base_url: str = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
    rate_limit_requests_per_minute: int = 10
    rate_limit_requests_per_hour: int = 100
    session_timeout_minutes: int = 30
    retry_attempts: int = 3
    retry_delay_seconds: float = 2.0


@dataclass
class SessionInfo:
    """Information about a browser session."""
    session_id: str
    service_name: str
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    request_count: int = 0
    success_count: int = 0
    failure_count: int = 0


@dataclass
class RateLimitStatus:
    """Rate limiting status for a service."""
    service_name: str
    requests_this_minute: int = 0
    requests_this_hour: int = 0
    last_request_time: float = field(default_factory=time.time)
    is_limited: bool = False
    reset_time: Optional[float] = None


