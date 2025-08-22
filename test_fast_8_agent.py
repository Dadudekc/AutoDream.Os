#!/usr/bin/env python3
"""
Fast 8-Agent Test - Verify All Agents Receive Messages
======================================================

This script tests the optimized messaging system to ensure
all 8 agents receive messages quickly and efficiently.
"""

import asyncio
from real_agent_communication_system_v2 import RealAgentCommunicationSystem

async def test_fast_8_agent():
    """Test fast messaging to all 8 agents"""
    print("🚀 FAST 8-AGENT MESSAGING TEST")
    print("="*50)
    
    # Initialize the system
    comm_system = RealAgentCommunicationSystem()
    
    # Display agent status
    print("📊 Current Agent Status:")
    for agent_id, info in comm_system.get_agent_status().items():
        coords = info['coordinates']
        print(f"  {agent_id}: ({coords['x']}, {coords['y']}) - {info['status']}")
    
    print(f"\n🎯 Total Agents Loaded: {len(comm_system.agent_coordinates)}")
    
    # Test 1: Quick single message to all agents
    print("\n🧪 Test 1: Quick broadcast to all 8 agents")
    print("Sending: 'Quick test message to all agents!'")
    
    start_time = asyncio.get_event_loop().time()
    
    try:
        success = await comm_system.send_message_to_all_agents(
            "Quick test message to all agents! 🚀",
            "input_box"
        )
        
        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time
        
        if success:
            print(f"✅ SUCCESS: All 8 agents received message in {duration:.2f} seconds!")
        else:
            print(f"⚠️ PARTIAL: Some agents may not have received the message")
        
        print(f"⏱️ Total time: {duration:.2f} seconds")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 2: Line break message to all agents
    print("\n🧪 Test 2: Line break broadcast to all 8 agents")
    print("Sending multi-line message with proper formatting")
    
    line_break_message = """🚀 SYSTEM UPDATE: Fast 8-Agent Messaging!

✅ All agents should receive this message
📊 With proper line breaks and formatting
🎯 In their isolated screen regions
⏱️ Much faster than before!"""
    
    start_time = asyncio.get_event_loop().time()
    
    try:
        success = await comm_system.send_message_to_all_agents_with_line_breaks(
            line_break_message,
            "workspace_box"
        )
        
        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time
        
        if success:
            print(f"✅ SUCCESS: All 8 agents received line break message in {duration:.2f} seconds!")
        else:
            print(f"⚠️ PARTIAL: Some agents may not have received the message")
        
        print(f"⏱️ Total time: {duration:.2f} seconds")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 3: Individual agent messaging
    print("\n🧪 Test 3: Individual agent messaging")
    
    test_agents = ["Agent-1", "Agent-5", "Agent-8"]
    for agent_id in test_agents:
        if agent_id in comm_system.agent_coordinates:
            print(f"  📤 Sending to {agent_id}...")
            try:
                success = await comm_system.send_message_to_agent(
                    agent_id, f"Individual test message for {agent_id}! 🎯", "status_box"
                )
                print(f"    {'✅ SUCCESS' if success else '❌ FAILED'}")
            except Exception as e:
                print(f"    ❌ ERROR: {e}")
        else:
            print(f"  ⚠️ {agent_id} not found in coordinates")
    
    # Final status
    print("\n🎯 Final System Status:")
    comm_system.display_agent_status()
    
    print("\n🎉 Fast 8-agent test complete!")
    print("📊 Check the logs above to verify all agents received messages")

if __name__ == "__main__":
    print("🚀 Starting Fast 8-Agent Test...")
    print("This will test optimized messaging to all 8 agents!")
    print("Make sure your applications are open at the target coordinates.\n")
    
    try:
        asyncio.run(test_fast_8_agent())
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")

