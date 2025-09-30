#!/usr/bin/env python3
"""
THEA Authentication Test - Check Login Status
=============================================

Simple test to check if THEA can properly authenticate with ChatGPT.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_authentication():
    """Test THEA authentication status."""
    print("🔍 THEA AUTHENTICATION TEST")
    print("=" * 50)

    try:
        from src.services.thea.thea_autonomous_system import TheaAutonomousSystem

        print("🚀 Initializing THEA system...")
        system = TheaAutonomousSystem(headless=False)

        print("🌐 Launching browser...")
        # Get the browser manager
        browser_manager = system.browser_manager
        driver = browser_manager.initialize_driver()

        if not driver:
            print("❌ Failed to initialize browser")
            return

        print("🔍 Navigating to ChatGPT...")
        driver.get("https://chatgpt.com")

        print("⏳ Waiting for page to load...")
        import time

        time.sleep(5)

        print("🔍 Checking authentication status...")

        # Check for login indicators
        login_indicators = [
            "Sign in",
            "Log in",
            "Login",
            "Continue with Google",
            "Continue with Microsoft",
            "Continue with Apple",
        ]

        logged_in_indicators = ["New chat", "New conversation", "Send message", "Ask anything"]

        page_source = driver.page_source.lower()

        print("\n" + "=" * 50)
        print("🔍 AUTHENTICATION ANALYSIS")
        print("=" * 50)

        # Check for login prompts
        login_found = False
        for indicator in login_indicators:
            if indicator.lower() in page_source:
                print(f"❌ LOGIN REQUIRED: Found '{indicator}' on page")
                login_found = True
                break

        # Check for logged-in indicators
        logged_in_found = False
        for indicator in logged_in_indicators:
            if indicator.lower() in page_source:
                print(f"✅ LOGGED IN: Found '{indicator}' on page")
                logged_in_found = True
                break

        if not login_found and not logged_in_found:
            print("⚠️  UNCLEAR STATUS: Could not determine authentication status")

        print("\n" + "=" * 50)
        print("🔍 COOKIE ANALYSIS")
        print("=" * 50)

        # Check current cookies
        cookies = driver.get_cookies()
        print(f"📊 Total cookies: {len(cookies)}")

        auth_cookies = []
        for cookie in cookies:
            name = cookie.get("name", "").lower()
            if any(
                auth_term in name for auth_term in ["auth", "session", "token", "login", "user"]
            ):
                auth_cookies.append(cookie)
                print(f"🔑 Auth cookie: {cookie['name']} = {cookie['value'][:20]}...")

        if auth_cookies:
            print(f"✅ Found {len(auth_cookies)} authentication cookies")
        else:
            print("❌ No authentication cookies found")

        print("\n" + "=" * 50)
        print("🔍 CURRENT URL")
        print("=" * 50)
        print(f"🌐 Current URL: {driver.current_url}")

        print("\n" + "=" * 50)
        print("🔍 PAGE TITLE")
        print("=" * 50)
        print(f"📄 Page Title: {driver.title}")

        print("\n" + "=" * 50)
        print("📝 RECOMMENDATIONS")
        print("=" * 50)

        if login_found:
            print("❌ ACTION REQUIRED: Manual login needed")
            print("1. Log in to ChatGPT manually in the browser")
            print("2. Let THEA save the authentication cookies")
            print("3. Test THEA again after login")
        elif logged_in_found:
            print("✅ STATUS: Appears to be logged in")
            print("1. THEA should work with current authentication")
            print("2. Test sending a message to verify")
        else:
            print("⚠️  STATUS: Authentication unclear")
            print("1. Check if ChatGPT interface has changed")
            print("2. Try manual login and test again")

        input("\nPress Enter to close browser...")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        try:
            if "driver" in locals():
                driver.quit()
                print("✅ Browser closed")
        except:
            pass


if __name__ == "__main__":
    test_authentication()
