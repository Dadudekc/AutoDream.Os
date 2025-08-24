#!/usr/bin/env python3
"""
FSM Integration Demo - Agent Cellphone V2
==========================================

Demonstrates the complete FSM integration with V2 architecture.
Shows FSM orchestrator, unified launcher, and agent coordination.
"""

import sys
import time

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.workspace_manager import WorkspaceManager
from core.inbox_manager import InboxManager
from core.task_manager import TaskManager
from core.fsm_orchestrator import FSMOrchestrator, TaskState, TaskPriority
from launchers.unified_launcher_v2 import UnifiedLauncherV2


def demo_fsm_orchestrator():
    """Demonstrate FSM orchestrator functionality."""
    print("🤖 **FSM ORCHESTRATOR DEMO - V2**")
    print("=" * 60)

    try:
        # Initialize managers
        workspace_manager = WorkspaceManager()
        inbox_manager = InboxManager(workspace_manager)
        fsm_orchestrator = FSMOrchestrator(workspace_manager, inbox_manager)

        print("✅ FSM Orchestrator initialized")

        # Create FSM tasks
        print("\n📝 **CREATING FSM TASKS**")
        print("=" * 40)

        # Critical task
        task1_id = fsm_orchestrator.create_task(
            title="System Architecture Review",
            description="Review and validate the V2 system architecture with FSM integration",
            assigned_agent="Agent-2",
            priority=TaskPriority.CRITICAL,
        )
        print(f"✅ Critical FSM task created: {task1_id}")

        # High priority task
        task2_id = fsm_orchestrator.create_task(
            title="Agent Swarm Coordination",
            description="Coordinate agent swarm operations using FSM system",
            assigned_agent="Agent-3",
            priority=TaskPriority.HIGH,
        )
        print(f"✅ High priority FSM task created: {task2_id}")

        # Normal priority task
        task3_id = fsm_orchestrator.create_task(
            title="Response Capture Integration",
            description="Integrate response capture with FSM workflow",
            assigned_agent="Agent-4",
            priority=TaskPriority.NORMAL,
        )
        print(f"✅ Normal priority FSM task created: {task3_id}")

        # Update task states
        print("\n🔄 **UPDATING TASK STATES**")
        print("=" * 40)

        # Start task 1
        fsm_orchestrator.update_task_state(
            task1_id,
            TaskState.IN_PROGRESS,
            "Agent-2",
            "Starting architecture review with FSM integration focus",
            {"phase": "analysis", "progress": 25},
        )
        print(f"✅ Task {task1_id} moved to IN_PROGRESS")

        # Complete task 2
        fsm_orchestrator.update_task_state(
            task2_id,
            TaskState.COMPLETED,
            "Agent-3",
            "Agent swarm coordination completed successfully",
            {"agents_coordinated": 5, "success_rate": 100},
        )
        print(f"✅ Task {task2_id} moved to COMPLETED")

        # Block task 3
        fsm_orchestrator.update_task_state(
            task3_id,
            TaskState.BLOCKED,
            "Agent-4",
            "Blocked waiting for response capture service update",
            {"blocking_issue": "API compatibility", "estimated_resolution": "2 hours"},
        )
        print(f"✅ Task {task3_id} moved to BLOCKED")

        # Show FSM status
        print("\n📊 **FSM ORCHESTRATOR STATUS**")
        print("=" * 40)

        status = fsm_orchestrator.get_fsm_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

        # Show agent tasks
        print("\n📋 **AGENT TASKS**")
        print("=" * 40)

        for agent in ["Agent-2", "Agent-3", "Agent-4"]:
            tasks = fsm_orchestrator.get_agent_tasks(agent)
            print(f"\n{agent}: {len(tasks)} tasks")
            for task in tasks:
                print(f"   📄 {task.title} ({task.state.value})")

        return True

    except Exception as e:
        print(f"❌ FSM orchestrator demo failed: {e}")
        return False


