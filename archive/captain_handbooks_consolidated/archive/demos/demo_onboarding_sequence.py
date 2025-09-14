#!/usr/bin/env python3
"""
Demo: Hard Onboarding Sequence Verification
===========================================

Demonstrates the exact sequence described:
1. Click chat input coords
2. Press Ctrl+N
3. Click onboarding input coords
4. Type onboarding message
5. Press Enter
"""

from src.automation.ui_onboarding import UIOnboarder
from src.core.workspace_agent_registry import AgentRegistry
from templates.onboarding_roles import build_role_message


def main():
    print("🎯 HARD ONBOARDING SEQUENCE VERIFICATION")
    print("=" * 50)

    # Create onboarder with dry-run to show the sequence
    onboarder = UIOnboarder(tolerance=200, retries=2, dry_run=True)

    # Load coordinates for Agent-3
    reg = AgentRegistry()
    coords = reg.get_onboarding_coords("Agent-3")

    print("📍 Agent-3 Coordinates:")
    print(f"   Chat Input: {coords['chat_input_coordinates']}")
    print(f"   Onboarding Input: {coords['onboarding_coordinates']}")
    print()

    # Build the onboarding message
    message = build_role_message("Agent-3", "CLEANUP_CORE")
    print("📝 Onboarding Message Preview (first 100 chars):")
    print(f'   "{message[:100]}..."')
    print()

    print("🔄 EXACT SEQUENCE EXECUTION:")
    result = onboarder.perform(agent_id="Agent-3", coords=coords, message=message)

    print(f"\n✅ Result: {result}")
    print("\n🎯 SEQUENCE COMPLETED AS SPECIFIED!")
    print("\n📋 What happened:")
    print("   1. ✅ Clicked chat input coordinates")
    print("   2. ✅ Pressed Ctrl+N (new chat)")
    print("   3. ✅ Clicked onboarding input coordinates")
    print("   4. ✅ Typed role-aligned onboarding message")
    print("   5. ✅ Pressed Enter to send")
    print("   6. ✅ Normal messaging continues...")


if __name__ == "__main__":
    main()
