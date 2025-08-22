#!/usr/bin/env python3
"""
8-Agent Setup Script - Configure and test all 8 agents
"""

from src.services.v1_v2_message_queue_system import MessageQueueManager, MessageQueuePriority
import time

def setup_8_agents():
    """Set up and test all 8 agents with proper configuration."""
    print("🚀 **8-AGENT SYSTEM SETUP** 🚀")
    print("=" * 60)
    
    # Create message queue manager with 8-agent config
    manager = MessageQueueManager()
    
    # Define all 8 agents with their roles and capabilities
    agents = [
        {
            "id": "agent_1",
            "name": "Foundation & Testing Specialist",
            "role": "Core system testing, foundation validation, and quality assurance",
            "capabilities": ["TASK_EXECUTION", "MONITORING", "TESTING", "VALIDATION"],
            "window_title": "Cursor - Agent_Cellphone_V2_Repository"
        },
        {
            "id": "agent_2", 
            "name": "AI/ML Specialist",
            "role": "Machine learning, AI integration, and intelligent automation",
            "capabilities": ["AI_ML", "AUTOMATION", "INTELLIGENCE", "LEARNING"],
            "window_title": "Cursor - AI/ML Projects"
        },
        {
            "id": "agent_3",
            "name": "Web Development Specialist", 
            "role": "Web applications, frontend/backend development, and web services",
            "capabilities": ["WEB_DEV", "FRONTEND", "BACKEND", "APIS"],
            "window_title": "Cursor - Web Development"
        },
        {
            "id": "agent_4",
            "name": "Multimedia & Gaming Specialist",
            "role": "Game development, multimedia content, and interactive experiences",
            "capabilities": ["GAMING", "MULTIMEDIA", "INTERACTIVE", "CONTENT"],
            "window_title": "Cursor - Gaming & Multimedia"
        },
        {
            "id": "agent_5",
            "name": "Security & Compliance Specialist",
            "role": "Security protocols, compliance, and threat protection",
            "capabilities": ["SECURITY", "COMPLIANCE", "THREAT_PROTECTION", "AUDITING"],
            "window_title": "Cursor - Security & Compliance"
        },
        {
            "id": "agent_6",
            "name": "Data & Analytics Specialist",
            "role": "Data processing, analytics, and business intelligence",
            "capabilities": ["DATA_ANALYTICS", "BI", "PROCESSING", "VISUALIZATION"],
            "window_title": "Cursor - Data & Analytics"
        },
        {
            "id": "agent_7",
            "name": "Infrastructure & DevOps Specialist",
            "role": "System infrastructure, deployment, and operational excellence",
            "capabilities": ["INFRASTRUCTURE", "DEVOPS", "DEPLOYMENT", "OPERATIONS"],
            "window_title": "Cursor - Infrastructure & DevOps"
        },
        {
            "id": "agent_8",
            "name": "Business Logic & Workflows Specialist",
            "role": "Business processes, workflow automation, and system integration",
            "capabilities": ["BUSINESS_LOGIC", "WORKFLOWS", "INTEGRATION", "PROCESSES"],
            "window_title": "Cursor - Business Logic & Workflows"
        }
    ]
    
    print(f"📋 Registering {len(agents)} agents...")
    
    # Register all agents using correct method signature
    for agent in agents:
        try:
            manager.register_agent(
                agent_id=agent["id"],
                agent_name=agent["name"],
                capabilities=agent["capabilities"],
                window_title=agent["window_title"]
            )
            print(f"✅ {agent['id']}: {agent['name']} - REGISTERED")
        except Exception as e:
            print(f"❌ {agent['id']}: {agent['name']} - FAILED: {e}")
    
    print(f"\n🎯 **AGENT REGISTRATION COMPLETE** 🎯")
    print(f"Total agents registered: {len(manager.agent_registry)}")
    
    # Test direct messaging between agents
    print(f"\n📨 **TESTING DIRECT MESSAGING** 📨")
    test_direct_messaging(manager)
    
    # Test broadcast messaging to all agents
    print(f"\n📢 **TESTING BROADCAST MESSAGING** 📢")
    test_broadcast_messaging(manager)
    
    # Test high-priority messaging
    print(f"\n🚨 **TESTING HIGH-PRIORITY MESSAGING** 🚨")
    test_high_priority_messaging(manager)
    
    # Display system status
    print(f"\n📊 **SYSTEM STATUS** 📊")
    display_system_status(manager)
    
    # Cleanup
    print(f"\n🧹 **CLEANUP** 🧹")
    manager.stop()
    print("✅ 8-Agent system setup completed successfully!")

def test_direct_messaging(manager):
    """Test direct messaging between agents."""
    print("Testing direct messaging from Agent-1 to Agent-5...")
    
    try:
        # Send high-priority message
        message_id = manager.send_message(
            source_agent="agent_1",
            target_agent="agent_5", 
            content="🔒 Security check required - Agent-1 to Agent-5",
            priority="high"
        )
        print(f"✅ High-priority message sent: {message_id}")
        
        # Send normal message
        message_id = manager.send_message(
            source_agent="agent_1",
            target_agent="agent_5",
            content="📋 Regular status update - Agent-1 to Agent-5",
            priority="normal"
        )
        print(f"✅ Normal message sent: {message_id}")
        
    except Exception as e:
        print(f"❌ Direct messaging test failed: {e}")

def test_broadcast_messaging(manager):
    """Test broadcast messaging to all agents."""
    print("Testing broadcast message to all agents...")
    
    try:
        # Send broadcast message
        message_id = manager.broadcast_message(
            source_agent="agent_1",
            content="📢 SYSTEM BROADCAST: All agents report status and confirm coordination",
            priority="normal"
        )
        print(f"✅ Broadcast message sent: {message_id}")
        
        # Wait for processing
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Broadcast messaging test failed: {e}")

def test_high_priority_messaging(manager):
    """Test high-priority messaging system."""
    print("Testing high-priority messaging...")
    
    try:
        # Send urgent message
        message_id = manager.send_message(
            source_agent="agent_5",
            target_agent="agent_1",
            content="🚨 URGENT: Security protocol validation required immediately",
            priority="urgent"
        )
        print(f"✅ Urgent message sent: {message_id}")
        
        # Wait for processing
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ High-priority messaging test failed: {e}")

def display_system_status(manager):
    """Display current system status."""
    print(f"Active agents: {len(manager.agent_registry)}")
    print(f"Queue system: {'ACTIVE' if manager.queue_system.is_running else 'INACTIVE'}")
    print(f"Message persistence: {'ENABLED' if manager.queue_system.config.get('message_persistence') else 'DISABLED'}")
    
    # Show agent details
    for agent_id, agent_info in manager.agent_registry.items():
        status = agent_info.get('status', 'unknown')
        print(f"  {agent_id}: {status}")

if __name__ == "__main__":
    setup_8_agents()
