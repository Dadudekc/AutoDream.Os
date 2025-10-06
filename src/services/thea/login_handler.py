#!/usr/bin/env python3
"""
Thea Login Handler - Main Interface
===================================

Main interface for Thea/ChatGPT authentication system.
V2 Compliant: ≤100 lines, imports from modular components.

Features:
- Automated login status detection
- Cookie-based session persistence
- Manual login fallback
- Selenium WebDriver integration
- ChatGPT/Thea specific selectors

Usage:
    from src.services.thea.login_handler import TheaLoginHandler

    handler = TheaLoginHandler(username="user@example.com", password="password")
    if handler.ensure_login(driver):
        print("Logged in successfully!")
"""

# Import main components from modular files
from .login_handler_core import TheaLoginHandler
from .login_handler_utils import TheaCookieManager
from .login_handler_detection import TheaLoginDetector

# Re-export main classes for backward compatibility
__all__ = [
    "TheaLoginHandler",
    "TheaCookieManager", 
    "TheaLoginDetector",
    "create_thea_login_handler",
    "check_thea_login_status",
]


# Convenience functions for easy integration
def create_thea_login_handler(username=None, password=None, cookie_file="thea_cookies.json"):
    """
    Create a Thea login handler with default settings.

    Args:
        username: ChatGPT username/email
        password: ChatGPT password
        cookie_file: Path to cookie file

    Returns:
        TheaLoginHandler instance
    """
    return TheaLoginHandler(username=username, password=password, cookie_file=cookie_file)


def check_thea_login_status(driver) -> bool:
    """
    Quick check of Thea login status.

    Args:
        driver: Selenium webdriver instance

    Returns:
        True if logged in, False otherwise
    """
    handler = TheaLoginHandler()
    return handler.detector.is_logged_in(driver)


if __name__ == "__main__":
    # Example usage
    print("🐝 V2_SWARM Thea Login Handler")
    print("=" * 40)

    # Create handler (add credentials as needed)
    handler = create_thea_login_handler()

    print("✅ Thea Login Handler created")
    print("📝 To use with credentials:")
    print(
        "   handler = create_thea_login_handler(username='your@email.com', password='your_password')"
    )
    print("   success = handler.ensure_login(driver)")
