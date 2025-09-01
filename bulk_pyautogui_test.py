#!/usr/bin/env python3
"""
🚨 BULK PYAUTOGUI TEST - Agent Cellphone V2 🚨
============================================

Bulk PyAutoGUI test for coordinate-based message delivery to all agents.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import sys
import os
import time
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.messaging_core import UnifiedMessagingCore
from services.models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)


def run_bulk_pyautogui_test():
    """Execute bulk PyAutoGUI test to all agents."""
    
    print("🚨 **BULK PYAUTOGUI TEST** 🚨")
    print("=" * 50)
    print()
    
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
    
    print("📋 TEST PARAMETERS:")
    print(f"   • Bulk delivery to all agents: ✅")
    print(f"   • PyAutoGUI automation: ✅")
    print(f"   • No onboarding system used: ✅")
    print(f"   • Direct message routing: ✅")
    print()
    
    print("📍 AGENT COORDINATES:")
    messaging_core.show_coordinates()
    
    print("🚀 STARTING BULK PYAUTOGUI DELIVERY...")
    print("=" * 50)
    
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
    
    print()
    print("📊 TEST RESULTS:")
    print("=" * 30)
    
    # CORRECT ORDER: Agent-4 LAST
    agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
    
    success_count = sum(results)
    total_count = len(results)
    
    for i, (agent_id, success) in enumerate(zip(agent_order, results)):
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{i+1:2d}. {agent_id}: {status}")
    
    print()
    print(f"📈 OVERALL RESULTS: {success_count}/{total_count} successful deliveries")
    
    if success_count == total_count:
        print("🎉 **ALL AGENTS RECEIVED BULK PYAUTOGUI TEST MESSAGE** 🎉")
    else:
        print(f"⚠️  **PARTIAL SUCCESS**: {total_count - success_count} agents failed to receive message")
    
    print()
    print("🔍 VERIFICATION:")
    print("   • Check each agent's interface for the test message")
    print("   • Verify coordinate-based navigation worked correctly")
    print("   • Confirm PyAutoGUI automation completed successfully")
    print()
    print("**BULK PYAUTOGUI TEST COMPLETED** 🚨")


if __name__ == "__main__":
    try:
        run_bulk_pyautogui_test()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
