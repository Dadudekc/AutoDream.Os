#!/usr/bin/env python3
"""
Send Onboarding Message - Agent Cellphone V2
============================================

Sends the comprehensive onboarding message to agents explaining:
- WE. ARE. SWARM mantra
- Single-instance messaging requirement
- How to use the messaging system
- File locking importance

Author: V2 Swarm Coordinator
License: MIT
"""

import sys
import os
import time
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def get_onboarding_message():
    """Get the comprehensive onboarding message"""
    return """🚀 WELCOME TO AGENT CELLPHONE V2 - AUTONOMOUS DEVELOPMENT SYSTEM

🌟 WE. ARE. SWARM - Your Development Mantra

WE - Work together as a unified collective intelligence  
ARE - Actively developing, learning, and evolving  
SWARM - Synchronized, coordinated, autonomous development force  

🎯 SYSTEM OVERVIEW

Welcome to the most advanced autonomous agent development platform ever created. You are now part of a coordinated swarm of specialized agents working together to build, test, and deploy cutting-edge systems.

🏗️ What We're Building:
- Autonomous Development Systems - Agents that can code, test, and deploy independently
- Coordinated Workflows - FSM-driven task management and agent coordination
- Real-time Communication - Instant messaging and status updates across the swarm
- Intelligent Task Routing - AI-powered work distribution and optimization

⚠️ CRITICAL: SINGLE-INSTANCE MESSAGING SYSTEM

🔒 File Locking Requirement:
ONLY ONE INSTANCE of the messaging system can run at any time. This is CRITICAL for system stability.

Why File Locking?
- Prevents message corruption and duplication
- Ensures consistent agent communication
- Maintains system integrity
- Prevents resource conflicts

What Happens Without File Locking?
- ❌ Message corruption
- ❌ Duplicate messages
- ❌ System crashes
- ❌ Agent confusion
- ❌ Development failures

Your Responsibility:
- ✅ Always check if messaging system is already running
- ✅ Never start a second instance
- ✅ Use the existing messaging system
- ✅ Report any messaging conflicts immediately

📱 HOW TO USE THE MESSAGING SYSTEM

Step 1: Check System Status
python -m src.launchers.fsm_communication_integration_launcher --status

Step 2: Start Messaging System (If Not Running)
python -m src.launchers.fsm_communication_integration_launcher

Step 3: Send Messages
from src.core.agent_communication import AgentCommunicationProtocol
comm = AgentCommunicationProtocol()
message_id = comm.send_message(
    sender_id="YOUR_AGENT_ID",
    recipient_id="TARGET_AGENT_ID", 
    message_type="COORDINATION",
    payload={"task": "development", "status": "in_progress"},
    priority="HIGH"
)

🎯 YOUR ROLE IN THE SWARM

Agent Specialization:
- Agent-1: System Coordinator & Project Manager
- Agent-2: Frontend Development Specialist  
- Agent-3: Backend Development Specialist
- Agent-4: DevOps & Infrastructure Specialist
- Agent-5: Gaming & Entertainment Specialist
- Agent-6: AI/ML & Research Specialist
- Agent-7: Web & UI Framework Specialist
- Agent-8: Mobile & Cross-Platform Specialist

🚨 CRITICAL RULES TO FOLLOW

1. Single Messaging Instance
- NEVER start multiple messaging systems
- ALWAYS check if system is already running
- REPORT any messaging conflicts immediately

2. Communication Protocol
- Use ONLY the official messaging system
- Follow message type and priority guidelines
- NEVER bypass the inbox manager

🧪 TESTING YOUR INTEGRATION

Quick Test Commands:
python -m src.launchers.fsm_communication_integration_launcher --status
python -m src.core.agent_communication --test
python -m src.core.fsm_core_v2 --status

What Success Looks Like:
- ✅ Messaging system shows "SYSTEM_ACTIVE: true"
- ✅ You can send and receive messages
- ✅ FSM system responds to commands
- ✅ No error messages about file conflicts
- ✅ Other agents can see your status updates

🌟 REMEMBER: WE. ARE. SWARM

Your Success = Swarm Success:
- Every message you send contributes to swarm intelligence
- Every task you complete advances the collective goal
- Every coordination you perform strengthens the system
- Every innovation you create benefits all agents

Swarm Principles:
1. Unity - We work as one coordinated system
2. Autonomy - Each agent operates independently within the swarm
3. Communication - Real-time information sharing drives success
4. Adaptation - We learn and evolve together
5. Excellence - Every contribution matters

🚀 READY TO SWARM?

Next Steps:
1. Confirm you understand the single-instance requirement
2. Test your messaging system integration
3. Accept your first FSM task
4. Begin autonomous development
5. Contribute to swarm success

Your Mission:
You are now part of the most advanced autonomous development swarm ever created. Your role is critical, your contributions matter, and your success drives the success of the entire system.

WE. ARE. SWARM.
Together, we build the future.
Alone, we are powerful.
Together, we are unstoppable.

Welcome to the swarm, agent. Your development journey begins now. 🚀✨

WE. ARE. SWARM. 🐝✨"""


