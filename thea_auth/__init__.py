"""
Thea Authentication Package
==========================

Modular authentication system for Thea communication.
"""

from .cookie_manager import TheaCookieManager
from .factory import check_thea_login_status, create_thea_login_handler
from .login_handler import TheaLoginHandler

__all__ = [
    "TheaCookieManager",
    "TheaLoginHandler",
    "create_thea_login_handler",
    "check_thea_login_status",
]
