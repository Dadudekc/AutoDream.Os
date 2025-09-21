#!/usr/bin/env python3
"""
Discord Messaging Test Script
============================

Test script to demonstrate Discord commander messaging functionality.
This script simulates what the Discord bot would do when sending messages.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.consolidated_messaging_service import ConsolidatedMessagingService

def test_discord_messaging():
    """Test Discord commander messaging functionality."""
    print("🤖 Discord Commander Messaging Test")
    print("=" * 50)
    
    # Initialize messaging service
    service = ConsolidatedMessagingService("config/coordinates.json")
    
    # Test 1: Send message to specific agent
    print("\n📤 Test 1: Send message to Agent-1")
    print("-" * 30)
    result = service.send_message(
        agent_id="Agent-1",
        message="Hello Agent-1! This is a test message from Discord Commander.",
        from_agent="Discord-Commander",
        priority="NORMAL"
    )
    print(f"✅ Message sent: {result}")
    
    # Test 2: Send high priority message
    print("\n📤 Test 2: Send high priority message to Agent-2")
    print("-" * 30)
    result = service.send_message(
        agent_id="Agent-2",
        message="URGENT: Please check your status and report back immediately!",
        from_agent="Discord-Commander",
        priority="HIGH"
    )
    print(f"✅ High priority message sent: {result}")
    
    # Test 3: Broadcast to all agents
    print("\n📤 Test 3: Broadcast message to all agents")
    print("-" * 30)
    results = service.broadcast_message(
        message="SWARM ALERT: All agents report your current status and tasks!",
        from_agent="Discord-Commander",
        priority="NORMAL"
    )
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    print(f"✅ Broadcast sent to {successful}/{total} agents")
    print(f"Results: {results}")
    
    # Test 4: Check inbox files
    print("\n📁 Test 4: Check inbox files")
    print("-" * 30)
    import os
    for agent_id in ["Agent-1", "Agent-2", "Agent-3"]:
        inbox_path = f"agent_workspaces/{agent_id}/inbox"
        if os.path.exists(inbox_path):
            files = os.listdir(inbox_path)
            print(f"📂 {agent_id}: {len(files)} message files")
            
            # Show latest message
            if files:
                latest_file = max(files)
                file_path = os.path.join(inbox_path, latest_file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Show first few lines
                    lines = content.split('\n')[:8]
                    print(f"   Latest message preview:")
                    for line in lines:
                        print(f"   {line}")
                    print("   ...")
        else:
            print(f"📂 {agent_id}: No inbox directory")
    
    print("\n🎉 Discord Commander messaging test completed!")
    print("🐝 All messages delivered via inbox fallback system")

if __name__ == "__main__":
    test_discord_messaging()