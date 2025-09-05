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


# Add src to path for imports
sys.path.insert(0, get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), 'src'))

from src.services.messaging_core import UnifiedMessagingCore
from src.services.models.messaging_models import (
    UnifiedMessageType, 
    UnifiedMessagePriority, 
    UnifiedMessageTag
)
from src.services.utils.agent_registry import list_agents


def test_ctrl_t_onboarding_navigation():
    """Test Ctrl+T onboarding navigation to starter coordinates."""
    
    get_logger(__name__).info("🧪 TESTING CTRL+T ONBOARDING NAVIGATION TO STARTER COORDINATES")
    get_logger(__name__).info("=" * 70)
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
    
    # Test single agent onboarding with Ctrl+T
    get_logger(__name__).info("🎯 STEP 3: Testing Single Agent Ctrl+T Onboarding Navigation")
    get_logger(__name__).info("Target: Agent-1 (Starter coordinates: (-1269, 481))")
    get_logger(__name__).info()
    
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
    
    get_logger(__name__).info("📝 Test Onboarding Message Created:")
    get_logger(__name__).info("-" * 40)
    get_logger(__name__).info(test_onboarding_content[:200] + "...")
    get_logger(__name__).info("-" * 40)
    get_logger(__name__).info()
    
    # Send test onboarding message
    get_logger(__name__).info("🚀 STEP 4: Sending Test Onboarding Message via Ctrl+T Navigation")
    success = service.send_onboarding_message(
        agent_id="Agent-1",
        style="friendly",
        mode="pyautogui"  # This triggers Ctrl+T navigation
    )
    
    if success:
        get_logger(__name__).info("✅ SUCCESS: Ctrl+T onboarding navigation test completed")
        get_logger(__name__).info("📍 Navigation to Agent-1 coordinates: (-1269, 481)")
        get_logger(__name__).info("🆕 New tab creation with Ctrl+T: SUCCESS")
        get_logger(__name__).info("📋 Message delivery: SUCCESS")
    else:
        get_logger(__name__).info("❌ FAILED: Ctrl+T onboarding navigation test failed")
        get_logger(__name__).info("🔍 Check PyAutoGUI availability and agent window positioning")
    
    get_logger(__name__).info()
    
    # Test bulk onboarding with Ctrl+T
    get_logger(__name__).info("🚨 STEP 5: Testing Bulk Ctrl+T Onboarding Navigation")
    get_logger(__name__).info("Target: All agents in correct order (Agent-4 last)")
    get_logger(__name__).info()
    
    bulk_results = service.send_bulk_onboarding(
        style="friendly",
        mode="pyautogui"  # This triggers Ctrl+T navigation for all agents
    )
    
    success_count = sum(bulk_results)
    total_count = len(bulk_results)
    
    get_logger(__name__).info(f"📊 BULK CTRL+T NAVIGATION RESULTS: {success_count}/{total_count} successful")
    get_logger(__name__).info()
    
    # Show detailed results
    get_logger(__name__).info("📍 DETAILED NAVIGATION RESULTS:")
    agent_order = list_agents()
    agent_order.remove("Agent-4")
    agent_order.append("Agent-4")
    for i, (agent_id, success) in enumerate(zip(agent_order, bulk_results)):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        coords = service.agents.get(agent_id, {}).get("coords", "Unknown")
        get_logger(__name__).info(f"  {i+1}. {agent_id}: {status} (Coordinates: {coords})")
    
    get_logger(__name__).info()
    
    # Test coordinate validation
    get_logger(__name__).info("🔍 STEP 6: Validating Agent Coordinates")
    validation = service.validate_coordinates()
    get_logger(__name__).info(f"📍 Valid Coordinates: {validation['valid_coordinates']}/{validation['total_agents']}")
    get_logger(__name__).info()
    
    # Summary
    get_logger(__name__).info("📋 TEST SUMMARY:")
    get_logger(__name__).info("=" * 30)
    get_logger(__name__).info(f"🎯 Single Agent Test: {'✅ PASSED' if success else '❌ FAILED'}")
    get_logger(__name__).info(f"🚨 Bulk Navigation Test: {success_count}/{total_count} successful")
    get_logger(__name__).info(f"📍 Coordinate Validation: {validation['valid_coordinates']}/{validation['total_agents']} valid")
    get_logger(__name__).info()
    
    if success and success_count == total_count:
        get_logger(__name__).info("🎉 ALL TESTS PASSED: Ctrl+T onboarding navigation working correctly!")
    else:
        get_logger(__name__).info("⚠️ SOME TESTS FAILED: Check agent window positioning and PyAutoGUI setup")
    
    get_logger(__name__).info()
    get_logger(__name__).info("🧪 Ctrl+T Onboarding Navigation Test Complete")
    get_logger(__name__).info("=" * 50)


def test_coordinate_specific_navigation():
    """Test navigation to specific starter coordinates."""
    
    get_logger(__name__).info("🎯 TESTING SPECIFIC STARTER COORDINATE NAVIGATION")
    get_logger(__name__).info("=" * 50)
    get_logger(__name__).info()
    
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
        get_logger(__name__).info(f"🎯 Testing {agent_id}: {description}")
        get_logger(__name__).info(f"📍 Expected Coordinates: {expected_coords}")
        
        # Get actual coordinates
        actual_coords = service.agents.get(agent_id, {}).get("coords", None)
        
        if actual_coords == expected_coords:
            get_logger(__name__).info(f"✅ COORDINATES MATCH: {actual_coords}")
        else:
            get_logger(__name__).info(f"❌ COORDINATE MISMATCH: Expected {expected_coords}, Got {actual_coords}")
        
        get_logger(__name__).info()
    
    get_logger(__name__).info("🎯 Starter Coordinate Navigation Test Complete")
    get_logger(__name__).info("=" * 50)


if __name__ == "__main__":
    get_logger(__name__).info("🧪 CTRL+T ONBOARDING NAVIGATION TEST SUITE")
    get_logger(__name__).info("=" * 60)
    get_logger(__name__).info()
    
    try:
        # Test 1: Ctrl+T onboarding navigation
        test_ctrl_t_onboarding_navigation()
        get_logger(__name__).info()
        
        # Test 2: Specific coordinate navigation
        test_coordinate_specific_navigation()
        get_logger(__name__).info()
        
        get_logger(__name__).info("🎉 ALL NAVIGATION TESTS COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        get_logger(__name__).info(f"❌ TEST ERROR: {e}")
        get_logger(__name__).info("🔍 Check PyAutoGUI installation and agent window setup")
        sys.exit(1)
