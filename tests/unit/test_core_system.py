from pathlib import Path
import sys

        from core.agent_manager import AgentManager
        from core.config_manager import ConfigManager
        from core.message_router import MessageRouter
        from launchers.unified_launcher_v2 import UnifiedLauncherV2
        from services.agent_cell_phone import AgentCellPhone
        from services.coordination import CoordinationService
from src.utils.stability_improvements import stability_manager, safe_import

#!/usr/bin/env python3
"""
Core System Test - Agent Cellphone V2
====================================

Simple test script to verify core system functionality
without pytest dependencies.
"""



# Add src to path for imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_core_imports():
    """Test core component imports."""
    print("🧪 Testing core component imports...")

    try:

        print("✅ AgentManager import successful")
    except ImportError as e:
        print(f"❌ AgentManager import failed: {e}")
        return False

    try:

        print("✅ MessageRouter import successful")
    except ImportError as e:
        print(f"❌ MessageRouter import failed: {e}")
        return False

    try:

        print("✅ ConfigManager import successful")
    except ImportError as e:
        print(f"❌ ConfigManager import failed: {e}")
        return False

    return True


def test_services_imports():
    """Test services imports."""
    print("\n🧪 Testing services imports...")

    try:

        print("✅ AgentCellPhone import successful")
    except ImportError as e:
        print(f"❌ AgentCellPhone import failed: {e}")
        return False

    try:

        print("✅ CoordinationService import successful")
    except ImportError as e:
        print(f"❌ CoordinationService import failed: {e}")
        return False

    return True


def test_launcher_imports():
    """Test launcher imports."""
    print("\n🧪 Testing launcher imports...")

    try:

        print("✅ UnifiedLauncherV2 import successful")
    except ImportError as e:
        print(f"❌ UnifiedLauncherV2 import failed: {e}")
        return False

    return True


def test_basic_functionality():
    """Test basic functionality."""
    print("\n🧪 Testing basic functionality...")

    try:

        manager = AgentManager()
        print("✅ AgentManager instantiation successful")

        # Test basic methods
        agents = manager.get_available_agents()
        print(f"✅ AgentManager.get_available_agents() successful: {len(agents)} agents")

        # Test agent summary
        summary = manager.get_agent_summary()
        print(
            f"✅ AgentManager.get_agent_summary() successful: {len(summary)} summary items"
        )

    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

    return True


def main():
    """Run all tests."""
    print("🚀 AGENT_CELLPHONE_V2 CORE SYSTEM TEST")
    print("=" * 50)

    tests = [
        test_core_imports,
        test_services_imports,
        test_launcher_imports,
        test_basic_functionality,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Core system is operational.")
        return True
    else:
        print("⚠️  Some tests failed. Core system needs attention.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
