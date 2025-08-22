#!/usr/bin/env python3
"""
IMPROVED AGENT RESUME BROADCAST SCRIPT
Enhanced broadcast system using improved message templates for better agent coordination
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.improved_resume_message_template import ImprovedResumeMessageTemplate
from services.v1_v2_message_queue_system import MessageQueueManager, MessageQueuePriority

def main():
    """Send improved resume broadcast using enhanced message templates"""
    
    # Initialize the message queue manager
    manager = MessageQueueManager()
    
    # Register the 8 agents with enhanced capabilities
    agents = [
        {
            'id': 'agent_1', 
            'name': 'Foundation & Testing Specialist', 
            'capabilities': ['TASK_EXECUTION', 'MONITORING', 'TESTING', 'QUALITY_ASSURANCE'], 
            'window_title': 'Cursor - Agent_Cellphone_V2_Repository'
        },
        {
            'id': 'agent_2', 
            'name': 'AI/ML Specialist', 
            'capabilities': ['DECISION_MAKING', 'DATA_PROCESSING', 'AI_DEVELOPMENT', 'ML_OPTIMIZATION'], 
            'window_title': 'Cursor - AI_ML_Project'
        },
        {
            'id': 'agent_3', 
            'name': 'Web Development Specialist', 
            'capabilities': ['TASK_EXECUTION', 'COMMUNICATION', 'WEB_DEVELOPMENT', 'UI_UX'], 
            'window_title': 'Cursor - Web_Development_Project'
        },
        {
            'id': 'agent_4', 
            'name': 'Multimedia & Gaming Specialist', 
            'capabilities': ['DATA_PROCESSING', 'MONITORING', 'MULTIMEDIA', 'GAMING_DEVELOPMENT'], 
            'window_title': 'Cursor - Multimedia_Gaming_Project'
        },
        {
            'id': 'agent_5', 
            'name': 'Security & Compliance Specialist', 
            'capabilities': ['MONITORING', 'REPORTING', 'SECURITY', 'COMPLIANCE', 'COORDINATION'], 
            'window_title': 'Cursor - Security_Project'
        },
        {
            'id': 'agent_6', 
            'name': 'Data & Analytics Specialist', 
            'capabilities': ['DATA_PROCESSING', 'ANALYSIS', 'DATA_SCIENCE', 'BUSINESS_INTELLIGENCE'], 
            'window_title': 'Cursor - Data_Analytics_Project'
        },
        {
            'id': 'agent_7', 
            'name': 'Infrastructure & DevOps Specialist', 
            'capabilities': ['INFRASTRUCTURE', 'DEPLOYMENT', 'DEVOPS', 'SYSTEM_ADMINISTRATION'], 
            'window_title': 'Cursor - Infrastructure_Project'
        },
        {
            'id': 'agent_8', 
            'name': 'Business Logic & Workflows Specialist', 
            'capabilities': ['WORKFLOW_DESIGN', 'BUSINESS_LOGIC', 'PROCESS_OPTIMIZATION', 'AUTOMATION'], 
            'window_title': 'Cursor - Business_Logic_Project'
        }
    ]
    
    # Register all agents with enhanced capabilities
    print("🚀 Registering enhanced agents...")
    for agent in agents:
        success = manager.register_agent(
            agent['id'], 
            agent['name'], 
            agent['capabilities'], 
            agent['window_title']
        )
        if success:
            print(f"✅ {agent['name']} registered with enhanced capabilities")
        else:
            print(f"❌ Failed to register {agent['name']}")
    
    print(f"\n📊 Total agents registered: {len(manager.agent_registry)}")
    
    # Get coordinate status
    coord_status = manager.get_coordinate_status()
    print("\n📍 Agent Coordinate Status:")
    for agent_id, status in coord_status.items():
        name = status.get('name', 'Unknown')
        coords = status.get('coordinates', 'None')
        has_coords = status.get('has_coordinates', False)
        print(f"  {agent_id}: {name} - Coordinates: {coords} - Valid: {has_coords}")
    
    # Initialize the improved message template
    template = ImprovedResumeMessageTemplate()
    
    # Choose message type based on system status
    print("\n🎯 Selecting appropriate resume message type...")
    
    # For now, use standard resume message (can be enhanced with logic)
    resume_message = template.get_standard_resume_message()
    message_type = "STANDARD_RESUME"
    
    print(f"✅ Selected message type: {message_type}")
    
    # Send the improved broadcast message to all agents
    print("\n📢 Sending IMPROVED AGENT RESUME OPERATIONS broadcast...")
    message_ids = manager.broadcast_message(
        source_agent="agent_7",
        content=resume_message,
        priority="high",
        metadata={
            "type": "enhanced_coordination",
            "priority": "high",
            "action_required": "immediate",
            "captain": "agent_5",
            "message_template": message_type,
            "enhanced_features": True
        }
    )
    
    print(f"✅ Enhanced broadcast sent successfully! {len(message_ids)} message IDs generated")
    
    # Get system status
    system_status = manager.get_system_status()
    print(f"\n📊 Enhanced System Status:")
    print(f"  Registered Agents: {system_status.get('registered_agents', 0)}")
    print(f"  Queue Status: {system_status.get('queue_system', {})}")
    print(f"  Message Type: {message_type}")
    print(f"  Enhanced Features: Enabled")
    
    # Display message statistics
    print(f"\n📈 Message Statistics:")
    print(f"  Total Characters: {len(resume_message)}")
    print(f"  Total Lines: {len(resume_message.split(chr(10)))}")
    print(f"  Emoji Count: {resume_message.count('🚀') + resume_message.count('🎯') + resume_message.count('✅')}")
    print(f"  Action Items: {resume_message.count('•')}")
    
    # Cleanup
    print("\n🧹 Cleaning up enhanced broadcast system...")
    manager.stop()
    print("✅ Enhanced message queue system stopped successfully")
    
    print(f"\n🎉 IMPROVED RESUME BROADCAST COMPLETED SUCCESSFULLY!")
    print(f"   Message Type: {message_type}")
    print(f"   Enhanced Features: ✅ ENABLED")
    print(f"   Agent Engagement: 🚀 OPTIMIZED")
    print(f"   Coordination Protocol: 📋 ENHANCED")

if __name__ == "__main__":
    main()