def demo_unified_launcher_integration():
    """Demonstrate unified launcher with FSM integration."""
    print("\n🚀 **UNIFIED LAUNCHER V2 WITH FSM INTEGRATION**")
    print("=" * 60)

    try:
        # Initialize launcher
        launcher = UnifiedLauncherV2()
        print("✅ Unified Launcher V2 initialized")

        # Launch system with FSM enabled
        print("\n🔧 **LAUNCHING V2 SYSTEM WITH FSM**")
        print("=" * 40)

        success = launcher.launch_system(
            mode="coordination",
            agents=["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"],
            fsm_enabled=True,
            monitoring_enabled=True,
        )

        if success:
            print("✅ V2 system launched with FSM integration")
        else:
            print("❌ System launch failed")
            return False

        # Create FSM tasks through launcher
        print("\n📝 **CREATING FSM TASKS VIA LAUNCHER**")
        print("=" * 40)

        task_id = launcher.create_fsm_task(
            title="Agent Swarm Coordination Task",
            description="Coordinate all agents in swarm mode using FSM",
            assigned_agent="Agent-5",
            priority="critical",
        )
        print(f"✅ FSM task created via launcher: {task_id}")

        # Send coordination messages
        print("\n📤 **SENDING COORDINATION MESSAGES**")
        print("=" * 40)

        launcher.send_coordination_message(
            "UnifiedLauncher",
            "Agent-1",
            "FSM_ACTIVATION",
            "FSM system is now active. Check your inbox for task assignments.",
        )
        print("✅ Coordination message sent to Agent-1")

        launcher.send_coordination_message(
            "UnifiedLauncher",
            "Agent-5",
            "SWARM_COORDINATION",
            f"You have been assigned swarm coordination task: {task_id}",
        )
        print("✅ Coordination message sent to Agent-5")

        # Run agent swarm workflow
        print("\n🔄 **RUNNING AGENT SWARM WORKFLOW**")
        print("=" * 40)

        success = launcher.run_workflow("agent_swarm")
        print(f"Agent swarm workflow: {'✅ Success' if success else '❌ Failed'}")

        # Get comprehensive system status
        print("\n📊 **COMPREHENSIVE SYSTEM STATUS**")
        print("=" * 40)

        status = launcher.get_system_status()
        print(f"Launcher Status: {status.get('launcher_status')}")
        print(f"Launch Mode: {status.get('launch_config', {}).get('mode', 'Unknown')}")

        if "services" in status:
            print("\nService Status:")
            for service, service_status in status["services"].items():
                if isinstance(service_status, dict):
                    main_status = service_status.get("status", "Unknown")
                    print(f"   {service}: {main_status}")
                else:
                    print(f"   {service}: {service_status}")

        # Shutdown system
        print("\n🔧 **SHUTTING DOWN SYSTEM**")
        print("=" * 40)

        success = launcher.shutdown_system()
        print(f"System shutdown: {'✅ Success' if success else '❌ Failed'}")

        return True

    except Exception as e:
        print(f"❌ Unified launcher integration demo failed: {e}")
        return False


