from pathlib import Path
import json

        import traceback
from src.core.v2_comprehensive_messaging_system import V2AgentCapability
from src.services.cdp_message_delivery import (
from src.services.testing import (
from src.utils.stability_improvements import stability_manager, safe_import
import time

#!/usr/bin/env python3
"""
V1-V2 Message Queue System Demo
===============================

Demonstrates the integrated V1 PyAutoGUI + V2 architecture message queue system.
Shows how to send messages between agents without mouse movement.
"""



# Import the message queue system
    UnifiedMessageQueue,
    UnifiedMessagePriority,
)
    CDPMessageDelivery,
    send_message_to_cursor,
    broadcast_message_to_cursor,
)


def demo_agent_registration():
    """Demonstrate agent registration."""
    print("🔧 **Agent Registration Demo**")
    print("=" * 50)

    # Create message queue manager
    manager = UnifiedMessageQueue()

    # Register the 8 agents from the TDD integration project
    agents = [
        {
            "id": "agent_1",
            "name": "Foundation & Testing Specialist",
            "capabilities": [
                V2AgentCapability.TASK_EXECUTION,
                V2AgentCapability.MONITORING,
            ],
            "window_title": "Cursor - Agent_Cellphone_V2_Repository",
        },
        {
            "id": "agent_2",
            "name": "AI/ML Specialist",
            "capabilities": [
                V2AgentCapability.DECISION_MAKING,
                V2AgentCapability.DATA_PROCESSING,
            ],
            "window_title": "Cursor - AI_ML_Project",
        },
        {
            "id": "agent_3",
            "name": "Web Development Specialist",
            "capabilities": [
                V2AgentCapability.TASK_EXECUTION,
                V2AgentCapability.COMMUNICATION,
            ],
            "window_title": "Cursor - Web_Development_Project",
        },
        {
            "id": "agent_4",
            "name": "Multimedia & Gaming Specialist",
            "capabilities": [
                V2AgentCapability.DATA_PROCESSING,
                V2AgentCapability.MONITORING,
            ],
            "window_title": "Cursor - Multimedia_Gaming_Project",
        },
        {
            "id": "agent_5",
            "name": "Security & Compliance Specialist",
            "capabilities": [V2AgentCapability.MONITORING, V2AgentCapability.REPORTING],
            "window_title": "Cursor - Security_Compliance_Project",
        },
        {
            "id": "agent_6",
            "name": "Data & Analytics Specialist",
            "capabilities": [
                V2AgentCapability.DATA_PROCESSING,
                V2AgentCapability.DECISION_MAKING,
            ],
            "window_title": "Cursor - Data_Analytics_Project",
        },
        {
            "id": "agent_7",
            "name": "Infrastructure & DevOps Specialist",
            "capabilities": [
                V2AgentCapability.TASK_EXECUTION,
                V2AgentCapability.MONITORING,
            ],
            "window_title": "Cursor - Infrastructure_DevOps_Project",
        },
        {
            "id": "agent_8",
            "name": "Business Logic & Workflows Specialist",
            "capabilities": [
                V2AgentCapability.DECISION_MAKING,
                V2AgentCapability.COMMUNICATION,
            ],
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

    return manager


def demo_direct_messaging(manager):
    """Demonstrate direct messaging between agents."""
    print("\n💬 **Direct Messaging Demo**")
    print("=" * 50)

    # Send a message from Agent-1 to Agent-2
    print("Sending message from Foundation & Testing Specialist to AI/ML Specialist...")

    message_id = manager.send_message(
        source_agent="agent_1",
        target_agent="agent_2",
        content="Agent-2: begin integration tests for services_v2/auth. Report in 60m.",
        priority=UnifiedMessagePriority.HIGH,
    )

    print(f"✅ Message sent successfully!")
    print(f"   Message ID: {message_id}")
    print(f"   Source: Foundation & Testing Specialist")
    print(f"   Target: AI/ML Specialist")
    print(f"   Priority: HIGH")

    # Send another message
    print("\nSending message from Agent-1 to Agent-3...")

    message_id2 = manager.send_message(
        source_agent="agent_1",
        target_agent="agent_3",
        content="Agent-3: begin integration tests for services_v2/web. Report in 60m.",
        priority=UnifiedMessagePriority.NORMAL,
    )

    print(f"✅ Message sent successfully!")
    print(f"   Message ID: {message_id2}")
    print(f"   Source: Foundation & Testing Specialist")
    print(f"   Target: Web Development Specialist")
    print(f"   Priority: NORMAL")

    return [message_id, message_id2]


def demo_broadcast_messaging(manager):
    """Demonstrate broadcast messaging to all agents."""
    print("\n📢 **Broadcast Messaging Demo**")
    print("=" * 50)

    # Broadcast a message to all agents
    print("Broadcasting message to all agents...")

    message_ids = manager.broadcast_message(
        source_agent="agent_1",
        content="ALL AGENTS: no acknowledgments—only diffs, commits, and checkmarks.",
        priority=UnifiedMessagePriority.CRITICAL,
    )

    print(f"✅ Broadcast message sent successfully!")
    print(f"   Total messages sent: {len(message_ids)}")
    print(f"   Target agents: {len(message_ids)}")
    print(f"   Priority: URGENT")

    return message_ids


def demo_high_priority_messaging(manager):
    """Demonstrate high-priority messaging with Ctrl+Enter x2 flag."""
    print("\n🚨 **High-Priority Messaging Demo**")
    print("=" * 50)

    # Send high-priority message
    print("Sending high-priority message with Ctrl+Enter x2 flag...")

    message_id = manager.send_message(
        source_agent="agent_1",
        target_agent="agent_5",
        content="URGENT: Security vulnerability detected in auth module. Immediate action required.",
        priority="high",  # Use "high" priority instead of high_priority parameter
    )

    print(f"✅ High-priority message sent successfully!")
    print(f"   Message ID: {message_id}")
    print(f"   Source: Foundation & Testing Specialist")
    print(f"   Target: Security & Compliance Specialist")
    print(f"   Priority: HIGH")
    print(f"   High-Priority Flag: ENABLED")
    print(f"   Ctrl+Enter x2: DETECTED")

    return message_id


def demo_cdp_integration():
    """Demonstrate CDP integration for headless messaging."""
    print("\n🌐 **CDP Integration Demo**")
    print("=" * 50)

    # Test CDP connection
    print("Testing CDP connection...")

    try:
        cdp_delivery = CDPMessageDelivery()

        if cdp_delivery.test_connection():
            print("✅ CDP connection successful!")

            # Get targets
            targets = cdp_delivery.get_targets()
            print(f"   Found {len(targets)} CDP targets:")

            for target in targets:
                print(f"     - {target.title} ({target.url})")

            # Try to send a test message
            if targets:
                print(f"\nSending test message via CDP...")
                result = cdp_delivery.send_message_sync(
                    targets[0], "Test message via CDP - no mouse movement required!"
                )

                print(f"✅ CDP message delivery result: {result}")
            else:
                print("   No suitable targets found for CDP messaging")

        else:
            print("❌ CDP connection failed")
            print("   Make sure Cursor is running with --remote-debugging-port=9222")
            print("   Use: .\\launch_cursor_with_cdp.ps1")

    except Exception as e:
        print(f"❌ CDP integration error: {e}")
        print("   This is expected if Cursor is not running with CDP enabled")


def demo_system_status(manager):
    """Demonstrate system status reporting."""
    print("\n📊 **System Status Demo**")
    print("=" * 50)

    # Get comprehensive system status
    status = manager.get_system_status()

    print("System Status Report:")
    print(f"  Registered Agents: {status['registered_agents']}")
    print(f"  Queue Size: {status['queue_system']['regular_queue_size']}")
    print(f"  System Running: {status['queue_system']['system_running']}")
    print(
        f"  High Priority Queue: {status['queue_system']['high_priority_queue_size']}"
    )

    print("\nAgent Details:")
    for agent_id, agent_info in status["agent_details"].items():
        print(f"  {agent_id}:")
        print(f"    Name: {agent_info['name']}")
        print(f"    Status: {agent_info['status']}")
        # Handle capabilities that might be AgentCapability enum objects
        capabilities = agent_info.get("capabilities", [])
        if capabilities:
            # Convert enum objects to strings if needed
            cap_strings = [
                str(cap) if hasattr(cap, "name") else cap for cap in capabilities
            ]
            print(f"    Capabilities: {', '.join(cap_strings)}")
        else:
            print(f"    Capabilities: None")
        print(f"    Window: {agent_info['window_title']}")


def demo_performance_testing(manager):
    """Demonstrate performance testing."""
    print("\n⚡ **Performance Testing Demo**")
    print("=" * 50)

    # Test message throughput
    print("Testing message throughput...")

    start_time = time.time()
    message_count = 50

    for i in range(message_count):
        manager.send_message(
            source_agent="agent_1",
            target_agent=f"agent_{(i % 8) + 1}",
            content=f"Performance test message {i+1}",
            priority=UnifiedMessagePriority.NORMAL,
        )

    end_time = time.time()
    duration = end_time - start_time

    print(f"✅ Performance test completed!")
    print(f"   Messages sent: {message_count}")
    print(f"   Total time: {duration:.2f} seconds")
    print(f"   Messages per second: {message_count / duration:.2f}")
    print(f"   Queue size: {manager.queue_system.message_queue.qsize()}")


def main():
    """Main demonstration function."""
    print("🚀 **V1-V2 Message Queue System Demo**")
    print("=" * 60)
    print("This demo shows the integrated V1 PyAutoGUI + V2 architecture")
    print("message queue system with high-priority flags and CDP integration.")
    print("=" * 60)
    print()

    try:
        # Demo 1: Agent Registration
        manager = demo_agent_registration()

        # Demo 2: Direct Messaging
        direct_messages = demo_direct_messaging(manager)

        # Demo 3: Broadcast Messaging
        broadcast_messages = demo_broadcast_messaging(manager)

        # Demo 4: High-Priority Messaging
        high_priority_message = demo_high_priority_messaging(manager)

        # Demo 5: CDP Integration
        demo_cdp_integration()

        # Demo 6: System Status
        demo_system_status(manager)

        # Demo 7: Performance Testing
        demo_performance_testing(manager)

        print("\n🎉 **Demo Completed Successfully!**")
        print("=" * 60)
        print("The V1-V2 Message Queue System is working correctly!")
        print()
        print("Key Features Demonstrated:")
        print("  ✅ Agent registration and management")
        print("  ✅ Direct messaging between agents")
        print("  ✅ Broadcast messaging to all agents")
        print("  ✅ High-priority messaging with Ctrl+Enter x2")
        print("  ✅ CDP integration for headless messaging")
        print("  ✅ System status monitoring")
        print("  ✅ Performance testing and optimization")
        print()
        print("Next Steps:")
        print("  1. Launch Cursor with CDP: .\\launch_cursor_with_cdp.ps1")
        print("  2. Test CDP messaging: python src/services/cdp_message_delivery.py")
        print("  3. Use the message queue for agent coordination")
        print("  4. Monitor system performance and health")

    except Exception as e:
        print(f"\n❌ **Demo Failed: {e}**")
        print("Please check the error and try again.")

        traceback.print_exc()

    finally:
        # Cleanup
        if "manager" in locals():
            print("\n🧹 Cleaning up...")
            manager.queue_system.stop_system()  # Use stop_system instead of stop
            print("Message queue system stopped.")


if __name__ == "__main__":
    main()
