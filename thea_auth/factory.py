#!/usr/bin/env python3
"""
Thea Authentication Factory
===========================

Factory functions for creating Thea authentication components.
"""

from .login_handler import TheaLoginHandler


def create_thea_login_handler(username=None, password=None):
    """Create a Thea login handler instance."""
    return TheaLoginHandler(username=username)


def check_thea_login_status(driver=None):
    """Check if user is currently logged in to Thea."""
    if driver:
        try:
            # Check for login indicators
            page_source = driver.page_source.lower()
            login_indicators = [
                "sign in",
                "log in",
                "login",
                "continue with google",
                "continue with microsoft",
            ]

            for indicator in login_indicators:
                if indicator in page_source:
                    return False

            return True
        except Exception:
            return False

    return False
