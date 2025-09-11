#!/usr/bin/env python3
"""
Agent Message Template - Stripped-down template for easy agent messaging.
Use this to quickly send messages to any agent with full enhanced guidance.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.messaging_core import send_message, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag

def send_template_message(recipient: str, content: str, sender: str = "CAPTAIN"):
    """Send a template message with full enhanced guidance to any agent."""
    
    # Available agents
    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    
    if recipient not in agents:
        print(f"❌ Invalid agent: {recipient}")
        print(f"Available agents: {', '.join(agents)}")
        return False
    
    print(f"📤 Sending template message to {recipient}...")
    print(f"📝 Content: {content[:50]}...")
    
    success = send_message(
        content=content,
        sender=sender,
        recipient=recipient,
        message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.SYSTEM]
    )
    
    if success:
        print(f"✅ Template message sent to {recipient}!")
        print("📋 Message includes:")
        print("   • Clean markdown formatting")
        print("   • Inbox checking guidance")
        print("   • Message sending commands")
        print("   • Discord devlog instructions")
        print("   • 5-step protocol")
    else:
        print(f"❌ Failed to send message to {recipient}")
    
    return success

def send_broadcast_template(content: str, sender: str = "CAPTAIN"):
    """Send template message to all agents."""
    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    
    print(f"📢 Broadcasting template message to all agents...")
    print(f"📝 Content: {content[:50]}...")
    
    results = {}
    for agent in agents:
        success = send_message(
            content=content,
            sender=sender,
            recipient=agent,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.REGULAR,
            tags=[UnifiedMessageTag.SYSTEM]
        )
        results[agent] = success
        status = "✅" if success else "❌"
        print(f"   {status} {agent}")
    
    successful = sum(1 for success in results.values() if success)
    print(f"\n🎯 Broadcast complete: {successful}/{len(agents)} agents received message")
    
    return results

if __name__ == "__main__":
    # Example usage
    print("🤖 Agent Message Template System")
    print("=" * 40)
    
    # Send to specific agent
    send_template_message("Agent-4", "This is a test template message with enhanced guidance.")
    
    # Uncomment to broadcast to all agents
    # send_broadcast_template("Broadcast message to all agents with enhanced guidance.")
