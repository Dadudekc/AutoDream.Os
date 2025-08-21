#!/usr/bin/env python3
"""
V1-V2 Message Queue System Demo
===============================

Demonstrates the integrated message queue system that combines:
- V1's proven PyAutoGUI approach
- V2's scalable architecture
- High-priority flag system (Ctrl+Enter x2)
- Message queuing for multiple agents
"""

import time
import threading
from pathlib import Path
import sys

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent))

from v1_v2_message_queue_system import (
    V1V2MessageQueueSystem,
    MessagePriority,
    send_high_priority_message,
    send_normal_message
)

def demo_basic_messaging():
    """Demonstrate basic message queuing and delivery"""
    print("🎯 Demo 1: Basic Message Queuing")
    print("=" * 50)
    
    # Create message queue system
    mq_system = V1V2MessageQueueSystem(max_workers=2)
    
    try:
        # Queue several messages
        messages = [
            ("Agent-1", "Agent-3", "Hello Agent-3! How are you today?"),
            ("Agent-2", "Agent-4", "Agent-4, please check the security protocols."),
            ("Agent-5", "Agent-1", "Agent-1, status update needed."),
            ("Agent-3", "Agent-2", "Agent-2, I need help with the AI integration."),
        ]
        
        print("📨 Queuing messages...")
        for sender, recipient, content in messages:
            msg_id = send_normal_message(mq_system, sender, recipient, content)
            print(f"   ✅ {sender} → {recipient}: {msg_id}")
        
        # Wait for processing
        print("\n⏳ Waiting for messages to be processed...")
        time.sleep(3)
        
        # Show status
        status = mq_system.get_queue_status()
        print(f"\n📊 Status Report:")
        print(f"   Queue Size: {status['queue_size']}")
        print(f"   Messages Delivered: {status['messages_delivered']}")
        print(f"   Messages Failed: {status['messages_failed']}")
        print(f"   Active Workers: {status['active_workers']}")
        
    finally:
        mq_system.shutdown()

def demo_priority_messaging():
    """Demonstrate priority-based message delivery"""
    print("\n🎯 Demo 2: Priority-Based Message Delivery")
    print("=" * 50)
    
    mq_system = V1V2MessageQueueSystem(max_workers=3)
    
    try:
        # Queue messages with different priorities
        print("📨 Queuing priority messages...")
        
        # Low priority
        msg_id1 = mq_system.queue_message(
            "Agent-1", "Agent-3", 
            "This is a low priority message for later review.",
            priority=MessagePriority.LOW
        )
        print(f"   🔵 LOW: {msg_id1}")
        
        # Normal priority
        msg_id2 = send_normal_message(
            mq_system, "Agent-2", "Agent-4",
            "This is a normal priority message for standard processing."
        )
        print(f"   🟢 NORMAL: {msg_id2}")
        
        # High priority
        msg_id3 = mq_system.queue_message(
            "Agent-5", "Agent-1",
            "This is a high priority message that needs attention soon.",
            priority=MessagePriority.HIGH
        )
        print(f"   🟡 HIGH: {msg_id3}")
        
        # Urgent priority
        msg_id4 = mq_system.queue_message(
            "Agent-3", "Agent-2",
            "This is an urgent message that requires immediate action!",
            priority=MessagePriority.URGENT
        )
        print(f"   🟠 URGENT: {msg_id4}")
        
        # Critical priority
        msg_id5 = mq_system.queue_message(
            "Agent-4", "Agent-5",
            "CRITICAL: System failure detected! Immediate intervention required!",
            priority=MessagePriority.CRITICAL
        )
        print(f"   🔴 CRITICAL: {msg_id5}")
        
        # Wait for processing
        print("\n⏳ Waiting for priority messages to be processed...")
        time.sleep(4)
        
        # Show status
        status = mq_system.get_queue_status()
        print(f"\n📊 Priority Processing Results:")
        print(f"   Messages Delivered: {status['messages_delivered']}")
        print(f"   Average Delivery Time: {status['average_delivery_time']:.2f}s")
        
    finally:
        mq_system.shutdown()

def demo_high_priority_flags():
    """Demonstrate the high-priority flag system with Ctrl+Enter x2"""
    print("\n🎯 Demo 3: High-Priority Flag System (Ctrl+Enter x2)")
    print("=" * 50)
    
    mq_system = V1V2MessageQueueSystem(max_workers=2)
    
    try:
        print("🚨 Testing high-priority flag system...")
        
        # Normal message without flag
        msg_id1 = send_normal_message(
            mq_system, "Agent-1", "Agent-3",
            "This is a normal message that will use standard Enter key delivery."
        )
        print(f"   📨 Normal: {msg_id1}")
        
        # High-priority message with Ctrl+Enter x2 flag
        msg_id2 = send_high_priority_message(
            mq_system, "Agent-5", "Agent-3",
            "URGENT: This message uses the Ctrl+Enter x2 high-priority delivery method!"
        )
        print(f"   🚨 High-Priority: {msg_id2}")
        
        # Another high-priority message
        msg_id3 = send_high_priority_message(
            mq_system, "Agent-2", "Agent-4",
            "CRITICAL ALERT: System requires immediate attention using Ctrl+Enter x2!"
        )
        print(f"   🚨 High-Priority: {msg_id3}")
        
        # Wait for processing
        print("\n⏳ Waiting for high-priority messages to be processed...")
        time.sleep(3)
        
        # Show status
        status = mq_system.get_queue_status()
        print(f"\n📊 High-Priority Processing Results:")
        print(f"   Messages Delivered: {status['messages_delivered']}")
        print(f"   Messages Failed: {status['messages_failed']}")
        
    finally:
        mq_system.shutdown()

