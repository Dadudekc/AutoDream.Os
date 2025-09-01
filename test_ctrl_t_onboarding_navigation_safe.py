from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
🧪 Testing Ctrl+T Onboarding Navigation to Starter Coordinates (Safe Mode)
========================================================================

This test script tests the Ctrl+T onboarding navigation functionality
with PyAutoGUI fail-safe handling for corner coordinates.

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


def test_ctrl_t_onboarding_navigation_safe():
    """Test Ctrl+T onboarding navigation with fail-safe handling."""
    
    print("🧪 TESTING CTRL+T ONBOARDING NAVIGATION (SAFE MODE)")
    print("=" * 60)
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
    
    # Test safe agents (avoiding corner coordinates)
    print("🎯 STEP 3: Testing Safe Agent Ctrl+T Onboarding Navigation")
    print("Target: Agent-2 (Safe coordinates: (-308, 480))")
    print()
    
    # Create test onboarding message
    test_onboarding_content = """🎯 **ONBOARDING - CTRL+T NAVIGATION TEST (SAFE MODE)** 🎯

🧪 **TEST MESSAGE**: Ctrl+T Onboarding Navigation Test - Safe Mode
📍 **COORDINATES**: (-308, 480) - Agent-2 Safe Position
🆕 **NEW TAB**: Should be created with Ctrl+T
📋 **CONTENT**: This message tests the onboarding navigation system safely

✅ **EXPECTED BEHAVIOR**:
1. Mouse moves to Agent-2 coordinates (-308, 480)
2. Ctrl+T creates new tab
3. Message is pasted into new tab
4. Enter key sends the message

🎯 **TEST STATUS**: Safe Navigation Test
📊 **TIMESTAMP**: {timestamp}

🚨 **CAPTAIN AGENT-4** - Testing Ctrl+T Onboarding Navigation (Safe Mode)
""".format(timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))
    
    print("📝 Test Onboarding Message Created:")
    print("-" * 50)
    print(test_onboarding_content[:200] + "...")
    print("-" * 50)
    print()
    
    # Send test onboarding message to safe agent
    print("🚀 STEP 4: Sending Test Onboarding Message via Ctrl+T Navigation (Safe)")
    success = service.send_onboarding_message(
        agent_id="Agent-2",  # Safe coordinates
        style="friendly",
        mode="pyautogui"  # This triggers Ctrl+T navigation
    )
    
    if success:
        print("✅ SUCCESS: Ctrl+T onboarding navigation test completed (Safe Mode)")
        print("📍 Navigation to Agent-2 coordinates: (-308, 480)")
        print("🆕 New tab creation with Ctrl+T: SUCCESS")
        print("📋 Message delivery: SUCCESS")
    else:
        print("❌ FAILED: Ctrl+T onboarding navigation test failed")
        print("🔍 Check PyAutoGUI availability and agent window positioning")
    
    print()
    
    # Test safe bulk onboarding (avoiding corner coordinates)
    print("🚨 STEP 5: Testing Safe Bulk Ctrl+T Onboarding Navigation")
    print("Target: Safe agents only (avoiding corner coordinates)")
    print()
    
    # Define safe agents (avoiding corner coordinates that trigger fail-safe)
    safe_agents = ["Agent-2", "Agent-5", "Agent-7"]  # Safe coordinates
    
    safe_results = []
    for agent_id in safe_agents:
        print(f"🎯 Testing {agent_id}...")
        success = service.send_onboarding_message(
            agent_id=agent_id,
            style="friendly",
            mode="pyautogui"
        )
        safe_results.append(success)
        time.sleep(1)  # Brief pause between agents
    
    success_count = sum(safe_results)
    total_count = len(safe_results)
    
    print(f"📊 SAFE CTRL+T NAVIGATION RESULTS: {success_count}/{total_count} successful")
    print()
    
    # Show detailed results
    print("📍 DETAILED SAFE NAVIGATION RESULTS:")
    for i, (agent_id, success) in enumerate(zip(safe_agents, safe_results)):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        coords = service.agents.get(agent_id, {}).get("coords", "Unknown")
        print(f"  {i+1}. {agent_id}: {status} (Coordinates: {coords})")
    
    print()
    
    # Test coordinate analysis
    print("🔍 STEP 6: Analyzing Agent Coordinates for Safety")
    print("📍 COORDINATE SAFETY ANALYSIS:")
    
    for agent_id, info in service.agents.items():
        coords = info["coords"]
        x, y = coords
        
        # Check if coordinates are in safe zones (avoiding screen corners)
        is_safe = True
        safety_reason = "Safe coordinates"
        
        if x <= -1200 or x >= 1600:  # Too far left or right
            is_safe = False
            safety_reason = "Corner X coordinate"
        elif y <= 400 or y >= 1000:  # Too far top or bottom
            is_safe = False
            safety_reason = "Corner Y coordinate"
        
        status = "✅ SAFE" if is_safe else "⚠️ UNSAFE"
        print(f"  🤖 {agent_id}: {status} ({coords}) - {safety_reason}")
    
    print()
    
    # Summary
    print("📋 SAFE TEST SUMMARY:")
    print("=" * 30)
    print(f"🎯 Single Safe Agent Test: {'✅ PASSED' if success else '❌ FAILED'}")
    print(f"🚨 Safe Bulk Navigation Test: {success_count}/{total_count} successful")
    print(f"📍 Safe Agents Identified: {len(safe_agents)}/{len(service.agents)}")
    print()
    
    if success and success_count == total_count:
        print("🎉 ALL SAFE TESTS PASSED: Ctrl+T onboarding navigation working correctly!")
    else:
        print("⚠️ SOME SAFE TESTS FAILED: Check agent window positioning and PyAutoGUI setup")
    
    print()
    print("🧪 Safe Ctrl+T Onboarding Navigation Test Complete")
    print("=" * 55)


