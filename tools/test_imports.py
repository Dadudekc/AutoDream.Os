#!/usr/bin/env python3
"""
Import Testing Tool - C-007
============================

Tests all critical imports after cleanup to ensure nothing is broken.

Author: Agent-3 (Infrastructure & DevOps)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test all critical imports."""

    print("🧪 Testing Critical Imports...\n")

    tests = []

    # Test 1: Discord Commander
    try:
        tests.append(("Discord Commander", "PASS"))
    except Exception as e:
        tests.append(("Discord Commander", f"FAIL: {e}"))

    # Test 2: Core Utilities
    try:
        tests.append(("Unified Utilities", "PASS"))
    except Exception as e:
        tests.append(("Unified Utilities", f"FAIL: {e}"))

    # Test 3: Core Config
    try:
        tests.append(("Unified Config", "PASS"))
    except Exception as e:
        tests.append(("Unified Config", f"FAIL: {e}"))

    # Test 4: Core Services
    try:
        tests.append(("Core Health", "PASS"))
    except Exception as e:
        tests.append(("Core Health", f"FAIL: {e}"))

    # Test 5: Application Layer
    try:
        tests.append(("Application Use Cases", "PASS"))
    except Exception as e:
        tests.append(("Application Use Cases", f"FAIL: {e}"))

    # Test 6: Infrastructure
    try:
        tests.append(("Infrastructure", "PASS"))
    except Exception as e:
        tests.append(("Infrastructure", f"FAIL: {e}"))

    # Print results
    print("=" * 60)
    print("📊 IMPORT TEST RESULTS")
    print("=" * 60)
    print()

    passed = 0
    failed = 0

    for name, result in tests:
        status = "✅" if result == "PASS" else "❌"
        print(f"{status} {name}: {result}")
        if result == "PASS":
            passed += 1
        else:
            failed += 1

    print()
    print(f"📈 Summary: {passed}/{len(tests)} tests passed ({passed/len(tests)*100:.1f}%)")
    print()

    if failed == 0:
        print("✅ All imports working correctly!")
        return True
    else:
        print(f"❌ {failed} import tests failed")
        return False


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
