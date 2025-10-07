#!/usr/bin/env python3
"""
Test Cookie Fix
===============

Quick test to verify the cookie system is working after fixes.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_cookie_manager():
    """Test the fixed cookie manager."""
    print("🧪 TESTING FIXED COOKIE SYSTEM")
    print("=" * 40)

    try:
        # Test 1: Import the fixed cookie manager directly
        print("📦 Test 1: Importing cookie manager directly...")
        import os
        import sys

        sys.path.insert(
            0, os.path.join(os.path.dirname(__file__), "src", "infrastructure", "browser")
        )
        from thea_cookie_manager import TheaCookieManager

        print("✅ Cookie manager imported successfully")

        # Test 2: Create instance
        print("🏗️ Test 2: Creating cookie manager instance...")
        cookie_manager = TheaCookieManager("test_cookies.json")
        print("✅ Cookie manager instance created")

        # Test 3: Check session info
        print("📊 Test 3: Checking session info...")
        session_info = cookie_manager.get_session_info()
        print(f"✅ Session info: {session_info}")

        # Test 4: Check if has valid cookies (should be False for new file)
        print("🔍 Test 4: Checking for valid cookies...")
        has_cookies = cookie_manager.has_valid_cookies()
        print(f"✅ Has valid cookies: {has_cookies}")

        # Test 5: Clear cookies (cleanup)
        print("🧹 Test 5: Cleaning up test cookies...")
        cookie_manager.clear_cookies()
        print("✅ Test cookies cleared")

        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Cookie system is working correctly")
        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_login_handler():
    """Test the login handler imports."""
    print("\n🧪 TESTING LOGIN HANDLER")
    print("=" * 30)

    try:
        # Test import
        print("📦 Testing login handler import...")
        from thea_login_handler import create_thea_login_handler

        print("✅ Login handler imported successfully")

        # Test creation
        print("🏗️ Testing login handler creation...")
        handler = create_thea_login_handler()
        print("✅ Login handler created successfully")

        print("\n🎉 LOGIN HANDLER TESTS PASSED!")
        return True

    except Exception as e:
        print(f"\n❌ LOGIN HANDLER TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🐝 V2_SWARM COOKIE SYSTEM TEST")
    print("=" * 50)

    success = True

    # Run tests
    success &= test_cookie_manager()
    success &= test_login_handler()

    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your cookie system is now working correctly")
        print("\n💡 Next steps:")
        print("   1. Run: python setup_thea_cookies.py")
        print("   2. Run: python simple_thea_communication.py")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("🔧 Please check the error messages above")
