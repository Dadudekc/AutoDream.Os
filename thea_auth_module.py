#!/usr/bin/env python3
"""
Thea Authentication Module - V2_SWARM Compliant Authentication Operations
==========================================================================

Handles all authentication operations for Thea communication with V2 compliance.

V2 COMPLIANCE:
- ✅ File size: <400 lines
- ✅ Type hints: Full coverage
- ✅ Modular design: Clean separation of concerns
- ✅ Repository pattern: Data access layer

Author: Agent-4 (Captain) - V2_SWARM
License: MIT
"""

import time
import webbrowser
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .simple_thea_communication import SimpleTheaCommunication


class TheaAuthModule:
    """Handles authentication operations for Thea - V2_SWARM Compliant."""

    def __init__(self, thea_url: str) -> None:
        """Initialize authentication module.

        Args:
            thea_url: URL of the Thea service
        """
        self.thea_url: str = thea_url

    def ensure_authenticated(self, comm_instance: Any) -> bool:
        """Ensure user is authenticated with Thea - maintains exact original behavior.

        Args:
            comm_instance: Thea communication instance

        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not comm_instance.use_selenium:
            print("🔄 USING MANUAL MODE")
            return self._manual_authentication()

        if not comm_instance.driver:
            if not comm_instance.initialize_driver():
                return self._manual_authentication()

        print("🔐 AUTOMATED AUTHENTICATION")
        print("-" * 30)

        # Use our modular login handler
        success: bool = comm_instance.login_handler.ensure_login(comm_instance.driver)

        if success:
            print("✅ AUTHENTICATION SUCCESSFUL")

            # Additional navigation to chatgpt.com to stabilize login detection
            print("🔄 STABILIZING LOGIN DETECTION...")
            try:
                comm_instance.driver.get("https://chatgpt.com")
                time.sleep(3)
                print("✅ Navigated to chatgpt.com for login verification")

                # Check login status after navigation
                if comm_instance.login_handler._is_logged_in(comm_instance.driver):
                    print("✅ LOGIN STATUS CONFIRMED after navigation")
                else:
                    print("⚠️  LOGIN STATUS UNCLEAR after navigation - continuing anyway")

            except Exception as e:
                print(f"⚠️  Navigation/stabilization warning: {e}")

            # Attach detector once driver is live
            try:
                from response_detector import ResponseDetector
                comm_instance.detector = ResponseDetector(comm_instance.driver)
            except Exception as e:
                print(f"⚠️  ResponseDetector init warning: {e}")

            return True
        else:
            print("❌ AUTOMATED AUTHENTICATION FAILED")
            print("🔄 FALLING BACK TO MANUAL MODE")
            return self._manual_authentication()

    def _manual_authentication(self) -> bool:
        """Handle manual authentication - maintains exact original behavior.

        Returns:
            bool: Always returns True (manual authentication always succeeds)
        """
        print("👤 MANUAL AUTHENTICATION REQUIRED")
        print("-" * 35)
        print("Please complete these steps:")
        print("1. Open your browser")
        print("2. Navigate to:", self.thea_url)
        print("3. Log in if needed")
        print("4. Return to this terminal")

        input("\n🎯 Press Enter when you're logged in and on the Thea page...")

        # Try to open browser for user
        try:
            webbrowser.open(self.thea_url, new=1)
            print("✅ Browser opened to Thea page")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")

        print("⏳ Waiting 5 seconds for page to load...")
        time.sleep(5)

        return True
