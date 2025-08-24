#!/usr/bin/env python3
"""
Non-Interactive Agent Setup Script
==================================

This script automatically sets up all 8 agents with their default coordinates
for testing and development purposes. No user interaction required.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.v1_v2_message_queue_system import MessageQueueManager
from core.shared_enums import AgentCapability

def setup_agents_automatically():
    """Automatically register all 8 agents with default coordinates"""
    
    print("🤖 " + "="*50)
    print("   AUTOMATIC 8-AGENT SETUP")
    print("="*54)
    print()
    
    # Create message queue manager
    print("🔧 Initializing MessageQueueManager...")
    manager = MessageQueueManager()
    print("✅ MessageQueueManager initialized")
    print()
    
    # Define the 8 agents with their default coordinates
    agents = [
        {
            "id": "agent_1",
            "name": "Foundation & Testing Specialist",
            "capabilities": [AgentCapability.TASK_EXECUTION, AgentCapability.MONITORING],
            "window_title": "Cursor - Agent_Cellphone_V2_Repository"
        },
        {
            "id": "agent_2", 
            "name": "AI/ML Specialist",
            "capabilities": [AgentCapability.DECISION_MAKING, AgentCapability.DATA_PROCESSING],
            "window_title": "Cursor - AI_ML_Project"
        },
        {
            "id": "agent_3",
            "name": "Web Development Specialist", 
            "capabilities": [AgentCapability.TASK_EXECUTION, AgentCapability.COMMUNICATION],
            "window_title": "Cursor - Web_Development_Project"
        },
        {
            "id": "agent_4",
            "name": "Multimedia & Gaming Specialist",
            "capabilities": [AgentCapability.DATA_PROCESSING, AgentCapability.MONITORING], 
            "window_title": "Cursor - Multimedia_Gaming_Project"
        },
        {
            "id": "agent_5",
            "name": "Security & Compliance Specialist",
            "capabilities": [AgentCapability.MONITORING, AgentCapability.REPORTING],
            "window_title": "Cursor - Security_Compliance_Project" 
        },
        {
            "id": "agent_6",
            "name": "Data & Analytics Specialist",
            "capabilities": [AgentCapability.DATA_PROCESSING, AgentCapability.DECISION_MAKING],
            "window_title": "Cursor - Data_Analytics_Project"
        },
        {
            "id": "agent_7", 
            "name": "Infrastructure & DevOps Specialist",
            "capabilities": [AgentCapability.TASK_EXECUTION, AgentCapability.MONITORING],
            "window_title": "Cursor - Infrastructure_DevOps_Project"
        },
        {
            "id": "agent_8",
            "name": "Business Logic & Workflows Specialist", 
            "capabilities": [AgentCapability.DECISION_MAKING, AgentCapability.COMMUNICATION],
            "window_title": "Cursor - Business_Logic_Project"
        }
    ]
    
    # Register all agents
    print("📝 Registering 8 agents with default coordinates...")
    successful_registrations = 0
    
    for agent in agents:
        try:
            success = manager.register_agent(
                agent_id=agent["id"],
                agent_name=agent["name"],
                capabilities=agent["capabilities"],
                window_title=agent["window_title"]
            )
            
            if success:
                status = "✅"
                successful_registrations += 1
            else:
                status = "❌"
                
            print(f"  {status} {agent['name']} ({agent['id']})")
            
        except Exception as e:
            print(f"  ❌ {agent['name']} ({agent['id']}) - Error: {e}")
    
    print(f"\n📊 Registration Summary:")
    print(f"   Successfully registered: {successful_registrations}/8 agents")
    print()
    
    # Check coordinate status
    print("🎯 Checking coordinate status...")
    try:
        coord_status = manager.get_coordinate_status()
        
        valid_coords = 0
        for agent_id, status in coord_status.items():
            name = status.get("name", "Unknown")
            coords = status.get("coordinates")
            has_coords = status.get("has_coordinates", False)
            
            if has_coords and coords:
                print(f"  ✅ {name} ({agent_id}): {coords}")
                valid_coords += 1
            else:
                print(f"  ❌ {name} ({agent_id}): No coordinates")
        
        print(f"\n🎯 Final Status:")
        print(f"   Agents with coordinates: {valid_coords}/8")
        
        if valid_coords == 8:
            print("   🎉 All agents ready! Broadcast system operational.")
        elif valid_coords >= 6:
            print("   ⚠️ Most agents ready. System partially operational.")
        else:
            print("   ❌ System needs coordinate calibration.")
            print("   💡 Run: python3 calibrate_coordinates.py")
            
    except Exception as e:
        print(f"❌ Coordinate status check failed: {e}")
    
    print()
    
    # Cleanup
    try:
        if hasattr(manager.queue_system, 'stop_system'):
            manager.queue_system.stop_system()
        else:
            manager.queue_system.is_running = False
        print("🧹 System cleanup completed")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")
    
    return manager, successful_registrations, valid_coords

if __name__ == "__main__":
    try:
        print("🚀 Starting automatic agent setup...")
        print()
        
        manager, registrations, coordinates = setup_agents_automatically()
        
        print("\n" + "="*54)
        print("🎯 SETUP COMPLETE!")
        print(f"   Registered agents: {registrations}/8")
        print(f"   Valid coordinates: {coordinates}/8")
        
        if coordinates >= 6:
            print("   Status: ✅ READY FOR OPERATION")
        else:
            print("   Status: ⚠️ NEEDS CALIBRATION")
            
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()