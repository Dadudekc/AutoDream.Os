#!/usr/bin/env python3
"""Test script to send messages to all 8 agents using fixed routing"""

from v1_v2_message_queue_system import V1V2MessageQueueSystem

def test_all_agents():
    print("Testing fixed message routing to all 8 agents...")
    
    # Initialize system
    mq = V1V2MessageQueueSystem()
    print("System initialized")
    
    # Start system
    mq.start_system()
    print("System started")
    
    # Send messages to all 8 agents
    agents = ['agent_1', 'agent_2', 'agent_3', 'agent_4', 'agent_5', 'agent_6', 'agent_7', 'agent_8']
    messages = [
        'Agent-1: System initialization test - PyAutoGUI coordination active',
        'Agent-2: Standards compliance check - PyAutoGUI coordination active',
        'Agent-3: Integration testing - PyAutoGUI coordination active',
        'Agent-4: Performance monitoring - PyAutoGUI coordination active',
        'Agent-5: Security audit - PyAutoGUI coordination active',
        'Agent-6: Data validation - PyAutoGUI coordination active',
        'Agent-7: Network diagnostics - PyAutoGUI coordination active',
        'Agent-8: Backup verification - PyAutoGUI coordination active'
    ]
    
    msg_ids = []
    for i, (agent, msg) in enumerate(zip(agents, messages)):
        msg_id = mq.send_message('agent_5', agent, msg)
        msg_ids.append(msg_id)
        print(f"Message sent to {agent}: {msg_id}")
    
    print(f"All {len(msg_ids)} messages sent!")
    
    # Wait for processing
    import time
    print("Waiting for message processing...")
    time.sleep(5)
    
    # Check results
    print(f"Message history length: {len(mq.message_history)}")
    
    # Verify all messages have correct routing
    success_count = 0
    for i, wrapper in enumerate(mq.message_history[-8:]):  # Last 8 messages
        message = wrapper.get('message', {})
        sender = message.get('sender_agent')
        target = message.get('target_agent')
        content = message.get('content', '')
        
        if sender == 'agent_5' and target in agents and content:
            success_count += 1
            print(f"✅ {target}: Message routed correctly")
        else:
            print(f"❌ {target}: Routing issue - Sender: {sender}, Target: {target}")
    
    print(f"\n🎯 Results: {success_count}/{len(agents)} messages routed correctly")
    
    if success_count == len(agents):
        print("🎉 ALL MESSAGES ROUTED CORRECTLY! The fix is working perfectly!")
    else:
        print("⚠️ Some messages still have routing issues")
    
    # Stop system
    mq.stop_system()
    print("System stopped")

if __name__ == "__main__":
    test_all_agents()
