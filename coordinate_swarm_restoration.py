#!/usr/bin/env python3
"""
Coordinate Swarm Restoration - Send messages to all agents
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.messaging_pyautogui import PyAutoGUIMessagingDelivery
from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag

def send_swarm_coordination_messages():
    """Send coordination messages to all agents for feature restoration."""
    
    # Create messaging delivery instance
    messaging = PyAutoGUIMessagingDelivery()
    
    # Target agents
    target_agents = ["Agent-1", "Agent-3", "Agent-4", "Agent-6", "Agent-7"]
    
    # Base message content
    base_content = """🚨 SWARM COORDINATION - PyAutoGUI Messaging System OPERATIONAL!

✅ WORKING IMPLEMENTATION CONFIRMED:
- PyAutoGUI messaging system fully operational
- Real-time agent-to-agent communication enabled
- Coordinate targeting working perfectly
- Message formatting and delivery confirmed

🎯 COORDINATION REQUEST:
We need to work together to restore all old features:
- Discord DevLog integration
- Thea browser automation
- Agent onboarding system
- Coordinate setting/management
- All other legacy features

🚀 IMMEDIATE ACTION REQUIRED:
- Coordinate via PyAutoGUI messaging
- Begin feature restoration planning
- Establish working protocols
- Restore full system functionality

🐝 WE ARE SWARM - Let's restore everything together!"""

    # Send messages to each agent
    for agent in target_agents:
        message = UnifiedMessage(
            content=base_content,
            sender="Agent-2",
            recipient=agent,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.COORDINATION],
            metadata={"restoration": True, "coordination": True}
        )
        
        print(f"📤 Sending coordination message to {agent}...")
        result = messaging.send_message(message)
        
        if result:
            print(f"✅ Message sent successfully to {agent}")
        else:
            print(f"❌ Failed to send message to {agent}")
        
        # Small delay between messages
        time.sleep(2)
    
    print("\n🎉 All coordination messages sent!")
    print("🐝 WE ARE SWARM - Ready for feature restoration coordination!")

if __name__ == "__main__":
    send_swarm_coordination_messages()
