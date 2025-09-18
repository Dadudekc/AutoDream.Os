"""
Browser Service Package
======================

Modular browser service components for V2 compliance.
"""

from .core.unified_browser_service import UnifiedBrowserService
from .adapters.chrome_adapter import ChromeBrowserAdapter
from .managers.cookie_manager import CookieManager
from .managers.session_manager import SessionManager
from .operations.browser_operations import BrowserOperations
from .config.browser_config import BrowserConfig, TheaConfig, SessionInfo, RateLimitStatus

__all__ = [
    'UnifiedBrowserService',
    'ChromeBrowserAdapter',
    'CookieManager',
    'SessionManager', 
    'BrowserOperations',
    'BrowserConfig',
    'TheaConfig',
    'SessionInfo',
    'RateLimitStatus'
]


