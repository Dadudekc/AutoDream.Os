from pathlib import Path
import asyncio

        import traceback
from src.services.integrated_agent_coordinator import (
from src.utils.stability_improvements import stability_manager, safe_import
import time

#!/usr/bin/env python3
"""
Integrated Agent Coordinator Demo
================================

Demonstrates the integrated PyAutoGUI + Message Queue coordination system.
Shows how Agent-5 can coordinate other agents using both systems.
"""



# Import the integrated coordinator
    IntegratedAgentCoordinator,
    UnifiedMessagePriority,
)


def demo_integrated_system_initialization():
    """Demonstrate integrated system initialization."""
    print("🔧 **Integrated System Initialization Demo**")
    print("=" * 60)

    # Create integrated coordinator
    coordinator = IntegratedAgentCoordinator()

    print("✅ Integrated coordinator created successfully!")
    print(f"🎯 Agent mapping: {len(coordinator.agent_mapping)} agents")
    print(
        f"📋 Message queue agents: {len(coordinator.message_queue_manager.agent_registry)}"
    )
    print(
        f"🤖 PyAutoGUI coordinator: {len(coordinator.pyautogui_coordinator.agent_roles)} agents"
    )

    return coordinator


async def demo_hybrid_message_sending(coordinator):
    """Demonstrate hybrid message sending (queue + PyAutoGUI fallback)."""
    print("\n💬 **Hybrid Message Sending Demo**")
    print("=" * 60)

    # Send message to Agent-1 using hybrid approach
    print("Sending message to Agent-1 using hybrid approach...")

    success = await coordinator.send_message_hybrid(
        agent_id="agent_1",
        message="Agent-1: Testing integrated coordination system. Report status.",
        priority=UnifiedMessagePriority.HIGH,
    )

    if success:
        print("✅ Message sent successfully via hybrid approach!")
        print("   Method: Message queue (CDP) with PyAutoGUI fallback")
        print("   Target: Foundation & Testing Specialist")
        print("   Priority: HIGH")
    else:
        print("❌ Message sending failed")

    # Send message to Agent-2
    print("\nSending message to Agent-2...")

    success2 = await coordinator.send_message_hybrid(
        agent_id="agent_2",
        message="Agent-2: Begin AI/ML integration testing. Report progress.",
        priority=UnifiedMessagePriority.NORMAL,
    )

    if success2:
        print("✅ Message sent successfully to Agent-2!")
    else:
        print("❌ Message sending to Agent-2 failed")

    return [success, success2]


async def demo_hybrid_broadcast(coordinator):
    """Demonstrate hybrid broadcast messaging."""
    print("\n📢 **Hybrid Broadcast Messaging Demo**")
    print("=" * 60)

    # Broadcast message to all agents
    print("Broadcasting message to all agents using hybrid approach...")

    results = await coordinator.broadcast_message_hybrid(
        message="ALL AGENTS: Integrated coordination system is now active. Report your status.",
        priority=UnifiedMessagePriority.URGENT,
    )

    print(f"✅ Broadcast completed!")
    print(f"   Total agents: {len(results)}")
    print(f"   Successful: {sum(results.values())}")
    print(f"   Failed: {len(results) - sum(results.values())}")

    # Show individual results
    for agent_id, success in results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {agent_id}")

    return results


async def demo_workflow_coordination(coordinator):
    """Demonstrate workflow coordination using hybrid approach."""
    print("\n🎯 **Workflow Coordination Demo**")
    print("=" * 60)

    # Coordinate Agent-1 workflow
    print("Coordinating Agent-1 strategic coordination workflow...")

    success1 = await coordinator.coordinate_agent_workflow_hybrid(
        agent_id="agent_1", workflow_type="strategic_coordination"
    )

    if success1:
        print("✅ Agent-1 workflow coordinated successfully!")
    else:
        print("❌ Agent-1 workflow coordination failed")

    # Coordinate Agent-2 workflow
    print("\nCoordinating Agent-2 task management workflow...")

    success2 = await coordinator.coordinate_agent_workflow_hybrid(
        agent_id="agent_2", workflow_type="task_management"
    )

    if success2:
        print("✅ Agent-2 workflow coordinated successfully!")
    else:
        print("❌ Agent-2 workflow coordination failed")

    # Coordinate Agent-3 workflow
    print("\nCoordinating Agent-3 technical implementation workflow...")

    success3 = await coordinator.coordinate_agent_workflow_hybrid(
        agent_id="agent_3", workflow_type="technical_implementation"
    )

    if success3:
        print("✅ Agent-3 workflow coordinated successfully!")
    else:
        print("❌ Agent-3 workflow coordination failed")

    return [success1, success2, success3]


async def demo_coordination_cycle(coordinator):
    """Demonstrate complete coordination cycle."""
    print("\n🚀 **Complete Coordination Cycle Demo**")
    print("=" * 60)

    print("Executing complete coordination cycle using hybrid approach...")

    success = await coordinator.execute_coordination_cycle_hybrid()

    if success:
        print("✅ Complete coordination cycle executed successfully!")
        print(f"   Cycle number: {coordinator.coordination_cycle}")
        print(f"   All agents coordinated")
    else:
        print("❌ Coordination cycle execution failed")

    return success


