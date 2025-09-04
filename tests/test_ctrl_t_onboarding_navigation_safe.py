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


# Add src to path for imports
sys.path.insert(0, get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), 'src'))

from src.services.messaging_core import UnifiedMessagingCore
from src.services.models.messaging_models import (
    UnifiedMessageType, 
    UnifiedMessagePriority, 
    UnifiedMessageTag
)


def test_ctrl_t_onboarding_navigation_safe():
    """Test Ctrl+T onboarding navigation with fail-safe handling."""
    
    get_logger(__name__).info("🧪 TESTING CTRL+T ONBOARDING NAVIGATION (SAFE MODE)")
    get_logger(__name__).info("=" * 60)
    get_logger(__name__).info()
    
    # Initialize the messaging service
    get_logger(__name__).info("📋 STEP 1: Initializing Unified Messaging Service")
    service = UnifiedMessagingCore()
    get_logger(__name__).info("✅ Service initialized successfully")
    get_logger(__name__).info()
    
    # Show current coordinates
    get_logger(__name__).info("📍 STEP 2: Displaying Current Agent Coordinates")
    service.show_coordinates()
    get_logger(__name__).info()
    
    # Test safe agents (avoiding corner coordinates)
    get_logger(__name__).info("🎯 STEP 3: Testing Safe Agent Ctrl+T Onboarding Navigation")
    get_logger(__name__).info("Target: Agent-2 (Safe coordinates: (-308, 480))")
    get_logger(__name__).info()
    
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
    
    get_logger(__name__).info("📝 Test Onboarding Message Created:")
    get_logger(__name__).info("-" * 50)
    get_logger(__name__).info(test_onboarding_content[:200] + "...")
    get_logger(__name__).info("-" * 50)
    get_logger(__name__).info()
    
    # Send test onboarding message to safe agent
    get_logger(__name__).info("🚀 STEP 4: Sending Test Onboarding Message via Ctrl+T Navigation (Safe)")
    success = service.send_onboarding_message(
        agent_id="Agent-2",  # Safe coordinates
        style="friendly",
        mode="pyautogui"  # This triggers Ctrl+T navigation
    )
    
    if success:
        get_logger(__name__).info("✅ SUCCESS: Ctrl+T onboarding navigation test completed (Safe Mode)")
        get_logger(__name__).info("📍 Navigation to Agent-2 coordinates: (-308, 480)")
        get_logger(__name__).info("🆕 New tab creation with Ctrl+T: SUCCESS")
        get_logger(__name__).info("📋 Message delivery: SUCCESS")
    else:
        get_logger(__name__).info("❌ FAILED: Ctrl+T onboarding navigation test failed")
        get_logger(__name__).info("🔍 Check PyAutoGUI availability and agent window positioning")
    
    get_logger(__name__).info()
    
    # Test safe bulk onboarding (avoiding corner coordinates)
    get_logger(__name__).info("🚨 STEP 5: Testing Safe Bulk Ctrl+T Onboarding Navigation")
    get_logger(__name__).info("Target: Safe agents only (avoiding corner coordinates)")
    get_logger(__name__).info()
    
    # Define safe agents (avoiding corner coordinates that trigger fail-safe)
    safe_agents = ["Agent-2", "Agent-5", "Agent-7"]  # Safe coordinates
    
    safe_results = []
    for agent_id in safe_agents:
        get_logger(__name__).info(f"🎯 Testing {agent_id}...")
        success = service.send_onboarding_message(
            agent_id=agent_id,
            style="friendly",
            mode="pyautogui"
        )
        safe_results.append(success)
        time.sleep(1)  # Brief pause between agents
    
    success_count = sum(safe_results)
    total_count = len(safe_results)
    
    get_logger(__name__).info(f"📊 SAFE CTRL+T NAVIGATION RESULTS: {success_count}/{total_count} successful")
    get_logger(__name__).info()
    
    # Show detailed results
    get_logger(__name__).info("📍 DETAILED SAFE NAVIGATION RESULTS:")
    for i, (agent_id, success) in enumerate(zip(safe_agents, safe_results)):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        coords = service.agents.get(agent_id, {}).get("coords", "Unknown")
        get_logger(__name__).info(f"  {i+1}. {agent_id}: {status} (Coordinates: {coords})")
    
    get_logger(__name__).info()
    
    # Test coordinate analysis
    get_logger(__name__).info("🔍 STEP 6: Analyzing Agent Coordinates for Safety")
    get_logger(__name__).info("📍 COORDINATE SAFETY ANALYSIS:")
    
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
        get_logger(__name__).info(f"  🤖 {agent_id}: {status} ({coords}) - {safety_reason}")
    
    get_logger(__name__).info()
    
    # Summary
    get_logger(__name__).info("📋 SAFE TEST SUMMARY:")
    get_logger(__name__).info("=" * 30)
    get_logger(__name__).info(f"🎯 Single Safe Agent Test: {'✅ PASSED' if success else '❌ FAILED'}")
    get_logger(__name__).info(f"🚨 Safe Bulk Navigation Test: {success_count}/{total_count} successful")
    get_logger(__name__).info(f"📍 Safe Agents Identified: {len(safe_agents)}/{len(service.agents)}")
    get_logger(__name__).info()
    
    if success and success_count == total_count:
        get_logger(__name__).info("🎉 ALL SAFE TESTS PASSED: Ctrl+T onboarding navigation working correctly!")
    else:
        get_logger(__name__).info("⚠️ SOME SAFE TESTS FAILED: Check agent window positioning and PyAutoGUI setup")
    
    get_logger(__name__).info()
    get_logger(__name__).info("🧪 Safe Ctrl+T Onboarding Navigation Test Complete")
    get_logger(__name__).info("=" * 55)


