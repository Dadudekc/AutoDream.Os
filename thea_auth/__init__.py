"""
Thea Authentication Package
==========================

Modular authentication system for Thea communication.
"""

from .cookie_manager import TheaCookieManager
from .login_handler import TheaLoginHandler
from .factory import create_thea_login_handler, check_thea_login_status

__all__ = [
    "TheaCookieManager",
    "TheaLoginHandler", 
    "create_thea_login_handler",
    "check_thea_login_status"
]


