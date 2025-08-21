#!/usr/bin/env python3
"""
Coordinate Calibration Script for V2 Broadcast System
====================================================

This script helps you calibrate the coordinates for all 8 agents
so the broadcast system can properly send messages to all agents.

Usage:
1. Run this script
2. Move your mouse to each agent's chat window
3. Press Ctrl+C to capture the current position
4. Repeat for all 8 agents
5. The script will update the coordinates automatically
"""

import time
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.v1_v2_message_queue_system import MessageQueueManager, MessageQueuePriority
from core.shared_enums import AgentCapability

def calibrate_agent_coordinates():
    """Interactive coordinate calibration for all 8 agents"""
    
    print("🎯 **Agent Coordinate Calibration**")
    print("=" * 50)
    print("This script will help you calibrate coordinates for all 8 agents.")
    print("Move your mouse to each agent's chat window and press Ctrl+C to capture.")
    print()
    
    # Create message queue manager
    manager = MessageQueueManager()
    
    # Define the 8 agents
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
    print("🔧 Registering 8 agents...")
    for agent in agents:
        success = manager.register_agent(
            agent_id=agent["id"],
            agent_name=agent["name"],
            capabilities=agent["capabilities"],
            window_title=agent["window_title"]
        )
        
        status = "✅" if success else "❌"
        print(f"  {status} {agent['name']} ({agent['id']})")
    
    print(f"\nTotal agents registered: {len(manager.agent_registry)}")
    
    # Check current coordinate status
    print("\n📊 **Current Coordinate Status**")
    print("=" * 50)
    coord_status = manager.get_coordinate_status()
    
    for agent_id, status in coord_status.items():
        name = status.get("name", "Unknown")
        coords = status.get("coordinates")
        has_coords = status.get("has_coordinates", False)
        
        if has_coords and coords:
            print(f"  ✅ {name} ({agent_id}): {coords}")
        else:
            print(f"  ❌ {name} ({agent_id}): No coordinates")
    
    # Interactive calibration
    print("\n🎯 **Interactive Coordinate Calibration**")
    print("=" * 50)
    print("For each agent, move your mouse to their chat window and press Ctrl+C")
    print("The script will capture the current mouse position and update coordinates.")
    print()
    
    for agent in agents:
        agent_id = agent["id"]
        agent_name = agent["name"]
        
        print(f"📍 **Calibrating {agent_name} ({agent_id})**")
        print(f"   Move your mouse to the chat window for {agent_name}")
        print(f"   Press Ctrl+C when ready...")
        
        try:
            # Wait for user to position mouse
            input("   Press Enter when mouse is positioned...")
            
            # Get current mouse position
            coords = manager.get_current_mouse_position()
            
            if coords["x"] > 0 and coords["y"] > 0:
                # Calibrate coordinates
                success = manager.calibrate_coordinates(agent_id, coords["x"], coords["y"])
                
                if success:
                    print(f"   ✅ Coordinates updated: {coords}")
                else:
                    print(f"   ❌ Failed to update coordinates")
            else:
                print(f"   ❌ Invalid mouse position: {coords}")
                
        except KeyboardInterrupt:
            print(f"   ⏭️ Skipping {agent_name}")
        except Exception as e:
            print(f"   ❌ Error calibrating {agent_name}: {e}")
        
        print()
    
    # Final coordinate status
    print("📊 **Final Coordinate Status**")
    print("=" * 50)
    coord_status = manager.get_coordinate_status()
    
    successful_calibrations = 0
    for agent_id, status in coord_status.items():
        name = status.get("name", "Unknown")
        coords = status.get("coordinates")
        has_coords = status.get("has_coordinates", False)
        
        if has_coords and coords:
            print(f"  ✅ {name} ({agent_id}): {coords}")
            successful_calibrations += 1
        else:
            print(f"  ❌ {name} ({agent_id}): No coordinates")
    
    print(f"\n🎯 **Calibration Summary**")
    print(f"   Successfully calibrated: {successful_calibrations}/8 agents")
    
    if successful_calibrations == 8:
        print("   🎉 All agents calibrated! Broadcast system should work perfectly.")
    elif successful_calibrations >= 6:
        print("   ⚠️ Most agents calibrated. Broadcast system should work for most agents.")
    else:
        print("   ❌ Many agents need calibration. Broadcast system may not work properly.")
    
    # Test broadcast
    if successful_calibrations > 0:
        print(f"\n🧪 **Testing Broadcast System**")
        print("=" * 50)
        
        try:
            message_ids = manager.broadcast_message(
                source_agent="agent_1",
                content="🧪 TEST: This is a test broadcast message to verify coordinate calibration.",
                priority=MessageQueuePriority.NORMAL
            )
            
            print(f"✅ Test broadcast completed!")
            print(f"   Messages sent: {len(message_ids)}")
            print(f"   Expected: {successful_calibrations - 1} (excluding sender)")
            
        except Exception as e:
            print(f"❌ Test broadcast failed: {e}")
    
    return manager

if __name__ == "__main__":
    try:
        manager = calibrate_agent_coordinates()
        print("\n🎉 **Calibration Complete!**")
        print("The broadcast system should now work properly for all calibrated agents.")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Calibration interrupted by user")
    except Exception as e:
        print(f"\n❌ **Calibration failed: {e}**")
        import traceback
        traceback.print_exc()
