#!/usr/bin/env python3
"""
Test Line Breaks in Autonomous Development System
================================================

This script tests the new line break handling functionality
that respects Shift+Enter for line breaks within messages.
"""

import asyncio
from autonomous_development_system import RealAgentCommunicationSystem, TaskManager

async def test_line_breaks():
    """Test line break handling in messages"""
    print("🧪 Testing Line Break Functionality")
    print("="*50)
    
    # Initialize the system
    comm_system = RealAgentCommunicationSystem()
    task_manager = TaskManager(comm_system)
    
    # Test message with multiple line breaks
    test_message = """🎯 TASK UPDATE: Repository Cleanup

📋 Current Status:
   • Progress: 75% Complete
   • Current Phase: Code optimization
   • Next Steps: Performance testing

🚀 Ready for next phase!
⏰ Estimated completion: 2 hours

This message demonstrates proper line break handling using Shift+Enter!"""
    
    print("📝 Test Message:")
    print(test_message)
    print("\n" + "="*50)
    
    # Test sending to a specific agent with line breaks
    print("📤 Testing single agent message with line breaks...")
    try:
        success = await comm_system.send_message_to_agent_with_line_breaks(
            "Agent-1", test_message, "workspace_box"
        )
        if success:
            print("✅ Successfully sent message with line breaks to Agent-1")
        else:
            print("❌ Failed to send message with line breaks")
    except Exception as e:
        print(f"❌ Error testing line breaks: {e}")
    
    print("\n" + "="*50)
    
    # Test broadcast with line breaks
    print("📢 Testing broadcast message with line breaks...")
    try:
        success = await comm_system.send_message_to_all_agents_with_line_breaks(
            "🚀 SYSTEM UPDATE: Line break functionality is now operational!\n\nAll messages will now properly handle line breaks using Shift+Enter.\n\nThis enables better formatting and readability for agent communications.",
            "status_box"
        )
        if success:
            print("✅ Successfully broadcasted message with line breaks to all agents")
        else:
            print("❌ Failed to broadcast message with line breaks")
    except Exception as e:
        print(f"❌ Error testing broadcast line breaks: {e}")
    
    print("\n" + "="*50)
    print("🎉 Line break testing complete!")
    print("\n📊 What was tested:")
    print("   • Single agent message with line breaks")
    print("   • Broadcast message with line breaks")
    print("   • Shift+Enter handling for proper formatting")
    print("   • Message delivery to isolated agent regions")

if __name__ == "__main__":
    print("🚀 Starting Line Break Test...")
    print("This will test the new Shift+Enter line break functionality!")
    print("Make sure your applications are open at the target coordinates.\n")
    
    try:
        asyncio.run(test_line_breaks())
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
