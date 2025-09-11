#!/usr/bin/env python3
"""
Basic Thea Integration Test - V2 Compliance
==========================================

Tests the core Thea integration components without full environment setup.
This allows us to verify our fixes work before running full integration tests.

Author: Agent-4 (Quality Assurance Specialist)
License: MIT
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")

    try:
        # Test unified browser service
        from src.infrastructure.unified_browser_service import UnifiedBrowserService, ChromeBrowserAdapter
        print("✅ Unified browser service imported successfully")

        # Test enhanced config system
        from src.core.enhanced_unified_config import get_enhanced_config
        config = get_enhanced_config()
        print("✅ Enhanced unified config imported successfully")

        # Test basic config functionality
        timeout_config = config.get_timeout_config()
        print(f"✅ Timeout config loaded: {len(timeout_config)} items")

        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during imports: {e}")
        return False

def test_browser_adapter():
    """Test browser adapter instantiation."""
    print("\n🧪 Testing browser adapter...")

    try:
        from src.infrastructure.unified_browser_service import ChromeBrowserAdapter, BrowserConfig

        # Create adapter
        adapter = ChromeBrowserAdapter()
        print("✅ Chrome browser adapter created")

        # Test config
        config = BrowserConfig(headless=True)
        print(f"✅ Browser config created: headless={config.headless}")

        # Test that adapter methods exist
        methods = ['start', 'stop', 'navigate', 'get_current_url', 'get_title',
                  'find_element', 'find_elements', 'execute_script', 'is_running',
                  'get_cookies', 'add_cookies']

        for method in methods:
            if hasattr(adapter, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False

        return True

    except Exception as e:
        print(f"❌ Browser adapter test failed: {e}")
        return False


def test_unified_service():
    """Test unified browser service."""
    print("\n🧪 Testing unified browser service...")

    try:
        from src.infrastructure.unified_browser_service import UnifiedBrowserService

        # Create service
        service = UnifiedBrowserService()
        print("✅ Unified browser service created")

        # Test methods exist
        methods = ['start_browser', 'stop_browser', 'create_session',
                  'navigate_to_conversation', 'send_message', 'wait_for_response',
                  'get_session_info', 'get_rate_limit_status', 'get_page_status', 
                  'is_browser_running', 'get_browser_info']

        for method in methods:
            if hasattr(service, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False

        return True

    except Exception as e:
        print(f"❌ Unified service test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Thea Integration Basic Tests")
    print("=" * 50)

    tests = [
        ("Import Test", test_imports),
        ("Browser Adapter Test", test_browser_adapter),
        ("Unified Service Test", test_unified_service),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Thea integration components are working.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