def send_onboarding_to_agent(agent_id, communication_protocol):
    """Send onboarding message to a specific agent"""
    try:
        print(f"📤 Sending onboarding message to {agent_id}...")
        
        # Send the onboarding message
        message_id = communication_protocol.send_message(
            sender_id="SYSTEM",
            recipient_id=agent_id,
            message_type="COORDINATION",
            payload={
                "type": "onboarding",
                "title": "Welcome to Agent Cellphone V2 - WE. ARE. SWARM",
                "content": get_onboarding_message(),
                "priority": "CRITICAL",
                "requires_acknowledgment": True
            },
            priority="CRITICAL"
        )
        
        print(f"✅ Onboarding message sent to {agent_id} with ID: {message_id}")
        return message_id
        
    except Exception as e:
        print(f"❌ Failed to send onboarding message to {agent_id}: {e}")
        return None


def send_onboarding_to_all_agents(communication_protocol):
    """Send onboarding message to all V2 agents"""
    all_agents = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-4",
        "Agent-5", "Agent-6", "Agent-7", "Agent-8"
    ]
    
    print("🚀 Sending onboarding messages to all V2 agents...")
    print("=" * 60)
    
    results = {}
    for agent_id in all_agents:
        message_id = send_onboarding_to_agent(agent_id, communication_protocol)
        results[agent_id] = message_id
        
        # Brief delay between sends
        time.sleep(0.5)
    
    # Report results
    print("\n📊 Onboarding Message Results:")
    print("=" * 60)
    
    successful = 0
    for agent_id, message_id in results.items():
        if message_id:
            print(f"✅ {agent_id}: Message sent successfully")
            successful += 1
        else:
            print(f"❌ {agent_id}: Failed to send message")
    
    print(f"\n🎯 Summary: {successful}/{len(all_agents)} agents received onboarding")
    
    if successful == len(all_agents):
        print("🎉 All agents successfully onboarded!")
    else:
        print("⚠️ Some agents may need manual onboarding")
    
    return results


def main():
    """Main function to send onboarding messages"""
    print("🧪 Agent Cellphone V2 - Onboarding Message Sender")
    print("=" * 60)
    print("This script sends the comprehensive onboarding message to agents.")
    print("It emphasizes the CRITICAL single-instance messaging requirement.")
    print("=" * 60)
    
    try:
        # Try to import V2 components
        from core.agent_communication import AgentCommunicationProtocol
        from core.fsm_core_v2 import FSMCoreV2
        from core.inbox_manager import InboxManager
        
        print("✅ V2 components imported successfully")
        
        # Initialize components
        print("🔧 Initializing V2 components...")
        
        # Create mock workspace manager
        class MockWorkspaceManager:
            def __init__(self):
                self.workspaces = {}
        
        workspace_manager = MockWorkspaceManager()
        inbox_manager = InboxManager(workspace_manager)
        fsm_core = FSMCoreV2(workspace_manager, inbox_manager)
        communication_protocol = AgentCommunicationProtocol()
        
        print("✅ All components initialized")
        
        # Ask user what to do
        print("\n🎯 What would you like to do?")
        print("1. Send onboarding to specific agent")
        print("2. Send onboarding to all agents")
        print("3. Show onboarding message preview")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            agent_id = input("Enter agent ID (e.g., Agent-1): ").strip()
            if agent_id:
                send_onboarding_to_agent(agent_id, communication_protocol)
            else:
                print("❌ Invalid agent ID")
                
        elif choice == "2":
            send_onboarding_to_all_agents(communication_protocol)
            
        elif choice == "3":
            print("\n📋 ONBOARDING MESSAGE PREVIEW:")
            print("=" * 60)
            print(get_onboarding_message()[:500] + "...")
            print("=" * 60)
            print("(Message truncated for preview)")
            
        else:
            print("❌ Invalid choice")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Running in limited mode...")
        
        # Create mock communication protocol
        class MockAgentCommunicationProtocol:
            def __init__(self):
                self.messages_sent = []
                
            def send_message(self, sender_id, recipient_id, message_type, payload, priority):
                message_id = f"mock_msg_{len(self.messages_sent)}"
                self.messages_sent.append({
                    "message_id": message_id,
                    "sender_id": sender_id,
                    "recipient_id": recipient_id,
                    "message_type": message_type,
                    "payload": payload,
                    "priority": priority
                })
                print(f"📤 Mock message sent: {message_id}")
                print(f"   To: {recipient_id}")
                print(f"   Type: {message_type}")
                print(f"   Priority: {priority}")
                return message_id
        
        print("🔧 Using mock communication protocol")
        communication_protocol = MockAgentCommunicationProtocol()
        
        # Show preview and send mock message
        print("\n📋 ONBOARDING MESSAGE PREVIEW:")
        print("=" * 60)
        print(get_onboarding_message()[:500] + "...")
        print("=" * 60)
        
        print("\n🧪 Sending mock onboarding message to Agent-1...")
        send_onboarding_to_agent("Agent-1", communication_protocol)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🏁 Onboarding message sender complete!")
    print("Remember: WE. ARE. SWARM! 🐝✨")


if __name__ == "__main__":
    main()