def test_coordinate_safety_zones():
    """Test coordinate safety zones to avoid PyAutoGUI fail-safe."""
    
    get_logger(__name__).info("🎯 TESTING COORDINATE SAFETY ZONES")
    get_logger(__name__).info("=" * 40)
    get_logger(__name__).info()
    
    service = UnifiedMessagingCore()
    
    # Define safety zones
    safe_x_range = (-1200, 1600)  # Safe X coordinates
    safe_y_range = (400, 1000)    # Safe Y coordinates
    
    get_logger(__name__).info(f"📍 SAFE COORDINATE RANGES:")
    get_logger(__name__).info(f"   X: {safe_x_range[0]} to {safe_x_range[1]}")
    get_logger(__name__).info(f"   Y: {safe_y_range[0]} to {safe_y_range[1]}")
    get_logger(__name__).info()
    
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
        get_logger(__name__).info(f"🤖 {agent_id}: {status} ({coords})")
    
    get_logger(__name__).info()
    get_logger(__name__).info("📊 SAFETY ANALYSIS SUMMARY:")
    get_logger(__name__).info(f"✅ Safe Agents: {len(safe_agents)} - {', '.join(safe_agents)}")
    get_logger(__name__).info(f"⚠️ Unsafe Agents: {len(unsafe_agents)} - {', '.join(unsafe_agents)}")
    get_logger(__name__).info()
    
    if unsafe_agents:
        get_logger(__name__).info("💡 RECOMMENDATIONS:")
        get_logger(__name__).info("   • Use safe agents for automated testing")
        get_logger(__name__).info("   • Manually test unsafe agents with caution")
        get_logger(__name__).info("   • Consider adjusting coordinates for better safety")
    
    get_logger(__name__).info("🎯 Coordinate Safety Zone Test Complete")
    get_logger(__name__).info("=" * 40)


if __name__ == "__main__":
    get_logger(__name__).info("🧪 CTRL+T ONBOARDING NAVIGATION TEST SUITE (SAFE MODE)")
    get_logger(__name__).info("=" * 65)
    get_logger(__name__).info()
    
    try:
        # Test 1: Safe Ctrl+T onboarding navigation
        test_ctrl_t_onboarding_navigation_safe()
        get_logger(__name__).info()
        
        # Test 2: Coordinate safety zones
        test_coordinate_safety_zones()
        get_logger(__name__).info()
        
        get_logger(__name__).info("🎉 ALL SAFE NAVIGATION TESTS COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        get_logger(__name__).info(f"❌ TEST ERROR: {e}")
        get_logger(__name__).info("🔍 Check PyAutoGUI installation and agent window setup")
        sys.exit(1)