def demo_multi_agent_coordination():
    """Demonstrate multi-agent coordination through the message queue"""
    print("\n🎯 Demo 4: Multi-Agent Coordination")
    print("=" * 50)
    
    mq_system = V1V2MessageQueueSystem(max_workers=4)
    
    try:
        print("🤝 Coordinating multiple agents...")
        
        # Simulate a coordinated workflow
        workflow_messages = [
            # Phase 1: Task assignment
            ("Agent-5", "Agent-1", "TASK: Begin strategic planning for Q4"),
            ("Agent-5", "Agent-2", "TASK: Prepare resource allocation analysis"),
            ("Agent-5", "Agent-3", "TASK: Start technical implementation planning"),
            ("Agent-5", "Agent-4", "TASK: Review security protocols"),
            
            # Phase 2: Status updates
            ("Agent-1", "Agent-5", "STATUS: Strategic planning 25% complete"),
            ("Agent-2", "Agent-5", "STATUS: Resource analysis in progress"),
            ("Agent-3", "Agent-5", "STATUS: Technical planning 40% complete"),
            ("Agent-4", "Agent-5", "STATUS: Security review completed"),
            
            # Phase 3: Coordination
            ("Agent-1", "Agent-2", "COORDINATION: Need resource estimates for strategic plan"),
            ("Agent-2", "Agent-3", "COORDINATION: Resource allocation ready for technical planning"),
            ("Agent-3", "Agent-4", "COORDINATION: Technical plan needs security validation"),
            ("Agent-4", "Agent-1", "COORDINATION: Security protocols approved for strategic plan"),
        ]
        
        # Queue all workflow messages
        for sender, recipient, content in workflow_messages:
            msg_id = mq_system.queue_message(
                sender, recipient, content,
                priority=MessagePriority.NORMAL
            )
            print(f"   ✅ {sender} → {recipient}: {msg_id}")
        
        # Wait for processing
        print("\n⏳ Processing coordinated workflow...")
        time.sleep(5)
        
        # Show final status
        status = mq_system.get_queue_status()
        print(f"\n📊 Coordination Results:")
        print(f"   Total Messages: {status['messages_queued']}")
        print(f"   Successfully Delivered: {status['messages_delivered']}")
        print(f"   Failed Deliveries: {status['messages_failed']}")
        print(f"   Agent Status: {len(status['agent_status'])} agents active")
        
        # Show agent status details
        if status['agent_status']:
            print(f"\n👥 Agent Status Details:")
            for agent_id, agent_info in status['agent_status'].items():
                print(f"   {agent_id}: {agent_info['messages_received']} messages received")
        
    finally:
        mq_system.shutdown()

def demo_error_handling_and_retries():
    """Demonstrate error handling and retry mechanisms"""
    print("\n🎯 Demo 5: Error Handling and Retry Mechanisms")
    print("=" * 50)
    
    mq_system = V1V2MessageQueueSystem(max_workers=2)
    
    try:
        print("🔄 Testing error handling and retry logic...")
        
        # Queue messages that might fail (e.g., to non-existent agents)
        test_messages = [
            ("Agent-1", "Agent-99", "This message will fail - agent doesn't exist"),
            ("Agent-2", "Agent-3", "This message should succeed"),
            ("Agent-3", "Agent-99", "Another message to non-existent agent"),
            ("Agent-4", "Agent-1", "This message should also succeed"),
        ]
        
        for sender, recipient, content in test_messages:
            msg_id = mq_system.queue_message(
                sender, recipient, content,
                priority=MessagePriority.NORMAL
            )
            print(f"   📨 {sender} → {recipient}: {msg_id}")
        
        # Wait for processing with retries
        print("\n⏳ Processing messages with retry logic...")
        time.sleep(6)
        
        # Show status including failed messages
        status = mq_system.get_queue_status()
        print(f"\n📊 Error Handling Results:")
        print(f"   Messages Delivered: {status['messages_delivered']}")
        print(f"   Messages Failed: {status['messages_failed']}")
        print(f"   Queue Size: {status['queue_size']}")
        
        # Show failed messages if any
        if mq_system.failed_messages:
            print(f"\n❌ Failed Messages:")
            for msg_id, failure_info in mq_system.failed_messages.items():
                msg = failure_info['message']
                print(f"   {msg_id}: {msg.sender} → {msg.recipient} - {failure_info['failure_reason']}")
        
    finally:
        mq_system.shutdown()

def main():
    """Run all demos"""
    print("🚀 V1-V2 Message Queue System Demo Suite")
    print("=" * 60)
    print("This demo shows the integrated message queue system that combines:")
    print("• V1's proven PyAutoGUI approach")
    print("• V2's scalable architecture") 
    print("• High-priority flag system (Ctrl+Enter x2)")
    print("• Message queuing for multiple agents")
    print("• Priority-based delivery")
    print("• Error handling and retries")
    print("=" * 60)
    
    try:
        # Run all demos
        demo_basic_messaging()
        demo_priority_messaging()
        demo_high_priority_flags()
        demo_multi_agent_coordination()
        demo_error_handling_and_retries()
        
        print("\n🎉 All demos completed successfully!")
        print("\n💡 Key Features Demonstrated:")
        print("   ✅ Message queuing system")
        print("   ✅ Priority-based delivery")
        print("   ✅ High-priority flag (Ctrl+Enter x2)")
        print("   ✅ Multi-agent coordination")
        print("   ✅ Error handling and retries")
        print("   ✅ V1 PyAutoGUI integration")
        print("   ✅ V2 architecture compatibility")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
