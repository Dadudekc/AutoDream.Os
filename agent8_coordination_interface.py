#!/usr/bin/env python3
"""
Agent-8 Coordination Interface
==============================
Operations & Support Specialist coordination interface
"""

import sys
sys.path.append('.')

from datetime import datetime
from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
from src.core.messaging_pyautogui import deliver_message_pyautogui, format_message_for_delivery

def send_coordination_message(agent_id: str, message: str, priority: str = "NORMAL", tag: str = "COORDINATION"):
    """Send coordination message to specified agent."""
    try:
        # Create unified message
        unified_message = UnifiedMessage(
            content=message,
            sender="Agent-8",
            recipient=agent_id,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority(priority),
            tags=[UnifiedMessageTag(tag)],
            timestamp=datetime.now()
        )
        
        # Format and deliver message
        formatted_message = format_message_for_delivery(unified_message)
        success = deliver_message_pyautogui(unified_message)
        
        print(f"✅ Message sent to {agent_id}: {success}")
        return success
        
    except Exception as e:
        print(f"❌ Failed to send message to {agent_id}: {e}")
        return False

def broadcast_coordination_message(message: str, priority: str = "NORMAL", tag: str = "COORDINATION"):
    """Broadcast coordination message to all agents."""
    try:
        # Create unified message for broadcast
        unified_message = UnifiedMessage(
            content=message,
            sender="Agent-8",
            recipient="ALL_AGENTS",
            message_type=UnifiedMessageType.BROADCAST,
            priority=UnifiedMessagePriority(priority),
            tags=[UnifiedMessageTag(tag)],
            timestamp=datetime.now()
        )
        
        # Format and deliver message
        formatted_message = format_message_for_delivery(unified_message)
        success = deliver_message_pyautogui(unified_message)
        
        print(f"✅ Broadcast message sent: {success}")
        return success
        
    except Exception as e:
        print(f"❌ Failed to send broadcast message: {e}")
        return False

if __name__ == "__main__":
    # Test coordination interface
    print("🛠️ Agent-8 Coordination Interface Active")
    
    # Send message to Captain
    send_coordination_message(
        "Agent-4",
        "AGENT-8 OPERATIONS SPECIALIST: Enhanced cycle coordination active. FSM State: IDLE → ACTIVE. Contract system operational. Operations tools available. Multi-agent coordination active. Consolidation opportunities: 70+ files identified. Requesting Captain coordination for operations mission execution. WE ARE SWARM!",
        "NORMAL",
        "COORDINATION"
    )