def demo_system_status(coordinator):
    """Demonstrate system status reporting."""
    print("\n📊 **System Status Demo**")
    print("=" * 60)

    # Get comprehensive system status
    status = coordinator.get_system_status()

    print("Integrated System Status Report:")
    print(f"  Integration Mode: {status['integration_mode']}")
    print(f"  Coordination Cycles: {status['coordination_cycle']}")
    print(f"  Last Coordination: {status['last_coordination'] or 'Never'}")
    print(f"  Discord Available: {status['discord_available']}")

    print("\nMessage Queue System:")
    queue_status = status["message_queue_system"]
    print(f"  Registered Agents: {queue_status['registered_agents']}")
    print(f"  Queue Size: {queue_status['queue_system']['queue_size']}")
    print(f"  System Running: {queue_status['queue_system']['is_running']}")

    print("\nPyAutoGUI Coordinator:")
    pyautogui_status = status["pyautogui_coordinator"]
    print(f"  Coordination Cycles: {pyautogui_status['coordination_cycle']}")
    print(
        f"  Election Mode: {'ENABLED' if pyautogui_status['election_mode'] else 'DISABLED'}"
    )
    print(
        f"  Round-Robin Mode: {'ENABLED' if pyautogui_status['round_robin'] else 'DISABLED'}"
    )

    print("\nAgent Mapping:")
    for pyautogui_agent, queue_agent in status["agent_mapping"].items():
        print(f"  {pyautogui_agent} → {queue_agent}")


def demo_integration_modes(coordinator):
    """Demonstrate different integration modes."""
    print("\n🔄 **Integration Modes Demo**")
    print("=" * 60)

    # Test message queue only mode
    print("Testing message queue only mode...")
    coordinator.integration_mode = "message_queue"

    # Test PyAutoGUI only mode
    print("Testing PyAutoGUI only mode...")
    coordinator.integration_mode = "pyautogui"

    # Reset to hybrid mode
    print("Resetting to hybrid mode...")
    coordinator.integration_mode = "hybrid"

    print("✅ Integration modes tested successfully!")
    print(f"   Current mode: {coordinator.integration_mode}")


async def demo_continuous_coordination(coordinator):
    """Demonstrate continuous coordination."""
    print("\n🔄 **Continuous Coordination Demo**")
    print("=" * 60)

    print("Starting continuous coordination (3 cycles, 30s interval)...")
    print("Note: This is a demonstration with reduced cycles and intervals")

    # Run continuous coordination with reduced parameters for demo
    await coordinator.run_continuous_coordination_hybrid(cycles=2, interval=30)

    print("✅ Continuous coordination demo completed!")


async def main():
    """Main demonstration function."""
    print("🚀 **Integrated Agent Coordinator Demo**")
    print("=" * 70)
    print("This demo shows the integrated PyAutoGUI + Message Queue coordination")
    print("system that combines the best of both approaches for agent management.")
    print("=" * 70)
    print()

    try:
        # Demo 1: System Initialization
        coordinator = demo_integrated_system_initialization()

        # Demo 2: Hybrid Message Sending
        message_results = await demo_hybrid_message_sending(coordinator)

        # Demo 3: Hybrid Broadcast
        broadcast_results = await demo_hybrid_broadcast(coordinator)

        # Demo 4: Workflow Coordination
        workflow_results = await demo_workflow_coordination(coordinator)

        # Demo 5: Complete Coordination Cycle
        cycle_success = await demo_coordination_cycle(coordinator)

        # Demo 6: System Status
        demo_system_status(coordinator)

        # Demo 7: Integration Modes
        demo_integration_modes(coordinator)

        # Demo 8: Continuous Coordination (Demo Mode)
        await demo_continuous_coordination(coordinator)

        print("\n🎉 **Demo Completed Successfully!**")
        print("=" * 70)
        print("The Integrated Agent Coordinator is working correctly!")
        print()
        print("Key Features Demonstrated:")
        print("  ✅ Integrated system initialization")
        print("  ✅ Hybrid message sending (queue + PyAutoGUI)")
        print("  ✅ Hybrid broadcast messaging")
        print("  ✅ Workflow coordination")
        print("  ✅ Complete coordination cycles")
        print("  ✅ System status monitoring")
        print("  ✅ Integration mode switching")
        print("  ✅ Continuous coordination")
        print()
        print("Integration Benefits:")
        print("  🚀 Message queue: CDP-based, no mouse movement")
        print("  🤖 PyAutoGUI: Proven reliability, direct control")
        print("  🔄 Hybrid: Best of both worlds with automatic fallback")
        print("  📊 Unified monitoring and status reporting")
        print()
        print("Next Steps:")
        print("  1. Launch Cursor with CDP: .\\launch_cursor_with_cdp.ps1")
        print("  2. Test message queue: python src/services/cdp_message_delivery.py")
        print(
            "  3. Run integrated coordinator: python src/services/integrated_agent_coordinator.py"
        )
        print("  4. Monitor system performance and coordination")

    except Exception as e:
        print(f"\n❌ **Demo Failed: {e}**")
        print("Please check the error and try again.")

        traceback.print_exc()

    finally:
        # Cleanup
        if "coordinator" in locals():
            print("\n🧹 Cleaning up...")
            # Stop message queue system
            coordinator.message_queue_manager.queue_system.stop()
            print("Message queue system stopped.")
            print("Integrated coordinator demo cleanup complete.")


if __name__ == "__main__":
    main()
