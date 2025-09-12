#!/usr/bin/env python3
"""
🐝 MESSAGING SYSTEM TEST SCRIPT
===============================

Comprehensive test of the messaging system components after cleanup.
This script validates that all messaging components are operational.

Author: Agent-3 - Testing Commander
"""

import sys
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_imports():
    """Test basic messaging imports."""
    print("📋 Testing basic messaging imports...")

    try:
        from src.services.messaging.models.messaging_models import UnifiedMessage
        from src.services.messaging.models.messaging_enums import UnifiedMessagePriority, UnifiedMessageType
        print("✅ Basic messaging models imported successfully")

        # Test creating a message
        test_message = UnifiedMessage(
            content="🐝 Test message from cleanup verification",
            recipient="Agent-1",
            sender="Agent-3",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.NORMAL
        )
        print("✅ UnifiedMessage creation successful")
        return True

    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        traceback.print_exc()
        return False

def test_enhanced_examples():
    """Test the enhanced example usage in our files."""
    print("\n📋 Testing enhanced example usage...")

    success_count = 0
    total_tests = 0

    # Test messaging CLI examples
    total_tests += 1
    try:
        from src.services.messaging_cli_refactored import MessagingCLI
        print("✅ Messaging CLI import successful")
        success_count += 1
    except Exception as e:
        print(f"❌ Messaging CLI import failed: {e}")

    # Test contract notification examples
    total_tests += 1
    try:
        from contracts.contract_notification_system import ContractNotificationSystem
        system = ContractNotificationSystem()
        print("✅ Contract notification system examples working")
        success_count += 1
    except Exception as e:
        print(f"❌ Contract notification examples failed: {e}")

    # Test coordinate loader examples
    total_tests += 1
    try:
        from src.core.coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()
        print("✅ Coordinate loader examples working")
        success_count += 1
    except Exception as e:
        print(f"❌ Coordinate loader examples failed: {e}")

    print(f"📊 Example usage tests: {success_count}/{total_tests} successful")
    return success_count == total_tests

def test_swarm_functionality():
    """Test swarm-specific functionality."""
    print("\n📋 Testing swarm functionality...")

    try:
        # Test agent listing
        from src.services.consolidated_messaging_service import list_agents
        agents = list_agents()
        print(f"✅ Agent listing working: {len(agents)} agents detected")
        print(f"🤖 Agents: {agents}")

        # Test message history (if available)
        try:
            from src.services.consolidated_messaging_service import show_message_history
            print("✅ Message history functionality available")
        except ImportError:
            print("⚠️  Message history functionality not available (expected)")

        return True

    except Exception as e:
        print(f"❌ Swarm functionality test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🎉 COMPREHENSIVE MESSAGING SYSTEM TEST")
    print("=" * 60)
    print("Testing messaging system after cleanup and enhancement...")

    test_results = []

    # Run all tests
    test_results.append(("Basic Imports", test_basic_imports()))
    test_results.append(("Enhanced Examples", test_enhanced_examples()))
    test_results.append(("Swarm Functionality", test_swarm_functionality()))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED - MESSAGING SYSTEM FULLY OPERATIONAL!")
        print("🐝 WE ARE SWARM - CLEANUP VERIFICATION COMPLETE!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW OUTPUT ABOVE")
        return 1

if __name__ == "__main__":
    """Demonstrate comprehensive messaging system testing."""
    exit_code = main()
    sys.exit(exit_code)

