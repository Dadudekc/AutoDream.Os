#!/usr/bin/env python3
"""
Simple Agent Message Sender - Agent Cellphone V2
===============================================

Quick script to send messages to agents using the V2 system.
"""

import sys
import os
import json
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

def send_message_to_agent(agent_id, message, high_priority=False):
    """Send a message to a specific agent."""
    
    # Create message data
    message_data = {
        "from": "Captain-5",
        "to": agent_id,
        "message": message,
        "priority": "HIGH" if high_priority else "NORMAL",
        "timestamp": "2024-08-19T11:25:00Z",
        "type": "coordination_directive"
    }
    
    # Save message to agent's inbox
    inbox_path = Path(f"agent_workspaces/{agent_id}/inbox")
    inbox_path.mkdir(parents=True, exist_ok=True)
    
    # Create message file
    message_file = inbox_path / f"message_{len(list(inbox_path.glob('*.json')))}.json"
    
    with open(message_file, 'w') as f:
        json.dump(message_data, f, indent=2)
    
    print(f"✅ Message sent to {agent_id}")
    print(f"📁 Saved to: {message_file}")
    print(f"📝 Message: {message[:100]}...")
    
    return True

def main():
    """Main function to send messages."""
    if len(sys.argv) < 3:
        print("Usage: python send_agent_message.py <agent_id> <message> [--high-priority]")
        print("Example: python send_agent_message.py Agent-4 'Hello from Captain-5!' --high-priority")
        return
    
    agent_id = sys.argv[1]
    message = sys.argv[2]
    high_priority = "--high-priority" in sys.argv
    
    print(f"📱 Sending message to {agent_id}...")
    print(f"🔑 Priority: {'HIGH' if high_priority else 'NORMAL'}")
    print(f"📝 Message: {message}")
    print("-" * 50)
    
    success = send_message_to_agent(agent_id, message, high_priority)
    
    if success:
        print(f"🎯 Message successfully delivered to {agent_id}")
        print(f"📊 Check {agent_id}'s inbox for the message")
    else:
        print(f"❌ Failed to send message to {agent_id}")

if __name__ == "__main__":
    main()
