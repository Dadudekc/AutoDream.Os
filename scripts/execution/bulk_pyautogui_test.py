from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
🚨 BULK PYAUTOGUI TEST - Agent Cellphone V2 🚨
============================================

Bulk PyAutoGUI test for coordinate-based message delivery to all agents.

Author: V2 SWARM CAPTAIN
License: MIT
"""


# Add src to path for imports
sys.path.insert(0, get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), 'src'))

    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)


def run_bulk_pyautogui_test():
    """Execute bulk PyAutoGUI test to all agents."""
    
    get_logger(__name__).info("🚨 **BULK PYAUTOGUI TEST** 🚨")
    get_logger(__name__).info("=" * 50)
    get_logger(__name__).info()
    
    # Initialize messaging core
    messaging_core = UnifiedMessagingCore()
    
    # Test message content
    test_message = """🚨 **BULK PYAUTOGUI TEST** 🚨

**From**: Test System
**Mode**: PyAutoGUI Bulk Delivery (No Onboarding)

**BULK MESSAGE**:
This is a bulk test message sent to all agents via PyAutoGUI mode.
The system is testing coordinate-based navigation and automated messaging.

**TEST PARAMETERS**:
- ✅ Bulk delivery to all agents
- ✅ PyAutoGUI automation
- ✅ No onboarding system used
- ✅ Direct message routing

**EXPECTED RESULT**: All agents should receive this message via their coordinates.

**Test System - Bulk PyAutoGUI Verification**"""
    
    get_logger(__name__).info("📋 TEST PARAMETERS:")
    get_logger(__name__).info(f"   • Bulk delivery to all agents: ✅")
    get_logger(__name__).info(f"   • PyAutoGUI automation: ✅")
    get_logger(__name__).info(f"   • No onboarding system used: ✅")
    get_logger(__name__).info(f"   • Direct message routing: ✅")
    get_logger(__name__).info()
    
    get_logger(__name__).info("📍 AGENT COORDINATES:")
    messaging_core.show_coordinates()
    
    get_logger(__name__).info("🚀 STARTING BULK PYAUTOGUI DELIVERY...")
    get_logger(__name__).info("=" * 50)
    
    # Send bulk message to all agents
    results = messaging_core.send_to_all_agents(
        content=test_message,
        sender="Test System",
        message_type=UnifiedMessageType.BROADCAST,
        priority=UnifiedMessagePriority.URGENT,
        tags=[UnifiedMessageTag.CAPTAIN],
        metadata={
            "test_type": "bulk_pyautogui",
            "timestamp": datetime.now().isoformat(),
            "mode": "coordinate_based",
            "onboarding_used": False
        },
        mode="pyautogui",
        use_paste=True
    )
    
    get_logger(__name__).info()
    get_logger(__name__).info("📊 TEST RESULTS:")
    get_logger(__name__).info("=" * 30)
    
    # CORRECT ORDER: Agent-4 LAST
    agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
    
    success_count = sum(results)
    total_count = len(results)
    
    for i, (agent_id, success) in enumerate(zip(agent_order, results)):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        get_logger(__name__).info(f"{i+1:2d}. {agent_id}: {status}")
    
    get_logger(__name__).info()
    get_logger(__name__).info(f"📈 OVERALL RESULTS: {success_count}/{total_count} successful deliveries")
    
    if success_count == total_count:
        get_logger(__name__).info("🎉 **ALL AGENTS RECEIVED BULK PYAUTOGUI TEST MESSAGE** 🎉")
    else:
        get_logger(__name__).info(f"⚠️  **PARTIAL SUCCESS**: {total_count - success_count} agents failed to receive message")
    
    get_logger(__name__).info()
    get_logger(__name__).info("🔍 VERIFICATION:")
    get_logger(__name__).info("   • Check each agent's interface for the test message")
    get_logger(__name__).info("   • Verify coordinate-based navigation worked correctly")
    get_logger(__name__).info("   • Confirm PyAutoGUI automation completed successfully")
    get_logger(__name__).info()
    get_logger(__name__).info("**BULK PYAUTOGUI TEST COMPLETED** 🚨")


if __name__ == "__main__":
    try:
        run_bulk_pyautogui_test()
    except KeyboardInterrupt:
        get_logger(__name__).info("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        get_logger(__name__).info(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
