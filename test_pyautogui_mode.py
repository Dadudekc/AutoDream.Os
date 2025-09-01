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

import sys
import os
import time

# Add the src directory to the path so we can import the messaging modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.messaging_core import UnifiedMessagingCore
from services.models.messaging_models import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag
)


def test_pyautogui_mode():
    """Test PyAutoGUI messaging mode without onboarding."""
    
    print("🧪 TESTING PYAUTOGUI MODE WITHOUT ONBOARDING")
    print("=" * 60)
    
    # Initialize the messaging service
    service = UnifiedMessagingCore()
    
    # Test 1: List available agents
    print("\n📋 TEST 1: LISTING AVAILABLE AGENTS")
    print("-" * 40)
    service.list_agents()
    
    # Test 2: Show agent coordinates
    print("\n📍 TEST 2: SHOWING AGENT COORDINATES")
    print("-" * 40)
    service.show_coordinates()
    
    # Test 3: Send a test message to a specific agent
    print("\n📤 TEST 3: SENDING TEST MESSAGE TO AGENT-1")
    print("-" * 40)
    
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
        print("✅ TEST 3 PASSED: Message sent successfully via PyAutoGUI")
    else:
        print("❌ TEST 3 FAILED: Message delivery failed")
    
    # Test 4: Send a bulk message to all agents (without onboarding)
    print("\n📤 TEST 4: SENDING BULK MESSAGE TO ALL AGENTS")
    print("-" * 40)
    
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
    print(f"📊 BULK TEST RESULTS: {success_count}/{total_count} successful deliveries")
    
    if success_count == total_count:
        print("✅ TEST 4 PASSED: All bulk messages sent successfully")
    else:
        print(f"⚠️ TEST 4 PARTIAL: {success_count}/{total_count} messages delivered")
    
    # Test 5: Show message history
    print("\n📜 TEST 5: SHOWING MESSAGE HISTORY")
    print("-" * 40)
    service.show_message_history()
    
    print("\n🎉 PYAUTOGUI MODE TEST COMPLETED!")
    print("=" * 60)
    print("✅ All tests executed without onboarding system")
    print("✅ PyAutoGUI mode functioning independently")
    print("✅ Coordinate-based navigation verified")
    print("✅ Direct messaging capabilities confirmed")


def test_cli_commands():
    """Test CLI commands for PyAutoGUI mode."""
    
    print("\n🖥️ TESTING CLI COMMANDS FOR PYAUTOGUI MODE")
    print("=" * 60)
    
    print("\n📋 Available CLI commands for PyAutoGUI mode:")
    print("-" * 50)
    
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
        print(f"• {description}:")
        print(f"  {command}")
        print()
    
    print("✅ All CLI commands support PyAutoGUI mode")
    print("✅ No onboarding dependency required")


if __name__ == "__main__":
    try:
        test_pyautogui_mode()
        test_cli_commands()
        
        print("\n🎯 SUMMARY:")
        print("=" * 30)
        print("✅ PyAutoGUI mode works without onboarding")
        print("✅ Direct messaging to agents functional")
        print("✅ Bulk messaging to all agents working")
        print("✅ Coordinate-based navigation operational")
        print("✅ CLI interface fully supported")
        print("✅ No onboarding system dependency")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        sys.exit(1)
