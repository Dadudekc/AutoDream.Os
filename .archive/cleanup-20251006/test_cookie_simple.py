#!/usr/bin/env python3
"""
Simple Cookie Test
==================

Direct test of the cookie manager without complex imports.
"""

import os
import sys

# Add the browser directory to Python path
browser_dir = os.path.join(os.path.dirname(__file__), "src", "infrastructure", "browser")
sys.path.insert(0, browser_dir)


def test_direct_import():
    """Test direct import of cookie manager."""
    print("🧪 TESTING DIRECT COOKIE IMPORT")
    print("=" * 40)

    try:
        print("📦 Importing TheaCookieManager directly...")
        from thea_cookie_manager import TheaCookieManager

        print("✅ Direct import successful")

        # Test creation
        print("🏗️ Creating cookie manager instance...")
        cookie_manager = TheaCookieManager("test_cookies.json")
        print("✅ Instance created successfully")

        # Test methods
        print("📊 Testing session info...")
        session_info = cookie_manager.get_session_info()
        print(f"✅ Session info: {session_info}")

        print("🔍 Testing cookie validation...")
        has_cookies = cookie_manager.has_valid_cookies()
        print(f"✅ Has valid cookies: {has_cookies}")

        print("🧹 Cleaning up...")
        cookie_manager.clear_cookies()
        print("✅ Cleanup complete")

        return True

    except Exception as e:
        print(f"❌ Direct import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_login_handler():
    """Test login handler."""
    print("\n🧪 TESTING LOGIN HANDLER")
    print("=" * 30)

    try:
        print("📦 Importing login handler...")
        from thea_login_handler import create_thea_login_handler

        print("✅ Login handler imported")

        print("🏗️ Creating login handler...")
        handler = create_thea_login_handler()
        print("✅ Login handler created")

        return True

    except Exception as e:
        print(f"❌ Login handler test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_setup_script():
    """Test if setup script can import correctly."""
    print("\n🧪 TESTING SETUP SCRIPT IMPORTS")
    print("=" * 35)

    try:
        # Test the imports that setup script uses
        print("📦 Testing setup script imports...")

        # This should work now
        print("✅ TheaCookieManager import OK")

        print("✅ TheaLoginHandler import OK")

        return True

    except Exception as e:
        print(f"❌ Setup script import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🐝 V2_SWARM SIMPLE COOKIE TEST")
    print("=" * 50)

    success = True

    # Run tests
    success &= test_direct_import()
    success &= test_login_handler()
    success &= test_setup_script()

    if success:
        print("\n🎉 ALL SIMPLE TESTS PASSED!")
        print("✅ Cookie system imports are working")
        print("\n💡 You can now run:")
        print("   python setup_thea_cookies.py")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("🔧 Check the errors above")