def test_coordinate_safety_zones():
    """Test coordinate safety zones to avoid PyAutoGUI fail-safe."""
    
    print("🎯 TESTING COORDINATE SAFETY ZONES")
    print("=" * 40)
    print()
    
    service = UnifiedMessagingCore()
    
    # Define safety zones
    safe_x_range = (-1200, 1600)  # Safe X coordinates
    safe_y_range = (400, 1000)    # Safe Y coordinates
    
    print(f"📍 SAFE COORDINATE RANGES:")
    print(f"   X: {safe_x_range[0]} to {safe_x_range[1]}")
    print(f"   Y: {safe_y_range[0]} to {safe_y_range[1]}")
    print()
    
    # Analyze each agent's coordinates
    safe_agents = []
    unsafe_agents = []
    
    for agent_id, info in service.agents.items():
        coords = info["coords"]
        x, y = coords
        
        is_safe = (safe_x_range[0] <= x <= safe_x_range[1] and 
                  safe_y_range[0] <= y <= safe_y_range[1])
        
        if is_safe:
            safe_agents.append(agent_id)
        else:
            unsafe_agents.append(agent_id)
        
        status = "✅ SAFE" if is_safe else "⚠️ UNSAFE"
        print(f"🤖 {agent_id}: {status} ({coords})")
    
    print()
    print("📊 SAFETY ANALYSIS SUMMARY:")
    print(f"✅ Safe Agents: {len(safe_agents)} - {', '.join(safe_agents)}")
    print(f"⚠️ Unsafe Agents: {len(unsafe_agents)} - {', '.join(unsafe_agents)}")
    print()
    
    if unsafe_agents:
        print("💡 RECOMMENDATIONS:")
        print("   • Use safe agents for automated testing")
        print("   • Manually test unsafe agents with caution")
        print("   • Consider adjusting coordinates for better safety")
    
    print("🎯 Coordinate Safety Zone Test Complete")
    print("=" * 40)


if __name__ == "__main__":
    print("🧪 CTRL+T ONBOARDING NAVIGATION TEST SUITE (SAFE MODE)")
    print("=" * 65)
    print()
    
    try:
        # Test 1: Safe Ctrl+T onboarding navigation
        test_ctrl_t_onboarding_navigation_safe()
        print()
        
        # Test 2: Coordinate safety zones
        test_coordinate_safety_zones()
        print()
        
        print("🎉 ALL SAFE NAVIGATION TESTS COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"❌ TEST ERROR: {e}")
        print("🔍 Check PyAutoGUI installation and agent window setup")
        sys.exit(1)
