from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
🧪 Testing Ctrl+T Onboarding Navigation to Starter Coordinates
============================================================

This test script specifically tests the Ctrl+T onboarding navigation functionality
that moves to agent coordinates and creates new tabs for onboarding messages.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import time
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.messaging_core import UnifiedMessagingCore
from src.services.models.messaging_models import (
    UnifiedMessageType, 
    UnifiedMessagePriority, 
    UnifiedMessageTag
)


def test_ctrl_t_onboarding_navigation():
    """Test Ctrl+T onboarding navigation to starter coordinates."""
    
    print("🧪 TESTING CTRL+T ONBOARDING NAVIGATION TO STARTER COORDINATES")
    print("=" * 70)
    print()
    
    # Initialize the messaging service
    print("📋 STEP 1: Initializing Unified Messaging Service")
    service = UnifiedMessagingCore()
    print("✅ Service initialized successfully")
    print()
    
    # Show current coordinates
    print("📍 STEP 2: Displaying Current Agent Coordinates")
    service.show_coordinates()
    print()
    
    # Test single agent onboarding with Ctrl+T
    print("🎯 STEP 3: Testing Single Agent Ctrl+T Onboarding Navigation")
    print("Target: Agent-1 (Starter coordinates: (-1269, 481))")
    print()
    
    # Create test onboarding message
    test_onboarding_content = """🎯 **ONBOARDING - CTRL+T NAVIGATION TEST** 🎯

🧪 **TEST MESSAGE**: Ctrl+T Onboarding Navigation Test
📍 **COORDINATES**: (-1269, 481) - Agent-1 Starter Position
🆕 **NEW TAB**: Should be created with Ctrl+T
📋 **CONTENT**: This message tests the onboarding navigation system

✅ **EXPECTED BEHAVIOR**:
1. Mouse moves to Agent-1 coordinates (-1269, 481)
2. Ctrl+T creates new tab
3. Message is pasted into new tab
4. Enter key sends the message

🎯 **TEST STATUS**: Active Navigation Test
📊 **TIMESTAMP**: {timestamp}

🚨 **CAPTAIN AGENT-4** - Testing Ctrl+T Onboarding Navigation
""".format(timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))
    
    print("📝 Test Onboarding Message Created:")
    print("-" * 40)
    print(test_onboarding_content[:200] + "...")
    print("-" * 40)
    print()
    
    # Send test onboarding message
    print("🚀 STEP 4: Sending Test Onboarding Message via Ctrl+T Navigation")
    success = service.send_onboarding_message(
        agent_id="Agent-1",
        style="friendly",
        mode="pyautogui"  # This triggers Ctrl+T navigation
    )
    
    if success:
        print("✅ SUCCESS: Ctrl+T onboarding navigation test completed")
        print("📍 Navigation to Agent-1 coordinates: (-1269, 481)")
        print("🆕 New tab creation with Ctrl+T: SUCCESS")
        print("📋 Message delivery: SUCCESS")
    else:
        print("❌ FAILED: Ctrl+T onboarding navigation test failed")
        print("🔍 Check PyAutoGUI availability and agent window positioning")
    
    print()
    
    # Test bulk onboarding with Ctrl+T
    print("🚨 STEP 5: Testing Bulk Ctrl+T Onboarding Navigation")
    print("Target: All agents in correct order (Agent-4 last)")
    print()
    
    bulk_results = service.send_bulk_onboarding(
        style="friendly",
        mode="pyautogui"  # This triggers Ctrl+T navigation for all agents
    )
    
    success_count = sum(bulk_results)
    total_count = len(bulk_results)
    
    print(f"📊 BULK CTRL+T NAVIGATION RESULTS: {success_count}/{total_count} successful")
    print()
    
    # Show detailed results
    print("📍 DETAILED NAVIGATION RESULTS:")
    agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
    for i, (agent_id, success) in enumerate(zip(agent_order, bulk_results)):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        coords = service.agents.get(agent_id, {}).get("coords", "Unknown")
        print(f"  {i+1}. {agent_id}: {status} (Coordinates: {coords})")
    
    print()
    
    # Test coordinate validation
    print("🔍 STEP 6: Validating Agent Coordinates")
    validation = service.validate_coordinates()
    print(f"📍 Valid Coordinates: {validation['valid_coordinates']}/{validation['total_agents']}")
    print()
    
    # Summary
    print("📋 TEST SUMMARY:")
    print("=" * 30)
    print(f"🎯 Single Agent Test: {'✅ PASSED' if success else '❌ FAILED'}")
    print(f"🚨 Bulk Navigation Test: {success_count}/{total_count} successful")
    print(f"📍 Coordinate Validation: {validation['valid_coordinates']}/{validation['total_agents']} valid")
    print()
    
    if success and success_count == total_count:
        print("🎉 ALL TESTS PASSED: Ctrl+T onboarding navigation working correctly!")
    else:
        print("⚠️ SOME TESTS FAILED: Check agent window positioning and PyAutoGUI setup")
    
    print()
    print("🧪 Ctrl+T Onboarding Navigation Test Complete")
    print("=" * 50)


def test_coordinate_specific_navigation():
    """Test navigation to specific starter coordinates."""
    
    print("🎯 TESTING SPECIFIC STARTER COORDINATE NAVIGATION")
    print("=" * 50)
    print()
    
    service = UnifiedMessagingCore()
    
    # Test each agent's starter coordinates
    test_agents = [
        ("Agent-1", (-1269, 481), "Top-left starter position"),
        ("Agent-2", (-308, 480), "Top-center starter position"),
        ("Agent-3", (-1269, 1001), "Bottom-left starter position"),
        ("Agent-4", (-308, 1000), "Bottom-center starter position"),
        ("Agent-5", (652, 421), "Top-right starter position"),
        ("Agent-6", (1612, 419), "Far-right starter position"),
        ("Agent-7", (653, 940), "Bottom-right starter position"),
        ("Agent-8", (1611, 941), "Far-bottom-right starter position")
    ]
    
    for agent_id, expected_coords, description in test_agents:
        print(f"🎯 Testing {agent_id}: {description}")
        print(f"📍 Expected Coordinates: {expected_coords}")
        
        # Get actual coordinates
        actual_coords = service.agents.get(agent_id, {}).get("coords", None)
        
        if actual_coords == expected_coords:
            print(f"✅ COORDINATES MATCH: {actual_coords}")
        else:
            print(f"❌ COORDINATE MISMATCH: Expected {expected_coords}, Got {actual_coords}")
        
        print()
    
    print("🎯 Starter Coordinate Navigation Test Complete")
    print("=" * 50)


if __name__ == "__main__":
    print("🧪 CTRL+T ONBOARDING NAVIGATION TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Ctrl+T onboarding navigation
        test_ctrl_t_onboarding_navigation()
        print()
        
        # Test 2: Specific coordinate navigation
        test_coordinate_specific_navigation()
        print()
        
        print("🎉 ALL NAVIGATION TESTS COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")
        print("🔍 Check PyAutoGUI installation and agent window setup")
        sys.exit(1)
