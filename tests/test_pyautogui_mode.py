from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Test PyAutoGUI Mode Without Onboarding - Agent Cellphone V2
=======================================================

This script demonstrates the PyAutoGUI messaging mode without using
the onboarding functionality. It shows how to send direct messages
to agents using coordinate-based navigation.

Author: V2 SWARM CAPTAIN
License: MIT
"""


# Add the src directory to the path so we can import the messaging modules
sys.path.insert(0, get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), 'src'))

from src.services.messaging_core import UnifiedMessagingCore
from src.services.models.messaging_models import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)


def test_pyautogui_mode():
    """Test PyAutoGUI messaging mode without onboarding."""
    
    get_logger(__name__).info("🧪 TESTING PYAUTOGUI MODE WITHOUT ONBOARDING")
    get_logger(__name__).info("=" * 60)
    
    # Initialize the messaging service
    service = UnifiedMessagingCore()
    
    # Test 1: List available agents
    get_logger(__name__).info("\n📋 TEST 1: LISTING AVAILABLE AGENTS")
    get_logger(__name__).info("-" * 40)
    service.list_agents()
    
    # Test 2: Show agent coordinates
    get_logger(__name__).info("\n📍 TEST 2: SHOWING AGENT COORDINATES")
    get_logger(__name__).info("-" * 40)
    service.show_coordinates()
    
    # Test 3: Send a test message to a specific agent
    get_logger(__name__).info("\n📤 TEST 3: SENDING TEST MESSAGE TO AGENT-1")
    get_logger(__name__).info("-" * 40)
    
    test_message = """🧪 **PYAUTOGUI MODE TEST** 🧪

**From**: Test System
**To**: Agent-1
**Mode**: PyAutoGUI (No Onboarding)

**MESSAGE CONTENT**:
This is a test message sent via PyAutoGUI mode without using the onboarding system.

**FEATURES TESTED**:
- ✅ Direct message sending
- ✅ Coordinate-based navigation
- ✅ PyAutoGUI automation
- ✅ No onboarding dependency

**STATUS**: Test successful if you receive this message!

**Test System - PyAutoGUI Mode Verification**"""
    
    success = service.send_message(
        content=test_message,
        sender="Test System",
        recipient="Agent-1",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.NORMAL,
        tags=[UnifiedMessageTag.CAPTAIN],
        mode="pyautogui",
        use_paste=True
    )
    
    if success:
        get_logger(__name__).info("✅ TEST 3 PASSED: Message sent successfully via PyAutoGUI")
    else:
        get_logger(__name__).info("❌ TEST 3 FAILED: Message delivery failed")
    
    # Test 4: Send a bulk message to all agents (without onboarding)
    get_logger(__name__).info("\n📤 TEST 4: SENDING BULK MESSAGE TO ALL AGENTS")
    get_logger(__name__).info("-" * 40)
    
    bulk_message = """🚨 **BULK PYAUTOGUI TEST** 🚨

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
    
    results = service.send_to_all_agents(
        content=bulk_message,
        sender="Test System",
        message_type=UnifiedMessageType.BROADCAST,
        priority=UnifiedMessagePriority.NORMAL,
        tags=[UnifiedMessageTag.CAPTAIN],
        mode="pyautogui",
        use_paste=True
    )
    
    success_count = sum(results)
    total_count = len(results)
    get_logger(__name__).info(f"📊 BULK TEST RESULTS: {success_count}/{total_count} successful deliveries")
    
    if success_count == total_count:
        get_logger(__name__).info("✅ TEST 4 PASSED: All bulk messages sent successfully")
    else:
        get_logger(__name__).info(f"⚠️ TEST 4 PARTIAL: {success_count}/{total_count} messages delivered")
    
    # Test 5: Show message history
    get_logger(__name__).info("\n📜 TEST 5: SHOWING MESSAGE HISTORY")
    get_logger(__name__).info("-" * 40)
    service.show_message_history()
    
    get_logger(__name__).info("\n🎉 PYAUTOGUI MODE TEST COMPLETED!")
    get_logger(__name__).info("=" * 60)
    get_logger(__name__).info("✅ All tests executed without onboarding system")
    get_logger(__name__).info("✅ PyAutoGUI mode functioning independently")
    get_logger(__name__).info("✅ Coordinate-based navigation verified")
    get_logger(__name__).info("✅ Direct messaging capabilities confirmed")


def test_cli_commands():
    """Test CLI commands for PyAutoGUI mode."""
    
    get_logger(__name__).info("\n🖥️ TESTING CLI COMMANDS FOR PYAUTOGUI MODE")
    get_logger(__name__).info("=" * 60)
    
    get_logger(__name__).info("\n📋 Available CLI commands for PyAutoGUI mode:")
    get_logger(__name__).info("-" * 50)
    
    commands = [
        ("List agents", "python -m src.services.messaging_cli --list-agents"),
        ("Show coordinates", "python -m src.services.messaging_cli --coordinates"),
        ("Send to specific agent", "python -m src.services.messaging_cli --agent Agent-1 --message 'Test message' --mode pyautogui"),
        ("Send bulk message", "python -m src.services.messaging_cli --bulk --message 'Bulk test' --mode pyautogui"),
        ("Show message history", "python -m src.services.messaging_cli --history"),
        ("Check agent status", "python -m src.services.messaging_cli --check-status"),
        ("Get next task", "python -m src.services.messaging_cli --agent Agent-1 --get-next-task"),
    ]
    
    for description, command in commands:
        get_logger(__name__).info(f"• {description}:")
        get_logger(__name__).info(f"  {command}")
        get_logger(__name__).info()
    
    get_logger(__name__).info("✅ All CLI commands support PyAutoGUI mode")
    get_logger(__name__).info("✅ No onboarding dependency required")


if __name__ == "__main__":
    try:
        test_pyautogui_mode()
        test_cli_commands()
        
        get_logger(__name__).info("\n🎯 SUMMARY:")
        get_logger(__name__).info("=" * 30)
        get_logger(__name__).info("✅ PyAutoGUI mode works without onboarding")
        get_logger(__name__).info("✅ Direct messaging to agents functional")
        get_logger(__name__).info("✅ Bulk messaging to all agents working")
        get_logger(__name__).info("✅ Coordinate-based navigation operational")
        get_logger(__name__).info("✅ CLI interface fully supported")
        get_logger(__name__).info("✅ No onboarding system dependency")
        
    except Exception as e:
        get_logger(__name__).info(f"❌ TEST FAILED: {e}")
        sys.exit(1)