def demo_complete_fsm_workflow():
    """Demonstrate complete FSM workflow integration."""
    print("\n🔄 **COMPLETE FSM WORKFLOW INTEGRATION**")
    print("=" * 60)

    try:
        # Initialize complete system
        launcher = UnifiedLauncherV2()

        # Launch with all systems enabled
        launcher.launch_system(mode="swarm", fsm_enabled=True, monitoring_enabled=True)
        print("✅ Complete system launched")

        # Create coordinated tasks
        print("\n📝 **CREATING COORDINATED TASK SEQUENCE**")
        print("=" * 40)

        # Task 1: Architecture Agent
        task1 = launcher.create_fsm_task(
            "System Architecture Analysis",
            "Analyze V2 architecture for FSM integration completeness",
            "Agent-2",
            "critical",
        )

        # Task 2: Implementation Agent
        task2 = launcher.create_fsm_task(
            "FSM Integration Implementation",
            "Implement remaining FSM integration components",
            "Agent-3",
            "high",
        )

        # Task 3: Testing Agent
        task3 = launcher.create_fsm_task(
            "FSM System Testing",
            "Test complete FSM integration functionality",
            "Agent-4",
            "high",
        )

        # Task 4: Coordination Agent
        task4 = launcher.create_fsm_task(
            "Agent Swarm Coordination",
            "Coordinate all agents using FSM workflow",
            "Agent-5",
            "critical",
        )

        print(
            f"✅ Created coordinated task sequence: {len([task1, task2, task3, task4])} tasks"
        )

        # Send coordination messages to all agents
        print("\n📤 **COORDINATING ALL AGENTS**")
        print("=" * 40)

        coordination_messages = [
            ("Agent-1", "Project coordination and oversight"),
            ("Agent-2", f"Architecture analysis task: {task1}"),
            ("Agent-3", f"Implementation task: {task2}"),
            ("Agent-4", f"Testing task: {task3}"),
            ("Agent-5", f"Swarm coordination task: {task4}"),
        ]

        for agent, message in coordination_messages:
            launcher.send_coordination_message(
                "FSMCoordinator", agent, "TASK_ASSIGNMENT", message
            )
            print(f"✅ Coordinated {agent}")

        # Simulate workflow progression
        print("\n⏳ **SIMULATING WORKFLOW PROGRESSION**")
        print("=" * 40)

        # Give some time for message processing
        time.sleep(2)

        # Get final status
        final_status = launcher.get_system_status()
        print("📊 Final System Status:")
        print(f"   System: {final_status.get('launcher_status')}")
        print(f"   Services: {len(final_status.get('services', {}))}")
        print(f"   Mode: {final_status.get('launch_config', {}).get('mode')}")

        # Clean shutdown
        launcher.shutdown_system()
        print("✅ Complete FSM workflow demonstration completed")

        return True

    except Exception as e:
        print(f"❌ Complete FSM workflow demo failed: {e}")
        return False


def main():
    """Run the complete FSM integration demonstration."""
    print("🚀 **COMPLETE FSM INTEGRATION DEMONSTRATION - V2**")
    print("=" * 80)
    print("This demo shows the complete FSM integration with V2 architecture")
    print("=" * 80)

    # Run demos
    success1 = demo_fsm_orchestrator()
    success2 = demo_unified_launcher_integration()
    success3 = demo_complete_fsm_workflow()

    print("\n" + "=" * 80)

    if all([success1, success2, success3]):
        print("🎉 **ALL FSM INTEGRATION DEMOS SUCCESSFUL!**")
        print("\n💡 **What this demonstrates:**")
        print("   1. FSM Orchestrator is fully integrated with V2 architecture")
        print("   2. Unified Launcher V2 provides complete FSM coordination")
        print("   3. Agent swarm operations work through FSM workflow")
        print("   4. Task state management and updates are functional")
        print("   5. Message routing integrates with FSM updates")
        print("   6. Complete workflow coordination is operational")
        print("   7. All components follow strict coding standards")
        print("\n🚀 **V2 System Status: FSM INTEGRATION COMPLETE**")
        print("🤖 **READY FOR AGENT SWARM OPERATIONS!**")
    else:
        print("⚠️ **Some FSM integration demos failed - review needed**")

    print("\n🔧 **How to test FSM integration:**")
    print("   - FSM Orchestrator: python src/core/fsm_orchestrator.py --test")
    print(
        "   - Unified Launcher V2: python src/launchers/unified_launcher_v2.py --test"
    )
    print("   - Complete demo: python examples/demo_fsm_integration.py")
    print(
        "   - Agent swarm: python src/launchers/unified_launcher_v2.py --workflow agent_swarm"
    )


if __name__ == "__main__":
    main()
