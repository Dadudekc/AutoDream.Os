#!/usr/bin/env python3
"""
Targeted Resume Demo - Send resume message to agents 5-8 only
"""

from src.services.v1_v2_message_queue_system import (
    MessageQueueManager,
    MessageQueuePriority,
)


def send_targeted_resume():
    """Send targeted resume message to agents 5-8 only."""
    print("🔄 **Targeted Resume Broadcast to Agents 5-8**")
    print("=" * 60)

    # Create message queue manager
    manager = MessageQueueManager()

    # Register the 8 agents
    agents = [
        {
            "id": "agent_1",
            "name": "Foundation & Testing Specialist",
            "capabilities": ["TASK_EXECUTION", "MONITORING"],
            "window_title": "Cursor - Agent_Cellphone_V2_Repository",
        },
        {
            "id": "agent_2",
            "name": "AI/ML Specialist",
            "capabilities": ["DECISION_MAKING", "DATA_PROCESSING"],
            "window_title": "Cursor - AI_ML_Project",
        },
        {
            "id": "agent_3",
            "name": "Web Development Specialist",
            "capabilities": ["TASK_EXECUTION", "COMMUNICATION"],
            "window_title": "Cursor - Web_Development_Project",
        },
        {
            "id": "agent_4",
            "name": "Multimedia & Gaming Specialist",
            "capabilities": ["DATA_PROCESSING", "MONITORING"],
            "window_title": "Cursor - Multimedia_Gaming_Project",
        },
        {
            "id": "agent_5",
            "name": "Security & Compliance Specialist",
            "capabilities": ["MONITORING", "REPORTING"],
            "window_title": "Cursor - Security_Compliance_Project",
        },
        {
            "id": "agent_6",
            "name": "Data & Analytics Specialist",
            "capabilities": ["DATA_PROCESSING", "DECISION_MAKING"],
            "window_title": "Cursor - Data_Analytics_Project",
        },
        {
            "id": "agent_7",
            "name": "Infrastructure & DevOps Specialist",
            "capabilities": ["TASK_EXECUTION", "MONITORING"],
            "window_title": "Cursor - Infrastructure_DevOps_Project",
        },
        {
            "id": "agent_8",
            "name": "Business Logic & Workflows Specialist",
            "capabilities": ["DECISION_MAKING", "COMMUNICATION"],
            "window_title": "Cursor - Business_Logic_Project",
        },
    ]

    print("Registering 8 agents...")
    for agent in agents:
        success = manager.register_agent(
            agent_id=agent["id"],
            agent_name=agent["name"],
            capabilities=agent["capabilities"],
            window_title=agent["window_title"],
        )

        status = "✅" if success else "❌"
        print(f"  {status} {agent['name']} ({agent['id']})")

    print(f"\nTotal agents registered: {len(manager.agent_registry)}")

    # Send targeted resume message to agents 5-8 only
    print("\n📢 **Sending Targeted Resume to Agents 5-8**")
    print("=" * 50)

    targeted_message = """🔄 TARGETED RESUME MESSAGE FOR AGENTS 5-8

URGENT: You did not receive the system resume broadcast
Status: NEED IMMEDIATE COORDINATION
Priority: CRITICAL

MISSING AGENTS STATUS:
❌ Agent-5 (Security & Compliance Specialist) - NO RESPONSE
❌ Agent-6 (Data & Analytics Specialist) - NO RESPONSE
❌ Agent-7 (Infrastructure & DevOps Specialist) - NO RESPONSE
❌ Agent-8 (Business Logic & Workflows Specialist) - NO RESPONSE

IMMEDIATE ACTIONS REQUIRED:

🔒 AGENT-5 (Security & Compliance Specialist):
• IMMEDIATELY acknowledge this message
• Report current security status
• Confirm auth module security
• Resume normal security protocols

📊 AGENT-6 (Data & Analytics Specialist):
• IMMEDIATELY acknowledge this message
• Report data system status
• Confirm no data breaches
• Resume normal analytics operations

🛡️ AGENT-7 (Infrastructure & DevOps Specialist):
• IMMEDIATELY acknowledge this message
• Report system infrastructure status
• Confirm system stability
• Resume normal monitoring

🔄 AGENT-8 (Business Logic & Workflows Specialist):
• IMMEDIATELY acknowledge this message
• Report workflow status
• Confirm business continuity
• Resume normal operations

⚠️ THIS IS A COORDINATION EMERGENCY ⚠️
🚨 AGENTS 5-8 MUST RESPOND IMMEDIATELY 🚨

End of Targeted Resume Message
Timestamp: IMMEDIATE
Priority: CRITICAL
Status: COORDINATION EMERGENCY
Response: IMMEDIATE REQUIRED"""

    # Send to agents 5-8 only
    target_agents = ["agent_5", "agent_6", "agent_7", "agent_8"]
    message_ids = []

    for agent_id in target_agents:
        message_id = manager.send_message(
            source_agent="[SYSTEM]",
            target_agent=agent_id,
            content=targeted_message,
            priority="critical",
        )
        if message_id:
            message_ids.append(message_id)
            print(f"✅ Resume message sent to {agent_id}")
        else:
            print(f"❌ Failed to send resume message to {agent_id}")

    print(f"\n📢 Targeted resume sent to {len(message_ids)} agents")
    print(f"🆔 Message IDs: {message_ids}")

    # Get system status
    print("\n📊 **System Status**")
    print("=" * 30)
    status = manager.get_system_status()
    print(f"Registered Agents: {status['registered_agents']}")

    # Cleanup
    print("\n🧹 Cleaning up...")
    manager.stop()
    print("Message queue system stopped.")

    return message_ids


if __name__ == "__main__":
    send_targeted_resume()
