"""
Thea Authentication Service - V2 Compliant Authentication Management
==================================================================

Handles login, cookie persistence, and authentication state management.

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

from .thea_authentication_service import AuthStatus, TheaAuthenticationService

__all__ = ["TheaAuthenticationService", "AuthStatus"]
