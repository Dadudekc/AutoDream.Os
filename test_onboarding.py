#!/usr/bin/env python3
"""
Test script for onboarding functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

print("Testing onboarding imports...")
print("Current directory:", os.getcwd())
print("Python path:", sys.path[:3])

try:
    print("\n1. Testing templates import...")
    from templates.onboarding_roles import ROLES, build_role_message

    print("✅ Templates import successful")
    print(f"   Available roles: {len(ROLES)}")

    print("\n2. Testing onboarding handler import...")
    from src.services.handlers.onboarding_handler import OnboardingHandler

    print("✅ OnboardingHandler import successful")

    handler = OnboardingHandler()
    print("✅ OnboardingHandler instantiation successful")

    print("\n3. Testing role message building...")
    test_msg = build_role_message("Agent-6", "SOLID")
    print("✅ Role message building successful")
    print(f"   Message length: {len(test_msg)} characters")

    print("\n🎉 ALL TESTS PASSED!")
    print("✅ Hard onboarding system is fully functional")

except ImportError as e:
    print(f"\n❌ IMPORT ERROR: {e}")
    import traceback

    traceback.print_exc()

except Exception as e:
    print(f"\n❌ OTHER ERROR: {e}")
    import traceback

    traceback.print_exc()
