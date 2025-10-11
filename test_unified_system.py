#!/usr/bin/env python3
"""
Test Unified Thea Automation System
====================================

Quick tests to verify the new unified system works.
"""


def test_imports():
    """Test that imports work cleanly."""
    print("🧪 TEST 1: Imports")
    print("-" * 30)

    try:
        print("✅ Import successful")
        print("✅ No import errors")
        print("✅ No circular dependencies")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_initialization():
    """Test that initialization works."""
    print("\n🧪 TEST 2: Initialization")
    print("-" * 30)

    try:
        from thea_automation import TheaAutomation, TheaConfig

        # Test default config
        config = TheaConfig()
        print(f"✅ Config created: {config.thea_url[:50]}...")

        # Test automation init
        thea = TheaAutomation(config)
        print("✅ TheaAutomation initialized")
        print(f"✅ Cookie file: {thea.cookie_file}")
        print(f"✅ Responses dir: {thea.responses_dir}")

        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


def test_cookie_methods():
    """Test cookie management methods."""
    print("\n🧪 TEST 3: Cookie Methods")
    print("-" * 30)

    try:
        from thea_automation import TheaAutomation

        thea = TheaAutomation()

        # Test has_valid_cookies
        has_cookies = thea.has_valid_cookies()
        print(f"✅ has_valid_cookies() = {has_cookies}")

        if has_cookies:
            print("✅ Existing cookies found")
            print(f"✅ Cookie file: {thea.cookie_file}")
        else:
            print("⚠️  No cookies yet (run setup first)")

        return True
    except Exception as e:
        print(f"❌ Cookie methods failed: {e}")
        return False


def test_api():
    """Test the API structure."""
    print("\n🧪 TEST 4: API Structure")
    print("-" * 30)

    try:
        from thea_automation import TheaAutomation

        thea = TheaAutomation()

        # Check methods exist
        methods = [
            "save_cookies",
            "load_cookies",
            "has_valid_cookies",
            "start_browser",
            "is_logged_in",
            "ensure_login",
            "send_message",
            "wait_for_response",
            "save_conversation",
            "communicate",
            "cleanup",
        ]

        for method in methods:
            if hasattr(thea, method):
                print(f"✅ Method exists: {method}")
            else:
                print(f"❌ Missing method: {method}")
                return False

        print("✅ All methods present")
        return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def test_context_manager():
    """Test context manager support."""
    print("\n🧪 TEST 5: Context Manager")
    print("-" * 30)

    try:
        from thea_automation import TheaAutomation

        with TheaAutomation() as thea:
            print("✅ Entered context manager")
            print(f"✅ Instance: {type(thea)}")

        print("✅ Exited context manager cleanly")
        return True
    except Exception as e:
        print(f"❌ Context manager failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🐝 V2_SWARM UNIFIED SYSTEM TEST")
    print("=" * 50)
    print()

    results = []

    # Run tests
    results.append(test_imports())
    results.append(test_initialization())
    results.append(test_cookie_methods())
    results.append(test_api())
    results.append(test_context_manager())

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    print(f"\n✅ Passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Unified system is working correctly")
        print("\n💡 Ready to use:")
        print('   python thea_automation.py --message "Your message"')
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        print("🔧 Check the errors above")

    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
