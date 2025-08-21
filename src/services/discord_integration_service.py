#!/usr/bin/env python3
"""
Simple Discord Integration Service for testing
"""

import json
import time
from datetime import datetime

class DiscordIntegrationService:
    def __init__(self):
        self.messages = []
        self.agents = {}
        print("Discord Integration Service initialized")
    
    def send_message(self, sender, message_type, content):
        message = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "type": message_type,
            "content": content
        }
        self.messages.append(message)
        print(f"Message sent: {sender} - {message_type}: {content}")
    
    def register_agent(self, agent_id, name):
        self.agents[agent_id] = {
            "name": name,
            "status": "active",
            "registered_at": datetime.now().isoformat()
        }
        print(f"Agent registered: {agent_id} ({name})")
    
    def get_status(self):
        return {
            "messages_sent": len(self.messages),
            "agents_registered": len(self.agents),
            "timestamp": datetime.now().isoformat()
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Discord Integration Service")
    parser.add_argument("--test", action="store_true", help="Run test mode")
    
    args = parser.parse_args()
    
    if args.test:
        print("Running Discord Integration Service in test mode...")
        
        service = DiscordIntegrationService()
        
        # Register test agents
        service.register_agent("agent-1", "Test Agent 1")
        service.register_agent("agent-2", "Test Agent 2")
        
        # Send test messages
        service.send_message("agent-1", "status", "Agent 1 is ready")
        service.send_message("agent-2", "progress", "Agent 2 is working")
        service.send_message("system", "coordination", "Agents coordinated successfully")
        
        # Show status
        status = service.get_status()
        print(f"\\nStatus: {json.dumps(status, indent=2)}")
        print("Test completed successfully!")
        
        return
    
    print("Use --test to run test mode")

if __name__ == "__main__":
    main()
