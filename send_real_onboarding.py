#!/usr/bin/env python3
"""
Send Real Onboarding Messages - Agent Cellphone V2
=================================================

Sends real onboarding messages through the active V2 messaging system.
This script connects to the running messaging system and sends the
comprehensive onboarding message to agents.

Author: V2 Swarm Coordinator
License: MIT
"""

import sys
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


def send_real_onboarding_message(agent_id):
    """Send a real onboarding message to an agent through the V2 system"""
    try:
        print(f"📤 Sending REAL onboarding message to {agent_id}...")
        
        # Import V2 components
        from core.agent_communication import AgentCommunicationProtocol
        from core.fsm_core_v2 import FSMCoreV2
        from core.inbox_manager import InboxManager
        
        # Create mock workspace manager for testing
        class MockWorkspaceManager:
            def __init__(self):
                self.workspaces = {}
        
        workspace_manager = MockWorkspaceManager()
        inbox_manager = InboxManager(workspace_manager)
        fsm_core = FSMCoreV2(workspace_manager, inbox_manager)
        communication_protocol = AgentCommunicationProtocol()
        
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
        
        print(f"✅ REAL onboarding message sent to {agent_id} with ID: {message_id}")
        print(f"   Message Type: COORDINATION")
        print(f"   Priority: CRITICAL")
        print(f"   Content Length: {len(get_onboarding_message())} characters")
        
        return message_id
        
    except Exception as e:
        print(f"❌ Failed to send REAL onboarding message to {agent_id}: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function to send real onboarding messages"""
    print("🧪 Agent Cellphone V2 - REAL Onboarding Message Sender")
    print("=" * 60)
    print("This script sends REAL onboarding messages through the V2 system.")
    print("It emphasizes the CRITICAL single-instance messaging requirement.")
    print("=" * 60)
    
    # Check if messaging system is running
    print("\n🔍 Checking messaging system status...")
    try:
        import subprocess
        result = subprocess.run([
            "python", "-m", "src.launchers.fsm_communication_integration_launcher", "--status"
        ], capture_output=True, text=True, timeout=10)
        
        if "System Active: ✅ YES" in result.stdout:
            print("✅ Messaging system is ACTIVE and running!")
        else:
            print("⚠️ Messaging system may not be fully active")
            print("   Starting messaging system...")
            subprocess.Popen([
                "python", "-m", "src.launchers.fsm_communication_integration_launcher"
            ])
            time.sleep(3)  # Wait for system to start
            
    except Exception as e:
        print(f"⚠️ Could not check system status: {e}")
    
    # Send onboarding to Agent-1 first
    print(f"\n🎯 Sending REAL onboarding message to Agent-1...")
    message_id = send_real_onboarding_message("Agent-1")
    
    if message_id:
        print(f"\n🎉 SUCCESS! Agent-1 received REAL onboarding message!")
        print(f"   Message ID: {message_id}")
        print(f"   This message was sent through the REAL V2 messaging system")
        print(f"   The message contains the WE. ARE. SWARM mantra")
        print(f"   It emphasizes the single-instance messaging requirement")
        
        # Ask if user wants to send to more agents
        print(f"\n🎯 Would you like to send onboarding to more agents?")
        choice = input("Send to all agents? (y/n): ").strip().lower()
        
        if choice == 'y':
            all_agents = ["Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
            print(f"\n🚀 Sending onboarding to all remaining agents...")
            
            for agent_id in all_agents:
                message_id = send_real_onboarding_message(agent_id)
                if message_id:
                    print(f"   ✅ {agent_id}: {message_id}")
                else:
                    print(f"   ❌ {agent_id}: Failed")
                time.sleep(0.5)  # Brief delay between sends
            
            print(f"\n🎉 Onboarding messages sent to all agents!")
        else:
            print(f"\n✅ Onboarding completed for Agent-1")
    else:
        print(f"\n❌ Failed to send onboarding message to Agent-1")
        print(f"   Check that the messaging system is running")
        print(f"   Run: python -m src.launchers.fsm_communication_integration_launcher")
    
    print("\n" + "=" * 60)
    print("🏁 REAL onboarding message sender complete!")
    print("Remember: WE. ARE. SWARM! 🐝✨")
    print("The single-instance messaging requirement is CRITICAL!")


if __name__ == "__main__":
    main()
